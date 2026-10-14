#!/usr/bin/env python3
"""One machine, three cadence rules (the 524e-vs-54d9 discriminator).

Planar CRTBP, primary GM=1 at origin, parent mu=1e-3 on a circular orbit R=1
(54d9's scene, same 32 bodies, seed 20261011). Machine = 524e's: a shared fine
sensor of W windows per parent orbit; within each window the body drifts on
exact Kepler while the tide quadrature (GL4 along the drifted path) accrues in
a HELD accumulator; at a *flush* the whole accrued impulse is applied as one
velocity kick. Only the flush rule differs:

  A   clock:            every M windows                      (control, bounded)
  C   analytic gate:    first window >= t + theta*|a|/|adot| (54d9 C, walks)
  Q   impulse quantum:  first window where carry |sum dp|>=q (524e D, open)

Oracle: barycentric-rotation Jacobi (54d9's jacobi1). Per-body outputs:
  d(t)  running max of |C-C0|/|C0|, sampled every quarter parent orbit
  slope log-log slope of d(t) over the second half (0 bounded, 1 walk)
  rate  kicks per body-orbit
  lock  max_{k<=8} circular concentration of k*phi over fires in the last half
  dphi_std  std of per-fire synodic phase increments, last half (0 = locked)
phi = accumulated (n_body - n_parent)*(t_fire - t_last) mod 2pi at each fire.

Usage: harness.py OUT.npz RULE PARAM [horizon_orbits] [W] [nbodies]
  RULE in {A, C, Q}; PARAM = M | theta | q (SI-ish: impulse units of GM=1,R=1).
"""
import math
import sys
import time

import numpy as np

MU_P = 1e-3
NB = math.sqrt(1.0 + MU_P)          # parent mean motion (R = 1)
T_ORB = 2.0 * math.pi / NB
MUP = MU_P / (1.0 + MU_P)

_S30 = math.sqrt(30.0)
_GLX = np.array([0.5 - 0.5 * math.sqrt(3.0 / 7.0 + 2.0 / 7.0 * math.sqrt(6.0 / 5.0)),
                 0.5 + 0.5 * math.sqrt(3.0 / 7.0 + 2.0 / 7.0 * math.sqrt(6.0 / 5.0)),
                 0.5 - 0.5 * math.sqrt(3.0 / 7.0 - 2.0 / 7.0 * math.sqrt(6.0 / 5.0)),
                 0.5 + 0.5 * math.sqrt(3.0 / 7.0 - 2.0 / 7.0 * math.sqrt(6.0 / 5.0))])
_GLW = np.array([(18 + _S30) / 36, (18 + _S30) / 36,
                 (18 - _S30) / 36, (18 - _S30) / 36])


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
    """Exact Kepler advance by dt; returns x, y, vx, vy at t0+dt."""
    nb = a ** -1.5
    M = E0 - e * np.sin(E0) + nb * dt
    M = np.mod(M, 2.0 * np.pi)
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


def advance_E(a, e, E0, dt):
    nb = a ** -1.5
    M = np.mod(E0 - e * np.sin(E0) + nb * dt, 2.0 * np.pi)
    E = M.copy()
    for _ in range(10):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


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
    """Slope of log d vs log t over the second half (54d9's slope)."""
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
    ks = range(1, 9)
    best = 0.0
    for k in ks:
        z = np.mean(np.exp(1j * k * phi))
        best = max(best, abs(z))
    return best


