#!/usr/bin/env python3
"""Validador de calidad para plugins de StrategyQuant X (skill sqx-plugin-pro).

Uso:  python validar_plugin.py ruta/al/index.html
Sale con código 1 si hay algún ERROR. Los AVISO no bloquean, pero conviene leerlos.
Solo analiza texto: no ejecuta el plugin.
"""
import re
import sys
from pathlib import Path


def main(path_arg):
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # que los acentos se vean bien en la consola de Windows
    except Exception:
        pass
    p = Path(path_arg)
    if p.is_dir():
        p = p / "index.html"
    if not p.exists():
        print(f"ERROR: no existe {p}")
        return 1
    src = p.read_text(encoding="utf-8", errors="replace")
    low = src.lower()
    errores, avisos, bien = [], [], []

    def check(cond, ok, msg, nivel="ERROR"):
        if cond:
            bien.append(ok)
        else:
            (errores if nivel == "ERROR" else avisos).append(msg)

    # --- Estructura y comunicación con SQX
    check(p.name.lower() == "index.html", "El archivo se llama index.html",
          "El archivo debe llamarse index.html (SQX solo detecta ese nombre).")
    check("addeventlistener('message'" in low.replace('"', "'") or "addeventlistener('message'" in low.replace(" ", ""),
          "Escucha mensajes de SQX", "No se encuentra window.addEventListener('message', ...): el plugin no recibe nada de SQX.")
    check("strategy_data" in low, "Gestiona STRATEGY_DATA", "No gestiona el mensaje STRATEGY_DATA.")
    check(re.search(r"\.trim\(\)", src) is not None and "strategyname" in low,
          "Valida STRATEGY_DATA (trim)", "No parece validar projectName/databankName/strategyName con trim() antes de pedir datos.")
    check("set_theme" in low, "Gestiona SET_THEME", "No gestiona SET_THEME: no seguirá el tema claro/oscuro de SQX.")
    check("set_language" in low, "Gestiona SET_LANGUAGE", "No gestiona SET_LANGUAGE (idioma).", "AVISO")
    check(("get_stats" not in low) or ("stats_response" in low), "Cada petición GET_STATS tiene su respuesta",
          "Pide GET_STATS pero no gestiona STATS_RESPONSE.")
    check(("get_orders" not in low) or ("orders_response" in low), "Cada petición GET_ORDERS tiene su respuesta",
          "Pide GET_ORDERS pero no gestiona ORDERS_RESPONSE.")
    check(not re.search(r"params\s*:\s*\{[^}]*(projectName|databankName|strategyName)", src),
          "No envía projectName/databankName/strategyName", "No envíes projectName/databankName/strategyName en las peticiones: SQX los añade solo.", "AVISO")

    # --- Robustez
    check(("timeout" in low or "settimeout" in low), "Tiene tiempo máximo de espera",
          "No hay tiempo máximo de espera para las respuestas de SQX: si SQX no responde, el plugin se queda esperando.", "AVISO")
    check("-99999999" in src or "99999999" in src, "Trata el valor no definido de SQX (-99999999)",
          "No trata -99999999 ni null como 'sin dato': puede mostrar números absurdos.", "AVISO")
    uses_canvas = "<canvas" in low or "createelement('canvas'" in low.replace('"', "'")
    if uses_canvas:
        check("resizeobserver" in low, "Usa ResizeObserver con canvas", "Hay canvas pero no ResizeObserver: no se redibujará al cambiar el tamaño del panel.")
        check("devicepixelratio" in low, "Escala el canvas por devicePixelRatio", "El canvas no usa devicePixelRatio: se verá borroso.", "AVISO")
        check("set_theme" in low and re.search(r"set_theme[\s\S]{0,400}(draw|render|repaint|redraw|pintar)", low) is not None,
              "Repinta el canvas al cambiar de tema", "Con canvas, SET_THEME debe repintar (los canvas no heredan el CSS).", "AVISO")
    check(re.search(r"overflow\s*:\s*hidden", low) is not None, "El body evita scroll externo", "Falta overflow:hidden en el body (el plugin está en un iframe).", "AVISO")
    check(("try" in low and "localstorage" in low) or "localstorage" not in low, "localStorage protegido con try/catch",
          "Usa localStorage sin try/catch: puede lanzar error si el navegador lo bloquea.", "AVISO")

    # --- Sin red
    externos = sorted(set(re.findall(r"""(?:src|href)\s*=\s*["'](https?://[^"']+)""", src, flags=re.I)))
    externos += sorted(set(re.findall(r"""@import\s+url\(\s*["']?(https?://[^"')]+)""", src, flags=re.I)))
    check(not externos, "No carga recursos de internet", "Carga recursos remotos (SQX funciona sin conexión): " + ", ".join(externos[:5]))
    check(not re.search(r"\b(fetch|XMLHttpRequest|WebSocket|sendBeacon)\b", src), "No hace llamadas de red",
          "Hace llamadas de red (fetch/XHR/WebSocket): un plugin de SQX debe funcionar sin conexión y no enviar datos fuera.")

    # --- Seguridad
    check(not re.search(r"\beval\s*\(|new\s+Function\s*\(", src), "Sin eval ni new Function", "Usa eval o new Function: no es seguro.")
    inner = re.findall(r"\.innerHTML\s*=", src)
    check(len(inner) <= 1, "innerHTML mínimo", "Hay varios usos de innerHTML: asegúrate de que nunca reciban texto que venga de SQX (nombres, comentarios).", "AVISO")
    check(not re.search(r"(api[_-]?key|password|passwd|secret|token)\s*[:=]\s*['\"][^'\"]{6,}", src, flags=re.I),
          "Sin claves ni contraseñas en el código", "Parece haber una clave o contraseña escrita en el código.")
    check(not re.search(r"[A-Za-z]:\\Users\\|/Users/[a-z]+/|/home/[a-z]+/", src), "Sin rutas personales", "Hay rutas personales en el código; quítalas.")

    # --- Aviso legal
    m = re.search(r'class\s*=\s*["\'][^"\']*disclaimer', low) or re.search(r"\.disclaimer", low)
    check(m is not None, "Tiene aviso legal (.disclaimer)", "Falta el aviso legal (.disclaimer). Es obligatorio.")
    check(("financial" in low and "advice" in low) or ("asesoramiento" in low), "El aviso legal menciona que no es asesoramiento",
          "El aviso legal debe decir que no es asesoramiento financiero.")
    check(("past performance" in low) or ("rendimiento pasado" in low), "El aviso legal menciona el rendimiento pasado",
          "El aviso legal debe incluir que el rendimiento pasado no garantiza resultados futuros.", "AVISO")
    # el aviso debe ir al final del #app
    app_end = low.rfind("</div>\n<script")
    disc_pos = low.rfind("disclaimer")
    check(disc_pos != -1, "El aviso aparece en el documento", "No se encuentra el aviso legal.", "AVISO")

    # --- Textos que no deben aparecer
    prohibidas = re.findall(r"(rentabilidad asegurada|ganancias garantizadas|estrategia ganadora|guaranteed profit|sure win|dinero fácil)", low)
    check(not prohibidas, "Sin promesas de rentabilidad", "Hay textos que prometen resultados: " + ", ".join(sorted(set(prohibidas))))

    # --- Calidad de interfaz
    check("data-tip" in low or "title=" in low, "Tiene tooltips o ayudas", "No hay tooltips: las métricas no obvias deben explicarse.", "AVISO")
    check("[data-theme" in low or "data-theme" in low, "Tema con atributo data-theme", "No usa data-theme para el tema claro/oscuro.", "AVISO")
    check("--" in src and re.search(r":root\s*\{", src) is not None, "Usa variables CSS (tokens)", "No define variables CSS en :root; usa tokens para los colores.", "AVISO")
    check(len(re.findall(r"#[0-9a-fA-F]{6}\b", re.sub(r":root\s*\{[^}]*\}|\[data-theme[^\]]*\]\s*\{[^}]*\}", "", src))) < 12,
          "Colores centralizados", "Hay muchos colores escritos fuera de las variables CSS.", "AVISO")
    check(re.search(r"\.(menu|empty|vacio|waiting|esperando)", low) is not None or "empty" in low or "waiting" in low,
          "Tiene estado de espera/vacío", "No se ve un estado vacío o de espera.", "AVISO")
    check(re.search(r"aria-|role=|aria_", low) is not None, "Detalles de accesibilidad", "No hay atributos aria/role: revisa accesibilidad.", "AVISO")

    # --- Informe
    print(f"\nInforme de {p}\n" + "=" * 60)
    print(f"{len(bien)} comprobaciones correctas, {len(avisos)} aviso(s), {len(errores)} error(es)\n")
    for e in errores:
        print("ERROR  " + e)
    for a in avisos:
        print("AVISO  " + a)
    if not errores and not avisos:
        print("Todo correcto. Recuerda probarlo en SQX real y contrastar los números.")
    elif not errores:
        print("\nSin errores. Revisa los avisos y prueba en SQX real.")
    else:
        print("\nCorrige los ERROR antes de entregar.")
    return 1 if errores else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python validar_plugin.py ruta/al/index.html")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
