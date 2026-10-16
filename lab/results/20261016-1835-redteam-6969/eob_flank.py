#!/usr/bin/env python3
"""Red-team 20261016-1835: 'nu only in the energy map' at strong field.

Doll (r3 v3 'eob-doll'): relative motion = exact Schwarzschild geodesic at
(E_eff, L_eff), real energy via the 2PN-accurate EOB map
  H_real^R = M sqrt(1 + 2 nu (E_eff - 1)),  j identical.
Truth: reduced 2PN ADM Hamiltonian (Buonanno-Damour 1999, eq 10a-c), planar,
invariant quadrature dphi/dr at fixed real invariants (E_NR, j).

One quadrature, three Hamiltonians: adm2, adm1 (drop H4), schw (exact
Schwarzschild effective; checks the analytic doll formula).
Units G=c=M=1.  All float; runtime a few seconds.
"""
import numpy as np, json, math, sys

GLN = 96
_x, _w = np.polynomial.legendre.leggauss(GLN)

def bound_constants(p, e):
    """Exact Schwarzschild (E, L) from Darwin's (p, e); ported from
    xtask/src/gr_oracle_extended.rs bound_constants (M=1 units)."""
    E = math.sqrt(((p - 2.0)**2 - 4.0*e*e) / (p*(p - 3.0 - e*e)))
    L = p / math.sqrt(p - 3.0 - e*e)
    return E, L

# ---------------- Hamiltonians: H(P2, x, r, nu), P2 = x + j^2/r^2 ----------
def adm(P2, x, r, nu, order):
    w = 1.0/r
    h = 0.5*P2 - w
    if order >= 1:
        h += (-0.125*(1.0-3.0*nu)*P2*P2 - 0.5*w*((3.0+nu)*P2 + nu*x) + 0.5*w*w)
    if order >= 2:
        h += ( (1.0/16.0)*(1.0-5.0*nu+5.0*nu*nu)*P2**3
             + (w/8.0)*((5.0-20.0*nu-3.0*nu*nu)*P2*P2 - 2.0*nu*nu*P2*x - 3.0*nu*nu*x*x)
             + 0.5*w*w*((5.0+8.0*nu)*P2 + 3.0*nu*x) - 0.25*w**3*(1.0+3.0*nu) )
    return h

def adm_partials(P2, x, r, nu, order):
    w = 1.0/r
    hP = 0.5
    hx = 0.0
    if order >= 1:
        hP += -0.25*(1.0-3.0*nu)*P2 - 0.5*w*(3.0+nu)
        hx += -0.5*w*nu
    if order >= 2:
        hP += (3.0/16.0)*(1.0-5.0*nu+5.0*nu*nu)*P2*P2 \
              + (w/4.0)*(5.0-20.0*nu-3.0*nu*nu)*P2 - (w/4.0)*nu*nu*x \
              + 0.5*w*w*(5.0+8.0*nu)
        hx += -(w/8.0)*(2.0*nu*nu*P2 + 6.0*nu*nu*x) + 1.5*w*w*nu
    return hP, hx

def schw_NR(P2, x, r, nu=0.0, order=99):
    """Exact Schwarzschild effective energy minus 1, as function of pr^2=x.
    E^2 = (1-2/r)(1 + L^2/r^2) + (1-2/r)^2 pr^2, L^2 = r^2*(P2 - x);
    pr is the canonical momentum conjugate to r."""
    A = 1.0 - 2.0/r
    L2 = r*r*(P2 - x)
    h2 = A*(1.0 + L2/(r*r)) + A*A*x
    if h2 < 0.0:
        return 1e9  # inside the horizon: never allowed
    return math.sqrt(h2) - 1.0

def schw_partials(P2, x, r, nu=0.0, order=99):
    A = 1.0 - 2.0/r
    L2 = r*r*(P2 - x)
    h2 = A*(1.0 + L2/(r*r)) + A*A*x
    if h2 < 0.0:
        return 0.0, 0.0
    H = math.sqrt(h2)
    hP = 0.5*A/H          # dh2/dP2 = A (at fixed x)
    hx = 0.5*(A*A - A)/H          # dh2/dx = -A + A^2 (at fixed P2)
    return hP, hx


