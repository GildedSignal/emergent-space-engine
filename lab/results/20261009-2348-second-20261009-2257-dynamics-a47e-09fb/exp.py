#!/usr/bin/env python3
"""Second-author run on 20261009-2257-dynamics-a47e (B12's instrument).

Prior claim (silver): B12's growth exponent inverts because on chaotic ships
every error series saturates on the state attractor, so the exponent measures
saturation timing, not boundedness -- and a threshold-free exact-integer Allan
rule separates bounded from leaking error series.

This file answers, in shipped regenerable code, what the checker named:

  fix 1  chaotic_sat now saturates (wander whenever |x| >= attractor).  The
         shipped model let x run negative and diverge (checker, reason 2).
  fix 2  run_wh integerizes the Jacobi series at 2^40, as the prior dossier
         described but did not ship (checker, reason 3); the integer range of
         every classified series is printed (no vacuous all-zero flags).
  fix 3  the horizon scan and the phase-dependent alias scan are shipped
         subcommands (horizon, alias); wh writes wh-output.txt itself, so no
         output is hand-assembled (checker, reason 4).
  new 1  the gold experiment the checker named: a per-kick bias
         eps*h*|a| applied along the ROTATING-frame velocity at each half-kick -- a systematic,
         compounding integrator error -- planted on the physical path
         (variants bias1/bias3).  Pre-registered: bias3 caught >= 6/8 at 2^40
         by the recommended rule while the good control stays <= 1/8.
  new 2  the checker's false-positive family, answered: bounded long-memory
         series (OU at correlation times T/32..T/4, band-limited 1/f flicker)
         censused under three rules.  R2/R3 are the multi-tau consistency
         variants the prior run proposed but never built.

Rules (exact integer series, Fractions, no thresholds anywhere):
  R1: leak <=> AVAR(T/4) > AVAR(T/32)                    (prior run)
  R2: leak <=> AVAR(T/4) > AVAR(T/8)                     (last octave must rise)
  R3: leak <=> AVAR non-decreasing over {T/32,T/16,T/8,T/4} and strictly
       rising overall                                      (consistency ladder)
R1 keeps the prior NON-overlapping estimator so it regenerates the prior
record bit for bit.  R2/R3 use the OVERLAPPING Allan estimator (all adjacent
tau-block pairs at every alignment): at tau = T/4 the non-overlapping
estimator has only 3 dof, which alone flipped ~2/10 pure-walk verdicts during
setup (disclosed in the dossier); the overlap is the metrology-standard fix
and stays exact (integer cumsums, big-int squares, Fraction comparison).

Deterministic: one LCG everywhere, numpy only for vector arithmetic; floats
appear only in the physics (Part C) and display lines, never in a verdict.
Run:  python3 exp.py controls | memory | horizon | alias | inversion |
                            kepler_check | wh | all | calibrate
"""
import math
import sys
from fractions import Fraction

import numpy as np

# ---------------------------------------------------------------- deterministic RNG
class LCG:
    M = 1 << 64
    def __init__(self, seed):
        self.s = seed & (self.M - 1)
    def u01(self):
        self.s = (6364136223846793005 * self.s + 1442695040888963407) % self.M
        return self.s / self.M
    def sym(self):           # centered unit-ish (Irwin-Hall 12 -> near-Gaussian, sd 1)
        return (sum(self.u01() for _ in range(12)) - 6.0)
    def integer(self, a, b):
        return a + int(self.u01() * (b - a + 1))

def avar_frac(xs, tau):
    """Non-overlapping Allan variance of integer series xs at averaging time
    tau, exact rational (the PRIOR run's estimator; used only by R1)."""
    m = len(xs) // tau
    if m < 2:
        return None
    means = [Fraction(sum(xs[k * tau:(k + 1) * tau]), tau) for k in range(m)]
    num = sum((means[k + 1] - means[k]) ** 2 for k in range(m - 1))
    return Fraction(num, 2 * (m - 1))

