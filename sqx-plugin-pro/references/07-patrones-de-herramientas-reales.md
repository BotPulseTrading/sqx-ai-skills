# Patrones de herramientas reales (panel de cuentas, Bridge, prop firms)

Extraídos de proyectos reales del canal: un panel web de cuentas de trading con análisis de prop firms, un agente de backtests para MetaTrader 5 y sus automatizaciones. Aquí solo van los **patrones**; no hay código ni datos del proyecto original. El código reutilizable está en `assets/patrones/` y está probado.

## 1. Que nada se envíe dos veces (idempotencia)
**Qué pasó:** un botón "Actualizar backtest" duplicaba trabajos en la cola. Había tres causas: dos pestañas abiertas continuaban la misma cadena; una comprobación de "ya hay uno" usaba datos viejos tras pulsar Reintentar; y solo se consideraban "en curso" dos estados, no todos los no terminados.
**Patrón:**
1. Antes de crear algo, **leer el estado real** y reutilizar lo que ya exista.
2. Un **cerrojo por clave** activado de forma síncrona, antes de cualquier `await`.
3. "En curso" = **cualquier estado que no sea terminal** (hecho, error, cancelado).
4. Si la lectura de verificación falla, **avisar y no enviar a ciegas**.
→ `Robust.withLock`, `Robust.submitOnce`, `Robust.isInProgress`. Aplícalo a cualquier botón que cree algo, incluida la cola de peticiones del plugin.

## 2. Guardar sin perder nada
**Qué pasó:** las rotaciones marcadas como hechas debían verse desde cualquier navegador; si el servidor no respondía, no podían perderse.
**Patrón:** guardar en el servidor; si falla, **cola local persistente** con reintento al abrir o al actuar, y un **aviso amarillo visible** mientras haya pendientes. Lo guardado solo en local se sube la primera vez.
→ `Robust.makeRetryQueue`. En un plugin sin servidor, la misma idea vale para el almacén local: aviso si el almacenamiento no está disponible.

## 3. Cuánta fe darle a un cálculo (fiabilidad)
**Qué pasó:** se calculaba la correlación entre robots. La pregunta del usuario fue "¿qué fiabilidad tiene ese cálculo?".
**Patrón:** todo cálculo estadístico muestra su **muestra** y un **grado de fiabilidad** (alta, media, baja) según cuántos datos tiene, más un **intervalo de confianza** cuando se pueda. Con pocos datos, se dice.
Ejemplo de cortes que se usaron con series semanales: alta con 150 o más semanas, media con 52 o más, baja por debajo. Ajústalos a tu caso.
→ `Stats.pearson`, `Stats.fisherCI`, `Stats.reliability`, `Stats.bucketSum`, `Stats.weekKey`.

## 4. Mínimos de muestra
Un ranking por robot y símbolo exigió **al menos 30 operaciones**; por debajo no se clasifica. Es la misma lógica de `DegreesOfFreedom`: pocas operaciones no sostienen una nota.
→ En el plugin: si `NumberOfTrades` es bajo, "Revisar" y se explica.

## 5. Simular sin prometer
Se usó **Monte Carlo por remuestreo de días** (150 corridas de 400 días) para ver un rango de resultados y de caídas posibles. Se muestran **percentiles** (p. ej. caída p50 y p95), no una cifra única, y se aclara que es una simulación sobre datos pasados.
→ `Stats.monteCarloDrawdown`. Rechaza series con menos de 20 días.
**Regla:** una proyección económica no supone que todos los meses son positivos; muestra escenarios realistas.

## 6. Recomendar sin abrumar
Un panel confuso se rediseñó con este orden: **la recomendación primero** (una opción clara: qué usar y dónde), y los detalles detrás de un botón "Ver estadísticas". La tabla completa de precios se usaba internamente y solo se mostraba el resultado elegido.
→ Primer pantallazo = respuesta; detalle bajo demanda. Un dato que no se pudo obtener se **excluye con aviso** ("esta cuenta no se tiene en cuenta porque no hay precio"), nunca en silencio.

## 7. Interfaz sin parpadeos ni cortes
- Un carrusel de tarjetas parpadeaba al refrescarse: **solo se repinta si cambió el contenido** (firma del estado).
- Un tooltip se cortaba en los bordes: calcular posición que **quepa en la ventana**.
- Iconos "i" para información, en vez de texto largo; indicador "n de N" en carruseles.
→ `Robust.changed`, `Robust.fitTooltip`.

## 8. Cómo se mantiene un archivo grande
El panel es un solo HTML grande. Se regeneraba con un **script de parche** a partir de una **copia base** más fragmentos, y se hacía copia de seguridad con nombre ("antes de X") antes de cada cambio.
**Regla:** no se edita a mano el resultado final; se cambia el fragmento y se regenera. Así no se pierden cambios.
→ Para plugins grandes: dividir por secciones comentadas (CONFIG, ESTADO, LÓGICA, VISTA), y guardar una copia `.bak` fuera de la carpeta de plugins antes de cambios grandes.

## 9. Automatizaciones que no dependen de la IA
Una revisión periódica de reglas se hizo con scripts del propio servidor, **sin IA**: comparar textos, filtrar ruido, publicar avisos y **validar el resultado** antes de guardarlo. Un fallo real fue una **condición de carrera**: dos procesos escribían el mismo archivo y desaparecía un programa; la solución fue **releer el archivo justo antes de guardar** y validar que no falten elementos.
→ Regla general: leer, modificar y guardar lo más seguido posible; y validar al terminar.

## 10. Pruebas honestas
En esos proyectos, cuando no se pudo probar contra el sistema real (Bridge, PHP, sesión de WordPress), **se dijo claramente** y se pidió al usuario una prueba concreta. Se probó la lógica con simulaciones y se anotó qué faltaba.
→ En cada entrega: "Probado con X, no probado con Y, haz esta comprobación".

## 11. Entorno
- Un proyecto solo debe usar **el equipo desde el que se trabaja**; no tocar otros equipos sin permiso.
- Scripts de PowerShell 5.1: mantener el texto en ASCII para evitar errores de acentos; usar archivos `.ps1` en lugar de comandos largos con comillas.
- Tras publicar una web con caché (Cloudflare), purgar y recargar con Ctrl+F5.