HAMS = {"adm2": (adm, adm_partials), "adm1": (adm, adm_partials), "schw": (schw_NR, schw_partials)}
def Hval(ham, x, r, j, nu, order):
    P2 = x + j*j/(r*r)
    return HAMS[ham][0](P2, x, r, nu, order)
def solve_x(ham, r, j, nu, order, E):
    """Newton for x >= 0 with H(x)=E."""
    x = max(0.0, 2.0*(E + 1.0/r) - j*j/(r*r))
    for _ in range(60):
        P2 = x + j*j/(r*r)
        h = HAMS[ham][0](P2, x, r, nu, order)
        hP, hx = HAMS[ham][1](P2, x, r, nu, order)
        d = hP + hx  # dH/dx
        if d == 0.0: break
        step = (E - h)/d
        x += step
        if x < 0.0: x = 0.0
        if abs(step) < 1e-15*(1.0+abs(x)): break
    return x

def turning_points(ham, E, j, nu, order, r_ref):
    """Turning points of the allowed annulus nearest r_ref (F<=0 inside)."""
    F = lambda r: Hval(ham, 0.0, r, j, nu, order) - E
    def bisect(lo, hi):
        flo = F(lo)
        for _ in range(200):
            mid = 0.5*(lo+hi)
            fm = F(mid)
            if (flo < 0.0) == (fm < 0.0):
                lo, flo = mid, fm
            else:
                hi = mid
            if hi - lo < 1e-14*(1.0+hi): break
        return 0.5*(lo+hi)
    rs = np.geomspace(max(1.05, 0.25*r_ref), 4.0*r_ref, 40000)
    Fr = np.array([F(r) for r in rs])
    inside = Fr <= 0.0
    # contiguous allowed segments
    segs = []
    i = 0
    while i < len(inside):
        if inside[i]:
            j2 = i
            while j2 < len(inside) and inside[j2]:
                j2 += 1
            segs.append((i, j2-1))
            i = j2
        else:
            i += 1
    if not segs:
        return None
    # choose the segment whose log-midpoint is closest to r_ref
    best = min(segs, key=lambda s: abs(math.sqrt(rs[s[0]]*rs[s[1]]) - r_ref))
    i0, i1 = best
    lo = rs[i0-1] if i0 > 0 else rs[i0]*0.999
    hi = rs[i1+1] if i1 < len(rs)-1 else rs[i1]*1.001
    rp = bisect(lo, rs[i0])
    ra = bisect(rs[i1], hi)
    return rp, ra

def delta_phi(ham, E, j, nu, order, r_ref, panels=8, nper=64):
    """Total azimuthal angle Phi per radial cycle (not the advance k=Phi-2pi)."""
    tp = turning_points(ham, E, j, nu, order, r_ref)
    if tp is None: return float("nan")
    rp, ra = tp
    gx, gw = np.polynomial.legendre.leggauss(nper)
    tot2 = 0.0
    for a in range(panels):
        a0 = (math.pi/2)*a/panels
        a1 = (math.pi/2)*(a+1)/panels
        th = a0 + (a1 - a0)*0.5*(gx + 1.0)
        wts = gw*(a1 - a0)*0.5
        for t, wgt in zip(th, wts):
            r = rp + (ra - rp)*math.sin(t)**2
            sc = math.sin(t)*math.cos(t)
            x = solve_x(ham, r, j, nu, order, E)
            if x <= 1e-300: continue
            P2 = x + j*j/(r*r)
            hP, hx = HAMS[ham][1](P2, x, r, nu, order)
            tot2 += wgt*( (j/(r*r))*hP/(math.sqrt(x)*(hP + hx)) )*sc
    return 2.0 * 2.0*(ra - rp)*tot2

def k_advance(ham, E, j, nu, order, r_ref):
    phi = delta_phi(ham, E, j, nu, order, r_ref)
    return phi - 2.0*math.pi

def chi_advance(p, e):
    """Exact Schwarzschild advance via the Darwin chi-integral (law.md's own
    dphi/dchi = sqrt(p/(p-6-2 e cos chi))), an independent second path."""
    gx, gw = np.polynomial.legendre.leggauss(400)
    chi = math.pi*(gx + 1.0)
    f = np.sqrt(p/(p - 6.0 - 2.0*e*np.cos(chi)))
    return math.pi*float(np.sum(gw*f)) - 2.0*math.pi

