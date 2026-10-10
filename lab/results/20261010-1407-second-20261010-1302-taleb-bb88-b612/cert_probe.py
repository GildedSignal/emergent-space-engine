#!/usr/bin/env python3
"""The re-sized phase-neighbour window, measured (checker's named experiment for
run 20261010-1302-taleb-bb88).

Claim under test: keying the co-orbital certificate by apsis-passage time with a
uniform window finds every real contact (zero misses) at candidate cost
2*W*n/P ~ the real contact count, for any e and density; the gold's fixed
rank-4 window drops a growing fraction. Two windows are computed per run:
  W  = R/v_apo + 3*(da/a)*(T+P)            (pre-registered, predictions.md)
  W' = (R + X)/v_apo + 3*(da/a)*(T+P)      (corrected; X = (1+e)*2da + 2de +
                                            (1+e)*2dw, the apoapsis differential-
                                            conjunction reach; predictions.md
                                            addendum) -- suffix _c in metrics.

Truth machinery is identical to the original probe.py (same fleet generator,
same KD-tree-per-epoch sampler), so pair counts are comparable run-to-run.
The certificate itself is O(n log n), no sampling: apsis-time keys
tau_i = M0_i/n_i mod Pm, frozen at t=0 (pairwise tau-distances are invariant:
tau_i(t) = tau_i(0) + t exactly).

Usage: python3 cert_probe.py out.json [full|bonly|pilot]
"""
import json, sys, time
import numpy as np
from scipy.spatial import cKDTree

MU = 4 * np.pi**2

def make_fleet(n, e0, da, de, dw, seed):
    # verbatim from the original probe.py (same draw order -> same fleets)
    r = np.random.default_rng(seed)
    a = 1.0 + r.uniform(-da, da, n)
    e = np.clip(e0 + r.uniform(-de, de, n), 0.0, 0.999)
    w = r.uniform(-dw, dw, n)
    M0 = r.uniform(0, 2 * np.pi, n)
    return a, e, w, M0

def positions(a, e, w, M):
    # verbatim from the original probe.py
    E = M + e * np.sin(M)
    for _ in range(30):
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    xo = a * (np.cos(E) - e)
    yo = a * np.sqrt(1 - e**2) * np.sin(E)
    c, s = np.cos(w), np.sin(w)
    return xo * c - yo * s, xo * s + yo * c

def truth_pairs(a, e, w, M0, nn, R, T, K):
    """All pairs ever within R over T at K sampled epochs (encoded i*n+j, i<j)."""
    n = len(a)
    acc = np.empty(0, dtype=np.int64)
    for k in range(K):
        t = T * k / K
        M = (M0 + nn * t) % (2 * np.pi)
        x, y = positions(a, e, w, M)
        tree = cKDTree(np.column_stack([x, y]))
        pr = tree.query_pairs(R, output_type="ndarray")
        if len(pr):
            acc = np.unique(np.concatenate([acc, pr[:, 0].astype(np.int64) * n + pr[:, 1]]))
    return acc

