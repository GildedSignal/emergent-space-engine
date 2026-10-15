#!/usr/bin/env python3
"""The in-band scan's candidate tier, falsified on a float replica of the ladder belt.

Scene (625b/d7e3/c481's ruin): player circular at 2.5 AU inside the ladder belt
(a U[2,3) AU, e Rayleigh(0.07) re-drawn above 0.4, doll 0), burn cadence: one minted
scan per 83 game-s for 16,000 game-s (193 mints). All floats; the tier is a
certificate (a superset), so floats may explore and only the miss count decides.

Tiers compared:
  shipped  — the radial index as shipped (16 bins/octave, apsidal filter, walk-all when
             the hit fraction exceeds bodies/4 + 64);
  naive-L  — sort by mean longitude only, NO eccentric widening (the kill control);
  LMe      — the proposed tier: buckets (a: 0.25 AU, M: 64, e: geometric), mean longitude
             L sorted within each bucket; every key is exactly linear or constant between
             kicks (L(t) = L0 + n t, M(t) = M0 + n t, a and e constant), so the only drift
             is the mean-motion shear n_max*dt, bounded from birth constants.
"""
import json
import sys
import time

import numpy as np

MU = 3.964e-14          # solar mu, AU^3/s^2
H = 83.0                # the burn's re-plan horizon, game-s
T_FLIGHT = 16_000.0     # the 625b cut
MINT = 83.3             # one minted scan per re-plan
SHIP_R_ROOT = 34 * 2**8          # Scalar::raw(34, 8) root units (scenario.rs ladder_ship)
ROOT_M = 1477.0                  # one root unit, m
R_CODE = 2**10 * 2 * SHIP_R_ROOT * ROOT_M / 1.496e11   # AU: 2^10 (ENCOUNTER_LOG2) * (ra+rb)
R_COUNT = 0.037                  # AU: back-solved from c481's ~21 encounters/mint at 1e5
PLAYER_A = 2.5
TAU = 2 * np.pi
SEEDS = {"1e5": (100_000, 1), "1e6": (1_000_000, 1)}
TRUTH_EVERY = {"1e5": 4, "1e6": 16}   # brute-force truth at every k-th mint


def belt(n, seed):
    rng = np.random.default_rng(seed)
    a = 2.0 + rng.random(n)
    e = 0.07 * np.sqrt(-2.0 * np.log(1.0 - rng.random(n)))
    bad = e > 0.4
    while bad.any():                       # the generator's re-draw above 0.4
        redraw = 0.07 * np.sqrt(-2.0 * np.log(1.0 - rng.random(int(bad.sum()))))
        e[bad] = redraw
        bad = e > 0.4
    varpi = rng.random(n) * TAU
    m0 = rng.random(n) * TAU
    nn = np.sqrt(MU / a**3)
    return a, e, varpi, m0, nn


def kepler_theta_r(a, e, varpi, m):
    """True longitude and radius at mean anomaly m (Newton on E; exact to fp)."""
    ea = m.copy()
    for _ in range(10):
        ea = ea - (ea - e * np.sin(ea) - m) / (1.0 - e * np.cos(ea))
    r = a * (1.0 - e * np.cos(ea))
    nu = np.arctan2(np.sqrt(np.maximum(1.0 - e**2, 0.0)) * np.sin(ea), np.cos(ea) - e)
    return varpi + nu, r


def eoc(e, m):
    return kepler_theta_r(np.ones_like(e), e, np.zeros_like(e), m)[0] - m


