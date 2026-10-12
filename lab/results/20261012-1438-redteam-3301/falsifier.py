#!/usr/bin/env python3
"""Premise red-team: the view gather's Newton-from-previous-frame at relativistic speeds.

Attacks representation.md SS2 'Observables': "Each visible tube crosses the observer's past
light cone once; Newton's method finds the crossing, starting from the previous frame's."
Flat 2D spacetime, c = 1, observer static (a constant-velocity observer is a pure frame
change), 60 Hz frames in observer time. Ground truth: bisection (g provably monotone:
g' = 1 - n.v >= 1 - beta > 0). Scenes: head-on constant beta; relativistic circular orbit;
close flyby; a thrusting chase (rapidity linear in proper time). Float64, run < 60 s.
"""
import json
import numpy as np

CAP = 8        # Newton iteration cap (the view has the hardest deadline; it must be capped)
TOL = 1e-7     # seconds; far below any sprite-position need
FPS = 60.0


def scenes():
    out = {}
    for beta in (0.1, 0.9, 0.99, 0.999):                  # A: head-on, constant beta
        x0 = 60.0
        T_end = x0 / beta
        T = np.arange(0.5, T_end, 1.0 / FPS)
        brack = (2.0 * x0 + 10.0) / (1.0 - beta)          # root lag <= D/(1-beta) + margin
        out[f"A{beta}"] = (T, (lambda b: lambda t: (x0 - b * t, np.zeros_like(t)))(beta),
                           (lambda b: lambda t: (-b * np.ones_like(t), np.zeros_like(t)))(beta),
                           np.zeros(2), ("t", brack))
    for beta, D0 in [(0.1, 3), (0.6, 3), (0.9, 3), (0.99, 3), (0.6, 10), (0.9, 10),
                     (0.99, 10), (0.995, 10), (0.999, 10)]:   # B: circular orbit
        a = 1.0
        w = beta / a
        T_end = min(63.0, max(20.0, 4 * np.pi * a / beta))
        T = np.arange(0.5, T_end, 1.0 / FPS)
        out[f"B{beta}@{D0}"] = (T, (lambda W: lambda t: (a * np.cos(W * t), a * np.sin(W * t)))(w),
                                (lambda W, b: lambda t: (-b * np.sin(W * t), b * np.cos(W * t)))(w, beta),
                                np.array([D0, 0.0]), ("t", 12000.0))
    for beta, b in [(0.9, 0.05), (0.9, 1.0), (0.99, 0.05), (0.99, 0.2), (0.99, 1.0)]:  # C: flyby
        T_end = 40.0 / beta
        out[f"C{beta}@{b}"] = (T, (lambda B, bb: lambda t: (-30.0 + B * t, np.full_like(t, bb)))(beta, b),
                               (lambda B: lambda t: (B * np.ones_like(t), np.zeros_like(t)))(beta),
                               np.zeros(2), ("t", 35000.0))
    # D: chase with burn. Rapidity r = r0 (tau<0), r0 + kappa*tau (tau>=0); x(0)=60, t(0)=0.
    r0, kappa, x0 = float(np.arctanh(0.95)), 0.02, 60.0
    ch0, sh0, er0 = np.cosh(r0), np.sinh(r0), np.exp(r0)

    def tx(tau):
        tau = np.asarray(tau, float)
        r = r0 + kappa * np.maximum(tau, 0.0)
        t = np.where(tau > 0, (np.sinh(r) - sh0) / kappa, ch0 * tau)
        x = x0 + np.where(tau > 0, -(np.cosh(r) - ch0) / kappa, sh0 * tau)
        return t, x

    def dtx(tau):
        r = r0 + kappa * np.maximum(np.asarray(tau, float), 0.0)
        return np.cosh(r), -np.sinh(r)

    def tau_of_t(t):
        t = np.asarray(t, float)
        return np.where(t > 0, (np.arcsinh(kappa * np.maximum(t, 0) + sh0) - r0) / kappa, t / ch0)

    T = np.arange(31.0, 65.0, 1.0 / FPS)

    def make_D(pre_sign, seed0):
        # pre_sign=-1: smooth chase (approaches throughout); +1: impulsive flip at tau=0
        def tx2(tau):
            tau = np.asarray(tau, float)
            r = r0 + kappa * np.maximum(tau, 0.0)
            t = np.where(tau > 0, (np.sinh(r) - sh0) / kappa, ch0 * tau)
            x = x0 + np.where(tau > 0, -(np.cosh(r) - ch0) / kappa, pre_sign * sh0 * tau)
            return t, x

        def dtx2(tau):
            r = r0 + kappa * np.maximum(np.asarray(tau, float), 0.0)
            return np.cosh(r), np.where(np.asarray(tau, float) > 0, -np.sinh(r),
                                        pre_sign * np.sinh(r))

        def g2(tau, Tt):
            t_arr, x = tx2(tau)
            dt, dx = dtx2(tau)
            return t_arr + np.abs(x) - Tt, dt + np.sign(x) * dx  # dA/dtau, per branch

        def pos_of2(p):
            _, x = tx2(p)
            return x, np.zeros_like(x)

        return g2, pos_of2, tau_of_t

    g1, p1, _ = make_D(-1, 1.05 * (T[0] - 60.0) * er0)   # pre-burn A slope e^{-r0}
    out["D1chase"] = (T, None, None, np.zeros(2), ("tau2", g1, p1, tau_of_t,
                                                   1.05 * (T[0] - 60.0) * er0))
    g2f, p2f, _ = make_D(+1, 1.05 * (T[0] - 60.0) / er0)  # pre-burn A slope e^{+r0}
    out["D2flip"] = (T, None, None, np.zeros(2), ("tau2", g2f, p2f, tau_of_t,
                                                  1.05 * (T[0] - 60.0) / er0))
    return out


