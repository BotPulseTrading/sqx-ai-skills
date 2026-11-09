# 04 · Dashboard de cuentas y app móvil reales: estructura, estados y lecciones

Mapa de un panel real (SPA de un archivo en iframe + app Android con WebView y pantallas nativas). Úsalo para decidir qué secciones, estados y componentes construir. Backend y contratos: ver `trading-bridge-pro/references/07-ecosistema-real-ea-web-cola-agente.md`.

## Estructura del dashboard web
- **Shell:** barra lateral con selector de cuenta (varias cuentas + "manual" para subir un archivo arrastrándolo), insignia "Nombre · N trades", menú de secciones con insignias (tareas en curso, alertas sin leer) y pantalla de arranque.
- **Estados globales:** `cargando` (con mensaje), `sin datos`, `subir archivo` (zona de arrastre .csv/.txt/.log) y `panel`. El menú se **deshabilita** si no hay datos.
- **Franja de alertas** visible desde cualquier sección: "N alertas de drawdown sin leer" (Ver / Marcar como leídas) y aviso "Tus límites no se están vigilando" si hay reglas activas y el EA está desconectado.
- **Filtros** (colapsables en móvil): identificar robot por comentario o por magic, símbolo, tipo, rango de fechas, limpiar. Se ocultan en las secciones donde no aplican.
- Última sección recordada en `localStorage`; el panel avisa su altura al padre (`iframe`).

## Secciones
1. **Resumen:** KPIs (balance, beneficio, trades, win rate, máx. drawdown, costes adicionales) + curva de equity.
2. **Análisis:** distribución de P&L, profit por robot/símbolo/mes/día de semana/hora, y **ranking detallado por robot y símbolo** con fiabilidad.
3. **Robots / Símbolos:** tarjetas con profit y nº de operaciones.
4. **Real vs Backtest:** estado en pasos (suscripción → tu PC → backtests), botón de "ping" al PC, tabla comparativa real vs MT5 vs SQX (con modo "solo ratios"), curva en vivo, salud del backtest (`ok | stale | nodata | data-gap`), recorte al periodo común y normalización por depósito.
5. **Alertas de drawdown:** estado de conexión del EA (conectado / sin conexión / sin datos todavía, versión, "puede cerrar"), cuenta (balance, equity, flotante), barra de DD usado, editor de dos reglas ("Cada operación", "Toda la cuenta": interruptor, límite en % o en importe con vista previa, "Solo avisarme / Avisarme y cerrar"), aviso de cierre automático, barra Guardar/Descartar, tabla de operaciones abiertas con estado por chip y lista de alertas con icono por tipo.
6. **Calendario:** año/mes/día, `$` o `%`, mejor/peor robot.
7. **Operaciones:** tabla ordenable con paginación de 50.

## Patrones de interfaz que funcionaron
- **Estado de configuración explícito:** "Sin configurar / Cambios sin guardar / Guardada / Aplicada en el EA" (comparando revisión guardada y confirmada). Evita el "¿se aplicó o no?".
- **Chips de estado** con umbrales: ≥100 % "Límite superado / Se cierra", ≥70 % "Cerca del límite", resto "Dentro del límite", "Sin límite". Barra proporcional al límite.
- **Fiabilidad por muestra:** ≥100 operaciones "Muy fiable", ≥30 "Fiable", <30 "Pocos datos" (aparte, atenuado y con barra de progreso hacia 30), con casilla "solo ≥30 trades".
- **Datos viejos visibles:** edad del último dato calculada como la del servidor + segundos desde la última lectura.
- **Mensajes de sesión claros:** "No recibimos tu sesión" (sin token) distinto de "Tu sesión expiró" (401/403).
- **Cerrojo anti-duplicados** entre pestañas (`localStorage`) y lectura de la cola real antes de enviar un trabajo.
- **Validación en la interfaz:** número > 0, ≤100 si es porcentaje, tope razonable en dinero, coma decimal aceptada.
- Escape de HTML en todo dato que viene del servidor.

## App móvil (Kotlin, Compose)
- Secciones: ranking de estrategias, portafolio, dashboard (WebView del mismo HTML con el token inyectado), nuevo backtest, historial, actualizar histórico, historial de actualizaciones, conexión con tu PC y tarjeta de alertas.
- **Alertas:** servicio en primer plano cada 60 s + trabajo periódico de 15 min, con un `Mutex` común para no avisar dos veces; "visto" por clave `cuenta|eid`; la primera ejecución **siembra sin notificar**; más de 3 alertas nuevas = una notificación resumen; token caducado = una sola notificación y se cancela el trabajo. Es **sondeo, no push**: dilo.
- **Sesión:** token en almacenamiento cifrado, caducidad leída del propio token, cierre de sesión con motivo en 401/403.
- Historial: sondeo cada 5 s mientras haya trabajos `queued/claimed` y refresco al volver a primer plano.
- Ajustes con **panel de diagnóstico** (último resultado, permiso de notificaciones, notificación de prueba, exclusión de batería): ahorra soporte.
- Banner de actualización de la app comparando versión instalada y última; la app envía su versión en cada llamada.
- Descargas a la carpeta pública (no a una carpeta privada invisible) y aviso al terminar.

## Fórmulas del panel (y trampas)
- Max drawdown del Resumen: caída pico-valle de la curva acumulada de profit neto, ordenada por fecha de cierre, **absoluta**; en Real vs Backtest se expresa **relativa al depósito/balance de referencia**, no al pico (un pico que parte de 0 dio 723 %).
- Costes adicionales = (balance − depósitos netos) − suma del neto de operaciones (swaps y comisiones no atribuidos).
- Depósito = suma de las filas de tipo BALANCE; tras retiros puede ser ≤0 → caer a balance. Créditos/bonos no son depósito.
- Win rate/PF: elige **neto o bruto** y úsalo en todas las pantallas (el panel real mezcló ambos).
- Calendario y "profit por hora": la hora del historial es de servidor, no del navegador; convierte con un desfase guardado.
- DD diario de prop firms y hora de reinicio: necesitan normalizar campos que vienen como texto libre (`daily_loss_basis`, `daily_reset`) a una lista cerrada (base: balance | equity | mayor de ambos; reinicio: zona + hora) antes de calcular.

## Carencias a evitar en tu panel
- Sin infraestructura de **idiomas** (todo en español dentro del código): empieza con un objeto de textos.
- Solo tema **oscuro**: añade claro y respeta `prefers-color-scheme`.
- Una sola divisa fija para dinero de trades.
- Reglas, plantillas y rotación no implementadas como lógica: si las prometes en la interfaz, impleméntalas o quita el hook vacío.

## Esquema de reglas de prop firms (datos del panel)
Cada firma tiene programas, y cada programa fases con: objetivo %, pérdida diaria máx. %, base de la pérdida diaria, si incluye flotante, reinicio diario, pérdida total máx. %, **tipo de DD** (`static`, `trailing_equity`, `trailing_balance`, `trailing_until_initial`), días mínimos, días máximos, consistencia (`none`, `best_day_pct_of_profit`, `best_trade_pct_of_profit`, `profit_share_per_day_vs_target`) y restricciones con gravedad `block | warn | info` (EAs, noticias, fin de semana, copy trading, martingala, lote máximo, inactividad, VPS…). Se valida con un script antes de publicar (rangos 0-100, enums, que una fase fondeada no tenga objetivo, que un programa no desaparezca sin marcarse `discontinued`). Se revisa cada pocos días **sin IA y sin modificar cifras automáticamente**: solo avisa si cambia el texto de la página oficial. Valores y textos de cada firma no se copian aquí.
