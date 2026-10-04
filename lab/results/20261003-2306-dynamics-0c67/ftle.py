#!/usr/bin/env python3
"""FTLE geography of the planar circular restricted 3-body problem (belt regime).

Plane's scene: parent (mass 1) + secondary (mass mu) on a circular orbit r=1,
test bodies (the fleet/belt) at a/a_sec in [0.30, 0.85].

Per body: RK4 on state + tangent (variational), per-body dt = P_body/steps.
Renormalized-deviation FTLE (Benettin), renorm every 2 steps (shear floor
(sP)^2/(2R), R=64/orbit -> ~0.018). A near-regular control at mu/1000 gives
the integrable floor per (a,e); excess lambda classifies chaos.

Outputs JSON: per-(shell,e) stats, windowed lambda traces summary, fractions.
"""
import json
import sys
import numpy as np

def rhs(t, pos, vel, mu, n):
    """acc and Jacobian dacc/dr, barycentric CR3BP, inertial frame.
    Primary (mass 1) at -mu*(cos nt, sin nt); secondary (mass mu) at
    (1-mu)*(cos nt, sin nt); n^2 = 1+mu."""
    ang = n * t[:, 0]
    cs, sn = np.cos(ang), np.sin(ang)
    r1p = np.stack([-mu * cs, -mu * sn], axis=1)
    r2p = np.stack([(1.0 - mu) * cs, (1.0 - mu) * sn], axis=1)
    d1 = pos - r1p
    s1 = np.hypot(d1[:, 0], d1[:, 1])
    inv1 = 1.0 / s1**3
    d2 = pos - r2p
    s2 = np.hypot(d2[:, 0], d2[:, 1])
    inv2 = 1.0 / s2**3
    a = -d1 * inv1[:, None] - mu * d2 * inv2[:, None]
    I2 = np.eye(2)[None]
    D = -(I2 * inv1[:, None, None]
          - 3.0 * inv1[:, None, None]**2 * d1[:, :, None] * d1[:, None, :]) \
        - mu * (I2 * inv2[:, None, None]
                - 3.0 * inv2[:, None, None]**2 * d2[:, :, None] * d2[:, None, :])
    return a, D

def deriv(t, y, mu, n):
    """y: (N, 8) = x,y,vx,vy,dx,dy,dvx,dvy -> (N, 8)."""
    pos, vel, dr, dv = y[:, 0:2], y[:, 2:4], y[:, 4:6], y[:, 6:8]
    a, D = rhs(t, pos, vel, mu, n)
    dadv = np.einsum('nij,nj->ni', D, dr)
    return np.concatenate([vel, a, dv, dadv], axis=1)

