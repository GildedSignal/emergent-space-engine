#!/usr/bin/env python3
"""Price the source of the calendar's standing post-mixing worst-window load excess
(calendar od 4). Data: the genesis census (45c0's instrument + this run's full dump).
Counterfactual arms evolve the extracted state with constant steps (validated by A0)
and recompute the example's own 64-window load statistic.

usage: analyze.py <run_dir> <census.tsv> <log> [--anchor-first 25 --horizon 5 --draws 4]
"""
import json
import re
import sys

import numpy as np

run_dir, census_path, log_path = sys.argv[1], sys.argv[2], sys.argv[3]
anchor_first = int(sys.argv[4]) if len(sys.argv) > 4 else 25
horizon = int(sys.argv[5]) if len(sys.argv) > 5 else 5
draws = int(sys.argv[6]) if len(sys.argv) > 6 else 4
MASTER = 20261021

# ---- the log: t_g, measured load stats, step_med -------------------------------------------------
gens, tgs, meas_max, meas_p99, meas_c50 = {}, {}, {}, {}, {}
step_med = None
for line in open(log_path):
    m = re.search(r"step_med=([\d.e+]+)", line)
    if m and step_med is None:
        step_med = float(m.group(1))
    m = re.match(r"gen g=(\d+) t=(-?\d+) .*C50=([\d.]+).*load_max=([\d.]+) load_p99=([\d.]+)", line)
    if m:
        g = int(m.group(1))
        gens[g] = True
        tgs[g] = int(m.group(2))
        meas_c50[g] = float(m.group(3))
        meas_max[g] = float(m.group(4))
        meas_p99[g] = float(m.group(5))
assert step_med, "no step_med in log"
gmax = max(gens)

# ---- the census ------------------------------------------------------------------------------------------------
rows = np.loadtxt(census_path, skiprows=0)
if rows.ndim == 1:
    rows = rows[None, :]
# columns: g id due step a
ids = np.unique(rows[:, 1]).astype(int)
idx = {v: i for i, v in enumerate(ids)}
N = len(ids)
per_gen = {}
for g in sorted(np.unique(rows[:, 0]).astype(int)):
    sel = rows[rows[:, 0] == g]
    per_gen[g] = np.column_stack([sel[:, 2], sel[:, 3], sel[:, 4]])  # due, step, a (in id order? enforce)
    order = np.argsort(sel[:, 1])
    per_gen[g] = per_gen[g][order]

# ---- the example's own load statistic ------------------------------------------------------------------------------
W = int(step_med / 64.0)


