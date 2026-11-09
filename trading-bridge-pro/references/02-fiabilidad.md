# 02 · Fiabilidad: que no se dupliquen, no se pierdan y no se bloqueen

## Idempotencia (el mismo mensaje dos veces = un solo efecto)
- Cada mensaje u orden lleva un **id único** generado por quien lo crea. El receptor guarda los ids ya vistos y descarta repetidos.
- En el cliente: el **cerrojo se pone de forma síncrona** antes de enviar (no después de la respuesta), porque un doble clic o un reintento llega antes de que acabe la primera petición.
- Si la comprobación previa ("¿ya existe?") falla, **no envíes a ciegas**: marca como pendiente de verificar. Un estado no terminal significa "en curso", no "reenviar".
- Prueba obligatoria: enviar 2 veces el mismo id y comprobar que hay un solo resultado.

## Colas persistentes con reintentos
- Lo que no se pudo enviar se guarda en disco (no en memoria) y se reintenta con espera creciente (1, 2, 4, 8… s hasta un tope) y límite de intentos.
- **Aviso visible** cuando la cola crece o lleva más de X minutos atascada. Un fallo silencioso es peor que uno ruidoso.
- Orden: respeta el orden por cuenta; las operaciones de una misma posición no se adelantan entre sí.

## Identidad de operaciones
- Identifica por ticket/ID, no por posición en lista ni por precio. Tras un cierre parcial el ticket puede cambiar: guarda la relación ticket viejo → nuevo.
- En copiadores: guarda en la copia el ticket del origen (en el comentario o en una tabla propia) para reconciliar.

## Reconciliación
- Compara periódicamente "lo que debería haber" con "lo que hay".
- **Solo hacia abajo de forma automática**: si la copia tiene de más, se corrige; si falta algo, se avisa o se decide con reglas (puede ser un cierre legítimo).
- Limpia huérfanos y slots ocupados; si no, el sistema se bloquea sin ruido.

## Relojes y zonas horarias
- Todo en **UTC** en el servidor. Convierte a hora local solo al mostrar. La hora del servidor del broker difiere de la tuya: guarda ambos o el desfase.
- Cuidado con el cambio de hora de verano en brokers y con el cierre de día (rollover).
- Compara horas en **minutos totales del día**, no hora y minuto por separado.

## Estados explícitos
Cada objeto con ciclo de vida (orden, tarea, copia) tiene un estado de una lista cerrada (`pendiente`, `enviada`, `confirmada`, `fallida`, `cancelada`) y solo se permiten ciertas transiciones. Lo que no encaja se registra como error, no se ignora.

## Límites y protección
- Límite de frecuencia por cuenta y por IP; tamaño máximo de mensaje; tope de lote y de órdenes simultáneas.
- Interruptor global de pausa y pausa por cuenta, visibles en el panel.
- Validación al leer y **relectura antes de guardar** cuando dos procesos pueden modificar lo mismo (evita carreras).

## Registro
Guarda un log con id de mensaje, cuenta, acción y resultado. Sin claves ni datos personales en el log. Rota archivos por tamaño.
