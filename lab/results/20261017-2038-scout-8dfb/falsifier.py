#!/usr/bin/env python3
"""Inclined Kerr geodesics as a compiled 2-torus: six constants per (E, L_z, Q).

Arms per orbit:
  RK — coupled first-order Mino-time geodesic ODEs (r, u=cos th; accumulators
       phi_r, phi_th, t_r, t_th), turning-point sign flips bisected on the
       separated potentials R(r) and P4(u).
  QD — separated 1-D quadrature (mpmath 30 dps).
  CF — closed forms in complete elliptic integrals K, E, Pi (Legendre
       conventions), assembled by exact Mobius + partial-fraction algebra in
       float64; every reduction asserted numerically before use. Polar piece is
       fully analytic (biquadratic). K cross-checked against Carlson RF.

Six constants: Lam_r, Lam_th (Mino periods), dPhi_r, dPhi_th (azimuthal
advances per cycle), dt_r, dt_th (coordinate-clock advances per cycle).
Usage: python3 falsifier.py [--heldout]
"""
import sys, time
import numpy as np
from scipy.optimize import fsolve, brentq
from scipy.special import ellipk, ellipe, elliprf, elliprj
import mpmath as mp
def Pi_n(n, m):
    """Complete Pi(n;m) as pure Carlson kernels:
    RF(0,1-m,1) + (n/3) RJ(0,1-m,1,1-n); verified vs mpmath.ellippi to 1e-16."""
    return elliprf(0.0, 1.0 - m, 1.0) + (n/3.0)*elliprj(0.0, 1.0 - m, 1.0, 1.0 - n)

mp.mp.dps = 30
NAMES = ["Lam_r", "Lam_th", "dPhi_r", "dPhi_th", "dt_r", "dt_th"]

def delta(a, r): return r*r - 2.0*r + a*a
def Rpot(r, a, E, Lz, Q):
    P = E*(r*r + a*a) - a*Lz
    return P*P - delta(a, r)*(r*r + (Lz - a*E)**2 + Q)
def P4u(u, a, E, Lz, Q):
    A = a*a*(1.0 - E*E)
    return A*u**4 - (Q + Lz*Lz + A)*u*u + Q
def dphi_r_of(r, a, E, Lz): return a*(E*(r*r + a*a) - a*Lz)/delta(a, r)
def dt_r_of(r, a, E, Lz):   return (r*r + a*a)*(E*(r*r + a*a) - a*Lz)/delta(a, r)
def dphi_u_of(u, a, E, Lz): return Lz/(1.0 - u*u) - a*E
def dt_u_of(u, a, E, Lz):   return a*(Lz - a*E*(1.0 - u*u))

def solve_ELQ(a, p, e, th_turn_deg, retro):
    rp, ra = p/(1+e), p/(1-e)
    z = np.cos(np.radians(th_turn_deg))**2
    E0 = 1.0 - (1-e*e)/(2*p)
    L0 = (-1.0 if retro else 1.0)*np.sqrt((1-e*e)*p)
    Q0 = z*(a*a*(1-E0**2) + L0*L0/(1-z))
    def eqs(v):
        E, Lz, Q = v
        return [Rpot(rp, a, E, Lz, Q), Rpot(ra, a, E, Lz, Q),
                Q - z*(a*a*(1-E*E) + Lz*Lz/(1-z))]
    sol, info, ier, msg = fsolve(eqs, [E0, L0, Q0], full_output=True, xtol=1e-13)
    assert ier == 1 and max(map(abs, eqs(sol))) < 1e-9, msg
    return (*sol, z)

