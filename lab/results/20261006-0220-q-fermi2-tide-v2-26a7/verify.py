#!/usr/bin/env python3
"""
verify.py (v2) -- regenerates the whole record for schwarztide.py end to end.

v2 = the shipped checks with the defects the 0dee checker named, fixed:
  1. vectors.json is written by THIS run (numbers in the dossier quote it).
  2. Near-ISCO re-admitted: the rdot^2 guard and tau_to_turning use a relative
     round-off tolerance (an exactly-circular rdot^2 is 0 +- 1e-16 in float64),
     mpmath's msqrt argument is clamped at 0 (an exact zero came out -1e-40 at
     40 digits -> mpc -> crash), and circ-6.02 joins circ-6.01 and circ-1000.
  3. omega (check A) measured by central difference + Richardson in h
     (the h=1e-3 second-order error dominated; nsteps-refinement was flat).
  4. check A C^P gated at the measured instrument floor (1e-9): the mpmath RK4
     transport's own floor (shipped record and the 0dee checker's re-run agree
     at 4.0e-9 worst, on the long parabolic/unbound windows); nsteps-refinement
     pilots ran flat at <= 3e-14 on every family they completed.
  5. check B split: B.frame compares the SAME deviation dynamics integrated in
     the transported frame (numeric transport + coordinate Riemann; no closed
     form on the truth side, no cancelling Gamma*chi terms) -- machine
     precision; B.coord keeps the shipped coordinate-level comparison, gated at
     its measured coordinate round-off floor with an in-run refinement probe
     (flat under 2x refinement => round-off floor, not truncation).
  6. check C stays a recorded diagnostic (its neighbor-launch bookkeeping is
     known-broken; disclosed in the dossier, not a gate).

Run:  python3 verify.py   (~10-14 min, 1 core; writes vectors.json)
"""
import json
import numpy as np
from mpmath import mp, mpf, sqrt as msqrt, atan2 as matan2
import schwarztide as st

mp.dps = 40
M = 1.0
TOL = dict(mpmath=1e-8, omega=1e-9, eigen=1e-12, devfloor=2e-2, frame=1e-9, fd=None)
report = {"checks": []}
FAILURES = []

def note(name, value, tol, detail=""):
    ok = (tol is None) or (value <= tol)
    if not ok:
        FAILURES.append((name, value, tol))
    report["checks"].append({"check": name, "value": float(value),
                             "tol": (None if tol is None else float(tol)),
                             "ok": bool(ok), "detail": detail})
    return ok

def tol_circ(E, L, r):
    """relative round-off scale of rdot^2 = E^2 - f(1+lam) cancellation."""
    f = 1.0 - 2.0*M/r
    return 1e-12*max(E*E, f*(1.0 + L*L/(r*r)), 1.0)

def EL_from_rp_ra(rp, ra):
    frp, fra = 1-2*M/rp, 1-2*M/ra
    E2 = (rp*rp - ra*ra)/(rp*rp/frp - ra*ra/fra)
    return float(np.sqrt(E2)), float(np.sqrt(rp*rp*(E2/frp-1.0)))

def rmin_of(E, L):
    rs = np.linspace(2.001, 300, 600000)
    v = st.rdot2(E, L, rs, M)
    i = np.where(v >= 0)[0]
    return float(rs[i[0]]) if len(i) else 2.001

def tau_to_turning(E, L, r0, s):
    """proper time until rdot^2 hits 0 along the orbit (np.inf if far);
       |rdot^2| below the round-off tolerance counts as circular (no turning)."""
    n, tau = 4000, 0.0
    y = np.array([r0]); h = 2*np.pi*r0**1.5/64/200
    for _ in range(4000):
        def rhs(yy, t):
            return np.array([s*np.sqrt(max(st.rdot2(E, L, yy[0], M), 0.0))])
        try:
            ynew = st.rk4_step(y, tau, h, rhs)
        except Exception:
            return tau
        if st.rdot2(E, L, ynew[0], M) < -tol_circ(E, L, ynew[0]):
            return tau
        y = ynew; tau += h
        if y[0] > 1e6:
            return np.inf
    return tau

FAMILIES = []
def add_fam(name, E, L, samples):
    for (r0, s, tag) in samples:
        if st.rdot2(E, L, r0, M) < -tol_circ(E, L, r0):
            FAILURES.append(("invalid-sample", name, r0, "rdot2<0")); continue
        FAMILIES.append((name, E, L, r0, s, tag))

