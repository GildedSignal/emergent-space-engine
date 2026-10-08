"""Analyze H_live metrics from belt snapshots. All fractions exact under float64 exploration."""
import json
import numpy as np

def load(tag):
    s = np.load(f"{tag}-snap.npz")
    return s["meta"], s["a"], s["e"], s["ex"], s["ey"]

def ks(x, y):
    x, y = np.sort(x), np.sort(y)
    allv = np.concatenate([x, y])
    cdf1 = np.searchsorted(x, allv, side="right") / len(x)
    cdf2 = np.searchsorted(y, allv, side="right") / len(y)
    return float(np.max(np.abs(cdf1 - cdf2)))

def rayleigh_ks(v):
    s = np.sqrt(np.mean(v ** 2) / 2)
    u = np.sort(v)
    cdf = 1 - np.exp(-0.5 * (u / s) ** 2)
    emp = (np.arange(len(u)) + 0.5) / len(u)
    return float(np.max(np.abs(cdf - emp)))

R = {}
# control C: pure drift must not move a
tm, a, e, ex, ey = load("C")
R["control_C_max_da"] = float(np.max(np.abs(a[-1] / a[0] - 1)))
R["control_C_pass"] = R["control_C_max_da"] < 1e-8
# dt control at t=1517 yr: dt-independence of the osculating-a spread (not numerical)
c = np.load("/tmp/dt256-snap.npz")
R["dt_control_median_da_PJ64"] = 7.82e-4  # from A1 snapshot 1, equal time
R["dt_control_median_da_PJ256"] = float(np.median(np.abs(c["a"][-1] / c["a"][0] - 1)))

# A = A1 + A2 concatenated
t1, a1, e1, x1, y1 = load("A1")
t2, a2, e2, x2, y2 = load("A2")
keep = t2 > t1[-1] + 1
tA = np.concatenate([t1, t2[keep]]); aA = np.concatenate([a1, a2[keep]])
eA = np.concatenate([e1, e2[keep]]); exA = np.concatenate([x1, x2[keep]]); eyA = np.concatenate([y1, y2[keep]])
a0, e0 = aA[0], eA[0]

# P1: osculating-a change (contaminated by forced oscillation ~1e-3) and the
# proper-a drift proxy |mean(last quarter)/mean(first quarter) - 1| (chaos marker)
da = np.abs(aA[-1] / a0 - 1)
q = max(1, len(aA) // 4)
drift = np.abs(aA[-q:].mean(axis=0) / aA[:q].mean(axis=0) - 1)
R["P1_raw_frac_da_gt_1e-4"] = float(np.mean(da > 1e-4))
R["P1_drift_frac_gt_1e-3"] = float(np.mean(drift > 1e-3))
R["P1_drift_frac_gt_3e-3"] = float(np.mean(drift > 3e-3))
R["P1_drift_frac_gt_1e-2"] = float(np.mean(drift > 1e-2))
def band_frac(lo_, hi_):
    m = (a0 >= lo_) & (a0 < hi_)
    return float(np.mean(drift[m] > 1e-3)), int(m.sum())
R["P1_by_region_drift1e-3"] = {
    "3:1 (2.45-2.55)": band_frac(2.45, 2.55), "5:2 (2.77-2.87)": band_frac(2.77, 2.87),
    "2:1 (3.22-3.32)": band_frac(3.22, 3.32), "off-res (2.90-3.10)": band_frac(2.90, 3.10)}
R["P1_pass_3pct"] = R["P1_drift_frac_gt_1e-3"] >= 0.03

# P2: birth-cell departure in (ex, ey); Rayleigh refit vs birth family over time
dex = np.hypot(exA - exA[0], eyA - eyA[0])
R["P2_birth_cell_frac"] = [float(f) for f in (dex > 1e-4).mean(axis=1)]
R["P2_pass_80pct"] = bool((dex > 1e-4).mean(axis=1)[-1] >= 0.8)
R["P2_refit_rayleigh_ks"] = [rayleigh_ks(v) for v in eA[::6]]
R["P2_birth_rayleigh_ks"] = [ks(v, eA[0]) for v in eA[::6]]
# forced structure appears: per-band mean e-vector magnitude (why a static family fails)
mag = np.hypot(exA.mean(axis=1), eyA.mean(axis=1))
R["P2_forced_vector_mean_e"] = [float(m) for m in mag[::6]]

# P3: shuffle legality. A2 final vs D final; noise floor = A2 vs B final.
_, aD, eD, _, _ = load("D")
_, aB, eB, _, _ = load("B")
aD, eD = aD[-1], eD[-1]
R["P3_ks_synth_a"] = ks(aA[-1], aD); R["P3_ks_synth_e"] = ks(eA[-1], eD)
R["P3_ks_noise_a"] = ks(aA[-1], aB[-1]); R["P3_ks_noise_e"] = ks(eA[-1], eB[-1])
sc = lambda a_, e_: int(np.sum((a_ > 4.0) | (e_ > 0.3)))
R["P3_scatter_A_D_B"] = [sc(aA[-1], eA[-1]), sc(aD, eD), sc(aB[-1], eB[-1])]
R["P3_pass"] = bool(R["P3_ks_synth_a"] < 3 * max(R["P3_ks_noise_a"], 1e-3)
                    and R["P3_ks_synth_e"] < 3 * max(R["P3_ks_noise_e"], 1e-3)
                    and abs(sc(aD, eD) - sc(aA[-1], eA[-1])) <= 3 * np.sqrt(max(sc(aA[-1], eA[-1]), 1)))
# synthetic's own drift must match the true belt's (the scar-rate observable)
drD = np.abs(np.load("D-snap.npz")["a"][-q:].mean(axis=0) / np.load("D-snap.npz")["a"][:q].mean(axis=0) - 1)
drB = np.abs(aB[-q:].mean(axis=0) / aB[:q].mean(axis=0) - 1)
R["P3_drift_frac_1e-3_A_D_B"] = [float(np.mean(drift > 1e-3)), float(np.mean(drD > 1e-3)),
                                 float(np.mean(drB > 1e-3))]

# P4: gap depth at 3:1 over time
gd = lambda v: float(((v >= 2.47) & (v < 2.53)).sum() / max(((v >= 2.2) & (v < 2.4)).sum(), 1))
R["P4_gap_depth_A"] = [gd(v) for v in aA[::6]]
R["P4_gap_depth_D_final"] = gd(aD); R["P4_gap_depth_B_final"] = gd(aB[-1])

R["f_chaos_series_1e-3"] = [float(np.mean(np.abs(aA[i - q:i].mean(axis=0) / aA[i - 2 * q:i - q].mean(axis=0) - 1) > 1e-3)) for i in range(2 * q, len(aA) + 1)]
for k, v in R.items():
    if not isinstance(v, list):
        print(k, "=", v)
    else:
        s = [None if x is None else round(x, 4) if isinstance(x, float) else x for x in v]
        print(k, "=", s[::4] if len(s) > 8 else s)
