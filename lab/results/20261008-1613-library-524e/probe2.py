#!/usr/bin/env python3
"""Probe 2: window-quantized error-quantum cadence (batched, fast).

Same setting as probe.py (CRTBP primary-centered, DOP853 truth rtol 1e-12).

One shared machine for both laws on a sensor grid of nW windows (length W):
  per window, per open group (particles sharing an interval start):
    - Kepler drift over the window (stacked DOP853, dense)
    - g evaluated at the window's 8 Gauss-Legendre nodes  (8 evals/member)
    - each member accumulates impulse  sum_j w_j g(node_j)
    - member FIRES at window end if max_j ||g(node_j) - g_open|| >= Q:
        v += accumulated impulse (covers its whole open interval),
        it reopens a fresh interval (g_open = g at window end, impulse = 0)
  at T, still-open members flush their accumulated impulse (counted as kicks).

Law U (clock)  = this machine with Q = 0 and one window per interval (K = nW):
  every member fires at every window end.  Same node evals per window.
Law T (quantum): Q = c * mu_p/R^3, sensor grid nW in {32, 64}.

Work unit: g evaluations (8 per member per window for both laws).
Kicks: interval closures (fires + final flush).
"""
import json, sys, time
import numpy as np
from scipy.integrate import solve_ivp

GL_X, GL_W = np.polynomial.legendre.leggauss(8)

def rp_of(cfg, t):
    n_p, R, ci, si = cfg['n_p'], cfg['R'], cfg['ci'], cfg['si']
    return np.array([R*np.cos(n_p*t), R*np.sin(n_p*t)*ci, R*np.sin(n_p*t)*si])

def g_many(cfg, Rs, t):
    rp = rp_of(cfg, t)
    d = rp[None, :] - Rs                       # (m,3)
    return cfg['mu_p'] * (d/np.linalg.norm(d, axis=1)[:, None]**3
                          - rp/np.linalg.norm(rp)**3)

def kepler_rhs(t, y):
    n = y.size // 6
    r, v = y[:3*n].reshape(n, 3), y[3*n:].reshape(n, 3)
    an = -r / np.linalg.norm(r, axis=1)[:, None]**3
    return np.concatenate([v.ravel(), an.ravel()])

def full_rhs(cfg):
    def f(t, y):
        n = y.size // 6
        r, v = y[:3*n].reshape(n, 3), y[3*n:].reshape(n, 3)
        an = -r / np.linalg.norm(r, axis=1)[:, None]**3
        gs = g_many(cfg, r, t)
        return np.concatenate([v.ravel(), (an + gs).ravel()])
    return f

def gl_nodes(t0, t1):
    m, h = 0.5*(t0+t1), 0.5*(t1-t0)
    return m + h*GL_X, h*GL_W

def elements(r, v):
    rn, vn2 = np.linalg.norm(r), v @ v
    a = 1.0/(2.0/rn - vn2)
    ev = (vn2 - 1.0/rn)*r - (r @ v)*v
    e = np.linalg.norm(ev)
    varpi = np.arctan2(ev[1], ev[0]) if e > 1e-9 else 0.0
    return a, e, varpi

def truth_els(cfg, belt, T, rtol=1e-12):
    n = len(belt)
    y0 = np.concatenate([s[0] for s in belt] + [s[1] for s in belt])
    sol = solve_ivp(full_rhs(cfg), (0.0, T), y0, method='DOP853', rtol=rtol,
                    atol=1e-14, t_eval=[T])
    y = sol.y[:, -1]
    return np.array([elements(y[:3*n][3*i:3*i+3], y[3*n:][3*i:3*i+3])
                     for i in range(n)])

def run_grid(cfg, belt, T, nW, c_q, mode='dg'):
    """Clock law: pass c_q = None (every member fires every window)."""
    n = len(belt)
    Q = None if c_q is None else c_q * cfg['mu_p']/cfg['R']**3
    W = T/nW
    evals = 0; kicks = 0
    idx = np.arange(n)
    rs = np.array([s[0] for s in belt]); vs = np.array([s[1] for s in belt])
    g_open = g_many(cfg, rs, 0.0); evals += n
    groups = {0: (idx, g_open, np.zeros((n, 3)))}   # key: window idx of open
    out_r = np.zeros((n, 3)); out_v = np.zeros((n, 3)); done = np.zeros(n, bool)
    for w in range(nW):
        t0, t1 = w*W, (w+1)*W
        xs, ws = gl_nodes(t0, t1)
        new_groups = {}
        for key in sorted(groups):
            members, g_o, imp = groups[key]
            m = len(members)
            y0 = np.concatenate([rs[members].ravel(), vs[members].ravel()])
            sol = solve_ivp(kepler_rhs, (t0, t1), y0, method='DOP853',
                            rtol=1e-11, atol=1e-13, dense_output=True)
            acc = np.zeros((m, 3))
            fire = np.zeros(m, bool)
            for x, wt in zip(xs, ws):
                Y = sol.sol(x); rr = Y[:3*m].reshape(m, 3)
                gv = g_many(cfg, rr, x); evals += m
                acc += wt * gv
                if Q is not None:
                    fire |= np.linalg.norm(gv - g_o, axis=1) >= Q
            imp = imp + acc
            Y1 = sol.sol(t1)
            rs[members] = Y1[:3*m].reshape(m, 3)
            vs[members] = Y1[3*m:].reshape(m, 3)
            if Q is None:
                fire = np.ones(m, bool)
            if fire.any() or w == nW - 1:
                sel = members[fire | (w == nW-1)]
                vs[sel] += imp[fire | (w == nW-1)]
                kicks += int((fire | (w == nW-1)).sum())
                done[sel] = True
                out_r[sel] = rs[sel]; out_v[sel] = vs[sel]
            stay = ~fire if w < nW - 1 else np.zeros(m, bool)
            if stay.any():
                keep = members[stay]
                if (w+1) in new_groups:
                    i2, g2, im2 = new_groups[w+1]
                    new_groups[w+1] = (np.concatenate([i2, keep]),
                                       np.concatenate([g2, g_o[stay]]),
                                       np.concatenate([im2, imp[stay]]))
                else:
                    new_groups[w+1] = (keep, g_o[stay].copy(), imp[stay].copy())
            if fire.any() and w < nW - 1:
                reopen = members[fire]
                gnew = g_many(cfg, rs[reopen], t1); evals += len(reopen)
                if (w+1) in new_groups:
                    i2, g2, im2 = new_groups[w+1]
                    new_groups[w+1] = (np.concatenate([i2, reopen]),
                                       np.concatenate([g2, gnew]),
                                       np.concatenate([im2, np.zeros((len(reopen), 3))]))
                else:
                    new_groups[w+1] = (reopen, gnew, np.zeros((len(reopen), 3)))
        groups = new_groups
        if not groups:
            break
    return list(zip(out_r, out_v)), kicks, evals

