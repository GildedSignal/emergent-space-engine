#!/usr/bin/env python3
"""CF conjunction-calendar probe, v2 (bug-fixed CF recurrence init; conjunction anchor j0).

Truth: brute-force fine time grid -> miss sequence d_k per synodic window, k=0..K-1.
Predictors (elements only, no orbit integration):
  cf   : candidates = convergent/semiconvergent denominators of omega = frac(n1/(n1-n2))
         (+ small multiples), pick k minimizing |lam_ref + k*omega - tau| mod 1.
  inv  : O(1) drift inversion k ~ (tau - lam_ref)/omega (nearest integers + boundaries).
tau = longitude (in turns) minimizing the 1D surrogate |r1(lam) - r2(lam)|.
lam_ref = mean longitude of the first conjunction at t>=0 (anchor j0, the v1 bug).
Outputs metrics.json.
"""
import json, math, random, sys

TWO_PI = 2.0 * math.pi

def kepler_E(M, e):
    E = M
    for _ in range(40):
        f = E - e * math.sin(E) - M
        E -= f / (1.0 - e * math.cos(E))
    return E

def radius_at_longitude(a, e, lam):
    E = 2.0 * math.atan2(math.sqrt(1.0 - e) * math.sin(lam / 2.0),
                         math.sqrt(1.0 + e) * math.cos(lam / 2.0))
    return a * (1.0 - e * math.cos(E))

def state(a, e, M0, w, t, n):
    M = (M0 + n * t) % TWO_PI
    E = kepler_E(M, e)
    x = a * (math.cos(E) - e)
    y = a * math.sqrt(1.0 - e * e) * math.sin(E)
    c, s = math.cos(w), math.sin(w)
    return (x * c - y * s, x * s + y * c)

def convergents(x, qmax):
    """Correct convergents + semiconvergents of x in (0,1): list of (p,q), q<=qmax."""
    out = []
    p_m2, p_m1 = 1, 0   # p_{-2}=1? No: process a0=0 first -> p0=0,q0=1
    q_m2, q_m1 = 0, 1
    # after consuming a0=0: convergent 0/1 already; recurrence continues with a1,a2,...
    r = x - math.floor(x)
    for _ in range(40):
        if r < 1e-12:
            break
        a = int(1.0 / r)
        if a > 10**9:
            break
        r = 1.0 / r - a
        p = a * p_m1 + p_m2
        q = a * q_m1 + q_m2
        if q > qmax:
            # semiconvergents up to qmax may still exist below this convergent
            mmax = (qmax - q_m2) // max(q_m1, 1)
            for m in range(1, mmax + 1):
                out.append((m * p_m1 + p_m2, m * q_m1 + q_m2))
            break
        for m in range(1, a + 1):  # semiconvergents ending at the convergent itself
            out.append((m * p_m1 + p_m2, m * q_m1 + q_m2))
        p_m2, p_m1 = p_m1, p
        q_m2, q_m1 = q_m1, q
    return [(p, q) for (p, q) in out if 0 < q <= qmax]

def cf_candidates(x, K):
    """Candidate conjunction indices: semiconvergent/convergent denominators + small multiples."""
    s = set()
    for (p, q) in convergents(x, 3 * K + 5):
        for mult in (1, 2, 3):
            k = q * mult
            if 0 < k < K:
                s.add(k)
    return sorted(s)

def dist1(v):
    v = v % 1.0
    return min(v, 1.0 - v)

def instrument_checks(rng, trials=1000):
    K = 30
    homog = inhomog = 0
    for _ in range(trials):
        x = rng.random()
        tau = rng.random()
        cands = set(cf_candidates(x, K))
        kh = min(range(1, K), key=lambda k: dist1(k * x))
        ki = min(range(0, K), key=lambda k: dist1(k * x - tau))
        homog += kh in cands
        inhomog += ki in cands
    return homog / trials, inhomog / trials

