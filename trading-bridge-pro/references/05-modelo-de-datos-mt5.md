# 05 · Modelo de datos de MetaTrader (lo que un puente debe entender)

Conocimiento para construir herramientas que lean o ejecuten sobre MT4/MT5. Comprueba siempre con la documentación oficial de tu versión; aquí está el modelo mental y las trampas.

## Objetos de MT5
| Objeto | Qué es | Campos clave |
|---|---|---|
| **Cuenta** | Estado financiero | login, servidor, divisa, balance, equity, margen, margen libre, nivel de margen, apalancamiento, modo (netting/hedging), profit flotante |
| **Posición** | Exposición abierta | ticket, **identifier** (id de posición), símbolo, tipo, volumen, precio de apertura, SL, TP, profit, swap, magic, comentario, hora de apertura |
| **Orden** | Instrucción pendiente o ejecutada | ticket, tipo (market/limit/stop/stop-limit), estado, precio, volumen, hora de expiración |
| **Deal (transacción)** | Ejecución real en el historial | ticket, **position_id**, orden, tipo, **entry** (IN/OUT/INOUT/OUT_BY), volumen, precio, profit, comisión, swap, fee, hora |
| **Símbolo** | Instrumento | dígitos, point, tick size, **tick value** (profit/loss), contract size, volumen mín/máx/paso, stops level, freeze level, horario, divisa de margen |

## Reglas que evitan errores de cálculo
- **El resultado de una operación está en los deals, no en la posición abierta.** Una posición cerrada se reconstruye agrupando deals por `position_id`: el deal de entrada (IN) y los de salida (OUT). Suma `profit + commission + swap + fee` de **todos** sus deals.
- **Cierres parciales:** generan varios deals OUT con el mismo `position_id`. En cuentas *netting* el volumen restante conserva la posición; en *hedging* cada posición es independiente.
- **Netting vs hedging:** en netting hay una sola posición por símbolo (las órdenes opuestas la reducen o la invierten). Un copiador o contador de "operaciones" debe contemplarlo.
- **Equity = balance + profit flotante.** Balance solo cambia al cerrar (y con depósitos/retiros). Los depósitos y retiros aparecen como deals de tipo *balance*: **exclúyelos** del rendimiento.
- **Comisión y swap** pueden estar en el deal de entrada o de salida según el broker; suma todos.
- **Divisa:** profit en divisa de la cuenta; para convertir un símbolo usa el tick value, no hagas cuentas con precios a mano.
- **Hora:** MT5 trabaja en hora del **servidor del broker**; guarda el desfase respecto a UTC y convierte en el servidor de tu API.
- **Símbolos con sufijo** (`XAUUSD.m`, `XAUUSD-ECN`): mapea por nombre base configurable.
- **Magic number:** identifica al EA que abrió la operación; úsalo para filtrar y para no tocar operaciones manuales.

## Qué se puede leer con Python (biblioteca oficial de MT5)
Inicializar y conectar terminal · info de cuenta · posiciones · órdenes pendientes · historial de deals y de órdenes por rango de fechas · info y ticks de símbolo · velas históricas. Limitaciones: un terminal por proceso, la API de Python solo funciona en Windows con el terminal instalado, el historial debe estar descargado en el terminal.

## Qué se puede hacer desde un EA (MQL5)
Leer todo lo anterior en tiempo real, enviar datos con `WebRequest` (URL permitida en opciones), operar. Funciona en `OnTimer` y `OnTradeTransaction` para reaccionar a cierres sin esperar al siguiente tick.

## Detectar cambios sin perder eventos
- Guarda el **último deal/ticket procesado** y pide el historial desde ahí hacia adelante; ante la duda reprocesa un margen de tiempo y deja que la **idempotencia** descarte duplicados.
- Reconcilia periódicamente la lista de posiciones abiertas contra el estado del servidor.

## Métricas que se derivan (y cómo no equivocarse)
- **Rentabilidad:** sobre capital depositado neto, no sobre el balance actual.
- **Drawdown:** define *sobre qué* (balance o equity), *desde qué pico* (máximo histórico o inicio del día) y *en qué zona horaria se reinicia el día*. Ver `06-reglas-cuentas-capital.md`.
- **Factor de beneficio, % de aciertos, ganancia media/pérdida media:** solo con operaciones **cerradas**, agrupadas por posición (no por deal) y con una muestra mínima (por ejemplo 30).
- **Racha de pérdidas:** ordena por hora de cierre.
