#!/usr/bin/env python3
"""Inversion probe (run 20261009-0208-inversion-a937).

Question: does the phase-neighbour 'train' certificate adopted from lab gold
20261006-0346-taleb-09b5 ("sort by longitude, watch k~4 neighbours, rebuild on
overtakes", triggered when the Binet clump diameter <= eps_u) survive
orientation spread inside a Binet clump?

Truth: exact and analytic for same-a circular orbits of arbitrary orientation
and sense: u1(t).u2(t) = c0 + A*cos(2t + psi), sampled at t in {0, pi/4, pi/2}
which determines (c0, A, psi) exactly.  d_min^2 = 2 (1 - min(1, c0 + A)).
Encounter: d_min < rho inside the horizon; meetings at t* = (-psi mod 2pi)/2
+ m*pi, i.e. exactly 2H meetings per encountering pair over H orbits.

Certificate (as adopted): ring-sorted by longitude lambda, watch k=4
ring-neighbours, distance-checked at evaluation times.

Scenes (all a=1, e=0, rho=1e-4, same Binet point -> clump diameter 0):
  phalanx   equatorial prograde, tight phase bunch          [gold's home regime]
  incl-node same node Omega=0, i ~ U(0, 0.1), tight phase   [orientation spread, safe axis]
  retro     one circle, half prograde half retrograde        [sense flip]
  polar     i=pi/2, Omega ~ U(0, pi), all prograde           [node spread at the degeneracy]

Usage: python3 train_probe.py [--scene all] [--json out.json]
"""
import argparse
import json
import math

import numpy as np

TWO_PI = 2.0 * math.pi
RHO = 1e-4          # encounter radius (the design's rho)
K = 4               # adopted watch width (ring neighbours each side)
H_ORBITS = 20       # horizon


def positions(om, inc, s, M, t):
    """Unit-sphere positions at time t (a=1, e=0, mean rate n=1)."""
    th = M + s * t
    cth, sth = np.cos(th), np.sin(th)
    cO, sO = np.cos(om), np.sin(om)
    ci, si = np.cos(inc), np.sin(inc)
    x = cO * cth - sO * ci * sth
    y = sO * cth + cO * ci * sth
    z = si * sth
    return np.stack([x, y, z], axis=-1)


def velocities(om, inc, s, M, t):
    th = M + s * t
    cth, sth = np.cos(th), np.sin(th)
    cO, sO = np.cos(om), np.sin(om)
    ci, si = np.cos(inc), np.sin(inc)
    vx = -cO * sth - sO * ci * cth
    vy = -sO * sth + cO * ci * cth
    vz = si * cth
    return s * np.stack([vx, vy, vz], axis=-1)  # dtheta/dt = s