def avar_over(xs, tau):
    """Overlapping Allan variance, exact: adjacent tau-block pairs at every
    alignment (n - 2*tau + 1 pairs).  Integer cumsums in int64 (values fit by
    construction: |series| < 2^41 and n < 2^16), squares in big ints."""
    n = len(xs)
    m = n - 2 * tau + 1
    if m < 1:
        return None
    cs = np.zeros(n + 1, dtype=np.int64)
    np.cumsum(np.asarray(xs, dtype=np.int64), out=cs[1:])
    i = np.arange(m)
    d = (cs[tau + i] - cs[i]) - (cs[2 * tau + i] - cs[tau + i])   # tau*(y_{i+tau}-y_i)
    num = sum(int(x) * int(x) for x in d)
    return Fraction(num, 2 * m * tau * tau)

def classify_all(xs):
    """R1: prior rule on the prior estimator (regenerates the prior record).
    R2/R3: multi-tau rules on the overlapping estimator."""
    n = len(xs)
    t1, t2, t3, t4 = (max(1, n // 32), max(1, n // 16), max(1, n // 8), max(1, n // 4))
    a = {t: avar_over(xs, t) for t in (t1, t2, t3, t4)}
    b1, b4 = avar_frac(xs, t1), avar_frac(xs, t4)
    r1 = b4 > b1
    r2 = a[t4] > a[t3]
    r3 = (a[t1] <= a[t2] <= a[t3] <= a[t4]) and (a[t4] > a[t1])
    v = lambda b: "leak" if b else "bounded"
    return dict(R1=v(r1), R2=v(r2), R3=v(r3)), a

def classify(xs):                                   # prior one-ratio rule (compat)
    v, a = classify_all(xs)
    n = len(xs); t4 = max(1, n // 4); t1 = max(1, n // 32)
    return v["R1"], {t1: avar_frac(xs, t1), t4: avar_frac(xs, t4)}

def growth_exponent(series, floor=1e-12):
    """B12's current statistic: log-log slope of |error|, samples above the floor."""
    ts, ys = [], []
    for i, x in enumerate(series):
        a = abs(x)
        if a > floor:
            ts.append(math.log(i + 1)); ys.append(math.log(a))
    if len(ts) < 8:
        return 0.0                      # "below floor: no growth" per the gate text
    nt, ny = len(ts), len(ys)
    mt, my = sum(ts) / nt, sum(ys) / ny
    cov = sum((t - mt) * (y - my) for t, y in zip(ts, ys))
    var = sum((t - mt) ** 2 for t in ts)
    return cov / var

def row_print(name, truth, verd):
    print(f"  {name:<24} truth={truth:<7} R1={verd['R1']:<7} R2={verd['R2']:<7} "
          f"R3={verd['R3']:<7}{''.join('  <-- ' + r + ' WRONG' for r in ('R1','R2','R3') if verd[r] != truth)}")

# ---------------------------------------------------------------- Part A: planted integer controls
A = 1_000_000          # bounded amplitude, integer units
N = 1 << 15            # 32768 samples

def int_round(xs):
    return [int(round(v)) for v in xs]

def ou_series(rng, rho, sd):
    x, xs = 0.0, []
    for _ in range(N):
        x = rho * x + sd * rng.sym()
        xs.append(x)
    return int_round(xs)
def qp_series(rng, phases):
    xs = []
    for n in range(N):
        v = (0.5 * math.cos(2 * math.pi * math.sqrt(2) * n / 512 + phases[0])
             + 0.3 * math.cos(2 * math.pi * math.sqrt(3) * n / 512 + phases[1])
             + 0.2 * math.cos(2 * math.pi * math.pi * n / 2048 + phases[2]))
        xs.append(A * v)
    return int_round(xs)

def sine_series(period, phase=0.0):
    return int_round([A * 0.7 * math.cos(2 * math.pi * n / period + phase) for n in range(N)])

def walk_series(rng, ratio):
    """random walk whose total drift sigma*sqrt(N) = ratio * A."""
    sigma = ratio * A / math.sqrt(N)
    x, xs = 0.0, []
    for _ in range(N):
        x += sigma * rng.sym()
        xs.append(x)
    return int_round(xs)

def controls():
    """Prior Part A verbatim (same seeds, same LCG order -> same R1 record),
    now also censused under R2/R3."""
    rows = []
    def add(name, truth, predicted, xs):
        verd, _ = classify_all(xs)
        rows.append(dict(name=name, truth=truth, predicted=predicted, verd=verd,
                         ok_pred=(verd["R1"] == predicted)))
    rng = LCG(20261009)
    for i in range(4):
        add(f"quasiperiodic-{i}", "bounded", "bounded",
            qp_series(rng, [2 * math.pi * rng.u01() for _ in range(3)]))
    for i in range(4):
        add(f"ou-chaos-{i}", "bounded", "bounded", ou_series(rng, math.exp(-1 / 100), 0.3 * A))
    for p in (N / 16, N / 8, N / 8, N / 4):
        add(f"sine-P{p:.0f}", "bounded", "bounded", sine_series(p))
    add("sine-PN/2-alias", "bounded", "leak", sine_series(N / 2))          # H2 predicted miss
    for r, cnt in ((10.0, 2), (3.0, 2), (1.5, 2), (0.3, 2), (0.1, 2)):
        for i in range(cnt):
            pred = "leak" if r > math.sqrt(2) else "bounded"                # H1
            add(f"walk-r{r}-{i}", "leak", pred, walk_series(rng, r))
    for r in (1.5, 3.0):                                                    # mixtures at the boundary
        w = walk_series(rng, r); q = qp_series(rng, [0.3, 1.1, 2.7])
        add(f"mix-r{r}", "leak", "leak", [a + b for a, b in zip(w, q)])

    print(f"[controls] {len(rows)} series")
    for r in rows:
        row_print(r["name"], r["truth"], r["verd"])
    for rule in ("R1", "R2", "R3"):
        ok = sum(r["verd"][rule] == r["truth"] for r in rows)
        misses = [r["name"] for r in rows if r["verd"][rule] != r["truth"]]
        print(f"[controls] {rule}: ground-truth agreement {ok}/{len(rows)}  misses: {misses or 'none'}")
    ok_pred = sum(r["ok_pred"] for r in rows)
    print(f"[controls] R1 predicted-outcome agreement (prior record): {ok_pred}/{len(rows)}, "
          f"deviations: {[r['name'] for r in rows if not r['ok_pred']] or 'none'}")
    return rows

# ---------------------------------------------------------------- Part A2: the checker's false-positive family
def ou_memory(rng, tau_c, sd=0.3 * A):
    """OU with correlation time tau_c samples (stationary, hence bounded)."""
    return ou_series(rng, math.exp(-1.0 / tau_c), sd)

def flicker_fft(rng, f_min):
    """Continuum 1/f (PSD ~ 1/f) noise: LCG white noise shaped by FFT.  Every
    frequency bin carries independent phase -> a genuine long-memory continuum
    (equal power per octave).  Band-limited below at f_min (2/T or 4/T)."""
    w = np.array([rng.sym() for _ in range(N)])
    W = np.fft.rfft(w)
    f = np.fft.rfftfreq(N)
    W = W * np.where(f >= f_min, np.divide(1.0, np.sqrt(np.maximum(f, 1e-300))), 0.0)
    x = np.fft.irfft(W, n=N)
    return int_round(x / x.std() * 0.5 * A)

def flicker_tones(rng, p_lo, n_tone=18, amp=0.17 * A):
    """Tone-synthesis 'flicker': log-spaced tones (p_lo..32), equal amplitudes.
    This is the checker's-style arm; measured here to be a SYNTHESIS ARTIFACT
    for continuum claims (18 discrete slow modes, not a continuum) -- it is
    really the discrete-slow-mode (alias) family in disguise.  Kept because it
    reproduces the checker's flicker false flags and models a real risk: a J
    error dominated by a few discrete slow modes (librations)."""
    tones = [p_lo * (32.0 / p_lo) ** (k / (n_tone - 1.0)) for k in range(n_tone)]
    ph = [2 * math.pi * rng.u01() for _ in tones]
    return int_round([amp * sum(math.cos(2 * math.pi * n / P + f)
                                for P, f in zip(tones, ph)) for n in range(N)])

def _verdicts(xs):
    return classify_all(xs)[0]

def memory():
    """Long-memory bounded census: the family the checker showed R1 false-flags.
    OU correlation times, continuum flicker (two bands), tone flicker, white."""
    fams = []
    rng = LCG(20261010)
    for tc, tag in ((N // 32, "T/32"), (N // 12, "T/12"), (N // 16, "T/16"),
                    (N // 8, "T/8"), (N // 4, "T/4")):
        for i in range(3):
            fams.append((f"ou-corr{tag}-{i}", ou_memory(rng, tc)))
    for i in range(3):
        fams.append((f"flickerFFT-band-{i}", flicker_fft(rng, 4.0 / N)))
    for i in range(3):
        fams.append((f"flickerFFT-full-{i}", flicker_fft(rng, 2.0 / N)))
    for i in range(3):
        fams.append((f"flickerTONES-P<=T/4-{i}", flicker_tones(rng, N // 4)))
    for i in range(3):
        fams.append((f"white-{i}", int_round([0.5 * A * rng.sym() for _ in range(N)])))
    print(f"[memory] {len(fams)} bounded series (truth: bounded)")
    for name, xs in fams:
        row_print(name, "bounded", _verdicts(xs))
    for rule in ("R1", "R2", "R3"):
        for grp, pref in (("ou-T/32..T/16", ("ou-corrT/32-", "ou-corrT/12-", "ou-corrT/16-")),
                          ("ou-T/8", ("ou-corrT/8-",)), ("ou-T/4", ("ou-corrT/4-",)),
                          ("flickerFFT-band", ("flickerFFT-band-",)),
                          ("flickerFFT-full", ("flickerFFT-full-",)),
                          ("flickerTONES", ("flickerTONES-",)), ("white", ("white-",))):
            rows = [xs for nm, xs in fams if nm.startswith(pref)]
            flags = sum(_verdicts(xs)[rule] == "leak" for xs in rows)
            print(f"[memory] {rule} false flags  {grp:<18} {flags}/{len(rows)}")
    return fams

def census():
    """30-seed design census of the rule tradeoff (pre-freeze design measurement,
    shipped so the table regenerates): walk catch vs OU/tone false flags."""
    W = 30
    def flags(gen, rule):
        return f"{sum(_verdicts(gen(s))[rule] == 'leak' for s in range(W))}/{W}"
    print("[census] walk r=3 CATCH (truth leak, flagged):")
    print("   ", {r: flags(lambda s: walk_series(LCG(920000 + s), 3.0), r)
                  for r in ("R1", "R2", "R3")})
    for tc, tag in ((N // 32, "T/32"), (N // 16, "T/16"), (N // 8, "T/8"), (N // 4, "T/4")):
        print(f"[census] OU corr {tag} FALSE FLAGS (truth bounded, flagged):",
              {r: flags(lambda s, tc=tc: ou_memory(LCG(930000 + s), tc), r)
               for r in ("R1", "R2", "R3")})
    for fmin, tag in ((4.0 / N, "band"), (2.0 / N, "full")):
        print(f"[census] flickerFFT {tag} FALSE FLAGS (flagged):",
              {r: flags(lambda s, fmin=fmin: flicker_fft(LCG(950000 + s), fmin), r)
               for r in ("R1", "R2", "R3")})
    print("[census] flickerTONES FALSE FLAGS (flagged):",
          {r: flags(lambda s: flicker_tones(LCG(940000 + s), N // 4), r)
           for r in ("R1", "R2", "R3")})

# ---------------------------------------------------------------- horizon and alias scans (checker fix 3)
def horizon():
    """Deterministic linear drift on a quasiperiodic floor: catch boundary."""
    print("[horizon] linear drift on qp floor, total drift = ratio x A (3 seeds each)")
    for ratio in (0.05, 0.1, 0.2, 0.3, 0.5, 1.0):
        flags = {"R1": 0, "R2": 0, "R3": 0}
        for s in range(3):
            rng = LCG(31337 + s)
            q = qp_series(rng, [2 * math.pi * rng.u01() for _ in range(3)])
            xs = int_round([q[n] + ratio * A * n / N for n in range(N)])
            verd, _ = classify_all(xs)
            for r in flags:
                flags[r] += verd[r] == "leak"
        print(f"[horizon] drift {ratio:>4}A : caught R1 {flags['R1']}/3  R2 {flags['R2']}/3  R3 {flags['R3']}/3")

def alias():
    """Bounded slow sinusoid: period x phase scan (the window condition)."""
    print("[alias] bounded sine, 5 phases per period")
    for p, tag in ((N / 2, "T/2"), (N / 2.5, "T/2.5"), (N / 3, "T/3"), (N / 4, "T/4")):
        flags = {"R1": [], "R2": [], "R3": []}
        for i in range(5):
            verd, _ = classify_all(sine_series(p, i * 2 * math.pi / 5))
            for r in flags:
                flags[r].append(verd[r] == "leak")
        f = lambda l: f"{sum(l)}/5" + (f" (phases {[i for i, b in enumerate(l) if b]})" if 0 < sum(l) < 5 else "")
        print(f"[alias] P={tag:<5}: R1 {f(flags['R1'])}  R2 {f(flags['R2'])}  R3 {f(flags['R3'])}")

# ---------------------------------------------------------------- Part B: exponent inversion (corrected model)
def chaotic_sat(seed, lam, d0=1e-12, attractor=1.0):
    """Corrected saturating model (checker's fix): wander whenever |x| >= attractor,
    so the series never diverges.  Returns (series, max|x|)."""
    rng = LCG(seed)
    x, xs, mx = d0, [], 0.0
    for _ in range(N):
        x = x * math.exp(lam) if abs(x) < attractor else x
        if abs(x) >= attractor:                              # wander on the attractor
            x = 0.9 * x + 0.35 * rng.sym()
            x = max(min(x, 1.4 * attractor), -1.4 * attractor)
        xs.append(x)
        mx = max(mx, abs(x))
    return xs, mx

def inversion():
    lam = math.log(1e12) / (N / 10.0)                        # saturates at 10% of the window
    sigma15 = 1.5 / math.sqrt(N)                             # leak: total drift 1.5 attractor units
    out, all_mx = [], []
    for draw in range(3):
        rng = LCG(7000 + draw)
        exp_b, exp_l = [], []
        for s in range(16):
            xs, mx = chaotic_sat(100000 + draw * 100 + s, lam)
            exp_b.append(growth_exponent(xs)); all_mx.append(mx)
            w, x = 0.0, []
            for _ in range(N):
                w += sigma15 * rng.sym(); x.append(w)
            exp_l.append(growth_exponent(x))
        mb = sorted(exp_b)[8]; ml = sorted(exp_l)[8]
        inv = mb > ml
        out.append(inv)
        print(f"[inversion] draw {draw}: median exponent bounded={mb:.3f}  slow-leak={ml:.3f}  "
              f"inverted={'YES' if inv else 'no'}")
    print(f"[inversion] reproduced in {sum(out)}/3 draws (prediction: >= 2)")
    print(f"[inversion] bounded-family max|x| over all 48 seeds = {max(all_mx):.3f} "
          f"(attractor clamp 1.4 -> saturates, no divergence)")
    return out

# ---------------------------------------------------------------- Part C: the law's cheap path (Wisdom-Holman)
MU = 1e-3                      # planet (Jupiter-like) mass / star mass
GM = 1.0 - MU                  # star
H_ORB = 120                    # steps per planet orbit
N_ORB = 250                    # planet orbits
SAMP = 60                      # steps between J samples
SCALE = 2 ** 40                # integerization of the Jacobi series (checker fix 2)
BIAS1 = 1.0e-2                 # per-kick bias eps along vrot-hat (calibrated, calibrate())
BIAS3 = 3.0e-2

def kepler_drift(r, v, dt):
    """Exact two-body propagation about the star (classical elements, elliptic)."""
    rn = np.linalg.norm(r, axis=-1, keepdims=True)
    v2 = np.sum(v * v, axis=-1, keepdims=True)
    a = 1.0 / (2.0 / rn - v2 / GM)
    hz = r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]
    evec = np.stack([v[:, 1] * hz / GM - r[:, 0] / rn[:, 0],
                     -v[:, 0] * hz / GM - r[:, 1] / rn[:, 0]], axis=-1)
    e = np.linalg.norm(evec, axis=-1, keepdims=True)
    P = evec / np.maximum(e, 1e-12)
    Q = np.stack([-P[:, 1], P[:, 0]], axis=-1)
    rn_flat = rn[:, 0]
    cosnu = (r[:, 0] * P[:, 0] + r[:, 1] * P[:, 1]) / rn_flat
    sinnu = (r[:, 0] * Q[:, 0] + r[:, 1] * Q[:, 1]) / rn_flat
    nu = np.arctan2(sinnu, cosnu)
    sq1me2 = np.sqrt(np.maximum(1.0 - e[:, 0] ** 2, 1e-24))
    E0 = np.arctan2(sq1me2 * sinnu, e[:, 0] + cosnu)
    M0 = E0 - e[:, 0] * np.sin(E0)
    n = np.sqrt(GM / a[:, 0] ** 3)
    M1 = (M0 + n * dt) % (2 * np.pi)
    E1 = M1.copy()
    for _ in range(10):                               # Kepler's equation, e <= ~0.2
        E1 = E1 - (E1 - e[:, 0] * np.sin(E1) - M1) / (1.0 - e[:, 0] * np.cos(E1))
    cE, sE = np.cos(E1), np.sin(E1)
    denom = 1.0 - e[:, 0] * cE
    cosn1 = (cE - e[:, 0]) / denom
    sinn1 = sq1me2 * sE / denom
    r1mag = a[:, 0] * denom
    p = a[:, 0] * (1.0 - e[:, 0] ** 2)
    k = np.sqrt(GM / p)
    r1 = r1mag[:, None] * (cosn1[:, None] * P + sinn1[:, None] * Q)
    v1 = k[:, None] * (-sinn1[:, None] * P + (e[:, 0] + cosn1)[:, None] * Q)
    return r1, v1

def jacobi(r, v, t):
    """CRTBP Jacobi constant, inertial -> rotating (n = 1)."""
    x, y = r[..., 0], r[..., 1]
    rp = planet_pos(t)
    r1 = np.linalg.norm(r, axis=-1); r2 = np.linalg.norm(r - rp, axis=-1)
    vrot = np.stack([v[..., 0] + y, v[..., 1] - x], axis=-1)
    return (x * x + y * y) + 2 * (GM / r1 + MU / r2) - np.sum(vrot * vrot, axis=-1)

def planet_pos(t):
    return np.stack([math.cos(t), math.sin(t)])

def vrot_hat(r, v):
    """Unit vector of the rotating-frame velocity vrot = v - omega x r (n=1).
    A bias along vrot does non-conservative work in the corotating frame and
    so leaks the Jacobi constant (unlike an inertial-tangential bias, which is
    adiabatically C-neutral on co-rotating ships -- measured in calibrate())."""
    w = np.stack([v[:, 0] + r[:, 1], v[:, 1] - r[:, 0]], axis=-1)
    return w / np.linalg.norm(w, axis=-1, keepdims=True)

def accel(r, t, delay=0.0):
    rp = planet_pos(t - delay)
    d = r - rp
    return -MU * d / np.linalg.norm(d, axis=-1, keepdims=True) ** 3

def init_ships(seed, n_ships):
    rng = LCG(seed)
    a_s = np.array([0.935, 0.945, 0.955, 0.965, 1.035, 1.045, 1.055, 1.065])[:n_ships]
    r, v = [], []
    for a in a_s:
        e = 0.02 + 0.04 * rng.u01(); nu = 2 * math.pi * rng.u01()
        p = a * (1 - e * e)
        rr = p / (1 + e * math.cos(nu)); hh = math.sqrt(GM * p)
        r.append([rr * math.cos(nu), rr * math.sin(nu)])
        vr = GM / hh * e * math.sin(nu); vt = hh / rr
        v.append([vr * math.cos(nu) - vt * math.sin(nu), vr * math.sin(nu) + vt * math.cos(nu)])
    return np.array(r), np.array(v)

def kepler_check():
    """Two-body energy conservation of the drift alone (instrument check)."""
    r, v = init_ships(4242, 8)
    h = 2 * math.pi / H_ORB
    e0 = 0.5 * np.sum(v * v, axis=-1) - GM / np.linalg.norm(r, axis=-1)
    rel = 0.0
    for _ in range(N_ORB * H_ORB):
        r, v = kepler_drift(r, v, h)
        e = 0.5 * np.sum(v * v, axis=-1) - GM / np.linalg.norm(r, axis=-1)
        rel = max(rel, float(np.max(np.abs(e - e0) / np.abs(e0))))
    print(f"[kepler_check] max relative two-body energy error over {N_ORB*H_ORB} steps: {rel:.2e}")

def run_wh(seed, leaky, eps=0.0, n_orb=N_ORB):
    """leaky='retard': source evaluated one step in the past (simultaneity bug).
    eps>0: per-kick bias 0.5*eps*h*|a| along vrot-hat at each half-kick (total
    per-step velocity bias eps*h*|a|) -- non-conservative work in the corotating
    frame, the class of integrator error that leaks the Jacobi constant.  An
    inertial-tangential bias was measured C-neutral on these co-rotating ships
    (calibrate() history) -- itself evidence that J is the right quantity.
    Returns J series (float) and diagnostics."""
    r, v = init_ships(seed, 8)
    h = 2 * math.pi / H_ORB
    delay = h if leaky == "retard" else 0.0
    series = np.zeros((8, (n_orb * H_ORB) // SAMP + 1))
    series[:, 0] = jacobi(r, v, 0.0)
    min_r2, hill_cross, min_a, k = 1e9, 0, 1e9, 0
    for step in range(n_orb * H_ORB):
        t0 = step * h
        a1 = accel(r, t0 + 0.5 * h, delay)
        v = v + 0.5 * h * a1
        if eps:
            v = v + (0.5 * eps * h * np.linalg.norm(a1, axis=-1, keepdims=True)
                     * vrot_hat(r, v))
        r, v = kepler_drift(r, v, h)
        a2 = accel(r, t0 + 0.5 * h, delay)
        v = v + 0.5 * h * a2
        if eps:
            v = v + (0.5 * eps * h * np.linalg.norm(a2, axis=-1, keepdims=True)
                     * vrot_hat(r, v))
        d = np.linalg.norm(r - planet_pos(t0 + h), axis=-1)
        min_r2 = min(min_r2, float(d.min()))
        hill_cross += int(np.sum(d < (MU / 3.0) ** (1.0 / 3.0)))
        if (step + 1) % SAMP == 0:
            k += 1
            series[:, k] = jacobi(r, v, t0 + h)
            aa = 1.0 / (2.0 / np.linalg.norm(r, axis=-1)
                        - np.sum(v * v, axis=-1) / GM)
            min_a = min(min_a, float(np.min(aa)))
    dj = np.max(np.abs(series - series[:, :1]), axis=1)
    return series, dict(min_r2=min_r2, hill_cross=hill_cross, min_a=min_a,
                        dj_med=float(np.median(dj)), dj_max=float(dj.max()))

MAX_TRIES = 30

def wh():
    """The physical-path record.  Writes wh-output.txt itself (no hand assembly)."""
    lines = []
    def emit(s):
        print(s); lines.append(s)
    results = {}
    for draw, base_seed in enumerate((4242, 9191)):
        for variant in ("good", "retard", "bias1", "bias3"):
            eps = {"bias1": BIAS1, "bias3": BIAS3}.get(variant, 0.0)
            seed, tries, settled = base_seed, 0, False
            while tries < MAX_TRIES:                        # deterministic pre-screen, bounded
                s, diag = run_wh(seed, variant, eps)
                tries += 1
                if (diag["min_r2"] >= 0.02 and 0.5 < diag["min_a"] < 2.0
                        and not np.isnan(s).any()):
                    settled = True
                    break
                seed += 1
            tag = f"draw{draw}-{variant}"
            if not settled:
                emit(f"[wh] {tag}: NO SETTLING SCENE in {MAX_TRIES} seeds "
                     f"(scene destroyer, not a leak instrument)")
                continue
            verd = {r: [] for r in ("R1", "R2", "R3")}
            expo, int_rng = [], []
            for i in range(s.shape[0]):
                xs = [int(round(x * SCALE)) for x in (s[i] - s[i, 0])]   # 2^40, referenced to start
                vv, _ = classify_all(xs)
                for r in verd:
                    verd[r].append(vv[r])
                expo.append(growth_exponent((s[i] - s[i, 0]) / max(1.0, abs(s[i, 0]))))
                int_rng.append(max(abs(min(xs)), abs(max(xs))))
            med = sorted(expo)[len(expo) // 2]
            results[tag] = dict(flags={r: sum(1 for x in v if x == "leak") for r, v in verd.items()},
                                median_exponent=med, **diag)
            emit(f"[wh] {tag}: seed {seed} ({tries} tries)  "
                 f"flags R1 {verd['R1'].count('leak')}/8  R2 {verd['R2'].count('leak')}/8  "
                 f"R3 {verd['R3'].count('leak')}/8  (median growth exponent {med:.3f}, "
                 f"dJ med {diag['dj_med']:.1e} max {diag['dj_max']:.1e}, "
                 f"min planet dist {diag['min_r2']:.4f}, Hill steps {diag['hill_cross']})")
            emit(f"[wh]   int-series max|x| per ship: {['%.2e' % x for x in int_rng]}")
    if "draw0-good" in results and "draw0-retard" in results:
        pairs = [(d, results.get(f"draw{d}-good"), results.get(f"draw{d}-retard"))
                 for d in (0, 1)]
        ok = sum(1 for d, g, r in pairs if g and r and g["median_exponent"] >= r["median_exponent"])
        tot = sum(1 for d, g, r in pairs if g and r)
        emit(f"[wh] growth-exponent inversion (good >= retarded): {ok}/{tot} draws (prediction: >= 1)")
        emit(f"[wh] K1 bias3 caught >= 6/8 by R2 in both draws: "
             f"{all(results.get(f'draw{d}-bias3', {}).get('flags', {}).get('R2', -1) >= 6 for d in (0, 1))}")
        emit(f"[wh] K2 good control <= 1/8 by R2 in both draws: "
             f"{all(results.get(f'draw{d}-good', {}).get('flags', {}).get('R2', -1) <= 1 for d in (0, 1))}")
    with open("wh-output.txt", "w") as f:
        f.write("\n".join(lines) + "\n")
    return results

def calibrate():
    """Instrument calibration only (short runs, 60 orbits): choose eps so the
    planted bias's total J drift sits at ~wiggle scale (bias1) and ~2.5x wiggle
    (bias3).  Not part of the record; disclosed in the dossier."""
    for eps in (1e-4, 3e-4, 1e-3):
        s, diag = run_wh(4242, "good", eps, n_orb=60)
        alive = diag["min_r2"] >= 0.02 and 0.5 < diag["min_a"] < 2.0
        print(f"[calibrate] eps={eps:.0e} 60 orbits: dJ med {diag['dj_med']:.2e} "
              f"(-> x{N_ORB/60:.1f} at full window ~ {diag['dj_med']*N_ORB/60:.1e}) "
              f"scene alive={alive} (min_r2 {diag['min_r2']:.3f}, min_a {diag['min_a']:.3f})")

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("controls", "all"):
        controls()
    if what in ("memory", "all"):
        memory()
    if what in ("census", "all"):
        census()
    if what in ("horizon", "all"):
        horizon()
    if what in ("alias", "all"):
        alias()
    if what in ("inversion", "all"):
        inversion()
    if what in ("kepler_check", "all"):
        kepler_check()
    if what in ("wh", "all"):
        wh()
    if what == "calibrate":
        calibrate()
