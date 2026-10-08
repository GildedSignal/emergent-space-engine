#!/usr/bin/env python3
"""Float replica of motion law v2 (root doll, planar circular restricted 3-body) + the SEM step (P8).

Faithful to lab/refs/opus-motion/memo.md §2.1-2.2:
  K = H_D - U_P + p_t ~= 0            H_D = p^2/2 - GM/|x|   (exact Kepler drift)
  U_P = Gm/|x - x_p(t)|               planet on a circle at rate Omega (star-centred frame)
  Gamma = f(H_D+p_t+c) - f(U_P+c),  f'(y) = 1/y^2 + 1/(b y),  b = 30 c,  c = Gm/R_H
  one step: Phi = D(ds/2) Kc(ds) D(ds/2), dt = (ds/2) f'(E_tube+p_t+c), w = ds f'(U_P+c)
  kick: dp = -w grad U_P, dp_t = -v_p . dp            (J = p_t + Omega L exact per kick/drift)

Jacobi analogue (exact invariant of this continuum flow, star-centred inertial):
  C = -v^2 + 2 Omega.(x x p) + 2 GM/|x| + 2 Gm/|x-x_p|  =  2(J - K)

SEM variant (Kane-Marsden-Ortiz style time-closure): per step solve a scalar lam per ship
s.t. K(after Phi_{lam*ds}) = 0 (secant, 3 iters, clipped, revert-to-lam=1 if worse).
J stays exactly conserved for any lam, so C - C0 = -2 K at samples.

Usage: python3 v2sem.py ensemble|flyby|control|scan [--sem] [-k N] [--ships N] [--periods N] [--out F]
"""
import argparse, json, math, os
import numpy as np

# ---------------- scene (Sun-Jupiter analogue, planar CR3BP) ----------------
GM, Gm, SEP = 1.0, 1e-3, 1.0
OMEGA = 1.0
P_ORB = 2 * math.pi / OMEGA
R_H = SEP * (Gm / (3 * GM)) ** (1.0 / 3.0)
C0P = Gm / R_H
B_PAR = 30 * C0P
R_PLANET = R_H / 1000.0


def fp(y):
    return 1.0 / y**2 + 1.0 / (B_PAR * y)


def planet_pos(t):
    return SEP * np.stack([np.cos(OMEGA * t), np.sin(OMEGA * t)], axis=-1)


def planet_vel(t):
    xp = planet_pos(t)
    return OMEGA * np.stack([-xp[..., 1], xp[..., 0]], axis=-1)


def u_pot(x, t):
    d = np.linalg.norm(x - planet_pos(t), axis=-1)
    return Gm / np.maximum(d, 1e-12)


def u_grad(x, t):
    r = x - planet_pos(t)
    d3 = np.maximum(np.linalg.norm(r, axis=-1), 1e-12) ** 3
    return -Gm * r / d3[..., None]


def _stumpff(z):
    az = np.abs(z)
    small = az < 1e-8
    zp = np.maximum(z, 1e-300)
    c2_pos = (1 - np.cos(np.sqrt(zp))) / zp
    w = np.sqrt(az)
    c2_neg = (np.cosh(w) - 1) / np.maximum(az, 1e-300)
    c3_pos = (np.sqrt(zp) - np.sin(np.sqrt(zp))) / (zp * np.sqrt(zp))
    c3_neg = (np.sinh(w) - w) / np.maximum(az * w, 1e-300)
    c2 = np.where(z > 0, c2_pos, c2_neg)
    c3 = np.where(z > 0, c3_pos, c3_neg)
    zs = np.where(small, z, 0.0)
    c2s = 0.5 - zs / 24 + zs * zs / 720
    c3s = 1.0 / 6 - zs / 120 + zs * zs / 5040
    return np.where(small, c2s, c2), np.where(small, c3s, c3)
def jacobi(x, p, t):
    v2 = np.sum(p * p, axis=-1)
    L = x[..., 0] * p[..., 1] - x[..., 1] * p[..., 0]
    return -v2 + 2 * OMEGA * L + 2 * GM / np.linalg.norm(x, axis=-1) + 2 * u_pot(x, t)


def h_d(x, p):
    return np.sum(p * p, axis=-1) / 2 - GM / np.linalg.norm(x, axis=-1)


