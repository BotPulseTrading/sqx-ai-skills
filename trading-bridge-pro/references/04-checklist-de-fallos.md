# 04 · Checklist de fallos y "hecho"

## Pruebas de fallo (anota resultado de cada una)
| # | Prueba | Debe pasar |
|---|---|---|
| 1 | Enviar el mismo mensaje/orden dos veces | Un solo efecto |
| 2 | Doble clic rápido en "enviar" | Un solo envío |
| 3 | Cortar la red a mitad de un envío | Queda en cola y se reintenta; aviso visible |
| 4 | Apagar el servidor 10 min y encenderlo | Se recupera sin duplicar ni perder |
| 5 | Reiniciar el agente/terminal con operaciones abiertas | Reconcilia sin abrir ni cerrar de más |
| 6 | Mensaje incompleto, campo nulo, número fuera de rango | Rechazado con motivo; no rompe el proceso |
| 7 | Reloj del servidor adelantado/atrasado | Se detecta o no afecta |
| 8 | Token de otra cuenta, caducado o ausente | 401/403; no se filtran datos |
| 9 | Cola crece sin parar | Alerta y límite |
| 10 | Pausa global activada | No se ejecuta ninguna orden |
| 11 | Cierre parcial de una posición | El ticket nuevo se relaciona con el anterior |
| 12 | Símbolo con nombre distinto en otro broker (sufijo) | Mapeo configurable o rechazo claro |

## Fallos típicos de EAs (MQL4/MQL5) a revisar
Comparar hora y minuto por separado · banderas "una vez al día" sin reiniciar · rango calculado con la vela en formación · lote sin redondear al `LotStep` · precios sin normalizar al `TickSize` · distancia mínima de stops/freeze · inputs que no se usan · objetos gráficos sin borrar en `OnDeinit` · reintentos sin tope · `WebRequest` bloqueado por no permitir la URL.

## Definición de "hecho"
- [ ] Contrato de mensajes escrito y probado con ejemplos buenos y malos.
- [ ] Tabla de pruebas de fallo completada (con resultado real, no supuesto).
- [ ] Probado en demo con tamaño mínimo; nada activado en real.
- [ ] Interruptor de pausa global y por cuenta funcionando.
- [ ] Sin claves en el código ni en el repositorio (escáner pasado).
- [ ] Aislamiento entre cuentas/clientes comprobado.
- [ ] Instrucciones de instalación, de vuelta atrás y de monitorización.
- [ ] Informe honesto de lo que NO se probó.
