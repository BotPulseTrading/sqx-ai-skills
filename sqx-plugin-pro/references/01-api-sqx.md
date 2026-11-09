# API de ResultsPlugins de SQX — resumen de trabajo

> Resumen para orientarse. **La fuente de verdad es el `CLAUDE.md` que viene en la instalación del usuario** (`user\extend\ResultsPlugins\CLAUDE.md`). Si algo de aquí no coincide con ese archivo, gana el archivo.

## Cómo funciona
- El plugin es una carpeta con un `index.html`. SQX la detecta y la muestra como una pestaña en Resultados, dentro de un `<iframe>`.
- Toda la comunicación es por `postMessage`: SQX → plugin con `window.addEventListener('message', ...)`; plugin → SQX con `window.parent.postMessage(...)`.
- Para ver cambios: icono de recargar plugins en Resultados, o reiniciar SQX.
- Licencia: Starter, ningún plugin propio; Pro, hasta 3; Ultimate, ilimitados. Los que pasan del límite se ignoran en silencio.

## Mensajes que llegan (SQX → plugin)
| Tipo | Cuándo | Qué traer |
|---|---|---|
| `STRATEGY_DATA` | Al seleccionar una estrategia o activar la pestaña | `data.projectName`, `databankName`, `strategyName`, `resultKey` y banderas de AlgoWizard. **Puede llegar con campos vacíos: valida antes de pedir nada.** |
| `SET_THEME` | Al cargar y al cambiar el aspecto | `theme`: `'dark'` o `'light'` |
| `SET_LANGUAGE` | Al cambiar el idioma de SQX | código de idioma (`en`, `es`, `de`, `pt`, `fr`, `it`, `ru`, `pl`, `cz`, `id`, `zh-CN`, `zh-TW`) en `language` o `data` |
| `STATS_RESPONSE` | Respuesta a `GET_STATS` | `data.stats` (objeto de métricas) |
| `ORDERS_RESPONSE` | Respuesta a `GET_ORDERS` | `data.orders` (lista de operaciones) |
| `LAST_SETTINGS_XML_RESPONSE` | Respuesta a `GET_LAST_SETTINGS_XML` | `data.lastSettingsXml` (XML con la configuración del backtest) |
| `SOURCE_CODE_RESPONSE` | Respuesta a `GET_SOURCE_CODE` | `data.success`, `data.code`, avisos |
| `SYMBOL_INFO_RESPONSE` | Respuesta a `GET_SYMBOL_INFO` | objeto del símbolo o `null` |

## Peticiones que envía el plugin (plugin → SQX)
```js
window.parent.postMessage({ type: 'GET_STATS',
  params: { resultKey: 'Portfolio', direction: '0', sampleType: '127', plType: '10' } }, '*');
```
- `direction`: `'0'` ambas, `'1'` largos, `'-1'` cortos.
- `sampleType`: `'127'` todo, `'10'` dentro de muestra (IS), `'20'` fuera de muestra (OOS).
- `plType`: `'10'` dinero, `'20'` porcentaje, `'30'` pips.
- `GET_ORDERS` usa `resultKey`, `direction`, `sampleType`.
- `GET_LAST_SETTINGS_XML` con `params: {}`.
- `GET_SOURCE_CODE` con `params: { format: 'xml' | 'pseudo' | 'mq4' | 'mq5' | 'el' | 'pla' | 'java' }`.
- `GET_SYMBOL_INFO` con `symbol: '...'`.
- SQX añade solo `projectName`, `databankName` y `strategyName`: no los envíes.

## Trampas conocidas (cada una ha roto plugins reales)
1. **Una estrategia por vez.** No hay un mensaje "dame todas". Hay que guardar cada una al recibirla.
2. **Las respuestas no repiten los parámetros de la petición.** Si pides IS, OOS y Full seguidos, no sabes cuál es cuál. Solución: **cola** con una petición en vuelo y tiempo máximo de espera (la plantilla la trae).
3. **`STRATEGY_DATA` vacío** al cargar: valida `projectName`, `databankName` y `strategyName` con `trim()`.
4. **Valores no definidos**: llegan como `null` o `-99999999`. Trátalos como "sin dato", nunca como número.
5. **Canvas no hereda el tema CSS**: al llegar `SET_THEME`, repinta.
6. **Sin scroll externo**: `body { height:100vh; overflow:hidden }`, y el contenido con su propio scroll interno.
7. **`ResizeObserver`**, no `window.resize`: el iframe cambia de tamaño sin que cambie la ventana.
8. **Sin red.** SQX corre sin internet: ni CDN ni fuentes remotas.
9. **El portapapeles puede estar bloqueado** en un iframe: usa `navigator.clipboard` con respaldo.
10. **`localStorage` puede no estar disponible**: envuélvelo en `try/catch` y ten un respaldo en memoria.

## Métricas habituales (`stats`)
Beneficio y operaciones: `NetProfit`, `NumberOfTrades`, `WinningPct`, `AvgTrade`.
Calidad: `ProfitFactor`, `SQN`, `Stability`, `SharpeRatio`, `RExpectancy`.
Riesgo: `Drawdown`, `PctDrawdown`, `ReturnDDRatio`, `CalmarRatio`, `MaxConsecLoss`.
Tiempo: `StagnationPeriod`, `StagnationPeriodPct`, `AvgTradesPerMonth`, `ProfitableMonths`.
Estadística: `ZScore`, `DegreesOfFreedom`, `Symmetry`, `Exposure`.
Costes: `Commission`, `SlippageInMoney`, `CommSwapInMoney`.
La lista completa y su descripción están en el `CLAUDE.md` del usuario.

## Operaciones (`orders`) más útiles
`OpenTime`, `CloseTime`, `Type`, `CloseType`, `SampleType`, `OpenPrice`, `ClosePrice`, `Size`, `ProfitLoss`, `ProfitLossPct`, `MAE`, `MFE`, `Balance`, `BarsInTrade`, `TimeInTrade`.
Tipos: 1 compra, 2 venta, 3-8 pendientes, 9-11 depósito/retirada/balance. Ignora 9-11 al calcular rendimiento de la estrategia.
