#!/usr/bin/env python3
"""CF probe v2: two predictors for a pair's close conjunctions.

Board premise under test (r8 v2 "next"): a pair's miss distance at successive
conjunctions is quasi-periodic, so its next close conjunction is a Diophantine
approximation (continued fractions); pay once per element change.

Predictor A (naive CF): close conjunctions sit at continued-fraction
convergent denominators of alpha = beat/2pi (homogeneous approximation).
Predictor B (jump arithmetic): the beat is constant, so from the current
conjunction's phase the next phase-near-periapsis conjunction is one division.

Model: inner circular orbit r1=1 (n1=1); outer eccentric a2,e2,varpi
(n2=a2^-1.5). Miss at a conjunction = |r2-r1|, smallest when the conjunction
longitude is near outer periapsis. Pure stdlib; ~3 s.
"""
import math, json, random

K = 600
SEEDS = 40
WINDOW = 3
TOP_FRAC = 0.05

def kepler(M, e):
    E = M
    for _ in range(50):
        d = (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        E -= d
        if abs(d) < 1e-13:
            break
    return E

def lam_outer(t, a2, e2, varpi, n2):
    M = (n2 * t) % (2 * math.pi)
    E = kepler(M, e2)
    nu = 2 * math.atan2(math.sqrt(1 + e2) * math.sin(E / 2),
                        math.sqrt(1 - e2) * math.cos(E / 2))
    return varpi + nu, a2 * (1 - e2 * math.cos(E))

def wrap(x):
    return (x + math.pi) % (2 * math.pi) - math.pi

def conjunctions(a2, e2, varpi):
    n2 = a2 ** -1.5
    T_syn = 2 * math.pi / (1 - n2)
    dt = T_syn / 24.0
    t, out, prev = 0.0, [], wrap(0.0 - lam_outer(0.0, a2, e2, varpi, n2)[0])
    while len(out) < K:
        t += dt
        cur = wrap(t - lam_outer(t, a2, e2, varpi, n2)[0])
        if prev * cur < 0:
            lo, hi = t - dt, t
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                v = wrap(mid - lam_outer(mid, a2, e2, varpi, n2)[0])
                if v * cur <= 0:
                    lo = mid
                else:
                    hi = mid
            tc = 0.5 * (lo + hi)
            lam2, r2 = lam_outer(tc, a2, e2, varpi, n2)
            out.append((tc, abs(r2 - 1.0), wrap(lam2 - varpi)))
        prev = cur
    return out

def cf_denominators(alpha, kmax):
    denoms = []
    x = alpha - int(alpha)
    m, d, a = 0, 1, int(x)
    p1, q1, p2, q2 = 1, 0, 0, 1
    for _ in range(40):
        p, q = a * p1 + p2, a * q1 + q2
        if q > kmax:
            break
        denoms.append(q)
        p2, q2, p1, q1 = p1, q1, p, q
        m = d * a - m
        d = (x - m) / d
        if abs(d) < 1e-15:
            break
        a = int(1.0 / d + 1e-12)
    return denoms

def main():
    rng = random.Random(20261009)
    rows = []
    for s in range(SEEDS):
        a2 = rng.uniform(1.05, 2.0)
        e2 = rng.uniform(0.05, 0.5)
        varpi = rng.uniform(0, 2 * math.pi)
        cs = conjunctions(a2, e2, varpi)
        phis = [c[2] for c in cs]
        miss = [c[1] for c in cs]
        acc, prev = 0.0, phis[0]
        for p in phis[1:]:
            acc += wrap(p - prev)
            prev = p
        b = acc / (K - 1)                       # mean beat (rad/conjunction)
        alpha = (b / (2 * math.pi)) % 1.0
        nclose = max(1, int(TOP_FRAC * K))
        close_idx = sorted(range(K), key=lambda i: miss[i])[:nclose]
        close_set = set(close_idx)
        miss_thr = sorted(miss)[nclose - 1]
        eps = max(abs(phis[i]) for i in close_idx)

        # Predictor A: CF denominators + small multiples
        cand = set()
        for q in cf_denominators(alpha, K):
            for m in range(1, 4):
                if m * q <= K:
                    cand.add(m * q)
        fA = sum(1 for i in close_idx if any(abs(i - c) <= WINDOW for c in cand)) / nclose

        # Predictor B: pure jump arithmetic on the beat, no drift correction
        predB = []
        k = 0
        while k < K - 1:
            phi = phis[k]
            gap = (-phi) % (2 * math.pi)        # forward distance of phase to 0
            step = int(math.ceil(max(0.0, gap - eps) / abs(b))) if abs(b) > 1e-12 else K
            k2 = k + max(1, step)
            if k2 >= K:
                break
            predB.append(k2)
            k = k2
        hitB = [i for i in predB if miss[i] <= miss_thr]
        precB = len(hitB) / max(1, len(predB))
        recB = len(hitB) / nclose

        lin_res = max(abs(wrap(phis[k] - (phis[0] + k * b))) for k in range(K))
        best = min(range(K), key=lambda i: miss[i])
        bestA = any(abs(best - c) <= WINDOW for c in cand)
        resonant = any(abs(alpha - p / q) < 1e-4
                       for q in range(1, 51) for p in range(q + 1))
        rows.append(dict(seed=s, a2=round(a2, 4), e2=round(e2, 4),
                         alpha=round(alpha, 6), fA=round(fA, 3),
                         bestA=bool(bestA), bestB=bool(best in predB),
                         precB=round(precB, 3), recB=round(recB, 3),
                         lin_res_rad=round(lin_res, 4), eps_rad=round(eps, 4),
                         resonant=bool(resonant), n_predB=len(predB)))
    def med(xs): return sorted(xs)[len(xs) // 2] if xs else None
    summary = dict(
        seeds=SEEDS, K=K, window=WINDOW, top_frac=TOP_FRAC,
        median_fA=round(med([r["fA"] for r in rows]), 3),
        bestA_rate=round(sum(r["bestA"] for r in rows) / len(rows), 3),
        median_precB=round(med([r["precB"] for r in rows]), 3),
        median_recB=round(med([r["recB"] for r in rows]), 3),
        bestB_rate=round(sum(r["bestB"] for r in rows) / len(rows), 3),
        median_lin_res_over_eps=round(med([r["lin_res_rad"] / max(1e-9, r["eps_rad"]) for r in rows]), 2),
        median_fA_resonant=(round(med([r["fA"] for r in rows if r["resonant"]]), 3)),
        median_fA_nonresonant=(round(med([r["fA"] for r in rows if not r["resonant"]]), 3)),
        median_fA_e_le_02=round(med([r["fA"] for r in rows if r["e2"] <= 0.2]), 3),
        median_fA_e_ge_03=round(med([r["fA"] for r in rows if r["e2"] >= 0.3]), 3),
    )
    with open(__file__.replace("cf_probe.py", "cf_probe_out.json"), "w") as f:
        json.dump(dict(summary=summary, rows=rows), f, indent=1)
    print(json.dumps(summary, indent=1))

if __name__ == "__main__":
    main()