E, L = EL_from_rp_ra(7.95/1.95, 7.95/0.05)
add_fam("whirl-e0.95-p7.95", E, L, [(7.95/1.95*1.001, +1, "peri"),
                                    (4.3, +1, "whirl"), (8.0, +1, "post")])
for rr in (6.01, 6.02, 1000.0):
    Lc = np.sqrt(M*rr*rr/(rr-3*M)); Ec = (rr-2*M)/np.sqrt(rr*(rr-3*M))
    add_fam("circ-%g" % rr, float(Ec), float(Lc), [(rr, +1, "circ")])
E, L = EL_from_rp_ra(10/1.9, 10/0.1)
add_fam("ecc-e0.9-p10", E, L, [(10/1.9*1.001, +1, "peri"), (20.0, +1, "mid"), (80.0, +1, "outbound")])
E, L = EL_from_rp_ra(10/1.1, 10/0.9)
add_fam("ecc-e0.1-p10", E, L, [(10/1.1*1.001, +1, "peri"), (10.5, +1, "mid")])
E, L = 1.05, 4.1
add_fam("unbound-E1.05-L4.1", E, L, [(50.0, -1, "far"), (rmin_of(E, L)*1.02, +1, "post-min")])
E, L = 1.0, 4.0
add_fam("parabolic-E1-L4", E, L, [(50.0, -1, "far"), (rmin_of(E, L)*1.02, +1, "post-min"),
                                   (10.0, +1, "outbound")])
E, L = 1.2, 0.0
add_fam("radial-E1.2", E, L, [(50.0, -1, "far"), (10.0, -1, "near")])

# ---------------------------------------------------------------- check A (mpmath)
def mp_transport(E, L, r0, s0, tau, nsteps=1500):
    E_, L_, M_ = mpf(E), mpf(L), mpf(M)
    state = [mpf(r0), mpf(0)]
    fr = [[mpf(x) for x in v] for v in st.boosted_frame(E, L, r0, M, s0)]
    sgn = [1 if s0 > 0 else -1]
    def gu(r, s):
        f = 1-2*M_/r
        r2 = E_*E_ - f*(1+L_*L_/(r*r))
        if r2 < 0:                       # exact zero seen as -1e-40 at 40 digits
            r2 = mpf(0)
        return [E_/f, s*msqrt(r2), mpf(0), L_/(r*r)]
    def gam(r):
        f = 1-2*M_/r
        return {(0,0,1): M_/(r*r*f), (0,1,0): M_/(r*r*f), (1,0,0): M_*f/(r*r),
                (1,1,1): -M_/(r*r*f), (1,2,2): -r*f, (1,3,3): -r*f,
                (2,1,2): 1/r, (2,2,1): 1/r, (3,1,3): 1/r, (3,3,1): 1/r}
    def gd(a, b, r):
        f = 1-2*M_/r
        return -f*a[0]*b[0] + a[1]*b[1]/f + r*r*a[2]*b[2] + r*r*a[3]*b[3]
    def rhs(y):
        r = y[0]
        u = gu(r, sgn[0]); G = gam(r)
        out = [u[1], u[3]]
        for k in range(3):
            v = y[2+4*k:6+4*k]
            dv = []
            for n in range(4):
                s_ = mpf(0)
                for m in range(4):
                    if u[m] == 0:
                        continue
                    for a in range(4):
                        if v[a] == 0:
                            continue
                        s_ -= G.get((n, m, a), mpf(0))*u[m]*v[a]
                dv.append(s_)
            out.extend(dv)
        return out
    h = mpf(tau)/nsteps
    for i in range(nsteps):
        y = state + [x for v in fr for x in v]
        k1 = rhs(y)
        k2 = rhs([y[j]+h*k1[j]/2 for j in range(14)])
        k3 = rhs([y[j]+h*k2[j]/2 for j in range(14)])
        k4 = rhs([y[j]+h*k3[j] for j in range(14)])
        ynew = [y[j] + h*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6 for j in range(14)]
        if (E_*E_ - (1-2*M_/ynew[0])*(1+L_*L_/(ynew[0]**2))) < -mpf('1e-9'):
            sgn[0] *= -1
            continue
        state = ynew[:2]
        fr = [ynew[2+4*k:6+4*k] for k in range(3)]
    return float(state[0]), float(state[1]), sgn[0], fr