def cert_metrics(a, e, M0, pairs, R, T, da, de, dw, e0):
    """Certificate metrics for both windows. pairs: int64 codes (i<j)."""
    n = len(a)
    nn = np.sqrt(MU / a**3)
    Pm = float(np.mean(2 * np.pi / nn))
    tau = np.mod(M0 / nn, Pm)                      # apsis-passage time key, frozen
    v_apo = np.sqrt(MU / a) * np.sqrt((1 - e) / (1 + e))
    W = R / v_apo.min() + 3 * da * (T + Pm)        # pre-registered window
    X = (1 + e0) * 2 * da + 2 * de + (1 + e0) * 2 * dw   # apoapsis sensitivities
    Wc = (R + X) / v_apo.min() + 3 * da * (T + Pm) # corrected window
    W0 = R / v_apo.min()                           # negative control: no drift term
    lam = W * n / Pm                               # one-sided mean reach (spacings)

    order = np.argsort(tau)
    tsort = tau[order]
    pos = np.empty(n, dtype=np.int64); pos[order] = np.arange(n)
    t3 = np.concatenate([tsort - Pm, tsort, tsort + Pm])
    def window_cost(W_):
        lo = np.searchsorted(t3, tsort - W_, side="left")
        hi = np.searchsorted(t3, tsort + W_, side="right")
        c = np.empty(n); c[order] = hi - lo - 1
        return c
    cost = window_cost(W)
    cost_c = window_cost(Wc)

    orderM = np.argsort(M0)                        # the gold's coordinate
    posM = np.empty(n, dtype=np.int64); posM[orderM] = np.arange(n)

    if len(pairs):
        i = pairs // n; j = pairs % n
        d = np.abs(tau[i] - tau[j]); dtau = np.minimum(d, Pm - d)
        r = np.abs(pos[i] - pos[j]); steps = np.minimum(r, n - r)
        rM = np.abs(posM[i] - posM[j]); stepsM = np.minimum(rM, n - rM)
        return {
            "n_pairs": int(len(pairs)),
            "enc_per_body": 2 * len(pairs) / n,
            "misses": int(np.sum(dtau > W)),
            "miss_frac": float(np.mean(dtau > W)),
            "misses_W0": int(np.sum(dtau > W0)),          # drift term removed
            "miss_frac_W0": float(np.mean(dtau > W0)),
            "misses_c": int(np.sum(dtau > Wc)),           # corrected window
            "tightness": float(dtau.max() / W),
            "tightness_c": float(dtau.max() / Wc),
            "W": float(W), "Wc": float(Wc),
            "cost_mean": float(cost.mean()),
            "cost_max": int(cost.max()),
            "cost_mean_c": float(cost_c.mean()),
            "cost_max_c": int(cost_c.max()),
            "cost_over_enc": float(cost.mean() / max(2 * len(pairs) / n, 1e-12)),
            "cost_over_enc_c": float(cost_c.mean() / max(2 * len(pairs) / n, 1e-12)),
            "cand_pairs": int(cost.sum() / 2),
            "required_k": int(steps.max()),               # fixed-k needed for zero miss
            "pred_k": float(lam + np.sqrt(2 * lam * np.log(n))),  # Poisson-max sizing
            "gold_drop_frac": float(np.mean(stepsM > 4)), # gold's rank-4 drops
            "max_rank_M": int(stepsM.max()),
            "n_spacings_mean": float(lam),
        }
    return {"n_pairs": 0, "enc_per_body": 0.0}

def famA(e0, seed, n=3000, R=3e-3, da=1e-6, T=2.0, K=240):
    return dict(fam="A", n=n, e0=e0, da=da, de=1e-6, dw=1e-6, R=R, T=T, K=K, seed=seed)

def famB(e0, seed, n=3000, R=1.5e-4, da=1e-4, T=10.0, K=2000):
    return dict(fam="B", n=n, e0=e0, da=da, de=1e-4, dw=1e-4, R=R, T=T, K=K, seed=seed)

def run_one(cfg):
    t0 = time.time()
    a, e, w, M0 = make_fleet(cfg["n"], cfg["e0"], cfg["da"], cfg["de"], cfg["dw"], cfg["seed"])
    nn = np.sqrt(MU / a**3)
    pairs = truth_pairs(a, e, w, M0, nn, cfg["R"], cfg["T"], cfg["K"])
    res = cert_metrics(a, e, M0, pairs, cfg["R"], cfg["T"], cfg["da"], cfg["de"], cfg["dw"], cfg["e0"])
    res["cfg"] = cfg; res["wall_s"] = round(time.time() - t0, 1)
    return res

def build_runs(mode):
    runs = []
    if mode == "pilot":
        return [famA(0.9, 11)]
    if mode == "bonly":
        for e0 in [0.0, 0.6, 0.9, 0.99]:
            for seed in [21, 22, 23]:
                runs.append(famB(e0, seed))
        runs.append(famB(0.9, 21, n=30000))
        return runs
    for e0 in [0.0, 0.6, 0.9, 0.99]:
        for n in [3000, 30000]:
            for seed in [11, 12, 13]:
                runs.append(famA(e0, seed, n=n))
    for e0 in [0.0, 0.6, 0.9, 0.99]:
        for seed in [21, 22, 23]:
            runs.append(famB(e0, seed))
    runs.append(famB(0.9, 21, n=30000))            # B at 10x density
    runs.append(famA(0.99, 11, K=480))             # K-control (fastest transits)
    return runs

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "cert_out.json"
    mode = sys.argv[2] if len(sys.argv) > 2 else "full"
    runs = build_runs(mode)
    out = []
    for cfg in runs:
        res = run_one(cfg)
        out.append(res)
        print({k: res.get(k) for k in ["n_pairs", "enc_per_body", "misses", "misses_c",
                                       "cost_mean_c", "cost_max_c", "required_k", "wall_s"]},
              cfg["fam"], "e=", cfg["e0"], "n=", cfg["n"], "seed=", cfg["seed"], flush=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    print("done", len(out), "runs")
