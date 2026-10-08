#!/usr/bin/env python3
"""Fast pass: same statistics, pairs capped at 2500/ship, 150 perms. S2 thresholds
calibrated on the echo control (method.md #9: calibrate on a planted pair)."""
import json, math
from pathlib import Path
import numpy as np

WORK = Path(__file__).parent
FLOOR = 1e-12
LAWS = ["echo", "scaled3e-13", "scaled1e-11", "bounded", "compound", "drift",
        "leak1e-12", "leak1e-13", "leak3e-14"]
CLEAN = {"echo", "scaled3e-13", "scaled1e-11", "bounded"}
rng = np.random.default_rng(20261008)

def growth_exponent(err):
    n = len(err); first = max(n // 10, 1)
    if n <= first or not np.isfinite(err).all(): return float("nan")
    def edge(j): return n if j == 16 else round(first * (n / first) ** (j / 16))
    used, pts = 0, []
    for j in range(16):
        a, b = edge(j), edge(j + 1)
        if b <= a: continue
        used += 1
        top = np.abs(err[a:b]).max()
        if top > 0.0: pts.append((math.log(math.sqrt(a * (b - 1))), math.log(top)))
    if used < 8: return float("nan")
    if not pts: return 0.0
    if len(pts) < 3: return float("nan")
    xs, ys = np.array(pts).T
    return float(np.polyfit(xs, ys, 1)[0])

def slope_z(t, X):
    tc = t - t.mean(); denom = (tc * tc).sum()
    b_obs = (tc * X).sum() / denom
    d0 = np.diff(X); d0 = d0 - d0.mean(); n = len(d0)
    shifts = np.unique(np.linspace(0, n - 1, 800).astype(int))
    null = np.array([(tc * np.concatenate([[X[0]], np.cumsum(np.roll(d0, k))])).sum() / denom for k in shifts])
    sd = null.std()
    z = (b_obs - null.mean()) / sd if sd > 0 else 0.0
    p = (1 + np.sum(np.abs(null - null.mean()) >= abs(b_obs - null.mean()))) / (len(null) + 1)
    return b_obs, z, p, sd

def rankv(a):
    return np.argsort(np.argsort(a)).astype(float)

def rho_fast(a, b):
    ra, rb = rankv(a), rankv(b)
    ra -= ra.mean(); rb -= rb.mean()
    den = math.sqrt((ra * ra).sum() * (rb * rb).sum())
    return float((ra * rb).sum() / den) if den > 0 else 0.0

def memory_p(E, L, X, t, nperm=150, cap=2500):
    n = len(X)
    def deciles(v):
        w = (v.max() - v.min()) / 10
        return np.clip(((v - v.min()) / w).astype(int), 0, 9)
    cell = deciles(E) * 10 + deciles(L)
    i, j = np.triu_indices(n, k=1)
    same = cell[i] == cell[j]
    gap = t[j] - t[i]
    keep = same & (gap > 0)
    i, j, gap = i[keep], j[keep], gap[keep]
    if len(i) > cap:
        sel = rng.choice(len(i), cap, replace=False)
        i, j, gap = i[sel], j[sel], gap[sel]
    if len(i) < 30: return float("nan"), float("nan"), len(i), float("nan")
    dX, dt = np.abs(X[j] - X[i]), gap
    dE, dL = E.max() - E.min(), L.max() - L.min()
    dstate = np.sqrt(((E[j] - E[i]) / dE) ** 2 + ((L[j] - L[i]) / dL) ** 2)
    rho = rho_fast(dX, dt)
    edges = np.quantile(dstate, np.linspace(0, 1, 8)); edges[0] -= 1e-12; edges[-1] += 1e-12
    bins = np.clip(np.digitize(dstate, edges) - 1, 0, 6)
    rX = rankv(dX)
    count = 0
    for _ in range(nperm):
        perm = dt.copy()
        for b in np.unique(bins):
            m = bins == b
            perm[m] = rng.permutation(perm[m])
        count += rho_fast(dX, perm) >= rho
    return rho, (1 + count) / (nperm + 1), len(i), float(np.median(dX))

def med(xs): return float(np.median(xs))

scene = json.loads((WORK / "scene.json").read_text())
ships = [int(s) for s in scene["ships"]]
P = scene["period"]
out, table = {}, []
for law in LAWS:
    per = []
    for s in ships:
        a = np.genfromtxt(WORK / f"{law}-{s:02}.csv", delimiter=",", names=True)
        t, X, E, L = a["t"], a["X"], a["E"], a["L"]
        b, z, p1, sd = slope_z(t, X)
        rho, p2, pairs, mdx = memory_p(E, L, X, t)
        per.append(dict(ship=s, exp=growth_exponent(np.abs(X)), worst=float(np.abs(X).max()),
                        z=z, p1=p1, rho=rho, p2=p2, pairs=pairs, med_dx=mdx, sd_null=sd))
    rising = [q["exp"] for q in per if q["worst"] > FLOOR]
    z = np.array([q["z"] for q in per]); p1 = np.array([q["p1"] for q in per])
    fl = (p1 < 0.05) & (np.abs(z) > 2)
    signs = int(max((z[fl] > 0).sum(), (z[fl] < 0).sum())) if fl.any() else 0
    rho = np.array([q["rho"] for q in per]); p2 = np.array([q["p2"] for q in per])
    table.append((law, med(rising) if rising else 0.0, max(q["worst"] for q in per),
                  int(fl.sum()), signs, med(z), med(rho), int(np.sum((p2 < 0.05) & (rho > 0.1))),
                  int(med([q["pairs"] for q in per]))))
    out[law] = per
echo_rho = med([q["rho"] for q in out["echo"]])
print(f"echo confound (median rho): {echo_rho:.4f}")
print(f"{'law':14}{'med.exp':>9}{'worst|X|':>10}{'S1 fl':>6}{'sign':>5}{'med z':>8}{'med rho':>9}{'S2 fl':>6}{'pairs':>8}")
for r in table:
    print(f"{r[0]:14}{r[1]:9.3f}{r[2]:10.2e}{r[3]:6d}{r[4]:5d}{r[5]:8.2f}{r[6]:9.3f}{r[7]:6d}{r[8]:8d}")

print("\nfloor calibration (bounded + clean leak, S1 |z|>2.5):")
rows = []
for ell in [1e-11, 3e-12, 1e-12, 3e-13, 1e-13, 3e-14, 1e-15]:
    det, pred = [], []
    for q in out["bounded"]:
        a = np.genfromtxt(WORK / f"bounded-{q['ship']:02}.csv", delimiter=",", names=True)
        t, X = a["t"], a["X"] + ell * t / P
        _, z, _, _ = slope_z(t, X)
        det.append(abs(z) > 2.5)
        pred.append(2.5 * q["sd_null"] * P)
    print(f"  leak {ell:8.0e}/P  detected {np.mean(det)*100:5.1f}%   ell/l_min(med) = {ell/med(pred):8.2f}")
    rows.append([ell, float(np.mean(det)), float(ell / med(pred))])
out["calibration"] = rows
(WORK / "analysis.json").write_text(json.dumps(out, indent=1, default=float))
print("wrote analysis.json")
