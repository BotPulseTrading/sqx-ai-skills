# 08 · Lecciones de un copiador de operaciones y de un EA de rango

Patrones generales sacados de dos proyectos reales de trading (un copiador de operaciones entre cuentas y un asesor experto de ruptura de rango). No incluyen datos privados. Úsalos cuando un plugin de SQX toque ideas parecidas (reconciliar estados, avisar de riesgos, generar código de un EA).

## A. Reconciliar estados entre dos sistemas (copiadores, paneles, sincronizaciones)
1. **Identidad estable.** Identifica cada operación por su ticket/ID, no por posición en la lista ni por precio. Tras un cierre parcial el ticket puede cambiar: guarda la relación vieja→nueva.
2. **Reconciliación solo hacia abajo.** Si la copia tiene más de lo que debería, se corrige (cerrar sobrante). Si le falta algo, no se abre a ciegas: puede ser un cierre legítimo. Decide y muestra el motivo.
3. **Huérfanos y huecos.** Limpia entradas que ya no existen en el origen y libera "slots" ocupados; si no, el sistema se queda bloqueado en silencio.
4. **Intercambio por archivos o colas.** Escribe a un archivo temporal y renombra (atómico), con marca de tiempo; el lector ignora datos viejos y avisa si dejan de llegar.
5. **Idempotencia.** Un reintento nunca debe duplicar (ver `07`: cerrojo síncrono + leer el estado real antes de reenviar).

## B. Servicios web y autenticación
- Distingue autenticación por sesión del navegador (con nonce) de la de aplicaciones (token en cabecera). No mezcles ambas en el mismo endpoint sin probarlo.
- Si un plugin de terceros intercepta la cabecera estándar `Authorization`, usa una cabecera propia para tu token.
- **No edites archivos de plugins ajenos.** Se pierde en la siguiente actualización. Extiende con filtros o un plugin propio.
- Unidades de red mapeadas (letras de disco) no existen para procesos del servidor ni para tareas programadas: usa rutas UNC o copia local.
- Despliega por reemplazo atómico y conserva copia con nombre de la versión anterior.

## C. Apps de escritorio o móviles que envuelven una web
- Una app envolviendo una WebView es más rápida de entregar y mantener que una app nativa; aprovecha la misma web. Rediseña solo la navegación y los permisos.
- Una sola app para todos los clientes con configuración por cliente, en lugar de una compilación por cliente.
- Declara honestamente qué se probó (emulador vs dispositivo real).

## D. Generar o revisar código de un EA (MQL4/MQL5)
Lista de fallos típicos a buscar antes de entregar:
1. **Comparar horas por separado** (`hora>=H && minuto>=M`) falla en el cambio de hora; compara minutos totales del día.
2. **Banderas "una vez al día"** que se reinician a medianoche; sin ellas el EA reentra tras cada SL.
3. **Rango con la vela en formación**: calcula con velas cerradas y una sola vez; contempla rangos que cruzan medianoche y arranques tardíos.
4. **Lotes**: redondea hacia abajo al `LotStep`, respeta mínimo/máximo, usa el valor del tick correcto para pérdida.
5. **Precios**: normaliza al `TickSize` y a los dígitos; comprueba distancia mínima de stops/freeze antes de enviar la orden.
6. **Inputs que no hacen nada**: revisa que cada parámetro del panel se use de verdad.
7. **Limpieza**: borra objetos gráficos en `OnDeinit`; reintentos con tope.
8. Entrega con declaración honesta: "no compilado / no probado en el Strategy Tester" si es así, y pide compilar (F7) y backtest antes de usar en real.

## E. Evaluar resultados de un backtest para una cuenta con reglas
- El drawdown del backtest escala casi en proporción al riesgo por operación: para bajarlo a un límite, reduce el riesgo en la misma proporción (y el beneficio cae igual).
- Con reinversión (interés compuesto) los números se exageran; evalúa riesgo fijo para comparar.
- Muchas reglas de cuentas con capital de terceros miden el **drawdown diario**, no solo el máximo: un plugin que ayude a un trader debería mostrar el peor día.
- Un porcentaje de aciertos más alto con ganancia media menor suele indicar break even o trailing: explícalo en lugar de celebrarlo.
- No digas límites exactos de una empresa de cuentas de memoria; pide al usuario la regla vigente.
