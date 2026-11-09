# 06 · Reglas de cuentas con capital de terceros (prop firms) y cómo modelarlas

Las empresas de fondeo tienen reglas distintas y **cambian**. Esta skill no las sabe de memoria: **pide siempre al usuario la regla vigente** (o que pegue el texto de la web) y modélala como configuración, nunca como valor fijo del código.

## Parámetros que casi siempre existen (ponlos en configuración por cuenta)
| Parámetro | Qué define |
|---|---|
| Capital inicial | Base de los porcentajes |
| Objetivo de beneficio | % o importe para pasar la fase |
| Pérdida diaria máxima | Límite por día (importe o %) |
| Pérdida máxima total | Límite acumulado |
| **Tipo de drawdown** | Estático (desde el capital inicial), trailing (sigue el máximo), con o sin bloqueo al llegar a break-even |
| **Base de cálculo** | Balance, equity, o el mayor de los dos |
| **Hora de reinicio del día** | Zona horaria y hora exacta (a menudo cierre de Nueva York o medianoche del servidor) |
| Días mínimos de trading | Cuenta de días con operaciones |
| Reglas de consistencia | Tope de % del beneficio en un solo día u operación |
| Restricciones | Operar en noticias, fin de semana, EAs, copiadores, martingala, tamaño máximo |
| Comisiones | Si el cálculo las incluye |

## Cómo modelar el límite diario
```
inicio_del_dia   = referencia a la hora de reinicio de la firma
referencia       = balance (o equity) al inicio del día   <- según regla
limite_diario    = referencia - pérdida_diaria_máxima
margen_restante  = equity_actual - limite_diario          <- usa equity: incluye flotante
```
- Calcula con **equity en vivo**, porque muchas firmas cuentan la pérdida flotante.
- El panel muestra **cuánto margen queda** y avisa por umbrales (por ejemplo 50 %, 75 %, 90 % consumido).
- Un EA o puente puede aplicar una **pausa preventiva** al acercarse al límite (por ejemplo al 80 %), siempre configurable y visible.

## Cómo modelar el drawdown total
- **Estático:** límite = capital inicial − pérdida máxima total (no se mueve).
- **Trailing:** límite = pico máximo − pérdida máxima total (sube con el pico; define si el pico es de balance o de equity y si se detiene en un nivel).
- Guarda el **pico** en el servidor de forma persistente; recalcular desde el historial puede dar otro valor si faltan datos.

## Rotación y asignación de bots a cuentas (idea del panel)
- Un mismo bot puede tener varias cuentas candidatas; decide con reglas visibles: margen de drawdown restante, racha reciente, días de trading pendientes, correlación entre bots en la misma cuenta.
- Muestra **el motivo** de cada recomendación ("cuenta B: 3,1 % de margen diario libre; cuenta A: 0,4 %"). La recomendación no ejecuta nada sin confirmación humana.

## Avisos y fiabilidad
- Un panel de reglas es una **ayuda**, no una garantía: los datos del broker y los de la firma pueden diferir (precio de cierre, swaps, hora de reinicio). Contrasta con el panel oficial de la firma.
- Si falta el dato (cuenta desconectada), muestra "sin dato" y la hora de la última actualización; no extrapoles.
- No des consejo de inversión ni prometas pasar una evaluación.

## Pruebas
Casos que deben cubrirse con datos sintéticos: justo en el límite, cruce de medianoche, cambio de hora de verano, depósito/retiro a mitad de día, posición abierta de un día a otro, cierre parcial, comisiones y swaps, cuenta sin operaciones.