# ---------------- exact Kepler drift (universal variables) ----------------
def _stumpff(z):
    az = np.abs(z)
    small = az < 1e-8
    zp = np.maximum(z, 1e-300)
    c2_pos = (1 - np.cos(np.sqrt(zp))) / zp
    w = np.sqrt(az)
    c2_neg = (np.cosh(w) - 1) / np.maximum(az, 1e-300)
    c3_pos = (np.sqrt(zp) - np.sin(np.sqrt(zp))) / (zp * np.sqrt(zp))
    c3_neg = (np.sinh(w) - w) / np.maximum(az * w, 1e-300)
    c2 = np.where(z > 0, c2_pos, c2_neg)
    c3 = np.where(z > 0, c3_pos, c3_neg)
    zs = np.where(small, z, 0.0)
    c2s = 0.5 - zs / 24 + zs * zs / 720
    c3s = 1.0 / 6 - zs / 120 + zs * zs / 5040
    return np.where(small, c2s, c2), np.where(small, c3s, c3)


def kepler_drift(x, p, dt, mu=GM):
    r0 = np.linalg.norm(x, axis=-1)
    v2 = np.sum(p * p, axis=-1)
    vr0 = np.sum(x * p, axis=-1) / r0
    alpha = 2.0 / r0 - v2 / mu
    sqmu = math.sqrt(mu)
    chi = sqmu * dt / r0
    for _ in range(100):
        z = alpha * chi * chi
        c2, c3 = _stumpff(z)
        F = (r0 * vr0 / sqmu) * chi * chi * c2 + (1 - alpha * r0) * chi**3 * c3 + r0 * chi - sqmu * dt
        dF = (r0 * vr0 / sqmu) * chi * (1 - z * c3) + (1 - alpha * r0) * chi * chi * c2 + r0
        step_ = F / dF
        chi = chi - step_
        if np.max(np.abs(step_)) < 1e-13:
            break
    z = alpha * chi * chi
    c2, c3 = _stumpff(z)
    f = 1 - chi * chi / r0 * c2
    g = dt - chi**3 / sqmu * c3
    xn = f[..., None] * x + g[..., None] * p
    rn = np.linalg.norm(xn, axis=-1)
    fdot = sqmu * chi * (z * c3 - 1.0) / (rn * r0)
    gdot = 1 - chi * chi / rn * c2
    pn = fdot[..., None] * x + gdot[..., None] * p
    return xn, pn


def v2_step2(t, x, p, pt, ds, lam_s, lam_w):
    """One v2 step. lam_s scales the whole step (P8 literal); lam_w scales only the
    kick impulse (energy closure candidate). Both keep J exact; each is symplectic."""
    s = lam_s * ds
    dt1 = 0.5 * s * fp(h_d(x, p) + pt + C0P)
    x1, p1 = kepler_drift(x, p, dt1)
    t1 = t + dt1
    w = lam_w * s * fp(u_pot(x1, t1) + C0P)
    dp = -w[..., None] * u_grad(x1, t1)
    p2 = p1 + dp
    pt2 = pt - np.sum(planet_vel(t1) * dp, axis=-1)
    dt2 = 0.5 * s * fp(h_d(x1, p2) + pt2 + C0P)
    x2, p2 = kepler_drift(x1, p2, dt2)
    return t1 + dt2, x2, p2, pt2, dt1


def Kafter(t, x, p, pt, ds, lam_s, lam_w):
    t2, x2, p2, pt2, _ = v2_step2(t, x, p, pt, ds, lam_s, lam_w)
    return t2, x2, p2, pt2, h_d(x2, p2) - u_pot(x2, t2) + pt2


def sem_solve(t, x, p, pt, ds, which, stats, iters=3):
    """Solve one scalar (lam_s or lam_w) so K=0 after the step. Secant; revert to 1
    when not improved by >=5x. Returns the chosen end state."""
    def ev(lam):
        if which == 'step':
            return Kafter(t, x, p, pt, ds, lam, np.ones_like(lam))
        return Kafter(t, x, p, pt, ds, np.ones_like(lam), lam)
    t1, x1, p1, pt1, K_b = ev(np.ones_like(pt))
    stats['evals'] += 1
    eps = 1e-3
    t2, x2, p2, pt2, K_c = ev(np.full_like(pt, 1 + eps))
    stats['evals'] += 1
    lam_a, Ka = np.ones_like(pt), K_b.copy()
    lam_b, Kb = np.full_like(pt, 1 + eps), K_c
    tN, xN, pN, ptN = t1, x1, p1, pt1
    for _ in range(iters):
        den = Kb - Ka
        ok = np.abs(den) > 1e-300
        lam_n = np.where(ok, lam_b - Kb * (lam_b - lam_a) / np.where(ok, den, 1.0),
                         0.5 * (lam_a + lam_b))
        lam_n = np.clip(lam_n, 0.05, 20.0) if which == 'kick' else np.clip(lam_n, 0.2, 5.0)
        tN, xN, pN, ptN, Kn = ev(lam_n)
        stats['evals'] += 1
        lam_b, Kb = lam_n, Kn
    solved = (np.abs(Kb) < np.abs(K_b) * 0.2) | (np.abs(Kb) < 1e-13)
    stats['unsolved'] += int(np.sum(~solved))
    stats['steps'] += 1
    return (np.where(solved, tN, t1), np.where(solved[..., None], xN, x1),
            np.where(solved[..., None], pN, p1), np.where(solved, ptN, pt1))