def run(rule, param, horizon=400.0, W=64, nbodies=32, record_fires=True):
    x0, y0, vx0, vy0, a0, e0 = init_bodies(nbodies)
    a, e, E, om = elements_from_state(x0, y0, vx0, vy0)
    nb = a ** -1.5
    C0 = jacobi1(x0, y0, vx0, vy0, 0.0)
    dmax = np.zeros(nbodies)
    holdx = np.zeros(nbodies)
    holdy = np.zeros(nbodies)
    carry = np.zeros(nbodies)
    kicks = np.zeros(nbodies, dtype=np.int64)
    next_flush = np.ones(nbodies, dtype=np.int64)  # window index of next flush
    if rule == 'A':
        next_flush[:] = int(param)
    elif rule == 'C':
        next_flush[:] = max(1, W // 128)
    fires = [[] for _ in range(nbodies)]
    fire_ph_inc = [[] for _ in range(nbodies)]  # per-fire synodic phase increment
    last_fire_t = np.zeros(nbodies)
    dt_w = T_ORB / W
    nwin = int(round(horizon * W))
    samp_every = max(1, W // 4)
    nsamp = nwin // samp_every + 1
    dser = np.zeros((nsamp, nbodies))
    tser = np.zeros(nsamp)
    Tb = 2 * np.pi * a ** 1.5
    si = 0
    twall = time.time()
    for w in range(1, nwin + 1):
        t0w = (w - 1) * dt_w
        t = w * dt_w
        # --- sensor: GL4 tide quadrature along the drifted path ---
        px = np.zeros(nbodies)
        py = np.zeros(nbodies)
        for gx, gw in zip(_GLX, _GLW):
            tg = t0w + gx * dt_w
            sx, sy, _, _ = kepler_state(a, e, E, om, tg - t0w)
            gx_, gy_ = tide(sx, sy, tg)
            px += gw * gx_ * dt_w
            py += gw * gy_ * dt_w
        holdx += px
        holdy += py
        carry += np.hypot(px, py)
        # --- flush decision at window close ---
        if rule == 'A':
            fl = np.arange(nbodies) if (w % int(param)) == 0 else np.array([], dtype=int)
        elif rule == 'Q':
            fl = np.where(carry >= param)[0]
        elif rule == 'C':
            fl = np.where(w >= next_flush)[0]
        else:
            raise ValueError(rule)
        flmask = np.zeros(nbodies, dtype=bool)
        flmask[fl] = True
        # --- advance everyone to window close ---
        cx, cy, cvx, cvy = kepler_state(a, e, E, om, dt_w)
        if len(fl):
            cvx = cvx.copy()
            cvy = cvy.copy()
            cvx[fl] += holdx[fl]
            cvy[fl] += holdy[fl]
            holdx[fl] = 0.0
            holdy[fl] = 0.0
            carry[fl] = 0.0
            kicks[fl] += 1
            if record_fires:
                inc = nb[fl] * (t - last_fire_t[fl])
                for j, i in enumerate(fl):
                    fires[i].append(t)
                    fire_ph_inc[i].append(inc[j])
                last_fire_t[fl] = t
            # recompute elements for flushed bodies (epoch = window close)
            af, ef, _, omf = elements_from_state(cx[fl], cy[fl], cvx[fl], cvy[fl])
            r = np.hypot(cx[fl], cy[fl])
            rv = cx[fl] * cvx[fl] + cy[fl] * cvy[fl]
            a[fl] = af
            e[fl] = ef
            om[fl] = omf
            E[fl] = np.arctan2(rv / (ef * np.sqrt(af)), (1.0 - r / af) / ef)
            nb[fl] = af ** -1.5
            if rule == 'C':
                ax_, ay_ = tide(cx[fl], cy[fl], t)
                adx, ady = tide_dot(cx[fl], cy[fl], cvx[fl], cvy[fl], t)
                amag = np.hypot(ax_, ay_)
                admag = np.hypot(adx, ady)
                nu = param * amag / np.maximum(admag, 1e-18)
                nu = np.clip(nu, T_ORB / 1024.0, T_ORB / 4.0)
                next_flush[fl] = w + np.maximum(1, np.rint(nu / dt_w).astype(np.int64))
        if not flmask.all():
            E[~flmask] = advance_E(a[~flmask], e[~flmask], E[~flmask], dt_w)
        # --- sample the invariant ---
        if w % samp_every == 0:
            C = jacobi1(cx, cy, cvx, cvy, t)
            dcur = np.abs(C - C0) / np.abs(C0)
            dmax = np.maximum(dmax, dcur)
            if si < nsamp:
                dser[si] = dmax
                tser[si] = t
                si += 1
    out = dict(a0=a0, e0=e0, kicks=kicks, dmax=dmax,
               Tb=Tb, rate=kicks / (horizon * T_ORB / Tb),
               wall=time.time() - twall, param=param, rule=rule,
               W=W, horizon=horizon)
    slopes = np.zeros(nbodies)
    locks = np.zeros(nbodies)
    dpstd = np.zeros(nbodies)
    for i in range(nbodies):
        slopes[i] = loglog_slope(tser[:si], dser[:si, i])
        inc = np.array(fire_ph_inc[i])
        if len(inc) >= 8:
            h = len(inc) // 2
            inc2 = inc[h:]
            # unwrap-free: increments mod 2pi; lock => tiny std AND few phases
            m = np.mod(inc2, 2 * np.pi)
            m = np.minimum(m, 2 * np.pi - m)  # signed shortest
            dpstd[i] = np.std(m)
            # phase series from increments
            ph = np.mod(np.cumsum(inc[h:]), 2 * np.pi)
            locks[i] = circular_concentration(ph)
    out['slope'] = slopes
    out['lock'] = locks
    out['dphi_std'] = dpstd
    return out


if __name__ == '__main__':
    outpath, rule, param = sys.argv[1], sys.argv[2], float(sys.argv[3])
    horizon = float(sys.argv[4]) if len(sys.argv) > 4 else 400.0
    W = int(sys.argv[5]) if len(sys.argv) > 5 else 64
    nb = int(sys.argv[6]) if len(sys.argv) > 6 else 32
    res = run(rule, param, horizon=horizon, W=W, nbodies=nb)
    np.savez(outpath, **{k: v for k, v in res.items()
                         if isinstance(v, np.ndarray)})
    ok = np.isfinite(res['slope'])
    sl = np.sort(res['slope'])
    dm = np.sort(res['dmax'])
    n = len(sl)
    print(f"{rule} param={param:g} H={horizon:g} W={W} wall={res['wall']:.1f}s "
          f"rate med={np.median(res['rate']):.2f}/orbit "
          f"D med={dm[n//2]:.2e} p90={dm[int(0.9*(n-1))]:.2e} "
          f"slope med={sl[n//2]:.3f} p90={sl[int(0.9*(n-1))]:.3f} "
          f"lock med={np.median(res['lock']):.2f} dphi med={np.median(res['dphi_std']):.3f}")
