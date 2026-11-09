# Ocho ideas de plugins con su spec

Cada idea trae lo que necesita para pedírselo a Claude: pregunta, datos, vista y límites. Los números son **ejemplos**; el usuario pone los suyos.

## 1. Clasificador por tipo de cuenta
- **Pregunta**: ¿en qué cuenta encaja mejor cada estrategia (propia, capital externo, prop firm)?
- **Datos**: `GET_STATS` (Full, IS, OOS). Métricas: `ReturnDDRatio`, `ProfitFactor`, `PctDrawdown`, `MaxConsecLoss`, `StagnationPeriodPct`.
- **Vista**: tabla con nota 0-100 por cuenta, "mejor cuenta" y motivo; selector de cuenta; panel de umbrales.
- **Límites**: la nota no predice nada; el filtro duro de drawdown marca "No cumple".

## 2. Scorecard de una estrategia
- **Pregunta**: ¿qué puntos fuertes y débiles tiene esta estrategia de un vistazo?
- **Datos**: `GET_STATS` ambos lados, largos y cortos.
- **Vista**: 5-6 pilares (rentabilidad, riesgo, consistencia, estabilidad, simetría, muestra) con barra y tooltip; nota global con letra.
- **Límites**: pesos editables; explicar siempre por qué.

## 3. Comparador de dos o tres estrategias
- **Pregunta**: ¿cuál de estas estrategias es mejor para mí y por qué?
- **Datos**: `GET_STATS` de cada una (almacén).
- **Vista**: columnas lado a lado, mejor valor resaltado por fila, diferencia en %.
- **Límites**: no mezclar `plType` distintos.

## 4. Visor dentro / fuera de muestra
- **Pregunta**: ¿se comporta igual fuera de la muestra?
- **Datos**: `GET_STATS` con `sampleType` 10 y 20.
- **Vista**: tabla IS vs OOS con degradación en % por métrica, color por degradación, gráfico de barras pareadas.
- **Límites**: pocas operaciones OOS = dato poco fiable; avisar si `NumberOfTrades` es bajo.

## 5. Mapa de calor de rendimiento por mes
- **Pregunta**: ¿cuándo gana y cuándo pierde la estrategia?
- **Datos**: `GET_ORDERS` (`CloseTime`, `ProfitLoss`).
- **Vista**: cuadrícula año × mes con color por resultado y total anual; tooltip con nº de operaciones.
- **Límites**: ignorar tipos 9-11 (depósitos); usar la zona horaria de SQX.

## 6. Perfil de las operaciones (MAE/MFE y duración)
- **Pregunta**: ¿cuánto va en contra una operación antes de ganar y cuánto tarda?
- **Datos**: `GET_ORDERS` (`MAE`, `MFE`, `ProfitLoss`, `TimeInTrade`).
- **Vista**: dispersión MAE vs resultado, histograma de duración, percentiles.
- **Límites**: orientativo para ajustar stops; no recomienda valores.

## 7. Informe exportable
- **Pregunta**: ¿cómo documento y comparto el análisis de una estrategia?
- **Datos**: `GET_STATS`, `GET_LAST_SETTINGS_XML`.
- **Vista**: hoja de una página con resumen, ajustes y avisos; botón "Copiar como texto" y CSV.
- **Límites**: el informe incluye el aviso legal.

## 8. Revisor de reglas propias (checklist)
- **Pregunta**: ¿esta estrategia cumple mi lista personal de requisitos?
- **Datos**: `GET_STATS`.
- **Vista**: lista de reglas editables (métrica, operador, valor) con "Cumple / No cumple" y total "7 de 9".
- **Límites**: las reglas las define el usuario; el plugin no sugiere umbrales como recomendación.

## Cómo elegir
1. Que responda a **una** pregunta que el usuario se hace de verdad.
2. Que use datos que SQX **ya entrega**.
3. Que se pueda terminar en una tarde. Lo demás va a la versión 2.
