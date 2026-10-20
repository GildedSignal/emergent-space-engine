#!/usr/bin/env python3
"""20261020-1503-redteam-039d: strong-field occlusion at the photon-sphere rim.

Premise under attack (representation.md L57 x 22d1's per-row worldtube cure, in the
hole's own doll): can a straight-chord occlusion predicate be right anywhere near a
black hole? Truth: exact 2D Schwarzschild null geodesics (quadrature + bisection).
Units M=1. Sky = circle. Run time target < 60 s.
"""
import json
import os
import time
import numpy as np

t0 = time.time()
BC = 3.0 * np.sqrt(3.0)          # critical impact parameter
_S, _W = np.polynomial.legendre.leggauss(96)

def V(r):
    return (r - 2.0) / r**3

def turn(b):
    th = np.arccos(np.clip(-3.0 * np.sqrt(3.0) / b, -1.0, 1.0)) / 3.0
    return 2.0 * b / np.sqrt(3.0) * np.cos(th)
def sweep(b, r_base, r_end):
    """Sweep from r_base out to r_end, substitution r = r_base + (r_end-r_base)sin^2 u.
    Radicand 1/b^2 - V(r) on both branches (at a turning point V(r0) = 1/b^2)."""
    bshape = np.shape(b)
    one = np.ones(bshape)
    D = np.asarray(r_end, float) - np.asarray(r_base, float)
    u = (0.25 * np.pi * (_S + 1.0)).reshape((len(_S),) + (1,) * np.ndim(b))
    one = np.ones(bshape)
    r = np.asarray(r_base, float) + D * np.sin(u) ** 2 * one
    drad = np.maximum(1.0 / np.asarray(b, float) ** 2 - V(r), 1e-300)
    val = np.sum(_W.reshape((len(_W),) + (1,) * np.ndim(b)) * (D * np.sin(2.0 * u) * one / (r**2 * np.sqrt(drad))), axis=0)
    return val * 0.25 * np.pi

def T_total(b, r_o, r_e):
    r0 = turn(b)
    return sweep(b, r0, r_o) + sweep(b, r0, r_e)

def D_direct(b, r_o, r_e):
    r_lo, r_hi = (r_e, r_o) if r_e < r_o else (r_o, r_e)
    return sweep(b, r_lo, r_hi)

def solve_targets(Ttg, r_o, r_e):
    """Solve T(b)=Ttg. Monotone branch (D increasing in b) below T_c, turning (G
    decreasing in b) above. Returns b and is_monotone flag."""
    r_lo = min(r_o, r_e)
    b_hi = float(np.sqrt(1.0 / V(r_lo))) * (1.0 - 1e-9)
    T_c = float(D_direct(np.array([b_hi]), r_o, r_e)[0])
    b_c_lo = BC * (1 + 1e-9)
    b = np.full(Ttg.shape, np.nan)
    mono = Ttg < T_c * (1 + 1e-4)   # razor band above T_c pinned to the mono branch
    if np.any(mono):
        lo, hi = np.zeros(Ttg.shape), np.full(Ttg.shape, b_hi)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            ok = D_direct(mid, r_o, r_e) < Ttg
            lo = np.where(ok, mid, lo); hi = np.where(ok, hi, mid)
        b = np.where(mono, 0.5 * (lo + hi), b)
    if np.any(~mono):
        lo = np.full(Ttg.shape, b_c_lo); hi = np.full(Ttg.shape, b_hi)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            ok = T_total(mid, r_o, r_e) > Ttg
            lo = np.where(ok, mid, lo); hi = np.where(ok, hi, mid)
        b = np.where(~mono, 0.5 * (lo + hi), b)
    return b, mono

def arrival_alpha(b, r_o):
    return np.arcsin(np.clip(b * np.sqrt(1 - 2.0 / r_o) / r_o, -1, 1))
