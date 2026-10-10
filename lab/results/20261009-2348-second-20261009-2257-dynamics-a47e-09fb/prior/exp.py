#!/usr/bin/env python3
"""B12's instrument, from the dynamics: does a series sit on a bounded attractor or leak?

Rule under test (no fitted thresholds; integers decide):
  leak  <=>  AVAR(T/4) > AVAR(T/32)   computed exactly on the integer series (Fractions).
Theory (to be tested, see predictions.md):
  H1 horizon: a walk of per-sample sigma is detected iff sigma*sqrt(N) > sqrt(2)*A.
  H2 alias:   a bounded oscillation with period P > T/4 is misclassified as a leak.

Deterministic everywhere: one LCG, no numpy randomness, integerized decisions.
Run:  python3 exp.py controls | inversion | wh | all
"""
import json
import math
import sys
from fractions import Fraction

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
    """Allan variance of integer series xs at averaging time tau, exact rational."""
    m = len(xs) // tau
    if m < 2:
        return None
    means = [Fraction(sum(xs[k * tau:(k + 1) * tau]), tau) for k in range(m)]
    num = sum((means[k + 1] - means[k]) ** 2 for k in range(m - 1))
    return Fraction(num, 2 * (m - 1))

def classify(xs):
    """leak iff AVAR(T/4) > AVAR(T/32), exact.  Returns (verdict, {tau: AVAR})."""
    n = len(xs)
    t2, t1 = max(1, n // 4), max(1, n // 32)
    a2, a1 = avar_frac(xs, t2), avar_frac(xs, t1)
    return ("leak" if a2 > a1 else "bounded"), {t1: a1, t2: a2}

def kepler_drift(r, v, dt):
    """Exact two-body propagation about the star, vectorized (universal variables)."""
    r0 = np.linalg.norm(r, axis=-1, keepdims=True)
    sq = math.sqrt(GM)
    rv = np.sum(r * v, axis=-1, keepdims=True)
    alpha = -np.sum(v * v, axis=-1, keepdims=True) / GM + 2.0 / r0      # 1/a
    chi = sq * dt * alpha
    def F_of(chi):
        z = alpha * chi * chi
        C, S = stumpff_scalar(z)
        return (r0 * chi + rv / sq * chi * chi * C
                + (1 - alpha * r0 * chi * chi * C) / sq * chi ** 3 * S - sq * dt)
    for _ in range(80):
        F = F_of(chi)
        eps = 1e-7 * np.maximum(1.0, np.abs(chi))
        dF = (F_of(chi + eps) - F) / eps
        step = F / dF
        chi = chi - step
        if np.all(np.abs(step) < 1e-12 * np.maximum(1.0, np.abs(chi))):
            break
    z = alpha * chi * chi
    C, S = stumpff_scalar(z)
    f = 1 - chi * chi / r0 * C
    g = dt - chi ** 3 / sq * S
    rn = f * r + g * v
    rn_mag = np.linalg.norm(rn, axis=-1, keepdims=True)
    fdot = sq / (r0 * rn_mag) * (alpha * chi ** 3 * S - chi)
    gdot = 1 - chi * chi / rn_mag * C
    vn = fdot * r + gdot * v
    return rn, vn
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

# ---------------------------------------------------------------- Part A: planted integer controls
A = 1_000_000          # bounded amplitude, integer units
N = 1 << 15            # 32768 samples

def int_round(xs):
    return [int(round(v)) for v in xs]

def stumpff(z):
    """Stumpff C(z), S(z), elementwise."""
    z = np.atleast_1d(np.asarray(z, dtype=float))
    C = np.zeros_like(z); S = np.zeros_like(z)
    pos, neg = z > 1e-8, z < -1e-8
    mid = ~(pos | neg)
    zp = z[pos]; sz = np.sqrt(zp)
    C[pos] = (1 - np.cos(sz)) / zp; S[pos] = (sz - np.sin(sz)) / (zp * sz)
    zn = z[neg]; szn = np.sqrt(-zn)
    C[neg] = (1 - np.cosh(szn)) / zn; S[neg] = (np.sinh(szn) - szn) / (-zn) ** 1.5
    C[mid] = 0.5 - z[mid] / 24 + z[mid] ** 2 / 720
    S[mid] = 1 / 6 - z[mid] / 120 + z[mid] ** 2 / 5040
    return C, S


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

def sine_series(period):
    return int_round([A * 0.7 * math.cos(2 * math.pi * n / period) for n in range(N)])

def walk_series(rng, ratio):
    """random walk whose total drift sigma*sqrt(N) = ratio * A."""
    sigma = ratio * A / math.sqrt(N)
    x, xs = 0.0, []
    for _ in range(N):
        x += sigma * rng.sym()
        xs.append(x)
    return int_round(xs)

def controls():
    rows = []
    def add(name, truth, predicted, xs):
        v, _ = classify(xs)
        rows.append(dict(name=name, truth=truth, predicted=predicted, verdict=v,
                         ok_pred=(v == predicted), ok_truth=(v == truth)))

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

    ok_pred = sum(r["ok_pred"] for r in rows)
    ok_truth = sum(r["ok_truth"] for r in rows)
    misses_pred = [r["name"] for r in rows if not r["ok_pred"]]
    print(f"[controls] {len(rows)} series: predicted-outcome agreement {ok_pred}/{len(rows)}, "
          f"ground-truth agreement {ok_truth}/{len(rows)}")
    print(f"[controls] deviations from prediction: {misses_pred or 'none'}")
    for r in rows:
        flag = "" if r["ok_pred"] else "   <-- UNSCHEDULED"
        print(f"  {r['name']:<22} truth={r['truth']:<7} predicted={r['predicted']:<7} "
              f"verdict={r['verdict']:<7}{flag}")
    return rows

# ---------------------------------------------------------------- Part B: exponent inversion (P2 model)
def chaotic_sat(seed, lam, d0=1e-12, attractor=1.0):
    rng = LCG(seed)
    x, xs = d0, []
    for _ in range(N):
        x = x * math.exp(lam) if x < attractor else x
        if x >= attractor:                                   # wander on the attractor
            x = 0.9 * x + 0.35 * rng.sym()
            x = max(min(x, 1.4 * attractor), -1.4 * attractor)
        xs.append(x)
    return xs

def inversion():
    lam = math.log(1e12) / (N / 10.0)                        # saturates at 10% of the window
    sigma15 = 1.5 / math.sqrt(N)                             # leak: total drift 1.5 attractor units
    out = []
    for draw in range(3):
        rng = LCG(7000 + draw)
        exp_b, exp_l = [], []
        for s in range(16):
            exp_b.append(growth_exponent(chaotic_sat(100000 + draw * 100 + s, lam)))
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
    return out

# ---------------------------------------------------------------- Part C: the law's cheap path (Wisdom-Holman)
import numpy as np

MU = 1e-3                      # planet (Jupiter-like) mass / star mass
GM = 1.0 - MU                  # star
H_ORB = 120                    # steps per planet orbit
N_ORB = 250                    # planet orbits
SAMP = 60                      # steps between J samples

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

def run_wh(seed, leaky, n_ships=8):
    """leaky: 'retard' = source evaluated one step in the past (simultaneity bug);
    'order1' = asymmetric first-order kick.  Returns J series and diagnostics."""
    r, v = init_ships(seed, n_ships)
    h = 2 * math.pi / H_ORB
    delay = {"retard": h, "retard10": 10 * h}.get(leaky, 0.0)
    asym = leaky == "order1"
    series = np.zeros((n_ships, (N_ORB * H_ORB) // SAMP + 1))
    series[:, 0] = jacobi(r, v, 0.0)
    min_r2, hill_cross, min_a, k = 1e9, 0, 1e9, 0
    for step in range(N_ORB * H_ORB):
        t0 = step * h
        v = v + 0.5 * h * accel(r, t0 + 0.5 * h, delay)
        r, v = kepler_drift(r, v, h)
        if asym:
            v = v + h * accel(r, t0 + h, delay)
        else:
            v = v + 0.5 * h * accel(r, t0 + 0.5 * h, delay)
        d = np.linalg.norm(r - planet_pos(t0 + h), axis=-1)
        min_r2 = min(min_r2, float(d.min()))
        hill_cross += int(np.sum(d < (MU / 3.0) ** (1.0 / 3.0)))
        if (step + 1) % SAMP == 0:
            k += 1
            series[:, k] = jacobi(r, v, t0 + h)
            aa = 1.0 / (2.0 / np.linalg.norm(r, axis=-1)
                        - np.sum(v * v, axis=-1) / GM)
            min_a = min(min_a, float(np.min(aa)))
    return series, dict(min_r2=min_r2, hill_cross=hill_cross, min_a=min_a)

def wh():
    results = {}
    for draw, base_seed in enumerate((4242, 9191)):
        for variant in (False, "retard", "retard10", "order1"):
            seed = base_seed
            while True:                                  # deterministic pre-screen
                s, diag = run_wh(seed, variant)
                if (diag["min_r2"] >= 0.02 and 0.5 < diag["min_a"] < 2.0
                        and not np.isnan(s).any()):
                    break
                seed += 1
            verd, expo = [], []
            for i in range(s.shape[0]):
                xs = [int(round(x)) for x in (s[i] - s[i, 0])]       # integerized, referenced to start
                v_allan, _ = classify(xs)
                verd.append(v_allan)
                expo.append(growth_exponent((s[i] - s[i, 0]) / max(1.0, abs(s[i, 0])), floor=1e-12))
            tag = f"draw{draw}-{variant or 'good'}"
            nl = sum(1 for x in verd if x == "leak")
            results[tag] = dict(verdicts=verd, n_leak=nl,
                                median_exponent=sorted(expo)[len(expo) // 2], **diag)
            print(f"[wh] {tag}: Allan leak flags {nl}/8 (median growth exponent "
                  f"{sorted(expo)[len(expo)//2]:.3f}, min planet distance {diag['min_r2']:.4f}, "
                  f"Hill-crossing steps {diag['hill_cross']})")
    good_med = [results[f"draw{d}-good"]["median_exponent"] for d in (0, 1)]
    leak_med = [results[f"draw{d}-retard"]["median_exponent"] for d in (0, 1)]
    inv = sum(g >= l for g, l in zip(good_med, leak_med))
    print(f"[wh] growth-exponent inversion (good >= retarded): {inv}/2 draws (prediction: >= 1)")
    return results

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = {}
    if what in ("controls", "all"):
        out["controls"] = controls()
    if what in ("inversion", "all"):
        out["inversion"] = inversion()
    if what in ("wh", "all"):
        out["wh"] = wh()
