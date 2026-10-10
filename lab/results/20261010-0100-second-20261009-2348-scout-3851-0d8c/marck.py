#!/usr/bin/env python3
"""Second author on 20261009-2348-scout-3851: the Marck-frame coupled certificate.

The second checker's gold experiment: run the Floquet certificate on the full
2x2 coupled member tide (parallel-transported Fermi axes, both in-plane
eigenchannels, frame precession), with the lambda table quantized to the
law's grid, and show (i) the avg law is still blind, (ii) the chart's bands
match the coupled truth, (iii) quantization shifts band edges by a stated bound.

Physics (verified in situ against exact transport; see `validate`):
  Doll on an eccentric equatorial Schwarzschild geodesic (Darwin psi, M=1).
  Member in the doll's Fermi frame:  x'' + Om^2 x = Lam(tau) x,  Lam = -E,
  E_ij = R(e_i, u, e_j, u)  (electric Weyl projected along the tube).
  In the orbital frame f1 = (e_r + u_r u)/N, f3 = (u_ph e_t + gam e_ph)/N
  (N^2 = 1 + u_r^2, gam = E/sqrt(f), u_ph = L u), the tide is the EXACT
  symmetric 2x2 (w = u^3; sympy-verified against the frozen phase-2 signs
  R_that rhat that rhat = -2w, R_thph = +2w, R_rph = -w):
      E_orb = w * [[ -2 - 3 u_ph^2/N^2 ,  -3 gam u_ph u_r / N^2 ],
                   [ -3 gam u_ph u_r / N^2 ,  1 - 3 u_r^2 u_ph^2/N^2 ]],
      E_22  = w (1 + 3 u_ph^2)   (out-of-plane, decoupled).
  Turning-point limit: diag(-(3 gam^2 -1), 1) = the frozen kernel.
  The Fermi axes precess relative to the orbital frame at
      omega = -gam u_ph u (f-u) / (N^2 sqrt(f))
  (circular check: Delta psi per orbit = -2 pi sqrt(1-3u), geodetic).
  Member ODE in the PERIODIC orbital frame:
      x'' + 2 om J x' + [om' J - om^2 I + Om^2 I - Lam_orb(tau)] x = 0,
  monodromy eigenvalues = Fermi-frame growth (conjugation by R(Delta psi)).

Laws (growth per orbit = ln max|eig M|; bands at 0.02/orbit; Om grid
geomspace(0.02,16,601)*Om_r as in the scout run):
  truth   tide + psi from RK4 coordinate transport of the tetrad
  chart   closed forms above (what the tube compiles from u(tau), E, L)
  avg     constant diag(mean Lam11, mean Lam33), om = 0 (law.md reading:
          orbit-averaged kicks, channels decoupled = the scout's avg law)
  avgkin  same constant tide, exact omega kept (steelman)
  chartQ16/chartQ12  closed forms quantized to Q fixed-point levels
  frozen  the scout's scalar drive lam = u^3 (3 gam^2 - 1), decoupled
  chan2   out-of-plane scalar channel Lam22: truth/closed + avg
"""
import json
import sys
import numpy as np
from scipy.integrate import solve_ivp


# ---------------- geodesic (Darwin) ----------------

def constants(rp, e):
    if e < 1e-12:
        L2 = rp ** 2 / (rp - 3.0)
        E2 = (1 - 2 / rp) ** 2 / (1 - 3 / rp)
        return np.sqrt(E2), np.sqrt(L2), rp
    ra = rp * (1 + e) / (1 - e)
    if ra <= 2.0 or rp <= 3.0:
        raise ValueError(f"unphysical orbit rp={rp} ra={ra}")
    num = (1 - 2 / ra) - (1 - 2 / rp)
    den = (1 - 2 / rp) / rp ** 2 - (1 - 2 / ra) / ra ** 2
    L2 = num / den
    if L2 <= 0:
        raise ValueError(f"unbound (rp,ra): L^2 = {L2} <= 0 (domain guard)")
    E2 = (1 - 2 / rp) * (1 + L2 / rp ** 2)
    return np.sqrt(E2), np.sqrt(L2), ra


