#!/usr/bin/env python3
"""Exact-instrument run for topic fleet-doll-speed (wiki od 1/3/4).

Schwarzschild, G=c=1, M=1, equatorial plane. No finite differences and no
separation parameter enter the coefficient claims: the tidal matrix E_ab =
R_{mu nu rho sigma} e_a^mu u^nu e_b^rho u^sigma is evaluated exactly (analytic
Christoffels, analytic d/dr, Riemann by the standard formula) and projected on
the boosted static orthonormal frame at periapsis. Eigenvalues are invariant
under the spatial rotation from that frame to the parallel-transported (Fermi)
frame, so this is the fleet doll's interior tide coefficient at the moment of
transverse closest approach.

The Fermi-frame history (parallel frame + geodesic-deviation ODE + true
finite-separation geodesic pairs) is carried for the second-order-in-xi
question (predictions P5) and the FD-pollution mechanism.
"""
import math
import sys
import numpy as np

# ---------------- Schwarzschild geometry (M = 1) ----------------

def christoffel(r, th):
    """All nonzero Gamma^mu_{nu sigma} as dict, plus the same with d/dr taken."""
    f = 1.0 - 2.0 / r
    s, c = math.sin(th), math.cos(th)
    G = {}
    G[('t', 't', 'r')] = 1.0 / (r * r * f)
    G[('r', 't', 't')] = f / (r * r)
    G[('r', 'r', 'r')] = -1.0 / (r * r * f)
    G[('r', 'th', 'th')] = -f * r
    G[('r', 'ph', 'ph')] = -f * r * s * s
    G[('th', 'r', 'th')] = 1.0 / r
    G[('th', 'ph', 'ph')] = -s * c
    G[('ph', 'r', 'ph')] = 1.0 / r
    G[('ph', 'th', 'ph')] = c / s
    dG = {}
    rrf = r * r - 2.0 * r
    dG[('t', 't', 'r')] = -(2.0 * r - 2.0) / (rrf * rrf)
    dG[('r', 't', 't')] = -2.0 / r ** 3 + 6.0 / r ** 4
    dG[('r', 'r', 'r')] = (2.0 * r - 2.0) / (rrf * rrf)
    dG[('r', 'th', 'th')] = -(1.0 - 2.0 / r) + r * (-2.0 / r ** 2) * -1.0 * -1.0  # -d(fr)/dr = -(f - 2/r)
    dG[('r', 'th', 'th')] = -(f + r * (2.0 / r ** 2))
    dG[('r', 'ph', 'ph')] = -s * s * (f + 2.0 / r)
    dG[('th', 'r', 'th')] = -1.0 / r ** 2
    dG[('th', 'ph', 'ph')] = 0.0
    dG[('ph', 'r', 'ph')] = -1.0 / r ** 2
    dG[('ph', 'th', 'ph')] = 0.0
    return G, dG

IDX = {'t': 0, 'r': 1, 'th': 2, 'ph': 3}

