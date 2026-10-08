#!/usr/bin/env python3
"""Atlas analysis: wall law vs mu, teeth, instrument check."""
import numpy as np, os
OUT = os.path.dirname(os.path.abspath(__file__))
z = np.load(os.path.join(OUT, "atlas.npz"))

print("=== chaotic-zone wall (innermost a with >=50% finite T_div in next 0.05) ===")
walls = {}
for mu in [1e-5, 1e-4, 3e-4, 1e-3]:
    td = z[f"mu_{mu:g}"]
    a = z[f"mu_{mu:g}_a"]
    bins = np.unique(a)
    fin = np.array([np.any(np.isfinite(td[a == b])) for b in bins])
    wall = np.nan
    for i, b in enumerate(bins):
        if b >= 0.97:
            break
        win = fin[i:i + 10]
        if len(win) == 10 and win.mean() >= 0.5:
            wall = b
            break
    walls[mu] = 1 - wall
    med = np.array([np.median(td[a == b]) if np.any(np.isfinite(td[a == b])) else np.inf
                    for b in bins])
    inner = (bins < 0.97) & fin
    idx = np.where(inner)[0]
    rat = [max(med[i] / med[i + 1], med[i + 1] / med[i]) for i in idx[:-1]
           if np.isfinite(med[i]) and np.isfinite(med[i + 1]) and med[i] > 0 and med[i + 1] > 0]
    print(f"mu={mu:.0e}: 1-a_wall={walls[mu]:.3f}  chaotic-bins={fin.mean():.0%}  "
          f"max neighbor T_div ratio={max(rat) if rat else float('nan'):.0f}x  "
          f"min median T_div={np.nanmin(np.where(np.isfinite(med), med, np.nan)):.0f} orbits")
mus = np.array([1e-5, 1e-4, 3e-4, 1e-3])
w = np.array([walls[m] for m in mus])
A = np.vstack([np.ones_like(mus), np.log(mus)]).T
coef = np.linalg.lstsq(A, np.log(w), rcond=None)[0]
resid = np.log(w) - A @ coef
print(f"fit: 1-a_wall = {np.exp(coef[0]):.3f} * mu^{coef[1]:.3f}  log-resids={np.round(resid,3)}")

print("\n=== instrument check: hdiv 64 vs 96 (mu=1e-4, T=2000, same seeds) ===")
t64, t96 = z["hchk_64"], z["hchk_96"]
both = np.isfinite(t64) & np.isfinite(t96)
print("n both finite=%d/%d  median|dlog10|=%.3f  classification agreement=%.0f%%" %
      (both.sum(), len(t64),
       np.median(np.abs(np.log10(t64[both]) - np.log10(t96[both]))),
       100 * (np.isfinite(t64) == np.isfinite(t96)).mean()))
