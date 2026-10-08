#!/usr/bin/env python3
"""B12 statistic lab (20261008-1719-dynamics-c13b).

Reads the CSVs dumped by xtask's b12_series_dump: per law and ship, t, X (signed
relative Jacobi error of the law's own series), heliocentric (E, L) and the state.

Computes:
  - the incumbent statistic: fit.growth_exponent ported exactly, median among
    ships above the 1e-12 floor, and worst |X|;
  - S1 trend blade: per ship, OLS slope of X on t, z against circular shifts of
    the mean-removed increments (a null that keeps the series' own diffusion and
    autocorrelation and destroys only the net drift);
  - S2 memory blade: same-cell pairs on (E, L) deciles (gap >= 1 period),
    Spearman rho(|dX|, dt) with a permutation null stratified on matched-state
    distance (kills the Lipschitz-through-coarse-cells confound);
  - floor calibration: bounded + leak ladders against the derived l_min.

A law FAILS if S1 flags it (>=14/16 same-signed at p<0.05, false alarm ~0.4%)
or S2 flags it (>=12/16 ships at p<0.05).
"""
import json, math, sys
from pathlib import Path
import numpy as np

WORK = Path(__file__).parent
FLOOR, ERR_MAX, GROWTH_MAX, N_PER = 1e-12, 1e-4, 0.2, 200.0
LAWS = ["echo", "scaled3e-13", "scaled1e-11", "bounded", "compound", "drift",
        "leak1e-12", "leak1e-13", "leak3e-14"]
CLEAN = {"echo", "scaled3e-13", "scaled1e-11", "bounded"}

def growth_exponent(err):
    n = len(err)
    first = max(n // 10, 1)
    if n <= first or not np.isfinite(err).all():
        return float("nan")
    def edge(j):
        return n if j == 16 else round(first * (n / first) ** (j / 16))
    used, pts = 0, []
    for j in range(16):
        a, b = edge(j), edge(j + 1)
        if b <= a:
            continue
        used += 1
        top = np.abs(err[a:b]).max()
        if top > 0.0:
            pts.append((math.log(math.sqrt(a * (b - 1))), math.log(top)))
    if used < 8:
        return float("nan")
    if not pts:
        return 0.0
    if len(pts) < 3:
        return float("nan")
    xs, ys = np.array(pts).T
    return float(np.polyfit(xs, ys, 1)[0])

def slope_z(t, X):
    """OLS slope of X on t and its z against circular shifts of mean-removed increments."""
    tc = t - t.mean()
    denom = (tc * tc).sum()
    b_obs = (tc * X).sum() / denom
    d = np.diff(X)
    d0 = d - d.mean()
    n = len(d0)
    idx = np.arange(n)
    null = np.empty(min(n, 1600))
    shifts = np.unique(np.linspace(0, n - 1, len(null)).astype(int))
    null = np.empty(len(shifts))
    for i, k in enumerate(shifts):
        Xs = X[0] + np.concatenate([[0.0], np.cumsum(np.roll(d0, k))])
        null[i] = (tc * Xs).sum() / denom
    sd = null.std()
    z = (b_obs - null.mean()) / sd if sd > 0 else 0.0
    p = (1 + np.sum(np.abs(null - null.mean()) >= abs(b_obs - null.mean()))) / (len(null) + 1)
    return b_obs, z, p, null.std()

def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)).astype(float), np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    den = math.sqrt((ra * ra).sum() * (rb * rb).sum())
    return float((ra * rb).sum() / den) if den > 0 else 0.0

def memory_p(E, L, X, t, rng, nperm=300):
    """Same-cell (E,L)-decile pairs (gap >= 1 period): rho(|dX|, dt), stratified permutation."""
    n = len(X)
    def deciles(v):
        w = (v.max() - v.min()) / 10
        return np.clip(((v - v.min()) / w).astype(int), 0, 9)
    cell = deciles(E) * 10 + deciles(L)
    dE, dL = (E.max() - E.min()), (L.max() - L.min())
    i, j = np.triu_indices(n, k=1)
    same = cell[i] == cell[j]
    gap = t[j] - t[i]
    i, j, gap = i[same & (gap > 0)], j[same & (gap > 0)], gap[same & (gap > 0)]
    if len(i) < 30:
        return float("nan"), float("nan"), len(i), float("nan")
    dX, dt = np.abs(X[j] - X[i]), gap
    dstate = np.sqrt(((E[j] - E[i]) / max(dE, 1e-300)) ** 2 + ((L[j] - L[i]) / max(dL, 1e-300)) ** 2)
    rho = spearman(dX, dt)
    edges = np.quantile(dstate, np.linspace(0, 1, 11))
    edges[0] -= 1e-12; edges[-1] += 1e-12
    bins = np.clip(np.digitize(dstate, edges) - 1, 0, 9)
    count = 0
    for _ in range(nperm):
        perm = dt.copy()
        for b in np.unique(bins):
            m = bins == b
            perm[m] = rng.permutation(perm[m])
        count += spearman(dX, perm) >= rho
    p = (1 + count) / (nperm + 1)
    return rho, p, len(i), float(np.median(dX))

