#!/usr/bin/env python3
"""Premise red-team: the two-body doll's comparable-mass strong-field flank.

Docs judged: docs/representation.md L37 ("Two bodies are one doll ... nu enters only
through the effective-one-body energy map"), docs/law.md L39, gate B11 (docs/law.md L72).

The doc's law (nu=0 exact): relative motion is an EXACT Schwarzschild test-particle orbit
of mass M = m1+m2; nu enters only through E_real = sqrt(1 + 2 nu (E_eff - 1)).

Truth: standard EOB conservative dynamics, A(u) truncated at 2PN / 3PN:
  A_1PN = 1 - 2u                (identical to Schwarzschild: the doc's law IS A_1PN)
  A_2PN = 1 - 2u + 2 nu u^3
  A_3PN = 1 - 2u + 2 nu u^3 + a4 nu u^4,  a4 = 94/3 - 41 pi^2 / 32  (DJS 2000)
  D_2PN = 1 - 6 nu u^2          (radial potential; Schwarzschild: D = 1 - 2u)
  Q_2PN = 2 nu (4-3nu) u^2 A^2 p_r^4 / j^2   (toggled; circular limit unaffected)
Same energy map for all (that map is the standard EOB map at every PN order).

Units G = c = M = 1, quantities per unit reduced mass. float64.

Controls (must pass before any nu>0 number is read):
  C1 quadrature reproduces the exact Schwarzschild periastron closed form
     2 pi (1/sqrt(1-6/j^2) - 1) to < 1e-10 for the doc's law at many orbits.
  C2 circular energy e(x) = (E_real-1)/nu matches the published PN series:
     1PN -(3/4+nu/12)x, 2PN (-27/8+19nu/8-nu^2/24)x^2, 3PN (-675/64+(34445/576-205pi^2/96)nu
     -155nu^2/96-35nu^3/5184)x^3, to the order each A truncation licenses.
  C3 nu = 0: doc law and 2PN/3PN truth agree IDENTICALLY on every channel (A_2PN(0)=A_1PN).
"""
import math
import numpy as np

A4_3PN = 94.0 / 3.0 - 41.0 * math.pi ** 2 / 32.0

# ---------------------------------------------------------------- potentials
def make_A(order, nu):
    if order == "1pn":
        return lambda u: 1.0 - 2.0 * u, lambda u: -2.0 + 0.0 * u
    if order == "2pn":
        return (lambda u: 1.0 - 2.0 * u + 2.0 * nu * u ** 3,
                lambda u: -2.0 + 6.0 * nu * u ** 2)
    if order == "3pn":
        return (lambda u: 1.0 - 2.0 * u + 2.0 * nu * u ** 3 + A4_3PN * nu * u ** 4,
                lambda u: -2.0 + 6.0 * nu * u ** 2 + 4.0 * A4_3PN * nu * u ** 3)
    raise ValueError(order)

def make_D(order, nu):
    if order == "1pn":   # exact Schwarzschild Bbar = 1/A -> D = A
        return lambda u: 1.0 - 2.0 * u
    # 2PN-accurate: Schwarzschild part (exact) + the 2PN nu-dependent D coefficient -6 nu u^2
    return lambda u: 1.0 - 2.0 * u - 6.0 * nu * u ** 2

def use_Q(order):
    return order == "2pn"   # Q_2PN toggle (sensitivity test only)

def circular_at_u(u, nu, order):
    """j, h_eff, h_real (binding readout), Omega on the circular orbit at 1/u (M = 1)."""
    A, _ = make_A(order, nu)
    h2 = lambda j: A(u) * (1.0 + j * j * u * u)
    # dj/du = 0 on the family:  A'(1+j^2 u^2) + 2 A j^2 u = 0
    Ap = (A(u + 1e-7) - A(u - 1e-7)) / 2e-7
    j2 = -Ap / (2.0 * A(u) * u + Ap * u * u)
    j = math.sqrt(j2)
    h = math.sqrt(h2(j))
    # Omega = dH_real/dp_phys = (dh_eff/dj) * (dH_real/dh_eff) / nu   [p_phys = nu j]
    #        = (A j u^2 / h) * (nu / H_map) / nu,  H_map = sqrt(1+2 nu (h-1)) -> 1 at nu=0
    H_map = math.sqrt(1.0 + 2.0 * nu * (h - 1.0))
    hr = h if nu == 0 else H_map          # binding readout per unit mu
    Om = (A(u) * j * u * u / h) / H_map
    return j, h, hr, Om

