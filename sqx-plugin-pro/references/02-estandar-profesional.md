# Estándar profesional para un plugin de SQX

La diferencia entre "funciona" y "profesional" son los detalles de esta lista. Aplícala siempre.

## 1. Estados que toda pantalla debe tener
| Estado | Qué ve el usuario |
|---|---|
| Esperando | "Selecciona una estrategia en la lista" con una línea que explica qué hará el plugin |
| Cargando | Indicador sutil y texto "Leyendo estadísticas (2 de 3)…", nunca pantalla en blanco |
| Con datos | La vista principal |
| Vacío tras filtrar | "Ninguna estrategia cumple este filtro", con botón para limpiar |
| Dato faltante | Guion "—" y tooltip "SQX no entregó este dato". Nunca `NaN`, `undefined` ni `-99999999` |
| Error o tiempo agotado | Mensaje en lenguaje llano, qué pasó, qué hacer y botón "Reintentar" |

## 2. Patrón "almacén" (guardar todas las estrategias)
SQX entrega una estrategia por vez. El plugin guarda cada una al recibirla:
- Clave: `proyecto|databank|estrategia`.
- Persistencia en `localStorage` bajo un prefijo propio del plugin, con `try/catch` y respaldo en memoria.
- Muestra siempre el **contador** ("12 estrategias guardadas") y un botón "Borrar todas" con confirmación.
- Guarda también la **fecha** y los umbrales con los que se calculó, para saber si una nota está desactualizada.
- Si cambian los umbrales, **recalcula** desde los datos crudos guardados; no guardes solo la nota.

## 3. Patrón "cola de peticiones"
Una sola petición en vuelo, tiempo máximo (p. ej. 8 s), reintento una vez y cierre limpio. Así sabes a qué petición responde cada `*_RESPONSE`. La plantilla lo implementa: `ask(type, params, expectedResponse)` devuelve una promesa.

## 4. Cálculo de notas (scores)
- Cada métrica se normaliza con **puntos de control** `[[valor, nota], …]` e interpolación lineal, acotada a 0-100. Ejemplo: Profit Factor `[[1.0,0],[1.3,50],[2.0,100]]`.
- Los **pesos** y los **puntos** viven en CONFIG y son editables en pantalla.
- Si falta una métrica, **no cuentes cero**: excluye esa métrica y reparte el peso entre las demás, y muéstralo ("calculado con 4 de 5 métricas").
- Un **filtro duro** (p. ej. drawdown máximo de la cuenta) es distinto de una nota: si lo incumple, marca "No cumple" y explica el motivo, aunque la nota sea alta.
- **Un filtro sin dato no se da por cumplido.** Si falta la métrica del filtro, o falta demasiado peso de las demás (menos del 80 %), el estado máximo es "Revisar" y se dice qué falta. Error real encontrado probando la plantilla: una estrategia sin drawdown salía con nota 99 y "Cumple".
- Siempre muestra **por qué** tiene esa nota: desglose por métrica en tooltip o panel.
- Una nota es una ayuda para ordenar, no una predicción. Escríbelo.

## 5. Tema, idioma y tamaño
- `SET_THEME`: cambia `data-theme` y **repinta todos los canvas**.
- `SET_LANGUAGE`: cambia el diccionario y vuelve a pintar textos y tooltips. Si no tienes ese idioma, cae a inglés.
- `ResizeObserver` en cada canvas; escala por `devicePixelRatio` para que no salga borroso.
- Funciona bien desde 700 px de ancho. Por debajo, tabla con scroll horizontal y columnas clave fijas.

## 6. Tooltips y explicaciones
- Todo lo que no sea obvio para un principiante tiene tooltip: qué es, cómo leerlo (con números), para qué sirve. Máximo 3 líneas.
- Se generan desde CONFIG, no se escriben a mano con números sueltos.
- Si la explicación no cabe, panel de ayuda con botón "?".
- Textos en el diccionario de idiomas.

## 7. Rendimiento
- Pide solo lo que usas. Cada `GET_*` es una petición a SQX.
- Dibuja con `requestAnimationFrame` y no más de una vez por cambio.
- Tablas de más de 200 filas: pinta por tandas o limita con paginación.
- Nada de timers que sigan corriendo con la pestaña oculta.

## 8. Accesibilidad y usabilidad
- Contraste de texto suficiente en tema claro y oscuro (≥ 4.5:1 en texto normal).
- El estado no se comunica solo con color: añade icono o texto ("Cumple" / "No cumple").
- Todo botón con texto o `aria-label`. Foco visible. Se puede usar con teclado.
- Tamaño mínimo de texto 12 px en datos y 11 px en el aviso legal.
- Números con separador y decimales coherentes; porcentajes con `%`; moneda con la unidad que entregue SQX.

## 9. Seguridad y privacidad
- `textContent` o escape para cualquier texto que venga de SQX (nombres de estrategia, comentarios). Nada de `innerHTML` con datos externos.
- Cero `eval`, cero `new Function`, cero scripts remotos.
- No guardes ni muestres claves, rutas personales ni datos de cuentas.
- Si exportas CSV, escapa comillas y evita que una celda empiece por `=`, `+`, `-` o `@` (inyección de fórmulas): antepón una comilla simple.

## 10. Aviso legal (obligatorio)
Último elemento de `#app`, siempre visible, fuera de la zona con scroll. Texto base en inglés (el de SQX) y su versión en español:

> This analysis is provided strictly for informational and educational purposes within StrategyQuant X. It does not constitute financial, investment, or trading advice. All results, including backtests and simulations, are based on historical data and hypothetical performance, which may not reflect future market conditions. Past performance is not indicative of future results. Trading involves substantial risk, and you should conduct your own independent research and consult a licensed financial advisor before making any investment or trading decisions.

> Este análisis se ofrece únicamente con fines informativos y educativos dentro de StrategyQuant X. No constituye asesoramiento financiero, de inversión ni de trading. Todos los resultados se basan en datos históricos y en rendimiento hipotético, que pueden no reflejar las condiciones futuras del mercado. El rendimiento pasado no garantiza resultados futuros. Operar conlleva un riesgo sustancial: haz tu propia investigación y consulta con un asesor financiero autorizado antes de tomar decisiones.

Si el plugin simula, puntúa o clasifica, añade **una frase** con su límite concreto (por ejemplo: "La nota depende de los umbrales que tú has fijado").

## 11. Lista de revisión antes de entregar
- [ ] Lee `STRATEGY_DATA` con validación y soporta campos vacíos
- [ ] Cola de peticiones con tiempo máximo y reintento
- [ ] Estados: esperando, cargando, datos, vacío, dato faltante, error
- [ ] Almacén persistente con contador, borrar y recalcular
- [ ] Umbrales y pesos editables y persistentes
- [ ] Tooltips en todo lo no obvio, generados desde CONFIG
- [ ] Tema claro/oscuro y repintado de canvas
- [ ] Español e inglés mínimo, con caída a inglés
- [ ] `ResizeObserver` y `devicePixelRatio`
- [ ] Nada de red, ni CDN, ni fuentes remotas
- [ ] Escape de datos externos; CSV seguro
- [ ] Aviso legal al final y visible
- [ ] Probado en `mock_sqx.html` con casos raros
- [ ] `validar_plugin.py` sin ERROR
- [ ] Contrastado en SQX real con los mismos números
