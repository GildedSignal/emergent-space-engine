#!/usr/bin/env python3
"""The separatrix (zoom-whirl) wedge vs representation.md L67's premise:
"a kick updates the cycle by a multiply-add" (linear update of the compiled cycle).

Instrument: exact equatorial Kerr bound-orbit cycle constants by quadrature.
M = 1, Kerr parameter a in [0,1), conserved (E, L) timelike, Q = 0 (equatorial).
  Delta(r) = r^2 - 2r + a^2,  P(r) = E(r^2+a^2) - aL,  C = L - aE
  R(r) = P^2 - Delta (r^2 + C^2)                [quartic; leading coeff E^2-1 < 0]
  dr/dl = +-sqrt(R)/r^2,  dphi/dl = (C + aP/Delta)/r^2,
  dt/dl = (-a(aE-L) + (r^2+a^2)P/Delta)/r^2
Bound orbit: 4 real roots r1<r2<r3<r4, motion r2..r3 (r2 = periapsis), r2 > r_+.
With r = m + d cos(chi) the turning-point square roots cancel exactly:
  Dphi = 2 Int_0^pi F(r)/sqrt((-cR)(r-r1)(r4-r)) dchi  (smooth), same for t, tau.
"""
import numpy as np

def roots_of_R(a, E, L):
    c4 = E*E - 1.0
    B1 = E*a*a - a*L
    C = L - a*E
    coeffs = [c4, 2.0, 2*E*B1 - a*a - C*C, 2*C*C, B1*B1 - a*a*C*C]
    r = np.roots(coeffs)
    return np.sort(r.real[np.abs(r.imag) < 1e-9 * (1 + np.abs(r.real))])

def horizon(a):
    return 1.0 + np.sqrt(1.0 - a*a)

def is_bound(a, E, L):
    if E >= 1.0 or E <= 0.0:
        return False
    rr = roots_of_R(a, E, L)
    if len(rr) != 4:
        return False
    r1, r2, r3, r4 = rr
    return r2 > horizon(a) + 1e-9 and r3 > r2 + 1e-9

def cycle(a, E, L, n=8192):
    """Exact per-radial-cycle constants (Dphi, Dt, Dtau) by smooth quadrature."""
    rr = roots_of_R(a, E, L)
    if len(rr) != 4:
        raise ValueError("plunge/unbound")
    r1, r2, r3, r4 = rr
    if r2 <= horizon(a):
        raise ValueError("inside horizon")
    cR = E*E - 1.0
    m, d = 0.5*(r2+r3), 0.5*(r3-r2)
    chi = np.linspace(0.0, np.pi, n)
    r = m + d*np.cos(chi)
    Delta = r*r - 2*r + a*a
    P = E*(r*r + a*a) - a*L
    C = L - a*E
    F = C + a*P/Delta                        # = r^2 dphi/dl
    T = -a*(a*E - L) + (r*r + a*a)*P/Delta   # = r^2 dt/dl
    lam = 1.0/np.sqrt((-cR)*(r-r1)*(r4-r))
    gtt = -(1.0 - 2.0/r)
    gtphi = -2.0*a/r
    gphphi = r*r + a*a + 2.0*a*a/r
    grr = r*r/Delta
    tdot = T/(r*r); phidot = F/(r*r)
    rdot2 = ((-cR)*(r-r1)*(r4-r)*(d*np.sin(chi))**2)/(r**4)
    taudot = np.sqrt(np.maximum(-(gtt*tdot*tdot + 2*gtphi*tdot*phidot
                                  + gphphi*phidot*phidot + grr*rdot2), 0.0))
    w = np.full(n, np.pi/(n-1)); w[0] *= 0.5; w[-1] *= 0.5
    Dphi = 2.0*np.sum((F*lam)*w)
    Dt = 2.0*np.sum((T*lam)*w)
    Dtau = 2.0*np.sum((taudot*(r*r)*lam)*w)
    return Dphi, Dt, Dtau, (r1, r2, r3, r4)

def dphi_schw_independent(L, E, n=20001):
    """a=0 check by an algebraically different route: u-space, the letter's own
    R(u) = (E^2-1)/L^2 + 2u/L^2 - u^2 + 2u^3, psi-substitution in u."""
    ur = np.sort(np.roots([2.0, -1.0, 2.0/L**2, (E*E-1)/L**2]).real)
    ua_, up_, uc_ = ur
    c, A = 0.5*(ua_+up_), 0.5*(up_-ua_)
    psi = np.linspace(0.0, np.pi, n)
    uu = c + A*np.cos(psi)
    g = 1.0/np.sqrt(2*(uc_-uu))
    w = np.full(n, np.pi/(n-1)); w[0]*=0.5; w[-1]*=0.5
    return 2.0*np.sum(g*w)

