"""Float premise probe library for es-lattice-gravity-v1 (draft H0195).

Painleve-Gullstrand river coordinates, G = c = M = 1.  Massive state (x, y, wx, wy):
position and proper velocity relative to the flow, w = gamma_u * u.  With canonical
momentum p = -w the PG Hamiltonian is

    H(x, p) = beta(x).p - sqrt(1 + p^2)        (massive)
    H(x, p) = beta(x).p - |p|                  (light)

with beta(x) = -sqrt(2/r) x/r.  Split H = [beta.p] + [-sqrt(mu^2+p^2)]:

  A (drift): straight line in the local inertial sheet at constant u (|u| = 1 for
             light); w constant.  Exact.
  B (kick) : river advection, r^(3/2)(T) = r^(3/2) - (3*sqrt(2)/2) T, direction fixed,
             plus momentum focusing  w_par *= sqrt(r'/r),  w_perp *= r/r'.  Exact
             closed form (flow of beta.p).  x x w is conserved exactly by B.

Step (2nd order, self-adjoint = time symmetric):  S2 = B(dt/2) A(dt) B(dt/2).
Step (4th order): Yoshida composition S2(w1 dt) S2(w2 dt) S2(w1 dt).
Step size dt = eta * r^(3/2)  (eta x local dynamical time, current state only).

Horizon: absorbed when a substep would take r <= 2 (river step crossing r^(3/2) =
2^(3/2), or r <= 2 after a drift).  Energy diagnostic E = sqrt(1+w^2) + beta.w,
angular momentum J = x*wy - y*wx.
"""
import math

SQ2 = math.sqrt(2.0)
CB2 = 1.5 * SQ2            # (3 sqrt(2)/2): river advects r^{3/2} down by CB2*T
HOR32 = 2.0 ** 1.5         # (2M)^{3/2} with M = 1
T23 = 2.0 / 3.0
W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
W2 = 1.0 - 2.0 * W1
PI = math.pi

# ----------------------------------------------------------------- oracle side

def ellip_k(m):
    """K(m) = int_0^{pi/2} dtheta/sqrt(1-m sin^2 theta), AGM (as gr_oracle.rs)."""
    a, g = 1.0, math.sqrt(1.0 - m)
    for _ in range(60):
        a1, g1 = 0.5 * (a + g), math.sqrt(a * g)
        if abs(a1 - g1) <= 1e-17 * a1:
            a = a1
            break
        a, g = a1, g1
    return PI / (2.0 * a)

def bound_constants(p, e):
    """Exact Schwarzschild first integrals (gr_oracle_extended.rs)."""
    energy = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / math.sqrt(p - 3.0 - e * e)
    return energy, angular

def periapsis_advance_gr(p, e):
    """Delta phi per orbit (minus 2 pi), exact elliptic form as gr_oracle.rs:
    4*(sqrt(p/d)*(K(m)-pi/2) + (pi/2)*(sqrt(p/d)-1)), d = p-6+2e, m = 4e/d."""
    d = p - 6.0 + 2.0 * e
    sp = math.sqrt(p / d)
    return 4.0 * (sp * (ellip_k(4.0 * e / d) - 0.5 * PI) + 0.5 * PI * (sp - 1.0))

def periapsis_advance_series(p, e):
    return 6.0 * PI / p * (1.0 + (18.0 + e * e) / (4.0 * p))

def periapsis_advance_ode(p, e, spr=2000.0):
    """Independent check: RK4 on Binet u'' = 1/L^2 - u + 3u^2, periapsis to periapsis.
    u is maximal at periapsis, so u' goes + -> - there."""
    _, L = bound_constants(p, e)
    invL2 = 1.0 / (L * L)
    h = 1.0 / spr
    u, up, phi = (1.0 + e) / p, 0.0, 0.0
    gone_apo = False
    up_prev = up
    for _ in range(int(8.0 * PI * spr) + 100):
        k1u = up;             k1v = invL2 - u + 3.0*u*u
        k2u = up + 0.5*h*k1v; ua = u + 0.5*h*k1u
        k2v = invL2 - ua + 3.0*ua*ua
        k3u = up + 0.5*h*k2v; ub = u + 0.5*h*k2u
        k3v = invL2 - ub + 3.0*ub*ub
        k4u = up + h*k3v;     uc = u + h*k3u
        k4v = invL2 - uc + 3.0*uc*uc
        u += h*(k1u + 2*k2u + 2*k3u + k4u)/6.0
        up += h*(k1v + 2*k2v + 2*k3v + k4v)/6.0
        phi += h
        if not gone_apo:
            if up > 0.0:
                gone_apo = True
        elif up <= 0.0:
            frac = up_prev / (up_prev - up)          # u' = 0 crossing, linear
            return (phi - h + frac*h) - 2.0*PI
        up_prev = up
    raise RuntimeError("periapsis not found")