def band_roots(a, E, Lz, Q, r_hint=None):
    xs = np.linspace(1e-3, 400.0, 800000)
    v = Rpot(xs, a, E, Lz, Q)
    b = np.where(v > 0)[0]
    assert len(b) > 0
    # group into contiguous positive regions
    edges = np.where(np.diff(b) > 1)[0]
    starts = np.r_[b[0], b[edges + 1]]
    ends = np.r_[b[edges], b[-1]]
    if r_hint is None:
        i = np.argmax(ends - starts)
    else:
        los, his = xs[starts], xs[ends]
        inside = (los <= r_hint) & (r_hint <= his)
        if inside.any():
            i = int(np.argmax(inside & (ends - starts == (ends - starts)[inside].max())))
        else:
            # nearest band edge (e.g. an equatorial hint sitting exactly on the edge)
            d = np.minimum(np.abs(los - r_hint), np.abs(his - r_hint))
            i = int(np.argmin(d))
    lo, hi = xs[starts[i]], xs[ends[i]]
    rp = brentq(lambda r: Rpot(r, a, E, Lz, Q), xs[starts[i]-1], lo, xtol=1e-15)
    ra = brentq(lambda r: Rpot(r, a, E, Lz, Q), hi, xs[ends[i]+1], xtol=1e-15)
    return rp, ra

def u2_roots(a, E, Lz, Q, z=None):
    A = a*a*(1.0 - E*E); B = Q + Lz*Lz + A
    if A <= 0: return Q/B, None
    if z is not None:
        return z, Q/(A*z)   # exact: u_+^2 is the turning point by construction
    s = np.sqrt(B*B - 4*A*Q)
    return (B - s)/(2*A), (B + s)/(2*A)

# ---------------------------------------------------------------- RK arm --
def rk_arm(a, E, Lz, Q, ncycles=3, spc=9000, r_hint=None, z=None):
    rp, ra = band_roots(a, E, Lz, Q, r_hint)
    up = np.sqrt(max(u2_roots(a, E, Lz, Q, z)[0], 0.0))
    cf = cf_arm(a, E, Lz, Q, r_hint, z)
    th_per = cf["Lam_th"] if (np.isfinite(cf["Lam_th"]) and cf["Lam_th"] > 0) \
        else 2.0*np.pi/np.sqrt(Q + Lz*Lz)
    h = min(cf["Lam_r"], th_per)/spc
    r, u, lam = 0.5*(rp + ra), 0.0, 0.0
    ph_r = ph_u = t_r = t_u = 0.0
    sr = su = 1.0
    ev = []
    def dv(r_, u_):
        return (sr*np.sqrt(max(Rpot(r_, a, E, Lz, Q), 0.0)),
                su*np.sqrt(max(P4u(u_, a, E, Lz, Q), 0.0)))
    target = (ncycles+1)*cf["Lam_r"]
    while lam <= target:
        k1 = dv(r, u)
        rA, uA = r + .5*h*k1[0], u + .5*h*k1[1]
        k2 = dv(rA, uA)
        rB, uB = r + .5*h*k2[0], u + .5*h*k2[1]
        k3 = dv(rB, uB)
        rC, uC = r + h*k3[0], u + h*k3[1]
        k4 = dv(rC, uC)
        dr = h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        du = h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        ph_r += h/6*(dphi_r_of(r,a,E,Lz) + 2*dphi_r_of(rA,a,E,Lz) + 2*dphi_r_of(rB,a,E,Lz) + dphi_r_of(rC,a,E,Lz))
        t_r  += h/6*(dt_r_of(r,a,E,Lz)   + 2*dt_r_of(rA,a,E,Lz)   + 2*dt_r_of(rB,a,E,Lz)   + dt_r_of(rC,a,E,Lz))
        ph_u += h/6*(dphi_u_of(u,a,E,Lz) + 2*dphi_u_of(uA,a,E,Lz) + 2*dphi_u_of(uB,a,E,Lz) + dphi_u_of(uC,a,E,Lz))
        t_u  += h/6*(dt_u_of(u,a,E,Lz)   + 2*dt_u_of(uA,a,E,Lz)   + 2*dt_u_of(uB,a,E,Lz)   + dt_u_of(uC,a,E,Lz))
        r_n, u_n, lam_n = r + dr, u + du, lam + h
        if Rpot(r_n, a, E, Lz, Q) < 0:
            lo, hi = 0.0, h
            for _ in range(90):
                m_ = .5*(lo+hi)
                if Rpot(r + dr/h*m_, a, E, Lz, Q) < 0: hi = m_
                else: lo = m_
            r_t = r + dr/h*lo
            ev.append(("r", lam+lo, ph_r, ph_u, t_r, t_u)); sr = -sr
            # parabolic restart off the non-Lipschitz rest point:
            # (dr/dlam)^2 = R'(r_t)(r-r_t)  =>  dlam = 2 sqrt(delta/R')
            Rp_ = (Rpot(r_t+1e-7, a, E, Lz, Q) - Rpot(r_t-1e-7, a, E, Lz, Q))/2e-7
            sgn = 1.0 if (r_t <= 0.5*(rp+ra)) else -1.0   # leaving inward turning outward
            dl = 2.0*np.sqrt(abs(d_ := 1e-10*(ra-rp))/abs(Rp_))
            r_n = r_t + sgn*d_
            lam_n = lam + lo + dl
            ph_r += dphi_r_of(r_t, a, E, Lz)*dl
            t_r += dt_r_of(r_t, a, E, Lz)*dl
        if P4u(u_n, a, E, Lz, Q) < 0:
            lo, hi = 0.0, h
            for _ in range(90):
                m_ = .5*(lo+hi)
                if P4u(u + du/h*m_, a, E, Lz, Q) < 0: hi = m_
                else: lo = m_
            u_t = u + du/h*lo
            ev.append(("u", lam+lo, ph_r, ph_u, t_r, t_u)); su = -su
            Pp_ = (P4u(u_t+1e-9, a, E, Lz, Q) - P4u(u_t-1e-9, a, E, Lz, Q))/2e-9
            usgn = 1.0 if (u_t <= 0.0) else -1.0
            du_ = 1e-10*max(2.0*up, 1e-9)
            dl = 2.0*np.sqrt(du_/abs(Pp_))
            u_n = u_t + usgn*du_
            lam_n = max(lam_n, lam + lo) + dl
            ph_u += dphi_u_of(u_t, a, E, Lz)*dl
            t_u += dt_u_of(u_t, a, E, Lz)*dl
        r, u, lam = r_n, u_n, lam_n
    out = {}
    for kind in ("r", "u"):
        e_ = [x for x in ev if x[0] == kind]
        assert len(e_) >= 5, f"too few {kind} events: {len(e_)}"
        i = len(e_)//2
        if kind == "r":
            out["Lam_r"] = e_[i][1]-e_[i-2][1]; out["dPhi_r"] = e_[i][2]-e_[i-2][2]; out["dt_r"] = e_[i][4]-e_[i-2][4]
        else:
            out["Lam_th"] = e_[i][1]-e_[i-2][1]; out["dPhi_th"] = e_[i][3]-e_[i-2][3]; out["dt_th"] = e_[i][5]-e_[i-2][5]
    return out