def riemann_lower(r, th):
    """R_{mu nu rho sigma} as 4x4x4x4 numpy array, from analytic Gamma and dGamma/dr."""
    G, dG = christoffel(r, th)
    # Gamma as arrays
    Gam = np.zeros((4, 4, 4))
    dGam = np.zeros((4, 4, 4))
    for (a, b, c), v in G.items():
        Gam[IDX[a]][IDX[b]][IDX[c]] = v
        Gam[IDX[a]][IDX[c]][IDX[b]] = v
    for (a, b, c), v in dG.items():
        dGam[IDX[a]][IDX[b]][IDX[c]] = v
        dGam[IDX[a]][IDX[c]][IDX[b]] = v
    # dGamma^mu_{nu sigma} / dxi : xi = r -> dGam ; xi = th -> only -s*c and cot(th) terms
    dth = np.zeros((4, 4, 4))
    th2 = th
    dth_G_thpp = math.sin(th2) ** 2 - math.cos(th2) ** 2   # d/dth (-sin cos)
    dth_G_phthph = -1.0 / math.sin(th2) ** 2                # d/dth cot
    dth[IDX['th']][IDX['ph']][IDX['ph']] = dth_G_thpp
    dth[IDX['ph']][IDX['th']][IDX['ph']] = dth_G_phthph
    dth[IDX['ph']][IDX['ph']][IDX['th']] = dth_G_phthph
    # R^mu_{nu rho sigma} = d_rho Gam^mu_{nu sigma} - d_sigma Gam^mu_{nu rho}
    #                       + Gam^mu_{rho l} Gam^l_{nu sigma} - Gam^mu_{sigma l} Gam^l_{nu rho}
    Rup = np.zeros((4, 4, 4, 4))
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                for sig in range(4):
                    a = dGam[mu][nu][sig] if rho == 1 else (dth[mu][nu][sig] if rho == 2 else 0.0)
                    b = dGam[mu][nu][rho] if sig == 1 else (dth[mu][nu][rho] if sig == 2 else 0.0)
                    val = a - b
                    for lam in range(4):
                        val += Gam[mu][rho][lam] * Gam[lam][nu][sig]
                        val -= Gam[mu][sig][lam] * Gam[lam][nu][rho]
                    Rup[mu][nu][rho][sig] = val
    g = np.diag([-(1.0 - 2.0 / r), 1.0 / (1.0 - 2.0 / r), r * r, r * r * math.sin(th) ** 2])
    return Rup, g

def riemann(r, th):
    Rup, g = riemann_lower(r, th)
    return np.einsum('mp,pnrs->mnrs', g, Rup)

def ricci_max(r, th):
    """Max |Ricci_{ab}| = |g^{mn} R_{m a n b}|: the vacuum control."""
    Rlo = riemann(r, th)
    ginv = np.diag([-1.0 / (1.0 - 2.0 / r), (1.0 - 2.0 / r), 1.0 / r ** 2,
                    1.0 / (r ** 2 * math.sin(th) ** 2)])
    Rc = np.einsum('mn,manb->ab', ginv, Rlo)
    return np.abs(Rc).max()


# ---------------- the tide at a transverse periapsis ----------------

def tide_at_periapsis(rp, beta):
    """Exact E_ab in the observer frame (boost of static frame along phi), at
    periapsis r=rp, theta=pi/2, purely azimuthal motion, local speed beta."""
    g = 2.0  # M
    f = 1.0 - 2.0 / rp
    gam = 1.0 / math.sqrt(1.0 - beta * beta)
    th = math.pi / 2
    Rlo = riemann(rp, th)
    # orthonormal static legs (contravariant components)
    e_t = np.array([1.0 / math.sqrt(f), 0, 0, 0])
    e_r = np.array([0, math.sqrt(f), 0, 0])
    e_th = np.array([0, 0, 1.0 / rp, 0])
    e_ph = np.array([0, 0, 0, 1.0 / rp])
    u = gam * (e_t + beta * e_ph)
    legs = {'r': e_r, 'y': gam * (e_ph + beta * e_t), 'z': e_th}
    E = {}
    for ka, a in legs.items():
        for kb, b in legs.items():
            E[(ka, kb)] = np.einsum('m,n,r,s,mnrs->', a, u, b, u, Rlo)
    return E, u, Rlo

def eigen_grid():
    betas = [0.25, 0.5, 0.7, 0.9, 0.95, 0.99, 0.999]
    radii = [6.0, 8.0, 10.0, 20.0, 50.0, 100.0, 300.0]
    print("== P1/P2/P3/P4: exact periapsis eigenvalue ratios (instrument: exact Riemann projection) ==")
    print("rp/M   beta     rad_meas   rad_closed  relerr     along      z_meas    z_closed   z_relerr  z_rival")
    rows = []
    for rp in radii:
        for beta in betas:
            E, u, _ = tide_at_periapsis(rp, beta)
            gam2 = 1.0 / (1.0 - beta * beta)
            rad_closed = gam2 * (2 + beta * beta) / 2.0
            z_closed = gam2 * (1 + 2 * beta * beta)
            z_rival = gam2 * abs(1 - 2 * beta * beta)
            rad_meas = abs(E[('r', 'r')]) / (2.0 / rp ** 3)
            along = abs(E[('y', 'y')]) / (1.0 / rp ** 3)
            z_meas = abs(E[('z', 'z')]) / (1.0 / rp ** 3)
            relerr = rad_meas / rad_closed - 1.0
            zerr = z_meas / z_closed - 1.0
            rows.append((rp, beta, rad_meas, rad_closed, relerr, along, z_meas, z_closed, zerr, z_rival))
            print(f"{rp:5.0f}  {beta:6.3f}  {rad_meas:9.6f}  {rad_closed:9.6f}  {relerr:10.2e}  "
                  f"{along:8.6f}  {z_meas:9.5f}  {z_closed:9.5f}  {zerr:9.2e}  {z_rival:8.4f}")
    # cross-term should vanish (orthogonal channels)
    E, _, _ = tide_at_periapsis(20.0, 0.9)
    print(f"\ncross-terms at rp=20M beta=0.9: E_ry={E[('r','y')]:.3e} E_rz={E[('r','z')]:.3e} "
          f"E_yz={E[('y','z')]:.3e}  (zero = channels decouple)")
    return rows