def gauss_legendre(n):
    out = []
    for i in range(1, n + 1):
        x = math.cos(PI * (i - 0.25) / (n + 0.5))
        dp = 0.0
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p2 = ((2*k - 1) * x * p1 - (k - 1) * p0) / k
                p0, p1 = p1, p2
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        out.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
    return out

_GL32 = None

def deflection_gr(b):
    """GL quadrature of the exact deflection (mirrors gr_oracle.rs)."""
    global _GL32
    if _GL32 is None:
        _GL32 = gauss_legendre(32)
    u0 = 1.0 / b
    for _ in range(100):
        h = 2.0*u0*u0*u0 - u0*u0 + 1.0/(b*b)
        dh = 6.0*u0*u0 - 2.0*u0
        stp = h / dh
        u0 -= stp
        if abs(stp) <= 1e-17 * u0:
            break
    total = 0.0
    pieces = 64
    for j in range(pieces):
        a, c = j / pieces, (j + 1) / pieces
        for x, w in _GL32:
            s = 0.5*(a + c) + 0.5*(c - a)*x
            u = u0 * (1.0 - s*s)
            qf = u0 + u
            rr = 2.0 * (u*u + u*u0 + u0*u0)
            q = qf - rr
            total += w * (c - a) * 0.5 * 4.0 * math.sqrt(u0) * rr / \
                (math.sqrt(q*qf) * (math.sqrt(qf) + math.sqrt(q)))
    return total

def deflection_series(b):
    return 4.0/b + 15.0*PI/(4.0*b*b)

def deflection_ode(b, spr=2000.0):
    """Independent check: RK4 on u'' + u = 3u^2 from u=0, u'=1/b until u returns to 0."""
    h = 1.0 / spr
    u, up, phi = 0.0, 1.0/b, 0.0
    u_prev = 0.0
    for _ in range(int(8.0*spr)):
        k1u = up;             k1v = 3.0*u*u - u
        k2u = up + 0.5*h*k1v; ua = u + 0.5*h*k1u
        k2v = 3.0*ua*ua - ua
        k3u = up + 0.5*h*k2v; ub = u + 0.5*h*k2u
        k3v = 3.0*ub*ub - ub
        k4u = up + h*k3v;     uc = u + h*k3u
        k4v = 3.0*uc*uc - uc
        u += h*(k1u + 2*k2u + 2*k3u + k4u)/6.0
        up += h*(k1v + 2*k2v + 2*k3v + k4v)/6.0
        phi += h
        if phi > 1.0 and u <= 0.0:
            frac = u_prev / (u_prev - u)            # u = 0 crossing, linear
            return (phi - h + frac*h) - PI
        u_prev = u
    raise RuntimeError("light did not return")

def null_turning_radius(b):
    """Outer root of r^2/(1-2/r) = b^2 (gr_oracle_extended.rs)."""
    r = b - 1.0
    for _ in range(40):
        fv = r*r/(1.0 - 2.0/r) - b*b
        df = 2.0*r*r*(r - 3.0)/(r - 2.0)**2
        stp = fv/df
        r -= stp
        if abs(stp) < 2e-15*r:
            break
    return r

# ------------------------------------------------------------------- law side

