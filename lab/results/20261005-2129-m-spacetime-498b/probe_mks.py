#!/usr/bin/env python3
"""Probe A: multi-Kerr-Schild superposition as the cell-addition rule (bottleneck 1).

Metric ansatz (contravariant, the candidate law):
    g^{mu nu} = eta^{mu nu} - sum_i f_i k_i^mu k_i^nu,   f_i = 2 M_i / r_i,  k_i^mu = (1, n_hat_i)
For ONE mass the Sherman-Morrison inverse of eta + f k k is exact (k null):
    (eta + f k_mu k_nu)^{-1} = eta - f k^mu k^nu
so one mass is exactly Schwarzschild (Eddington-Finkelstein/Kerr-Schild form).
For N masses the rank-1 sum is the *approximation under test*: exact to first
order in each f_i; the two-mass error is what this probe measures against a
1PN oracle (harmonic-gauge superposed metric, g00 = -1+2U-2U^2, gij = (1+2U) deltaij,
g0i = 0 for static sources; the standard 1PN test-particle metric, Poisson & Will).

Models integrated as Hamiltonian flows (all with identical machinery):
  mks     : H = 1/2 [ eta^{mu nu} p_mu p_nu - sum f_i (k_i . p)^2 ]
  oracle  : H = 1/2 [ -(1+2U+2U^2) p_t^2 + (1-2U) |p|^2 ]        (1PN metric)
  river   : H = sqrt(1+|p|^2) + beta(X) . p, beta = sum_i -sqrt(2 M_i/r_i) r_hat_i  (naive sum; NEGATIVE control)
  newton  : a = -grad Phi                                          (0PN reference)

Observables: perihelion advance per orbit (excess over Newtonian), light deflection.
"""
import json
import sys
import numpy as np
from fractions import Fraction
from scipy.integrate import solve_ivp

OUT = {}

# ---------------------------------------------------------------- geometry helpers
defSources = None

def f_of(x, srcs):
    return np.array([2.0 * m / np.hypot(*(x[:2] - c)) for (m, c) in srcs])

def n_of(x, srcs):
    out = []
    for (m, c) in srcs:
        d = x[:2] - c
        r = np.hypot(*d)
        out.append(d / r)
    return out

# ---------------------------------------------------------------- model: multi-KS
def rhs_mks(lam, y, srcs):
    t, x, y_, pt, px, py = y
    pos = np.array([x, y_])
    fs = f_of(pos, srcs)
    ns = n_of(pos, srcs)
    kd = pt + np.array([n[0] * px + n[1] * py for n in ns])   # k_i^mu p_mu = p_t + n_i . p
    # H = 1/2 (-pt^2 + p^2 - sum f (k.p)^2)
    dH_dpt = -pt - np.dot(fs, kd)
    dH_dp = np.array([px, py]) - np.einsum('i,ij->j', fs * kd, ns)
    dp = np.zeros(3)
    for f, n, (m, c) in zip(fs, ns, srcs):
        d = pos - c
        r = np.hypot(*d)
        # d f/dx = -2M d / r^3
        dfdx = -2.0 * m * d / r**3
        # d n^a/dx^b = (delta_ab r^2 - d_a d_b)/r^3
        dn = (np.eye(2) * r**2 - np.outer(d, d)) / r**3
        kdp = pt + n @ np.array([px, py])
        dp[:2] += 0.5 * dfdx * kdp**2 + f * kdp * (dn @ np.array([px, py]))
    return [dH_dpt, dH_dp[0], dH_dp[1], 0.0, dp[0], dp[1]]

# ---------------------------------------------------------------- model: 1PN oracle
def U_of(pos, srcs):
    return sum(m / np.hypot(*(pos - c)) for (m, c) in srcs)

