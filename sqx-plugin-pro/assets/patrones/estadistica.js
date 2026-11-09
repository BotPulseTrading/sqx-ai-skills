/* Funciones estadísticas reutilizables para plugins de SQX (JavaScript puro, sin dependencias).
   Se copian dentro de la sección LÓGICA del plugin. Todas son funciones puras: se pueden probar sin SQX.
   Escritas para esta skill; los umbrales de fiabilidad son un punto de partida, ajústalos a tus datos. */

const Stats = (() => {
  const isNum = (v) => typeof v === 'number' && isFinite(v) && v > -99999999;
  const clean = (arr) => arr.filter(isNum);

  const mean = (a) => (a.length ? a.reduce((s, x) => s + x, 0) / a.length : NaN);
  const stdev = (a) => {
    if (a.length < 2) return NaN;
    const m = mean(a);
    return Math.sqrt(a.reduce((s, x) => s + (x - m) * (x - m), 0) / (a.length - 1));
  };
  const percentile = (a, p) => {                       // p entre 0 y 100, interpolación lineal
    if (!a.length) return NaN;
    const s = a.slice().sort((x, y) => x - y), i = (p / 100) * (s.length - 1), lo = Math.floor(i), hi = Math.ceil(i);
    return s[lo] + (s[hi] - s[lo]) * (i - lo);
  };

  /* Correlación de Pearson entre dos series alineadas (mismo largo). Devuelve NaN si no hay datos suficientes. */
  const pearson = (x, y) => {
    const n = Math.min(x.length, y.length);
    if (n < 3) return NaN;
    const mx = mean(x.slice(0, n)), my = mean(y.slice(0, n));
    let sxy = 0, sxx = 0, syy = 0;
    for (let i = 0; i < n; i++) { const dx = x[i] - mx, dy = y[i] - my; sxy += dx * dy; sxx += dx * dx; syy += dy * dy; }
    return sxx > 0 && syy > 0 ? sxy / Math.sqrt(sxx * syy) : NaN;
  };

  /* Intervalo de confianza del 95 % de una correlación (transformación de Fisher).
     Con pocas observaciones el intervalo es ancho: eso es lo que hay que enseñar al usuario. */
  const fisherCI = (r, n) => {
    if (!isFinite(r) || n < 4) return { lo: NaN, hi: NaN };
    const z = Math.atanh(Math.max(-0.9999, Math.min(0.9999, r))), se = 1 / Math.sqrt(n - 3), k = 1.96;
    return { lo: Math.tanh(z - k * se), hi: Math.tanh(z + k * se) };
  };

  /* Grado de fiabilidad según el número de observaciones (semanas, operaciones...). Ajusta los cortes a tu caso. */
  const reliability = (n, cuts = { high: 150, mid: 52 }) => (n >= cuts.high ? 'alta' : n >= cuts.mid ? 'media' : 'baja');

  /* Agrupa una lista de {time, pl} por clave (día, semana, mes) y suma. Útil para alinear series antes de correlacionar. */
  const bucketSum = (rows, keyFn) => {
    const m = new Map();
    for (const r of rows) { if (!isNum(r.pl)) continue; const k = keyFn(new Date(r.time)); m.set(k, (m.get(k) || 0) + r.pl); }
    return m;
  };
  const weekKey = (d) => {                              // clave ISO simple año-semana
    const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    const day = t.getUTCDay() || 7; t.setUTCDate(t.getUTCDate() + 4 - day);
    const y0 = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    return t.getUTCFullYear() + '-W' + String(Math.ceil(((t - y0) / 86400000 + 1) / 7)).padStart(2, '0');
  };

  /* Monte Carlo por remuestreo de días: mezcla los resultados diarios con reemplazo y mide la caída máxima de cada corrida.
     Es una simulación sobre datos pasados: sirve para ver un rango de resultados posibles, nunca para predecir. */
  const monteCarloDrawdown = (dailyPL, { runs = 150, days = 400, start = 10000, rng = Math.random } = {}) => {
    const d = clean(dailyPL);
    if (d.length < 20) return { ok: false, reason: 'pocos-dias' };
    const dds = [], finals = [];
    for (let r = 0; r < runs; r++) {
      let eq = start, peak = start, maxDD = 0;
      for (let i = 0; i < days; i++) {
        eq += d[Math.floor(rng() * d.length)];
        if (eq > peak) peak = eq;
        maxDD = Math.max(maxDD, (peak - eq) / peak);
      }
      dds.push(maxDD * 100); finals.push(((eq - start) / start) * 100);
    }
    return { ok: true, runs, days, ddP50: percentile(dds, 50), ddP95: percentile(dds, 95), retP5: percentile(finals, 5), retP50: percentile(finals, 50) };
  };

  return { isNum, clean, mean, stdev, percentile, pearson, fisherCI, reliability, bucketSum, weekKey, monteCarloDrawdown };
})();

if (typeof module !== 'undefined') module.exports = Stats;   // permite probarlo con Node
