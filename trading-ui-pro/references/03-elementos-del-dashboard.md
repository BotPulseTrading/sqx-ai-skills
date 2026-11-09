# 03 · Elementos de un dashboard de cuentas de trading

Catálogo de piezas para construir paneles que consumen los datos de un puente MT5 (ver `trading-bridge-pro`). Para cada pieza: qué responde, qué datos usa y su trampa.

| Pieza | Responde | Datos | Trampa |
|---|---|---|---|
| **Tarjeta de cuenta** | ¿Cómo está esta cuenta ahora? | balance, equity, flotante, estado de conexión, hora de último dato | Mostrar datos viejos como actuales: siempre la hora de actualización |
| **Barra de límite diario** | ¿Cuánto margen me queda hoy? | equity vivo, referencia de inicio de día, pérdida diaria máx. | Reinicio de día en la zona horaria equivocada |
| **Barra de drawdown total** | ¿Estoy cerca del límite total? | pico, tipo de drawdown, límite | Pico recalculado del historial en vez de guardado |
| **Progreso al objetivo** | ¿Cuánto falta para pasar la fase? | beneficio neto, objetivo, días de trading | Contar depósitos como beneficio |
| **Curva de equity** | ¿Cómo evolucionó? | serie de equity/balance | Series con huecos que parecen caídas |
| **Calendario de resultados** | ¿Qué días ganó/perdió? | resultado por día cerrado | Zona horaria del día |
| **Tabla de operaciones** | ¿Qué hizo cada bot? | deals agrupados por posición | Contar deals como operaciones |
| **Resumen por bot (magic)** | ¿Qué bot rinde? | profit factor, % acierto, racha, muestra | Notas con pocas operaciones |
| **Matriz bot × cuenta** | ¿Dónde conecto cada bot? | rendimiento, margen libre, correlación | Recomendar sin mostrar el motivo |
| **Alertas** | ¿Qué requiere acción? | umbrales de límite, desconexión, cola atascada | Demasiadas alertas: prioriza y agrupa |
| **Estado del puente** | ¿Llegan los datos? | latido, cola, errores, versión del agente | Ocultar fallos del puente |
| **Control de pausa** | ¿Puedo detener todo ya? | interruptor global y por cuenta | Pausa sin confirmación visual de que surtió efecto |
| **Ajustes de reglas** | ¿Qué reglas usa cada cuenta? | parámetros de la firma por cuenta | Valores fijos en el código |

## Composición recomendada (recomendación primero)
1. **Franja de estado**: "N cuentas en riesgo hoy / todo en orden", con enlace a cuáles.
2. **Tarjetas de cuenta** ordenadas por riesgo (menos margen primero).
3. **Detalle de la cuenta seleccionada**: barras de límite, curva, operaciones.
4. **Matriz de bots** y **estado del puente** en pestañas secundarias.

## Semáforos
Verde < 50 % del límite consumido · ámbar 50-80 % · rojo > 80 % (configurable). Siempre con el porcentaje y el importe restante en texto.

## Multi-cuenta y multi-cliente
Un selector de cuenta persistente; en multi-cliente, el servidor filtra por `tenant_id` (nunca el panel). Permisos de solo lectura por defecto.

## Actualización
Sondeo cada 5-30 s con aviso si falla; no repintes todo, solo lo que cambió; guarda la última vista válida y márcala como "desactualizada" si la conexión cae.

## Datos de prueba
Genera un conjunto sintético con: cuenta al límite, cuenta desconectada, racha de pérdidas, depósito a mitad de día, cierre parcial, bot con 3 operaciones (muestra pequeña) y bot con 300. Así se revisan todos los estados antes de usar datos reales.
