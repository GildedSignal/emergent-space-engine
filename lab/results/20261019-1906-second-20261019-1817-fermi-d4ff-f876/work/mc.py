#!/usr/bin/env python3
"""Steady-state belt-belt pair-event rate on the exact shipped genesis.

Instrument: a pair of test bodies on exact Kepler orbits conjuncts (same polar
angle) |dn|/2pi times per root-time; each conjunction's miss distance is the
impact parameter b of the local relative motion (no mutual gravity -> straight
lines locally). Over the quasi-periodic conjunction-angle sequence the angle is
uniform, so the per-pair event rate at reach d is (|dn|/2pi) * P_theta(b < d).
Monte-Carlo over genesis pairs (bootstrap from the ported table, dwpi, th
uniform). Outputs Gamma(d) = pair events / game-s / root of reach at N = 1e9,
event-speed stats, slow-tail (curvature-risk) fraction, batch errors.

usage: mc.py [P_pairs] [K_th] [max_d_exp] [--validate]
  --validate restricts the reported ladder to d >= 1e4 (pre-registration gate)
"""
import json
import sys
import numpy as np
import beltlib as bl

def run(P=8_000_000, K=8, seed=7, dmin_report=0.0):
    a_t, e_t, p_t, w_t = bl.genesis_table()
    S = len(a_t)
    rng = np.random.default_rng(seed)
    n_t = bl.mean_motion(a_t)

    d_grid = np.array([bl.D_CONTACT, 0.25, 1.0, 4.0, 16.0, 64.0, bl.D_ENC,
                       256.0, 1e3, 3e3, 1e4, 3e4, 1e5, 3e5, 1e6, 2e6])
    d_grid = np.sort(d_grid)
    nb = 8                                   # error batches
    hits = np.zeros((nb, len(d_grid)))
    whits = np.zeros((nb, len(d_grid)))      # w-weighted
    shearbins = np.zeros((nb, len(d_grid), 4))   # |dv|/(Om|dr|) bins [0,3),[3,10),[10,30),[30,inf)
    vsum = np.zeros((nb, len(d_grid)))
    slow = np.zeros((nb, len(d_grid)))       # w-weighted |dv| < 3 Om |dr|
    dvr_sum = np.zeros((nb, len(d_grid)))    # |dr| of events (w-weighted)
    chunk = 400_000
    done = 0
    while done < P:
        m = min(chunk, P - done)
        i = rng.integers(0, S, m); j = rng.integers(0, S, m)
        a1, e1, p1 = a_t[i], e_t[i], p_t[i]
        a2, e2, p2 = a_t[j], e_t[j], p_t[j]
        dn = np.abs(n_t[i] - n_t[j]) / (2 * np.pi)     # crossings per root-time
        dwpi = rng.uniform(0, 2 * np.pi, m)
        th = rng.uniform(0, 2 * np.pi, (m, K))
        b = np.empty((m, K)); dv = np.empty((m, K))
        dr = np.empty((m, K)); om = np.empty((m, K))
        for k in range(K):
            b[:, k], dv[:, k], dr[:, k], om[:, k] = bl.conj_geom(
                a1, e1, p1, a2, e2, p2, th[:, k], dwpi)
        w = np.broadcast_to(dn[:, None], (m, K))
        ok = dv > 1e-12
        b = np.where(ok, b, np.inf)
        batch = np.minimum((done + np.arange(m)) * nb // P, nb - 1)
        bcol = np.repeat(batch[:, None], K, 1)
        v = np.broadcast_to(dv, (m, K))
        drc = np.broadcast_to(dr, (m, K))
        omc = np.broadcast_to(om, (m, K))
        ratio = v / np.maximum(omc * np.abs(drc), 1e-300)   # |dv|/(Om|dr|), shear-safety
        sbin = np.digitize(ratio, [3.0, 10.0, 30.0])
        for di, d in enumerate(d_grid):
            sel = (b < d) & ok
            if not sel.any():
                continue
            wb = np.where(sel, w, 0.0)
            hits[:, di] += np.bincount(bcol[sel], minlength=nb)
            whits[:, di] += np.bincount(bcol[sel], weights=wb[sel], minlength=nb)
            vsum[:, di] += np.bincount(bcol[sel], weights=(wb * v)[sel], minlength=nb)
            slowc = sel & (v < 3.0 * omc * np.abs(drc))
            slow[:, di] += np.bincount(bcol[slowc], weights=wb[slowc], minlength=nb)
            dvr_sum[:, di] += np.bincount(bcol[sel], weights=(wb * np.abs(drc))[sel], minlength=nb)
            for sb in range(4):
                m2 = sel & (sbin == sb)
                if m2.any():
                    shearbins[:, di, sb] += np.bincount(bcol[m2], weights=wb[m2], minlength=nb)
        done += m

    scale = (bl.N9 * (bl.N9 - 1) / 2.0) / (P * K) / bl.ROOT_T_S  # -> /game-s at 1e9
    out = {"P": P, "K": K, "seed": seed, "table": S, "ladder": []}
    for di, d in enumerate(d_grid):
        if d < dmin_report:
            continue
        wmean = whits[:, di].mean() * scale
        werr = whits[:, di].std(ddof=1) * scale / np.sqrt(nb)
        rate = wmean / d
        cerr = werr / d
        cnt = hits[:, di].sum()
        wtot = whits[:, di].mean()
        vmean = vsum[:, di].mean() / max(wtot, 1e-300)          # root/root-time
        drmean = dvr_sum[:, di].mean() / max(wtot, 1e-300)
        slowf = slow[:, di].mean() / max(wtot, 1e-300)
        sbmean = [float(shearbins[:, di, s].mean() * scale / d) for s in range(4)]
        out["ladder"].append({
            "d_root": float(d),
            "pair_events_per_game_s": wmean,
            "gamma_per_root_per_game_s": rate, "err": cerr,
            "gamma_shearbin_gt3_gt10_gt30_and_le3": sbmean,
            "gamma_shearsafe_gt10": sbmean[2] + sbmean[3],
            "mean_event_dv_km_s": vmean * bl.C_KM_S,
            "mean_event_abs_dr_root": abs(drmean), "slow_tail_frac": slowf,
            "raw_hits": int(cnt)})
    return out

if __name__ == "__main__":
    P = int(sys.argv[1]) if len(sys.argv) > 1 else 8_000_000
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    dmin = 1e4 if ("--validate" in sys.argv) else 0.0
    o = run(P, K, dmin_report=dmin)
    print(json.dumps(o, indent=1))
