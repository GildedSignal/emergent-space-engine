#!/usr/bin/env python3
"""Kinetic-theorem cross-check (third instrument, analytic side).

Gamma_kin(d->0) = int n(x)^2 <|dv|>(x) dx  [pair events / root / root-time]
computed shell-resolved from time-sampled genesis states (uniform in mean
anomaly = time-proportional). Also reports the co-located dispersion in cells
of several sizes (the checker's 4e6-root cell def) and the global annular
dispersion (the author's 22.9 km/s def), each vs the flux-weighted mean that
the d->0 rate actually needs (<|dv|> weighted by |dv|).
"""
import json
import numpy as np
import beltlib as bl
from brute import kepler_pos

def main(S=200000, R=4, seed=13):
    a_t, e_t, p_t, w_t = bl.genesis_table()
    rng = np.random.default_rng(seed)
    n = bl.mean_motion(a_t)
    xs, ys, vxs, vys = [], [], [], []
    for r in range(R):
        M = np.mod(rng.uniform(0, 2 * np.pi, S), 2 * np.pi)
        x, y, E = kepler_pos(a_t, e_t, w_t, M)
        denom = 1.0 - e_t * np.cos(E)
        vxo = -a_t * n * np.sin(E) / denom
        vyo = a_t * n * np.sqrt(1 - e_t * e_t) * np.cos(E) / denom
        cw = np.cos(w_t); sw = np.sin(w_t)
        xs.append(x); ys.append(y)
        vxs.append(vxo * cw - vyo * sw); vys.append(vxo * sw + vyo * cw)
    x = np.concatenate(xs); y = np.concatenate(ys)
    vx = np.concatenate(vxs); vy = np.concatenate(vys)
    r = np.hypot(x, y)
    # shells over occupied band
    nsh = 48
    edges = np.linspace(r.min(), r.max(), nsh + 1)
    gam_kin = 0.0
    shell_rows = []
    for i in range(nsh):
        m = (r >= edges[i]) & (r < edges[i + 1])
        cnt = m.sum()
        if cnt < 200:
            continue
        area = np.pi * (edges[i + 1] ** 2 - edges[i] ** 2)
        nN = (cnt / (R * area)) * (bl.N9 / S)   # density at N = 1e9
        idx = np.nonzero(m)[0]
        ii = rng.choice(idx, 4000); jj = rng.choice(idx, 4000)
        dv = np.hypot(vx[ii] - vx[jj], vy[ii] - vy[jj])
        dv = dv[ii != jj]
        gam_kin += nN * nN * dv.mean() * area    # per root per root-time
        shell_rows.append((edges[i] / bl.AU, nN, dv.mean() * bl.C_KM_S))
    gam_kin_gs = gam_kin / bl.ROOT_T_S           # per game-s
    # co-located dispersion in cells (checker def) and global annular
    def cell_disp(cell):
        ix = (x / cell).astype(np.int64); iy = (y / cell).astype(np.int64)
        k = (ix << 32) | iy
        o = np.argsort(k); sk = k[o]
        dv_m, dv2_m = 0.0, 0.0
        mcnt = 0
        for _ in range(3000):
            b = rng.integers(0, len(k))
            q = k[b]
            lo = np.searchsorted(sk, q, "left"); hi = np.searchsorted(sk, q, "right")
            c = hi - lo
            if c < 2:
                continue
            j = o[rng.integers(lo, hi)]
            if j == b:
                continue
            d = np.hypot(vx[b] - vx[j], vy[b] - vy[j])
            dv_m += d; dv2_m += d * d; mcnt += 1
        return dv_m / mcnt, np.sqrt(dv2_m / mcnt)
    cd4e6, cd4e6f = cell_disp(4e6)
    ii = rng.integers(0, len(vx), 200000); jj = rng.integers(0, len(vx), 200000)
    glob = np.hypot(vx[ii] - vx[jj], vy[ii] - vy[jj]) * bl.C_KM_S
    out = {
        "gamma_kin_shell_per_root_per_game_s": gam_kin_gs,
        "note": "flux theorem needs <|dv|>; the 1.74 km/s co-located MEAN underweights it",
        "colocated_mean_dv_km_s_4e6cell": cd4e6 * bl.C_KM_S,
        "colocated_rms_dv_km_s_4e6cell": cd4e6f * bl.C_KM_S,
        "global_annular_dv_km_s": glob.mean(),
        "occupied_r_AU": [r.min() / bl.AU, r.max() / bl.AU],
        "samples": int(len(vx)),
    }
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