def make_scene(name, n, rng):
    """Returns (om, inc, s, M). All scenes share the Binet point (1,0,0)."""
    if name == "phalanx":
        # the gold's tightest regime: mean ring spacing 3*rho (their
        # "traffic-jam case" stopped at ~3*rho spacing)
        return (np.zeros(n), np.zeros(n), np.ones(n, dtype=np.int64),
                rng.uniform(-1.5e-1, 1.5e-1, n))
    if name == "incl-node":
        return (np.zeros(n), rng.uniform(0.0, 0.1, n), np.ones(n, dtype=np.int64),
                rng.uniform(-1.5e-1, 1.5e-1, n))
    if name == "retro":
        s = np.where(np.arange(n) < n // 2, 1, -1).astype(np.int64)
        return (np.zeros(n), np.zeros(n), s, rng.uniform(0.0, TWO_PI, n))
    if name == "polar":
        return (rng.uniform(0.0, math.pi, n), np.full(n, math.pi / 2),
                np.ones(n, dtype=np.int64), rng.uniform(0.0, TWO_PI, n))
    raise ValueError(name)


def pair_truth(om, inc, s, M):
    """Exact per-pair d_min and phase psi for all pairs (same-a circular)."""
    p0 = positions(om, inc, s, M, 0.0)
    p1 = positions(om, inc, s, M, math.pi / 4)
    p2 = positions(om, inc, s, M, math.pi / 2)
    D0 = p0 @ p0.T
    D1 = p1 @ p1.T
    D2 = p2 @ p2.T
    c0 = 0.5 * (D0 + D2)
    ac = 0.5 * (D0 - D2)            # A cos(psi)
    as_ = c0 - D1                   # A sin(psi)
    A = np.hypot(ac, as_)
    psi = np.arctan2(as_, ac)
    maxdot = np.clip(c0 + A, None, 1.0)
    dmin = np.sqrt(np.maximum(0.0, 2.0 * (1.0 - maxdot)))
    return dmin, psi


def ring_ranks(lam, pairs_i, pairs_j):
    """Ring rank (circular-order distance) of j relative to i at one time."""
    order = np.argsort(lam, kind="stable")
    inv = np.empty(len(lam), dtype=np.int64)
    inv[order] = np.arange(len(lam))
    d = np.abs(inv[pairs_i] - inv[pairs_j])
    return np.minimum(d, len(lam) - d)


def dist_rank(pos, i, j):
    """Rank of j among i's nearest by 3D distance (self excluded)."""
    d = np.linalg.norm(pos - pos[i], axis=1)
    d[i] = np.inf
    return int(np.sum(d < d[j])) + 1


def lambdas(om, inc, s, M, t):
    p = positions(om, inc, s, M, t)
    return np.arctan2(p[:, 1], p[:, 0])


def run_scene(name, n, seed, budget_cadence_per_orbit=8, mc_events=4000):
    rng = np.random.default_rng(seed)
    om, inc, s, M = make_scene(name, n, rng)
    dmin, psi = pair_truth(om, inc, s, M)
    iu = np.triu_indices(n, 1)
    enc = dmin[iu] < RHO
    n_pairs_enc = int(enc.sum())

    res = {
        "scene": name, "n": n, "seed": seed, "rho": RHO, "k": K,
        "orbits": H_ORBITS,
        "binet_clump_diameter": 0.0,   # identical (U,V,W) by construction
        "true_encounter_pairs": n_pairs_enc,
        "true_pair_events": n_pairs_enc * 2 * H_ORBITS,
    }
    if n_pairs_enc == 0:
        res.update({"missed_any_cadence": 0, "frac_missed_any": 0.0,
                    "dist_rank_le4_frac": None})
        return res

    ei, ej = iu[0][enc], iu[1][enc]
    t0 = ((-psi[ei, ej]) % TWO_PI) / 2.0   # first meeting time, then every pi

    # Ring rank of the partner through the contact, evaluated just outside it
    # (ts +/- delta, delta = 10 contact half-durations, capped at pi/4 so
    # co-moving pairs with vrel ~ 0 stay sane).  ts itself is NOT used: at a
    # polar contact both bodies sit at the pole, where lambda = atan2(0,0) is
    # degenerate; the rank during contact equals one of the two flank values
    # (a polar body's lambda is piecewise constant and flips only at the pole).
    ranks_any, drank = [], []
    idx = np.arange(len(ei))
    if len(ei) > 6000:
        idx = rng.choice(len(ei), 6000, replace=False)
    for k_ in idx:
        i, j, ts = int(ei[k_]), int(ej[k_]), float(t0[k_])
        vi = velocities(om[i:i+1], inc[i:i+1], s[i:i+1], M[i:i+1], ts)[0]
        vj = velocities(om[j:j+1], inc[j:j+1], s[j:j+1], M[j:j+1], ts)[0]
        vrel = max(float(np.linalg.norm(vi - vj)), 1e-9)
        delta = min(10.0 * RHO / vrel, math.pi / 4)
        best = n  # worse than any rank
        for tt in (ts - delta, ts + delta):
            r = int(ring_ranks(lambdas(om, inc, s, M, tt),
                               np.array([i]), np.array([j]))[0])
            best = min(best, r)
        ranks_any.append(best)
        if len(drank) < 4000:
            drank.append(dist_rank(positions(om, inc, s, M, ts), i, j))
    ranks_any = np.array(ranks_any)
    drank = np.array(drank)
    res["rank_at_contact_median"] = float(np.median(ranks_any))
    res["rank_at_contact_p90"] = float(np.percentile(ranks_any, 90))
    res["rank_at_contact_max"] = int(ranks_any.max())
    res["frac_rank_gt_k_best_cadence"] = float(np.mean(ranks_any > K))
    res["missed_any_cadence"] = int(np.sum(ranks_any > K))
    res["n_rank_sample"] = int(len(ranks_any))
    res["dist_rank_le4_frac"] = float(np.mean(drank <= 4))  # the gold's statistic

    # --- budgeted cadence: fixed grid of evals, O(n*k) checks per orbit ----
    tau = TWO_PI / budget_cadence_per_orbit
    grid = np.arange(0.0, TWO_PI, tau)  # pattern repeats each orbit
    if len(ei) > mc_events:
        mc = rng.choice(len(ei), mc_events, replace=False)
    else:
        mc = np.arange(len(ei))
    caught = np.zeros(len(mc), dtype=bool)
    for g in grid:
        posg = positions(om, inc, s, M, g)
        lam = np.arctan2(posg[:, 1], posg[:, 0])
        ii, jj = ei[mc], ej[mc]
        r = ring_ranks(lam, ii, jj)
        d_g = np.linalg.norm(posg[ii] - posg[jj], axis=1)
        caught |= (r <= K) & (d_g < RHO)
    res["budget_evals_per_orbit"] = int(budget_cadence_per_orbit * n * (2 * K + 1))
    res["missed_budget_sample"] = int(np.sum(~caught))
    res["n_budget_sample"] = int(len(mc))
    res["frac_missed_budget"] = float(np.mean(~caught))

    # --- maintenance lower bound: order-change (overtake) count ------------
    if name == "retro":
        # every opposite-sense pair's longitude difference wraps twice per orbit
        res["overtakes_per_orbit"] = int(2 * (n // 2) * (n - n // 2))
    elif name == "polar":
        # lambda jumps by pi at each pole passage: 2 flips per body per orbit;
        # spot-check the ring displacement of one flip across many bodies.
        disp = []
        for _ in range(24):
            b = int(rng.integers(0, n))
            ts = float((math.pi / 2 - M[b]) % TWO_PI)  # next N-pole passage
            la = np.argsort(lambdas(om, inc, s, M, ts - 1e-3), kind="stable")
            lb = np.argsort(lambdas(om, inc, s, M, ts + 1e-3), kind="stable")
            inva = np.empty(n, dtype=np.int64); inva[la] = np.arange(n)
            invb = np.empty(n, dtype=np.int64); invb[lb] = np.arange(n)
            d = abs(int(inva[b]) - int(invb[b]))
            disp.append(min(d, n - d))
        med = float(np.median(disp))
        res["polar_flip_rank_displacement_median"] = med
        res["overtakes_per_orbit"] = int(2 * n * med)
    else:
        res["overtakes_per_orbit"] = 0
    return res


def adjudicate(name, n, seed, n_true=150, n_false=150):
    """Independent check of the analytic truth by dense position sampling:
    one full period at step rho/4 (resolves head-on dips), refined around the
    coarse minimum and around the analytic t* of claimed events."""
    rng = np.random.default_rng(seed + 777)
    om, inc, s, M = make_scene(name, n, rng)
    dmin, psi = pair_truth(om, inc, s, M)
    iu = np.triu_indices(n, 1)
    dm = dmin[iu]
    claimed = dm < RHO
    maxdot = 1.0 - dm * dm / 2.0
    thr = 1.0 - RHO * RHO / 2.0
    near = (~claimed) & (maxdot > thr - 1e-4)
    ti = np.where(claimed)[0]
    fi = np.where(near)[0]
    if len(ti) > n_true:
        ti = rng.choice(ti, n_true, replace=False)
    if len(fi) > n_false:
        fi = rng.choice(fi, n_false, replace=False)

    def brute_min(i, j, hint=None):
        ts = np.arange(0.0, TWO_PI, RHO / 4.0)
        pi_ = positions(om[i:i+1], inc[i:i+1], s[i:i+1], M[i:i+1], ts)
        pj_ = positions(om[j:j+1], inc[j:j+1], s[j:j+1], M[j:j+1], ts)
        d = np.linalg.norm(pi_ - pj_, axis=1)
        k_ = int(np.argmin(d))
        best = float(d[k_])
        centres = [float(ts[k_])]
        if hint is not None:
            centres.append(float(hint))
        for c in centres:
            fine = np.arange(max(0.0, c - RHO), min(TWO_PI, c + RHO), RHO / 16.0)
            if len(fine):
                pf_i = positions(om[i:i+1], inc[i:i+1], s[i:i+1], M[i:i+1], fine)
                pf_j = positions(om[j:j+1], inc[j:j+1], s[j:j+1], M[j:j+1], fine)
                best = min(best, float(np.min(np.linalg.norm(pf_i - pf_j, axis=1))))
        return best

    agree = {"scene": name, "true_checked": 0, "true_confirmed": 0,
             "false_checked": 0, "false_confirmed": 0}
    for k_ in ti:
        ii, jj = int(iu[0][k_]), int(iu[1][k_])
        agree["true_checked"] += 1
        if brute_min(ii, jj, hint=float(((-psi[ii, jj]) % TWO_PI) / 2.0)) < RHO:
            agree["true_confirmed"] += 1
    for k_ in fi:
        ii, jj = int(iu[0][k_]), int(iu[1][k_])
        agree["false_checked"] += 1
        if brute_min(ii, jj) >= RHO:
            agree["false_confirmed"] += 1
    return agree


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", default="all")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    scenes = {
        "phalanx": (1000, [1, 2]),
        "incl-node": (1000, [1, 2]),
        "retro": (1000, [1, 2]),
        "polar": (1500, [1, 2, 3]),
    }
    if args.scene != "all":
        scenes = {k: v for k, v in scenes.items() if k == args.scene}
    out = []
    for name, (n, seeds) in scenes.items():
        for sd in seeds:
            r = run_scene(name, n, sd)
            out.append(r)
            print(json.dumps(r), flush=True)
        adj = adjudicate(name, n, seeds[0])
        out.append(adj)
        print(json.dumps(adj), flush=True)
    if args.json:
        with open(args.json, "w") as f:
            json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