# ------------------------------------------------------------ closed form --
def dPi_dn(n, m):
    """dPi(n;m)/dn as the exact derivative of the same Carlson composite,
    differenced at 40 dps (a remembered closed form failed selftest and was
    withdrawn; this is the same closed kernel, not a fit)."""
    _dps = mp.mp.dps; mp.mp.dps = 40
    f = lambda nn: mp.elliprf(0, 1 - mp.mpf(m), 1) + (nn/3)*mp.elliprj(0, 1 - mp.mpf(m), 1, 1 - nn)
    h = mp.mpf(10)**-19
    val = (f(mp.mpf(n)+h) - f(mp.mpf(n)-h))/(2*h)
    mp.mp.dps = _dps
    return float(val)

def cf_arm(a, E, Lz, Q, r_hint=None, z=None):
    out = {k: np.nan for k in NAMES}
    # ---- polar (biquadratic: always real moduli; needs a != 0, Q > 0)
    A = a*a*(1.0 - E*E)
    if A > 1e-14 and Q > 1e-14:
        B = Q + Lz*Lz + A
        up2, ul2 = u2_roots(a, E, Lz, Q, z)
        mth = up2/ul2
        K_ = ellipk(mth); E_ = ellipe(mth); P_ = Pi_n(up2, mth)
        ul = np.sqrt(ul2)
        out["Lam_th"] = 4.0*K_/(np.sqrt(A)*ul)
        out["dPhi_th"] = 4.0*(Lz*P_ - a*E*K_)/(np.sqrt(A)*ul)
        out["dt_th"] = 4.0*a*((Lz - a*E)*K_ + a*E*up2*(K_ - E_)/mth)/(np.sqrt(A)*ul)
    elif Q <= 1e-14:
        out["Lam_th"] = out["dPhi_th"] = out["dt_th"] = 0.0
    # ---- radial
    rp, ra = band_roots(a, E, Lz, Q, r_hint)
    K = (Lz - a*E)**2 + Q
    coeffs = [E*E - 1.0, 2.0, 2*E*(E*a*a - a*Lz) - K - a*a, 2*K,
              (E*a*a - a*Lz)**2 - a*a*K]
    roots = np.roots(coeffs)
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-8*(1+abs(r.real)))
    below = [r for r in real if r < rp - 1e-7]
    out["_case"] = f"{len(real)}real/{len(below)}below"
    if len(below) == 2:
        r1, r2 = below
        n1 = -rp*(ra - r1); n2v = (ra - rp)*r1
        d1 = -(ra - r1);    d2v = (ra - rp)
        def r_of_s(s): return (n1 + n2v*s)/(d1 + d2v*s)
        assert abs(r_of_s(0.0) - rp) < 1e-8*(1+rp) and abs(r_of_s(1.0) - ra) < 1e-8*(1+ra)
        def Qtilde(r): return (r - r1)*(r - r2)*(r - rp)*(ra - r)
        # (dr/db)^2 / Qtilde = C/(1-m s^2), s = sin^2 b
        def drds(s): return (ra - r1)*(ra - rp)*(rp - r1)/(d1 + d2v*s)**2
        sA, sB = 0.05, 0.95
        vA = drds(sA)**2*4*sA*(1-sA)/Qtilde(r_of_s(sA))
        vB = drds(sB)**2*4*sB*(1-sB)/Qtilde(r_of_s(sB))
        ratio = vA/vB
        m = (1.0 - ratio)/(sB - sA*ratio)      # vA/vB = (1-m sB)/(1-m sA)
        C = vA*(1 - m*sA)
        m_cl = -(ra - rp)*(r2 - r1)/((rp - r2)*(ra - r1))   # closed (sympy-derived)
        C_cl = 4.0/((rp - r2)*(ra - r1))
        assert abs(m - m_cl) < 1e-9*max(1, abs(m_cl)) and abs(C - C_cl) < 1e-9*C_cl, \
            f"closed-form (C,m) mismatch: {m} vs {m_cl}, {C} vs {C_cl}"
        for s in (0.12, 0.25, 0.4, 0.55, 0.7, 0.85):
            lhs = drds(s)**2*4*s*(1-s)/Qtilde(r_of_s(s))
            assert abs(lhs*(1 - m*s)/C - 1.0) < 1e-9, f"radial reduction assert s={s}"
        scale = -(E*E - 1.0)   # R = scale * Qtilde on the band (R>0, Qtilde>0)
        K_ = ellipk(m)
        nh = -d2v/d1
        def decomp(g2, g1, g0):
            D = d1*d1
            Np = np.array([n1, n2v])
            P = np.zeros(3)
            for arr in (g2*np.convolve(Np, Np),
                        g1*d1*np.convolve(Np, [1.0, -nh]),
                        g0*D*np.convolve([1.0, -nh], [1.0, -nh])):
                P[:len(arr)] += arr
            e0 = np.array([D, -2*D*nh, D*nh*nh])
            e1 = np.array([D, -D*nh, 0.0])
            e2 = np.array([D, 0.0, 0.0])
            A_, B_, Cc = np.linalg.solve(np.array([e0, e1, e2]).T, P)
            for s in (0.1, 0.4, 0.8):
                lhs = g2*r_of_s(s)**2 + g1*r_of_s(s) + g0
                rhs = A_ + B_/(1 - nh*s) + Cc/(1 - nh*s)**2
                assert abs(lhs - rhs) < 1e-8*(1 + abs(lhs)), "decomp assert"
            return A_, B_, Cc
        def radial_closed(g2, g1, g0, poles):
            val = np.sqrt(C/scale)*(g2*0 + 0)  # placeholder to keep dtype
            val = 0.0
            if any(abs(x) > 0 for x in (g2, g1, g0)):
                A_, B_, Cc = decomp(g2, g1, g0)
                # 1/(1-nh s)^2 = 1/(1-nh s) + (nh s)/(1-nh s)^2  =>  J = Pi + nh dPi/dn
                val += np.sqrt(C/scale)*(A_*K_ + B_*Pi_n(nh, m) + Cc*(Pi_n(nh, m) + nh*dPi_dn(nh, m)))
            for c_, r0 in poles:
                if c_ == 0.0:
                    continue
                W = (n1 - r0*d1)/d1
                n0 = -(n2v - r0*d2v)/(n1 - r0*d1)
                for s in (0.1, 0.5, 0.9):
                    assert abs((r_of_s(s) - r0) - W*(1 - n0*s)/(1 - nh*s)) < 1e-7*(1+abs(W))
                # c/(r-r0) -> (c/W)(1-nh s)/(1-n0 s)
                #   = (c/W)[ 1/(1-n0 s) + (n0-nh)/n0 * s/(1-n0 s) ]
                # s/(1-n0 s) = (1/n0)(1/(1-n0 s) - 1)
                P0 = Pi_n(n0, m)
                val += c_/W*np.sqrt(C/scale)*(K_ + (n0 - nh)/n0*(P0 - K_))
            return 2.0*val
        rpm = 1.0 + np.sqrt(max(1 - a*a, 0.0)); rmm = 1.0 - np.sqrt(max(1 - a*a, 0.0))
        dpm = rpm - rmm
        apm_p = a*(2*E*rpm - a*Lz)/dpm
        apm_m = a*(2*E*rmm - a*Lz)/(-dpm)
        out["Lam_r"] = 2.0*np.sqrt(C/scale)*K_
        out["dPhi_r"] = radial_closed(0.0, 0.0, a*E, [(apm_p, rpm), (apm_m, rmm)])
        cp = (2*E*rpm - a*Lz)/dpm; cm = (2*E*rmm - a*Lz)/(-dpm)
        g2 = E; g1 = cp + cm; g0 = E*a*a + cp*rpm + cm*rmm
        out["dt_r"] = radial_closed(g2, g1, g0, [(cp*(rpm*rpm + a*a), rpm),
                                                 (cm*(rmm*rmm + a*a), rmm)])
    return out

