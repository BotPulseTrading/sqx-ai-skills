# SQX Plugin Pro

Skill gratuita del canal **Bot Pulse Trading** para crear plugins de StrategyQuant X con Claude, con calidad profesional y sin saber programar.

## Qué incluye
- Un **flujo de trabajo** que Claude sigue paso a paso: pregunta, spec, construcción, pruebas, pulido y entrega.
- Una **plantilla de plugin** ya hecha: tema claro y oscuro, español e inglés, tabla ordenable, notas 0-100 con umbrales editables, tooltips, gráfico, exportar CSV, almacén de estrategias y aviso legal.
- Un **simulador de SQX** (`tools/mock_sqx.html`) para probar el plugin sin abrir SQX, con casos raros: datos faltantes, nombres largos, tiempo agotado.
- Un **validador** (`tools/validar_plugin.py`) que revisa 30 puntos de calidad y te dice qué corregir, en español.
- **8 ideas de plugins** con su spec, y los **mensajes exactos** para pedírselos a Claude.
- **Funciones probadas** (`assets/patrones/`): correlación con intervalo de confianza, fiabilidad por muestra, simulación Monte Carlo, cerrojos contra envíos duplicados y cola de reintentos. Nacieron de fallos reales en herramientas de trading.

## Requisitos
- StrategyQuant X con licencia **Pro** (hasta 3 plugins propios) o **Ultimate** (ilimitados). Con Starter no se pueden usar plugins propios.
- Claude (Claude Code o el chat de claude.ai) y Python 3 solo si quieres usar el validador.

## Instalación
**Claude Code**
1. Copia la carpeta `sqx-plugin-pro` dentro de `%USERPROFILE%\.claude\skills\`.
2. Abre Claude Code en la carpeta `user\extend\ResultsPlugins` de tu SQX.
3. Escribe: `Usa la skill sqx-plugin-pro y ayúdame a crear un plugin para SQX`.

**Claude en el navegador o la app**
1. Comprime la carpeta `sqx-plugin-pro` en un `.zip`.
2. En Configuración → Capacidades (o Skills), sube el `.zip`.
3. En un chat nuevo, adjunta el archivo `CLAUDE.md` de tu `ResultsPlugins` y pide el plugin.

## Cómo se usa (resumen)
1. Dile a Claude qué quieres ver que SQX no te muestra (mensajes listos en `references/06-mensajes-para-claude.md`).
2. Confirma la spec de 5 líneas.
3. Claude construye el plugin a partir de la plantilla.
4. Pruébalo en el simulador y pasa el validador.
5. Copia la carpeta del plugin a `ResultsPlugins`, recarga plugins en SQX y **contrasta los números con los de SQX**.

## Importante
- **Contenido educativo.** Los plugins analizan datos históricos; no constituyen asesoramiento financiero ni garantizan resultados. Todo plugin lleva su aviso legal y no debe quitarse.
- Un plugin hecho con IA puede equivocarse. Compruébalo siempre contra SQX antes de fiarte.
- Esta skill **no está afiliada a StrategyQuant**. StrategyQuant X es marca de sus propietarios. El archivo `CLAUDE.md` de tu instalación es la fuente oficial: si algo de aquí no coincide con él, manda el tuyo.
- Estado de las pruebas: la plantilla se ha probado con el simulador incluido y pasa el validador. Pruébala en tu versión de SQX antes de usarla con decisiones reales.

© Bot Pulse Trading · https://www.youtube.com/@BotPulseTrading
