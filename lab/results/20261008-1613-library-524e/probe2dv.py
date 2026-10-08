#!/usr/bin/env python3
"""Probe 2b: impulse-quantum trigger (delta-hedge cadence).

Grid machine, one stacked Kepler drift per window for ALL members (a member's
velocity changes only at its own fires, and drift state is carried per member):

  per window w:
    - GL8 quadrature of g along the drift (8 evals/member; sensor = quadrature)
    - imp_acc[member] += window impulse vector   (HELD, not applied)
    - s_acc[member]  += ||window impulse||       (total variation)
    - fire when s_acc >= Q2 = c2 * (mu_p/R^3) * (2*pi/n_p):
        v += imp_acc  (the whole open interval's impulse, applied at fire),
        imp_acc = 0, s_acc = 0
  last window: everyone flushes (held impulse applied, counted as a kick).

Clock law U of probe2 = this with Q2 <= per-window variation (fires always).
"""
import json, sys
import numpy as np
from probe2 import (g_many, kepler_rhs, gl_nodes, elements, truth_els,
                    belt_make, solve_ivp)

def run_dv(cfg, belt, T, nW, c2):
    n = len(belt)
    Q2 = c2 * cfg['mu_p']/cfg['R']**3 * (2*np.pi/cfg['n_p'])
    W = T/nW
    evals = 0; kicks = 0
    rs = np.array([s[0] for s in belt]); vs = np.array([s[1] for s in belt])
    imp_acc = np.zeros((n, 3)); s_acc = np.zeros(n)
    for w in range(nW):
        t0, t1 = w*W, (w+1)*W
        xs, ws = gl_nodes(t0, t1)
        y0 = np.concatenate([rs.ravel(), vs.ravel()])
        sol = solve_ivp(kepler_rhs, (t0, t1), y0, method='DOP853',
                        rtol=1e-11, atol=1e-13, dense_output=True)
        acc = np.zeros((n, 3))
        for x, wt in zip(xs, ws):
            Y = sol.sol(x); rr = Y[:3*n].reshape(n, 3)
            acc += wt * g_many(cfg, rr, x); evals += n
        imp_acc += acc
        s_acc += np.linalg.norm(acc, axis=1)
        Y1 = sol.sol(t1)
        rs = Y1[:3*n].reshape(n, 3); vs = Y1[3*n:].reshape(n, 3)
        fire = (s_acc >= Q2) | (w == nW - 1)
        vs[fire] += imp_acc[fire]
        imp_acc[fire] = 0.0; s_acc[fire] = 0.0
        kicks += int(fire.sum())
    return list(zip(rs, vs)), kicks, evals

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
    e_ref = np.array([b[3] for b in belt])
    ETR = truth_els(cfg, belt_s, T)
    res = dict(config=which, mode='dv', cfg={k: float(v) for k, v in cfg.items()},
               T=T, runs=[])
    def score(final):
        E = np.array([elements(r, v) for r, v in final])
        de = np.abs(E[:, 1] - ETR[:, 1])
        dwp = np.abs(np.angle(np.exp(1j*(E[:, 2] - ETR[:, 2]))))
        return de, dwp
    for nW in [32, 64]:
        for c2 in [0.05, 0.15, 0.45, 1.35, 4.0, 12.0]:
            fin, kicks, evals = run_dv(cfg, belt_s, T, nW, c2)
            de, dwp = score(fin)
            r = dict(law='D', nW=nW, c_q=c2, kicks=int(kicks), evals=int(evals),
                     p95_de=float(np.percentile(de, 95)), med_de=float(np.median(de)),
                     p95_dwp=float(np.percentile(dwp, 95)),
                     sub_e06_p95=float(np.percentile(de[e_ref >= 0.4], 95)),
                     sub_e005_med=float(np.median(de[e_ref <= 0.1])))
            res['runs'].append(r); print('D', nW, c2, r)
    with open(f'probe2d_{which}.json', 'w') as f:
        json.dump(res, f, indent=1)
