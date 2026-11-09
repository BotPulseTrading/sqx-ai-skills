# Mensajes para pedirle un plugin a Claude

Copia, rellena lo que va entre corchetes y envía. Funcionan en Claude Code (abre la carpeta `ResultsPlugins` de tu SQX) o en el chat (adjunta el `CLAUDE.md` de esa carpeta).

## Mensaje 1 · Objetivo
```
Quiero crear un plugin para la pestaña de Resultados de StrategyQuant X.
Lee primero el archivo CLAUDE.md de esta carpeta y úsalo como única fuente sobre cómo se comunican los plugins.
El plugin debe responder a esta pregunta: [¿qué quiero ver que SQX no me muestra?].
Usa la skill sqx-plugin-pro y sigue su flujo. Antes de escribir código, devuélveme la spec en 5 líneas y espera mi confirmación.
```

## Mensaje 2 · Reglas y valores
```
Estas son mis reglas y valores de ejemplo (puedo cambiarlos después en pantalla):
- Métricas que quiero usar: [ProfitFactor, ReturnDDRatio, PctDrawdown...]
- Qué es bueno, aceptable y malo para cada una: [valores]
- Límites que no se pueden incumplir: [por ejemplo, drawdown máximo]
- Qué decisión voy a tomar con el resultado: [...]
No inventes umbrales: si falta alguno, pregúntamelo.
```

## Mensaje 3 · Qué quiero ver
```
Quiero ver: [una tabla ordenable / una nota de 0 a 100 / un gráfico de... ].
Cada métrica que no sea obvia lleva tooltip con qué es, cómo leerla y para qué sirve.
Quiero poder cambiar los umbrales en pantalla, que se guarden y que todo se recalcule.
Quiero copiar el resultado como CSV.
Idiomas: español e inglés. Tema claro y oscuro según SQX.
```

## Mensaje 4 · Guardar todas las estrategias
```
SQX entrega una estrategia cada vez. Haz que el plugin guarde cada una al recibirla,
muestre cuántas hay guardadas, permita borrarlas (con confirmación) y recalcule al cambiar los umbrales.
```

## Mensaje 5 · Pruebas y errores
```
Ejecuta el validador de la skill y prueba el plugin con el simulador mock_sqx.html.
Cuéntame qué falló y qué corregiste. No me digas que está listo hasta que el validador no marque ningún ERROR.
```

## Cuando algo falla
```
Al probar el plugin en SQX me sale este error: [pega el texto exacto o describe lo que ves].
Corrige solo eso, explícame en una frase qué pasaba y vuelve a ejecutar el validador.
```

## Para pulir
```
Revisa el plugin con la lista de revisión de la skill (estados, tooltips, tema, idiomas, aviso legal)
y dime qué falta antes de usarlo con mis estrategias.
```

## Para entender lo que hizo
```
Explícame por qué cada estrategia tiene su nota, con un ejemplo concreto.
Si no lo entiendo, no me fío del resultado.
```
