/* Patrones de robustez reutilizables (JavaScript puro). Nacieron de fallos reales en herramientas de trading:
   órdenes duplicadas, guardados que se perdían, pantallas que parpadeaban. Pensados para pegar en la sección LÓGICA / COMUNICACIÓN. */

const Robust = (() => {

  /* 1. Cerrojo: una sola ejecución a la vez por clave. La segunda llamada recibe la misma promesa en vez de repetir el trabajo.
        Se activa de forma SÍNCRONA, antes de cualquier await: ahí estaba el hueco de los envíos duplicados. */
  const locks = new Map();
  const withLock = (key, fn) => {
    if (locks.has(key)) return locks.get(key);
    const p = Promise.resolve().then(fn).finally(() => locks.delete(key));
    locks.set(key, p);
    return p;
  };

  /* 2. Envío idempotente: antes de crear algo, mira si ya existe (estado real, no un dato viejo) y, si existe, reutilízalo.
        `findExisting` lee el estado actual; `create` solo se llama si no hay nada. "En curso" = cualquier estado NO terminal. */
  const TERMINAL = new Set(['done', 'error', 'cancelled', 'canceled', 'failed']);
  const isInProgress = (status) => !TERMINAL.has(String(status || '').toLowerCase());
  const submitOnce = (key, findExisting, create) => withLock(key, async () => {
    const existing = await findExisting();            // si esta lectura falla, el error sube: NO se envía a ciegas
    if (existing) return { reused: true, item: existing };
    return { reused: false, item: await create() };
  });

  /* 3. Cola de reintentos persistente: si guardar falla (red, servidor), el cambio queda en cola local y se reintenta.
        Mientras haya pendientes, la interfaz muestra un aviso visible. */
  const makeRetryQueue = (storageKey, send) => {
    let q = [];
    try { q = JSON.parse(localStorage.getItem(storageKey) || '[]'); } catch (e) { q = []; }
    const save = () => { try { localStorage.setItem(storageKey, JSON.stringify(q)); } catch (e) { /* sin almacenamiento: queda en memoria */ } };
    return {
      add(item) { q.push(item); save(); return this.flush(); },
      async flush() {
        const rest = [];
        for (const it of q) { try { await send(it); } catch (e) { rest.push(it); } }
        q = rest; save(); return q.length;               // devuelve cuántos siguen pendientes
      },
      pending() { return q.length; }
    };
  };

  /* 4. Redibujar solo si cambió algo: una "firma" del contenido evita parpadeos en tarjetas, rotaciones y tablas.
        Úsalo así: if (changed('tabla', datos)) pintar(); */
  const signatures = new Map();
  const changed = (key, value) => {
    const sig = JSON.stringify(value);
    if (signatures.get(key) === sig) return false;
    signatures.set(key, sig); return true;
  };

  /* 5. Tooltip que no se corta: calcula una posición que cabe en la ventana (el tooltip CSS simple se sale por los bordes). */
  const fitTooltip = (tipEl, anchorEl, margin = 8) => {
    const a = anchorEl.getBoundingClientRect(), t = tipEl.getBoundingClientRect();
    let left = Math.min(Math.max(margin, a.left), window.innerWidth - t.width - margin);
    let top = a.bottom + 6; if (top + t.height > window.innerHeight - margin) top = Math.max(margin, a.top - t.height - 6);
    tipEl.style.left = left + 'px'; tipEl.style.top = top + 'px';
  };

  return { withLock, submitOnce, isInProgress, makeRetryQueue, changed, fitTooltip };
})();

if (typeof module !== 'undefined') module.exports = Robust;
