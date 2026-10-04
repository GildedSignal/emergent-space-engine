#!/usr/bin/env python3
"""Element-decorrelation geography of the planar CR3BP (the plane's fleet scene).

Barycentric CR3BP: primary mass 1, secondary mass mu at separation 1,
n = sqrt(1+mu). Test bodies on orbits of semi-major axis a about the primary.

Each body carries a twin at full-state separation eps. We renormalize the
separation to eps whenever it exceeds 1e-4 (linear regime) and track the
ELEMENT separation d_el = sqrt(da^2 + (a*de)^2) of osculating (a, e).
Decorrelation time T_d = first orbit index at which d_el > theta = 1e-3*a.

Rationale: the engine derives phase from compiled cycles (phase shear is
free); only unpredictability in the ACTIONS (a, e) forces kick work.
Regular orbits: d_el bounded (no crossing). Chaotic: exponential growth.

RK4, drift control via Jacobi constant. Deaths (escape >4, close <0.03)
count as decorrelation at death time.
"""
import json
import sys
import numpy as np

def rhs_acc(t, pos, mu, n):
    ang = n * t[:, 0]
    cs, sn = np.cos(ang), np.sin(ang)
    d1 = pos - np.stack([-mu * cs, -mu * sn], axis=1)
    d2 = pos - np.stack([(1.0 - mu) * cs, (1.0 - mu) * sn], axis=1)
    s1 = np.hypot(d1[:, 0], d1[:, 1])
    s2 = np.hypot(d2[:, 0], d2[:, 1])
    return -d1 / s1[:, None]**3 - mu * d2 / s2[:, None]**3

def deriv4(t, y, mu, n):
    return np.concatenate([y[:, 2:4], rhs_acc(t, y[:, 0:2], mu, n)], axis=1)

def elements(y, t, mu, n):
    """Osculating (a, e) about the primary."""
    ang = n * t[:, 0]
    cs, sn = np.cos(ang), np.sin(ang)
    r1p = np.stack([-mu * cs, -mu * sn], axis=1)
    v1p = np.stack([mu * n * sn, -mu * n * cs], axis=1)
    rel = y[:, 0:2] - r1p
    vrel = y[:, 2:4] - v1p
    r = np.hypot(rel[:, 0], rel[:, 1])
    v2 = (vrel**2).sum(axis=1)
    energy = 0.5 * v2 - 1.0 / r
    a = -1.0 / (2.0 * energy)
    h = rel[:, 0] * vrel[:, 1] - rel[:, 1] * vrel[:, 0]
    e = np.sqrt(np.maximum(0.0, 1.0 - h**2 / a))
    return a, e