def median(xs):
    xs = [np.inf if (isinstance(x, float) and math.isnan(x)) else x for x in xs]
    return float(np.median(xs))

def main():
    rng = np.random.default_rng(20261008)
    scene = json.loads((WORK / "scene.json").read_text())
    ships = [int(s) for s in map(str, scene["ships"])]
    out = {}
    print(f"{'law':14} {'med.exp(rising)':>15} {'worst|X|':>9} {'S1:flag/sign':>12} "
          f"{'S1 med z':>8} {'S2:flag':>6} {'S2 med rho':>9} {'pairs':>6}  verdict")
    for law in LAWS:
        per = []
        for s in ships:
            a = np.genfromtxt(WORK / f"{law}-{s:02}.csv", delimiter=",", names=True)
            t, X, E, Lh = a["t"], a["X"], a["E"], a["L"]
            b, z, p1, sd_null = slope_z(t, X)
            rho, p2, pairs, med_dx = memory_p(E, Lh, X, t, rng)
            per.append(dict(ship=s, exp=growth_exponent(np.abs(X)), worst=float(np.abs(X).max()),
                            z=z, p1=p1, rho=rho, p2=p2, pairs=pairs, med_dx=med_dx, sd_null=sd_null,
                            slope=b))
        rising = [q["exp"] for q in per if q["worst"] > FLOOR]
        z = np.array([q["z"] for q in per]); p1 = np.array([q["p1"] for q in per])
        flagged = (p1 < 0.05) & (np.abs(z) > 2)
        signs = int(max((z[flagged] > 0).sum(), (z[flagged] < 0).sum())) if flagged.any() else 0
        p2 = np.array([q["p2"] for q in per]); rho = np.array([q["rho"] for q in per])
        s2flag = int(np.sum((p2 < 0.05) & (rho > 0)))
        s1flag = signs if flagged.sum() >= 14 else 0
        fail = s1flag >= 14 or s2flag >= 12
        verdict = ("FAIL" if fail else "pass") + ("" if law in CLEAN or fail else "  (control: must FAIL!)")
        warn = "" if (fail or law in CLEAN) else "  <-- CONTROL NOT FLAGGED"
        print(f"{law:14} {median(rising) if rising else 0.0:15.3f} {max(q['worst'] for q in per):9.2e} "
              f"{int(flagged.sum()):2d}/{signs:2d}      {median(list(z)):8.2f} {s2flag:6d} {median(list(rho)):9.3f} "
              f"{int(median([q['pairs'] for q in per])):6d}  {verdict}{warn}")
        out[law] = dict(per_ship=per, median_exp=median(rising) if rising else 0.0,
                        s1_flagged=int(flagged.sum()), s1_signs=signs, s1_flag=s1flag,
                        s2_flag=s2flag, fail=bool(fail))

    # Floor calibration: bounded series + clean linear leaks; derived l_min = 2.5 * sd_null * P.
    print("\nfloor calibration on bounded+leak mixtures (S1, |z|>2.5):")
    P = scene["period"]
    ladder = [1e-11, 3e-12, 1e-12, 3e-13, 1e-13, 3e-14, 1e-15]
    base = {q["ship"]: q for q in out["bounded"]["per_ship"]}
    rows = []
    for ell in ladder:
        det, pred = [], []
        for s in ships:
            a = np.genfromtxt(WORK / f"bounded-{s:02}.csv", delimiter=",", names=True)
            t, X = a["t"], a["X"] + ell * t / P
            b, z, p1, sd = slope_z(t, X)
            det.append(abs(z) > 2.5)
            pred.append(ell * P if False else 2.5 * base[s]["sd_null"] * P)
        det_rate = np.mean(det)
        ratio = ell / float(np.median(pred))
        rows.append((ell, det_rate, ratio))
        print(f"  leak {ell:8.0e}/P  detected {det_rate*100:5.1f}%   ell/l_min(median) = {ratio:8.2f}")
    out["calibration"] = rows
    (WORK / "analysis.json").write_text(json.dumps(out, indent=1, default=float))
    print("\nwrote analysis.json")

if __name__ == "__main__":
    main()
