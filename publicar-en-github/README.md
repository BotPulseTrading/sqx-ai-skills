# Publicar en GitHub

Skill del canal **Bot Pulse Trading**. Hace que Claude suba una skill o proyecto a GitHub con cabeza: escanea secretos y datos privados, valida `SKILL.md`, prepara README/LICENSE/.gitignore, te enseña un resumen y **solo sube si tú dices que sí**.

## Instalación
Copia la carpeta `publicar-en-github` a `%USERPROFILE%\.claude\skills\` y pide: `Usa la skill publicar-en-github para subir esta carpeta`.

## Requisitos
Git y GitHub CLI (`winget install Git.Git` y `winget install GitHub.cli`). Inicias sesión tú con `gh auth login`; la skill nunca toca tus claves.

## Escáner suelto
```
python tools/escanear_antes_de_subir.py RUTA --skill
```
Solo lee archivos. Busca claves/tokens, rutas personales, correos, IPs privadas, archivos sensibles y archivos grandes.

Estado de las pruebas: el escáner se probó con datos falsos; el flujo con `gh` depende de tu instalación y no se ha ejecutado contra tu cuenta.
