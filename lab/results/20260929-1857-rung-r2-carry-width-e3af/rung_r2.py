#!/usr/bin/env python3
"""Rung r2 — carry width. Sigma-delta storage of memoized per-cycle increments and of
kick streams, at 16/24/32 bits, against the ported Schwarzschild oracle.

Mechanism (first-order sigma-delta, stated in the dossier): per body, per quantity
Q in {dphi, dt, dtau, E, L}: one shared exponent (block floating point) and two w-bit
registers, value + carry, together one 2w-bit fixed-point accumulator at unit F.
  - increments (constant per body): the pair holds the increment once (value = top w
    bits, carry = low w bits); the wide phase counter advances by exact integer adds.
    For w = 32 the pair is exact (a float64 has <= 53 significant bits).
  - E, L: the pair accumulates the kick stream, each kick gridded at F (half-even);
    the carry holds the sub-LSB residue and spills into the value word. The stored sum
    is exact in integers; the only loss is the input graining.
  - trunc16/round16: a single w-bit word, truncation or round-half-even, no carry.

Reference (rung truth): the same float64 increments, summed exactly (fsum semantics:
phi_ref(N) = N*x exactly). All metric differences are exact (integers / Fractions).
"""
import json, math, random
from fractions import Fraction

import numpy as np

RUN = "lab/results/20260929-1857-rung-r2-carry-width-e3af"
N_SEEDS, N_CYCLES, N_SYNODIC, N_KICKS = 64, 10**6, 10**4, 10**6
CONFIGS = [("sd16", 16, "sd"), ("sd24", 24, "sd"), ("sd32", 32, "sd"),
           ("trunc16", 16, "trunc"), ("round16", 16, "round")]

# ---------------------------------------------------------------- ported oracle
def ellip_k(m):
    a, g = 1.0, math.sqrt(1.0 - m)
    for _ in range(40):
        a1, g1 = (a + g) / 2.0, math.sqrt(a * g)
        if abs(a1 - g1) <= 1e-17 * a1:
            a = a1
            break
        a, g = a1, g1
    return math.pi / (2.0 * a)

def ellip_k_minus_half_pi(m):
    if m >= 0.25:
        return ellip_k(m) - math.pi / 2.0
    c, mn, s = 1.0, 1.0, 0.0
    for n in range(1, 200):
        c *= (2 * n - 1) / (2 * n)
        mn *= m
        term = c * c * mn
        s += term
        if term < 1e-19 * s:
            break
    return math.pi / 2.0 * s

def periapsis_elliptic(p, e):
    d = p - 6.0 + 2.0 * e
    s = math.sqrt(p / d)
    s_minus_1 = (6.0 - 2.0 * e) / d / (s + 1.0)
    return 4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + math.pi / 2.0 * s_minus_1)

_GL32 = None
def gauss_legendre(n):
    out = []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        dp = 0.0
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p2 = ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
                p0, p1 = p1, p2
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        out.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
    return out

def integrate_gl(lo, hi, pieces, f):
    global _GL32
    if _GL32 is None:
        _GL32 = gauss_legendre(32)
    s = 0.0
    for j in range(pieces):
        a = lo + (hi - lo) * j / pieces
        b = lo + (hi - lo) * (j + 1) / pieces
        for x, w in _GL32:
            s += (b - a) * 0.5 * w * f((a + b) * 0.5 + (b - a) * 0.5 * x)
    return s

def bound_constants(p, e):
    energy = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / math.sqrt(p - 3.0 - e * e)
    return energy, angular

def bound_period_quad(p, e):
    energy, angular = bound_constants(p, e)
    def refine(f):
        pieces, v = 16, integrate_gl(0.0, 2.0 * math.pi, 16, f)
        while pieces < 1 << 14:
            pieces *= 2
            w = integrate_gl(0.0, 2.0 * math.pi, pieces, f)
            done = abs(w - v) <= 1e-14 * abs(w)
            v = w
            if done:
                break
        return v
    def r_of(chi):
        return p / (1.0 + e * math.cos(chi))
    t = refine(lambda chi: (p / (p - 6.0 - 2.0 * e * math.cos(chi))) ** 0.5
               * r_of(chi) ** 2 / angular * energy / (1.0 - 2.0 / r_of(chi)))
    tau = refine(lambda chi: (p / (p - 6.0 - 2.0 * e * math.cos(chi))) ** 0.5
                 * r_of(chi) ** 2 / angular)
    return t, tau

