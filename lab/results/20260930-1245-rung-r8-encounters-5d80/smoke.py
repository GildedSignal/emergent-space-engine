"""Smoke test + brute-force validation of the machinery on a small belt."""
import random, time
import numpy as np
from common import *

rng = random.Random(20261008)
sigma_e, rho = draw_belt_params(rng)
print(f"belt params: sigma_e={sigma_e:.4g} rho={rho:.4g}")
N = 1500
a, e, varpi, lam0 = sample_belt(rng, N, sigma_e)
n = a ** -1.5

t0 = time.time()
res = analyse_belt(a, e, varpi, lam0, rho, keep_dips=True)
t1 = time.time()
for k in ("element-sort", "shear-grid", "ring-cells", "oracle"):
    print(k, {kk: round(vv, 4) if isinstance(vv, float) else vv for kk, vv in res[k].items()})
print(f"ref encounters={res['ref_encounters']} dips={res['dip_count']} "
      f"rate/body/orbit={res['rate']:.4g}  [{t1-t0:.1f}s]")

# ---------------- brute validation ----------------------------------------
i, j = overlap_pairs(a, e, rho, pad=0.0)
tk = timing_filter(i, j, a, e, lam0, rho, T_TOTAL)
i, j = i[tk], j[tk]
keep, g = g_filter(i, j, a, e, varpi, rho)
dips = res['_dips']
enc_set = set(np.unique(dips['pair']).tolist()) if dips['pair'].size else set()

rng2 = np.random.default_rng(7)
surv = np.array(sorted(enc_set), dtype=int)
extra = rng2.choice(np.nonzero(keep)[0], size=min(80, int(keep.sum())), replace=False)
disc_pool = np.nonzero(~keep)[0]
disc = rng2.choice(disc_pool, size=min(80, len(disc_pool)), replace=False) if len(disc_pool) else np.empty(0, int)
sub = np.unique(np.concatenate([surv, extra, disc]).astype(int))
sub_i, sub_j = i[sub], j[sub]

def brute_min(ii, jj, S=40001):
    ts = np.linspace(0.0, T_TOTAL, S)
    xi, yi, _, _, _, _ = states(a[ii][:, None], e[ii][:, None], varpi[ii][:, None],
                                lam0[ii][:, None], n[ii][:, None], ts[None, :])
    xj, yj, _, _, _, _ = states(a[jj][:, None], e[jj][:, None], varpi[jj][:, None],
                                lam0[jj][:, None], n[jj][:, None], ts[None, :])
    dd = np.hypot(xi - xj, yi - yj)
    k = np.argmin(dd, axis=1)
    out = dd[np.arange(len(ii)), k]
    tt = ts[k]
    # ternary refine +-2 grid steps
    h = ts[1] - ts[0]
    lo, hi = tt - 2 * h, tt + 2 * h
    for _ in range(50):
        m1 = lo + (hi - lo) / 3; m2 = hi - (hi - lo) / 3
        d1 = np.hypot(*[x - y for x, y in zip(states(a[ii], e[ii], varpi[ii], lam0[ii], n[ii], m1)[:2],
                                              states(a[jj], e[jj], varpi[jj], lam0[jj], n[jj], m1)[:2])])
        d2 = np.hypot(*[x - y for x, y in zip(states(a[ii], e[ii], varpi[ii], lam0[ii], n[ii], m2)[:2],
                                              states(a[jj], e[jj], varpi[jj], lam0[jj], n[jj], m2)[:2])])
        lo = np.where(d1 < d2, lo, m1); hi = np.where(d1 < d2, m2, hi)
    dm = np.hypot(*[x - y for x, y in zip(states(a[ii], e[ii], varpi[ii], lam0[ii], n[ii], 0.5 * (lo + hi))[:2],
                                          states(a[jj], e[jj], varpi[jj], lam0[jj], n[jj], 0.5 * (lo + hi))[:2])])
    return np.minimum(out, dm)

bm = brute_min(sub_i, sub_j)
fd = find_encounters(sub_i, sub_j, a, e, varpi, lam0, rho)
mmin = np.full(len(sub_i), np.inf)
np.minimum.at(mmin, fd['pair'], fd['d'])
cls_m, cls_b = mmin < rho, bm < rho
mism = np.nonzero(cls_m != cls_b)[0]
print(f"validation set: {len(sub)} pairs ({len(surv)} encounter, {len(extra)} random kept, 80 discarded)")
print(f"classification mismatches: {len(mism)}", mism)
both = np.isfinite(mmin)
rel = np.abs(mmin[both] - bm[both]) / bm[both]
print(f"max rel diff (machinery vs brute-refined min): {rel.max():.3g} over {both.sum()} pairs")
dd_min = bm[[p for p in range(len(sub)) if sub[p] in set(disc.tolist())]]
print(f"discarded-pair brute minimum distance / rho: min={dd_min.min()/rho if len(dd_min) else float('nan'):.2f} (must be > 1); n_disc={len(dd_min)}")