def separatrix_E(a, L, nscan=250):
    """E_sep(L): top of the bound window in E at fixed L (bisect bound->plunge)."""
    Ebound = None
    for E in np.linspace(0.90, 0.9999999, nscan):
        if is_bound(a, E, L):
            Ebound = E
            break
    if Ebound is None:
        raise ValueError("no bound orbit found in scan")
    Elo, Ehi = Ebound, Ebound + 1e-4
    step = 1e-4
    while is_bound(a, Ehi, L) and Ehi < 1.0 - 1e-12:
        Elo = Ehi
        step *= 8.0
        Ehi = min(1.0 - 1e-12, Ehi + step)
    for _ in range(80):
        Em = 0.5*(Elo+Ehi)
        if is_bound(a, Em, L): Elo = Em
        else: Ehi = Em
        if Ehi - Elo < 1e-15: break
    return Elo

def _below(a, L, nscan=250):
    """low edge of the bound window (circular side): scan down."""
    Ebound = None
    for E in np.linspace(0.9999999, 0.5, nscan):
        if is_bound(a, E, L):
            Ebound = E
            break
    return Ebound if Ebound is not None else 0.9

def rk_kerr_cycle(a, E, L, nmax=2_000_000, hs=0.02):
    """Direct geodesic integration (RK4 in affine parameter with turning-point
    bisection): returns phi at successive periapsis passages. Pure-float math."""
    from math import sqrt
    rr = roots_of_R(a, E, L); r1, r2, r3, r4 = rr
    a2 = a*a
    rmid = 0.5*(r2+r3)
    def Rd_(r):
        P = E*(r*r+a2) - a*L
        return P*P - (r*r-2*r+a2)*(r*r+(L-a*E)**2)
    def f(r, sg):
        Rd = Rd_(r)
        rd = sg*sqrt(Rd if Rd > 0.0 else 0.0)/(r*r)
        Delta = r*r - 2*r + a2
        phid = ((L-a*E) + a*(E*(r*r+a2)-a*L)/Delta)/(r*r)
        return rd, phid
    r, phi, sgn = r3, 0.0, -1.0
    phi_at_peri = []
    hs2, hs6 = hs/2, hs/6
    for i in range(nmax):
        rd1, pd1 = f(r, sgn)
        rd2, pd2 = f(r+hs2*rd1, sgn)
        rd3, pd3 = f(r+hs2*rd2, sgn)
        rd4, pd4 = f(r+hs*rd3, sgn)
        dr = hs6*(rd1+2*rd2+2*rd3+rd4)
        dp = hs6*(pd1+2*pd2+2*pd3+pd4)
        r2n = r + dr
        if Rd_(r2n) < 0.0:
            lo, hi = 0.0, hs
            for _ in range(80):
                mid = 0.5*(lo+hi)
                if Rd_(r + (mid/hs)*dr) < 0.0: hi = mid
                else: lo = mid
            r = r + (lo/hs)*dr
            phi = phi + (lo/hs)*dp
            if r < rmid:
                phi_at_peri.append(phi)
                if len(phi_at_peri) >= 3:
                    return phi_at_peri
            sgn = -sgn
        else:
            phi = phi + dp
            r = r2n
    return phi_at_peri

def controls():
    print("=== controls ===", flush=True)
    a = 0.0
    L = 4.2
    E = 0.5*(separatrix_E(a, L) + _below(a, L))
    D1, Dt, Dtau, rr = cycle(a, E, L)
    D2 = dphi_schw_independent(L, E)
    p = 2.0/(1.0/rr[2]+1.0/rr[1]); e = (rr[2]-rr[1])/(rr[2]+rr[1])
    print(f"C1 a=0 L={L} E={E:.6f}: Dphi(chi)={D1:.12f} Dphi(u-sub)={D2:.12f} rel={abs(D1-D2)/D1:.2e}")
    print(f"   advance={D1-2*np.pi:.6f} 1PN 6pi/p={6*np.pi/p:.6f} ratio={(D1-2*np.pi)/(6*np.pi/p):.4f} (p={p:.2f}, e={e:.3f})")
    D1b = cycle(a, E, L, n=2048)[0]
    print(f"C2 Simpson 2048 vs 8192 rel: {abs(D1b-D1)/D1:.2e}")
    aK = 0.9; LK = 3.2
    EK = 0.5*(separatrix_E(aK, LK) + _below(aK, LK))
    DphiK, DtK, DtauK, rrK = cycle(aK, EK, LK)
    peris = rk_kerr_cycle(aK, EK, LK, hs=0.02)
    sp = [peris[1]-peris[0], peris[2]-peris[1]]
    print(f"C3 Kerr a=0.9 L={LK} E={EK:.6f}: RK spacings {sp[0]:.9f} {sp[1]:.9f} "
          f"repeat-ratio={sp[1]/sp[0]:.10f}; quad Dphi={DphiK:.9f} rel={abs(sp[1]-DphiK)/DphiK:.2e}")
    return dict(C3_repeat=sp[1]/sp[0], C3_quad_rel=abs(sp[1]-DphiK)/DphiK,
                C1_rel=abs(D1-D2)/D1)