def run(mu, shells, e_vals, n_phase, n_orbits, steps_per_orbit,
        seed=7, prefix=None, eps=1e-9, cap=1e-4, theta=1e-3):
    rng = np.random.default_rng(seed)
    n = np.sqrt(1.0 + mu)
    bodies = []
    for a in shells:
        for e in e_vals:
            for ph in rng.uniform(0, 2 * np.pi, n_phase):
                bodies.append((a, e, ph))
    bodies = np.array(bodies)
    a0, ecc0, f = bodies[:, 0], bodies[:, 1], bodies[:, 2]
    N = len(bodies)
    p_ = a0 * (1 - ecc0**2)
    r = p_ / (1 + ecc0 * np.cos(f))
    hh = np.sqrt(p_)
    vr = ecc0 * np.sin(f) / hh
    vt = hh / r
    pos = np.stack([r * np.cos(f) - mu, r * np.sin(f)], axis=1)
    vel = np.stack([vr * np.cos(f) - vt * np.sin(f),
                    vr * np.sin(f) + vt * np.cos(f) - mu * n], axis=1)
    yA = np.concatenate([pos, vel], axis=1)
    d0 = rng.normal(size=(N, 4))
    d0 /= np.linalg.norm(d0, axis=1)[:, None]
    scale = np.concatenate([np.abs(yA[:, 0:2]).max(axis=1)[:, None],
                            np.abs(yA[:, 2:4]).max(axis=1)[:, None]], axis=1)
    yB = yA + eps * d0 * np.concatenate([scale, scale], axis=1)
    P = 2 * np.pi * a0**1.5
    dt = (P / steps_per_orbit)[:, None]
    t = np.zeros((2 * N, 1))
    Y = np.concatenate([yA, yB], axis=0)
    DT = np.concatenate([dt, dt], axis=0)
    aA0, eA0 = elements(Y[:N], t[:N], mu, n)
    Td = np.full(N, np.inf)      # decorrelation orbit (element threshold)
    deadA = np.zeros(N, bool)
    deadT = np.full(N, np.nan)
    nren = np.zeros(N)
    a_ref = a0.copy()
    nsteps = n_orbits * steps_per_orbit
    def jacobi(Y):
        ang = n * t[:, 0]
        cs, sn = np.cos(ang), np.sin(ang)
        s1 = np.hypot(*(Y[:, 0:2] - np.stack([-mu * cs, -mu * sn], axis=1)).T)
        s2 = np.hypot(*(Y[:, 0:2] - np.stack([(1 - mu) * cs, (1 - mu) * sn], axis=1)).T)
        vrot = Y[:, 2:4] + np.stack([n * Y[:, 1], -n * Y[:, 0]], axis=1)
        return n**2 * (Y[:, 0:2]**2).sum(axis=1) + 2 / s1 + 2 * mu / s2 \
            - (vrot**2).sum(axis=1)
    CJ0 = jacobi(Y)
    for k in range(nsteps):
        k1 = deriv4(t, Y, mu, n)
        k2 = deriv4(t + 0.5 * DT, Y + 0.5 * DT * k1, mu, n)
        k3 = deriv4(t + 0.5 * DT, Y + 0.5 * DT * k2, mu, n)
        k4 = deriv4(t + DT, Y + DT * k3, mu, n)
        Y = Y + (DT / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + DT
        if (k + 1) % steps_per_orbit == 0:
            orb = (k + 1) // steps_per_orbit
            aA, eA = elements(Y[:N], t[:N], mu, n)
            aB, eB = elements(Y[N:], t[N:], mu, n)
            d_el = np.hypot(aA - aB, a_ref * (eA - eB))
            cross = np.isinf(Td) & (d_el > theta * a_ref) & ~deadA
            Td[cross] = orb
            ang = n * t[:N, 0]
            cs, sn = np.cos(ang), np.sin(ang)
            rs = np.stack([(1 - mu) * cs, (1 - mu) * sn], axis=1)
            bad = (np.hypot(Y[:N, 0], Y[:N, 1]) > 4.0) | \
                  (np.hypot(*(Y[:N, 0:2] - rs).T) < 0.03)
            newly = bad & ~deadA
            if newly.any():
                deadA |= bad
                deadT[bad] = orb
                Td[bad & np.isinf(Td)] = orb  # death = full decorrelation
        # renormalize twin separation to eps (only pairs still both alive)
        d = Y[N:] - Y[:N]
        dn = np.linalg.norm(d / np.concatenate([scale, scale], axis=1), axis=1)
        ren = dn > cap / eps
        if ren.any():
            alive_pair = ~deadA
            ren &= alive_pair
            nren[ren] += 1
            g = np.where(dn > 0, eps / np.maximum(dn, 1e-300), 1.0)[:, None]
            Y[N:][ren] = Y[:N][ren] + (d * g)[ren]
    CJ1 = jacobi(Y)
    dCJ = np.abs(CJ1 - CJ0) / np.abs(CJ0)
    out = dict(mu=mu, n_orbits=n_orbits, steps=steps_per_orbit,
               dead_fraction=float(deadA.mean()),
               dCJ_median=float(np.median(dCJ[:N])))
    rows = []
    TdF = np.where(np.isinf(Td), n_orbits + 1, Td)
    for a in shells:
        for e in e_vals:
            sel = (bodies[:, 0] == a) & (bodies[:, 1] == e)
            Td_sel = TdF[sel]
            rows.append(dict(a=float(a), e=float(e), n=int(sel.sum()),
                             frac_dec=float((Td_sel <= n_orbits).mean()),
                             Td_med=float(np.median(Td_sel)),
                             Td_min=float(Td_sel.min()),
                             frac_dead=float(deadA[sel].mean()),
                             nren_med=float(np.median(nren[sel]))))
    out['rows'] = rows
    out['frac_deco_all'] = float((TdF <= n_orbits).mean())
    prefix = prefix if prefix is not None else sys.argv[2]
    np.savez(prefix + '.npz', bodies=bodies, Td=TdF, deadA=deadA, deadT=deadT, nren=nren)
    with open(prefix + '.json', 'w') as fo:
        json.dump(out, fo)
    print(json.dumps({k: v for k, v in out.items() if k != 'rows'}))

if __name__ == '__main__':
    mode = sys.argv[1]
    shells = np.round(np.arange(0.30, 0.8501, 0.025), 4)
    if mode == 'main':
        run(0.0123, shells, [0.0, 0.05, 0.20], 12, 120, 128, prefix='main')
    elif mode == 'floor':
        run(0.0123 / 1000.0, shells, [0.0, 0.05, 0.20], 12, 120, 128, prefix='floor')
    elif mode == 'sweep':
        for mu in [1e-4, 1e-3, 3e-2]:
            run(mu, shells, [0.05], 10, 100, 128, prefix=f'sweep{mu}')
    elif mode == 'heldout':
        for mu in [0.05, 0.10]:
            run(mu, shells, [0.05], 10, 100, 128, prefix=f'held{mu}')
    elif mode == 'step':
        run(0.0123, np.round(np.arange(0.40, 0.8001, 0.05), 4), [0.05], 8, 100, 256, prefix='step256')
        run(0.0123, np.round(np.arange(0.40, 0.8001, 0.05), 4), [0.05], 8, 100, 128, prefix='step128')