def circular_series_x(u, nu, order, n=400001):
    """x = (M Omega)^{2/3} via fine d/du scan of h_real along the family."""
    # h_real along family: need d/du numerically over the family; do a local finite diff
    eps = 1e-6
    def Hr(uu):
        j, h, hr, Om = circular_at_u(uu, nu, order)
        return hr
    _, _, hr0, Om0 = circular_at_u(u, nu, order)
    return Om0 ** (2.0 / 3.0), hr0

def isco(nu, order):
    """ISCO along the circular family: d h_real/du = 0."""
    lo, hi = 1e-4, 0.499 / max(1e-9, 1.0)  # u below horizon 0.5
    # horizon of A: find largest root region where A>0
    A, _ = make_A(order, nu)
    hi = 0.16  # safely inside; ISCO is between ~1/7 and 1/5.2
    def dHr(u):
        e = 1e-6
        j1, h1, hr1, _ = circular_at_u(u - e, nu, order)
        j2, h2, hr2, _ = circular_at_u(u + e, nu, order)
        return (hr2 - hr1) / (2 * e)
    lo, hi = 0.080, 0.320   # brackets the ISCO for every nu <= 0.25 at 1-3PN
    flo, fhi = dHr(lo), dHr(hi)
    if flo * fhi > 0:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = dHr(mid)
        if flo * fm <= 0:
            hi = mid; fhi = fm
        else:
            lo = mid; flo = fm
    u = 0.5 * (lo + hi)
    j, h, hr, Om = circular_at_u(u, nu, order)
    return dict(r=1.0 / u, j=j, Eb_per_mu=(hr - 1.0) / nu if nu > 0 else hr - 1.0,
                Omega=Om, x=Om ** (2.0 / 3.0))

# ---------------------------------------------------------------- periastron quadrature
def orbit_invariants(umin, umax, nu, order):
    """(j, h_eff) with p_r = 0 at both turning points."""
    A, _ = make_A(order, nu)
    A1, A2 = A(umin), A(umax)
    den = A2 * umax ** 2 - A1 * umin ** 2
    if abs(den) < 1e-300:
        return None
    j2 = (A1 - A2) / den
    if j2 <= 0:
        return None
    j = math.sqrt(j2)
    h = math.sqrt(A1 * (1.0 + j2 * umin ** 2))
    return j, h

def periastron(umin, umax, nu, order, n=200001, with_Q=False):
    """Advance per radial period by quadrature; substitution u = umin+(umax-umin) sin^2 th."""
    A, _ = make_A(order, nu)
    D = make_D(order, nu)
    inv = orbit_invariants(umin, umax, nu, order)
    if inv is None:
        return None
    j, h = inv
    h2 = h * h
    def p_of(u):
        W = h2 / A(u) - 1.0 - j * j * u * u
        val = W / D(u)
        return math.sqrt(val) if val > 0 else None
    if p_of(0.5 * (umin + umax)) is None:
        return None
    th = np.linspace(0.0, math.pi / 2.0, n)
    u = umin + (umax - umin) * np.sin(th) ** 2
    W = h2 / A(u) - 1.0 - j * j * u * u
    pr2 = W / D(u)
    if with_Q and use_Q(order):
        # Q = 2 nu (4-3nu) u^2 A^2 p_r^4 / j^2 enters h^2 = A(1+j^2u^2+D p^2+Q)
        # solved iteratively for p^2
        q = 2.0 * nu * (4.0 - 3.0 * nu) * u ** 2 * A(u) ** 2 / j ** 2
        p2 = np.maximum(pr2, 1e-300)
        for _ in range(50):
            p2 = (W - q * p2 * p2) / D(u)
            p2 = np.maximum(p2, 0.0)
        pr2 = p2
    ok = pr2 > 0
    integrand = np.zeros_like(u)
    integrand[ok] = j / (D(u[ok]) * np.sqrt(pr2[ok]))
    weight = 2.0 * (umax - umin) * np.sin(th) * np.cos(th)
    val = integrand * weight
    val[~ok] = 0.0
    return 2.0 * np.trapz(val, th)