def main():
    out = controls()
    print("=== decisive: the wedge ===", flush=True)
    kicks = {"q48": 2.0**-48, "q32": 2.0**-32, "q20": 2.0**-20,
             "k1e-4": 1e-4, "k1e-3": 1e-3}
    ladder = np.logspace(-2, -13, 23)
    for aK, L, name in [(0.0, 4.2, "Schw L4.2"), (0.5, 3.2, "a.5pro L3.2"),
                        (0.9, 3.2, "a.9pro L3.2"), (0.998, 2.6, "a.998pro L2.6")]:
        Esep = separatrix_E(aK, L)
        print(f"--- {name}: E_sep={Esep:.12f}", flush=True)
        rows = []
        for d_ in ladder:
            drel = d_*abs(Esep)
            E = Esep - drel
            if not is_bound(aK, E, L): continue
            D0 = cycle(aK, E, L)[0]
            h = drel/50.0
            if not (is_bound(aK, E-h, L) and is_bound(aK, E+h, L)): continue
            dDdE = (cycle(aK, E+h, L)[0]-cycle(aK, E-h, L)[0])/(2*h)
            row = {"delta_rel": d_, "Dphi": D0, "dDphi_dE": dDdE}
            for kn, ke in kicks.items():
                if ke*abs(E) < drel and is_bound(aK, E+ke*abs(E), L):
                    Dk = cycle(aK, E+ke*abs(E), L)[0]
                    row[kn] = abs(Dk - D0 - dDdE*ke*abs(E))/max(abs(Dk), 1e-300)
            rows.append(row)
        for row in rows:
            s = f"delta={row['delta_rel']:.0e} Dphi={row['Dphi']:9.2f} dD/dE={row['dDphi_dE']:.2e}"
            for kn in kicks:
                if kn in row:
                    s += f" {kn}:{row[kn]:.1e}"
            print(s, flush=True)
        dd = np.array([r['delta_rel'] for r in rows]); DD = np.array([r['Dphi'] for r in rows])
        m_ = (dd < 1e-4) & (dd > 1e-12)
        if m_.sum() > 4:
            A = np.vstack([np.ones(m_.sum()), np.log10(dd[m_])]).T
            slope, itc = np.linalg.lstsq(A, DD[m_], rcond=None)[0]
            print(f"   fit Dphi ~= {slope:.2f}*log10(1/delta) + {itc:.2f} rad/decade")
            out[f"slope|{name}"] = slope
        out[f"rows|{name}"] = rows
    # inspiral walk: the letter's chained multiply-add vs exact recompiles
    aK = 0.998; L = 2.6
    Esep = separatrix_E(aK, L)
    E = Esep - 1e-3*abs(Esep)
    D0 = cycle(aK, E, L)[0]
    h = 1e-3*abs(Esep)/50.0
    dDdE0 = (cycle(aK, E+h, L)[0]-cycle(aK, E-h, L)[0])/(2*h)
    dk = 1e-5*abs(E)
    phi_exact, phi_lin = 0.0, 0.0
    Dlin = D0
    nsteps = 0
    while Esep - E > 20*dk and nsteps < 4000:
        phi_exact += cycle(aK, E, L)[0]
        phi_lin += Dlin
        Dlin = Dlin + dDdE0*dk    # the letter's multiply-add (stored derivative)
        E = E + dk
        nsteps += 1
    err = abs(phi_exact-phi_lin)
    print(f"=== walk a=0.998 pro: {nsteps} kicks dE={dk:.1e}: exact={phi_exact:.1f} lin={phi_lin:.1f} "
          f"err={err:.2f} rad = {err/(2*np.pi):.2f} cycles wrong")
    out['walk'] = (phi_exact, phi_lin, nsteps)
    # blind spot: uniform seeds vs the wedge
    rng = np.random.default_rng(382)
    for aK, Lrange in [(0.9, (2.5, 4.5)), (0.998, (1.8, 4.5))]:
        tot = near6 = near9 = 0
        for Lv in rng.uniform(*Lrange, 1200):
            try:
                Es = separatrix_E(aK, Lv)
            except ValueError:
                continue
            if Es < 0.5 or Es > 1.0: continue
            E = rng.uniform(0.9, Es)   # uniform over the deep-bound to separatrix range
            if not is_bound(aK, E, Lv): continue
            tot += 1
            if (Es-E)/abs(Es) < 1e-6: near6 += 1
            if (Es-E)/abs(Es) < 1e-9: near9 += 1
        f6, f9 = near6/max(tot,1), near9/max(tot,1)
        print(f"=== blind spot a={aK}: {tot} bound uniform seeds: frac d<1e-6 = {f6:.2e}, d<1e-9 = {f9:.2e}")
        out[f"blind|{aK}"] = (tot, f6, f9)
    # wedge magnitude at the key's own quantum floor
    aK = 0.998; L = 2.6
    Esep = separatrix_E(aK, L)
    E = Esep - 2.0**-48
    Dq = cycle(aK, E, L)[0] if is_bound(aK, E, L) else float('nan')
    print(f"=== closest representable key (one q48 from sep): Dphi={Dq:.1f} rad = {Dq/(2*np.pi):.1f} whirls")
    out['floor_Dphi'] = Dq
    import json
    with open("wedge_results.json", "w") as f:
        json.dump({k: v for k, v in out.items() if not str(k).startswith("rows|")}, f, indent=1, default=str)
    return out

if __name__ == "__main__":
    main()