def rhs_pn(lam, y, srcs):
    t, x, y_, pt, px, py = y
    pos = np.array([x, y_])
    U = U_of(pos, srcs)
    dU = np.zeros(2)
    for (m, c) in srcs:
        d = pos - c
        r = np.hypot(*d)
        dU += -m * d / r**3
    g00i = -(1 + 2 * U + 2 * U * U)      # g^{tt}
    giji = 1 - 2 * U                      # g^{ij} (isotropic)
    dH_dpt = g00i * pt
    dH_dp = giji * np.array([px, py])
    dH_dU = -((1 + 2 * U) * pt * pt + px * px + py * py)
    dp = -dH_dU * dU
    return [dH_dpt, dH_dp[0], dH_dp[1], 0.0, dp[0], dp[1]]

# ---------------------------------------------------------------- model: naive river
def beta_of(pos, srcs):
    b = np.zeros(2)
    J = np.zeros((2, 2))
    for (m, c) in srcs:
        d = pos - c
        r = np.hypot(*d)
        s = np.sqrt(2.0 * m)
        b += -s * d / r**1.5
        J += -s * (np.eye(2) * r** -1.5 - 1.5 * np.outer(d, d) * r** -3.5)

    return b, J

def rhs_river(T, y, srcs):
    x, y_, px, py = y
    pos = np.array([x, y_])
    p = np.array([px, py])
    b, J = beta_of(pos, srcs)
    g = 1.0 / np.sqrt(1.0 + p @ p)
    dx = g * p + b
    dp = -J.T @ p
    return [dx[0], dx[1], dp[0], dp[1]]

# ---------------------------------------------------------------- model: Newtonian
def rhs_newt(T, y, srcs):
    x, y_, vx, vy = y
    pos = np.array([x, y_])
    a = np.zeros(2)
    for (m, c) in srcs:
        d = pos - c
        r = np.hypot(*d)
        a += -m * d / r**3
    return [vx, vy, a[0], a[1]]

# ---------------------------------------------------------------- observable: advance per orbit
def perihelion_advance(sol_t, sol_y, colx, coly):
    xs, ys = sol_y[colx], sol_y[coly]
    r = np.hypot(xs, ys)
    phi = np.unwrap(np.arctan2(ys, xs))
    idx = [i for i in range(1, len(r) - 1) if r[i] < r[i - 1] and r[i] < r[i + 1]]
    if len(idx) < 3:
        return None, len(idx), None
    # parabolic refinement of each minimum
    phis = []
    for i in idx:
        t0, t1, t2 = sol_t[i - 1], sol_t[i], sol_t[i + 1]
        r0, r1, r2 = r[i - 1], r[i], r[i + 1]
        den = (r0 - 2 * r1 + r2)
        tau = 0.5 * (r0 - r2) / den if abs(den) > 1e-300 else 0.0
        ti = t1 + tau * (t2 - t0) / 2
        phis.append(np.interp(ti, sol_t, phi))
    adv = np.diff(phis) - 2 * np.pi
    rmin, rmax = float(r.min()), float(r.max())
    p_act = 2 * rmin * rmax / (rmin + rmax)
    e_act = (rmax - rmin) / (rmax + rmin)
    return float(np.median(adv)), len(idx), dict(p_act=p_act, e_act=e_act)


