#!/usr/bin/env python3
"""Is the plane's kick cadence (1/64 radial period, step_for) a derivable certificate or a magic tick?

Float premise probe in the lab's probe idiom (gravity-v1 probe 1/2): exact Kepler drift (the tube),
kick = the same sources `crates/universe/src/force.rs` reads, symmetric D(h/2) K D(h) ... D(h/2)
with per-body fixed h = T0/n. Reference = the same scheme at n=512 (convergence checked against
n=256). Behaviours judged: a, e, apsidal rate, Jacobi error type, resonant e-pumping,
bound/escape classification. Escaped (hyperbolic) bodies are frozen out and classified.

Scenes: belt (Sun + circular Jupiter + test asteroids, dense 2:1 slice) and moon (planet's doll,
full differential solar tide). Units GM_sun = 4 pi^2, AU, yr.
"""
import json
import sys
import time

import numpy as np

GM = 4 * np.pi**2
MU_J = GM / 1047.0          # Jupiter-like secondary / planet
A_J = 5.2
W_J = np.sqrt(GM / A_J**3)  # its circular rate
C_AUYR = 63241.0            # speed of light
KEPLER_ITERS = 8


def elements(x, v, mu):
    r = np.hypot(x[:, 0], x[:, 1])
    v2 = v[:, 0] ** 2 + v[:, 1] ** 2
    a = 1.0 / (2.0 / r - v2 / mu)
    rv = x[:, 0] * v[:, 0] + x[:, 1] * v[:, 1]
    fac = v2 - mu / r
    ex = (fac * x[:, 0] - rv * v[:, 0]) / mu
    ey = (fac * x[:, 1] - rv * v[:, 1]) / mu
    e = np.maximum(np.hypot(ex, ey), 1e-12)
    w = np.arctan2(ey, ex)
    cosnu = np.clip((x[:, 0] * ex + x[:, 1] * ey) / (r * e), -1.0, 1.0)
    nu = np.arccos(cosnu)
    nu = np.where(rv < 0, -nu, nu)
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(nu / 2), np.sqrt(1 + e) * np.cos(nu / 2))
    M = E - e * np.sin(E)
    return a, e, w, M


def from_plane(a, e, w, E, mu):
    ca, sa = np.cos(w), np.sin(w)
    s1 = np.sqrt(np.maximum(1 - e * e, 0.0))
    xp = a * (np.cos(E) - e)
    yp = a * s1 * np.sin(E)
    x = np.stack([ca * xp - sa * yp, sa * xp + ca * yp], -1)
    n_ = np.sqrt(mu / a**3)
    Ed = n_ / (1 - e * np.cos(E))
    vxp = -a * np.sin(E) * Ed
    vyp = a * s1 * np.cos(E) * Ed
    v = np.stack([ca * vxp - sa * vyp, sa * vxp + ca * vyp], -1)
    return x, v


def drift(x, v, h, mu):
    a, e, w, M = elements(x, v, mu)
    M = M + np.sqrt(mu / a**3) * h
    E = M + e * np.sin(M)
    for _ in range(KEPLER_ITERS):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return from_plane(a, e, w, E, mu)


def accel_belt(x, t):
    rj = np.stack([A_J * np.cos(W_J * t), A_J * np.sin(W_J * t)], -1)
    d = rj - x
    return MU_J * d / np.linalg.norm(d, axis=-1, keepdims=True) ** 3


def accel_moon(x, t):
    S = np.stack([-A_J * np.cos(W_J * t), -A_J * np.sin(W_J * t)], -1)
    d = S - x
    return GM * (d / np.linalg.norm(d, axis=-1, keepdims=True) ** 3
                 - S / np.linalg.norm(S, axis=-1, keepdims=True) ** 3)


def jacobi_belt(x, v, t):
    r = np.hypot(x[:, 0], x[:, 1])
    rj = np.stack([A_J * np.cos(W_J * t), A_J * np.sin(W_J * t)], -1)
    d = np.linalg.norm(rj - x, axis=-1)
    lz = x[:, 0] * v[:, 1] - x[:, 1] * v[:, 0]
    return 0.5 * (v[:, 0] ** 2 + v[:, 1] ** 2) - GM / r - MU_J / d - W_J * lz


def T_of(a, mu):
    return 2 * np.pi * np.sqrt(a**3 / mu)


