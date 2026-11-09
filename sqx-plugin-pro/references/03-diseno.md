# Diseño visual de un plugin de SQX

Un plugin de SQX es una herramienta de trabajo (se usa para decidir), no una web de marketing. Prioridad: **leer rápido, comparar fácil y no cansar la vista**. La personalidad va en los detalles, no en el ruido.

## Principios
1. **Jerarquía clara**: un dato protagonista (la nota o la respuesta), los datos de apoyo más pequeños, el resto en gris.
2. **Densidad útil**: muchos números, pero alineados, con la misma unidad y el mismo número de decimales por columna.
3. **Color con significado**: verde = cumple, ámbar = límite, rojo = no cumple. Mismo significado en todo el plugin. No decorar con colores.
4. **Sin sorpresas**: se ve y se comporta como SQX (tema claro u oscuro según el de SQX), no como otra aplicación.
5. **Movimiento mínimo**: transiciones de 120-200 ms para cambios de estado; nada que se mueva solo.

## Tokens (variables CSS)
Define todo en `:root` y `[data-theme="dark"]`. Nunca pongas un color suelto en el código.
```css
:root {
  --bg: #ffffff;        --surface: #f6f7f9;   --surface-2: #eceff3;
  --border: #d9dee6;    --text: #1f2933;      --muted: #6b7785;
  --accent: #2f7fd6;    --ok: #1f9d55;        --warn: #c98a00;   --bad: #d64545;
  --radius: 8px;        --gap: 12px;
}
[data-theme="dark"] {
  --bg: #12161b;        --surface: #1a2027;   --surface-2: #232b34;
  --border: #2e3946;    --text: #e6edf3;      --muted: #8b98a8;
  --accent: #4da3ff;    --ok: #34d399;        --warn: #f5b942;   --bad: #f87171;
}
```
Escala de espacios: 4, 8, 12, 16, 24. Radios: 6 u 8 px. Un solo color de acento.

## Tipografía
- Texto: fuentes del sistema (`system-ui, "Segoe UI", Arial, sans-serif`). No cargues fuentes remotas (SQX va sin conexión).
- Números: `font-variant-numeric: tabular-nums` y, si quieres un toque técnico, `ui-monospace, "Cascadia Mono", Consolas`.
- Tamaños: 12 px datos secundarios, 13-14 px base, 18-22 px título, 28-40 px para la nota principal.
- Etiquetas en mayúsculas pequeñas con `letter-spacing: .04em` solo para cabeceras de tabla.

## Componentes
- **Tarjeta de métrica**: etiqueta (pequeña, gris), valor (grande), unidad y estado (icono + texto).
- **Barra de nota (0-100)**: pista gris, relleno con el color del estado, valor numérico a la derecha. Altura 8-10 px.
- **Tabla**: cabecera fija, filas de 32-36 px, orden por clic con flecha visible, fila seleccionada resaltada, columna de nota alineada a la derecha.
- **Insignia de estado**: "Cumple" / "Revisar" / "No cumple" con icono; nunca solo un punto de color.
- **Panel de ajustes**: plegable, con "Restaurar valores" y vista previa del efecto. Los cambios se aplican al momento.
- **Estado vacío**: icono sencillo, una frase de qué hacer y, si procede, un botón.

## Gráficos en canvas
- Escala por `devicePixelRatio`; redimensiona con `ResizeObserver`.
- Ejes con pocas marcas, rejilla muy tenue, sin 3D, sin gradientes llamativos.
- Colores desde las variables CSS leídas con `getComputedStyle`, para que el tema oscuro funcione.
- Etiqueta directa en la serie en vez de leyendas lejanas cuando sea posible.
- Repinta en `SET_THEME` y en cambio de tamaño.
- Si el gráfico no se entiende en 3 segundos, simplifícalo.

## Texto de la interfaz
- Verbos claros: "Guardar", "Recalcular", "Copiar CSV". Nada de "Aceptar".
- Mensajes de error: qué pasó, por qué, qué hacer ("SQX no respondió en 8 s. Selecciona la estrategia otra vez.").
- Tono neutro y sin promesas: "Encaja con tus reglas", no "Estrategia ganadora".

## Prueba visual (hazla siempre)
Revisa el plugin en: tema claro y oscuro; ancho 700 px y 1200 px; 0, 1 y 50 estrategias; con datos faltantes; con textos largos (nombres de estrategia de 60 caracteres). Corrige todo lo que se corte, se solape o parpadee antes de entregar.

## Si tienes la skill `impeccable`
Úsala sobre el plugin ya funcional: `critique` para revisión de UX, `polish` para el repaso final y `harden` para bordes y errores. Sus reglas son para webs; en un plugin de SQX prevalece lo de arriba (modo "Operate": claridad y precisión por encima de la expresión).