ctl = {}
ctl["turn_at_bc"] = float(turn(np.array([BC * (1 + 1e-12)]))[0])
b_ctl = np.array([1e4])
half = float(sweep(b_ctl, turn(b_ctl), 1e6)[0])
ctl["deflection_relerr"] = abs(half - (np.pi / 2 + 2.0 / 1e4 - np.arcsin(1e4 / 1e6))) / (2.0 / 1e4)
for r_o in (20.0, 6.0, 4.0, 3.2):
    b_deep, _ = solve_targets(np.array([40.0]), r_o, 30.0)
    a_num = float(arrival_alpha(b_deep, r_o)[0])
    a_cl = float(np.arcsin(BC * np.sqrt(1 - 2 / r_o) / r_o))
    ctl[f"shadow_relerr_r{r_o}"] = abs(a_num - a_cl) / a_cl
    ctl[f"shadow_frac_circle_r{r_o}"] = a_cl / np.pi

# ---------------------------------------------------------------- scene sweep
NAZ = 240
PHI = np.linspace(0.0, 2 * np.pi, NAZ, endpoint=False)
VIS_FLOOR = 1e-3          # image visible if magnification ratio >= floor (9f4a tail)
scenes = {}
for r_o in (20.0, 6.0, 4.0, 3.2):
    f_o = np.sqrt(1 - 2.0 / r_o)
    for r_e in (30.0, 6.5, 3.5):
        key = f"r{o if False else r_o}_{r_e}".replace(".", "p")
        Ttg = np.concatenate([PHI + 2 * np.pi * k for k in range(4)]
                             + [(2 * np.pi - PHI) + 2 * np.pi * k for k in range(4)])
        nb = 8
        b_map, mono_map = solve_targets(Ttg, r_o, r_e)
        b_map = b_map.reshape(nb, NAZ); mono_map = mono_map.reshape(nb, NAZ)
        Tchk = np.where(mono_map, D_direct(b_map, r_o, r_e), T_total(b_map, r_o, r_e))
        good = np.isfinite(b_map) & (np.abs(Tchk - Ttg.reshape(nb, NAZ)) < 1e-3 * Ttg.reshape(nb, NAZ))
        b_map = np.where(good, b_map, np.nan)
        b_map2, _ = solve_targets(Ttg + 1e-5, r_o, r_e)
        b_map2 = b_map2.reshape(nb, NAZ)
        dbdT = np.abs(b_map2 - b_map) / 1e-5
        al = arrival_alpha(b_map, r_o)
        dal_db = f_o / (r_o * np.sqrt(np.maximum(1 - (b_map * f_o / r_o) ** 2, 1e-300)))
        mu = np.where(np.isfinite(b_map), 1.0 / np.maximum(dbdT * dal_db, 1e-300), 0.0)
        vis = np.isfinite(b_map) & (mu > VIS_FLOOR) & (mu < 1e3) & ((b_map - BC) > 1e-3)
        n_vis = vis.sum(axis=0)
        idx = np.arange(NAZ)
        i_best = np.where(vis, mu, -1).argmax(axis=0)
        b_best, mono_best = b_map[i_best, idx], mono_map[i_best, idx]
        sc = scenes.setdefault(key, dict(r_o=r_o, r_e=r_e))
        sc.update(n_vis_mean=float(n_vis.mean()), n_vis_max=int(n_vis.max()),
                  mu_best_p50=float(np.median(mu[i_best, idx])))
        if r_e < r_o:                       # near-side rows: chord predicate on the row
            blk2 = mono_best & (b_best * f_o < 2.0)     # horizon-radius occluder
            blk3 = mono_best & (b_best * f_o < 3.0)     # photon-sphere-radius occluder
            other = vis.copy(); other[i_best, idx] = False
            no_other = ~other.any(axis=0)
            sc.update(near_blocked_R2=float(blk2.mean()), near_blocked_R3=float(blk3.mean()),
                      near_vanished_R2=float((blk2 & no_other).mean()),
                      near_vanished_R3=float((blk3 & no_other).mean()))
        # naive-bearing composition: flat chord observer->emitter
        d_oe = np.sqrt(r_o**2 + r_e**2 - 2 * r_o * r_e * np.cos(PHI))
        b_flat = r_o * r_e * np.abs(np.sin(PHI)) / d_oe
        sc["naive_fab_frac"] = float((b_flat < BC).mean())
        al_flat = np.abs(np.arctan2(r_e * np.sin(PHI), r_e * np.cos(PHI) - r_o))
        err = np.nanmin(np.where(np.isfinite(al), np.abs(al - al_flat[None, :]), np.inf), axis=0)
        err_v = err[vis.any(axis=0)]
        sc.update(flat_row_err_p50=float(np.median(err_v)),
                  flat_row_err_p99=float(np.quantile(err_v, 0.99)))
        if vis.any():                       # rim wall: pixel-resolution db vs distance to b_c
            need = np.where(vis & (dal_db > 0), 1e-3 / np.maximum(dal_db, 1e-300), np.inf)
            j = np.unravel_index(need.argmin(), need.shape)   # most sensitive visible image
            sc["rim_delta_b_1px"] = float(need[j])
            sc["rim_dist_to_bc"] = float(b_map[j] - BC)
            sc["rim_wall_ratio"] = float(need[j] / (b_map[j] - BC))

