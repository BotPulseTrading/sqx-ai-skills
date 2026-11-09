# SQX AI

Kit gratuito del canal **Bot Pulse Trading** para crear, con Claude, todo lo necesario alrededor del trading algorítmico: plugins de StrategyQuant X, interfaces profesionales y software conectado a servidores (puentes MT4/MT5, paneles de cuentas, copiadores, monitores).

| Skill | Para qué |
|---|---|
| [`sqx-plugin-pro`](sqx-plugin-pro/) | Plugins de resultados para StrategyQuant X: plantilla, simulador de SQX, validador y patrones probados. |
| [`trading-ui-pro`](trading-ui-pro/) | Interfaces de trading (paneles, dashboards, tablas): sistema visual, recomendación primero, checklist de calidad y accesibilidad. |
| [`trading-bridge-pro`](trading-bridge-pro/) | Software vinculado a servidores (puente MT5↔API, copiadores, monitores): arquitectura, idempotencia, seguridad, despliegue y pruebas de fallo. |
| [`publicar-en-github`](publicar-en-github/) | Subir una skill o proyecto a GitHub con escáner de secretos y confirmación antes de publicar. |

## Cómo se combinan
1. Idea → `sqx-plugin-pro` (si va dentro de SQX) o `trading-ui-pro` (si es una app/panel).
2. Si necesita datos de cuentas o enviar órdenes → `trading-bridge-pro`.
3. Cuando está listo → `publicar-en-github`.

## Instalación (Claude Code)
Copia las carpetas de las skills que quieras a `%USERPROFILE%\.claude\skills\`. Cada una tiene su `SKILL.md`; las de SQX y GitHub traen además su propio README.

## Importante
- Contenido educativo; no es asesoramiento financiero ni garantiza resultados. El trading con dinero real conlleva riesgo de pérdida.
- Todo lo que pueda ejecutar órdenes debe probarse primero en cuenta demo.
- No está afiliado a StrategyQuant ni a MetaQuotes. Sus nombres son marcas de sus propietarios.
- Estado de las pruebas: las plantillas y herramientas de `sqx-plugin-pro` se probaron con su simulador y pruebas unitarias; `trading-ui-pro` y `trading-bridge-pro` son guías de método basadas en proyectos reales y **no incluyen código ejecutable probado contra un broker real**. Pruébalo en tu entorno antes de fiarte.

© Bot Pulse Trading · https://www.youtube.com/@BotPulseTrading
