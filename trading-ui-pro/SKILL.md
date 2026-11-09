---
name: trading-ui-pro
description: Diseña y construye interfaces profesionales para herramientas de trading: paneles de cuentas, dashboards, tablas de estrategias, monitores, apps web o de escritorio. Úsala cuando el usuario pida una pantalla, panel, dashboard o app para ver cuentas, operaciones, riesgo o resultados, con recomendación primero, datos claros, tema claro/oscuro, español/inglés y accesibilidad.
---

# Trading UI Pro — interfaces de trading que se leen y se usan

Una interfaz de trading es una herramienta de decisión. Debe responder rápido a "¿cómo voy y qué hago?" sin esconder los riesgos.

## Reglas
1. **Recomendación primero, detalle bajo demanda.** Arriba: la conclusión y la acción (por ejemplo "Esta cuenta está a 1,2 % del límite diario"). Debajo, el detalle desplegable.
2. **Todo número con su contexto:** muestra de datos, periodo, unidad y fiabilidad. Con pocos datos, aviso, no nota.
3. **Un dato ausente nunca se pinta como cero ni como "cumple".** Se muestra "sin dato".
4. **Color con significado** (verde/ámbar/rojo) más icono y texto; nunca solo color.
5. **Los riesgos no se esconden.** El drawdown, el límite diario y la pausa global siempre visibles.
6. **Aviso legal visible:** contenido informativo, no es asesoramiento financiero ni garantiza resultados.
7. **Estados siempre cubiertos:** vacío, cargando, error, sin conexión, datos viejos (con la hora de la última actualización).

## Flujo
1. **Pregunta de la pantalla** (¿qué decisión habilita?) y **usuario** (trader, gestor, cliente).
2. **Jerarquía:** un dato protagonista, 3-5 de apoyo, el resto en detalle. Boceta en texto antes de codificar.
3. **Tokens de diseño** (colores, espacios, tipografía) en variables; tema claro y oscuro desde el principio. Ver `references/01-sistema-visual.md`.
4. **Construye** componentes pequeños (tarjeta de métrica, tabla, insignia, gráfico, panel de ajustes) y reutilízalos.
5. **Prueba** con datos reales y raros (ver lista abajo) y en móvil, tableta y escritorio.
6. **Revisa** con `references/02-checklist-ui.md`. Si el usuario tiene la skill `impeccable`, úsala para `critique` y `polish`.

## Casos raros que siempre se prueban
Sin datos · un solo dato · 500 filas · nombres larguísimos · números enormes o negativos · `null` · cambio de tema a mitad · idioma inglés (textos más largos) · pantalla pequeña · conexión perdida · datos de hace horas.

## Tecnología
Por defecto HTML + CSS + JavaScript puro en un solo archivo (fácil de entregar y de revisar). Vue/React solo si el proyecto ya los usa o hay una razón clara. Gráficos en canvas o SVG sin librerías remotas si la herramienta debe funcionar sin conexión. Sin CDN en herramientas que se usan dentro de otros programas.

## Referencias
- `references/01-sistema-visual.md` — tokens, tipografía, componentes y gráficos.
- `references/02-checklist-ui.md` — revisión de calidad y accesibilidad.
- `references/03-elementos-del-dashboard.md` — catálogo de piezas de un dashboard de cuentas (límites, drawdown, matriz bot × cuenta, estado del puente) con sus trampas.
- `references/04-dashboard-y-app-reales.md` — estructura, estados, patrones, fórmulas y carencias de un dashboard y una app móvil reales de cuentas de trading.
- Para plugins dentro de StrategyQuant X: skill `sqx-plugin-pro` (incluye plantilla y simulador).
- Para el backend que alimenta el panel: skill `trading-bridge-pro`.