# ---------------- letter-vs-cure budget line (P6) ----------------

def budget_line():
    print("\n== P6: the letter's own cap beta=0.25 (nR = c/4) ==")
    beta = 0.25
    gam2 = 1.0 / (1.0 - beta * beta)
    exact = gam2 * (2 + beta * beta) / 2.0 - 1.0
    series = 1.5 * beta ** 2 + 1.875 * beta ** 4
    print(f"radial coefficient error of the Newtonian letter at beta 0.25: "
          f"exact {100*exact:.3f}%  series(1.5b^2+1.875b^4) {100*series:.3f}%  "
          f"letter budget line O(beta^2)={100*beta**2:.2f}%")


def gammas_at(r):
    G, _ = christoffel(r, math.pi / 2)
    Gam = np.zeros((4, 4, 4))
    for (a, b, c), v in G.items():
        Gam[IDX[a]][IDX[b]][IDX[c]] = v
        Gam[IDX[a]][IDX[c]][IDX[b]] = v
    return Gam

def metric_at(r):
    return np.diag([-(1 - 2 / r), 1 / (1 - 2 / r), r * r, r * r])

def geodesic_ic(rp, beta, r0):
    fp = 1.0 - 2.0 / rp
    gam = 1.0 / math.sqrt(1.0 - beta * beta)
    Et = gam * math.sqrt(fp)
    L = rp * beta * gam
    f0 = 1.0 - 2.0 / r0
    ut = Et / f0
    uph = L / r0 ** 2
    ur = -math.sqrt(max(Et * Et - f0 * (1.0 + L * L / r0 ** 2), 0.0))
    return np.array([ut, ur, 0.0, uph]), Et, L

def rhs8(y):
    x, u = y[0:4], y[4:8]
    Gam = gammas_at(x[1])
    du = -np.einsum('mab,a,b->m', Gam, u, u)
    return np.concatenate([u.copy(), du])