def run(x0, v0, T_end, n, mu, accel, jacobi=None):
    """Symmetric WH, per-body fixed h. Returns (t, a, e, w_unwrapped, J, alive)."""
    N = x0.shape[0]
    a0, e0, _, _ = elements(x0, v0, mu)
    h = T_end / np.maximum((T_end / (T_of(a0, mu) / n)).astype(int), 1)
    x, v = x0.copy(), v0.copy()
    t = np.zeros(N)
    alive = np.ones(N, bool)
    x, v = drift(x, v, h / 2, mu)
    smax = int(np.max(T_end / h))
    thin = max(1, smax // 1500)
    rec_t, rec_a, rec_e, rec_w, rec_J = [], [], [], [], []
    for k in range(smax):
        act = k * h < T_end
        tmid = t + h / 2
        v = np.where(act[:, None], v + h[:, None] * accel(x, tmid), v)
        x2, v2 = drift(x, v, h, mu)
        x = np.where(act[:, None], x2, x)
        v = np.where(act[:, None], v2, v)
        t = t + np.where(act, h, 0.0)
        a, e, w, _ = elements(x, v, mu)
        dead = (~np.isfinite(a)) | (a <= 0) | (e >= 1.0) | (~np.isfinite(e))
        if dead.any() and alive.any():
            newly = dead & alive
            alive = alive & ~dead
        if (k % thin == 0) or (k == smax - 1):
            rec_t.append(np.where(alive, t, np.nan)); rec_a.append(a)
            rec_e.append(np.where(alive, e, np.nan)); rec_w.append(w)
            if jacobi is not None:
                rec_J.append(jacobi(x, v, t))
    rec_t.append(np.where(alive, t, np.nan))
    a, e, w, _ = elements(x, v, mu)
    rec_a.append(np.where(alive, a, np.nan))
    rec_e.append(np.where(alive, e, np.nan))
    rec_w.append(w)
    if jacobi is not None:
        rec_J.append(jacobi(x, v, t))
    return (np.array(rec_t), np.array(rec_a), np.array(rec_e),
            np.unwrap(np.nan_to_num(np.array(rec_w), nan=0.0), axis=0), rec_J, alive)


def growth_exp(t, y):
    d = np.abs(y)
    m = np.isfinite(d) & (d > 0)
    if m.sum() < 10:
        return 0.0
    tt, dd = np.log10(t[m]), np.log10(d[m])
    sel = tt >= tt[0] + 0.9 * (tt[-1] - tt[0])
    if sel.sum() < 5:
        return 0.0
    return float(np.polyfit(tt[sel], dd[sel], 1)[0])
def slopes(t, w, m):
    nS = t.shape[0]
    sel = slice(int(0.4 * nS), None)
    tt = np.nan_to_num(t[sel][:, m], nan=0.0)
    ww = np.nan_to_num(w[sel][:, m], nan=0.0)
    tc = tt - tt.mean(0, keepdims=True)
    return (tc * ww).sum(0) / np.maximum((tc * tc).sum(0), 1e-12)



def summarize(tag, res, ref, res64, mask, out):
    t, a, e, w, J, alive = res
    tr, ar, er, wr, Jr, aliver = ref
    _, a64, e64, w64, _, _ = res64
    cls = (alive == aliver) & mask
    m = mask & alive & aliver
    if m.sum() == 0:
        out.append(dict(tag=tag, n_class_match=float(cls.mean())))
        return
    da = np.abs(a[-1][m] - ar[-1][m]) / ar[-1][m]
    da_ctrl = np.abs(a64[-1][m] - ar[-1][m]) / ar[-1][m]
    de = np.abs(e[-1][m] - er[-1][m])
    de_ctrl = np.abs(e64[-1][m] - er[-1][m])
    sl, slr = slopes(t, w, m), slopes(tr, wr, m)
    sl64 = slopes(res64[0], w64, m)
    dw = np.abs(sl - slr) / np.maximum(np.abs(slr), 1e-12)
    dw_ctrl = np.abs(sl64 - slr) / np.maximum(np.abs(slr), 1e-12)
    row = dict(tag=tag, n_class_match=float(cls.mean()), n_alive=int(m.sum()),
               med_da_over_a=float(np.median(da)), med_da_ctrl=float(np.median(da_ctrl)),
               med_de=float(np.median(de)), med_de_ctrl=float(np.median(de_ctrl)),
               med_wrate_rel_err=float(np.median(dw)), med_wrate_rel_ctrl=float(np.median(dw_ctrl)),
               max_da_over_a=float(np.nanmax(da)))
    if J:
        Jm = np.array(J)[:, m]
        row["jacobi_max_drift"] = float(np.nanmax(np.abs(Jm - Jm[0][None, :])))
        row["jacobi_walk_exponent"] = growth_exp(np.nanmean(t[:, m], 1), (Jm - Jm[0][None, :]).mean(1))
    out.append(row)
    print(json.dumps(row))


def main():
    scene = sys.argv[1]
    rng = np.random.default_rng(27)
    t0 = time.time()
    out = []
    if scene == "belt":
        N = 120
        a_base = np.concatenate([np.linspace(2.45, 3.15, 96), 3.24 + 0.09 * rng.random(24)])
        e0 = 0.02 + 0.18 * rng.random(N)
        phi = 2 * np.pi * rng.random(N)
        mu = GM
        x0 = np.stack([a_base * np.cos(phi), a_base * np.sin(phi)], -1)
        v0 = np.stack([-np.sin(phi), np.cos(phi)], -1) * (np.sqrt(GM / a_base) * np.sqrt(1 + e0))[:, None]
        T_end = 6000.0
        res_mask = (a_base > 3.22) & (a_base < 3.34)
        ns = [64, 16, 8, 4, 2, 1]
        runs = {n: run(x0, v0, T_end, n, mu, accel_belt, jacobi_belt) for n in [512] + ns}
        ref, res64 = runs[512], runs[64]
        print(f"# belt runs done {time.time()-t0:.0f}s", file=sys.stderr)
        for n in ns:
            res = runs[n]
            emax = np.nanmax(res[2], 0); emax_r = np.nanmax(ref[2], 0)
            summarize(f"belt_nonres_n{n}", res, ref, res64, ~res_mask, out)
            out[-1]["emax_rel_err"] = float(np.median(np.abs(emax - emax_r)[~res_mask] / np.maximum(emax_r[~res_mask], 1e-3)))
            summarize(f"belt_res_n{n}", res, ref, res64, res_mask, out)
            out[-1]["emax_rel_err"] = float(np.median(np.abs(emax - emax_r)[res_mask] / np.maximum(emax_r[res_mask], 1e-3)))
        conv = run(x0[:40], v0[:40], T_end, 256, mu, accel_belt, jacobi_belt)
        da = np.abs(conv[1][-1] - runs[512][1][-1][:40]) / runs[512][1][-1][:40]
        out.append(dict(tag="ref_convergence_256_vs_512",
                        med_da_over_a=float(np.nanmedian(da)), max_da_over_a=float(np.nanmax(da))))
    elif scene == "moon":
        a_m = np.repeat([0.15, 0.25, 0.35, 0.45], 2) * A_J * (1 / 1047 / 3) ** (1 / 3)
        e0 = np.tile([0.05, 0.2], 4)
        phi = 2 * np.pi * rng.random(8)
        mu = MU_J
        x0 = np.stack([a_m * np.cos(phi), a_m * np.sin(phi)], -1)
        v0 = np.stack([-np.sin(phi), np.cos(phi)], -1) * (np.sqrt(mu / a_m) * np.sqrt(1 + e0))[:, None]
        T_end = 600 * float(np.median(T_of(a_m, mu)))
        ns = [64, 16, 8, 4, 2]
        runs = {n: run(x0, v0, T_end, n, mu, accel_moon) for n in [512] + ns}
        ref, res64 = runs[512], runs[64]
        print(f"# moon runs done {time.time()-t0:.0f}s", file=sys.stderr)
        for n in ns:
            summarize(f"moon_all_n{n}", runs[n], ref, res64, np.ones(8, bool), out)
    qrows = []
    if scene == "belt":
        a_ast, T_ast = 3.0, T_of(3.0, GM)
        w_syn = abs(2 * np.pi / T_of(A_J, GM) - 2 * np.pi / T_ast)
        aprime = MU_J / (A_J - a_ast) ** 2 * (w_syn + 2 * np.pi / T_ast) ** 2
    else:
        T_ast = float(np.median(T_of(a_m, MU_J)))
        aprime = 2 * GM * float(np.median(a_m)) / A_J**3 * (2 * np.pi / T_ast) ** 2
    for Q, name in [(2**20, "Q=2^20"), (2**40, "Q=2^40")]:
        h_req = (24 * (C_AUYR / Q) / aprime) ** (1 / 3)
        row = dict(tag=f"certificate_{scene}", q=name, aprime_est=float(aprime),
                   h_req_yr=float(h_req), n_pred_per_orbit=float(T_ast / h_req))
        out.append(row); qrows.append(row)
    json.dump(dict(rows=out, elapsed_s=time.time() - t0), open(f"metrics-{scene}.json", "w"), indent=1)
    for r in qrows:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