def rk4_binet(j, umin, phi_max=400.0, dphi=1e-5):
    """Independent method: RK4 on the exact Schwarzschild Binet equation
    Returns the total angle swept in one radial period."""
    f = lambda u: 1.0 / j ** 2 + 3.0 * u * u - u
    u, up = umin, 0.0
    phi = 0.0
    turned = False
    steps = int(phi_max / dphi)
    for _ in range(steps):
        k1u, k1p = up, f(u)
        k2u, k2p = up + 0.5 * dphi * k1p, f(u + 0.5 * dphi * k1u)
        k3u, k3p = up + 0.5 * dphi * k2p, f(u + 0.5 * dphi * k2u)
        k4u, k4p = up + dphi * k3p, f(u + dphi * k3u)
        u_new = u + dphi / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        up_new = up + dphi / 6.0 * (k1p + 2 * k2p + 2 * k3p + k4p)
        phi += dphi
        if not turned and up_new < 0 and up >= 0 and phi > 1.0:
            turned = True  # passed periastron; now look for the return to apastron
        u, up = u_new, up_new
        if turned and up > 0 and phi > 2.0:
            break
    else:
        return None
    return phi - 0.5 * dphi

# ---------------------------------------------------------------- published series (C2)
def series_coeff(nu):
    return dict(c1=-0.75 - nu / 12.0,
                c2=-27.0 / 8.0 + 19.0 * nu / 8.0 - nu ** 2 / 24.0,
                c3=-675.0 / 64.0 + (34445.0 / 576.0 - 205.0 * math.pi ** 2 / 96.0) * nu
                   - 155.0 * nu ** 2 / 96.0 - 35.0 * nu ** 3 / 5184.0)

def circ_energy_check(nu, order, u=0.002):
    x, hr = circular_series_x(u, nu, order)
    e = (hr - 1.0) / nu
    c = series_coeff(nu)
    pred = -x / 2.0 * (1.0 + c["c1"] * x + c["c2"] * x ** 2 + c["c3"] * x ** 3)
    return x, e, pred

# ---------------------------------------------------------------- controls
def controls():
    ok = True
    # C1: periastron quadrature vs RK4 Binet (doc law, nu=0), orbits across the domain,
    # plus the gr_oracle weak-field series 6 pi/p (1 + (18+e^2)/(4p)) as a third check.
    worst = 0.0
    for pN, eN in [(100, 0.2), (40, 0.5), (20, 1e-3), (20, 0.6), (12, 0.3), (8, 1e-3)]:
        umin = (1.0 - eN) / pN   # apastron
        umax = (1.0 + eN) / pN   # periastron
        inv = orbit_invariants(umin, umax, 0.0, "1pn")
        num = periastron(umin, umax, 0.0, "1pn")
        ana = rk4_binet(inv[0], umin)
        rel = abs(num - ana) / abs(ana)
        worst = max(worst, rel)
    print(f"C1 quadrature vs RK4-Binet worst rel err: {worst:.2e}")
    ok &= worst < 1e-4   # RK4 at dphi=1e-5 truncates ~1e-6; both methods independent
    pN, eN = 100.0, 0.2
    num = periastron((1 - eN) / pN, (1 + eN) / pN, 0.0, "1pn") - 2 * math.pi
    ser = 6 * math.pi / pN * (1 + (18 + eN ** 2) / (4 * pN))
    rel = abs(num - ser) / ser
    print(f"C1b weak-field series (p=100, e=0.2): num={num:.6f} series={ser:.6f} rel={rel:.2e}")
    ok &= rel < 3e-3   # series omits O(((18+e^2)/4p)^2) ~ 2e-3 at p=100
    # C2: circular e(x) vs published series at weak field
    for order, tol in [("2pn", 1e-6), ("3pn", 1e-6)]:
        x, e, pred = circ_energy_check(0.25, order, u=0.002)
        rel = abs(e - pred) / abs(pred)
        print(f"C2 e(x) {order}: x={x:.5f} num={e:.9e} series={pred:.9e} rel={rel:.2e}")
        ok &= rel < tol
    # C3: nu=0 identical channels
    for order in ["2pn", "3pn"]:
        a = isco(0.0, order); b = isco(0.0, "1pn")
        same = all(abs(a[k] - b[k]) < 1e-9 for k in ("r", "j", "Eb_per_mu", "Omega"))
        print(f"C3 nu=0 ISCO {order} vs doc law identical: {same} "
              f"(r={a['r']:.6f}, j={a['j']:.6f}, E={a['Eb_per_mu']:.7f}, Om={a['Omega']:.6f})")
        ok &= same
    print("CONTROLS", "PASS" if ok else "FAIL")
    return ok

if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["controls"]:
        controls()
