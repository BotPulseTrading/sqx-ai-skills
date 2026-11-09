# 02 · Checklist de calidad de interfaz

## Contenido y honestidad
- [ ] La pantalla responde a una pregunta concreta y la respuesta está arriba.
- [ ] Cada cifra lleva periodo, unidad y tamaño de muestra.
- [ ] "Sin dato" distinto de cero; nada cuenta como "cumple" sin datos.
- [ ] Riesgos visibles (drawdown, límites, pausa).
- [ ] Aviso legal presente; sin promesas de rentabilidad.
- [ ] Hora de la última actualización y aviso si los datos están viejos.

## Diseño
- [ ] Todo con variables; tema claro y oscuro revisados (incluidos gráficos).
- [ ] Contraste de texto suficiente (mínimo 4,5:1) en ambos temas.
- [ ] Estado nunca solo por color.
- [ ] Alineación de números, mismos decimales por columna.
- [ ] Sin parpadeos al actualizar; transiciones de 120-200 ms como máximo.

## Interacción
- [ ] Todo se maneja con teclado; foco visible; orden de tabulación lógico.
- [ ] Zonas táctiles de 40 px o más en móvil.
- [ ] Acciones destructivas con confirmación (sin `window.confirm` si puede estar bloqueado: usa confirmación en la propia interfaz).
- [ ] Doble clic no duplica envíos.
- [ ] Estados: vacío, cargando, error, sin conexión.

## Adaptación
- [ ] Sin scroll horizontal de página a 360 px de ancho.
- [ ] Tabla que se adapta (columnas clave o tarjetas) en móvil.
- [ ] Español e inglés sin textos cortados.
- [ ] Probado con 0, 1, 50 y 500 elementos y con nombres largos.

## Datos y seguridad
- [ ] Sin claves ni datos personales en el código ni en la URL.
- [ ] Los textos de datos se insertan como texto (no como HTML) para evitar inyección.
- [ ] Exportar CSV neutraliza fórmulas (`=`, `+`, `-`, `@` al inicio de celda).
- [ ] Sin dependencias remotas si la herramienta debe funcionar sin conexión.

## Entrega
- [ ] Instrucciones de uso en lenguaje llano.
- [ ] Informe honesto: qué se probó y qué no.
