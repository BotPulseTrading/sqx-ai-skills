# 03 · Seguridad y despliegue

## Claves y secretos
- Nunca en el código, en el repositorio ni en capturas. Usa variables de entorno o un archivo de configuración fuera del repositorio (y en `.gitignore`).
- Una clave por cuenta/cliente, revocable de forma individual. Se guarda **hasheada** en el servidor cuando sea posible.
- Si una clave se filtró (aunque se borre del commit), **se revoca y se crea otra**. Borrar no basta.
- Antes de subir a GitHub, pasa el escáner de la skill `publicar-en-github`.

## Autenticación de la API
- HTTPS siempre. Token en cabecera, comparado en tiempo constante, con caducidad si es posible.
- **WordPress/REST:** la sesión del navegador usa *nonce*; las aplicaciones usan token. No mezcles ambos en el mismo endpoint sin probarlo. Si un plugin de terceros (por ejemplo, de JWT) intercepta la cabecera `Authorization`, usa una **cabecera propia** para tu token.
- Autoriza **por recurso**: que un token válido de la cuenta A nunca pueda leer ni ordenar sobre la cuenta B.
- Limita permisos: un token de solo lectura no puede enviar órdenes.

## Multi-cliente
- Todo registro lleva `tenant_id`; toda consulta lo filtra en el servidor (no en el panel).
- Pruebas obligatorias de aislamiento: pedir datos de otro cliente con un token válido debe dar 403/404.
- Respeta la privacidad: si hay datos de pacientes, clientes u otros datos personales, minimiza lo guardado y no los pongas en logs.

## Despliegue
- **Reemplazo atómico:** sube la versión nueva a una carpeta aparte y cambia por renombrado; mover archivo a archivo deja huecos en los que se pierden mensajes reales.
- Conserva una **copia con nombre** de la versión anterior para volver atrás en un minuto.
- Despliega primero en un entorno de pruebas o con una cuenta demo; activa en producción en un momento tranquilo (fuera de la apertura de mercados y de noticias).
- Las unidades de red mapeadas (letras de disco) no existen para procesos del servidor ni tareas programadas: usa rutas UNC o copia local.
- Documenta cómo **volver atrás** antes de desplegar.

## Apps para escritorio o móvil
- Una app que envuelve la web (WebView/Electron) es más rápida de entregar y de mantener que una nativa. Una sola app para todos los clientes con configuración por cliente.
- Firma y versiona; actualiza con aviso. Declara qué se probó (emulador o dispositivo real).

## Monitorización
- Latido de cada agente; alerta si falta más de N minutos.
- Panel de estado: cola pendiente, último mensaje recibido, errores recientes, versión de cada agente.
- Arreglos automáticos solo si son seguros e idempotentes (reiniciar una cola, limpiar un huérfano); lo demás se avisa.
