#!/usr/bin/env python3
"""Probe: kick cadence law for the tide layer.

Setting (circular restricted 3-body, primary-centered frame):
  a(r,t) = -r/|r|^3  +  g(r,t)
  g(r,t) = mu_p * [ (r_p(t)-r)/|r_p(t)-r|^3 - r_p(t)/|r_p(t)|^3 ]
  r_p(t) = R*(cos n_p t, sin n_p t cos i, sin n_p t sin i), n_p = sqrt((1+mu_p)/R^3)

Truth: full ODE, DOP853 rtol 1e-12 (checked against 1e-13).
Cheap path (both laws share identical per-kick machinery):
  Kepler drift between kicks (DOP853 on -r/|r|^3 only, dense output),
  impulse = 8-pt Gauss-Legendre integral of g along the Kepler path,
  velocity jump at kick time.

Law U (clock): kicks every T/K.
Law T (threshold): sensor windows of length W; kick at the first GL node
  where ||g(r(t),t) - g_last|| >= Q = c * (mu_p/R^3)  (dimensionless c).

Work unit = number of g evaluations (the engine's dominant per-kick cost).
"""
import json, sys, time
import numpy as np
from scipy.integrate import solve_ivp

GL_X, GL_W = np.polynomial.legendre.leggauss(8)

def rp_of(cfg, t):
    n_p, R, ci, si = cfg['n_p'], cfg['R'], cfg['ci'], cfg['si']
    return np.array([R*np.cos(n_p*t), R*np.sin(n_p*t)*ci, R*np.sin(n_p*t)*si])

def g_of(cfg, r, t):
    rp = rp_of(cfg, t)
    d = rp - r
    return cfg['mu_p'] * (d/np.linalg.norm(d)**3 - rp/np.linalg.norm(rp)**3)

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
        gs = np.array([g_of(cfg, r[i], t) for i in range(n)])
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

def truth(cfg, belt, T, rtol=1e-12):
    n = len(belt)
    y0 = np.concatenate([s[0] for s in belt] + [s[1] for s in belt])
    sol = solve_ivp(full_rhs(cfg), (0.0, T), y0, method='DOP853', rtol=rtol,
                    atol=1e-14, t_eval=[T])
    y = sol.y[:, -1]
    return [(y[:3*n][3*i:3*i+3], y[3*n:][3*i:3*i+3]) for i in range(n)]

def run_uniform(cfg, belt, T, K):
    n = len(belt); evals = 0; kicks = 0
    rs = np.array([s[0] for s in belt]); vs = np.array([s[1] for s in belt])
    dt = T/K
    for k in range(K):
        t0, t1 = k*dt, (k+1)*dt
        y0 = np.concatenate([rs.ravel(), vs.ravel()])
        sol = solve_ivp(kepler_rhs, (t0, t1), y0, method='DOP853',
                        rtol=1e-11, atol=1e-13, dense_output=True)
        xs, ws = gl_nodes(t0, t1)
        dv = np.zeros((n, 3))
        for x, w in zip(xs, ws):
            Y = sol.sol(x); rr = Y[:3*n].reshape(n, 3)
            for i in range(n):
                dv[i] += w * g_of(cfg, rr[i], x)
            evals += n
        Y1 = sol.sol(t1)
        rs = Y1[:3*n].reshape(n, 3); vs = Y1[3*n:].reshape(n, 3) + dv
        kicks += n
    return list(zip(rs, vs)), kicks, evals