def setup(n, seed):
    a, e, varpi, m0, nn = belt(n, seed)
    l0 = (varpi + m0) % TAU
    n_p = np.sqrt(MU / PLAYER_A**3)
    v_p = n_p * PLAYER_A
    v_cap = np.sqrt(MU * (1 + e) / (a * (1 - e))).max()
    sweep = (v_p + v_cap) * H / PLAYER_A            # the player's swept-arc slack, rad
    shear_m = nn.max() * (T_FLIGHT + H)             # bucket drift bound over the whole flight

    a_edges = np.arange(2.0, 3.0001, 0.25)
    m_edges = np.linspace(0.0, TAU, 65)
    e_edges = np.array([0.0, 0.008, 0.016, 0.032, 0.064, 0.128, 0.256, 0.41])
    ai = np.clip(np.digitize(a, a_edges) - 1, 0, len(a_edges) - 2)
    mi = np.clip(np.digitize(m0, m_edges) - 1, 0, len(m_edges) - 2)
    ei = np.clip(np.digitize(e, e_edges) - 1, 0, len(e_edges) - 2)
    nm, ne = len(m_edges) - 1, len(e_edges) - 1
    bucket = (ai * nm + mi) * ne + ei
    nb = int(bucket.max()) + 1
    order = np.lexsort((l0, bucket))                 # L0-sorted inside contiguous buckets
    b_sorted = bucket[order]
    l_sorted = l0[order]
    starts = np.searchsorted(b_sorted, np.arange(nb), "left")
    ends = np.searchsorted(b_sorted, np.arange(nb), "right")
    live = (ends - starts) > 0

    # EOC band over each (M, e) bucket's sheared M-window, once, at max shear
    bd = np.empty((nm, ne, 2))
    for i in range(nm):
        mw = np.linspace(m_edges[i] - shear_m, m_edges[i + 1] + shear_m, 24)
        for j in range(ne):
            ew = np.linspace(e_edges[j], e_edges[j + 1], 24)
            g = eoc(ew[:, None], mw[None, :] % TAU)
            bd[i, j, 0] = g.min() - 1e-4
            bd[i, j, 1] = g.max() + 1e-4

    bid = np.arange(nb)
    ai_b = np.floor_divide(bid, nm * ne)
    mi_b = np.mod(np.floor_divide(bid, ne), nm)
    ei_b = np.mod(bid, ne)
    a_lo_b = a_edges[np.clip(ai_b, 0, len(a_edges) - 2)]
    return dict(a=a, e=e, varpi=varpi, m0=m0, nn=nn, n_p=n_p, v_p=v_p, v_cap=v_cap,
                sweep=sweep, shear_m=shear_m, l_sorted=l_sorted, order=order,
                starts=starts, ends=ends, live=live, nb=nb,
                a_lo_b=a_lo_b, a_hi_b=a_lo_b + 0.25, e_hi_b=e_edges[ei_b + 1],
                band_lo=bd[mi_b, ei_b, 0], band_hi=bd[mi_b, ei_b, 1])


def count_window(arr, lo, hi):
    """Count of arr (sorted) inside [lo, hi], wrap-aware (lo may exceed hi mod TAU)."""
    if lo <= hi:
        return np.searchsorted(arr, hi, "right") - np.searchsorted(arr, lo, "left")
    return (np.searchsorted(arr, TAU, "right") - np.searchsorted(arr, lo, "left")
            + np.searchsorted(arr, hi, "right"))