def run_orbit(model, srcs, p_orb, e, n_orb=8, rtol=1e-12):
    M_tot = sum(m for (m, c) in srcs)
    a = p_orb / (1 - e * e)
    rp = p_orb / (1 + e)
    v2 = M_tot * (2.0 / rp - 1.0 / a)
    v = np.sqrt(v2)
    T_orb = 2 * np.pi * np.sqrt(a**3 / M_tot)
    te = np.linspace(0, n_orb * T_orb, 4000)
    if model in ('mks', 'pn'):
        pos = np.array([rp, 0.0])
        gam = 1.0 / np.sqrt(1 - v * v)
        pvec = gam * v * np.array([0.0, 1.0])
        pt = -np.sqrt(pvec @ pvec + 1.0)
        if model == 'mks':
            # exact constraint for this ansatz: solve for pt in H = -1/2
            fs = f_of(pos, srcs); ns = n_of(pos, srcs)
            kd = lambda ptx: ptx + sum(n[0] * pvec[0] + n[1] * pvec[1] for n in ns)
            # -pt^2 + |p|^2 - sum f (pt + n.p)^2 = -1 ; solve quadratic in pt
            A = -(1.0 + sum(fs))
            B = -2.0 * sum(f * (n @ pvec) for f, n in zip(fs, ns))
            C = pvec @ pvec - sum(f * (n @ pvec)**2 for f, n in zip(fs, ns)) + 1.0
            pt = (-B + np.sqrt(B * B - 4 * A * C)) / (2 * A)
            rhs = lambda t, y: rhs_mks(t, y, srcs)
            y0 = [0.0, pos[0], pos[1], pt, pvec[0], pvec[1]]
            cols = (1, 2)
        else:
            pt = -np.sqrt((1 - (1 - 2 * U_of(pos, srcs)) * (pvec @ pvec)) / (1 + 2 * U_of(pos, srcs) + 2 * U_of(pos, srcs) ** 2))
            rhs = lambda t, y: rhs_pn(t, y, srcs)
            y0 = [0.0, pos[0], pos[1], pt, pvec[0], pvec[1]]
            cols = (1, 2)
        sol = solve_ivp(rhs, (0, te[-1]), y0, t_eval=te, rtol=rtol, atol=1e-14, method='DOP853')
        return perihelion_advance(sol.t, sol.y, cols[0], cols[1])
    elif model == 'river':
        # The naive beta-sum cannot hold the shared Newtonian initial condition
        # (it escapes); scan launch speeds for its own bound eccentric orbit so
        # the negative control still yields a precession number.
        pos = np.array([rp, 0.0])
        rhs = lambda t, y: rhs_river(t, y, srcs)
        best = (None, -1, None)
        for f in np.linspace(0.80, 1.45, 27):
            b, _ = beta_of(pos, srcs)
            u = np.array([0.0, f * v]) - b
            if u @ u >= 1.0:
                continue
            g = 1.0 / np.sqrt(1 - u @ u)
            pvec = g * u
            y0 = [pos[0], pos[1], pvec[0], pvec[1]]
            try:
                sol = solve_ivp(rhs, (0, te[-1]), y0, t_eval=te, rtol=rtol, atol=1e-14, method='DOP853')
            except Exception:
                continue
            r = np.hypot(sol.y[0], sol.y[1])
            if not np.all(np.isfinite(r)):
                continue
            adv, n_min, shp = perihelion_advance(sol.t, sol.y, 0, 1)
            if adv is None or n_min < 4 or r.max() > 8 * rp or r.min() < 0.5 * rp:
                continue
            if n_min > best[1]:
                best = ((adv, n_min, shp), n_min, f)
        return best[0] if best[0] is not None else (None, 0, None)
    else:
        y0 = [rp, 0.0, 0.0, v]
        rhs = lambda t, y: rhs_newt(t, y, srcs)
        sol = solve_ivp(rhs, (0, te[-1]), y0, t_eval=te, rtol=rtol, atol=1e-14, method='DOP853')
        return perihelion_advance(sol.t, sol.y, 0, 1)

