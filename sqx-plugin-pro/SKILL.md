---
name: sqx-plugin-pro
description: Crea plugins de resultados (ResultsPlugins) para StrategyQuant X con calidad profesional usando Claude. Úsala cuando el usuario quiera diseñar, construir, probar, mejorar o revisar un plugin para la pestaña de resultados de StrategyQuant X (SQX), por ejemplo un clasificador de estrategias, un scorecard, una tabla comparativa, un gráfico propio o cualquier panel que lea estadísticas, operaciones o configuración de una estrategia. Incluye plantilla probada, simulador de SQX sin necesidad del programa y validador de calidad.
---

# SQX Plugin Pro — plugins de StrategyQuant X con nivel profesional

Skill del canal Bot Pulse Trading. Sirve para pasar de "una idea" a un plugin de SQX que se ve, se comporta y se prueba como un producto, aunque quien lo pide no sepa programar.

## Reglas que mandan sobre todo lo demás

1. **El `CLAUDE.md` del propio SQX del usuario manda.** Está en `user\extend\ResultsPlugins\CLAUDE.md` dentro de su instalación. Léelo siempre antes de escribir código. Si lo que dice choca con esta skill (versiones nuevas de SQX cambian mensajes y campos), gana el archivo del usuario. Si no lo encuentras, pídeselo; no inventes campos ni mensajes.
2. **Nunca prometas resultados.** Un plugin analiza el pasado. No escribas textos como "estrategias ganadoras" o "rentabilidad asegurada". Usa "encaja con las reglas que definiste".
3. **Aviso legal obligatorio**, siempre el último elemento visible del plugin (ver `references/02-estandar-profesional.md`). No se quita ni se esconde.
4. **Todo local y sin red.** SQX funciona sin conexión: nada de CDN, fuentes de Google, analíticas ni llamadas a servidores. Si algo necesita una librería, se copia a la carpeta del plugin.
5. **Privacidad.** No pidas ni guardes claves, contraseñas ni datos de cuentas. No incluyas rutas personales en el código.
6. **No copies plugins de terceros, de pago ni de academias.** Si el usuario te da uno como referencia, describe lo que hace y escribe el tuyo desde cero.

## Flujo de trabajo (síguelo en orden)

### Paso 0 · Contexto
- Lee `CLAUDE.md` de SQX. Anota: versión, mensajes disponibles, campos de `stats` y de `orders`, límites de licencia (Starter 0 plugins, Pro 3, Ultimate sin límite).
- Pregunta qué licencia tiene y cuántos plugins ya usa. Si está en el límite, avísale antes de construir.
- Mira qué carpetas hay en `ResultsPlugins` solo para no pisar nombres. No nombres ni copies lo que haya dentro.

### Paso 1 · La pregunta del plugin (spec en 5 líneas)
Antes de código, escribe y confirma con el usuario:
1. **Pregunta que responde**: "¿qué quiero ver que SQX no me muestra?"
2. **Datos que necesita**: qué estadísticas (`GET_STATS`), operaciones (`GET_ORDERS`), configuración (`GET_LAST_SETTINGS_XML`) o código (`GET_SOURCE_CODE`).
3. **Decisión que habilita**: qué hará el usuario con lo que vea.
4. **Qué muestra en pantalla**: una tabla, un score, un gráfico, una comparación.
5. **Qué NO hace**: lo que queda fuera de esta primera versión.
Si el plugin necesita ver **todas** las estrategias a la vez, recuerda que SQX entrega **una cada vez**: el plugin debe guardarlas (ver patrón "almacén" en `references/02-estandar-profesional.md`).
Ideas listas con su spec: `references/04-ideas-de-plugins.md`.

### Paso 2 · Arquitectura mínima
- Un solo `index.html` dentro de su carpeta (`ResultsPlugins\NombreDelPlugin\index.html`). JavaScript puro por defecto; Vue 3 solo si ya hay una copia local de `vue.global.prod.js`.
- Separa en el mismo archivo, en este orden: **CONFIG** (umbrales, pesos, textos) → **ESTADO** → **COMUNICACIÓN con SQX** → **LÓGICA** (cálculos puros) → **VISTA** (pintar) → **ARRANQUE**.
- Parte de `assets/plantilla-plugin/index.html`. Ya trae tema claro/oscuro, idiomas, cola de peticiones, almacén persistente, tabla ordenable, exportar CSV, tooltips, gráfico en canvas, estados vacío/cargando/error y aviso legal.

### Paso 3 · Construir
- Cambia primero **CONFIG** y la función de cálculo. Después la vista. Lo demás de la plantilla se mantiene.
- Si el plugin necesita **correlaciones, intervalos de confianza, fiabilidad por muestra o una simulación Monte Carlo**, copia lo que haga falta de `assets/patrones/estadistica.js`. Si necesita **cerrojos, envíos sin duplicados, cola de reintentos, repintado sin parpadeo o tooltips que no se cortan**, copia de `assets/patrones/robustez.js`. Están probados; no los reescribas.
- Todo cálculo muestra su **muestra y su fiabilidad**, y por debajo de un mínimo de operaciones no puntúa (ver `references/07-patrones-de-herramientas-reales.md`).
- Cada métrica que no sea obvia lleva tooltip de 3 líneas: qué es, cómo leerla con números, para qué sirve.
- Los umbrales viven en CONFIG y se pueden editar en pantalla (el usuario ajusta a sus reglas). Los tooltips se generan desde esos mismos umbrales para que nunca se contradigan.
- Textos de interfaz en el objeto de idiomas, no repartidos por el HTML. Mínimo español e inglés.