def run_seed(rng, e_band, K=30, NSTEP=200):
    a1, a2 = 1.0, rng.uniform(0.90, 1.10)
    e1, e2 = rng.uniform(*e_band), rng.uniform(*e_band)
    M01, M02 = rng.uniform(0, TWO_PI), rng.uniform(0, TWO_PI)
    w1, w2 = rng.uniform(0, TWO_PI), rng.uniform(0, TWO_PI)
    n1 = 1.0
    n2 = a2 ** -1.5
    dsyn = n1 - n2
    if abs(dsyn) < 1e-9:
        return None
    Tsyn = TWO_PI / abs(dsyn)
    d = [math.inf] * K
    for k in range(K):
        for i in range(NSTEP):
            t = k * Tsyn + i * Tsyn / NSTEP
            x1, y1 = state(a1, e1, M01, w1, t, n1)
            x2, y2 = state(a2, e2, M02, w2, t, n2)
            dd = math.hypot(x1 - x2, y1 - y2)
            if dd < d[k]:
                d[k] = dd
    # --- predictor inputs from elements only ---
    NL = 720
    S = [abs(radius_at_longitude(a1, e1, j * TWO_PI / NL) -
             radius_at_longitude(a2, e2, j * TWO_PI / NL)) for j in range(NL)]
    lam_t = min(range(NL), key=lambda j: S[j])
    tau = lam_t / NL
    omega = (n1 / (n1 - n2)) % 1.0
    phi1, phi2 = M01 + w1, M02 + w2
    j0 = math.ceil(-(phi2 - phi1) / TWO_PI) if dsyn > 0 else math.floor(-(phi2 - phi1) / TWO_PI)
    lam_ref = ((phi1 + n1 * (phi2 - phi1 + TWO_PI * j0) / (n1 - n2)) / TWO_PI) % 1.0
    # CF predictor
    cands = [k for k in cf_candidates(omega, K) if 0 < k < K]
    k_cf = min(cands, key=lambda k: dist1(lam_ref + k * omega - tau))
    # O(1) inversion predictor
    k0f = (tau - lam_ref) / omega if omega > 1e-12 else 1.0
    scan = set([int(k0f) + i for i in range(-3, 5)] + [0, 1, K - 1, K // 2])
    k_inv = min((k for k in scan if 0 <= k < K), key=lambda k: dist1(lam_ref + k * omega - tau),
                default=0)
    # truth stats
    ds = sorted(d)
    k_true = min(range(K), key=lambda k: d[k])
    rank = lambda k: ds.index(d[k]) / (K - 1)
    # recurrence (controlled): q_best = convergent denominator minimizing ||q*omega||
    convs = [(p, q) for (p, q) in convergents(omega, K // 2) if q > 0]
    q_best = min((q for (p, q) in convs), key=lambda q: dist1(q * omega), default=1)
    q_rand = rng.randrange(1, K // 2 + 1)
    med_d = sorted(d)[K // 2]
    rec = (d[(k_true + q_best) % K] / med_d, d[(k_true + q_rand) % K] / med_d)
    chi = 2.0 * max(e1, e2) * 1.0 / abs(dsyn)  # wobble rate / synodic drift rate
    return {"chi": chi, "rank_cf": rank(k_cf), "ratio_cf": d[k_cf] / d[k_true],
            "rank_inv": rank(k_inv), "ratio_inv": d[k_inv] / d[k_true],
            "rank_rand": rank(rng.randrange(K)), "dk_cf": abs(k_cf - k_true),
            "dk_inv": abs(k_inv - k_true), "rec_best": rec[0], "rec_rand": rec[1],
            "n_cands": len(cands)}

def degeneracy(rng):
    q = 7
    base = 7.0 ** (2.0 / 3.0)  # n2/n1 = 7 exactly when a2 = 7^(2/3)
    res = {}
    K, NSTEP = 30, 200
    e1 = e2 = 0.05
    M01, M02, w1, w2 = 0.3, 5.0, 0.0, 1.0
    for eps in [0.0, 1e-6, 1e-4, 1e-2]:
        a2 = base * (1.0 + eps)
        a1 = 1.0
        n1, n2 = 1.0, a2 ** -1.5
        dsyn = n1 - n2
        Tsyn = TWO_PI / abs(dsyn)
        d = [math.inf] * K
        for k in range(K):
            for i in range(NSTEP):
                t = k * Tsyn + i * Tsyn / NSTEP
                x1, y1 = state(a1, e1, M01, w1, t, n1)
                x2, y2 = state(a2, e2, M02, w2, t, n2)
                dd = math.hypot(x1 - x2, y1 - y2)
                if dd < d[k]:
                    d[k] = dd
        k_true = min(range(K), key=lambda k: d[k])
        res[f"eps={eps:g}"] = {"k_true": k_true, "k_true_mod_q": k_true % q,
                               "flatness": (max(d) - min(d)) / max(d)}
    return res

def main():
    rng = random.Random(1897)
    homog, inhomog = instrument_checks(rng)
    out = {"instrument_homog_pass_rate": homog, "instrument_inhomog_pass_rate": inhomog}
    for name, band in {"e_le_0.05": (0.0, 0.05), "e_05_15": (0.05, 0.15),
                       "e_15_30": (0.15, 0.30)}.items():
        seeds = []
        while len(seeds) < 66:
            r = run_seed(rng, band)
            if r:
                seeds.append(r)
        med = lambda key: sorted(s[key] for s in seeds)[len(seeds) // 2]
        frac = lambda key, th: sum(1 for s in seeds if s[key] <= th) / len(seeds)
        strat = {"chi<0.5": [], "0.5<=chi<2": [], "chi>=2": []}
        for s in seeds:
            if s["chi"] < 0.5: strat["chi<0.5"].append(s)
            elif s["chi"] < 2.0: strat["0.5<=chi<2"].append(s)
            else: strat["chi>=2"].append(s)
        out[name] = {
            "median_rank_cf": med("rank_cf"), "frac_rank_cf_le_10": frac("rank_cf", 0.10),
            "median_ratio_cf": med("ratio_cf"), "frac_ratio_cf_le_2x": frac("ratio_cf", 2.0),
            "median_rank_inv": med("rank_inv"), "frac_rank_inv_le_10": frac("rank_inv", 0.10),
            "median_ratio_inv": med("ratio_inv"), "frac_ratio_inv_le_2x": frac("ratio_inv", 2.0),
            "median_rank_rand": med("rank_rand"),
            "exact_k_cf": frac("dk_cf", 0), "within2_k_cf": frac("dk_cf", 2),
            "exact_k_inv": frac("dk_inv", 0), "within2_k_inv": frac("dk_inv", 2),
            "median_rec_best": med("rec_best"), "median_rec_rand": med("rec_rand"),
            "median_n_cands": med("n_cands"),
            "strat": {g: {"n": len(v),
                          "median_rank_cf": (sorted(x["rank_cf"] for x in v)[len(v)//2] if v else None),
                          "median_rank_inv": (sorted(x["rank_inv"] for x in v)[len(v)//2] if v else None),
                          "median_ratio_cf": (sorted(x["ratio_cf"] for x in v)[len(v)//2] if v else None),
                          "exact_k_cf": (sum(1 for x in v if x["dk_cf"]==0)/len(v) if v else None)}
                      for g, v in strat.items()}}
    out["degeneracy"] = degeneracy(rng)
    path = sys.argv[1] if len(sys.argv) > 1 else "metrics.json"
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