def loads(dues, g):
    lo, hi = tgs[g], tgs[g] + int(step_med)
    nwin = max(int((hi - lo) / W), 1)
    k = ((dues - lo) // W).astype(np.int64)
    counts = np.bincount(k[(k >= 0) & (k < nwin)], minlength=nwin)[:nwin].astype(float)
    mu = len(dues) / nwin
    c = np.sort(counts)
    return counts, mu, c[-1] / mu, c[min(int(round(0.99 * (len(c) - 1))), len(c) - 1)] / mu


# Poisson floor (uniform placement, M draws)
rng = np.random.default_rng(7)
floor_max, floor_p99 = [], []
for _ in range(4000):
    c = np.bincount(rng.integers(0, 64, N), minlength=64).astype(float)
    c.sort()
    floor_max.append(c[-1] * 64 / N)
    floor_p99.append(c[62] * 64 / N)
floor = {
    "max_med": float(np.median(floor_max)), "max_p10": float(np.percentile(floor_max, 10)),
    "max_p90": float(np.percentile(floor_max, 90)),
    "p99_med": float(np.median(floor_p99)),
}

# ---- calibration A0: model vs measured ----------------------------------------------------------------------------
calib1 = []  # one-fire-ahead
for g in sorted(gens):
    if g + 1 not in gens:
        continue
    d0, s0 = per_gen[g][:, 0], per_gen[g][:, 1]
    d1m = per_gen[g + 1][:, 0]
    k = (tgs[g + 1] - d0) // s0 + 1  # smallest k with d0 + k*s > t_{g+1}
    pred = d0 + k * s0
    err = np.abs(pred - d1m) / step_med
    _, _, pm, pp = loads(pred, g + 1)
    calib1.append({"g": g, "err_p50": float(np.median(err)), "err_p90": float(np.percentile(err, 90)),
                   "pred_max": pm, "meas_max": meas_max[g + 1], "pred_p99": pp, "meas_p99": meas_p99[g + 1]})
late1 = [c for c in calib1 if c["g"] >= 16]
calib_late = {
    "err_p50": float(np.median([c["err_p50"] for c in late1])), "err_p90": float(np.median([c["err_p90"] for c in late1])),
    "pred_max": float(np.median([c["pred_max"] for c in late1])), "meas_max": float(np.median([c["meas_max"] for c in late1])),
    "pred_p99": float(np.median([c["pred_p99"] for c in late1])), "meas_p99": float(np.median([c["meas_p99"] for c in late1])),
}

# ---- counterfactual arms --------------------------------------------------------------------------------------------
anchors = [g for g in range(anchor_first, gmax - 1) if g in gens and (g + 1) in gens]


def evolve(due, step, g_from, g_to):
    k = (tgs[g_to] - due) // step + 1
    return due + k * step


def arm_stats(transform, name):
    out = {"max": [], "p99": [], "per_anchor": []}
    for a in anchors:
        due, step, aau = per_gen[a][:, 0].copy(), per_gen[a][:, 1].copy(), per_gen[a][:, 2].copy()
        for r in range(draws):
            d2, s2 = transform(due, step, aau, MASTER + 1000 * a + r)
            for g in range(a + 1, min(a + 1 + horizon, gmax + 1)):
                if g not in gens:
                    continue
                _, _, pm, pp = loads(evolve(d2, s2, a, g), g)
                out["max"].append(pm)
                out["p99"].append(pp)
        out["per_anchor"].append(float(np.median(out["max"][len(out["max"]) // len(anchors):])) if out["max"] else 0)
    out["max_med"] = float(np.median(out["max"])) if out["max"] else None
    out["p99_med"] = float(np.median(out["p99"])) if out["p99"] else None
    out.pop("per_anchor", None)
    return out


arms = {
    "A6_marginal_resample": arm_stats(lambda d, s, a, seed: (np.random.default_rng(seed).choice(d, len(d), replace=True), s), "A6"),
    "A0_identity": arm_stats(lambda d, s, a, seed: (d, s), "A0"),
    "A1_step_shuffle": arm_stats(lambda d, s, a, seed: (d, np.random.default_rng(seed).permutation(s)), "A1"),
    "A5_phase_shuffle": arm_stats(lambda d, s, a, seed: (np.random.default_rng(seed).permutation(d), s), "A5"),
    "A2_jit1e-5": arm_stats(lambda d, s, a, seed: (d, np.round(s * (1 + np.random.default_rng(seed).uniform(-1e-5, 1e-5, len(s)))).astype(np.int64)), "A2"),
    "A3_jit1e-3": arm_stats(lambda d, s, a, seed: (d, np.round(s * (1 + np.random.default_rng(seed).uniform(-1e-3, 1e-3, len(s)))).astype(np.int64)), "A3"),
    "A4_phase_uniform": arm_stats(lambda d, s, a, seed: (tgs[0] + np.random.default_rng(seed).integers(0, int(step_med) * 16, len(s)).astype(np.int64), s), "A4"),
}

# ---- diagnostics ------------------------------------------------------------------------------------------------------
# D1: consecutive-gen window-count correlation, measured late gens
d1 = []
for g in sorted(gens):
    if g + 1 in gens and g >= 16:
        c1, _, _, _ = loads(per_gen[g][:, 0], g)
        c2, _, _, _ = loads(per_gen[g + 1][:, 0], g + 1)
        if c1.std() > 0 and c2.std() > 0:
            d1.append(float(np.corrcoef(c1, c2)[0, 1]))

# D2: persistent co-firing pairs (same window at g and g+1, late gens): |da| and |ds| vs random pairs
cf_da, cf_ds, rnd_da, rnd_ds = [], [], [], []
for g in sorted(gens):
    if g + 1 not in gens or g < 16:
        continue
    w1 = ((per_gen[g][:, 0] - tgs[g]) // W).astype(np.int64)
    w2 = ((per_gen[g + 1][:, 0] - tgs[g + 1]) // W).astype(np.int64)
    ok1 = (w1 >= 0) & (w1 < 64)
    srt = np.argsort(w1, kind="stable")
    ws = w1[srt]
    for win in np.unique(ws[(ws >= 0) & (ws < 64)]):
        i = np.searchsorted(ws, win, "left")
        j = np.searchsorted(ws, win, "right")
        mem = srt[i:j]
        mem = mem[ok1[mem]]
        if len(mem) < 2:
            continue
        for x in range(len(mem)):
            for y in range(x + 1, len(mem)):
                u, v = mem[x], mem[y]
                if w2[u] == w2[v]:  # still co-firing one gen later -> persistent pair
                    cf_da.append(abs(per_gen[g][u, 2] - per_gen[g][v, 2]))
                    cf_ds.append(abs(per_gen[g][u, 1] - per_gen[g][v, 1]) / step_med)
        if len(cf_da) > 400000:
            break
rg = np.random.default_rng(11)
for _ in range(len(cf_da) * 3 + 100):
    u, v = rg.integers(0, N, 2)
    if u != v:
        rnd_da.append(abs(per_gen[16][u, 2] - per_gen[16][v, 2]))
        rnd_ds.append(abs(per_gen[16][u, 1] - per_gen[16][v, 1]) / step_med)

diag = {
    "D1_count_autocorr_med": float(np.median(d1)) if d1 else None,
    "D2_persistent_pairs": len(cf_da),
    "D2_cf_da_med": float(np.median(cf_da)) if cf_da else None,
    "D2_rnd_da_med": float(np.median(rnd_da)) if rnd_da else None,
    "D2_cf_ds_med": float(np.median(cf_ds)) if cf_ds else None,
    "D2_rnd_ds_med": float(np.median(rnd_ds)) if rnd_ds else None,
    "D2_cf_ds_frac_lt_1e-4": float(np.mean(np.array(cf_ds) < 1e-4)) if cf_ds else None,
    "D2_cf_ds_frac_lt_1e-3": float(np.mean(np.array(cf_ds) < 1e-3)) if cf_ds else None,
    "D2_rnd_ds_frac_lt_1e-3": float(np.mean(np.array(rnd_ds) < 1e-3)) if rnd_ds else None,
}

# D3: exact step collisions in the whole belt
s_uniq, s_cnt = np.unique(per_gen[gmax][:, 1], return_counts=True)

# D4: the step distribution's clump census (threshold 1e-3 relative): gaps in sorted steps
ssort = np.sort(per_gen[gmax][:, 1])
gaps = np.diff(ssort) / step_med
clump_id = np.concatenate([[0], np.cumsum(gaps > 1e-3)])
sizes = np.bincount(clump_id)
big = sizes[sizes >= 2]
diag["D4_clumps_ge2"] = int(len(big))
diag["D4_max_clump"] = int(sizes.max())
diag["D4_frac_in_clumps_ge2"] = float(big.sum() / N)
internal = []
for c in np.unique(clump_id[sizes[clump_id] >= 8] if True else []):
    m = ssort[clump_id == c]
    internal.append((m[-1] - m[0]) / step_med)
diag["D4_bigclump_internal_spread_med"] = float(np.median(internal)) if internal else None

# D5: the measured trend, g = 16..gmax
d5 = {str(g): {"max": meas_max[g], "p99": meas_p99[g], "c50": meas_c50[g]} for g in sorted(gens) if g >= 16}
diag["D5_trend"] = d5
diag["D3_exact_step_collisions"] = int((s_cnt > 1).sum())
diag["D3_max_multiplicity"] = int(s_cnt.max())

meas_late = {
    "max_med": float(np.median([meas_max[g] for g in gens if g >= anchor_first])),
    "p99_med": float(np.median([meas_p99[g] for g in gens if g >= anchor_first])),
    "gens": sorted(int(g) for g in gens if g >= anchor_first),
    "N": int(N), "mu": N / 64.0, "step_med": step_med,
}

res = {"floor": floor, "measured_late": meas_late, "calib_1fire_late": calib_late, "calib_1fire": calib1,
       "arms": arms, "diagnostics": diag, "anchor_first": anchor_first, "horizon": horizon, "draws": draws}
outp = f"{run_dir}/excess_source.json"
json.dump(res, open(outp, "w"), indent=1)

fm = floor["max_med"]
ex = lambda v: None if v is None else round(v - fm, 3)
print(f"D4 clumps>=2 {diag['D4_clumps_ge2']} max {diag['D4_max_clump']} frac_in {diag['D4_frac_in_clumps_ge2']:.3f} "
      f"internal_spread {diag.get('D4_bigclump_internal_spread_med')}")
gs = sorted(int(g) for g in gens if g >= 16)
print("D5 max/mu by g:", " ".join(f"{g}:{meas_max[g]:.2f}" for g in gs[::4]))
print(f"N={N} mu={N/64:.1f} gens<={gmax} anchors>={anchor_first} horizon={horizon}")
print(f"floor max/mu med {fm:.3f} [p10 {floor['max_p10']:.3f}, p90 {floor['max_p90']:.3f}]  measured late med {meas_late['max_med']:.3f}  p99 {meas_late['p99_med']:.3f} (floor {floor['p99_med']:.3f})")
print(f"calib 1-fire late: err_p50 {calib_late['err_p50']:.2e} err_p90 {calib_late['err_p90']:.2e} pred_max {calib_late['pred_max']:.3f} vs meas {calib_late['meas_max']:.3f}")
for k, v in arms.items():
    print(f"{k:18s} max/μ {v['max_med']:.3f} (excess {ex(v['max_med'])})  p99/μ {v['p99_med']:.3f}")
print(f"D1 autocorr {diag['D1_count_autocorr_med']:.3f}  D2 persistent pairs {diag['D2_persistent_pairs']}  "
      f"cf|da| {diag['D2_cf_da_med']:.4f} vs rnd {diag['D2_rnd_da_med']:.4f}  cf|ds|/s {diag['D2_cf_ds_med']:.2e} vs rnd {diag['D2_rnd_ds_med']:.2e}  "
      f"cf ds<1e-3 {diag['D2_cf_ds_frac_lt_1e-3']:.3f} (rnd {diag['D2_rnd_ds_frac_lt_1e-3']:.4f})  exact collisions {diag['D3_exact_step_collisions']} max mult {diag['D3_max_multiplicity']}")
print("wrote", outp)
