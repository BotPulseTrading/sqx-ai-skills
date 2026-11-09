#!/usr/bin/env python3
"""Escáner previo a subir una carpeta a GitHub. Solo lee; no modifica ni sube nada.
Uso: python escanear_antes_de_subir.py RUTA_CARPETA [--skill]
Sale con código 1 si hay BLOQUEOS (secretos, claves, datos privados)."""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
BIN_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".zip", ".mp4", ".mp3", ".wav",
           ".woff", ".woff2", ".ttf", ".otf", ".pdf", ".ex4", ".ex5", ".exe", ".dll"}
RISKY_NAMES = (".env", "id_rsa", "id_ed25519", ".pem", ".pfx", ".p12", ".kdbx", ".sqlite", ".db",
               "credentials", "secrets", "wp-config.php", ".htpasswd")
BIG = 5 * 1024 * 1024  # GitHub avisa a 50 MB y bloquea a 100 MB; aquí avisamos a 5 MB

SECRETS = [
    ("Token de GitHub", r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    ("Token de GitHub (fino)", r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    ("Clave de API tipo sk-", r"\bsk-[A-Za-z0-9_\-]{20,}\b"),
    ("Clave de AWS", r"\bAKIA[0-9A-Z]{16}\b"),
    ("Clave de Google", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("Token de Slack", r"\bxox[baprs]-[A-Za-z0-9\-]{10,}\b"),
    ("Token de Telegram", r"\b\d{8,10}:[A-Za-z0-9_\-]{35}\b"),
    ("Clave privada", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("Contraseña asignada", r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"][^'\"\s]{6,}['\"]"),
]
PRIVATE = [
    ("Ruta personal de Windows", r"(?i)\b[A-Z]:\\Users\\[^\\\s\"']+"),
    ("Ruta personal de Linux/Mac", r"(?:/home|/Users)/[A-Za-z0-9_.\-]+/"),
    ("Correo electrónico", r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    ("IP privada", r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"),
]
ALLOW_MAIL = re.compile(r"(?i)(example\.(com|org)|noreply@|tu@|usuario@|name@)")


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            yield os.path.join(d, f)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    is_skill = "--skill" in sys.argv
    if not args or not os.path.isdir(args[0]):
        print("Uso: python escanear_antes_de_subir.py RUTA_CARPETA [--skill]")
        sys.exit(2)
    root = os.path.abspath(args[0])
    block, warn, info = [], [], []
    n = 0
    total = 0
    for p in walk(root):
        n += 1
        rel = os.path.relpath(p, root)
        name = os.path.basename(p).lower()
        size = os.path.getsize(p)
        total += size
        if any(name == r or name.endswith(r) for r in RISKY_NAMES):
            block.append(f"Archivo sensible por su nombre: {rel}")
        if size > BIG:
            warn.append(f"Archivo grande ({size//1024//1024} MB): {rel} (¿debe ir al repositorio?)")
        if os.path.splitext(name)[1] in BIN_EXT:
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        for label, rx in SECRETS:
            for m in re.finditer(rx, text):
                line = text.count("\n", 0, m.start()) + 1
                block.append(f"{label}: {rel}:{line}")
        for label, rx in PRIVATE:
            for m in re.finditer(rx, text):
                if label == "Correo electrónico" and ALLOW_MAIL.search(m.group(0)):
                    continue
                line = text.count("\n", 0, m.start()) + 1
                warn.append(f"{label}: {rel}:{line}  →  {m.group(0)[:60]}")

    names = {os.path.basename(p).lower() for p in walk(root)}
    for need, msg in (("readme.md", "Falta README.md"), ("license", "Falta LICENSE (sin licencia nadie puede reutilizarlo legalmente)")):
        if need not in names and not any(x.startswith(need) for x in names):
            warn.append(msg)
    if ".gitignore" not in names:
        info.append("No hay .gitignore (conviene crear uno antes del primer commit)")
    if is_skill:
        sk = os.path.join(root, "SKILL.md")
        if not os.path.isfile(sk):
            block.append("Falta SKILL.md en la raíz de la skill")
        else:
            head = open(sk, encoding="utf-8", errors="ignore").read(4000)
            m = re.match(r"---\s*\n(.*?)\n---", head, re.S)
            if not m:
                block.append("SKILL.md sin frontmatter (---)")
            else:
                fm = m.group(1)
                if not re.search(r"(?m)^name:\s*\S+", fm):
                    block.append("Frontmatter sin 'name'")
                if not re.search(r"(?m)^description:\s*\S+", fm):
                    block.append("Frontmatter sin 'description'")

    print(f"Carpeta: {root}\nArchivos: {n}   Tamaño total: {total/1024:.0f} KB\n")
    for title, items in (("BLOQUEOS (no subir hasta resolver)", block), ("AVISOS (revisar uno a uno)", warn), ("INFO", info)):
        print(f"== {title}: {len(items)}")
        for it in items[:60]:
            print("  -", it)
        if len(items) > 60:
            print(f"  ... y {len(items)-60} más")
    print()
    if block:
        print("RESULTADO: NO subir. Hay bloqueos.")
        sys.exit(1)
    print("RESULTADO: sin bloqueos. Revisa los avisos y confirma con el usuario antes de subir.")


if __name__ == "__main__":
    main()