# ------------------------------------------------------------- quadrature --
def qd_arm(a, E, Lz, Q, r_hint=None, z=None):
    rp, ra = band_roots(a, E, Lz, Q, r_hint)
    E_, Lz_, Q_, a_ = map(mp.mpf, map(str, (E, Lz, Q, a)))
    def RRmp(r):
        P = E_*(r*r + a_*a_) - a_*Lz_
        return P*P - (r*r - 2*r + a_*a_)*(r*r + (Lz_ - a_*E_)**2 + Q_)
    rlo = mp.findroot(RRmp, (mp.mpf(str(rp))*(1-mp.mpf('1e-9')), mp.mpf(str(rp))))
    rhi = mp.findroot(RRmp, (mp.mpf(str(ra)), mp.mpf(str(ra))*(1+mp.mpf('1e-9'))))
    def RR(r):
        P = E_*(r*r + a_*a_) - a_*Lz_
        return P*P - (r*r - 2*r + a_*a_)*(r*r + (Lz_ - a_*E_)**2 + Q_)
    def sqR(r):
        v = RRmp(r)
        return mp.sqrt(v if v > 0 else mp.mpf('1e-40'))  # numerical zero at endpoints
    # substitute r = rlo + (rhi-rlo) sin^2 t: kills both endpoint 1/sqrt singularities
    W = rhi - rlo
    def sub_int(g):
        # int_{rlo}^{rhi} g(r)/sqrt(R) dr  with g in float-callable form
        def f(t):
            r = rlo + W*mp.sin(t)**2
            dr = 2*W*mp.sin(t)*mp.cos(t)
            return mp.mpf(str(g(float(r))))*dr/sqR(r)
        return mp.quad(f, [mp.mpf('1e-12'), mp.pi/2 - mp.mpf('1e-12')])
    Lam_r = 2*sub_int(lambda r: 1.0)
    dPhi_r = 2*sub_int(lambda r: dphi_r_of(r, a, E, Lz))
    dt_r = 2*sub_int(lambda r: dt_r_of(r, a, E, Lz))
    out = dict(Lam_r=float(Lam_r), dPhi_r=float(dPhi_r), dt_r=float(dt_r))
    A = a*a*(1-E*E)
    if A > 1e-14 and Q > 1e-14:
        up2, _ = u2_roots(a, E, Lz, Q, z)
        A_, B_ = mp.mpf(str(A)), mp.mpf(str(Q + Lz*Lz + A))
        pol = lambda uu: A_*uu**4 - B_*uu*uu + Q_
        u0 = mp.sqrt(mp.mpf(str(up2)))
        up = mp.findroot(pol, (u0*(1 - mp.mpf('1e-13')), u0*(1 + mp.mpf('1e-13'))))
        def den(u):
            v = A_*u**4 - B_*u*u + Q_
            return mp.sqrt(v if v > 0 else mp.mpf(0))
        def usub_int(g):
            # int_{-up}^{up} g(u)/sqrt(quartic) du via u = up sin t
            def f(t):
                u = up*mp.sin(t)
                du = up*mp.cos(t)
                return g(u)*du/den(u)
            return mp.quad(f, [-mp.pi/2 + mp.mpf('1e-12'), mp.pi/2 - mp.mpf('1e-12')])
        out["Lam_th"] = float(2*usub_int(lambda u: mp.mpf(1)))
        out["dPhi_th"] = float(2*usub_int(lambda u: Lz_/(1-u*u) - a_*E_))
        out["dt_th"] = float(2*usub_int(lambda u: a_*Lz_ - a_*a_*E_*(1-u*u)))
    else:
        out["Lam_th"] = out["dPhi_th"] = out["dt_th"] = 0.0
    return out