# ---------------- ships ----------------
def state_from_elems(a, e, om, M):
    E = M + e * np.sin(M)
    for _ in range(80):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    r = a * (1 - e * np.cos(E))
    h = np.sqrt(GM * a * (1 - e**2))
    th = om + nu
    x = r[..., None] * np.stack([np.cos(th), np.sin(th)], -1)
    p = (h / r)[..., None] * np.stack([-np.sin(th), np.cos(th)], -1)
    return x, p


def elements(x, p):
    r = np.linalg.norm(x, axis=-1); v2 = np.sum(p * p, axis=-1)
    a = 1.0 / (2.0 / r - v2 / GM)
    rv = np.sum(x * p, axis=-1)
    evec = ((v2 - GM / r)[..., None] * x - rv[..., None] * p) / GM
    e = np.linalg.norm(evec, axis=-1)
    om = np.arctan2(evec[..., 1], evec[..., 0])
    return a, e, om


# ---------------- driver ----------------
def run(x0, p0, k, periods, sem, sample_per=64, want_elems=False):
    n = x0.shape[0]
    ds = (P_ORB / (2.0 ** k * fp(C0P))) * np.ones(n)
    t = np.zeros(n); x, p = x0.copy(), p0.copy()
    pt = u_pot(x, 0.0) - h_d(x, p)
    Cref = jacobi(x, p, 0.0)
    stats = {'evals': 0, 'unsolved': 0, 'steps': 0}
    T_end = periods * P_ORB
    rows = []      # each entry: (row_t, row_C, row_d) full-length, NaN except sampled ship
    next_sample = np.full(n, P_ORB / sample_per)
    dmin = np.full(n, 1e9)
    ekick = np.zeros(n)
    while True:
        act = t < T_end
        if not act.any():
            break
        if sem and sem != 'off':
            t2, x2, p2, pt2 = sem_solve(t, x, p, pt, ds, sem, stats)
            dt1 = None
        else:
            t2, x2, p2, pt2, dt1 = v2_step2(t, x, p, pt, ds, np.ones(n), np.ones(n))
            stats['steps'] += 1; stats['evals'] += 1
        for i in np.where(act & (t2 > next_sample))[0]:
            t_mid = 0.5 * (t[i] + t2[i])
            if next_sample[i] <= t_mid:
                xr, pr = kepler_drift(x[i][None], p[i][None], next_sample[i] - t[i])
            else:
                if sem or dt1 is None:
                    _, x1, p1, _, d1 = v2_step2(t[i][None], x[i][None], p[i][None], pt[i][None], ds[i][None], np.ones(1), np.ones(1))
                    t1 = t[i] + d1[0]
                else:
                    x1, p1 = kepler_drift(x[i][None], p[i][None], dt1[i])
                    t1 = t[i] + dt1[i]
                up = u_pot(x1, t1) + C0P
                w = ds[i] * fp(up)
                dp = -w[..., None] * u_grad(x1, t1)
                p1b = p1 + dp
                xr, pr = kepler_drift(x1, p1b, next_sample[i] - t1)
            row_t = np.full(n, np.nan); row_C = np.full(n, np.nan); row_d = np.full(n, np.nan)
            row_t[i] = next_sample[i]
            row_C[i] = jacobi(xr, pr, next_sample[i])[0]
            row_d[i] = np.linalg.norm(xr[0] - planet_pos(next_sample[i]))
            rows.append((row_t, row_C, row_d))
            next_sample[i] += P_ORB / sample_per
        dm = np.linalg.norm(x2 - planet_pos(t2), axis=-1)
        dmin = np.minimum(dmin, np.where(act, dm, dmin))
        ekick += (act & (dm < R_H))
        t, x, p, pt = t2, x2, p2, pt2
    TS = np.array([r[0] for r in rows]); CS = np.array([r[1] for r in rows])
    DS_ = np.array([r[2] for r in rows])
    return TS, CS, Cref, stats, dmin, ekick, DS_, (x, p)