def rk4_8(y, h):
    k1 = rhs8(y)
    k2 = rhs8(y + 0.5 * h * k1)
    k3 = rhs8(y + 0.5 * h * k2)
    k4 = rhs8(y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

def rhs(y):
    """y = (x[4], u[4], s[4], q[4]). Equatorial; e3 = (0,0,1/r,0) exact."""
    x, u, s, q = y[0:4], y[4:8], y[8:12], y[12:16]
    r = x[1]
    Gam = gammas_at(r)
    du = -np.einsum('mab,a,b->m', Gam, u, u)
    ds = -np.einsum('mab,a,b->m', Gam, u, s)
    dq = -np.einsum('mab,a,b->m', Gam, u, q)
    return np.concatenate([u.copy(), du, ds, dq])

def rk4(y, h):
    k1 = rhs(y)
    k2 = rhs(y + 0.5 * h * k1)
    k3 = rhs(y + 0.5 * h * k2)
    k4 = rhs(y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

def fermi_E(x, u, s, q):
    r = x[1]
    Rlo = riemann(r, math.pi / 2)
    e3 = np.array([0.0, 0.0, 1.0 / r, 0.0])
    legs = [s, q, e3]
    E = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            E[a][b] = np.einsum('m,n,r,s,mnrs->', legs[a], u, legs[b], u, Rlo)
    return E

def flyby(rp, beta, r0=300.0, h=0.25):
    """Geodesic + parallel frame from r0 in to r0 out; returns tau samples of E
    (Fermi frame, axes s,q,e3), periapsis E, exit frame, and psi(r) record."""
    u0, Et, L = geodesic_ic(rp, beta, r0)
    x = np.array([0.0, r0, math.pi / 2, 0.0])
    g = metric_at(r0)
    def gd(a, b):
        return a @ g @ b
    er = np.array([0.0, math.sqrt(1 - 2 / r0), 0.0, 0.0])
    s = er - gd(er, u0) * u0 * (-1.0)
    s = s / math.sqrt(abs(gd(s, s)))
    eph = np.array([0.0, 0.0, 0.0, 1.0 / r0])
    q = eph - gd(eph, u0) * u0 * (-1.0) - gd(eph, s) * s
    q = q / math.sqrt(abs(gd(q, q)))
    y = np.concatenate([x, u0, s, q])
    tau = 0.0
    Es, taus, rs, psis = [], [], [], []
    peri = None
    n = 0
    while True:
        # step
        ynew = rk4(y, h)
        # periapsis crossing: u^r changes sign
        if y[5] < 0 <= ynew[5] and peri is None:
            peri = (tau, fermi_E(y[0:4], y[4:8], y[8:12], y[12:16]), y[1].copy())
        y = ynew
        tau += h
        n += 1
        if n % 4 == 0 or y[1] < rp * 1.05:
            Es.append(fermi_E(y[0:4], y[4:8], y[8:12], y[12:16]))
            taus.append(tau)
            rs.append(y[1])
            rr = y[1]
            er_now = np.array([0.0, math.sqrt(1 - 2 / rr), 0.0, 0.0])
            eph_now = np.array([0.0, 0.0, 0.0, 1.0 / rr])
            svec = y[8:12]
            psis.append(math.atan2(svec @ metric_at(rr) @ eph_now,
                                   svec @ metric_at(rr) @ er_now))
        if y[1] >= r0 and tau > 10 * h:
            break
        if n > 400000:
            raise RuntimeError("no exit")
    return dict(taus=np.array(taus), Es=np.array(Es), rs=np.array(rs),
                peri=peri, psi=np.array(psis), y_exit=y, tau_exit=tau)

def dev_solve(fly, ic):
    """Deviation ODE on interpolated Fermi E. ic = (xi0_3, xidot0_3)."""
    taus, Es = fly['taus'], fly['Es']
    def Eat(t):
        return np.array([np.interp(t, taus, Es[:, i, j]) for i in range(3) for j in range(3)]).reshape(3, 3)
    h = (taus[-1] - taus[0]) / 4000.0
    xi = np.array(ic[0], float)
    xd = np.array(ic[1], float)
    t = taus[0]
    for k in range(4000):
        def acc(xv, tt):
            return -Eat(tt) @ xv
        k1x, k1v = xd, acc(xi, t)
        k2x, k2v = xd + 0.5 * h * k1v, acc(xi + 0.5 * h * k1x, t + 0.5 * h)
        k3x, k3v = xd + 0.5 * h * k2v, acc(xi + 0.5 * h * k2x, t + 0.5 * h)
        k4x, k4v = xd + h * k3v, acc(xi + h * k3x, t + h)
        xi = xi + h / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        xd = xd + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += h
    return xi

def member_geodesic(rp, beta, r0, xi0_axis, xi0, tau_exit):
    """True geodesic offset from the origin IC by xi0 along the initial Fermi axis
    (s or q or e3), same coordinate u. Returns exit separation in exit Fermi axes."""
    u0, Et, L = geodesic_ic(rp, beta, r0)
    g = metric_at(r0)
    def gd(a, b):
        return a @ g @ b
    er = np.array([0.0, math.sqrt(1 - 2 / r0), 0.0, 0.0])
    s = er - gd(er, u0) * u0 * (-1.0)
    s = s / math.sqrt(abs(gd(s, s)))
    eph = np.array([0.0, 0.0, 0.0, 1.0 / r0])
    q = eph - gd(eph, u0) * u0 * (-1.0) - gd(eph, s) * s
    q = q / math.sqrt(abs(gd(q, q)))
    e3 = np.array([0.0, 0.0, 1.0 / r0, 0.0])
    axes = {'s': s, 'q': q, 'z': e3}
    off = xi0 * axes[xi0_axis]
    # offset position: x + off (t,r,theta,phi components); theta stays pi/2 for z via dtheta
    xm = np.array([0.0 + off[0], r0 + off[1], math.pi / 2 + off[2], 0.0 + off[3]])
    # same coordinate 4-velocity (zero relative coordinate velocity at start)
    ym = np.concatenate([xm, u0.copy()])
    nsteps = int(round(tau_exit / 0.25))
    for _ in range(nsteps):
        ym = rk4_8(ym, 0.25)
    return ym

def nonlin():
    print("== P5: second-order-in-xi and the FD pollution mechanism ==")
    rp = 20.0
    for beta in (0.5, 0.9, 0.99):
        fly = flyby(rp, beta)
        tp, Eperi, rperi = fly['peri']
        gam2 = 1.0 / (1 - beta * beta)
        # control: Fermi-frame eigen at periapsis == boosted-static closed form
        ev = np.linalg.eigvalsh(Eperi)
        print(f"\nbeta={beta}: periapsis r={rperi:.4f} (target {rp}); Fermi eigen of E (units M/r^3): "
              f"{np.sort(ev)[0]/(1/rperi**3):.4f},{np.sort(ev)[1]/(1/rperi**3):.4f},{np.sort(ev)[2]/(1/rperi**3):.4f}"
              f"  closed: -{gam2*(2+beta*beta)/2*2:.4f}, +1, +{gam2*(1+2*beta*beta):.4f}")
        # frame rotation (the FD probe's pollution): psi at exit vs entry
        print(f"  parallel-frame rotation psi: entry {fly['psi'][0]:+.2e} rad, periapsis-adjacent "
              f"{fly['psi'][np.argmin(fly['rs'])]:+.2e}, exit {fly['psi'][-1]:+.2e} rad")
        for axis, idx in (('s', 0), ('q', 1), ('z', 2)):
            ic = np.zeros(3); ic[idx] = 1.0
            xi_out = dev_solve(fly, (ic, np.zeros(3)))
            S_ode = xi_out[idx]
            row = []
            for frac in (1e-4, 1e-3, 1e-2, 1.0 / 32):
                xi0 = frac * rp
                ym = member_geodesic(rp, beta, 300.0, axis, xi0, fly['tau_exit'])
                # separation at exit in exit Fermi axes
                ye = fly['y_exit']
                dx = ym[0:4] - ye[0:4]
                g = metric_at(ye[1])
                e3 = np.array([0.0, 0.0, 1.0 / ye[1], 0.0])
                comp = [dx @ g @ ye[8:12], dx @ g @ ye[12:16], dx @ g @ e3]
                S_true = comp[idx] / xi0
                row.append((frac, S_true, S_true / S_ode - 1.0))
            print(f"  axis {axis}: S_ode={S_ode:.5f}; " +
                  " ".join(f"xi/rp={f:.0e}:S={st:.5f}(d={dl:+.2e})" for f, st, dl in row))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'grid'
    # control: Ricci-flatness of the analytic Riemann at a generic point
    for (r, th) in [(20.0, math.pi/2), (7.3, 1.1)]:
        print(f"Ricci-flatness control at r={r}, th={th:.3f}: max|Ric_ab| = {ricci_max(r, th):.3e}")
    # control: Newtonian limit beta -> 0 recovers diag(-2,1,1) M/r^3
    E, _, _ = tide_at_periapsis(20.0, 1e-8)
    print(f"beta->0 control at r=20M: E_rr/(2/r^3)={E[('r','r')]/(-2/20**3):.9f} "
          f"E_yy/(1/r^3)={E[('y','y')]/(1/20**3):.9f} E_zz/(1/r^3)={E[('z','z')]/(1/20**3):.9f}")
    if mode == 'grid':
        eigen_grid()
        budget_line()
    elif mode == 'nonlin':
        nonlin()
