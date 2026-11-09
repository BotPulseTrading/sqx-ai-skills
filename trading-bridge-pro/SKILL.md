---
name: trading-bridge-pro
description: Diseña y construye software de trading conectado a servidores, como un puente MT5 con una API web, un copiador de operaciones, un panel de cuentas, un monitor o un agente de backtests. Úsala cuando el usuario quiera vincular MetaTrader (MT4/MT5), StrategyQuant u otro programa de trading con un servidor, una web o una app, o enviar y recibir datos de cuentas, operaciones y señales de forma fiable y segura.
---

# Trading Bridge Pro — software de trading vinculado a servidores

Skill del canal Bot Pulse Trading. Resume cómo construir puentes entre plataformas de trading y servidores sin duplicar órdenes, perder mensajes ni exponer claves. Parte de patrones que fallaron en proyectos reales.

## Reglas que mandan
1. **Seguridad primero.** Ninguna clave, token ni contraseña dentro del código, del repositorio ni de un chat. Van en variables de entorno o archivo de configuración fuera del repositorio. Si el usuario pega una clave, avísale de que debe revocarla y crear otra.
2. **Dinero real = riesgo real.** Todo lo que pueda abrir, cerrar o modificar operaciones se prueba primero en cuenta demo con tamaño mínimo, y nunca se activa en real sin que el usuario lo ordene explícitamente. Pon un interruptor global de pausa visible.
3. **Nunca prometas resultados** ni des consejo de inversión. Estas herramientas ejecutan y muestran; no garantizan nada.
4. **Honestidad de pruebas.** Di siempre qué se probó (demo, simulador, prueba unitaria) y qué no (broker real, picos de carga, desconexiones).
5. **No edites software de terceros** (plugins de WordPress, bibliotecas, la plataforma). Se extiende con código propio.
6. **Cumplimiento.** Respeta los términos de la plataforma, del broker y de las empresas de cuentas de capital; algunos prohíben copiadores o ciertas automatizaciones. Pídele al usuario la regla vigente y no la supongas.

## Flujo
### Paso 1 · Spec en 6 líneas
Qué datos viajan y en qué sentido (cuenta→servidor, servidor→cuenta, ambos) · cuántas cuentas y plataformas · latencia aceptable · qué pasa si se corta la conexión · quién puede ver y quién puede ordenar · qué NO hace la primera versión.

### Paso 2 · Arquitectura (elige la más simple que sirva)
Ver `references/01-arquitectura.md`: EA/agente ↔ API ↔ base de datos ↔ panel. Decide: sondeo (polling) o push, formato de mensajes, identidad de operaciones, autenticación.

### Paso 3 · Contrato de mensajes
Define por escrito cada mensaje: campos, tipos, unidades, versión, id único (idempotencia) y marca de tiempo UTC. El contrato se escribe antes que el código y se prueba con ejemplos buenos y malos.

### Paso 4 · Construir en capas y probar cada una
Lado plataforma (EA/script) → API → persistencia → panel. Cada capa con su prueba. Usa `references/02-fiabilidad.md` (idempotencia, colas, reintentos, reconciliación) y `references/03-seguridad-y-despliegue.md`.

### Paso 5 · Prueba de fallos (obligatoria)
Corta la red a mitad, envía el mismo mensaje dos veces, apaga el servidor y vuélvelo a encender, manda datos incompletos, reloj desfasado. Anota el resultado de cada uno. Plantilla en `references/04-checklist-de-fallos.md`.

### Paso 6 · Entrega
Instrucciones de instalación en lenguaje llano, cómo pausar todo, cómo ver errores, qué probar primero en demo, y las limitaciones. Si todo va a GitHub, usa la skill `publicar-en-github` (escáner de secretos antes de subir).

## Referencias
| Archivo | Para qué |
|---|---|
| `references/01-arquitectura.md` | Patrones de conexión plataforma↔servidor y cuándo usar cada uno |
| `references/02-fiabilidad.md` | Idempotencia, colas, reintentos, reconciliación, relojes |
| `references/03-seguridad-y-despliegue.md` | Autenticación, claves, WordPress/REST, despliegue atómico, copias |
| `references/04-checklist-de-fallos.md` | Pruebas de fallo y definición de "hecho" |
| `references/05-modelo-de-datos-mt5.md` | Cuenta, posición, orden, deal y símbolo de MT5; netting/hedging; cómo calcular resultados sin errores |
| `references/06-reglas-cuentas-capital.md` | Modelar límites diarios, drawdown estático/trailing y rotación de bots en cuentas de fondeo (reglas siempre como configuración) |
| `references/07-ecosistema-real-ea-web-cola-agente.md` | Mapa de un sistema real: EA→web→panel/app, cola de trabajos con agente en el PC, watchdog, 12 bugs corregidos y lista de revisión |
| `assets/contrato-mensajes.md` | Plantilla de contrato de mensajes |

Para plugins de resultados de StrategyQuant X usa `sqx-plugin-pro`; para el diseño de paneles, `trading-ui-pro`.