def analyze(TS, CS, Cref, DS_):
    err = CS - Cref[None, :]
    far = ~(DS_ < 3 * R_H)          # far-field only (memo §1.1); encounter readouts are Kepler-drift garbage
    err = np.where(far, err, np.nan)
    P = P_ORB
    edges = [1, 10, 100, TS[:, 0].max() / P if np.isfinite(TS[:, 0].max()) else 1]
    edges = sorted(set([1, 10, 100, max(11, int(edges[3]))]))
    wins, cents = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (TS >= lo * P) & (TS < hi * P)
        if m.any():
            wins.append(float(np.nanmax(np.abs(np.where(m, err, np.nan)))))
            cents.append(math.sqrt(lo * hi))
    exp = float('nan')
    if len(wins) >= 2:
        y = np.log(np.maximum(np.array(wins), 1e-300))
        exp = float(np.polyfit(np.log(cents), y, 1)[0])
    # per-encounter jumps (memo §1.1): level of err in quiet windows (d>3R_H) around each encounter
    jumps = []
    for i in range(err.shape[1]):
        ti, ei, di = TS[:, i], err[:, i], DS_[:, i]
        m = np.isfinite(ti) & np.isfinite(di)
        ti, ei, di = ti[m], ei[m], di[m]
        if len(ti) < 30:
            continue
        close = di < 3 * R_H
        j = 0
        while j < len(ti):
            if close[j]:
                j2 = j
                while j2 < len(ti) and close[j2]:
                    j2 += 1
                t_pre = (ti > ti[j] - P / 4) & (ti < ti[j] - P / 16) & ~close
                t_post = (ti > ti[j2] + P / 16) & (ti < ti[j2] + P / 4) & ~close
                if t_pre.sum() >= 3 and t_post.sum() >= 3:
                    jumps.append(float(np.mean(ei[t_post]) - np.mean(ei[t_pre])))
                j = j2
            else:
                j += 1
    return {'decade_maxerr': wins, 'exponent': exp,
            'final_maxerr': float(np.nanmax(np.abs(err))),
            'n_enc': len(jumps),
            'jump_rms': float(np.sqrt(np.mean(np.square(jumps)))) if jumps else float('nan'),
            'jump_mean': float(np.mean(jumps)) if jumps else float('nan')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['ensemble', 'flyby', 'control', 'scan'])
    ap.add_argument('--sem', default='off', choices=['off', 'step', 'kick'])
    ap.add_argument('-k', type=int, default=6)
    ap.add_argument('--ships', type=int, default=12)
    ap.add_argument('--periods', type=int, default=200)
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    if a.mode == 'scan':
        # pick a deep-flyby ship: a=0.8 e=0.3, scan omega for min distance in [15,60] R_p
        best = None
        for om in np.linspace(0, 2 * math.pi, 97):
            x0, p0 = state_from_elems(np.array([0.8]), np.array([0.3]), np.array([om]), np.array([0.0]))
            TS, CS, Cr, st, dm, ek, D, _fs = run(x0, p0, 6, 6, False, sample_per=16)
            q = dm[0] / R_PLANET
            if 15 <= q <= 60 and (best is None or q < best[1]):
                best = (om, q)
        print('omega', best[0], 'q/R_p', best[1])
        open('flyby_omega.txt', 'w').write(repr(best[0]))
        return
    if a.mode == 'ensemble':
        rng = np.random.default_rng(7)
        n = a.ships
        aa = rng.uniform(0.45, 0.78, n); ee = rng.uniform(0.02, 0.30, n)
        om = rng.uniform(0, 2 * math.pi, n); M = rng.uniform(0, 2 * math.pi, n)
        x0, p0 = state_from_elems(aa, ee, om, M)
    elif a.mode == 'control':
        x0, p0 = state_from_elems(np.full(4, 0.50), np.full(4, 0.01),
                                  np.linspace(0, 2 * math.pi, 4), np.full(4, 1.0))
    else:
        omf = 'flyby_omega.txt'
        om = float(open(omf).read().strip()) if os.path.exists(omf) else 2.0
        x0, p0 = state_from_elems(np.array([0.8]), np.array([0.3]), np.array([om]), np.array([0.0]))
    TS, CS, Cref, stats, dmin, ek, D, (xf, pf) = run(x0, p0, a.k, a.periods, a.sem)
    res = {'mode': a.mode, 'sem': a.sem, 'k': a.k, 'periods': a.periods,
           'ships': int(x0.shape[0])}
    res.update(analyze(TS, CS, Cref, D))
    res['evals_per_ship_step'] = stats['evals'] / max(1, stats['steps'])
    res['unsolved_frac'] = stats['unsolved'] / max(1, stats['steps'] * x0.shape[0])
    res['min_q_Rp'] = (dmin / R_PLANET).tolist()
    res['enc_steps_frac'] = (ek / max(1, a.periods)).tolist()
    if a.mode == 'flyby':
        af, ef, of = elements(xf, pf)
        res['final_elements'] = {'a': float(af[0]), 'e': float(ef[0]), 'om': float(of[0])}
        res['kicks_flyby'] = float(ek[0])
    print(json.dumps(res, indent=1, default=float))
    if a.out:
        json.dump(res, open(a.out, 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