# ------------------------------------------- planet occluder: chord ray vs true path
occ = {}
for phi_e in (2.6, 2.9, 3.1):
    r_o, r_e, r_c, R_p = 6.0, 30.0, 5.5, 0.2
    b_p = float(solve_targets(np.array([phi_e]), r_o, r_e)[0][0])
    r0 = float(turn(np.array([b_p]))[0])
    S_e = float(sweep(np.array([b_p]), np.array([r0]), np.array([r_e]))[0])
    a_arr = float(arrival_alpha(np.array([b_p]), r_o)[0])
    rs = np.geomspace(max(r0, 1e-6), r_e, 300)
    sw = sweep(np.array([b_p]), np.array([r0]), rs).ravel()
    theta_obs_side = (phi_e - S_e) - sw                      # observer-side branch
    theta_em_side = (phi_e - S_e) + sw                       # emitter-side branch
    pts = []
    for th, rr, sel in ((theta_obs_side, rs, rs <= r_o), (theta_em_side, rs, rs > r0)):
        th, rr = th[sel], rr[sel]
        pts.append(np.stack([rr * np.cos(th), rr * np.sin(th)], axis=1))
    pts = np.concatenate(pts)
    phis_c = np.linspace(0, 2 * np.pi, 1440, endpoint=False)
    cpos = np.stack([r_c * np.cos(phis_c), r_c * np.sin(phis_c)], axis=1)
    d_path = np.min(np.hypot(pts[:, None, 0] - cpos[None, :, 0],
                             pts[:, None, 1] - cpos[None, :, 1]), axis=0)
    u = np.array([np.cos(a_arr), np.sin(a_arr)])             # backward ray direction
    t_pr = (cpos - np.array([r_o, 0.0])) @ u
    foot = np.array([r_o, 0.0]) + np.clip(t_pr, 0, None)[:, None] * u
    d_ray = np.hypot(cpos[:, 0] - foot[:, 0], cpos[:, 1] - foot[:, 1])
    mism = (d_ray < R_p) != (d_path < R_p)
    occ[f"phi{phi_e}"] = dict(b_prime=b_p, r_turn=r0, arrival_alpha=a_arr,
                              mismatch_frac=float(mism.mean()),
                              max_dev_M=float(np.max(np.abs(d_ray - d_path))),
                              ray_blocked_frac=float((d_ray < R_p).mean()),
                              path_blocked_frac=float((d_path < R_p).mean()))

out = dict(controls=ctl, scenes=scenes, occluder_chord_vs_path=occ,
           elapsed_s=time.time() - t0)
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "results.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