def run_threshold(cfg, belt, T, c_q, W):
    evals = 0; kicks = 0
    Q = c_q * cfg['mu_p']/cfg['R']**3
    out = []
    for s in belt:
        r, v = s[0].copy(), s[1].copy(); t = 0.0
        g_last = g_of(cfg, r, t); evals += 1
        while t < T - 1e-12:
            t_seg = min(t + 8*W, T)
            y0 = np.concatenate([r, v])
            sol = solve_ivp(kepler_rhs, (t, t_seg), y0, method='DOP853',
                            rtol=1e-11, atol=1e-13, dense_output=True)
            fired = False; w_t = t
            while w_t < t_seg - 1e-12:
                w1 = min(w_t + W, T)
                xs, ws = gl_nodes(w_t, w1)
                for x in xs:
                    Y = sol.sol(x)
                    if np.linalg.norm(g_of(cfg, Y[:3], x) - g_last) >= Q:
                        evals += 1
                        t_fire = x
                        xs2, ws2 = gl_nodes(t, t_fire)
                        dv = np.zeros(3)
                        for x2, w2 in zip(xs2, ws2):
                            dv += w2 * g_of(cfg, sol.sol(x2)[:3], x2); evals += 1
                        Yf = sol.sol(t_fire)
                        r, v = Yf[:3], Yf[3:] + dv
                        t = t_fire; g_last = g_of(cfg, r, t); evals += 1
                        kicks += 1; fired = True
                        break
                    evals += 1
                if fired:
                    break
                w_t = w1
                if w_t >= T - 1e-12:  # final flush at T
                    xs2, ws2 = gl_nodes(t, T)
                    dv = np.zeros(3)
                    for x2, w2 in zip(xs2, ws2):
                        dv += w2 * g_of(cfg, sol.sol(x2)[:3], x2); evals += 1
                    Yf = sol.sol(T)
                    r, v = Yf[:3], Yf[3:] + dv
                    t = T
            if not fired:  # no trigger in this segment: pure drift, continue
                Y = sol.sol(t_seg)
                r, v = Y[:3], Y[3:]
                t = t_seg
        out.append((r, v))
    return out, kicks, evals

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
    elif which == 'B':  # held-out: inclined perturber
        cfg = dict(mu_p=1e-3, R=4.0, ci=np.cos(np.pi/6), si=np.sin(np.pi/6))
    else:               # held-out: heavier, closer perturber
        cfg = dict(mu_p=3e-3, R=3.0, ci=1.0, si=0.0)
    cfg['n_p'] = np.sqrt((1+cfg['mu_p'])/cfg['R']**3)
    T = 100.0
    belt = belt_make(rng)
    belt_s = [(b[0], b[1]) for b in belt]
    e_ref = np.array([b[3] for b in belt]); a_ref = np.array([b[2] for b in belt])

    t0 = time.time()
    ETR = np.array([elements(r, v) for r, v in truth(cfg, belt_s, T)])
    ETRv = np.array([elements(r, v) for r, v in truth(cfg, belt_s, T, rtol=1e-13)])
    ctrl_e = float(np.max(np.abs(ETR[:, 1] - ETRv[:, 1])))
    res = dict(config=which, cfg={k: float(v) for k, v in cfg.items()}, T=T,
               truth_control_max_de=ctrl_e, runs=[])
    print(f"[{which}] truth control max|de| (rtol 1e-12 vs 1e-13): {ctrl_e:.2e}")

    def score(final):
        E = np.array([elements(r, v) for r, v in final])
        de = np.abs(E[:, 1] - ETR[:, 1])
        da = np.abs(E[:, 0] - ETR[:, 0])/a_ref
        dwp = np.abs(np.angle(np.exp(1j*(E[:, 2] - ETR[:, 2]))))
        return de, da, dwp

    # positive control: converged clock scheme must approach truth
    fin, kicks, evals = run_uniform(cfg, belt_s, T, 1536)
    de, da, dwp = score(fin)
    print(f"[{which}] positive control U K=1536: p95 de={np.percentile(de,95):.2e}")
    res['control_U1536_p95_de'] = float(np.percentile(de, 95))

    for K in [12, 24, 48, 96, 192, 384]:
        fin, kicks, evals = run_uniform(cfg, belt_s, T, K)
        de, da, dwp = score(fin)
        r = dict(law='U', K=K, kicks=int(kicks), evals=int(evals),
                 p95_de=float(np.percentile(de, 95)), med_de=float(np.median(de)),
                 p95_dwp=float(np.percentile(dwp, 95)),
                 sub_e06_p95=float(np.percentile(de[e_ref >= 0.4], 95)),
                 sub_e005_med=float(np.median(de[e_ref <= 0.1])))
        res['runs'].append(r); print('U', K, r)
    W = T/64.0
    for cq in [0.05, 0.15, 0.45, 1.35, 4.0]:
        fin, kicks, evals = run_threshold(cfg, belt_s, T, cq, W)
        de, da, dwp = score(fin)
        r = dict(law='T', c_q=cq, kicks=int(kicks), evals=int(evals),
                 p95_de=float(np.percentile(de, 95)), med_de=float(np.median(de)),
                 p95_dwp=float(np.percentile(dwp, 95)),
                 sub_e06_p95=float(np.percentile(de[e_ref >= 0.4], 95)),
                 sub_e005_med=float(np.median(de[e_ref <= 0.1])))
        res['runs'].append(r); print('T', cq, r)
    res['wall_s'] = time.time() - t0
    with open(f'probe_{which}.json', 'w') as f:
        json.dump(res, f, indent=1)
    print('wall', res['wall_s'])