def run(mu, shells, e_vals, n_phase, n_orbits, steps_per_orbit,
        renorm_every=2, seed=7, prefix=None):
    rng = np.random.default_rng(seed)
    n = np.sqrt(1.0 + mu)
    bodies = []  # (shell a, e, phase)
    for a in shells:
        for e in e_vals:
            for ph in rng.uniform(0, 2 * np.pi, n_phase):
                bodies.append((a, e, ph))
    bodies = np.array(bodies)
    a0, ecc0, ph0 = bodies[:, 0], bodies[:, 1], bodies[:, 2]
    N = len(bodies)
    # two-body IC at true anomaly f = ph0, periapsis along +x
    f = ph0
    p = a0 * (1 - ecc0**2)
    r = p / (1 + ecc0 * np.cos(f))
    pos = np.stack([r * np.cos(f) - mu, r * np.sin(f)], axis=1)  # primary at (-mu,0)
    h = np.sqrt(1.0 * p)  # GM=1
    vr = (1.0 / h) * ecc0 * np.sin(f)
    vt = h / r
    vel = np.stack([vr * np.cos(f) - vt * np.sin(f),
                    vr * np.sin(f) + vt * np.cos(f) - mu * n], axis=1)
    # tangent: unit deviation vector
    tan0 = rng.normal(size=(N, 4))
    tan0 /= np.linalg.norm(tan0, axis=1)[:, None]
    y = np.concatenate([pos, vel, tan0], axis=1).copy()
    P = 2 * np.pi * a0**1.5
    dt = (P / steps_per_orbit)[:, None] * np.ones((N, 1))
    t = np.zeros((N, 1))
    # Jacobi constant, barycentric CR3BP:
    # CJ = n^2|r|^2 + 2/s1 + 2 mu/s2 - |v_rot|^2
    def jacobi(y):
        pos, vel = y[:, 0:2], y[:, 2:4]
        ang = n * t[:, 0]
        cs, sn = np.cos(ang), np.sin(ang)
        s1 = np.hypot(*(pos - np.stack([-mu * cs, -mu * sn], axis=1)).T)
        s2 = np.hypot(*(pos - np.stack([(1 - mu) * cs, (1 - mu) * sn], axis=1)).T)
        vrot = vel + np.stack([n * pos[:, 1], -n * pos[:, 0]], axis=1)
        return n**2 * (pos**2).sum(axis=1) + 2.0 / s1 + 2.0 * mu / s2 \
            - (vrot**2).sum(axis=1)
    CJ0 = jacobi(y)
    logsum = np.zeros(N)          # accumulated log growth
    alive = np.ones(N, bool)
    dead_at = np.full(N, np.nan)
    lam_cum = np.zeros((n_orbits, N))  # lambda*P per body-orbit index
    nsteps = n_orbits * steps_per_orbit
    for k in range(nsteps):
        m = alive if alive.all() else None
        if m is not None:
            yy = y
        else:
            idx = np.where(alive)[0]
            yy = y[idx]
        tt = t if m is not None else t[idx]
        dtt = dt if m is not None else dt[idx]
        k1 = deriv(tt, yy, mu, n)
        k2 = deriv(tt + 0.5 * dtt, yy + 0.5 * dtt * k1, mu, n)
        k3 = deriv(tt + 0.5 * dtt, yy + 0.5 * dtt * k2, mu, n)
        k4 = deriv(tt + dtt, yy + dtt * k3, mu, n)
        ynew = yy + (dtt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        if m is not None:
            y = ynew; t = tt + dtt
        else:
            y[idx] = ynew; t[idx] = tt + dtt
        if (k + 1) % renorm_every == 0:
            nz = np.linalg.norm(y[:, 4:8], axis=1)
            ok = nz > 0
            logsum[ok] += np.log(nz[ok])
            y[ok, 4:8] /= nz[ok, None]
        if (k + 1) % steps_per_orbit == 0:
            orb = (k + 1) // steps_per_orbit
            lam_cum[orb - 1] = logsum  # /1 orbit per body => lambda*P
        pos_now = y[:, 0:2]
        rs_now = np.stack([(1 - mu) * np.cos(n * t[:, 0]),
                           (1 - mu) * np.sin(n * t[:, 0])], axis=1)
        bad = (np.hypot(pos_now[:, 0], pos_now[:, 1]) > 4.0) | \
              (np.hypot(*(pos_now - rs_now).T) < 0.03)
        newly = bad & alive
        if newly.any():
            dead_at[newly] = (k + 1) / steps_per_orbit
            alive &= ~bad
            # freeze tangent to unit so it stops contributing
            y[~alive, 4:8] = 0.0
    CJ1 = jacobi(y)
    # windowed lambda over last window
    out = dict(mu=mu, n_orbits=n_orbits, steps=steps_per_orbit,
               dead_fraction=float((~alive).mean()),
               dCJ_median=float(np.median(np.abs((CJ1 - CJ0)[alive]) / np.abs(CJ0[alive]))) if alive.any() else float('nan'))
    rows = []
    for ia, a in enumerate(shells):
        for ie, e in enumerate(e_vals):
            sel = (bodies[:, 0] == a) & (bodies[:, 1] == e)
            alive_sel = sel & alive
            if alive_sel.sum() == 0:
                rows.append(dict(a=float(a), e=float(e), n=0))
                continue
            lt = lam_cum[-1][alive_sel] / n_orbits
            # last-half mean (bypasses transient)
            lt_half = (lam_cum[n_orbits // 2] - lam_cum[0])[alive_sel] / (n_orbits // 2)
            # windowed: 5-orbit windows over second half
            w = 5
            half0 = n_orbits // 2
            nw = (n_orbits - half0) // w
            duty = np.full(alive_sel.sum(), np.nan)
            if nw >= 2:
                wc = np.zeros((nw, int(alive_sel.sum())))
                for i in range(nw):
                    lo = half0 + i * w
                    wc[i] = ((lam_cum[lo + w - 1] - (lam_cum[lo - 1] if lo > 0 else 0)) / w)[alive_sel]
                duty = (wc < 1e-4).mean(axis=0)
            rows.append(dict(a=float(a), e=float(e), n=int(alive_sel.sum()),
                             lam_med=float(np.median(lt)),
                             lam_p90=float(np.percentile(lt, 90)),
                             lam_half_med=float(np.median(lt_half)),
                             duty_med=float(np.nanmedian(duty)),
                             frac_dead=float((~alive[sel]).mean())))
    out['rows'] = rows
    # traces for chaotic bodies (kept small): lambda*P of 20-orbit windows
    out['lam_total_median_all'] = float(np.median(lam_cum[-1][alive] / n_orbits))
    np.save(prefix + '.lamcum.npy', lam_cum if lam_cum.size < 8e6 else lam_cum[::4])
    np.save(prefix + '.meta.npy', bodies)
    with open(prefix + '.json', 'w') as f:
        json.dump(out, f)
    print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))

if __name__ == '__main__':
    mode = sys.argv[1]
    shells = np.round(np.arange(0.30, 0.8501, 0.025), 4)
    if mode == 'main':       # the tuned scene
        run(0.0123, shells, [0.0, 0.05, 0.20], 40, 200, 128)
    elif mode == 'floor':    # near-regular control, same ICs
        run(0.0123 / 1000.0, shells, [0.0, 0.05, 0.20], 40, 200, 128)
    elif mode == 'sweep':
        for mu in [1e-4, 1e-3, 3e-2]:
            run(mu, shells, [0.05], 40, 100, 128)
    elif mode == 'heldout':
        for mu in [0.05, 0.10]:
            run(mu, shells, [0.05], 40, 100, 128)
    elif mode == 'step':     # step-halving control
        run(0.0123, np.round(np.arange(0.40, 0.8001, 0.05), 4), [0.05], 16, 100, 256)
        run(0.0123, np.round(np.arange(0.40, 0.8001, 0.05), 4), [0.05], 16, 200, 128)