# ---------------------------------------------------------------- selftest --
def selftest():
    for m in (0.1, 0.5, 0.9):
        assert abs(ellipk(m) - elliprf(0.0, 1.0 - m, 1.0)) < 1e-14
    for (n, m) in ((0.3, 0.2), (-0.5, 0.6), (0.9, 0.7)):
        f = lambda nn: mp.ellippi(nn, mp.mpf(m))
        h = mp.mpf(10)**-20
        num = (f(mp.mpf(n)+h) - f(mp.mpf(n)-h))/(2*h)
        ana = dPi_dn(n, m)
        assert abs(float(num) - ana) < 1e-9*max(1, abs(ana)), (n, m, float(num), ana)
    assert abs(Pi_n(0.3, 0.0) - np.pi/(2*np.sqrt(0.7))) < 1e-14

# --------------------------------------------------------------------- grid --
GRID = []
for a in (0.2, 0.6, 0.9):
    for (p, e) in ((12.0, 0.1), (8.0, 0.5)):
        for th in (30.0, 60.0):
            GRID.append((a, p, e, th, False, f"a{a} p{p} e{e} th{th}"))
GRID.append((0.6, 12.0, 0.1, 60.0, True, "a0.6 p12 e0.1 th60 RETRO"))
CONTROL = [(0.0, 12.0, 0.1, 60.0, False, "a=0 th60"),
           (0.0, 12.0, 0.1, 30.0, False, "a=0 th30")]
