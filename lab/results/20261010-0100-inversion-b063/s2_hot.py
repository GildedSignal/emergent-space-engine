#!/usr/bin/env python3
"""S2: one stream, hot (sigma_e=0.05), wp spread 0.3 — the generic 'debris torus' scene.

Truth over one orbit (drift <= 0.3 rank slots, so a single t=0 M-sort ranks all events):
per pair, orbit curves cross where r_i(lam) = r_j(lam) -> A cos + B sin = C (closed form);
at each crossing, pass-time offset dt and local velocity sum give
d_min ~ |dt| * |v_i + v_j| / 2; encounter iff d_min < rho (verified on a subsample
by dense Kepler). Rank = circular position distance in the t=0 mean-anomaly sort.
"""
import json
import numpy as np
import sys
sys.path.insert(0, ".")
from harness import P, wrap_pm, body_state, vel_at_M, nu_to_M, ranks_at

rng = np.random.default_rng(23)
n, rho, sig_e, sig_w = 2000, 1e-4, 0.05, 0.3
e = np.abs(rng.normal(0, sig_e, n))
wp = rng.normal(0, sig_w, n)
a = 1.0 + rng.uniform(-rho / 2, rho / 2, n)
M0 = rng.uniform(0, 2 * np.pi, n)
p = a * (1 - e * e)
nmm = a ** -1.5
A = p[:, None] * e[None, :] * np.cos(wp[None, :]) - p[None, :] * e[:, None] * np.cos(wp[:, None])
B = p[:, None] * e[None, :] * np.sin(wp[None, :]) - p[None, :] * e[:, None] * np.sin(wp[:, None])
C = p[None, :] - p[:, None]


order0 = np.argsort(M0 % (2 * np.pi))
pos0 = np.empty(n, dtype=np.int64)
pos0[order0] = np.arange(n)

enc_ranks, enc_dt, enc_d = [], [], []
CH = 100_000
for lo in range(0, n, CH):
    i1 = min(lo + CH, n)
    rows = np.arange(lo, i1)
    ii, jj = np.meshgrid(rows, np.arange(n), indexing="ij")
    m = ii < jj
    ii, jj = ii[m], jj[m]
    Ai, Bi, Ci = A[ii, jj], B[ii, jj], C[ii, jj]
    R2 = Ai * Ai + Bi * Bi
    okx = R2 > Ci * Ci
    for sgn in (-1, 1):
        ph = np.arctan2(Bi, Ai)
        lam = ph + sgn * np.arccos(np.clip(Ci / np.sqrt(np.maximum(R2, 1e-300)), -1, 1))
        good = okx
        # pass times through lam for both bodies
        nu_i = wrap_pm(lam - wp[ii])
        nu_j = wrap_pm(lam - wp[jj])
        Mst_i = nu_to_M(nu_i, e[ii])
        Mst_j = nu_to_M(nu_j, e[jj])
        tA = (Mst_i - M0[ii]) % P
        tB = (Mst_j - M0[jj]) % P
        dt = wrap_pm(tA - tB)
        vi = vel_at_M(Mst_i, e[ii], wp[ii])
        vj = vel_at_M(Mst_j, e[jj], wp[jj])
        vsum = 0.5 * np.linalg.norm(vi + vj, axis=-1)
        dmin = np.abs(dt) * vsum
        hit = good & (dmin < rho)
        if hit.any():
            r = np.abs(pos0[ii[hit]] - pos0[jj[hit]]).astype(float)
            enc_ranks.append(np.minimum(r, n - r))
            enc_dt.append(dt[hit])
            enc_d.append(dmin[hit])

enc_ranks = np.concatenate(enc_ranks) if enc_ranks else np.array([])
res = {"n": n, "rho": rho, "sigma_e": sig_e, "sigma_wp": sig_w,
       "candidates_per_orbit_closed_form": int(len(enc_ranks))}
hits_meta = []
for lo in range(0, n, CH):
    i1 = min(lo + CH, n)
    rows = np.arange(lo, i1)
    ii, jj = np.meshgrid(rows, np.arange(n), indexing="ij")
    msk = ii < jj
    ii, jj = ii[msk], jj[msk]
    Ai, Bi, Ci = A[ii, jj], B[ii, jj], C[ii, jj]
    R2 = Ai * Ai + Bi * Bi
    okx = R2 > Ci * Ci
    for sgn in (-1, 1):
        ph = np.arctan2(Bi, Ai)
        lam = ph + sgn * np.arccos(np.clip(Ci / np.sqrt(np.maximum(R2, 1e-300)), -1, 1))
        nu_i = wrap_pm(lam - wp[ii]); nu_j = wrap_pm(lam - wp[jj])
        Mst_i = nu_to_M(nu_i, e[ii]); Mst_j = nu_to_M(nu_j, e[jj])
        tA = (Mst_i - M0[ii]) % P; tB = (Mst_j - M0[jj]) % P
        dt = wrap_pm(tA - tB)
        vi = vel_at_M(Mst_i, e[ii], wp[ii]); vj = vel_at_M(Mst_j, e[jj], wp[jj])
        dmin = np.abs(dt) * 0.5 * np.linalg.norm(vi + vj, axis=-1)
        hit = okx & (dmin < rho)
        w = np.where(hit)[0]
        for k in w:
            hits_meta.append((ii[k], jj[k], 0.5 * (tA[k] + tB[k])))

# authoritative truth: Kepler-confirm every candidate; ranks on confirmed only
conf_ranks = []
for (i, j, tm) in hits_meta:
    ts = np.linspace(tm - 2e-3, tm + 2e-3, 2001)
    xi, yi = body_state(M0[i] + nmm[i] * ts, e[i], wp[i])[:2]
    xj, yj = body_state(M0[j] + nmm[j] * ts, e[j], wp[j])[:2]
    if np.hypot(xi - xj, yi - yj).min() < rho:
        r = abs(pos0[i] - pos0[j])
        conf_ranks.append(min(r, n - r))
conf_ranks = np.array(conf_ranks)
res_conf = {
    "encounters_confirmed": int(len(conf_ranks)),
    "candidates_from_closed_form": len(hits_meta),
    "rank_median": float(np.median(conf_ranks)),
    "rank_p99": float(np.quantile(conf_ranks, 0.99)),
    "rank_max": int(conf_ranks.max()),
    "catch@4": float(np.mean(conf_ranks <= 4)),
    "frac_over_n/8": float(np.mean(conf_ranks > n / 8)),
}
print(json.dumps(res_conf, indent=1))
res.update(res_conf)
with open("s2_metrics.json", "w") as f:
    json.dump(res, f, indent=1)
sys.exit(0)
