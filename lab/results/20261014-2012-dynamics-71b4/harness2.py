#!/usr/bin/env python3
"""Machine 2: the 524e-vs-54d9 discriminator on a BOUNDED kernel.

Same scene as harness.py (54d9's CRTBP, 32 bodies, seed 20261011), but the
kernel is second-order: each kick interval [t_s, t*] drifts on exact Kepler
while a fine sensor substeps the tide (midpoint quadrature along the drifted
path); at interval end the accrued impulse is applied at the interval MIDPOINT
(rewind: drift half, kick, drift half). Rules choose only t*:

  A   clock:            t* = t_s + T_ORB/K                  (control, bounded)
  C   analytic gate:    t* = t_s + theta*|a|/|adot|          (54d9 C, walks)
  Q   impulse quantum:  t* = first sensor substep where accrued |dp| >= q
                                                               (524e D, open)

Oracle: barycentric-rotation Jacobi. Series d(t) = running max of |C-C0|/|C0|
at quarter-parent-orbit samples, rebuilt post hoc from the fire log (exact
Kepler between kicks). slope = log-log slope over the second half (0 bounded,
1 walk). Phase diagnostics: per-fire synodic phase increment (n_b - n_p)*dt;
lock = max_{k<=8} circular concentration of accumulated phase, last half;
dphi_std = std of the increment over the last half (0 = phase-locked).

Usage: harness2.py OUT.npz RULE PARAM [horizon] [WS] [nbodies]
  RULE in {A, C, Q}; PARAM = K | theta | q.
"""
import math
import sys
import time

import numpy as np

MU_P = 1e-3
NB = math.sqrt(1.0 + MU_P)
T_ORB = 2.0 * math.pi / NB
MUP = MU_P / (1.0 + MU_P)


def init_bodies(n=32, seed=20261011):
    rng = np.random.default_rng(seed)
    a = 0.25 + 0.30 * rng.random(n)
    e = 0.4 * rng.random(n)
    om = 2 * np.pi * rng.random(n)
    f = 2 * np.pi * rng.random(n)
    p = a * (1 - e * e)
    r = p / (1 + e * np.cos(f))
    h = np.sqrt(p)
    vr = h / p * e * np.sin(f)
    vt = h / r
    x = r * np.cos(om + f)
    y = r * np.sin(om + f)
    vx = vr * np.cos(om + f) - vt * np.sin(om + f)
    vy = vr * np.sin(om + f) + vt * np.cos(om + f)
    return x, y, vx, vy, a, e


def elements_from_state(x, y, vx, vy):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = np.maximum(np.hypot(ex, ey), 1e-12)
    om = np.arctan2(ey, ex)
    E = np.arctan2(rv / (e * np.sqrt(a)), (1.0 - r / a) / e)
    return a, e, E, om


def kepler_state(a, e, E0, om, dt):
    nb = a ** -1.5
    M = np.mod(E0 - e * np.sin(E0) + nb * dt, 2.0 * np.pi)
    E = M.copy()
    for _ in range(10):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    sq = np.sqrt(np.maximum(1 - e * e, 1e-18))
    cE, sE = np.cos(E), np.sin(E)
    den = 1.0 - e * cE
    px = a * (cE - e)
    py = a * sq * sE
    pvx = -a * nb * sE / den
    pvy = a * sq * nb * cE / den
    co, so = np.cos(om), np.sin(om)
    return px * co - py * so, px * so + py * co, pvx * co - pvy * so, pvx * so + pvy * co


def tide(x, y, t):
    c, s = np.cos(NB * t), np.sin(NB * t)
    dx, dy = c - x, s - y
    d3 = (dx * dx + dy * dy) ** 1.5
    return MU_P * (dx / d3 - c), MU_P * (dy / d3 - s)


def tide_dot(x, y, vx, vy, t):
    nt = NB * t
    c, s = np.cos(nt), np.sin(nt)
    vpx, vpy = -NB * s, NB * c
    wx, wy = x - c, y - s
    d2 = wx * wx + wy * wy
    d3 = d2 ** 1.5
    d5 = d3 * d2
    ex, ey = vx - vpx, vy - vpy
    wd = wx * ex + wy * ey
    return (-MU_P * (ex / d3 - 3 * wx * wd / d5) - MU_P * vpx,
            -MU_P * (ey / d3 - 3 * wy * wd / d5) - MU_P * vpy)