def orbit_increments(p, e):
    dphi = 2.0 * math.pi + periapsis_elliptic(p, e)
    t, tau = bound_period_quad(p, e)
    return dphi, t, tau

# ---------------------------------------------------------------- sampler (frozen)
def draw_case(rng):
    p = math.exp(rng.uniform(math.log(10.0), math.log(1000.0)))
    e = rng.uniform(0.0, 0.7)
    return p, e

master = random.Random(20261001)
PHASE = [draw_case(master) for _ in range(N_SEEDS)]
CONJ = [(*draw_case(master), *draw_case(master), 10.0 ** master.uniform(-6.0, -2.0))
        for _ in range(N_SEEDS)]                       # (pA,eA,pB,eB,rho)
KICK_ORB = [draw_case(master) for _ in range(N_SEEDS)]
KICK_SEEDS = [[master.getrandbits(62), master.getrandbits(62)] for _ in range(N_SEEDS)]

MEAN_M = (1e-6 - 1e-10) / (4.0 * math.log(10.0))       # mean of log-uniform [1e-10,1e-6]
Q_PLUS = 0.5 * (1.0 + 1e-8 / MEAN_M)                   # sign bias => drift +1e-8/kick

def sd_pair(x, w):
    """2w-bit pair for a positive float64 x: (X, F), F a power of two, X = round(x/F)
    using the 2w bits (value = top w, carry = low w). Exact when 2w >= 54."""
    E = math.floor(math.log2(x))
    F = 2.0 ** (E - (2 * w - 1))
    X = int(round(x / F))                               # x/F exact (power-of-2 scale)
    if X >= 1 << (2 * w):
        F *= 2.0
        X >>= 1
    return X, F

def plain_word(x, w, mode):
    E = math.floor(math.log2(x))
    q = 2.0 ** (E - (w - 1))
    v = x / q                                           # exact
    n = int(math.trunc(v)) if mode == "trunc" else int(round(v))
    if n >= 1 << w:
        q *= 2.0
        n >>= 1
    return n, q

def growth_exponent(ns, errs):
    """Fitted exponent of |err| vs n over the last 90%: Theil-Sen (median of
    pairwise slopes) through medians of 10 log-spaced windows. Robust on
    stochastic single paths; a global least-squares fit is estimator-dominated.
    Identically-zero error => 0.0 by definition."""
    nmax = max(ns)
    pts = [(n, e) for n, e in zip(ns, errs) if e > 0.0 and n >= 0.1 * nmax]
    if len(pts) < 3:
        return 0.0
    ln_n = np.array([math.log(n) for n, _ in pts])
    ln_e = np.array([math.log(e) for _, e in pts])
    edges = np.linspace(ln_n.min(), ln_n.max(), 11)
    bx, by = [], []
    for i in range(10):
        sel = (ln_n >= edges[i]) & ((ln_n <= edges[i + 1]) if i == 9 else (ln_n < edges[i + 1]))
        if sel.sum() >= 1:
            bx.append(float(np.median(ln_n[sel]))); by.append(float(np.median(ln_e[sel])))
    if len(bx) < 3:
        return 0.0
    slopes = [(by[j] - by[i]) / (bx[j] - bx[i])
              for i in range(len(bx)) for j in range(i + 1, len(bx)) if bx[j] > bx[i]]
    return float(np.median(slopes))

SAMPLE_N = sorted(set(int(round(10.0 ** (6.0 * i / 159.0))) for i in range(160)))

