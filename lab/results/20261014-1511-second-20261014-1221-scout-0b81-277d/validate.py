#!/usr/bin/env python3
"""Control: the exact event search vs brute force (min-miss), 60 random pairs."""
import numpy as np
import gate2 as G

rs = np.random.default_rng(42)
n = 400
a = rs.uniform(0.95, 1.05, n); e = rs.rayleigh(0.05, n).clip(max=0.35)
w = rs.uniform(0, 2*np.pi, n); M0 = rs.uniform(0, 2*np.pi, n)
peri, apo = a*(1-e), a*(1+e)
ii = rs.integers(0, n, 3000); jj = rs.integers(0, n, 3000)
ok = (ii != jj) & (peri[ii] < apo[jj]) & (peri[jj] < apo[ii])
i, j = ii[ok][:60], jj[ok][:60]
wmin, dmin, vmin, K = G.exact_gate(a, e, w, M0, i, j, nproc=4, chunk=60)
fails = 0; worst = -1e9
for k in range(60):
    b = G.brute_dmin(a[i[k]], e[i[k]], w[i[k]], M0[i[k]], a[j[k]], e[j[k]], w[j[k]], M0[j[k]], nsamp=2_000_000)
    rel = (dmin[k] - b) / b
    worst = max(worst, rel)
    if dmin[k] > b * 1.05:
        fails += 1
        print(f"  FAIL {k}: event {dmin[k]:.4e} brute {b:.4e} rel {rel:+.3f}")
print(f"control: exact event search vs brute (min-miss, 60 pairs): worst rel {worst:+.5f}, fails {fails}/60")
print("checker-table spot check (8 seeds, e=0.05, random omega): da=0.005/0.02/0.1 ->")