### Paso 4 · Probar sin SQX
- Abre `tools/mock_sqx.html` en el navegador con el plugin a probar: simula SQX (tema, idioma, estrategias, `GET_STATS`, `GET_ORDERS`). Sirve para ver casos raros: estrategia sin datos, campos `null`, `-99999999`, cambio de tema a mitad, 50 estrategias.
- Ejecuta el validador: `python tools/validar_plugin.py ruta/al/index.html`. Corrige todo lo marcado como ERROR; lee los AVISO.
- Después prueba en SQX real: recarga plugins con el icono de recargar, selecciona estrategias una a una y compara **los mismos números** que muestra SQX. Si no coinciden, el plugin está mal, no SQX.

### Paso 5 · Pulir (nivel producto)
Recorre `references/03-diseno.md` y la lista de `references/02-estandar-profesional.md`. Si el usuario tiene instalada la skill `impeccable`, úsala para `critique`, `polish` o `harden` sobre el archivo ya funcional; no sustituye al validador.

### Paso 6 · Entrega
Dile al usuario, en lenguaje llano: dónde copiar la carpeta, que reinicie o recargue plugins, cómo usarlo, qué umbrales puede cambiar, qué limitaciones tiene y que contrastes siempre con SQX. Si hubo errores durante las pruebas, cuéntalos; no los escondas.

## Definición de "hecho" (10/10)
Un plugin solo se entrega cuando cumple todo esto; si algo no se pudo, se dice:
- [ ] Spec de 5 líneas confirmada por el usuario y respetada (nada extra sin pedirlo).
- [ ] `validar_plugin.py` sin ERROR y con los AVISO leídos y explicados.
- [ ] Probado en `mock_sqx.html` con: sin datos, `null`, `-99999999`, 50 estrategias, nombres largos, tema claro/oscuro, español/inglés y panel pequeño.
- [ ] Cada cifra mostrada se recalculó a mano con una estrategia y coincide con SQX (o se avisa de que falta esa comprobación).
- [ ] Un dato ausente nunca cuenta como "cumple" ni como cero.
- [ ] Muestra pequeña = aviso de fiabilidad, no nota.
- [ ] Sin red, sin claves, sin rutas personales, con aviso legal.
- [ ] Informe final honesto: qué se probó, qué no (por ejemplo "no probado en SQX real"), limitaciones y próximos pasos.

## Protocolo de depuración (cuando algo no cuadra)
1. Reproduce en el simulador con el mismo dato. 2. Imprime la respuesta cruda de SQX y compárala con lo que pinta el plugin. 3. Cambia una sola cosa por intento. 4. Añade al simulador el caso que falló para que no vuelva. 5. Repasa `references/05`, `07` y `08`: casi siempre es una clase de fallo ya conocida (dato ausente, petición duplicada, hora/unidad, estado sin reiniciar).

## Más allá del plugin
Si el usuario pide algo conectado (un EA, un script, una web, un panel), aplica las mismas reglas: spec corta, parte de algo probado, prueba sin riesgo (simulador, datos sintéticos), revisa con la lista de fallos de `references/08` y entrega con declaración honesta. Para subir el resultado a GitHub usa la skill `publicar-en-github`.

## Cuando el plugin falla
Pide al usuario el texto exacto del error o una captura de la consola del navegador (F12 dentro del iframe, si SQX lo permite). Corrige un problema cada vez y vuelve a ejecutar el validador. Explica en una frase qué fallaba.

## Archivos de esta skill
| Archivo | Para qué |
|---|---|
| `references/01-api-sqx.md` | Resumen de mensajes y campos (gana el `CLAUDE.md` del usuario) |
| `references/02-estandar-profesional.md` | Nivel de calidad, patrones y lista de revisión |
| `references/03-diseno.md` | Sistema visual: colores, tipografía, densidad, gráficos |
| `references/04-ideas-de-plugins.md` | Ocho plugins con su spec, para empezar rápido |
| `references/05-lecciones-proyectos-reales.md` | Lo aprendido construyendo herramientas reales de trading |
| `references/06-mensajes-para-claude.md` | Los mensajes que el usuario debe escribir a Claude |
| `references/07-patrones-de-herramientas-reales.md` | Patrones de un panel de cuentas, un agente de backtests y automatizaciones: idempotencia, fiabilidad, simulación, recomendación primero |
| `references/08-lecciones-copiadores-y-eas.md` | Reconciliar estados, autenticación web, apps WebView, fallos típicos de EAs y cómo leer un backtest con reglas de cuenta |
| `assets/patrones/estadistica.js` | Pearson, intervalo de Fisher, fiabilidad, percentiles y Monte Carlo (probado) |
| `assets/patrones/robustez.js` | Cerrojo, envío idempotente, cola de reintentos, repintado por firma y tooltip que cabe (probado) |
| `assets/plantilla-plugin/index.html` | Plantilla profesional lista para adaptar |
| `tools/mock_sqx.html` | Simulador de SQX para probar sin el programa |
| `tools/validar_plugin.py` | Validador de calidad con informe en español |