def _V(ham, r, j, nu, order):
    return Hval(ham, 0.0, r, j, nu, order)

def circ_k_and_omega(ham, j, nu, order, r_guess):
    """Circular orbit of this Hamiltonian at angular momentum j (min of V_j
    near r_guess): returns (k = 2pi(Om_phi/om_r - 1), Om_phi)."""
    # grid-scan the well (avoid the plunge region at small r), then refine
    gr = (math.sqrt(5.0) - 1.0)/2.0
    grid = np.linspace(0.65*r_guess, 2.2*r_guess, 400)
    vals = [_V(ham, r, j, nu, order) for r in grid]
    i = int(np.argmin(vals))
    span = 2.0*(grid[1] - grid[0])
    a, b = max(0.62*r_guess, grid[i] - span), min(2.25*r_guess, grid[i] + span)
    c, d = b - gr*(b - a), a + gr*(b - a)
    for _ in range(200):
        if _V(ham, c, j, nu, order) < _V(ham, d, j, nu, order):
            b, d = d, c
            c = b - gr*(b - a)
        else:
            a, c = c, d
            d = a + gr*(b - a)
    r_c = 0.5*(a + b)
    h = 1e-4*r_c
    B = (-_V(ham, r_c-2*h, j, nu, order) + 16*_V(ham, r_c-h, j, nu, order)
         - 30*_V(ham, r_c, j, nu, order) + 16*_V(ham, r_c+h, j, nu, order)
         - _V(ham, r_c+2*h, j, nu, order))/(12*h*h)
    P2 = j*j/(r_c*r_c)
    hP, hx = HAMS[ham][1](P2, 0.0, r_c, nu, order)
    A = 2.0*(hP + hx)
    if A*B <= 0.0:
        return float("nan"), float("nan"), r_c  # no stable well here (truncation artifact)
    om_r = math.sqrt(A*B)
    om_phi = 2.0*j*hP/(r_c*r_c)
    return 2.0*math.pi*(om_phi/om_r - 1.0), om_phi, r_c

def doll_energy_map(E_eff, nu):
    if nu == 0.0:
        return E_eff - 1.0
    return (math.sqrt(1.0 + 2.0*nu*(E_eff - 1.0)) - 1.0)/nu

# ---------------- ISCO (circular-orbit stability in each Hamiltonian) ------
def circ_j2(ham, r, nu):
    """j^2 for circular orbit at r: dH/dr|x=0 = 0."""
    H00 = lambda y: Hval(ham, 0.0, r, math.sqrt(max(y,1e-12)), nu, 2)
    # numeric dH00/dr via richardson on r
    def dHdr(y):
        h = 1e-5*r
        f = lambda rr: Hval(ham, 0.0, rr, math.sqrt(max(y, 1e-12)), nu, 2)
        return (f(r-2*h) - 8*f(r-h) + 8*f(r+h) - f(r+2*h))/(12*h)
    y = r  # Newtonian start
    for _ in range(80):
        d = dHdr(y)
        # numeric derivative wrt y by central diff of dHdr
        dy = max(1e-8, 1e-8*y)
        dd = (dHdr(y+dy) - dHdr(y-dy))/(2*dy)
        if dd == 0.0: break
        step = -d/dd
        y += step
        if y <= 0.0: y = 1e-8
        if abs(step) < 1e-13*(1.0+y): break
    return y

def kappa2(ham, r, nu, j2c):
    """Second radial derivative of V_j(r) = H(x=0, r; j=j_circ(r0)) at r0."""
    j = math.sqrt(j2c)
    f = lambda rr: Hval(ham, 0.0, rr, j, nu, 2)
    h = 1e-4*r
    return (-f(r-2*h) + 16*f(r-h) - 30*f(r) + 16*f(r+h) - f(r+2*h))/(12*h*h)


