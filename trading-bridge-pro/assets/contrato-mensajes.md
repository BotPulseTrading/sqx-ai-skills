# Plantilla de contrato de mensajes

Copia, rellena y confirma con el usuario **antes** de escribir código.

## Reglas generales
- Formato: JSON, UTF-8. Hora: ISO 8601 en UTC (`2026-01-31T14:05:00Z`).
- Cada mensaje: `id` (único), `v` (versión del contrato), `account_id`, `ts`.
- Números como números (no texto), con la unidad en el nombre si hay duda (`profit_usd`, `lots`).

## Mensaje: `heartbeat`
```json
{ "id": "uuid", "v": 1, "account_id": "A1", "ts": "…Z", "type": "heartbeat",
  "agent_version": "1.0.3", "platform": "MT5", "server_time": "…" }
```
Respuesta: `{ "ok": true, "server_time": "…Z", "paused": false }`

## Mensaje: `account_state`
```json
{ "id": "uuid", "v": 1, "account_id": "A1", "ts": "…Z", "type": "account_state",
  "balance": 1000.0, "equity": 1012.5, "margin": 20.0, "currency": "USD" }
```

## Mensaje: `trade_closed`
```json
{ "id": "uuid", "v": 1, "account_id": "A1", "ts": "…Z", "type": "trade_closed",
  "ticket": 123456, "symbol": "XAUUSD", "side": "sell", "lots": 0.10,
  "open_time": "…Z", "close_time": "…Z", "open_price": 0.0, "close_price": 0.0,
  "profit": 0.0, "commission": 0.0, "swap": 0.0 }
```

## Errores
`400` datos inválidos (con `field` y `reason`) · `401` sin token · `403` token de otra cuenta · `409` id repetido (se trata como éxito idempotente) · `429` límite de frecuencia · `5xx` reintentar con espera.

## Idempotencia
Un `id` repetido devuelve el mismo resultado que la primera vez y **no** crea otro registro.

## Cambios del contrato
Cualquier campo nuevo sube `v`. El servidor acepta la versión anterior durante un periodo y avisa del cambio.
