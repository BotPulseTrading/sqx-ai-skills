# 01 · Arquitectura plataforma ↔ servidor

## Opciones de conexión
| Opción | Cómo | Cuándo | Ojo con |
|---|---|---|---|
| **EA con WebRequest** (MT4/MT5) | El EA llama a tu API por HTTPS | Enviar estado de la cuenta, operaciones, recibir órdenes | Hay que permitir la URL en Herramientas → Opciones → Asesores Expertos. WebRequest no funciona en el probador de estrategias ni dentro de indicadores. Es síncrono: no bloquees `OnTick` con tiempos largos. |
| **Intercambio por archivos** | Un proceso escribe un archivo y otro lo lee (carpeta Common o Files) | MT4 sin WebRequest estable, copiadores locales entre terminales | Escribe a temporal y renombra (atómico), incluye marca de tiempo y versión, el lector ignora datos viejos. |
| **Servicio local / Python** | Biblioteca oficial de MT5 para Python, o un servicio propio | Procesar, guardar y publicar desde el PC o VPS | Un terminal MT5 por proceso; la sesión de Windows debe seguir abierta; usa VPS para continuidad. |
| **Sockets / ZeroMQ** | Conexión directa de baja latencia | Solo si la latencia importa de verdad | Más piezas que fallar; casi nunca hace falta. |

Regla: elige la opción más simple que cumpla la latencia. Para paneles y monitorización, **sondeo cada 5-30 s** basta.

## Esquema típico
```
[EA / agente en cada cuenta]  --HTTPS-->  [API]  -->  [Base de datos]  -->  [Panel web / app]
          ^                                  |
          +---------- órdenes/ajustes -------+   (el agente las consulta; el servidor no empuja a la cuenta)
```
- El agente **inicia** siempre la conexión (sale por 443). Así no abres puertos en el PC del trader.
- El servidor guarda el **último estado** y un histórico; el panel lee del servidor, no de la cuenta.
- Varias cuentas/clientes: cada registro lleva `tenant_id`/`account_id`; el servidor valida que el token pertenece a ese id.

## Qué enviar (mínimo útil)
Estado de la cuenta (balance, equity, margen, divisa) cada N segundos; operaciones abiertas con su ticket; operaciones cerradas con resultado; latido (heartbeat) con versión del agente y hora. Todo con id único y hora UTC (ver `02-fiabilidad.md`).

## Qué NO hacer
- No enviar la contraseña de la cuenta ni claves del broker. Para un panel de solo lectura basta la **contraseña de inversor** (solo lectura), si el usuario decide usarla; nunca la de trading.
- No ejecutar órdenes recibidas sin validarlas (símbolo permitido, tamaño máximo, firma/autenticación, límite de frecuencia).
- No acoplar el panel a la plataforma: si cambia MT4→MT5, solo cambia el agente.
