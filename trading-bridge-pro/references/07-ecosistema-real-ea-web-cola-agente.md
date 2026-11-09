# 07 · Ecosistema real: EA ↔ web ↔ dashboard/app y cola de backtests

Método extraído de un sistema real en producción (EA Connector, panel de cuentas, servidor central de trabajos, agente en el PC del usuario y app Android). Está **generalizado**: dominios, claves y rutas son marcadores. Úsalo como mapa de qué piezas hay, qué contrato tienen entre sí y qué fallos ya se vieron.

## A. Dos familias de datos que comparten backend
```
FAMILIA 1 · Monitor de cuentas reales
 MT5 → EA Connector (timer 1 s)
   ├─ cada ~10 s  POST <API>/dd/sync        (form-urlencoded; respuesta en TEXTO "OK\nclave=valor")
   │     envía: estado + posiciones abiertas + cola de eventos de alerta
   │     recibe: configuración de límites (rev + t_* por operación, a_* por cuenta)
   └─ cada ~1 h (o 30 s tras un cierre forzado) POST <SITIO>/upload-trades   (historial TXT con ';')
 Web (WordPress) → GET <API>/dd/state , /trades ; POST /dd/config , /dd/ack
 Dashboard (iframe) y App (WebView + notificaciones locales) leen del servidor, nunca de la cuenta.

FAMILIA 2 · Cola de backtests
 Dashboard / App / plugin SQX → REST del sitio → servidor central (Node, tras proxy HTTPS)
 PC del usuario: agente (bridge.exe) con long-poll SALIENTE → SQX (API local) + MT5 dedicado (Strategy Tester)
 Resultados ligeros suben; los informes pesados se quedan en el PC y se piden en vivo (kind=fetchReport).
```
Reglas de diseño que se repiten: el agente **inicia** siempre la conexión; el servidor guarda estado, el cliente lo pinta; lo pesado no viaja por defecto; la identidad del usuario es la del sitio web.

## B. Contrato EA → web (patrón reutilizable)
- Petición: `application/x-www-form-urlencoded`. Campos: clave de API, número y nombre de cuenta, balance, equity, divisa, versión del EA, permiso de cerrar, `positions` (líneas `ticket|symbol|type|volume|profit|swap|commission|open_ts|magic|comment`, máx. 300), `cfg_rev` (revisión de configuración que el EA ya aplicó) y `events` (líneas `eid|type|ticket|symbol|pct|money|limTxt|action|result|msg|ts`).
- Respuesta en **texto simple**: primera línea `OK`, luego `clave=valor` (`rev`, `t_en`, `t_mode` pct|money, `t_limit`, `t_act` alert|close, y lo mismo con `a_`). Es fácil de parsear en MQL5 (no hace falta un JSON parser).
- Éxito = HTTP 200 **y** cuerpo que empieza por `OK`. Todo lo demás = fallo.
- `eid` único por evento (`tipo_ticket_epoch_secuencia`): base de la **idempotencia**; el servidor debe deduplicar por `eid`.
- Tipos de evento: `trade_alert`, `account_alert`, `trade_closed`, `account_closed`, `close_failed`.
- Saneado de textos: separadores (`|`, `;`) y saltos de línea fuera de los campos.
- `rev`/`applied`: el panel compara la revisión guardada con la que el EA confirmó para mostrar "Aplicada en el EA".
- Dos claves por EA (una cuenta compartida entre dos usuarios): un POST por clave, configuración separada, y para cerrar se aplica el límite más estricto.

### Historial (TXT con `;`)
Cabeceras `#ACCOUNT_NAME` y `#BALANCE`, y una fila por operación: id de posición, símbolo, volumen, Long/Short, precio y hora de apertura, precio y hora de cierre, comisión, swap, profit, SL, TP, magic, comentario. Los movimientos de cuenta (BALANCE, CREDIT, CHARGE, CORRECTION, BONUS, COMMISSION, DIVIDEND, INTEREST) van con otro formato y **no son operaciones**. Tipo de operación y comentario se toman del deal de **entrada**.

## C. Lógica de alertas de drawdown del EA
- Cada 1 s: primero cada operación contra su límite (de mayor a menor pérdida), después la cuenta. Lo urgente va antes que el envío.
- Operación: `pérdida = -(profit + swap)`; límite en % del balance actual o en dinero. Cuenta: `dd = max(0, balance − equity)`.
- Acción `alert`: un evento y marca de enviada, con **rearme por histéresis** (vuelve a armarse al bajar del 90 % del límite). Acción `close`: cierra la operación (o todas, de la que más pierde a la que menos), reintento mínimo de 5 s, un solo `close_failed` por operación, desviación máxima configurable.
- Con el permiso de cierre ausente (algorítmico, MQL, cuenta) se informa `close_failed`.
- Caché de configuración en disco: tras reiniciar usa el último límite conocido aunque la web esté caída.
- **Limitación importante:** este DD es flotante contra el balance de ese momento. No incluye DD diario ni trailing; por sí solo **no sirve para reglas de prop firm** (ver `06`).