def s2_mass(x, y, wx, wy, dt):
    """One 2nd-order step: kick(half) drift kick(half).  Returns (x,y,wx,wy,absorbed)."""
    r = math.sqrt(x*x + y*y)
    rs = math.sqrt(r)
    s = r*rs - CB2*(0.5*dt)
    if s <= HOR32:
        return x, y, wx, wy, True
    q = (s/(r*rs)) ** T23
    inv = 1.0/r
    nx, ny = x*inv, y*inv
    wd = wx*nx + wy*ny
    fp = math.sqrt(q)
    fq = 1.0/q
    wx = fq*wx + wd*nx*(fp - fq)
    wy = fq*wy + wd*ny*(fp - fq)
    x *= q
    y *= q
    g = math.sqrt(1.0 + wx*wx + wy*wy)
    hdt = dt/g
    x += hdt*wx
    y += hdt*wy
    if x*x + y*y <= 4.0:
        return x, y, wx, wy, True
    r = math.sqrt(x*x + y*y)
    rs = math.sqrt(r)
    s = r*rs - CB2*(0.5*dt)
    if s <= HOR32:
        return x, y, wx, wy, True
    q = (s/(r*rs)) ** T23
    inv = 1.0/r
    nx, ny = x*inv, y*inv
    wd = wx*nx + wy*ny
    fp = math.sqrt(q)
    fq = 1.0/q
    wx = fq*wx + wd*nx*(fp - fq)
    wy = fq*wy + wd*ny*(fp - fq)
    x *= q
    y *= q
    return x, y, wx, wy, False

def s4_mass(x, y, wx, wy, dt):
    for c in (W1, W2, W1):
        x, y, wx, wy, ab = s2_mass(x, y, wx, wy, c*dt)
        if ab:
            return x, y, wx, wy, True
    return x, y, wx, wy, False

def s2_phot(x, y, px, py, dt):
    """Photon step in (x, p): drift straight at |u| = 1, same river kick."""
    r = math.sqrt(x*x + y*y)
    rs = math.sqrt(r)
    s = r*rs - CB2*(0.5*dt)
    if s <= HOR32:
        return x, y, px, py, True
    q = (s/(r*rs)) ** T23
    inv = 1.0/r
    nx, ny = x*inv, y*inv
    wd = px*nx + py*ny
    fp = math.sqrt(q)
    fq = 1.0/q
    px = fq*px + wd*nx*(fp - fq)
    py = fq*py + wd*ny*(fp - fq)
    x *= q
    y *= q
    pn = math.sqrt(px*px + py*py)
    x -= dt*px/pn
    y -= dt*py/pn
    if x*x + y*y <= 4.0:
        return x, y, px, py, True
    r = math.sqrt(x*x + y*y)
    rs = math.sqrt(r)
    s = r*rs - CB2*(0.5*dt)
    if s <= HOR32:
        return x, y, px, py, True
    q = (s/(r*rs)) ** T23
    inv = 1.0/r
    nx, ny = x*inv, y*inv
    wd = px*nx + py*ny
    fp = math.sqrt(q)
    fq = 1.0/q
    px = fq*px + wd*nx*(fp - fq)
    py = fq*py + wd*ny*(fp - fq)
    x *= q
    y *= q
    return x, y, px, py, False

def s4_phot(x, y, px, py, dt):
    for c in (W1, W2, W1):
        x, y, px, py, ab = s2_phot(x, y, px, py, c*dt)
        if ab:
            return x, y, px, py, True
    return x, y, px, py, False

def energy_mass(x, y, wx, wy):
    r = math.sqrt(x*x + y*y)
    return math.sqrt(1.0 + wx*wx + wy*wy) - SQ2*(x*wx + y*wy)/(r*math.sqrt(r))

def angmom(x, y, wx, wy):
    return x*wy - y*wx

# ------------------------------------------------------------- initial states

def ic_bound_periapsis(p, e):
    """Massive IC exactly at periapsis; returns (x, y, wx, wy, E, L, selfcheck).
    At a radial turning point dr/dT = 0, so u_r = sqrt(2/r); gamma = E/(1-2/r);
    u_t = L/(gamma r).  Self-check: |u|^2 must equal 1 - 1/gamma^2."""
    E, L = bound_constants(p, e)
    rp = p/(1.0 + e)
    sig = math.sqrt(2.0/rp)
    gam = E/(1.0 - 2.0/rp)
    ut = L/(gam*rp)
    lhs = sig*sig + ut*ut
    rhs = 1.0 - 1.0/(gam*gam)
    return rp, 0.0, gam*sig, gam*ut, E, L, abs(lhs - rhs)/rhs

def ic_e1_infall(L, r0):
    """Inward E=1 anchor at r0 with angular momentum L.  Closure gamma =
    1/sqrt(1-|u|^2) with u_r = (1-1/gamma)/sigma, u_t = L/(gamma r0); fixed
    point to machine precision.  Inward branch (small u_r)."""
    sig = math.sqrt(2.0/r0)
    gam = 1.0
    for _ in range(200):
        ut = L/(gam*r0)
        ur = (1.0 - 1.0/gam)/sig
        gn = 1.0/math.sqrt(1.0 - ur*ur - ut*ut)
        if abs(gn - gam) < 1e-16*gam:
            gam = gn
            break
        gam = gn
    ur = (1.0 - 1.0/gam)/sig
    ut = L/(gam*r0)
    return r0, 0.0, gam*ur, gam*ut