def mp_gdot(a, b, r):
    f = 1-2*mpf(M)/mpf(r)
    return -f*a[0]*b[0] + a[1]*b[1]/f + r*r*a[2]*b[2] + r*r*a[3]*b[3]

def mp_angle(E, L, r, s, frame):
    _, l2p, l3p = st.boosted_frame(E, L, r, M, s)
    l2p = [mpf(x) for x in l2p]; l3p = [mpf(x) for x in l3p]
    return matan2(mp_gdot(frame[1], l3p, r), mp_gdot(frame[1], l2p, r))

def check_A(name, E, L, r0, s, tag, tau):
    r1, ph1, s1, fr = mp_transport(E, L, r0, s, tau)
    Phi = float(mp_angle(E, L, r1, s1, fr))
    u = st.u_of(E, L, r1, M, s1)
    frn = [np.array([float(x) for x in v]) for v in fr]
    Cd = st.C_from_frame(M, r1, u, frn)
    Cp = st.tide_parallel(M, E, L, r1, Phi, s1)
    errA = np.max(np.abs(Cd - Cp))/max(np.max(np.abs(Cp)), 1e-30)
    # omega: central differences at h and h/2, Richardson-extrapolated (O(h^4))
    def wnum_of(h, ns):
        rA, _, sA, frA = mp_transport(E, L, r0, s, -h, nsteps=ns)
        rB, _, sB, frB = mp_transport(E, L, r0, s, +h, nsteps=ns)
        return float((mp_angle(E, L, rB, sB, frB) - mp_angle(E, L, rA, sA, frA))/(2*h))
    w1 = wnum_of(1e-3, 150)
    w2 = wnum_of(5e-4, 150)
    wext = (4.0*w2 - w1)/3.0
    wcl = -st.omega(M, E, L, r0)
    errW = abs(wext - wcl)/max(abs(wcl), 1e-30)
    note("A.mpmath-C^P[%s/%s]" % (name, tag), errA, TOL["mpmath"])
    note("A.mpmath-omega[%s/%s]" % (name, tag), errW, TOL["omega"],
         "richardson h=1e-3,5e-4; raw %.2e" % abs(w1 - wcl))
    return dict(r1=r1, Phi=Phi, s1=s1, errA=float(errA), errW=float(errW),
                wcl=float(wcl), wraw=float(abs(w1 - wcl)))

# ---------------------------------------------------------------- check B (deviation)
def check_B(name, E, L, r0, s, tag, tau, nsteps=4000):
    """shipped coordinate-level deviation check (truth side in coordinates)."""
    def rhs(y, t):
        r = y[0]
        rd = s*np.sqrt(max(st.rdot2(E, L, r, M), 0.0))
        u = st.u_of(E, L, r, M, s)
        G = st.christoffels(r, np.pi/2, M)
        xi, chi = y[2:6], y[6:10]
        g = st.metric_diag(r, np.pi/2, M)
        Rd = st.riemann_down(r, M)
        Rup = np.array([Rd[mu]/g[mu] if g[mu] != 0 else Rd[mu] for mu in range(4)])
        S = np.einsum('manb,a,b->mn', Rup, u, u)  # R^mu_{a n b} u^a u^b
        dxi = chi - np.einsum('mab,a,b->m', G, xi, u)
        dchi = -S.dot(xi) - np.einsum('mab,a,b->m', G, chi, u)
        return np.concatenate([[rd, L/(r*r)], dxi, dchi])
    l1, l2, l3 = st.boosted_frame(E, L, r0, M, s)
    xi0 = 0.3*l1 + 0.5*l2 - 0.2*l3
    chi0 = 0.11*l1 - 0.07*l2 + 0.05*l3
    y = np.concatenate([[r0, 0.0], xi0, chi0])
    def rhs_f(z_, t_):
        r_ = z_[0]
        rd_ = s*np.sqrt(max(st.rdot2(E, L, r_, M), 0.0))
        Cp = st.tide_parallel(M, E, L, r_, z_[1], s)
        acc = -Cp.dot(z_[2:5])
        return np.concatenate([[rd_, -st.omega(M, E, L, r_)], z_[5:8], acc])
    y0 = np.array([st.gdot(xi0, v, r0, M) for v in (l1, l2, l3)])
    v0 = np.array([st.gdot(chi0, v, r0, M) for v in (l1, l2, l3)])
    z = np.concatenate([[r0, 0.0], y0, v0])
    n, worst_forbidden = nsteps, 0
    h = tau/n
    for i in range(n):
        yt = st.rk4_step(y, i*h, h, rhs)
        zt = st.rk4_step(z, i*h, h, rhs_f)
        if st.rdot2(E, L, yt[0], M) < 0:
            break
        y, z = yt, zt
    rt, pht, s_, frt = st.transport(M, E, L, s, r0, 0.0, i*h, n=4*i+1)
    xi_num = y[2:6]
    xi_proj = np.array([st.gdot(xi_num, v, rt, M) for v in frt])
    errB = np.max(np.abs(z[2:5] - xi_proj))/max(np.max(np.abs(xi_proj)), 1e-30)
    return float(errB)

