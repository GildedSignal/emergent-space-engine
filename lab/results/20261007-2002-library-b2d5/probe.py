#!/usr/bin/env python3
"""Calendar-rate probe v2: does encounter work track events, not N?

Candidate pair = orbit-crossing (q_i <= Q_j and q_j <= Q_i), counted EXACTLY by
endpoint sorting (no pair enumeration): partners of i, m_i = c_i - 1 - d_i.
Event = one conjunction (calendar pop/push), rate |dn|/(mean n) per orbit.
Conjunctions are an upper bound on real encounters (the miss filter is a
distribution-constant factor, independent of N at fixed sigma_e).

Disclosed change from v1 (pre-registered setup kept as setup A): v1 counted
pairs by local windows and OOM'd at 1e6 - windows grow with a at fixed
AU-density. That failure is itself the first result: the crossing band is
a*e, so linear AU-density is the wrong unit. Setup A measures it; setup A'
uses constant per-band (log a) density; setup B holds extent fixed instead.
"""
import json
import numpy as np

RHO = 5_000.0  # bodies per AU, setup A


def belt(n, sig_e, mode, seed):
    r = np.random.default_rng(seed)
    if mode == "lin":      # A: fixed density per AU, extent grows
        a = 1.0 + r.random(n) * (n / RHO)
    elif mode == "log":    # A': fixed density per crossing band (log a)
        a = np.exp(r.random(n) * np.log(1.0 + n / RHO))
    else:                  # B: fixed extent [1,2], density grows with n
        a = 1.0 + r.random(n)
    e = r.rayleigh(sig_e, size=n)
    return a, e


def partners_per_body(a, e):
    q, Q = a * (1 - e), a * (1 + e)
    qs, Qs = np.sort(q), np.sort(Q)
    c = np.searchsorted(qs, Q, "right") - 1     # j != i with q_j <= Q_i
    d = np.searchsorted(Qs, q, "left")          # j with Q_j < q_i (no overlap)
    return c - d


def rate_subsample(a, e, nsamp, seed):
    """Conjunctions per orbit per sampled body, exact per body (calendar load)."""
    r = np.random.default_rng(seed)
    idx = r.choice(len(a), size=nsamp, replace=False)
    n_m = a ** -1.5
    order = np.argsort(a)
    a_s, e_s, n_s = a[order], e[order], n_m[order]
    q_s, Q_s = a_s * (1 - e_s), a_s * (1 + e_s)
    ecap = min(3 * e.max(), 0.6)
    half = 2 * ecap * a / (1 - ecap)
    rates = np.empty(nsamp)
    for k, i in enumerate(idx):
        qi, Qi = a[i] * (1 - e[i]), a[i] * (1 + e[i])
        lo = np.searchsorted(a_s, a[i] - half[i], "left")
        hi = np.searchsorted(a_s, a[i] + half[i], "right")
        w = np.arange(lo, hi)
        keep = w[(Q_s[w] >= qi) & (q_s[w] <= Qi)]
        keep = keep[a_s[keep] != a[i]]           # drop self
        rbar = 0.5 * (n_s[keep] + n_m[i])
        rates[k] = (np.abs(n_s[keep] - n_m[i]) / rbar).sum()
    return rates


def slope(x, y):
    lx, ly = np.log(np.asarray(x, float)), np.log(np.asarray(y, float))
    return float(np.polyfit(lx, ly, 1)[0])


def main():
    out = {"cases": [], "controls": {}}

    # instrument control: endpoint count == brute force, n=2000
    a, e = belt(2000, 0.05, "lin", 11)
    m = partners_per_body(a, e)
    q, Q = a * (1 - e), a * (1 + e)
    ii, jj = np.triu_indices(len(a), 1)
    brute = int(((Q[jj] >= q[ii]) & (Q[ii] >= q[jj])).sum())
    out["controls"]["endpoint_vs_brute_2000"] = [int(m.sum() // 2), brute]

    # Setup A (pre-registered): fixed AU density, n=1e5 -> pairs/body vs a
    a, e = belt(100_000, 0.05, "lin", 101)
    m = partners_per_body(a, e)
    ok = a > 1.05
    out["controls"]["setupA_slope_pairsbody_vs_a"] = slope(a[ok], m[ok])

    # Setup A': constant per-band density; P1 across N
    rowsA = []
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        a, e = belt(n, 0.05, "log", 202)
        m = partners_per_body(a, e)
        rowsA.append({"n": n, "pairs_per_body": float(m.mean()),
                      "all_pairs_control": n * (n - 1) / 2})
    out["cases"].append({"setup": "A'_perband_fixed", "rows": rowsA,
                         "slope_pairsbody_vs_N": slope([r["n"] for r in rowsA],
                                                       [r["pairs_per_body"] for r in rowsA])})

    # P2: conjunction rate per body per orbit, A' setup, subsample
    for n in [1_000, 100_000, 1_000_000]:
        a, e = belt(n, 0.05, "log", 303)
        m = partners_per_body(a, e)
        rates = rate_subsample(a, e, min(500, n), 7)
        out["cases"].append({"setup": "A'_rate", "n": n,
                             "events_per_body_per_orbit": float(rates.mean()),
                             "rate_dispersion": float(rates.var() / rates.mean()),
                             "pairs_per_body": float(m.mean())})

    # Setup B: fixed extent, density grows -> the board's O(N^2) premise
    rowsB = []
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        a, e = belt(n, 0.05, "fix", 404)
        m = partners_per_body(a, e)
        rowsB.append({"n": n, "pairs_per_body": float(m.mean()),
                      "all_pairs_control": n * (n - 1) / 2})
    out["cases"].append({"setup": "B_fixed_extent", "rows": rowsB,
                         "slope_pairsbody_vs_N": slope([r["n"] for r in rowsB],
                                                       [r["pairs_per_body"] for r in rowsB])})

    # P3 (held out): sigma_e sweep, A' n=1e5 -> pairs/body vs sigma_e
    se_rows = []
    for se in [0.05, 0.10, 0.20]:
        a, e = belt(100_000, se, "log", 505)
        m = partners_per_body(a, e)
        se_rows.append({"sig_e": se, "pairs_per_body": float(m.mean())})
    out["cases"].append({"setup": "P3_sigma_sweep", "rows": se_rows,
                         "slope_pairsbody_vs_sigmae": slope([r["sig_e"] for r in se_rows],
                                                            [r["pairs_per_body"] for r in se_rows])})

    # P4 (held out): burstiness. 90% belt + 10% fleet on one orbit, fixed extent.
    n = 100_000
    r = np.random.default_rng(5)
    a = np.concatenate([1.0 + r.random(int(0.9 * n)), 1.5 + r.normal(0, 1e-4, int(0.1 * n))])
    e = np.concatenate([r.rayleigh(0.05, int(0.9 * n)), np.full(int(0.1 * n), 0.001)])
    rates = rate_subsample(a, e, 500, 9)
    out["controls"]["P4_mixed_dispersion"] = float(rates.var() / rates.mean())
    out["controls"]["P4_mixed_mean_events"] = float(rates.mean())
    a2, e2 = belt(n, 0.05, "fix", 5)
    rates2 = rate_subsample(a2, e2, 500, 9)
    out["controls"]["P4_pure_belt_dispersion"] = float(rates2.var() / rates2.mean())

    import pathlib
    with open(pathlib.Path(__file__).parent / "probe-out.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
