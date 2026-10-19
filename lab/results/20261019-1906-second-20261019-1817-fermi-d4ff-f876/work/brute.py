#!/usr/bin/env python3
"""Brute-force validator: exact Kepler propagation of M genesis bodies,
per-pair debounced threshold crossings (a pair counts one event each time it
comes within d and leaves; sample-0 burn-in pairs excluded), spatial-hash
candidate finding, warm-started Newton. Reports Gamma(d) scaled to N = 1e9
and mean event speed at entry.

usage: brute.py d_root M T_game_s [seed]
"""
import json
import sys
import time
import numpy as np
import beltlib as bl

def kepler_pos(a, e, wpi, M, E0=None):
    """Positions from wrapped mean anomaly M (8 Newton iters, e <= 0.4)."""
    E = M.copy() if E0 is None else E0.copy()
    for _ in range(8):
        f = E - e * np.sin(E) - M
        E = E - f / (1.0 - e * np.cos(E))
    cosE = np.cos(E); sinE = np.sin(E)
    xo = a * (cosE - e); yo = a * np.sqrt(1 - e * e) * sinE
    cw = np.cos(wpi); sw = np.sin(wpi)
    return xo * cw - yo * sw, xo * sw + yo * cw, E

def run(d, M, T_gs, seed=11):
    a_t, e_t, p_t, w_t = bl.genesis_table()
    rng = np.random.default_rng(seed)
    a = a_t[:M]; e = e_t[:M]; wpi = w_t[:M]
    n = bl.mean_motion(a)                      # rad/root-time
    ph = rng.uniform(0, 1, M)
    vmax = 15.0 / bl.ROOT_KM                   # 15 km/s cap (measured conj. speeds <= 6.3), ~2% bias
    dt_gs = d / (2.0 * vmax)
    nsamp = max(2, int(T_gs / dt_gs))
    ts = (np.arange(nsamp) + 0.5) * (T_gs / nsamp)          # game-s
    ts_rt = ts / bl.ROOT_T_S                                 # root-time

    OFF = 1 << 30
    prev_active = set()
    events = 0
    nspd = 0
    vsum = 0.0
    Mcache = None
    Ecache = None
    t0 = time.time()
    for si, t_rt in enumerate(ts_rt):
        Manom = np.mod(2 * np.pi * ph + n * t_rt, 2 * np.pi)
        if Ecache is None:
            x, y, Ecache = kepler_pos(a, e, wpi, Manom)
        else:
            dM = np.mod(Manom - Mcache + np.pi, 2 * np.pi) - np.pi
            x, y, Ecache = kepler_pos(a, e, wpi, Manom, E0=Ecache + dM)
        Mcache = Manom
        ixi = (x / d).astype(np.int64)
        iyi = (y / d).astype(np.int64)
        key = ((ixi + OFF) << 32) | (iyi + OFF)
        order = np.argsort(key)
        sk = key[order]
        newkeys = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = ((ixi + dx + OFF) << 32) | (iyi + dy + OFF)
                lo = np.searchsorted(sk, q, "left")
                hi = np.searchsorted(sk, q, "right")
                cnt = hi - lo
                m = cnt > 0
                if not m.any():
                    continue
                ii = np.nonzero(m)[0]
                reps = cnt[ii]
                tot = int(reps.sum())
                if tot == 0:
                    continue
                starts = np.repeat(lo[ii], reps)
                offs = np.arange(tot) - np.repeat(np.concatenate(([0], np.cumsum(reps)[:-1])), reps)
                jj = order[starts + offs]
                vi = np.repeat(ii, reps)
                sel = vi < jj
                vi = vi[sel]; jj = jj[sel]
                if len(vi) == 0:
                    continue
                ddx = x[vi] - x[jj]; ddy = y[vi] - y[jj]
                keep = (ddx * ddx + ddy * ddy) < d * d
                if not keep.any():
                    continue
                vi = vi[keep]; jj = jj[keep]
                for pkk in (vi.astype(np.int64) * M + jj).tolist():
                    newkeys.add(pkk)
        # debounce: count first appearances vs previous sample's active set;
        # sample 0 is burn-in (pairs already inside d) and is excluded.
        if si > 0:
            entries = [k for k in newkeys if k not in prev_active]
            events += len(entries)
            if entries:
                vi = np.array([k // M for k in entries], dtype=np.int64)
                jj = np.array([k % M for k in entries], dtype=np.int64)
                denom = 1.0 - e * np.cos(Ecache)
                vxo = -a * n * np.sin(Ecache) / denom
                vyo = a * n * np.sqrt(1 - e * e) * np.cos(Ecache) / denom
                cw = np.cos(wpi); sw = np.sin(wpi)
                vx = vxo * cw - vyo * sw; vy = vxo * sw + vyo * cw
                dvx = vx[vi] - vx[jj]; dvy = vy[vi] - vy[jj]
                vsum += float(np.sum(np.sqrt(dvx * dvx + dvy * dvy)))
                nspd += len(entries)
        prev_active = newkeys
    rate = events / (T_gs * (nsamp - 1) / nsamp)
    rate9 = rate * (bl.N9 / M) ** 2
    out = {"d_root": d, "M": M, "T_game_s": T_gs, "dt_game_s": dt_gs,
           "samples": nsamp, "events": events, "burnin_note": "sample-0 pairs excluded",
           "gamma_per_root_per_game_s_at_1e9": rate9 / d,
           "pair_events_per_game_s_at_1e9": rate9,
           "mean_event_dv_km_s": (vsum / max(nspd, 1)) * bl.C_KM_S,
           "wall_s": time.time() - t0}
    return out

if __name__ == "__main__":
    d = float(sys.argv[1]); M = int(sys.argv[2]); T = float(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 11
    print(json.dumps(run(d, M, T, seed), indent=1))