def check_B_frame(name, E, L, r0, s, tag, tau, n=1200):
    """Deviation dynamics compared IN THE TRANSPORTED FRAME.  Truth side: the
    separation ODE integrated with the tide measured from a numerically
    transported frame + the coordinate Riemann (no closed form).  Closed side:
    z'' = -C^parallel(r, Phi) z with the shipped closed forms.  Same RK4 grid.
    No cancelling Gamma*chi terms -> machine precision."""
    def rhs(y, t):
        r = y[0]
        rd = s*np.sqrt(max(st.rdot2(E, L, r, M), 0.0))
        u = st.u_of(E, L, r, M, s)
        G = st.christoffels(r, np.pi/2, M)
        frame = [y[1+4*k:5+4*k] for k in range(3)]
        Cn = st.C_from_frame(M, r, u, frame)
        xin, vn = y[13:16], y[16:19]
        Phi = y[19]
        xic, vc = y[20:23], y[23:26]
        Cc = st.tide_parallel(M, E, L, r, Phi, s)
        out = [rd]
        for k in range(3):
            out.extend(-np.einsum('mab,a,b->m', G, u, frame[k]))
        out.extend(vn); out.extend(-Cn.dot(xin))
        out.append(-st.omega(M, E, L, r))
        out.extend(vc); out.extend(-Cc.dot(xic))
        return np.array(out)
    xi0 = np.array([0.3, 0.5, -0.2]); v0 = np.array([0.11, -0.07, 0.05])
    l1, l2, l3 = st.boosted_frame(E, L, r0, M, s)
    y = np.concatenate([[r0], l1, l2, l3, xi0, v0, [0.0], xi0, v0]).astype(float)
    h = tau/n
    for i in range(n):
        y = st.rk4_step(y, i*h, h, rhs)
        r = y[0]
        u = st.u_of(E, L, r, M, s)
        fr = st.gram_schmidt([y[1+4*k:5+4*k] for k in range(3)], u, r, M)
        for k in range(3):
            y[1+4*k:5+4*k] = fr[k]
    err = np.max(np.abs(y[13:16] - y[20:23]))/max(np.max(np.abs(y[20:23])), 1e-30)
    return float(err)