def run(name, T, pos, vel, Xo, mode):
    F = T.size
    if isinstance(mode, tuple) and mode[0] == "t":
        brack = mode[1]
        mode = "t"
    if mode == "t":
        def g_gp(t, Tt):
            x, y = pos(t)
            vx, vy = vel(t)
            dx, dy = Xo[0] - x, Xo[1] - y
            D = np.hypot(dx, dy)
            return t + D - Tt, 1.0 - (dx * vx + dy * vy) / D
        hi, lo = T.copy(), T - brack
        def pos_of(p):  # position at parameter (here: time)
            return pos(p)
    elif isinstance(mode, tuple) and mode[0] == "tau2":
        _, g_gp, pos_of, tau_of_t, seed0 = mode
        hi = tau_of_t(T)
        lo = (T - 200.0) * (np.exp(r0 := 0.0) if False else 1.0)  # replaced below
        lo = np.minimum((T - 200.0) / 6.25, (T - 200.0) * 6.25)   # safe on both branches
    else:
        _, tx, dtx, tau_of_t, er0, seed0 = mode

        def g_gp(tau, Tt):
            t_arr, x = tx(tau)
            dt, dx = dtx(tau)
            return t_arr + np.abs(x) - Tt, dt + np.sign(x) * dx

        hi, lo = tau_of_t(T), (T - 200.0) / er0
        def pos_of(p):
            _, x = tx(p)
            return x, np.zeros_like(x)

    # ground truth: bisection, 80 halvings
    a_, b_ = lo.copy(), hi.copy()
    for _ in range(80):
        m = 0.5 * (a_ + b_)
        neg = g_gp(m, T)[0] < 0
        a_ = np.where(neg, m, a_)
        b_ = np.where(neg, b_, m)
    t_true = 0.5 * (a_ + b_)

    # uniqueness scan (subsample): sign changes of g on a fine grid over the bracket
    max_roots, min_fp = 0, np.inf
    for i in np.arange(0, F, max(1, F // 100)):
        grid = np.linspace(lo[i], hi[i], 20001)
        f, fp = g_gp(grid, T[i])
        sg = np.sign(f)
        max_roots = max(max_roots, int(np.sum(sg[:-1] * sg[1:] < 0)))
        min_fp = min(min_fp, float(np.min(fp)))

    def newton(seed):
        t = np.array(seed, dtype=float, copy=True)
        iters, done = 0, False
        for _ in range(CAP):
            if done:
                break
            f, fp = g_gp(t, T[i:i+1])
            step = f / fp if abs(fp) > 1e-18 else np.inf
            iters += 1
            t = t - step
            done = abs(step) < TOL or not np.isfinite(t)
        return t.item(), iters, done

    # seeded run: frame 0 cold, then the previous frame's Newton root (the design)
    if mode == "t":
        x0s, y0s = pos_of(np.array([T[0]]))
        prev = T[0] - float(np.hypot(Xo[0] - x0s[0], Xo[1] - y0s[0]))
    else:
        prev = seed0  # tau-modes carry their own sane frame-0 seed
    t_seed = np.empty(F); it_seed = np.empty(F, int); dn_seed = np.empty(F, bool)
    for i in range(F):
        t_seed[i], it_seed[i], dn_seed[i] = newton(np.array([prev]))
        prev = t_seed[i]

    # cold-start control: naive seed every frame (t = T - D(T); for tau-mode, light lag
    # taken at the relativistic closure rate 1-beta0 = 0.05, a fair static guess)
    if mode == "t":
        xs, ys = pos_of(hi)
        cold_seeds = hi - np.hypot(Xo[0] - xs, Xo[1] - ys)
    else:
        _, xh = pos_of(hi)
        cold_seeds = tau_of_t(hi - np.abs(xh) * (1.0 - 0.95))
    t_cold = np.empty(F); it_cold = np.empty(F, int); dn_cold = np.empty(F, bool)
    for i in range(F):
        t_cold[i], it_cold[i], dn_cold[i] = newton(np.array([cold_seeds[i]]))

    def sky_deg(t_new, t_ref):
        xn, yn = pos_of(t_new)
        xr, yr = pos_of(t_ref)
        dn = np.arctan2(yn - Xo[1], xn - Xo[0])
        dr = np.arctan2(yr - Xo[1], xr - Xo[0])
        return np.degrees(np.abs((dn - dr + np.pi) % (2 * np.pi) - np.pi))

    capped = ~dn_seed
    err = sky_deg(t_seed, t_true)
    comp = np.abs(np.diff(t_seed)) * FPS
    return {
        "scene": name, "frames": int(F),
        "it_mean": float(np.mean(it_seed)), "it_p99": float(np.percentile(it_seed, 99)),
        "it_max": int(np.max(it_seed)), "cap_hits": int(capped.sum()),
        "sky_err_max_deg_capped": float(np.max(err[capped])) if capped.any() else 0.0,
        "seed_one_iter_frac": float(np.mean(it_seed <= 1)),
        "compression_max": float(np.max(comp)) if comp.size else 0.0,
        "cold_it_p99": float(np.percentile(it_cold, 99)), "cold_cap_hits": int((~dn_cold).sum()),
        "uniqueness_max_roots": int(max_roots), "min_gp_grid": float(min_fp),
    }


if __name__ == "__main__":
    res = []
    for name, args in scenes().items():
        r = run(name, *args)
        res.append(r)
        print(f"{r['scene']:>12} F={r['frames']:5d} it mean/p99/max={r['it_mean']:5.2f}/"
              f"{r['it_p99']:3.0f}/{r['it_max']:2d} cap={r['cap_hits']:4d} "
              f"skyErr(cap)={r['sky_err_max_deg_capped']:8.3f}deg comp<={r['compression_max']:8.1f} "
              f"1-iter={r['seed_one_iter_frac']:.3f} cold p99/cap={r['cold_it_p99']:3.0f}/"
              f"{r['cold_cap_hits']:4d} roots={r['uniqueness_max_roots']} minG'={r['min_gp_grid']:.2e}",
              flush=True)
    with open("metrics.json", "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote metrics.json")