def ic_photon_turning(b):
    """Photon IC at the turning point (b > 3 sqrt 3); p = -u, |p| = 1."""
    rmin = null_turning_radius(b)
    sig = math.sqrt(2.0/rmin)
    ut = math.sqrt(1.0 - sig*sig)
    return rmin, 0.0, -sig, -ut

# ------------------------------------------------------------------- self test

if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    print("== oracle self-test ==")
    for (p, e) in [(20.0, 0.2), (20.0, 0.5), (100.0, 0.2), (100.0, 0.5),
                   (1000.0, 0.2), (1000.0, 0.5), (10000.0, 0.2)]:
        a_ell = periapsis_advance_gr(p, e)
        a_ser = periapsis_advance_series(p, e)
        a_ode = periapsis_advance_ode(p, e)
        print(f"p={p:7.1f} e={e:.2f}  ell={a_ell:.12f} ode={a_ode:.12f} "
              f"ser={a_ser:.12f}  rel(ell-ode)={abs(a_ell-a_ode)/a_ell:.2e} "
              f"rel(ser-ell)={abs(a_ser-a_ell)/a_ell:.2e}")
    for b in (10.0, 30.0):
        d_q = deflection_gr(b)
        d_s = deflection_series(b)
        d_o = deflection_ode(b)
        print(f"b={b:5.1f}  quad={d_q:.12f} ode={d_o:.12f} ser={d_s:.12f} "
              f"rel(quad-ode)={abs(d_q-d_o)/d_q:.2e} rel(ser-quad)={abs(d_s-d_q)/d_q:.2e}")
    print("== formulation self-checks ==")
    for (p, e) in [(20.0, 0.2), (20.0, 0.5), (1000.0, 0.2), (1000.0, 0.5)]:
        x, y, wx, wy, E, L, sc = ic_bound_periapsis(p, e)
        print(f"p={p:7.1f} e={e:.2f} IC |u|^2 vs 1-1/gam^2 rel={sc:.2e} "
              f"E_check={energy_mass(x,y,wx,wy)-E:.2e} L_check={angmom(x,y,wx,wy)-L:.2e}")
    for L in (3.98, 4.02):
        x, y, wx, wy = ic_e1_infall(L, 100.0)
        E = energy_mass(x, y, wx, wy)
        Lv = angmom(x, y, wx, wy)
        r = math.sqrt(x*x + y*y)
        sig = math.sqrt(2.0/r)
        gam = math.sqrt(1.0 + wx*wx + wy*wy)
        vr = (wx/gam) - sig
        print(f"L={L:.2f} E1-anchor: E-1={E-1.0:.2e} L-L0={Lv-L:.2e} v_r={vr:.6f} (inward<0)")
    r = 20.0
    sig = math.sqrt(2.0/r)
    ut = 1.0/math.sqrt(r)
    gam = 1.0/math.sqrt(1.0 - 3.0/r)
    print(f"circular r=20: L={gam*r*ut:.9f} vs r/sqrt(r-3)={r/math.sqrt(r-3):.9f} "
          f"E={gam*(1-2.0/r):.9f} vs (1-2/r)/sqrt(1-3/r)={(1-2.0/r)/math.sqrt(1-3.0/r):.9f}")
    # free fall at u = 0 must ride the river exactly: r^{3/2}(T) linear in T
    x, y, wx, wy = 100.0, 0.0, 0.0, 0.0
    T = 0.0
    for _ in range(300):
        r = math.sqrt(x*x + y*y)
        dt = 0.001*r*math.sqrt(r)
        x, y, wx, wy, ab = s2_mass(x, y, wx, wy, dt)
        if ab:
            print("u=0 river fall: ABSORBED unexpectedly")
            break
        T += dt
    r = math.sqrt(x*x + y*y)
    print(f"u=0 river fall: r(T)^(3/2) = {r*math.sqrt(r):.9f} vs "
          f"{100.0*math.sqrt(100.0) - CB2*T:.9f} (exact linear law)")
    print(f"self-test wall: {time.perf_counter()-t0:.2f} s")
