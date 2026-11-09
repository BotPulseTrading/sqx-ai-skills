# Lecciones de herramientas reales de trading

Aprendidas construyendo un conector para MetaTrader 5, un panel web de cuentas y un agente local de backtests (proyectos del canal Bot Pulse Trading). No hay código ni claves aquí: solo lo que se aplica a cualquier herramienta de este tipo.

## 1. Estado visible siempre
Una herramienta que depende de otra (SQX, MetaTrader, un servicio) debe decir **en qué estado está**: conectada, sin datos, esperando, con error. Un banner de salud arriba con una frase ("Sin datos desde hace 90 s") evita el "¿está rota o está pensando?".
→ En un plugin: línea de estado fija con "Esperando estrategia / Leyendo 2 de 3 / 12 guardadas".

## 2. Los errores se explican, no se vuelcan
Cuando algo falla, el usuario necesita saber **qué pasó y qué hacer**, no un código. Mantén una función que traduzca errores técnicos a frases claras.
Ejemplo real: una API de SQX respondió "acceso remoto desactivado"; el mensaje útil es "Activa el acceso remoto en la configuración de SQX".
→ Todos los errores del plugin pasan por una función `explain(error)` con textos en el diccionario.

## 3. Lo largo se hace por pasos y se puede reanudar
Los procesos de varios pasos (varias peticiones, una cadena de tareas) guardan su progreso. Si se corta, continúan donde iban y muestran "paso 2 de 4".
→ En un plugin: la cola de peticiones muestra el avance y un fallo en un paso no tira los demás.

## 4. Separa configuración de lógica
Las reglas (umbrales, límites, catálogos) viven en datos que se editan y validan sin tocar el código. Un archivo de reglas con un validador evitó muchos errores al actualizar.
→ En un plugin: bloque CONFIG arriba, editable en pantalla y persistente; el código solo lo lee.

## 5. Valida los datos al entrar
Todo dato externo puede venir vacío, fuera de rango o en otro formato. Valida al recibirlo y marca lo dudoso; no dejes que un `null` llegue a un cálculo.
→ `isValidStrategy`, tratar `null` y `-99999999` como "sin dato", comprobar rangos de umbrales.

## 6. Versiona antes de cambiar
Las herramientas con muchos cambios acumulan copias de seguridad con fecha. Hazlas **antes** de cada cambio importante y con un nombre que diga qué cambió ("antes de Alertas"). Permite volver atrás en un minuto.
→ Antes de modificar un plugin ya entregado, copia `index.html` como `index.AAAAMMDD.bak.html` fuera de la carpeta de plugins (SQX cargaría la copia).

## 7. Una pantalla = una decisión
El panel que más se usa es el que responde rápido a una pregunta concreta (¿cómo van mis cuentas? ¿cuál conecto?). Las funciones extra van en pestañas o paneles plegables, no en la pantalla principal.

## 8. Comparar contra la realidad
Lo más valioso de un panel de cuentas fue comparar **backtest contra real** con diferencias en %. Comparar con una referencia externa detecta errores que ningún test interno ve.
→ Siempre pide al usuario contrastar los números del plugin con los de SQX antes de fiarse.

## 9. Alertas con límites claros
Cuando una herramienta avisa (por ejemplo, por drawdown), cada límite tiene: valor, tipo (porcentaje o importe), acción (solo avisar o actuar) y registro de lo que pasó. Nada de avisos sin explicación.
→ Un plugin que marca "No cumple" siempre dice qué regla y qué valor.

## 10. Seguridad por defecto
- Claves y contraseñas nunca van en el código ni en el chat; se piden como entradas y se guardan fuera.
- Un usuario solo ve lo suyo.
- Todo lo que se guarda en el navegador se considera visible para quien use ese equipo.
- Toda herramienta que toca dinero o datos de cuentas necesita un aviso claro y no debe actuar sin confirmación.

## 11. Compatibilidad de entorno
- Probar en el entorno real (versión concreta de SQX, Windows, MetaTrader 5) y anotar qué versión se usó.
- Rutas con espacios, acentos y unidades distintas rompen scripts: usa rutas entre comillas y nunca las escribas a mano en el código.
- Archivos de texto en UTF-8 sin BOM cuando una herramienta es estricta con el formato.