def isco_adm(nu, ham="adm2"):
    rs = np.linspace(3.5, 30.0, 800)
    prev = None
    for r in rs:
        j2c = circ_j2(ham, r, nu)
        k2 = kappa2(ham, r, nu, j2c)
        if prev is not None and prev > 0.0 >= k2:
            # bisect on r
            lo, hi = r - (rs[1]-rs[0]), r
            for _ in range(80):
                mid = 0.5*(lo+hi)
                if kappa2(ham, mid, nu, circ_j2(ham, mid, nu)) > 0.0: lo = mid
                else: hi = mid
            return 0.5*(lo+hi)
        prev = k2
    return None

def main():
    out = {"controls": {}, "grid": [], "isco": {}}
    # ---- C0: machinery vs analytic doll (exact Schwarzschild quadrature) ----
    worst = 0.0
    for p in (8.0, 10.0, 15.0, 20.0, 30.0, 50.0, 100.0):
        for e in (0.3, 0.6):   # e=0 degenerates in the quad control
            E, L = bound_constants(p, e)
            k_exact = chi_advance(p, e)
            k_quad = k_advance("schw", E - 1.0, L, 0.0, 99, p)
            worst = max(worst, abs(k_quad/k_exact - 1.0))
    out["controls"]["C0_schw_quad_vs_analytic_maxrel"] = worst

    # ---- C1: ADM2 at nu=0 vs exact Schwarzschild quad (truncation residual) -
    c1 = []
    for p in (10.0, 20.0, 50.0, 100.0):
        E, L = bound_constants(p, 0.3)
        k_exact = k_advance("schw", E - 1.0, L, 0.0, 99, p)
        k_adm = k_advance("adm2", E - 1.0, L, 0.0, 2, p)
        c1.append({"p": p, "e": 0.3, "resid_rel": k_adm/k_exact - 1.0})
    out["controls"]["C1_adm2_nu0_vs_exact"] = c1


    # ---- grid ----
    for p in (8.0, 10.0, 15.0, 20.0, 30.0, 50.0, 100.0):
        for e in (0.0, 0.3, 0.6):
            E_eff, L = bound_constants(p, e)
            k_ana = 2.0*math.pi*(1.0/math.sqrt(1.0 - 6.0/p) - 1.0)
            row = {"p": p, "e": e, "k_doll_ana": k_ana}
            for nu in (0.0, 0.05, 0.125, 0.25):
                E_real = doll_energy_map(E_eff, nu)
                if e == 0.0:
                    k_adm2, om2, rc2 = circ_k_and_omega("adm2", L, nu, 2, p)
                    k_adm1, om1, rc1 = circ_k_and_omega("adm1", L, nu, 1, p)
                else:
                    k_adm2 = k_advance("adm2", E_real, L, nu, 2, p)
                    k_adm1 = k_advance("adm1", E_real, L, nu, 1, p)
                k_schw = k_advance("schw", E_eff - 1.0, L, 0.0, 99, p) if e > 0 else k_ana
                row[f"nu{nu}"] = {
                    "E_NR": E_real,
                    "om_phi_2PN": om2 if e == 0.0 else None,
                    "om_phi_doll": p**-1.5 if e == 0.0 else None,
                    "k_adm2": k_adm2,
                    "k_adm1": k_adm1,
                    "k_doll_quad": k_schw,
                    "eps_doll_vs_2PN": k_schw/k_adm2 - 1.0 if k_adm2 == k_adm2 else float("nan"),
                }
            # nu-dependent 2PN term beyond the energy map (clean, O(nu u^2)):
            k2_25 = row["nu0.25"]["k_adm2"]; k2_0 = row["nu0.0"]["k_adm2"]
            k1_25 = row["nu0.25"]["k_adm1"]; k1_0 = row["nu0.0"]["k_adm1"]
            row["nu_term_2PN_rel"] = (k2_25 - k2_0 - (k1_25 - k1_0))/k2_0
            out["grid"].append(row)

    # ---- ISCO ----
    for nu in (0.0, 0.05, 0.125, 0.25):
        out["isco"][f"nu{nu}"] = isco_adm(nu)
    out["isco"]["doll"] = 6.0
    print(json.dumps(out, indent=1))
    with open(sys.argv[1] if len(sys.argv) > 1 else "out.json", "w") as f:
        json.dump(out, f, indent=1)

if __name__ == "__main__":
    main()
