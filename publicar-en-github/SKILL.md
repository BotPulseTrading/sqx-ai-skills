---
name: publicar-en-github
description: Publica una skill, plugin o proyecto en GitHub de forma segura. Úsala cuando el usuario quiera subir, publicar, compartir o actualizar una carpeta en GitHub (repositorio nuevo o existente). Escanea secretos y datos privados, valida SKILL.md, prepara README, LICENSE y .gitignore, muestra un resumen previo y solo sube tras la confirmación explícita del usuario.
---

# Publicar en GitHub (con revisión de privacidad)

Subir algo a GitHub es **público y difícil de deshacer** (puede quedar en cachés y forks aunque se borre). Por eso esta skill nunca sube nada sin confirmación y siempre escanea primero.

## Reglas
1. **Nunca manejes ni pegues tokens, contraseñas ni claves.** La autenticación la hace el usuario con `gh auth login` (abre el navegador) o con el Git Credential Manager. Si pide un token, que lo introduzca él en su terminal.
2. **No crees repositorio ni hagas push sin pedir y recibir un "sí" claro** sobre: nombre del repositorio, **público o privado**, y la lista de archivos que se subirán. Un "sí" a otra cosa no vale.
3. **Por defecto, repositorio privado** si el usuario duda. Publicar es un paso aparte y se puede hacer después.
4. Nunca subas con `--force`, ni reescribas historial, ni saltes comprobaciones, salvo petición expresa.
5. Si el escáner da BLOQUEOS, no se sube. Se corrigen (quitar el archivo, mover el secreto a una variable) y se vuelve a escanear. Si un secreto ya estuvo en un commit, hay que **revocarlo/cambiarlo** aunque se borre.

## Flujo

### Paso 1 · Comprobar herramientas
```powershell
git --version
gh --version
gh auth status
```
- Si falta **git**: `winget install --id Git.Git -e` (el usuario lo aprueba) y reabrir la terminal.
- Si falta **gh** (GitHub CLI): `winget install --id GitHub.cli -e`.
- Si no hay sesión: pide al usuario ejecutar `gh auth login` (GitHub.com → HTTPS → navegador). No lo hagas tú con tokens.
- Si no quiere instalar nada: alternativa manual, crear el repositorio en github.com y subir la carpeta con "Add file → Upload files" (límite 100 archivos por subida desde el navegador). Dale esos pasos.

### Paso 2 · Escanear
```powershell
python tools/escanear_antes_de_subir.py "RUTA\CARPETA" --skill
```
(`--skill` solo si es una skill: valida `SKILL.md` y su frontmatter `name` y `description`.)
Lee **todos** los AVISOS con el usuario: rutas personales, correos, IPs. Quita lo que no deba ser público. Los correos de contacto público (canal, soporte) pueden quedarse si el usuario lo decide.

### Paso 3 · Preparar la carpeta
- **README.md** con: qué es, para quién, requisitos, instalación, uso, aviso de estado de pruebas honesto, y créditos/enlace del canal.
- **LICENSE**: pregunta al usuario qué quiere (MIT = libre uso; "todos los derechos reservados" si no quiere que se reutilice). No elijas por él; si no sabe, explica MIT en una frase y propón MIT.
- **.gitignore**: `node_modules/`, `__pycache__/`, `.env`, `*.log`, `*.zip` grandes, carpetas de exportación.
- Material de terceros o de pago (cursos, plugins ajenos, `CLAUDE.md` propietarios): fuera salvo permiso claro.

### Paso 4 · Resumen previo (dry-run) y confirmación
Muestra al usuario, antes de tocar GitHub:
- Nombre propuesto del repo (minúsculas con guiones, ej. `sqx-plugin-pro`) y visibilidad.
- Número de archivos y tamaño, árbol de carpetas resumido.
- Resultado del escáner (bloqueos 0, avisos resueltos o aceptados).
- Mensaje del primer commit.
Pregunta: "¿Creo el repositorio `<nombre>` como `<público|privado>` y subo estos archivos?" y **espera**.

### Paso 5 · Subir (solo tras el sí)
Repositorio nuevo, desde la carpeta:
```powershell
git init -b main
git add .
git status            # revisa lo que entra
git commit -m "Primera versión"
gh repo create NOMBRE --private --source . --remote origin --push   # o --public si confirmó público
```
Repositorio existente: `git remote add origin URL` (o comprobar el que hay) → `git pull --rebase` → `git add` → `git commit` → `git push`. Si hay conflicto, para y pregunta.
Si `git commit` pide identidad, pregunta al usuario qué nombre y correo usar (puede ser el correo `noreply` de GitHub); no uses el de otra persona ni lo inventes.

### Paso 6 · Verificar y entregar
- `gh repo view --web` o abre la URL; confirma que se ve README y archivos.
- Entrega el enlace y di: visibilidad, qué se subió, qué se excluyó y por qué, y los siguientes pasos (releases, etiquetas/topics, cómo instalar la skill).
- Para publicar la skill como descarga: `gh release create v1.0 archivo.zip --title ... --notes ...` (solo con confirmación).

## Actualizar un repo ya publicado
Mismo flujo: escanear → resumen de cambios (`git diff --stat`) → confirmación → commit con mensaje claro → push. Si cambia el comportamiento, sube versión en el README/CHANGELOG.

## Informe final honesto
Di qué se hizo de verdad (comandos que se ejecutaron y su resultado), y si algo no se pudo comprobar (por ejemplo "no se verificó la instalación desde cero").