# ---------------------------------------------------------------- observable: light deflection
def run_light(model, srcs, xspan, b_off):
    x0, x1 = xspan
    if model in ('mks', 'pn'):
        pos0 = np.array([x0, b_off])
        # far away: p ~ (1, 0); pt from null condition
        if model == 'mks':
            pvec = np.array([1.0, 0.0])
            fs = f_of(pos0, srcs); ns = n_of(pos0, srcs)
            A = -(1.0 + sum(fs))
            B = -2.0 * sum(f * (n @ pvec) for f, n in zip(fs, ns))
            C = pvec @ pvec - sum(f * (n @ pvec)**2 for f, n in zip(fs, ns))
            pt = (-B + np.sqrt(B * B - 4 * A * C)) / (2 * A)
            rhs = lambda t, y: rhs_mks(t, y, srcs)
        else:
            pvec = np.array([1.0, 0.0])
            U0 = U_of(pos0, srcs)
            pt = -np.sqrt((pvec @ pvec) * (1 - 2 * U0) / (1 + 2 * U0 + 2 * U0 ** 2))
            rhs = lambda t, y: rhs_pn(t, y, srcs)
        y0 = [0.0, pos0[0], pos0[1], pt, pvec[0], pvec[1]]
        sol = solve_ivp(rhs, (0, 1e7), y0, rtol=1e-13, atol=1e-16, method='DOP853',
                        events=[lambda t, y: y[1] - x1], dense_output=True)
        te = np.linspace(0, sol.t[-1], 20001)
        yy = sol.sol(te)
        # velocity direction from dH/dp at start and end
        def dirpt(yv):
            t_, x_, y_, pt, px, py = yv
            pos = np.array([x_, y_])
            if model == 'mks':
                fs = f_of(pos, srcs); ns = n_of(pos, srcs)
                kd = pt + np.array([n @ np.array([px, py]) for n in ns]).sum(axis=0) \
                     if False else pt + sum(n[0] * px + n[1] * py for n in ns)
                dpx = px - sum(f * kd * n[0] for f, n in zip(fs, ns))
                dpy = py - sum(f * kd * n[1] for f, n in zip(fs, ns))
            else:
                U = U_of(pos, srcs)
                dpx = (1 - 2 * U) * px
                dpy = (1 - 2 * U) * py
            return np.array([dpx, dpy])
        d0 = dirpt(yy[:, 0]); d1 = dirpt(yy[:, -1])
        return float(np.arctan2(d1[1], d1[0]) - np.arctan2(d0[1], d0[0]))
    else:
        raise ValueError('light only for mks/pn')