def orbit_tables(rp, e, n_tau=12001):
    """u(tau) uniform over one radial period + derived tables (M = 1)."""
    E, L, ra = constants(rp, e)
    if e < 1e-12:
        u0 = 1.0 / rp
        T_r = 2 * np.pi * rp ** 2 / L
        tau = np.linspace(0.0, T_r, n_tau, endpoint=False)
        uu = np.full(n_tau, u0)
        dphi_r = 2 * np.pi
    else:
        up, ua = 1.0 / rp, 1.0 / ra
        roots = np.roots([2.0, -1.0, 2.0 / L ** 2, (E ** 2 - 1.0) / L ** 2])
        u3 = roots[(roots.real > up + 1e-12) & (np.abs(roots.imag) < 1e-9)].real[0]
        c, A = 0.5 * (up + ua), 0.5 * (up - ua)

        def rhs(psi, y):
            u = c + A * np.cos(psi)
            dphi = 1.0 / np.sqrt(2.0 * (u3 - u))
            return [dphi, dphi / (L * u ** 2)]

        sol = solve_ivp(rhs, (0.0, np.pi), [0.0, 0.0], rtol=1e-13, atol=1e-14,
                        dense_output=True, max_step=0.01)
        dphi_r = 2.0 * sol.y[0, -1]
        T_r = 2.0 * sol.y[1, -1]
        psi = np.linspace(0.0, np.pi, 8 * n_tau)[1:]
        yy = sol.sol(psi)
        tau_out, u_out = yy[1], c + A * np.cos(psi)
        g = np.linspace(0.0, T_r / 2, n_tau // 2 + 1)
        u_h = np.interp(g, tau_out, u_out)
        tau = np.linspace(0.0, T_r, n_tau, endpoint=False)
        uu = np.where(tau <= T_r / 2, np.interp(tau, g, u_h),
                      np.interp(T_r - tau, g, u_h))
    f = 1.0 - 2.0 * uu
    gam = E / np.sqrt(f)
    uph = L * uu
    ur2 = np.maximum(gam ** 2 - 1.0 - uph ** 2, 0.0)
    sgn = np.where(tau <= T_r / 2, 1.0, -1.0)  # r increases from periapsis
    ur = sgn * np.sqrt(ur2)
    return dict(tau=tau, u=uu, f=f, gam=gam, uph=uph, ur=ur, E=E, L=L,
                T_r=T_r, dphi_r=dphi_r, Om_r=2 * np.pi / T_r, ra=ra)


# ---------------- closed forms (the chart) ----------------

def closed_tables(o):
    u, f, gam, uph, ur = (o[k] for k in ('u', 'f', 'gam', 'uph', 'ur'))
    w = u ** 3
    N2 = 1.0 + ur ** 2
    E11 = -w * (2.0 + 3.0 * uph ** 2 / N2)
    E33 = w * (1.0 - 3.0 * ur ** 2 * uph ** 2 / N2)
    E13 = w * 3.0 * gam * uph * ur / N2
    E22 = w * (1.0 + 3.0 * uph ** 2)
    om = -gam * uph * u * (f - u) / (N2 * np.sqrt(f))
    return dict(L11=-E11, L33=-E33, L13=-E13, L22=-E22, om=om)


# ---------------- exact transport (truth) ----------------
# coordinate Riemann needed (equatorial, M = 1): pairs (t,r),(t,phi),(r,phi)

def transport(o):
    """Exact parallel transport of the in-plane tetrad (solve_ivp, DOP853,
    coordinate Christoffels).  Returns truth tide tables in the ORBITAL
    frame, psi, and Delta psi."""
    tau, u, f, gam, uph, ur = (o[k] for k in ('tau', 'u', 'f', 'gam', 'uph', 'ur'))
    E, L, T_r = o['E'], o['L'], o['T_r']
    n = len(tau)
    drd = ur * np.sqrt(f)          # dr/dtau (coordinate)
    utc = E / f                    # u^t
    upc = L * u ** 2               # u^phi

    def rhs(t_, y):
        u_ = float(np.interp(t_, tau, u))
        f_ = 1.0 - 2.0 * u_
        r_ = 1.0 / u_
        ut_ = float(np.interp(t_, tau, utc))
        ur_ = float(np.interp(t_, tau, drd))
        up_ = float(np.interp(t_, tau, upc))
        g010 = 1.0 / (r_ ** 2 * f_)   # Gamma^t_{tr} = Gamma^t_{rt}
        g100 = f_ / r_ ** 2           # Gamma^r_{tt}
        g111 = -g010                  # Gamma^r_{rr}
        g122 = -f_ * r_               # Gamma^r_{phiph}
        g212 = 1.0 / r_               # Gamma^ph_{rph}
        e = y.reshape(2, 3)
        out = np.empty((2, 3))
        out[:, 0] = -g010 * (ut_ * e[:, 1] + ur_ * e[:, 0])
        out[:, 1] = -g100 * ut_ * e[:, 0] - g111 * ur_ * e[:, 1] \
            + f_ * r_ * up_ * e[:, 2]
        out[:, 2] = -g212 * (ur_ * e[:, 2] + up_ * e[:, 1])
        return out.ravel()

    rp = 1.0 / u[0]
    f0 = 1.0 - 2.0 / rp
    y0 = np.array([0.0, np.sqrt(f0), 0.0, uph[0] / np.sqrt(f0), 0.0,
                   gam[0] / rp])
    sol = solve_ivp(rhs, (0.0, T_r), y0, method='DOP853', rtol=1e-12,
                    atol=1e-14, dense_output=True, max_step=T_r / 4000.0)
    Y = np.ascontiguousarray(sol.sol(tau).T).reshape(n, 2, 3)     # transported e1, e3 at grid times
    uu, ff, gg, pp, rr_, ss = u, f, gam, uph, ur, drd
    R6 = np.stack([-2.0 * uu ** 3, ff * uu, -uu / ff])          # (3, n)
    # orbital frame vectors (coordinate components)
    N2 = 1.0 + rr_ ** 2
    N = np.sqrt(N2)
    f1 = np.stack([gg * rr_ / np.sqrt(ff), N2 * np.sqrt(ff),
                   pp * rr_ * uu]) / N
    f3 = np.stack([pp / np.sqrt(ff), np.zeros(n), gg * uu]) / N
    # orbital-frame tide: DIRECT wedge contraction with f1, f3
    # (coordinate-Riemann path; independent of the closed-form algebra path)
    Af = np.stack([f1[0] * ss - f1[1] * utc,
                   f1[0] * upc - f1[2] * utc,
                   f1[1] * upc - f1[2] * ss])
    Bf = np.stack([f3[0] * ss - f3[1] * utc,
                   f3[0] * upc - f3[2] * utc,
                   f3[1] * upc - f3[2] * ss])
    E11 = np.sum(R6 * Af * Af, axis=0)
    E13 = np.sum(R6 * Af * Bf, axis=0)
    E33 = np.sum(R6 * Bf * Bf, axis=0)
    E22 = (ff * uu) * utc ** 2 * uu ** 2 - (uu / ff) * ss ** 2 * uu ** 2 \
        + (2.0 / uu) * upc ** 2 * uu ** 2
    # psi of the transported axis relative to the orbital frame
    gv = np.stack([-ff, 1.0 / ff, (1.0 / uu) ** 2])              # metric diag
    e1c = Y[:, 0, :].T  # (3, n) coordinate comps of transported e1
    d11 = np.sum(gv * e1c * f1, axis=0)
    d13 = np.sum(gv * e1c * f3, axis=0)
    psi = np.unwrap(np.arctan2(d13, d11))
    dpsi = float(psi[-1] - psi[0] + np.arctan2(d13[0], d11[0]))
    return dict(L11=-E11, L33=-E33, L13=-E13, L22=-E22, psi=psi, dpsi=dpsi)


def spectral_dpsi(psi, T_r):
    n = len(psi)
    tr = np.linspace(0.0, T_r, n, endpoint=False)
    trend = ((2.0 * psi[-1] - psi[-2]) - psi[0]) / T_r  # one-step extrapolation
    per = psi - trend * tr
    c = np.fft.rfft(per)
    fr = 2j * np.pi * np.fft.rfftfreq(n, T_r / n)
    return np.fft.irfft(c * fr, n) + trend


def spectral_d(om, T_r):
    n = len(om)
    c = np.fft.rfft(om)
    fr = 2j * np.pi * np.fft.rfftfreq(n, T_r / n)
    return np.fft.irfft(c * fr, n)


# ---------------- Floquet over the Om grid ----------------

def floquet2x2(a, b, cc, om, dom, T_r, Om_grid, sub=3):
    """Monodromy of x'' + 2 om J x' + [dom' J - om^2 I + Om^2 I - Lam] x = 0
    with Lam = [[a, cc], [cc, b]].  RK4, vectorized over Om.  Returns ln rho."""
    n = len(a)
    h = T_r / (n * sub)
    n_fine = 2 * n * sub
    grid = (np.arange(n_fine + 1) * (T_r / n_fine)) % T_r
    tq = np.linspace(0.0, T_r, n, endpoint=False)
    aq = np.interp(grid, tq, a)
    bq = np.interp(grid, tq, b)
    cq = np.interp(grid, tq, cc)
    oq = np.interp(grid, tq, om)
    dq = np.interp(grid, tq, dom)
    Om = Om_grid
    O2 = Om ** 2
    def deriv(y, i):
        x1, x3, v1, v3 = y[0], y[1], y[2], y[3]
        v1p = 2 * oq[i] * v3 + (dq[i] + cq[i]) * x3 \
            + (oq[i] ** 2 + aq[i] - O2) * x1
        v3p = -2 * oq[i] * v1 + (cq[i] - dq[i]) * x1 \
            + (oq[i] ** 2 + bq[i] - O2) * x3
        return np.stack((v1, v3, v1p, v3p))

    M = len(Om)
    y = np.zeros((4, 4, M))  # 4 basis vectors of the 4-state
    for j in range(4):
        y[j, j] = 1.0
    for k in range(n * sub):
        k1 = deriv(y, 2 * k)
        k2 = deriv(y + h / 2 * k1, 2 * k + 1)
        k3 = deriv(y + h / 2 * k2, 2 * k + 1)
        k4 = deriv(y + h * k3, 2 * k + 2)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    # conjugate back to the Fermi frame: M_F = R(Delta psi) M_orb
    dpsi = float(np.mean(om)) * T_r
    c_, s_ = np.cos(dpsi), np.sin(dpsi)
    rho = np.empty(M)
    for m in range(M):
        MM = y[:, :, m].copy()
        MM[0] = c_ * y[0, :, m] + s_ * y[1, :, m]
        MM[1] = -s_ * y[0, :, m] + c_ * y[1, :, m]
        MM[2] = c_ * y[2, :, m] + s_ * y[3, :, m]
        MM[3] = -s_ * y[2, :, m] + c_ * y[3, :, m]
        ev = np.linalg.eigvals(MM)
        rho[m] = max(np.abs(ev).max(), 1.0)
    return np.log(rho)
    grid = (np.arange(n_fine + 1) * (T_r / n_fine)) % T_r
    tq = np.linspace(0, T_r, n, endpoint=False)
    lq = np.interp(grid, tq, lam)
    w2 = Om_grid[None, :] ** 2 - alpha * lq[:, None]

    def deriv(y, i):
        return np.stack((y[1], -w2[i] * y[0], y[3], -w2[i] * y[2]))

    y = np.zeros((4, len(Om_grid)))
    y[0] = 1.0
    y[3] = 1.0
    for k in range(n * sub):
        k1 = deriv(y, 2 * k)
        k2 = deriv(y + h / 2 * k1, 2 * k + 1)
        k3 = deriv(y + h / 2 * k2, 2 * k + 1)
        k4 = deriv(y + h * k3, 2 * k + 2)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    tr = np.abs(y[0] + y[3])
    mu = np.zeros_like(tr)
    unst = tr > 2.0 + 1e-9
    mu[unst] = np.arccosh(np.clip(tr[unst] / 2.0, 1.0, 1e18))
    return mu


    out = []
    m = np.asarray(mu) > thresh
    if not m.any():
        return out
    edges = np.diff(m.astype(int))
    starts = list(np.where(edges == 1)[0] + 1)
    ends = list(np.where(edges == -1)[0] + 1)
    if m[0]:
        starts = [0] + starts
    if m[-1]:
        ends = ends + [len(m)]
    for s, e in zip(starts, ends):
        out.append(dict(center=float(0.5 * (Om_ratio[s] + Om_ratio[e - 1])),
                        lo=float(Om_ratio[s]), hi=float(Om_ratio[e - 1]),
                        peak=float(np.max(np.asarray(mu)[s:e]))))
    return out


def floquet1d(lam, T_r, Om_grid, alpha=1.0, sub=3):
    """Scalar channel x'' + (Om^2 - alpha*lam) x = 0; trace criterion."""
    n = len(lam)
    h = T_r / (n * sub)
    n_fine = 2 * n * sub
    grid = (np.arange(n_fine + 1) * (T_r / n_fine)) % T_r
    tq = np.linspace(0, T_r, n, endpoint=False)
    lq = np.interp(grid, tq, lam)
    w2 = Om_grid[None, :] ** 2 - alpha * lq[:, None]

    def deriv(y, i):
        return np.stack((y[1], -w2[i] * y[0], y[3], -w2[i] * y[2]))

    y = np.zeros((4, len(Om_grid)))
    y[0] = 1.0
    y[3] = 1.0
    for k in range(n * sub):
        k1 = deriv(y, 2 * k)
        k2 = deriv(y + h / 2 * k1, 2 * k + 1)
        k3 = deriv(y + h / 2 * k2, 2 * k + 1)
        k4 = deriv(y + h * k3, 2 * k + 2)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    tr = np.abs(y[0] + y[3])
    mu = np.zeros_like(tr)
    unst = tr > 2.0 + 1e-9
    mu[unst] = np.arccosh(np.clip(tr[unst] / 2.0, 1.0, 1e18))
    return mu


def bands(Om_ratio, mu, thresh=0.02):
    out = []
    m = np.asarray(mu) > thresh
    if not m.any():
        return out
    edges = np.diff(m.astype(int))
    starts = list(np.where(edges == 1)[0] + 1)
    ends = list(np.where(edges == -1)[0] + 1)
    if m[0]:
        starts = [0] + starts
    if m[-1]:
        ends = ends + [len(m)]
    for s, e in zip(starts, ends):
        out.append(dict(center=float(0.5 * (Om_ratio[s] + Om_ratio[e - 1])),
                        lo=float(Om_ratio[s]), hi=float(Om_ratio[e - 1]),
                        peak=float(np.max(np.asarray(mu)[s:e]))))
    return out


def quant(x, Q):
    xmax = np.max(np.abs(x))
    if xmax == 0:
        return x.copy()
    return np.round(x / xmax * Q) / Q * xmax


# ---------------- one case ----------------

def run_case(rp, e, n_om=601, n_tau=4001, sub=2):
    o = orbit_tables(rp, e, n_tau=n_tau)
    T_r, Om_r = o['T_r'], o['Om_r']
    cc = closed_tables(o)
    tr = transport(o)
    om_truth = spectral_dpsi(tr['psi'], T_r)

    # ---- validation of the chart's closed forms against transport ----
    wmax = float(np.max(o['u'] ** 3))
    val = dict(
        dL11=float(np.max(np.abs(tr['L11'] - cc['L11'])) / wmax),
        dL33=float(np.max(np.abs(tr['L33'] - cc['L33'])) / wmax),
        dL13=float(np.max(np.abs(tr['L13'] - cc['L13'])) / wmax),
        dL22=float(np.max(np.abs(tr['L22'] - cc['L22'])) / wmax),
        dom=float(np.max(np.abs(om_truth - cc['om'])) / np.max(np.abs(cc['om']))),
        dpsi_int=float(abs(np.sum(cc['om']) * (T_r / n_tau) - tr['dpsi'])
                       / max(abs(tr['dpsi']), 2 * np.pi)),
    )
    # truth channel coupling: max |L13|/wmax (the shear the scalar laws drop)
    val['shear_rel'] = float(np.max(np.abs(tr['L13'])) / wmax)

    Om = np.geomspace(0.02, 16.0, n_om) * Om_r
    Om_ratio = Om / Om_r

    laws = {}
    dom_t = spectral_d(om_truth, T_r)
    laws['truth'] = floquet2x2(tr['L11'], tr['L33'], tr['L13'], om_truth,
                               dom_t, T_r, Om, sub=sub)
    dom_c = spectral_d(cc['om'], T_r)
    laws['chart'] = floquet2x2(cc['L11'], cc['L33'], cc['L13'], cc['om'],
                               dom_c, T_r, Om, sub=sub)
    a_bar, b_bar = float(np.mean(tr['L11'])), float(np.mean(tr['L33']))
    zeros = np.zeros(n_tau)
    # avg law (law.md reading): decoupled constant channels -> analytic trace
    def mu_const(lam_bar):
        w2 = Om ** 2 - lam_bar
        t2 = np.where(w2 >= 0, 2 * np.cos(np.sqrt(np.abs(w2)) * T_r),
                      2 * np.cosh(np.sqrt(np.abs(w2)) * T_r))
        t2 = np.abs(t2)
        mu = np.zeros_like(t2)
        u_ = t2 > 2.0 + 1e-9
        mu[u_] = np.arccosh(np.clip(t2[u_] / 2.0, 1.0, 1e18))
        return mu
    laws['avg'] = np.maximum(mu_const(a_bar), mu_const(b_bar))
    laws['avgkin'] = floquet2x2(np.full(n_tau, a_bar), np.full(n_tau, b_bar),
                                zeros, om_truth, dom_t, T_r, Om, sub=sub)
    for Q, nm in ((2 ** 16, 'chartQ16'), (2 ** 12, 'chartQ12')):
        cq = {k: quant(cc[k], Q) for k in ('L11', 'L33', 'L13', 'om')}
        laws[nm] = floquet2x2(cq['L11'], cq['L33'], cq['L13'], cq['om'],
                              spectral_d(cq['om'], T_r), T_r, Om, sub=sub)
    lam_frozen = o['u'] ** 3 * (3 * o['gam'] ** 2 - 1)
    laws['frozen'] = floquet1d(lam_frozen, T_r, Om, alpha=1.0, sub=sub)
    laws['chan2'] = floquet1d(tr['L22'], T_r, Om, alpha=1.0, sub=sub)

    # convergence: sub doubled on a subsample
    idx = np.arange(0, n_om, 30)
    laws2 = floquet2x2(tr['L11'], tr['L33'], tr['L13'], om_truth, dom_t,
                       T_r, Om[idx], sub=2 * sub)
    conv = float(np.max(np.abs(laws['truth'][idx] - laws2)))

    mu_orbit = {k: (np.asarray(v) * 1.0).tolist() for k, v in laws.items()}
    res = dict(rp=rp, e=e, T_r=T_r, dphi_r=o['dphi_r'], Om_r=Om_r,
               gamma_p=float(o['gam'][0]), lam_mean=float(np.mean(lam_frozen)),
               lam_max=float(np.max(lam_frozen)),
               L11_bar=a_bar, L33_bar=b_bar, dpsi=tr['dpsi'],
               om_max=float(np.max(np.abs(om_truth))), val=val, conv=conv,
               Om_over_Om_r=Om_ratio.tolist(),
               laws=mu_orbit,
               bands={k: bands(Om_ratio, v) for k, v in mu_orbit.items()})
    return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    cases = json.loads(sys.argv[2])
    tag = sys.argv[3] if len(sys.argv) > 3 else "out"
    if cmd == "sweep":
        out = []
        for c in cases:
            r = run_case(c["rp"], c["e"])
            v = r["val"]
            print(f"rp={r['rp']:>7} e={r['e']} dpsi={r['dpsi']:8.4f} "
                  f"val(dL11)={v['dL11']:.1e} val(dom)={v['dom']:.1e} "
                  f"shear={v['shear_rel']:.3f} conv={r['conv']:.1e} "
                  f"truth_bands={len(r['bands']['truth'])} "
                  f"chart_bands={len(r['bands']['chart'])} "
                  f"avg_bands={len(r['bands']['avg'])}", file=sys.stderr)
            out.append(r)
        with open(f"results2-{tag}.json", "w") as fo:
            json.dump(out, fo)
    elif cmd == "validate":
        for c in cases:
            o = orbit_tables(c["rp"], c["e"])
            cc = closed_tables(o)
            tr = transport(o)
            om_t = spectral_dpsi(tr['psi'], o['T_r'])
            wmax = float(np.max(o['u'] ** 3))
            print(json.dumps(dict(
                rp=c["rp"], e=c["e"],
                dL11=float(np.max(np.abs(tr['L11'] - cc['L11'])) / wmax),
                dL33=float(np.max(np.abs(tr['L33'] - cc['L33'])) / wmax),
                dL13=float(np.max(np.abs(tr['L13'] - cc['L13'])) / wmax),
                dL22=float(np.max(np.abs(tr['L22'] - cc['L22'])) / wmax),
                dom=float(np.max(np.abs(om_t - cc['om'])) / np.max(np.abs(cc['om']))),
                dpsi_int=float(abs(np.sum(cc['om']) * (o['T_r'] / len(tr['psi']))
                                   - tr['dpsi']) / abs(tr['dpsi'])),
                dpsi=tr['dpsi'],
            )))