# ================================================================ phase runs
def phase_case(configs):
    expo = {n: [] for n, _, _ in configs}
    worst = {}
    for p, e in PHASE:
        dphi, dt, dtau = orbit_increments(p, e)
        for name, w, mode in configs:
            if mode == "sd":
                X, F = sd_pair(dphi, w)
                stored = Fraction(X) * Fraction(F)
            else:
                nn, q = plain_word(dphi, w, mode)
                stored = Fraction(nn) * Fraction(q)
            rho = abs(stored - Fraction(dphi))          # exact dyadic residue
            errs = [rho * N for N in SAMPLE_N]          # exact: err(N) = N * rho
            ex = growth_exponent(SAMPLE_N, [float(x) for x in errs])
            expo[name].append(ex)
            if name not in worst or ex >= worst[name][0]:
                worst[name] = (ex, [float(x) for x in errs])
    return ({n: max(v) for n, v in expo.items()},
            {n: v for n, v in expo.items()},
            worst)

# ================================================================ conjunctions
PI_F = Fraction("3.14159265358979323846264338327950288419716939937510582097494459"
                "2307816406286208998628034825342117067982148086513282306647093844")

def event_sequence(dphiA, dtA, dphiB, dtB):
    """Closed form, exact rationals. Memoized uniform rate Omega = dphi/dt per body;
    events over N_SYNODIC synodic periods: conjunctions C (phiA-phiB = 0 mod 2pi) and
    each body's periapsis passages (A, B). Returns the ordered type string."""
    OA = Fraction(dphiA) / Fraction(dtA)
    OB = Fraction(dphiB) / Fraction(dtB)
    dO = abs(OA - OB)
    if dO == 0:
        return None
    Psyn = 2 * PI_F / dO
    Tend = N_SYNODIC * Psyn
    fA, fB = Fraction(dtA), Fraction(dtB)
    nA, nB = int(Tend / fA), int(Tend / fB)
    D = Psyn.denominator * (1 << 400)
    dP = Psyn.numerator * (D // Psyn.denominator)
    kA = fA.numerator * (D // fA.denominator)
    kB = fB.numerator * (D // fB.denominator)
    ev = [(dP * k, 1, "C") for k in range(1, N_SYNODIC + 1)]
    ev += [(kA * m, 2, "A") for m in range(1, nA + 1)]
    ev += [(kB * m, 3, "B") for m in range(1, nB + 1)]
    ev.sort()
    return "".join(t for _, _, t in ev)

def conj_stored(w, mode, case):
    pA, eA, pB, eB, rho = case
    phiA, tA, _ = orbit_increments(pA, eA)
    phiB, tB, _ = orbit_increments(pB, eB)
    tB = tB * (rho * tA / tB)                           # B's clock scaled: T_B = rho*T_A
    def store(x):
        if mode == "sd":
            X, F = sd_pair(x, w)
            return Fraction(X) * Fraction(F)
        nn, q = plain_word(x, w, mode)
        return Fraction(nn) * Fraction(q)
    return store(phiA), store(tA), store(phiB), store(tB), phiA, tA, phiB, tB

def conj_case(configs):
    ok = {n: 0 for n, _, _ in configs}
    for case in CONJ:
        *ref_incs, phiA, tA, phiB, tB = conj_stored(32, "sd", case)
        ref = event_sequence(phiA, tA, phiB, tB)
        for name, w, mode in configs:
            if mode == "sd" and w == 32:
                sto = ref                               # sd32 increments stored exactly
            else:
                sA, stA, sB, stB, *_ = conj_stored(w, mode, case)
                sto = event_sequence(sA, stA, sB, stB)
            if ref is not None and sto == ref:
                ok[name] += 1
    return {n: ok[n] / len(CONJ) for n, _, _ in configs}

# ================================================================ kick runs
BOUNDS = sorted(set(min(N_KICKS, max(1, int(round(10.0 ** (6.0 * i / 239.0))))) for i in range(240)))

def gen_kicks(seed, v0):
    """Log-uniform magnitudes in [1e-10,1e-6] of the value; signs biased so the true
    secular drift is +1e-8 per kick. numpy PCG64 seeded from the master sampler."""
    rng = np.random.default_rng(seed)
    m = 10.0 ** (-10.0 + 4.0 * rng.random(N_KICKS))
    s = np.where(rng.random(N_KICKS) < Q_PLUS, 1.0, -1.0)
    return s * m * v0

def reference_prefixes(kicks):
    seg = np.zeros(N_KICKS + 1, dtype=bool)
    seg[BOUNDS] = True; seg[0] = True
    idx = np.flatnonzero(seg)
    seg_ref = [math.fsum(kicks[a:b]) for a, b in zip(idx[:-1], idx[1:])]
    return idx, seg_ref, [math.fsum(seg_ref[:j + 1]) for j in range(len(seg_ref))]

def kick_all_configs(configs):
    npass = {n: 0 for n, _, _ in configs}
    worst = {n: 0.0 for n, _, _ in configs}
    per_seed = {n: [] for n, _, _ in configs}
    for i, (p, e) in enumerate(KICK_ORB):
        E0, L0 = bound_constants(p, e)
        ok_name = {n: True for n, _, _ in configs}
        for q, v0 in ((0, E0), (1, L0)):
            kicks = gen_kicks(KICK_SEEDS[i][q], v0)
            idx, seg_ref, ref_pref = reference_prefixes(kicks)
            ref_total = math.fsum(seg_ref)              # == fsum(all kicks)
            v0F = Fraction(v0)
            for name, w, mode in configs:
                if mode == "sd":
                    F = 2.0 ** (math.floor(math.log2(v0)) - (2 * w - 2))
                    kf = np.rint(kicks / F).astype(np.int64)
                    S0 = int(round(v0 / F))
                else:
                    F = 2.0 ** (math.floor(math.log2(v0)) - (w - 1))
                    div = kicks / F
                    kf = (np.trunc(div) if mode == "trunc" else np.rint(div)).astype(np.int64)
                    S0 = int(round(v0 / F))
                seg_st = np.add.reduceat(kf, idx[:-1]).astype(object)
                pref, acc = [], 0
                for s in seg_st:
                    acc = int(acc) + int(s)
                    pref.append(acc)
                Fs = Fraction(F)
                dst = abs(Fraction(pref[-1] + S0) * Fs - v0F - Fraction(ref_total))
                dref = abs(Fraction(ref_total))
                if dref == 0 or dst > Fraction(1, 100) * dref:
                    ok_name[name] = False
                res = [abs(Fraction(pref[j] + S0) * Fs - v0F - Fraction(ref_pref[j]))
                       for j in range(len(pref))]
                ex = growth_exponent(BOUNDS, [float(r) for r in res])
                worst[name] = max(worst[name], ex)
                per_seed[name].append(ex)
        for name, _, _ in configs:
            if ok_name[name]:
                npass[name] += 1
    return ({n: npass[n] / len(KICK_ORB) for n, _, _ in configs}, worst, per_seed)

# ================================================================ driver
def main():
    ph_max, ph_all, ph_worst = phase_case(CONFIGS)
    order = conj_case(CONFIGS)
    drift, kick_worst, kick_all = kick_all_configs(CONFIGS)
    metrics, detail = {}, {}
    for name, w, mode in CONFIGS:
        metrics[name] = {
            "phase_error_growth_exponent": round(ph_max[name], 4),
            "conjunction_order_fraction": round(order[name], 4),
            "kick_drift_pass_fraction": round(drift[name], 4),
            "kick_residual_growth_exponent": round(kick_worst[name], 4),
            "bits_per_body": 5 * (2 * w) if mode == "sd" else 5 * w,
        }
        detail[name] = {
            "phase_exponents": [round(x, 3) for x in ph_all[name]],
            "kick_exponents": [round(x, 3) for x in kick_all[name]],
            "worst_phase_errors": ph_worst[name][1],
        }
        print(name, json.dumps(metrics[name]), flush=True)
    with open(f"{RUN}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=1)
    with open(f"{RUN}/detail.json", "w") as f:
        json.dump({"sample_N": SAMPLE_N, "kick_bounds": BOUNDS, "detail": detail}, f)

if __name__ == "__main__":
    main()