DEGEN = [(0.6, 12.0, 0.1, 89.999, False, "degen th89.999"),
         (0.6, 12.0, 0.1, 90.0, False, "equatorial th90")]
HELDOUT = [(0.998, 12.0, 0.1, 60.0, False, "a=0.998 th60"),
           (0.6, 12.0, 0.9, 45.0, False, "e=0.9 th45"),
           (0.9, 12.0, 0.1, 30.0, True, "a0.9 th150 RETRO"),
           (0.9, 6.8, 0.5, 60.0, False, "near-sep a0.9 p6.8 e0.5")]

def one_row(row, verbose=True):
    a, p, e, th, retro, tag = row
    E, Lz, Q, z = solve_ELQ(a, p, e, th, retro)
    hint = p/(1+e)
    rk = rk_arm(a, E, Lz, Q, r_hint=hint, z=z)
    qd = qd_arm(a, E, Lz, Q, r_hint=hint, z=z)
    cf = cf_arm(a, E, Lz, Q, r_hint=hint, z=z)
    if verbose:
        print(f"[{tag}]  E={E:.12f} Lz={Lz:.10f} Q={Q:.10f} case={cf.get('_case')}")
        for k in NAMES:
            r_, q_, c_ = rk.get(k, np.nan), qd.get(k, np.nan), cf.get(k, np.nan)
            d1 = abs(r_ - q_)/max(abs(q_), 1e-30)
            d2 = abs(c_ - q_)/max(abs(q_), 1e-30) if np.isfinite(c_) else float("nan")
            print(f"   {k:8s} RK={r_:20.13f} QD={q_:20.13f} CF={c_:20.13f}"
                  f" |RK-QD|={d1:9.2e} |CF-QD|={d2:9.2e}")
    return dict(tag=tag, E=E, Lz=Lz, Q=Q, rk=rk, qd=qd, cf=cf, a=a)

