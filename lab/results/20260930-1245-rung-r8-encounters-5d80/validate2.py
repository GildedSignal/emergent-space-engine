"""Second validation pass on the densest belt (highest sigma_e):
- brute-force minimum distance vs machinery on encounter + random pairs;
- shear-grid per-body event formula vs an ultra-fine cell-index trajectory.
Writes validate2.json."""
import json, random, time
import numpy as np
from common import *

belts = json.load(open('belts.json'))
b = max(belts, key=lambda r: r['sigma_e'])
bi = b['belt']
rng = random.Random(20261008)
for _ in range(bi + 1):
    sigma_e, rho = draw_belt_params(rng)
assert abs(sigma_e - b['sigma_e']) < 1e-12 and abs(rho - b['rho']) < 1e-15
a, e, varpi, lam0 = sample_belt(rng, b['N'], sigma_e)
n = a ** -1.5
print(f"densest belt {bi}: sigma_e={sigma_e:.3g} rho={rho:.3g}")

res = analyse_belt(a, e, varpi, lam0, rho, keep_dips=True)
i, j = res['_pairs']; dips = res['_dips']
enc = np.unique(dips['pair'])
rng2 = np.random.default_rng(11)
keep_all = np.arange(len(i))
extra = rng2.choice(keep_all, size=120, replace=False)
sub = np.unique(np.concatenate([enc, extra]))
sub_i, sub_j = i[sub], j[sub]

def brute_min(ii, jj, S=60001):
    ts = np.linspace(0.0, T_TOTAL, S)
    xi, yi, _, _, _, _ = states(a[ii][:, None], e[ii][:, None], varpi[ii][:, None],
                                lam0[ii][:, None], n[ii][:, None], ts[None, :])
    xj, yj, _, _, _, _ = states(a[jj][:, None], e[jj][:, None], varpi[jj][:, None],
                                lam0[jj][:, None], n[jj][:, None], ts[None, :])
    dd = np.hypot(xi - xj, yi - yj)
    k = np.argmin(dd, axis=1)
    out = dd[np.arange(len(ii)), k]
    tt = ts[k]; h = ts[1] - ts[0]
    lo, hi = tt - 2 * h, tt + 2 * h
    for _ in range(60):
        m1 = lo + (hi - lo) / 3; m2 = hi - (hi - lo) / 3
        d1 = np.hypot(*(np.array(states(a[ii], e[ii], varpi[ii], lam0[ii], n[ii], m1)[:2]) -
                        np.array(states(a[jj], e[jj], varpi[jj], lam0[jj], n[jj], m1)[:2])))
        d2 = np.hypot(*(np.array(states(a[ii], e[ii], varpi[ii], lam0[ii], n[ii], m2)[:2]) -
                        np.array(states(a[jj], e[jj], varpi[jj], lam0[jj], n[jj], m2)[:2])))
        lo = np.where(d1 < d2, lo, m1); hi = np.where(d1 < d2, m2, hi)
    dm = np.hypot(*(np.array(states(a[ii], e[ii], varpi[ii], lam0[ii], n[ii], 0.5 * (lo + hi))[:2]) -
                    np.array(states(a[jj], e[jj], varpi[jj], lam0[jj], n[jj], 0.5 * (lo + hi))[:2])))
    return np.minimum(out, dm)

bm = brute_min(sub_i, sub_j)
fd = find_encounters(sub_i, sub_j, a, e, varpi, lam0, rho)
mmin = np.full(len(sub_i), np.inf)
np.minimum.at(mmin, fd['pair'], fd['d'])
mism = int(np.sum((mmin < rho) != (bm < rho)))
both = np.isfinite(mmin)
rel = float(np.max(np.abs(mmin[both] - bm[both]) / bm[both]))
print(f"pairs checked: {len(sub)} (encounters: {len(enc)}); mismatches: {mism}; max rel diff: {rel:.3g}")

# ---- shear E_body formula vs ultra-fine trajectory cell counting
sel = rng2.choice(len(a), size=30, replace=False)
base_r = float((a * (1 - e)).min() - rho - 1e-9)
S = 40000
t0 = T_TOTAL / 2
ts = t0 + np.linspace(0.0, TWOPI, S, endpoint=False) / n[sel][:, None]
x, y, _, _, th, r = states(a[sel][:, None], e[sel][:, None], varpi[sel][:, None],
                           lam0[sel][:, None], n[sel][:, None], ts)
rb = np.clip(np.floor((r - base_r) / rho), 0, None)
nb = (base_r + (rb + 0.5) * rho) ** -1.5
pp = np.mod(th - nb * ts, TWOPI) / rho
cell = np.stack([rb, pp], axis=-1)
chg = np.sum(np.any(np.abs(np.diff(cell, axis=1)) > 0, axis=-1), axis=1)  # per orbit
Nlev = np.maximum(np.floor((a[sel] * (1 + e[sel]) - base_r) / rho) -
                  np.ceil((a[sel] * (1 - e[sel]) - base_r) / rho) + 1.0, 0.0)
formula = 2.0 * Nlev  # radial part only; phi' path from formula below
Eb_formula = shear_events_per_body(a[sel], e[sel], varpi[sel], lam0[sel], n[sel], rho, T_TOTAL, base_r)
# compare totals
ratio = chg / Eb_formula
print(f"shear events/orbit: brute cell-index count vs formula, per body ratio min/med/max: "
      f"{ratio.min():.3f}/{np.median(ratio):.3f}/{ratio.max():.3f}")

json.dump(dict(belt=bi, sigma_e=sigma_e, rho=rho, pairs_checked=len(sub),
               encounters=len(enc), mismatches=mism, max_rel=rel,
               shear_ratio=[float(ratio.min()), float(np.median(ratio)), float(ratio.max())]),
          open('validate2.json', 'w'), indent=1)
print("validate2.json written")