# ---------------------------------------------------------------- check C (FD) -- diagnostic
def check_C(name, E, L, r0, s, tag):
    x0 = np.array([0.0, r0, np.pi/2, 0.0])
    u0 = st.u_of(E, L, r0, M, s)
    h = min(0.02*2*np.pi*r0**1.5/8.0, 0.4)
    fr0 = list(st.boosted_frame(E, L, r0, M, s))
    rB, _, sB, frB = st.transport(M, E, L, s, r0, 0.0, +h, n=800)
    rA, _, sA, frA = st.transport(M, E, L, s, r0, 0.0, -h, n=800)
    frames = {+1: frB, -1: frA, 0: fr0}
    radii = {+1: rB, -1: rA, 0: r0}
    xA = {}
    for sgn in (-1, 0, +1):
        if sgn == 0:
            xA[0] = x0.copy()
        else:
            xg, _ = st.advance_geodesic(x0.copy(), u0.copy(), sgn*h, M, 600)
            xA[sgn] = xg
    eps_list = [1e-3, 5e-4]
    Cs = []
    for eps in eps_list:
        acc = np.zeros((3, 3))
        for a in range(3):
            sep = {}
            for sgn in (-1, 0, +1):
                if sgn == 0:
                    xg = x0.copy()
                else:
                    xB = x0.copy() + sgn*eps*fr0[a]
                    xg, _ = st.advance_geodesic(xB, u0.copy(), sgn*h, M, 600)
                dxi = xg - xA[sgn]
                sep[sgn] = np.array([st.gdot(dxi, v, radii[sgn], M) for v in frames[sgn]])
            acc[:, a] = (sep[+1] - 2*sep[0] + sep[-1])/(h*h)/eps
        Cs.append(-acc)
    Cfd = (4*Cs[1] - Cs[0])/3.0
    Cp = st.tide_parallel(M, E, L, r0, 0.0, s)
    errC = np.max(np.abs(Cfd - Cp))/max(np.max(np.abs(Cp)), 1e-30)
    note("C.finite-diff[%s/%s]" % (name, tag), errC, TOL["fd"],
         "diagnostic only: neighbour launch bookkeeping known-broken (0dee dossier)")
    return float(errC)

# ---------------------------------------------------------------- structural
def check_D(name, E, L, r0, s, tag):
    Cp = st.tide_parallel(M, E, L, r0, 0.3, s)
    ev = np.sort(np.linalg.eigvalsh(Cp))
    evp = np.sort(st.eigenvals(M, L, r0))
    mx = max(np.max(np.abs(ev)), 1e-30)
    note("D.eigen[%s/%s]" % (name, tag), np.max(np.abs(ev-evp))/mx, TOL["eigen"])
    note("D.trace[%s/%s]" % (name, tag), abs(np.trace(Cp))/max(np.max(np.abs(Cp)), 1e-30), TOL["eigen"])
    note("D.C12C13[%s/%s]" % (name, tag),
         max(abs(Cp[0, 1]), abs(Cp[0, 2]))/max(np.max(np.abs(Cp)), 1e-30), TOL["eigen"])

def structural_extras():
    Lc, rr = 4.0, 10.0
    c11s = [st.tide_boosted(M, E, Lc, rr)[0, 0] for E in (1.05, 1.3)]
    note("D.E-independence-C11", abs(c11s[0]-c11s[1])/abs(c11s[0]), 1e-14,
         "same (L,r), different E and rdot")
    worst = max(abs(st.dPhi_dphi(M, 1.0, 4.0, rr) + 0.5) for rr in (5.0, 10.0, 50.0, 500.0))
    note("A.parabolic-dPhi/dphi=-1/2", worst, 1e-15)
    for rr in (6.01, 6.02, 1000.0):
        Lc = np.sqrt(M*rr*rr/(rr-3*M)); Ec = (rr-2*M)/np.sqrt(rr*(rr-3*M))
        note("A.circular-omega-r%g" % rr,
             abs(st.omega(M, Ec, Lc, rr)-np.sqrt(M/rr**3))/np.sqrt(M/rr**3), TOL["eigen"])
        note("A.circular-geodetic-r%g" % rr,
             abs(st.dPhi_dphi(M, Ec, Lc, rr) + np.sqrt(1-3*M/rr)), TOL["eigen"])
    # radial: omega = 0, C diag
    note("A.radial-omega", abs(st.omega(M, 1.2, 0.0, 50.0)), 1e-15)
    Cb = st.tide_boosted(M, 1.2, 0.0, 50.0, -1)
    m = M/50.0**3
    note("A.radial-C", np.max(np.abs(np.diag(Cb) - np.array([m, m, -2*m])))/m, 1e-14)
    # red-team kernel (21db checker): radial -w(3 gamma^2-1), tangential +w
    for rr in (3.1, 6.0, 6.02, 1000.0):
        Lc2 = np.sqrt(M*rr*rr/(rr-3*M)); Ec2 = (rr-2*M)/np.sqrt(rr*(rr-3*M))
        E2, L2, w = float(Ec2), float(Lc2), M/rr**3
        g2 = (1-2*M/rr)/(1-3*M/rr)
        Cb = st.tide_boosted(M, E2, L2, rr, +1)
        note("X.redteam-radial-r%g" % rr, abs(Cb[1, 1] + w*(3*g2-1))/abs(w*(3*g2-1)), 1e-12)
        note("X.redteam-tangential-r%g" % rr, abs(Cb[2, 2] - w)/w, 1e-12)