# ================================================================ experiments
def main():
    res = {}

    # ---- controls and cases, v2 (post-diagnosis design):
    # per-model actual orbit shape is measured (p_act) and each model's excess
    # is normalized by 6*pi*M_tot/p_act; the two-mass test runs WEAK field
    # (M_tot/p = 0.002) where 2PN monopole content cannot mask cross terms.
    e = 0.1

    def orbit_case(tag, srcs, p_orb):
        M_tot = sum(m for (m, c) in srcs)
        am, n_, shm = run_orbit('mks', srcs, p_orb, e)
        ap, _n, shp = run_orbit('pn', srcs, p_orb, e)
        an, _nn, shn = run_orbit('newt', srcs, p_orb, e)
        ar, _nr, shr = run_orbit('river', srcs, p_orb, e)
        exm = am - an; expn = ap - an; exr = (ar - an) if (ar is not None and an is not None) else None
        pred_m = 6 * np.pi * M_tot / shm['p_act']
        pred_p = 6 * np.pi * M_tot / shp['p_act']
        res[tag] = dict(
            excess_mks=exm, excess_pn=expn, excess_river=exr,
            excess_mks_1pn_at_pact=exm / pred_m - 1, excess_pn_1pn_at_pact=expn / pred_p - 1,
            mks_vs_pn_rel=abs(exm - expn) / abs(expn),
            river_vs_pn_rel=(abs(exr - expn) / abs(expn)) if exr is not None else None,
            p_act=dict(mks=shm, pn=shp, newton=shn, river=shr), peri_count=n_)

    # single-mass controls, weak and strong
    orbit_case('single_weak', [(0.04, np.array([0.0, 0.0]))], 20.0)
    orbit_case('single_strong', [(0.2, np.array([0.0, 0.0]))], 20.0)
    # held-out two-mass, weak field (M_tot/p = 0.002), p/d = 10 and 30
    for pd in (10.0, 30.0):
        d = 2.0; Meach = 0.02
        orbit_case(f'two_weak_pd{int(pd)}',
                   [(Meach, np.array([-d / 2, 0.0])), (Meach, np.array([d / 2, 0.0]))], pd * d)
    # secondary: the original strong-field pair (M_tot/p = 0.01)
    for pd in (10.0,):
        d = 2.0; Meach = 0.1
        orbit_case(f'two_strong_pd{int(pd)}',
                   [(Meach, np.array([-d / 2, 0.0])), (Meach, np.array([d / 2, 0.0]))], pd * d)

    # ---- light, v2: masses on the SAME side of the ray so deflections add;
    # b1 = b2 = b; compare two-mass MKS vs single-mass MKS of equal total mass
    # (the cross-term test) and vs the linear 1PN sum; R = 200 b.
    for b in (40.0, 4000.0):
        Meach = 1.0
        src2 = [(Meach, np.array([0.0, b])), (Meach, np.array([4 * b, b]))]
        R = 200 * b
        defl_m = run_light('mks', src2, (-R, R), 0.0)
        defl_p = run_light('pn', src2, (-R, R), 0.0)
        lin = 2 * 4.0 * Meach / b
        src1L = [(2 * Meach, np.array([0.0, b]))]
        defl_m1 = run_light('mks', src1L, (-R, R), 0.0)
        res[f'light_b{int(b)}'] = dict(defl_mks=defl_m, defl_pn=defl_p, defl_mks_single=defl_m1,
                                       linear_1PN=lin, mks_vs_lin_rel=defl_m / lin - 1,
                                       mks2_vs_mks1_rel=defl_m / defl_m1 - 1,
                                       pn_vs_lin_rel=defl_p / lin - 1)

    # ---- determinism: integer rank-1 accumulation, random deposit orders
    import hashlib, random
    rng = random.Random(7)
    srcs = [(0.1 * (i + 1), np.array([13.0 * (i + 1), 7.0 * (i + 3)])) for i in range(12)]
    # integer data: f_num (2*M*SCALE / r den) via Fraction-free: use Fractions converted to
    # a common integer denominator, then integer matrices.
    from fractions import Fraction as F
    SCALE = 10**6
    deposits = []
    for (m, c) in srcs:
        fx = F(2 * m).limit_denominator(SCALE)
        # direction components as fractions of a unit-ish integer triple (kt, kx, ky)
        dx, dy = 60 - c[0] % 61, 40 - c[1] % 43   # arbitrary deterministic ints
        deposits.append((int(round(2 * m * SCALE)), int(dx), int(dy)))
    digests = []
    for trial in range(20):
        order = list(range(len(deposits)))
        rng.shuffle(order)
        g = np.array([[-1 << 20, 0, 0], [0, 1 << 20, 0], [0, 0, 1 << 20]], dtype=object)
        # eta^{mu nu} - sum f k k  with integer arithmetic (object dtype)
        base = np.array([[-(1 << 40), 0, 0], [0, 1 << 40, 0], [0, 0, 1 << 40]], dtype=object)
        for i in order:
            fn, kx, ky = deposits[i]
            k = (1 << 20, kx, ky)
            for a in range(3):
                for b_ in range(3):
                    base[a, b_] -= fn * k[a] * k[b_]
        digests.append(hashlib.sha256(
            b''.join(int(base[a, b_]).to_bytes(64, 'big', signed=True) for a in range(3) for b_ in range(3))).hexdigest())
    res['determinism'] = dict(identical=len(set(digests)) == 1, n_trials=20)

    # ---- cone slide: characteristic variety shifts only along k_j
    rng2 = np.random.default_rng(3)
    x = np.array([3.0, 4.0])
    srcA = [(0.3, np.array([0.0, 0.0]))]
    srcB = [(0.2, np.array([5.0, 1.0]))]
    def Sval(xi, srcs):
        fs = f_of(x, srcs); ns = n_of(x, srcs)
        s = -xi[0]**2 + xi[1]**2 + xi[2]**2
        for f, n in zip(fs, ns):
            kd = xi[0] + n[0] * xi[1] + n[1] * xi[2]
            s -= f * kd * kd
        return s
    worst = 0.0
    for _ in range(2000):
        xi = rng2.normal(size=3)
        fB = 2 * srcB[0][0] / np.hypot(*(x - srcB[0][1]))
        nB = (x - srcB[0][1]) / np.hypot(*(x - srcB[0][1]))
        kd = xi[0] + nB[0] * xi[1] + nB[1] * xi[2]
        lhs = Sval(xi, srcA + srcB) - Sval(xi, srcA)
        worst = max(worst, abs(lhs + fB * kd * kd))
    res['cone_slide'] = dict(max_residual=worst)

    json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else 'metrics.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))

if __name__ == '__main__':
    main()