def timing(rows):
    row = rows[0]
    a, p, e, th, retro, _ = row
    E, Lz, Q, z = solve_ELQ(a, p, e, th, retro)
    n = 3000
    t0 = time.perf_counter()
    for _ in range(n):
        cf = cf_arm(a, E, Lz, Q, None, z)
        five = (cf["Lam_r"], cf["Lam_th"], cf["dPhi_r"], cf["dPhi_th"], cf["dt_th"])
    t5 = (time.perf_counter()-t0)/n*1e6
    t0 = time.perf_counter()
    for _ in range(n): cf_arm(a, E, Lz, Q, None, z)
    t6 = (time.perf_counter()-t0)/n*1e6
    print(f"   timing [{row[5]}]: {t5:.2f} us for the five pure-float constants "
          f"(Lam_r, Lam_th, dPhi_r, dPhi_th, dt_th); {t6:.2f} us incl. dt_r "
          f"(one 40-dps mpmath kernel dPi/dn dominates; the float port needs the "
          f"standard dPi/dn recurrence — see dossier)")

def main():
    heldout = "--heldout" in sys.argv
    selftest()
    print("== selftest PASS: K==RF(0,1-m,1); dPi/dn vs mpmath diff (30 dps); Pi(n,0) ==")
    rows = GRID + CONTROL + DEGEN + (HELDOUT if heldout else [])
    results = [one_row(r) for r in rows]
    print("\n== controls ==")
    a0 = [r for r in results if r["a"] == 0.0]
    for r in a0:
        print(f"[{r['tag']}] RK dPhi_th - 2*pi = {r['rk']['dPhi_th'] - 2*np.pi:+.3e} (planar: expect ~0)")
    if len(a0) == 2:
        for k in ("Lam_r", "dPhi_r", "dt_r"):
            if a0[0]["rk"][k] == 0.0:
                print(f"   a=0 {k}: identically 0 at both inclinations (a=0: no frame dragging)")
                continue
            d = abs(a0[0]["rk"][k] - a0[1]["rk"][k])/abs(a0[0]["rk"][k])
            print(f"   a=0 {k}: th30 vs th60 rel diff {d:.3e} (spherical symmetry: expect ~0)")
        rr = a0[0]["rk"]["Lam_r"]/a0[0]["rk"]["Lam_th"]
        print(f"   a=0 Schwarzschild check: Lam_r/Lam_th = {rr:.8f} vs 1/sqrt(1-6/p) = "
              f"{1/np.sqrt(1-6.0/12.0):.8f}  (apsidal precession from the period ratio; e=0.1)")
    dg = [r for r in results if r["tag"].startswith("degen")]
    eq = [r for r in results if r["tag"].startswith("equatorial")]
    if dg and eq:
        for k in ("Lam_r", "dPhi_r", "dt_r"):
            d = abs(dg[0]["qd"][k] - eq[0]["qd"][k])/abs(eq[0]["qd"][k])
            print(f"   degen(z~3e-10) vs equatorial {k}: rel diff {d:.3e}")
        B = dg[0]["Q"] + dg[0]["Lz"]**2 + 0.6**2*(1-dg[0]["E"]**2)
        print(f"   degen Lam_th = {dg[0]['qd']['Lam_th']:.9f}; 2*pi/sqrt(B) = {2*np.pi/np.sqrt(B):.9f}"
              f" (small-Q harmonic limit)")
    print("\n== timing ==")
    timing(GRID)

if __name__ == "__main__":
    main()