def jacobi1(x, y, vx, vy, t):
    c, s = np.cos(NB * t), np.sin(NB * t)
    bx, by = x - MUP * c, y - MUP * s
    r = np.hypot(x, y)
    d = np.hypot(x - c, y - s)
    wrx, wry = vx + NB * y, vy - NB * x
    return (NB * NB * (bx * bx + by * by) + 2.0 / r + 2.0 * MU_P / d
            - (wrx * wrx + wry * wry))


def loglog_slope(t, d):
    n = len(t)
    h = n // 2
    tt = t[h:]
    dd = np.maximum(d[h:], 1e-18)
    if dd.max() <= 1e-17:
        return 0.0
    A = np.vstack([np.log(tt), np.ones_like(tt)]).T
    coef, *_ = np.linalg.lstsq(A, np.log(dd), rcond=None)
    return float(coef[0])


def circular_concentration(phi):
    best = 0.0
    for k in range(1, 9):
        z = np.mean(np.exp(1j * k * phi))
        best = max(best, abs(z))
    return best


def run(rule, param, horizon=400.0, WS=128, nbodies=32):
    x0, y0, vx0, vy0, a0, e0 = init_bodies(nbodies)
    a, e, E, om = elements_from_state(x0, y0, vx0, vy0)
    a_init, e_init, E_init, om_init = a.copy(), e.copy(), E.copy(), om.copy()
    nb = a ** -1.5
    t_ep = np.zeros(nbodies)
    C0 = jacobi1(x0, y0, vx0, vy0, 0.0)
    Px = np.zeros(nbodies)
    Py = np.zeros(nbodies)
    carry = np.zeros(nbodies)
    kicks = np.zeros(nbodies, dtype=np.int64)
    t_target = np.zeros(nbodies)
    if rule == 'A':
        t_target[:] = T_ORB / param
    elif rule == 'C':
        t_target[:] = T_ORB / 128.0
    fire_t = [[] for _ in range(nbodies)]
    fire_el = [[] for _ in range(nbodies)]
    fire_inc = [[] for _ in range(nbodies)]
    h_s = T_ORB / WS
    T_end = horizon * T_ORB
    Tb = 2 * np.pi * a ** 1.5
    t = np.zeros(nbodies)
    twall = time.time()
    niter = 0
    while (t < T_end - 1e-9).any() and niter < 400000:
        alive = t < T_end - 1e-9
        if rule == 'Q':
            h = np.where(alive, np.minimum(h_s, T_end - t), 0.0)
        else:
            h = np.clip(np.minimum(t_target - t, h_s), 1e-14, h_s)
            h = np.where(alive, np.minimum(h, np.maximum(T_end - t, 1e-14)), 0.0)
        act = h > 1e-15
        # sensor: midpoint quadrature along the drifted path
        tg = t + 0.5 * h
        sx, sy, _, _ = kepler_state(a, e, E, om, tg - t_ep)
        gx, gy = tide(sx, sy, tg)
        carry0 = carry.copy()
        P0x = Px.copy()
        P0y = Py.copy()
        Px += gx * h
        Py += gy * h
        dcarry = np.hypot(gx, gy) * h
        carry += dcarry
        if rule == 'Q':
            done = act & ((carry >= param) | (t + h >= T_end - 1e-9))
        else:
            done = act & ((t + h >= t_target - 1e-12) | (t + h >= T_end - 1e-9))
        if done.any():
            idx = np.where(done)[0]
            # QUANT_SNAP=1 disables interpolation (fires at substep end) —
            import os
            if rule == 'Q' and os.environ.get('QUANT_SNAP') == '1':
                fr = np.ones(len(idx))
            elif rule == 'Q':
                fr = np.where(dcarry[idx] > 0,
                              np.clip((param - carry0[idx]) / np.maximum(dcarry[idx], 1e-300), 0.0, 1.0),
                              1.0)
                at_end = t[idx] + h[idx] >= T_end - 1e-9
                fr = np.where(at_end, 1.0, fr)
            else:
                fr = np.ones(len(idx))
            tstar = np.minimum(t[idx] + fr * h[idx], T_end)
            # impulse accrued up to the crossing
            Pfx = P0x[idx] + fr * gx[idx] * h[idx]
            Pfy = P0y[idx] + fr * gy[idx] * h[idx]
            # rewind: apply the accrued impulse at the interval midpoint
            tm = 0.5 * (t_ep[idx] + tstar)
            mx, my, mvx, mvy = kepler_state(a[idx], e[idx], E[idx], om[idx], tm - t_ep[idx])
            mvx = mvx + Pfx
            mvy = mvy + Pfy
            am, em, Em, omm = elements_from_state(mx, my, mvx, mvy)
            fx, fy, fvx, fvy = kepler_state(am, em, Em, omm, tstar - tm)
            nb_old = nb[idx].copy()
            a[idx] = am
            e[idx] = em
            om[idx] = omm
            r = np.hypot(fx, fy)
            rv = fx * fvx + fy * fvy
            Enew = np.arctan2(rv / (em * np.sqrt(am)), (1.0 - r / am) / em)
            E[idx] = Enew
            nb[idx] = am ** -1.5
            t_ep[idx] = tstar
            kicks[idx] += 1
            for j, i in enumerate(idx):
                prev_t = fire_t[i][-1] if fire_t[i] else 0.0
                fire_t[i].append(tstar[j])
                fire_el[i].append((am[j], em[j], Enew[j], omm[j]))
                fire_inc[i].append(nb_old[j] * (tstar[j] - prev_t))
            Px[idx] = 0.0
            Py[idx] = 0.0
            carry[idx] = 0.0
            if rule == 'A':
                t_target[idx] = tstar + T_ORB / param
            elif rule == 'C':
                ax_, ay_ = tide(fx, fy, tstar)
                adx, ady = tide_dot(fx, fy, fvx, fvy, tstar)
                amag = np.hypot(ax_, ay_)
                admag = np.hypot(adx, ady)
                nu = param * amag / np.maximum(admag, 1e-18)
                nu = np.clip(nu, T_ORB / 1024.0, T_ORB / 4.0)
                t_target[idx] = tstar + nu
        t = t + h
        niter += 1
    wall = time.time() - twall
    # ---- post hoc: rebuild the C series from fire logs ----
    samp = T_ORB / 4.0
    samp_t = np.arange(samp, T_end + 1e-9, samp)
    ns = len(samp_t)
    dser = np.zeros((ns, nbodies))
    slopes = np.zeros(nbodies)
    locks = np.zeros(nbodies)
    dpstd = np.zeros(nbodies)
    for i in range(nbodies):
        ts = np.array([0.0] + fire_t[i])
        el = np.array([(a_init[i], e_init[i], E_init[i], om_init[i])] + fire_el[i])
        k = np.searchsorted(ts, samp_t, side='right') - 1
        k = np.clip(k, 0, len(ts) - 1)
        aa, ee, EE, oo = el[k, 0], el[k, 1], el[k, 2], el[k, 3]
        xs, ys, vxs, vys = kepler_state(aa, ee, EE, oo, samp_t - ts[k])
        C = jacobi1(xs, ys, vxs, vys, samp_t)
        d = np.abs(C - C0[i]) / np.abs(C0[i])
        dser[:, i] = np.maximum.accumulate(d)
        slopes[i] = loglog_slope(samp_t, dser[:, i])
        inc = np.array(fire_inc[i])
        if len(inc) >= 8:
            hlf = len(inc) // 2
            m = np.mod(inc[hlf:], 2 * np.pi)
            m = np.minimum(m, 2 * np.pi - m)
            dpstd[i] = np.std(m)
            ph = np.mod(np.cumsum(inc[hlf:]), 2 * np.pi)
            locks[i] = circular_concentration(ph)
    out = dict(a0=a0, e0=e0, kicks=kicks, dmax=dser[-1], Tb=Tb,
               rate=kicks / (horizon * T_ORB / Tb), wall=wall,
               param=param, rule=rule, WS=WS, horizon=horizon,
               slope=slopes, lock=locks, dphi_std=dpstd,
               samp_t=samp_t, dser=dser)
    return out


if __name__ == '__main__':
    outpath, rule, param = sys.argv[1], sys.argv[2], float(sys.argv[3])
    horizon = float(sys.argv[4]) if len(sys.argv) > 4 else 400.0
    WS = int(sys.argv[5]) if len(sys.argv) > 5 else 128
    nb = int(sys.argv[6]) if len(sys.argv) > 6 else 32
    res = run(rule, param, horizon=horizon, WS=WS, nbodies=nb)
    np.savez_compressed(outpath, **{k: v for k, v in res.items()
                                    if isinstance(v, np.ndarray)})
    sl = np.sort(res['slope'])
    dm = np.sort(res['dmax'])
    n = len(sl)
    print(f"{rule} param={param:g} H={horizon:g} WS={WS} wall={res['wall']:.1f}s "
          f"rate med={np.median(res['rate']):.2f}/orbit "
          f"D med={dm[n//2]:.2e} p90={dm[int(0.9*(n-1))]:.2e} "
          f"slope med={sl[n//2]:.3f} p90={sl[int(0.9*(n-1))]:.3f} "
          f"lock med={np.median(res['lock']):.2f} dphi med={np.median(res['dphi_std']):.3f}")
