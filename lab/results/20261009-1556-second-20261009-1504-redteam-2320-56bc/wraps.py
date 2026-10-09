#!/usr/bin/env python3
"""Wrap family for the BH lens (r* = 3M), zoomed at the capture edges
theta_lens +- b_c/r0 (eta-dependent; the winding family accumulates there),
on the SHIPPED tracer. Brightness = 1/|ds/dtheta| relative to the brightest
primary at that alignment. Three parts:
  1 zooms at eta = 1600, 400, 40, both sides, two levels each;
  2 instrument check: dphi halving + refinement at eta=190.3;
  3 hold test: can an extended-march continuation (mine, same RK4/Binet law,
    44000-step march) hold a HANDED wrap branch across frames, where the
    shipped scalar tracer (1100-step march) cannot even evaluate it?
Writes wraps-out.json.
"""
import numpy as np, json, time
import falsifier as F
from bh import roots_on_grid
from diag import extended_trace1

B_C = 3*np.sqrt(3)*F.M

def edges(eta):
    tl = np.arctan2(eta, F.D_OL)
    r0 = float(np.hypot(F.D_OL, eta))
    hw = B_C / r0
    return tl, tl + hw, tl - hw

def zoom(eta, side, dphi=0.005, n1=4001, ms=6000):
    L, Srel, rS = F.geom(eta)
    tl, eP, eM = edges(eta)
    c = eP if side > 0 else eM
    w1 = np.linspace(c - 1e-4, c + 0.012, n1) if side > 0 else np.linspace(c - 0.012, c + 1e-4, n1)
    r1 = roots_on_grid(w1, L, Srel, rS, dphi, max_steps=ms)
    w2 = np.linspace(c - 1e-6, c + 3e-5, 4001) if side > 0 else np.linspace(c - 3e-5, c + 1e-6, 4001)
    r2 = roots_on_grid(w2, L, Srel, rS, dphi, max_steps=ms)
    base = roots_on_grid(np.linspace(-0.25, 0.25, 2001), L, Srel, rS, dphi)
    p1 = min((sl for _, sl in base), default=np.inf)
    return dict(
        theta_lens=float(tl), edge=float(c),
        level1=[[float(t - c), float(sl)] for t, sl in r1],
        level2=[[float(t - c), float(sl)] for t, sl in r2],
        relmag_vs_brightest_primary=[[float(t - c), float(p1/sl)] for t, sl in r1 + r2
                                     if sl > 0])

def continuation_ext(tracked, L, Srel, rS, tol=0.5, maxit=6, dom=0.3):
    """F.continuation_frame, but evaluating with the extended march."""
    out = []
    for (th, s_prev, _ip) in tracked:
        t_seed, s_seed = th, s_prev
        t = th; conv = False; its = 0; s = None
        for it in range(maxit):
            s, rm = extended_trace1(t, L, Srel, rS)
            if s is None or rm < F.R_STAR: break
            its = it + 1
            if abs(s) < tol: conv = True; break
            if s_seed is None or abs(t - t_seed) < 1e-12:
                t_new = t - s/8000.0
            else:
                denom = (s - s_seed)
                t_new = t - s*(t - t_seed)/denom if abs(denom) > 1e-12 else t - s/8000.0
            if not np.isfinite(t_new) or abs(t_new - t) < 1e-12:
                t_new = t - s/8000.0
            t_seed, s_seed = t, s
            t = float(np.clip(t_new, -dom, dom))
        if conv: out.append(dict(theta=t, s=s, iters=its))
    return out

def main():
    t0 = time.time()
    F.R_STAR = 3.0
    out = {}
    for eta in (1600.0, 400.0, 40.0):
        out[str(eta)] = {f'side_+1' if s > 0 else 'side_-1': zoom(eta, s) for s in (+1, -1)}
    # instrument: refinement at eta=190.3, side +1
    a = zoom(190.3, +1, dphi=0.005, n1=4001)
    b = zoom(190.3, +1, dphi=0.0025, n1=6001)
    ta = [t for t, _ in a['level1']]; tb = [t for t, _ in b['level1']]
    match = [min((abs(t - u) for u in tb), default=None) for t in ta]
    out['refinement_190.3'] = dict(
        n_coarse=len(ta), n_fine=len(tb), max_root_shift=max(match) if match else None)
    # hold test: hand the wrap branch (zoom root) to the extended continuation
    hold = []
    etas = [190.3, 177.2, 164.1, 151.0, 137.9]
    seed_t = ta[0] + a['edge'] if ta else None
    tracked = None
    for eta in etas:
        L, Srel, rS = F.geom(eta)
        if tracked is None:
            s0, _ = extended_trace1(seed_t, L, Srel, rS)
            tracked = [(seed_t, s0, 0)]
        cont = continuation_ext(tracked, L, Srel, rS)
        truth = zoom(eta, +1)['level1']
        hold.append(dict(eta=eta, n_cont=len(cont),
                         theta=float(cont[0]['theta']) if cont else None,
                         iters=cont[0]['iters'] if cont else None,
                         truth_offsets=[o for o, _ in truth]))
        if cont: tracked = [(cont[0]['theta'], cont[0]['s'], cont[0]['iters'])]
        else: break
    out['hold_test'] = dict(seed_offset_from_edge=float(seed_t - a['edge']) if seed_t else None,
                            frames=hold)
    out['wall_s'] = round(time.time() - t0, 1)
    print(json.dumps(out, indent=1))
    with open('wraps-out.json', 'w') as fh:
        json.dump(out, fh, default=float)

if __name__ == '__main__':
    main()