## D. Cola central de trabajos
- Estados `queued → claimed → done | error`; carriles (`lane`) por tipo: `backtest` y `metadata`; un trabajo a la vez por carril y por agente, FIFO.
- El agente hace **long-poll saliente** (≈25 s). Progreso por `POST /progress` (en memoria); resultado por `POST /result`.
- Tres niveles de clave independientes: por agente (solo ve y resuelve lo suyo), de "submitter" (encola y consulta) y de administración (altas, estadísticas, purga).
- Limpieza horaria: `done/error` de más de 48 h se borran; `claimed` de más de 8 h pasan a `error`. Al arrancar el agente avisa (`reset`) y se abandonan sus `claimed` anteriores.
- **Cancelación cooperativa:** si el servidor responde 404 al progreso, el agente entiende que el trabajo se borró y para los bucles largos.
- Resultado pesado (informes) solo en memoria, no se persiste.
- Reintento: lo decide el cliente creando otro trabajo; el servidor no re-encola.

## E. Agente en el PC del usuario
- No abre puertos. Error de red → reintento a los 10 s. `postResult` reintenta 6 veces con espera creciente para cubrir reinicios del servidor, y **separa el éxito del trabajo del éxito del aviso** (antes un fallo de aviso convertía un backtest bueno en error).
- Fases: export → compile → test (con fracción y fecha simulada) → compare. Actualización de histórico: update → export → import → retest.
- **No es un servicio de Windows:** un servicio (LocalSystem) no encuentra el perfil del usuario ni puede lanzar MT5 (sesión 0). Se usan dos tareas programadas: una al iniciar sesión y un **vigilante cada 5 min**, ambas con un lanzador oculto idempotente (comprueba el proceso antes de arrancar).
- Instalador: detiene tareas y mata el proceso viejo **antes** de copiar, escribe la configuración (modo central solo si hay credenciales), crea las tareas y arranca. El login de MT5 nunca se automatiza ni se pide. La versión del cliente y la del instalador deben sincronizarse (mejor automatizarlo).
- Despliegue del servidor: scripts autocontenidos que reescriben los archivos y reinician el servicio **sin tocar claves ni datos**, con copia `.bak` con fecha. No hay rollback automático.

## F. Seguridad observada (mecanismos)
- EA→web: clave en el cuerpo (no en cabecera), URL en la lista blanca de WebRequest, HTTPS.
- Dashboard: sesión del sitio + nonce. App: JWT en almacenamiento cifrado, caducidad leída del token, 401/403 fuerzan cierre de sesión con aviso único, sin copias de seguridad ni tráfico en claro. Si un plugin JWT intercepta `Authorization: Basic`, pasar a Bearer.
- Rol obligatorio en la fachada REST (`forbidden_role`).
- Servidor central: tres claves Bearer; recomendado HTTPS con proxy inverso y no exponer el puerto de la aplicación.

## G. Bugs reales ya corregidos (no los repitas)
1. Guardar resultados pesados en el JSON de trabajos lo hizo crecer a >300 MB y colgó el servidor → solo memoria.
2. Guardar el progreso cada 2 s con escritura síncrona bloqueaba Node → progreso solo en memoria.
3. Trabajos `claimed` eternos tras caída del agente → limpieza a las 8 h y `reset` al arrancar.
4. Resultado correcto perdido si el servidor reiniciaba → reintentos con backoff.
5. Borrar un trabajo no detenía una importación de horas → 404 como cancelación.
6. Drawdown del backtest recortado dio 723 % por partir el pico de 0 → usar balance real de referencia.
7. El parser del informe HTML leía la tabla de **Órdenes** en vez de **Transacciones** → profits absurdos.
8. Envíos duplicados a la cola (varias pestañas, recargas, lote anterior aún `queued`) → cerrojo en `localStorage` y **leer la cola real antes de encolar**; mirar también `queued/claimed`, no solo `done`.
9. Token caducado dejaba la app vacía → cierre de sesión con motivo y notificación única.
10. Historial vacío tras fallo de red porque `init()` solo corría una vez → refrescar al volver a primer plano.
11. Reinstalar dejaba vivo el proceso antiguo → `taskkill` antes de copiar; el arranque de una tarea con `schtasks /Run` lo mataba → arrancar con el lanzador.
12. Tipo Long/Short invertido al tomarlo del deal de salida → tomar el de entrada.

## H. Revisión final
Antes de dar por buena una herramienta parecida, pasa la lista de  4-checklist-de-fallos.md y revisa: cierres parciales agrupados por posición, cuerpos codificados (URL-encode), colas que no se descartan enteras, zonas horarias en UTC, comparación de claves en tiempo constante, orígenes permitidos y autenticación también en servicios locales, y HTTPS en todos los tramos.

## I. Cómo reutilizarlo
Para una herramienta nueva: copia el **método** (contrato de texto simple + idempotencia por id + cola con carriles + agente saliente + tareas programadas con vigilante + lectura de estado real antes de encolar + limpieza por antigüedad), y revisa las listas G y H para no reintroducir los mismos fallos.