def measure(tag, n, seed, r_win, truth_every):
    s = setup(n, seed)
    a, e, varpi, m0, nn = s["a"], s["e"], s["varpi"], s["m0"], s["nn"]
    starts, ends, live, nb = s["starts"], s["ends"], s["live"], s["nb"]
    order, l_sorted = s["order"], s["l_sorted"]
    n_p, sweep, shear_m = s["n_p"], s["sweep"], s["shear_m"]
    v_p, v_cap = s["v_p"], s["v_cap"]
    r_min_b = s["a_lo_b"] * (1 - s["e_hi_b"])
    a_lo_b = s["a_lo_b"]
    n_lo_b, n_hi_b = np.sqrt(MU / s["a_hi_b"]**3), np.sqrt(MU / s["a_lo_b"]**3)
    band_lo, band_hi = s["band_lo"], s["band_hi"]
    rw = r_win + (v_p + v_cap) * H
    cone = ((s["a_lo_b"] * (1 - s["e_hi_b"]) < PLAYER_A + rw)
            & (s["a_hi_b"] * (1 + s["e_hi_b"]) > PLAYER_A - rw))
    ok = live & cone

    out = {"tag": tag, "n": n, "r_win_au": r_win, "r_code_au": R_CODE}
    cand_ship, cand_naive, cand_tier, aps_frac = [], [], [], []
    truth_hits, miss_naive, miss_tier, checked = [], 0, 0, 0
    t0 = time.time()
    for k, t in enumerate(np.arange(0.0, T_FLIGHT, MINT)):
        rmin, rmax = a * (1 - e), a * (1 + e)
        aps = (rmin < PLAYER_A + rw) & (rmax > PLAYER_A - rw)
        aps_frac.append(float(aps.mean()))
        cand_ship.append(float(n if aps.mean() > 0.25 + 64 / n else aps.sum()))

        centre = n_p * t + n_p * H / 2
        half = r_win / np.maximum(r_min_b, 1e-9) + n_p * H / 2 + sweep + shear_m
        lo = centre - half - n_hi_b * (t + H) - band_hi - 1e-9
        hi = centre + half - n_lo_b * t - band_lo + 1e-9
        half_n = r_win / a_lo_b + n_p * H / 2 + sweep + shear_m
        lo_n = centre - half_n - n_hi_b * (t + H) - 1e-9
        hi_n = centre + half_n - n_lo_b * t + 1e-9

        c_t = c_n = 0
        sel_t = np.zeros(n, dtype=bool)
        sel_n = np.zeros(n, dtype=bool)
        want_truth = (k % truth_every == 0)
        for b in np.flatnonzero(ok):
            s_i, e_i = starts[b], ends[b]
            if e_i <= s_i:
                continue
            arr = l_sorted[s_i:e_i]
            c_t += count_window(arr, lo[b] % TAU, hi[b] % TAU)
            c_n += count_window(arr, lo_n[b] % TAU, hi_n[b] % TAU)
            if want_truth:
                lt, ht = lo[b] % TAU, hi[b] % TAU
                w = (arr >= lt) & (arr <= ht) if lt <= ht else (arr >= lt) | (arr <= ht)
                sel_t[order[s_i:e_i]] |= w
                ln, hn = lo_n[b] % TAU, hi_n[b] % TAU
                w = (arr >= ln) & (arr <= hn) if ln <= hn else (arr >= ln) | (arr <= hn)
                sel_n[order[s_i:e_i]] |= w
        cand_tier.append(c_t)
        cand_naive.append(c_n)

        if want_truth:
            checked += 1
            hit = np.zeros(n, dtype=bool)
            for frac in (0.0, 0.5, 1.0):
                tau = t + H * frac
                th, r = kepler_theta_r(a, e, varpi, (m0 + nn * tau) % TAU)
                dx = r * np.cos(th) - PLAYER_A * np.cos(n_p * tau)
                dy = r * np.sin(th) - PLAYER_A * np.sin(n_p * tau)
                hit |= np.hypot(dx, dy) <= r_win
            truth_hits.append(int(hit.sum()))
            if hit.any():
                miss_tier += int((hit & ~sel_t).sum())
                miss_naive += int((hit & ~sel_n).sum())

    cs, cn, ct = np.array(cand_ship), np.array(cand_naive), np.array(cand_tier)
    th = np.array(truth_hits)
    mints = len(cs)
    out.update({
        "shipped_cand_mean": float(cs.mean()), "tier_cand_mean": float(ct.mean()),
        "tier_cand_p95": float(np.percentile(ct, 95)), "tier_cand_max": float(ct.max()),
        "naive_cand_mean": float(cn.mean()),
        "cut_mean": float(cs.mean() / max(ct.mean(), 1)),
        "apsidal_frac_mean": float(np.mean(aps_frac)),
        "truth_mints": checked, "truth_hits_mean": float(th.mean()) if len(th) else 0.0,
        "miss_tier": int(miss_tier), "miss_naive": int(miss_naive),
        "standing_mb_per_mint": float(ct.mean() * 224 / 1e6),
        "flight_held_gb": float(ct.mean() * 224 * mints / 1e9),
        "capture_ms_shipped": float(cs.mean() * 0.303e-3),
        "capture_ms_tier": float(ct.mean() * 0.303e-3),
        "shear_rad_at_end": float(shear_m),
        "wall_s": round(time.time() - t0, 1),
    })
    return out


if __name__ == "__main__":
    results = []
    for tag, (n, seed) in SEEDS.items():
        for name, r in (("R_code", R_CODE), ("R_count", R_COUNT)):
            o = measure(tag, n, seed, r, TRUTH_EVERY[tag])
            o["window"] = name
            results.append(o)
            print(name, tag, json.dumps(o), flush=True)
    path = sys.argv[1] if len(sys.argv) > 1 else "out/scan_tier.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", path)
