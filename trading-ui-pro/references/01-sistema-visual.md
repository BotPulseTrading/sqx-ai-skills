# 01 · Sistema visual

## Tokens (define todo en variables; nunca un color suelto)
```css
:root {
  --bg:#ffffff; --surface:#f6f7f9; --surface-2:#eceff3; --border:#d9dee6;
  --text:#1f2933; --muted:#6b7785; --accent:#2f7fd6;
  --ok:#1f9d55; --warn:#c98a00; --bad:#d64545;
  --radius:8px; --gap:12px;
}
[data-theme="dark"] {
  --bg:#12161b; --surface:#1a2027; --surface-2:#232b34; --border:#2e3946;
  --text:#e6edf3; --muted:#8b98a8; --accent:#4da3ff;
  --ok:#34d399; --warn:#f5b942; --bad:#f87171;
}
```
Espacios 4/8/12/16/24. Un solo color de acento. Tema inicial según `prefers-color-scheme`, con selector manual guardado.

## Tipografía
Fuentes del sistema. Números con `font-variant-numeric: tabular-nums` para que las columnas alineen. Tamaños: 12 datos secundarios, 14 base, 18-22 título, 28-40 dato protagonista.

## Componentes base
- **Tarjeta de métrica:** etiqueta pequeña, valor grande, unidad, variación y estado (icono + texto).
- **Barra de límite:** muestra cuánto se ha consumido de un límite (drawdown diario/total) con umbrales ámbar y rojo.
- **Tabla:** cabecera fija, orden por clic, filas de 32-36 px, números a la derecha con los mismos decimales por columna, fila seleccionada visible.
- **Insignia de estado:** "Cumple / Revisar / No cumple / Sin dato" con icono.
- **Panel de ajustes:** plegable, con "Restaurar valores" y cambios inmediatos; los umbrales editables se guardan por usuario.
- **Aviso de datos viejos:** hora de la última actualización; se vuelve ámbar si pasa de N minutos y rojo si el agente no da señales.

## Gráficos
- Curva de equity/balance: línea fina, área suave, marcador de drawdown máximo; eje con fechas legibles.
- Barras para resultados por día/semana; verde y rojo con el mismo significado en toda la app.
- Etiqueta de valor al pasar el ratón y tooltip que **cabe en el viewport** (no se corta en los bordes).
- Repinta solo cuando cambia una firma de los datos o el tema; redimensiona con `ResizeObserver` y escala por `devicePixelRatio`.
- Accesible: resumen en texto del gráfico (`aria-label`) y tabla alternativa.

## Recomendación primero (patrón de pantalla)
```
┌ Estado: "2 cuentas en riesgo hoy"  [Ver cuáles] ┐
├ Tarjetas: Equity · Drawdown hoy · Límite diario ┤
├ Tabla de cuentas (ordenable, con insignias)     ┤
└ Detalle desplegable + aviso legal               ┘
```

## Internacionalización
Textos en un objeto por idioma, no repartidos por el HTML. Mínimo español e inglés. Formatea números y fechas con `Intl` según el idioma. Deja holgura: el inglés/alemán ocupa más.

## Rendimiento
Listas largas con paginación o virtualización. Actualiza solo las filas que cambian. Agrupa las peticiones y usa sondeo con intervalo razonable (5-30 s).