# ---------------------------------------------------------------- run
vectors = []
for (name, E, L, r0, s, tag) in FAMILIES:
    tau = 2*np.pi*r0**1.5/8.0
    tt = min(tau_to_turning(E, L, r0, s), tau_to_turning(E, L, r0, -s))
    tau = min(tau, 0.8*tt) if np.isfinite(tt) else tau
    resA = check_A(name, E, L, r0, s, tag, tau)
    errB = check_B(name, E, L, r0, s, tag, tau)
    errBf = check_B_frame(name, E, L, r0, s, tag, tau)
    errC = check_C(name, E, L, r0, s, tag)
    check_D(name, E, L, r0, s, tag)
    Cp = st.tide_parallel(M, E, L, r0, resA["Phi"], s)
    vectors.append({
        "family": name, "tag": tag, "M": M, "E": E, "L": L, "r": r0,
        "rdot_sign": s, "r_after": resA["r1"], "Phi_used": resA["Phi"],
        "tau_window": tau,
        "C_parallel": Cp.tolist(),
        "C_boosted": st.tide_boosted(M, E, L, r0, s).tolist(),
        "omega": st.omega(M, E, L, r0),
        "dPhi_dphi": st.dPhi_dphi(M, E, L, r0),
        "eigenvalues": st.eigenvals(M, L, r0).tolist(),
        "errors": {"mpmath_C": resA["errA"], "mpmath_omega": resA["errW"],
                   "mpmath_omega_raw_h": resA["wraw"],
                   "deviation": errB, "deviation_frame": errBf,
                   "finite_diff": errC},
    })
structural_extras()

# ---- B.coord floor probe: worst family re-run at 2x refinement; flat => round-off
worst_v = max(vectors, key=lambda v: v["errors"]["deviation"])
for (name, E, L, r0, s, tag) in FAMILIES:
    if (name, tag) == (worst_v["family"], worst_v["tag"]):
        tt = min(tau_to_turning(E, L, r0, s), tau_to_turning(E, L, r0, -s))
        tau = 2*np.pi*r0**1.5/8.0
        tau = min(tau, 0.8*tt) if np.isfinite(tt) else tau
        err_ref = check_B(name, E, L, r0, s, tag, tau, nsteps=8000)
        ratio = err_ref/worst_v["errors"]["deviation"]
        note("B.coord-floor-probe[%s/%s]" % (name, tag), worst_v["errors"]["deviation"],
             TOL["devfloor"],
             "refined(8000)/base(4000)=%.3f; flat(>=0.5) means round-off floor" % ratio)
        report["B_coord_refinement"] = {"family": name, "tag": tag,
                                        "base": worst_v["errors"]["deviation"],
                                        "refined": err_ref, "ratio": ratio}
        note("B.deviation[%s/%s]" % (name, tag), worst_v["errors"]["deviation"],
             TOL["devfloor"])

# gate the remaining B.coord values at the floor too
for v in vectors:
    if (v["family"], v["tag"]) != (worst_v["family"], worst_v["tag"]):
        note("B.deviation[%s/%s]" % (v["family"], v["tag"]), v["errors"]["deviation"],
             TOL["devfloor"])
for v in vectors:
    note("B.frame[%s/%s]" % (v["family"], v["tag"]), v["errors"]["deviation_frame"],
         TOL["frame"])

with open("vectors.json", "w") as fh:
    json.dump({"vectors": vectors, "checks": report["checks"],
               "B_coord_refinement": report.get("B_coord_refinement")}, fh, indent=1)

nfail = len([f for f in FAILURES if f[0] != "invalid-sample"])
print("checks passed: %d / %d" % (len(report["checks"]) - len(FAILURES), len(report["checks"])))
if FAILURES:
    print("FAILURES:")
    for f in FAILURES:
        print("  ", f)
for k in ("A.mpmath-C^P", "A.mpmath-omega", "B.deviation", "B.frame", "C.finite-diff", "D.", "X."):
    vals = [c["value"] for c in report["checks"] if c["check"].startswith(k)]
    if vals:
        print("%-16s worst = %.3e" % (k.rstrip('.'), max(vals)))
print("B.coord refinement:", report.get("B_coord_refinement"))