def belt_make(rng):
    belt = []
    for a in [0.8, 1.2, 1.6, 2.0]:
        for e in [0.05, 0.2, 0.4, 0.6]:
            for _ in range(3):
                varpi, M0 = rng.uniform(0, 2*np.pi), rng.uniform(0, 2*np.pi)
                r0 = a*(np.cos(M0) - e); rf = a*np.sqrt(1-e*e)*np.sin(M0)
                v0 = -np.sin(M0)/(a*(1-e*np.cos(M0)))
                vf = np.sqrt(1-e*e)*np.cos(M0)/(a*(1-e*np.cos(M0)))
                cf, sf = np.cos(varpi), np.sin(varpi)
                belt.append((np.array([cf*r0 - sf*rf, sf*r0 + cf*rf, 0.0]),
                             np.array([cf*v0 - sf*vf, sf*v0 + cf*vf, 0.0]), a, e))
    return belt

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'A'
    rng = np.random.default_rng(42)
    if which == 'A':
        cfg = dict(mu_p=1e-3, R=4.0, ci=1.0, si=0.0)
    elif which == 'B':
        cfg = dict(mu_p=1e-3, R=4.0, ci=np.cos(np.pi/6), si=np.sin(np.pi/6))
    else:
        cfg = dict(mu_p=3e-3, R=3.0, ci=1.0, si=0.0)
    cfg['n_p'] = np.sqrt((1+cfg['mu_p'])/cfg['R']**3)
    T = 100.0
    belt = belt_make(rng)
    belt_s = [(b[0], b[1]) for b in belt]
    e_ref = np.array([b[3] for b in belt]); a_ref = np.array([b[2] for b in belt])

    t0 = time.time()
    ETR = truth_els(cfg, belt_s, T)
    ETRv = truth_els(cfg, belt_s, T, rtol=1e-13)
    ctrl = float(np.max(np.abs(ETR[:, 1] - ETRv[:, 1])))
    res = dict(config=which, cfg={k: float(v) for k, v in cfg.items()}, T=T,
               truth_control_max_de=ctrl, runs=[])
    print(f"[{which}] truth control max|de|: {ctrl:.2e}")

    def score(final):
        E = np.array([elements(r, v) for r, v in final])
        de = np.abs(E[:, 1] - ETR[:, 1])
        dwp = np.abs(np.angle(np.exp(1j*(E[:, 2] - ETR[:, 2]))))
        return de, dwp

    for nW in [12, 24, 48, 96, 192]:
        fin, kicks, evals = run_grid(cfg, belt_s, T, nW, None)
        de, dwp = score(fin)
        r = dict(law='U', nW=nW, kicks=int(kicks), evals=int(evals),
                 p95_de=float(np.percentile(de, 95)), med_de=float(np.median(de)),
                 p95_dwp=float(np.percentile(dwp, 95)),
                 sub_e06_p95=float(np.percentile(de[e_ref >= 0.4], 95)),
                 sub_e005_med=float(np.median(de[e_ref <= 0.1])))
        res['runs'].append(r); print('U', nW, r)
    for nW in [32, 64]:
        for cq in [0.05, 0.15, 0.45, 1.35, 4.0, 12.0]:
            fin, kicks, evals = run_grid(cfg, belt_s, T, nW, cq)
            de, dwp = score(fin)
            r = dict(law='T', nW=nW, c_q=cq, kicks=int(kicks), evals=int(evals),
                     p95_de=float(np.percentile(de, 95)), med_de=float(np.median(de)),
                     p95_dwp=float(np.percentile(dwp, 95)),
                     sub_e06_p95=float(np.percentile(de[e_ref >= 0.4], 95)),
                     sub_e005_med=float(np.median(de[e_ref <= 0.1])))
            res['runs'].append(r); print('T', nW, cq, r)
    res['wall_s'] = time.time() - t0
    with open(f'probe2_{which}.json', 'w') as f:
        json.dump(res, f, indent=1)
    print('wall', res['wall_s'])
