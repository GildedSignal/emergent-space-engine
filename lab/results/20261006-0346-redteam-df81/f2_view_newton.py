#!/usr/bin/env python3
"""F2 — is 'Newton from the previous frame's crossing' well conditioned at high c?

Flat spacetime (c = 1). Emitters on circular orbits (beta_e); observer flying
through the scene at beta_o (the game's 0.9c stream is a designed case, B15).
Per frame, solve g(te) = te + |x_obs - x_e(te)| - t_obs = 0 for the emission
time te; Newton seeded from the previous frame's root (representation.md 2,
'the view'); truth by bisection. Counts iterations, non-convergence, and
Newton leaving the causal window [t_obs - Dmax, t_obs].
"""
import numpy as np

R = 1.0            # emitter orbit radius
DFRAME = 2 * np.pi / 360  # ~1 degree of emitter orbit per frame
NFRAMES = 2_000
MAXIT = 50
TOL = 1e-13


def emitter_x(te, beta_e):
    """circular orbit in the x-y plane, phase chosen so te=0 is at (R, 0)."""
    w = beta_e / R
    return np.array([R * np.cos(w * te), R * np.sin(w * te), 0.0])


def g(te, t_obs, x_obs, beta_e):
    return te + np.linalg.norm(x_obs - emitter_x(te, beta_e)) - t_obs


def bisect(t_obs, x_obs, beta_e):
    lo, hi = t_obs - 100.0 * R, t_obs  # causal window: max separation is 61R
    flo, fhi = g(lo, t_obs, x_obs, beta_e), g(hi, t_obs, x_obs, beta_e)
    assert flo < 0 < fhi, (flo, fhi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(mid, t_obs, x_obs, beta_e) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def run(beta_e, beta_o, geometry):
    v_obs = beta_o * np.array([-1.0, 0.0, 0.0])  # observer flies toward scene
    x0_obs = np.array([60.0 * R, 0.0, 0.0])
    te_seed = None
    iters, bad_window, bad_conv, err_max = [], 0, 0, 0.0
    for k in range(1, NFRAMES):
        t_obs = k * DFRAME * R
        x_obs = x0_obs + v_obs * t_obs
        truth = bisect(t_obs, x_obs, beta_e)
        te = te_seed if te_seed is not None else truth - DFRAME * R
        te = min(max(te, t_obs - 100.0 * R), t_obs)  # clamp to causal window
        it = 0
        ok = False
        while it < MAXIT:
            f = g(te, t_obs, x_obs, beta_e)
            h = 1e-7 * R
            gp = (g(te + h, t_obs, x_obs, beta_e) - g(te - h, t_obs, x_obs, beta_e)) / (2 * h)
            step = f / gp
            te_new = te - step
            if not (t_obs - 100.0 * R < te_new < t_obs):
                bad_window += 1
                te_new = min(max(te_new, t_obs - 100.0 * R), t_obs)
            te = te_new
            it += 1
            if abs(g(te, t_obs, x_obs, beta_e)) < TOL:
                ok = True
                break
        if not ok:
            bad_conv += 1
        iters.append(it)
        err_max = max(err_max, abs(te - truth))
        te_seed = te
    iters = np.array(iters)
    return dict(med=np.median(iters), p99=np.percentile(iters, 99), mx=iters.max(),
                bad_window=bad_window, bad_conv=bad_conv, err_max=err_max)


def main():
    print(f"{'beta_e':>6} {'beta_o':>6} | {'med it':>6} {'p99':>5} {'max':>4} {'outWin':>6} {'noConv':>6} {'max |te-truth|':>15}")
    for beta_e in (0.0, 0.3, 0.6):
        for beta_o in (0.0, 0.9, 0.99):
            r = run(beta_e, beta_o, "through")
            print(f"{beta_e:6.2f} {beta_o:6.2f} | {r['med']:6.1f} {r['p99']:5.1f} {r['mx']:4d} "
                  f"{r['bad_window']:6d} {r['bad_conv']:6d} {r['err_max']:15.3e}")


if __name__ == "__main__":
    main()
