"""Cell-step re-probe library (gravity-v1-reprobe), pure Python 3 stdlib.

Reuses the earlier probe's integrator (PG river Hamiltonian, exact drift and
kick, S2 = kick-half/drift/kick-half, Yoshida S4) from /gv1/gv1.py, with the
step rule replaced by CELL steps: shells [2^k, 2^{k+1}), dyn(r) = r^{3/2},
Delta_k = eta * 2^{1.5k}.  The step belongs to the cell, never to the body.

  C1  event-clipped cell leapfrog (NOT time-symmetric).  Inside shell k the
      step is the constant Delta_k.  A subflow that would cross a shell circle
      is advanced EXACTLY to the crossing and the step pattern restarts in the
      new shell:  kick crossings are closed-form (r^{3/2} is linear in tau),
      drift crossings are the first root of the chord quadratic |x + t v| = R,
      direction from the radial velocity at the root.  Landings snap onto the
      circle.  Works for both signs of the Yoshida sub-steps.
  C2  time-symmetric shell choice: Hut-Makino-McMillan-style symmetrized step
      selection.  A step uses Delta_k of the shell containing the step's
      time-midpoint (palindromic midpoint = kick(Delta/2) then drift(Delta/2)
      of the would-be step), found by fixed-point iteration seeded at the
      current shell; a 2-cycle is broken by the finest visited shell.
      Steps are then full S2/S4 with Delta off the menu; no clipping.
  C3  control: one global fixed Delta = eta * rref^{3/2}, rref = sqrt(rp*ra)
      of the p=20, e=0.2 orbit (= 92.20), as in the earlier probe's control.

The shell index is re-derived from r (frexp) at every sub-step, so the
convention [2^k, 2^{k+1}) holds exactly.  Horizon: crossing the circle r = 2
inward, or ending a drift at r <= 2, absorbs.
"""
import math

SQ2 = math.sqrt(2.0)
CB2 = 1.5 * SQ2            # river advects r^{3/2} down by CB2*tau
HOR32 = 2.0 ** 1.5
T23 = 2.0 / 3.0
W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
W2 = 1.0 - 2.0 * W1
PI = math.pi
T32 = [2.0 ** (1.5 * k) for k in range(48)]      # dyn(2^k)
R2K = [2.0 ** k for k in range(48)]              # shell circles
RREF = math.sqrt((20.0 / 1.2) * (20.0 / 0.8))    # 20.412 (p=20, e=0.2)
RREF32 = RREF * math.sqrt(RREF)                  # 92.20: C3 global step ref
sqrt = math.sqrt

# ----------------------------------------------------------------- oracle side
# (verbatim from gv1.py, proven against gr_oracle.rs in the earlier probe)

def ellip_k(m):
    a, g = 1.0, math.sqrt(1.0 - m)
    for _ in range(60):
        a1, g1 = 0.5 * (a + g), math.sqrt(a * g)
        if abs(a1 - g1) <= 1e-17 * a1:
            a = a1
            break
        a, g = a1, g1
    return PI / (2.0 * a)

def bound_constants(p, e):
    energy = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / math.sqrt(p - 3.0 - e * e)
    return energy, angular

def periapsis_advance_gr(p, e):
    d = p - 6.0 + 2.0 * e
    sp = math.sqrt(p / d)
    return 4.0 * (sp * (ellip_k(4.0 * e / d) - 0.5 * PI) + 0.5 * PI * (sp - 1.0))

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

_GL48 = None

def exact_tail(b, r_e):
    """Remaining rotation of psi_v from r_e to infinity along the exact geodesic."""
    global _GL48
    if _GL48 is None:
        _GL48 = gauss_legendre(48)
    u0 = 1.0 / r_e
    total = 0.0
    for x, w in _GL48:
        u = 0.5 * u0 * (1.0 + x)
        total += 0.5 * u0 * w / math.sqrt(1.0 / (b * b) - u * u + 2.0 * u * u * u)
    th = math.atan2(u0, math.sqrt(1.0 / (b * b) - u0 * u0 + 2.0 * u0 * u0 * u0))
    return total - th

def deflection_gr(b):
    """GL quadrature of the exact Schwarzschild deflection (mirrors gr_oracle.rs)."""
    global _GL48
    if _GL48 is None:
        _GL48 = gauss_legendre(48)

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
        for x, w in _GL48:
            s = 0.5*(a + c) + 0.5*(c - a)*x
            u = u0 * (1.0 - s*s)
            qf = u0 + u
            rr = 2.0 * (u*u + u*u0 + u0*u0)
            q = qf - rr
            total += w * (c - a) * 0.5 * 4.0 * math.sqrt(u0) * rr / \
                (math.sqrt(q*qf) * (math.sqrt(qf) + math.sqrt(q)))
    return total

def null_turning_radius(b):
    r = b - 1.0
    for _ in range(40):
        fv = r*r/(1.0 - 2.0/r) - b*b
        df = 2.0*r*r*(r - 3.0)/(r - 2.0)**2
        stp = fv/df
        r -= stp
        if abs(stp) < 2e-15*r:
            break
    return r

def energy_mass(x, y, wx, wy):
    r = math.sqrt(x*x + y*y)
    return math.sqrt(1.0 + wx*wx + wy*wy) - SQ2*(x*wx + y*wy)/(r*math.sqrt(r))

def angmom(x, y, wx, wy):
    return x*wy - y*wx

# ------------------------------------------------------------- initial states

def ic_bound_periapsis(p, e):
    E, L = bound_constants(p, e)
    rp = p/(1.0 + e)
    sig = math.sqrt(2.0/rp)
    gam = E/(1.0 - 2.0/rp)
    ut = L/(gam*rp)
    return rp, 0.0, gam*sig, gam*ut, E, L

def ic_e1_infall(L, r0):
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
    rmin = null_turning_radius(b)
    sig = math.sqrt(2.0/rmin)
    ut = math.sqrt(1.0 - sig*sig)
    return rmin, 0.0, -sig, -ut

def ic_photon_r(b, r0):
    """Exact inbound photon state at (r0, 0) with impact parameter b."""
    sig = math.sqrt(2.0/r0)
    R = math.sqrt(r0*r0 + b*b*sig*sig)
    dl = math.atan2(b*sig, r0)
    s = b/R
    A = math.asin(s) - dl
    if math.cos(A) - sig >= 0.0:                 # want inbound: v_r = cosA - sig < 0
        A = PI - math.asin(s) - dl
    cA, sA = math.cos(A), math.sin(A)
    return r0, 0.0, -cA, -sA

def psi_v_of(x, y, px, py):
    """Direction angle of the coordinate velocity v = u + beta (photon state)."""
    pn = math.sqrt(px*px + py*py)
    r = math.sqrt(x*x + y*y)
    rs = math.sqrt(r)
    f_ = -SQ2/(r*rs)
    return math.atan2(-py/pn + f_*y, -px/pn + f_*x)

def b_of_state(x, y, px, py):
    r = math.sqrt(x*x + y*y)
    pn = math.sqrt(px*px + py*py)
    Eph = pn + SQ2*(x*px + y*py)/(r*math.sqrt(r))
    Lph = abs(x*py - y*px)
    return Lph/Eph

# ------------------------------------------------------- plain steppers (C3)
# verbatim subflows from gv1.py; fixed dt, horizon endchecks only

def s2_mass(x, y, wx, wy, dt):
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

def c3_step(x, y, vx1, vy1, eta, order, phot):
    dt = eta*RREF32
    if phot:
        return (s2_phot if order == 2 else s4_phot)(x, y, vx1, vy1, dt)
    return (s2_mass if order == 2 else s4_mass)(x, y, vx1, vy1, dt)

# ------------------------------------------------------------------- C1 core

def _kickc_mass(x, y, wx, wy, tau):
    """River kick of duration tau (any sign), clipped exactly at the adjacent
    shell circle (r^{3/2} is linear in tau).  Returns
    (x, y, wx, wy, t_used, landed, absorbed)."""
    r = sqrt(x*x + y*y)
    rs = sqrt(r)
    r32 = r*rs
    k = math.frexp(r)[1] - 1
    if tau >= 0.0:
        m = k if r32 > T32[k] else k - 1
        if m < 1:
            m = 1
        r32e = r32 - CB2*tau
        if r32e < T32[m] and (r32 - T32[m]) > 1e-12*abs(tau)*CB2:
            taux = (r32 - T32[m])/CB2
            q = (T32[m]/r32) ** T23
            inv = 1.0/r
            nx, ny = x*inv, y*inv
            wd = wx*nx + wy*ny
            fp = sqrt(q)
            fq = 1.0/q
            wx = fq*wx + wd*nx*(fp - fq)
            wy = fq*wy + wd*ny*(fp - fq)
            x *= q
            y *= q
            sc = R2K[m]/sqrt(x*x + y*y)
            return x*sc, y*sc, wx, wy, taux, True, (m == 1)
    else:
        m = k + 1
        r32e = r32 - CB2*tau
        if r32e > T32[m] and (T32[m] - r32) > 1e-12*abs(tau)*CB2:
            taux = (T32[m] - r32)/CB2
            q = (T32[m]/r32) ** T23
            inv = 1.0/r
            nx, ny = x*inv, y*inv
            wd = wx*nx + wy*ny
            fp = sqrt(q)
            fq = 1.0/q
            wx = fq*wx + wd*nx*(fp - fq)
            wy = fq*wy + wd*ny*(fp - fq)
            x *= q
            y *= q
            sc = R2K[m]/sqrt(x*x + y*y)
            return x*sc, y*sc, wx, wy, taux, True, False
    q = (r32e/r32) ** T23
    inv = 1.0/r
    nx, ny = x*inv, y*inv
    wd = wx*nx + wy*ny
    fp = sqrt(q)
    fq = 1.0/q
    wx = fq*wx + wd*nx*(fp - fq)
    wy = fq*wy + wd*ny*(fp - fq)
    return x*q, y*q, wx, wy, tau, False, False

def _driftc_mass(x, y, wx, wy, tau):
    """Straight drift of duration tau (any sign), clipped exactly at the first
    shell-circle crossing of the chord.  Returns (x, y, wx, wy, t_used, landed,
    absorbed)."""
    g = sqrt(1.0 + wx*wx + wy*wy)
    vx = wx/g
    vy = wy/g
    k = math.frexp(sqrt(x*x + y*y))[1] - 1
    aa = vx*vx + vy*vy
    bb = x*vx + y*vy
    cc = x*x + y*y
    tbest = None
    Rbest = 0.0
    dirin = False
    tol = 1e-12*abs(tau)
    for R in (R2K[k], R2K[k+1]):
        cq = cc - R*R
        disc = bb*bb - aa*cq
        if disc <= 0.0:
            continue
        sd = sqrt(disc)
        t1 = (-bb - sd)/aa
        t2 = (-bb + sd)/aa
        t = None
        if tau > 0.0:
            if tol < t1 <= tau:
                t = t1
            elif tol < t2 <= tau:
                t = t2
        else:
            if tau <= t2 < -tol:
                t = t2
            elif tau <= t1 < -tol:
                t = t1
        if t is None:
            continue
        if tbest is None or abs(t) < abs(tbest):
            tbest = t
            Rbest = R
            dirin = ((x + t*vx)*vx + (y + t*vy)*vy) < 0.0
    if tbest is not None:
        x += tbest*vx
        y += tbest*vy
        sc = Rbest/sqrt(x*x + y*y)
        return x*sc, y*sc, wx, wy, tbest, True, (dirin and Rbest <= 2.0)
    x += tau*vx
    y += tau*vy
    return x, y, wx, wy, tau, False, (x*x + y*y <= 4.0)

def _kickc_phot(x, y, px, py, tau):
    r = sqrt(x*x + y*y)
    rs = sqrt(r)
    r32 = r*rs
    k = math.frexp(r)[1] - 1
    if tau >= 0.0:
        m = k if r32 > T32[k] else k - 1
        if m < 1:
            m = 1
        r32e = r32 - CB2*tau
        if r32e < T32[m] and (r32 - T32[m]) > 1e-12*abs(tau)*CB2:
            taux = (r32 - T32[m])/CB2
            q = (T32[m]/r32) ** T23
            inv = 1.0/r
            nx, ny = x*inv, y*inv
            wd = px*nx + py*ny
            fp = sqrt(q)
            fq = 1.0/q
            px = fq*px + wd*nx*(fp - fq)
            py = fq*py + wd*ny*(fp - fq)
            x *= q
            y *= q
            sc = R2K[m]/sqrt(x*x + y*y)
            return x*sc, y*sc, px, py, taux, True, (m == 1)
    else:
        m = k + 1
        r32e = r32 - CB2*tau
        if r32e > T32[m] and (T32[m] - r32) > 1e-12*abs(tau)*CB2:
            taux = (T32[m] - r32)/CB2
            q = (T32[m]/r32) ** T23
            inv = 1.0/r
            nx, ny = x*inv, y*inv
            wd = px*nx + py*ny
            fp = sqrt(q)
            fq = 1.0/q
            px = fq*px + wd*nx*(fp - fq)
            py = fq*py + wd*ny*(fp - fq)
            x *= q
            y *= q
            sc = R2K[m]/sqrt(x*x + y*y)
            return x*sc, y*sc, px, py, taux, True, False
    q = (r32e/r32) ** T23
    inv = 1.0/r
    nx, ny = x*inv, y*inv
    wd = px*nx + py*ny
    fp = sqrt(q)
    fq = 1.0/q
    px = fq*px + wd*nx*(fp - fq)
    py = fq*py + wd*ny*(fp - fq)
    return x*q, y*q, px, py, tau, False, False

def _driftc_phot(x, y, px, py, tau):
    pn = sqrt(px*px + py*py)
    vx = -px/pn
    vy = -py/pn
    k = math.frexp(sqrt(x*x + y*y))[1] - 1
    aa = vx*vx + vy*vy
    bb = x*vx + y*vy
    cc = x*x + y*y
    tbest = None
    Rbest = 0.0
    dirin = False
    tol = 1e-12*abs(tau)
    for R in (R2K[k], R2K[k+1]):
        cq = cc - R*R
        disc = bb*bb - aa*cq
        if disc <= 0.0:
            continue
        sd = sqrt(disc)
        t1 = (-bb - sd)/aa
        t2 = (-bb + sd)/aa
        t = None
        if tau > 0.0:
            if tol < t1 <= tau:
                t = t1
            elif tol < t2 <= tau:
                t = t2
        else:
            if tau <= t2 < -tol:
                t = t2
            elif tau <= t1 < -tol:
                t = t1
        if t is None:
            continue
        if tbest is None or abs(t) < abs(tbest):
            tbest = t
            Rbest = R
            dirin = ((x + t*vx)*vx + (y + t*vy)*vy) < 0.0
    if tbest is not None:
        x += tbest*vx
        y += tbest*vy
        sc = Rbest/sqrt(x*x + y*y)
        return x*sc, y*sc, px, py, tbest, True, (dirin and Rbest <= 2.0)
    x += tau*vx
    y += tau*vy
    return x, y, px, py, tau, False, (x*x + y*y <= 4.0)

def _c1_mass(x, y, wx, wy, eta, order):
    """C1 massive step attempt, PER-SUBFLOW cell anchoring: every kick/drift
    subflow derives its shell from its own starting r and runs for its share of
    that shell's Delta, clipped exactly at any crossing.  Returns
    (x, y, wx, wy, T_subflow_sum, steps, crossings, absorbed)."""
    T = 0.0
    nev = 0
    ncr = 0
    for c in ((1.0,) if order == 2 else (W1, W2, W1)):
        nev += 1
        for role in (0, 1, 0):
            r = sqrt(x*x + y*y)
            k = math.frexp(r)[1] - 1
            tau = c*eta*T32[k]*(0.5 if role == 0 else 1.0)
            if role == 0:
                x, y, wx, wy, tu, landed, ab = _kickc_mass(x, y, wx, wy, tau)
            else:
                x, y, wx, wy, tu, landed, ab = _driftc_mass(x, y, wx, wy, tau)
            T += tu
            if ab:
                return x, y, wx, wy, T, nev, ncr, True
            if landed:
                return x, y, wx, wy, T, nev, ncr + 1, False
    return x, y, wx, wy, T, nev, ncr, False

def _c1_phot(x, y, px, py, eta, order):
    """C1 photon step attempt, per-subflow cell anchoring (drift at |u| = 1)."""
    T = 0.0
    nev = 0
    ncr = 0
    for c in ((1.0,) if order == 2 else (W1, W2, W1)):
        nev += 1
        for role in (0, 1, 0):
            r = sqrt(x*x + y*y)
            k = math.frexp(r)[1] - 1
            tau = c*eta*T32[k]*(0.5 if role == 0 else 1.0)
            if role == 0:
                x, y, px, py, tu, landed, ab = _kickc_phot(x, y, px, py, tau)
            else:
                x, y, px, py, tu, landed, ab = _driftc_phot(x, y, px, py, tau)
            T += tu
            if ab:
                return x, y, px, py, T, nev, ncr, True
            if landed:
                return x, y, px, py, T, nev, ncr + 1, False
    return x, y, px, py, T, nev, ncr, False

# ------------------------------------------------------------------- C2 core

def _c2_pick(x, y, vx1, vy1, k, eta, phot):
    """Hut-Makino-McMillan symmetrized shell choice: fixed point of
    k -> shell(kick(Delta_k/2) + drift(Delta_k/2)).  Returns chosen k."""
    visited = [k]
    for _ in range(8):
        sub = eta*T32[k]
        h = 0.5*sub
        r = sqrt(x*x + y*y)
        rs = sqrt(r)
        r32 = r*rs
        s_ = r32 - CB2*h
        if s_ <= HOR32:                       # midpoint would plunge: go finer
            kk = k - 1
            if kk < 1 or kk in visited:
                return min(visited)
            visited.append(kk)
            k = kk
            continue
        q = (s_/r32) ** T23
        inv = 1.0/r
        nx, ny = x*inv, y*inv
        wd = vx1*nx + vy1*ny
        fp = sqrt(q)
        fq = 1.0/q
        wx_ = fq*vx1 + wd*nx*(fp - fq)
        wy_ = fq*vy1 + wd*ny*(fp - fq)
        mx = x*q
        my = y*q
        if phot:
            pn = sqrt(wx_*wx_ + wy_*wy_)
            mx -= h*wx_/pn
            my -= h*wy_/pn
        else:
            g = sqrt(1.0 + wx_*wx_ + wy_*wy_)
            mx += h*wx_/g
            my += h*wy_/g
        km = math.frexp(sqrt(mx*mx + my*my))[1] - 1
        if km == k:
            return k
        if km in visited:
            return min(visited)
        visited.append(km)
        k = km
    return min(visited)

def _c2_step(x, y, vx1, vy1, k, eta, order, phot):
    kuse = _c2_pick(x, y, vx1, vy1, k, eta, phot)
    dt = eta*T32[kuse]
    if phot:
        x, y, vx1, vy1, ab = (s2_phot if order == 2 else s4_phot)(x, y, vx1, vy1, dt)
    else:
        x, y, vx1, vy1, ab = (s2_mass if order == 2 else s4_mass)(x, y, vx1, vy1, dt)
    nev = 1 if order == 2 else 3
    return x, y, vx1, vy1, kuse, dt, nev, ab

# ------------------------------------------------------------ public steppers

def c1_step(x, y, vx1, vy1, k, eta, order, phot):
    """Returns (x, y, v..., k, T_used, steps, crossings, absorbed).
    T_used is the represented step time: within one split step the subflow
    durations sum to twice the represented time (kick h + drift dt + kick h),
    so the accumulated subflow time is halved."""
    if phot:
        x, y, vx1, vy1, T, ev, cr, ab = _c1_phot(x, y, vx1, vy1, eta, order)
    else:
        x, y, vx1, vy1, T, ev, cr, ab = _c1_mass(x, y, vx1, vy1, eta, order)
    kk = math.frexp(sqrt(x*x + y*y))[1] - 1
    return x, y, vx1, vy1, kk, 0.5*T, ev, cr, ab

def c2_step(x, y, vx1, vy1, k, eta, order, phot):
    x, y, vx1, vy1, kuse, T, ev, ab = _c2_step(x, y, vx1, vy1, k, eta, order, phot)
    return x, y, vx1, vy1, kuse, T, ev, 0, ab

def c3_step_pub(x, y, vx1, vy1, k, eta, order, phot):
    out = c3_step(x, y, vx1, vy1, eta, order, phot)
    ab = out[4]
    return out[0], out[1], out[2], out[3], k, eta*RREF32, 1 if order == 2 else 3, 0, ab
# ------------------------------------------------------------------- drivers

def run_bound(cfg, order, eta, p, e, korbits, maxfact=120.0):
    """Bound-orbit probe (massive): advance/orbit, events, energy samples."""
    step = STEPPERS[cfg]
    x, y, wx, wy, E0, L0 = ic_bound_periapsis(p, e)
    k = shell_of(math.sqrt(x*x + y*y))
    T = 0.0
    phi = 0.0
    ph_prev = 0.0
    ev = 0
    cr = 0
    pts = []
    periT = [0.0]
    periPhi = [0.0]
    samples = []
    maxerr = 0.0
    absorbed = False
    maxsteps = int(maxfact*korbits/eta) + 1000
    atan2 = math.atan2
    twopi = 2.0*PI
    r_ = math.sqrt(x*x + y*y)
    while len(periPhi) < korbits + 1 and ev < maxsteps:
        x, y, wx, wy, k, dT, dev, dcr, ab = step(x, y, wx, wy, k, eta, order, False)
        if ab:
            absorbed = True
            break
        T += dT
        ev += 1
        cr += dcr
        ph = atan2(y, x)
        d = ph - ph_prev
        if d > PI:
            d -= twopi
        elif d < -PI:
            d += twopi
        phi += d
        ph_prev = ph
        p3 = (T, math.sqrt(x*x + y*y), phi)
        if len(pts) >= 2:
            (ta, ra, fa), (tb, rb, fb) = pts[-2], pts[-1]
            tc, rc, fc = p3
            if ra > rb and rb <= rc:
                d1 = (rb - ra)/(tb - ta)
                d2 = (rc - rb)/(tc - tb)
                cc = (d2 - d1)/(tc - ta)
                if cc > 0.0:
                    ts = 0.5*(ta + tb) - d1/(2.0*cc)
                    fs = fb + (fb - fa)/(tb - ta)*(ts - tb)
                    periT.append(ts)
                    periPhi.append(fs)
                    n = len(periPhi) - 1
                    err = abs(energy_mass(x, y, wx, wy) - E0)/abs(E0)
                    if err > maxerr:
                        maxerr = err
                    if n % 10 == 0:
                        samples.append((n, maxerr))
                pts = [p3]
            else:
                pts.append(p3)
                if len(pts) > 3:
                    pts = pts[-3:]
        else:
            pts.append(p3)
    n = len(periPhi) - 1
    Ef = energy_mass(x, y, wx, wy)
    Lf = angmom(x, y, wx, wy)
    return {
        "n_orbits": n,
        "advance": (periPhi[n] - periPhi[0])/n - twopi if n > 0 else float("nan"),
        "events": ev, "crossings": cr,
        "events_per_orbit": (ev + cr)/n if n else float("nan"),
        "steps_per_orbit": ev/n if n else float("nan"),
        "T_orbit": periT[n]/n if n else float("nan"),
        "max_dE": maxerr,
        "E_drift": (Ef - E0)/E0, "L_drift": (Lf - L0)/L0,
        "absorbed": absorbed, "samples": samples,
    }

def fit_slope(samples, kmin, kmax):
    xs, ys = [], []
    for k, m in samples:
        if kmin <= k <= kmax and m > 0.0:
            xs.append(math.log(k))
            ys.append(math.log(m))
    if len(xs) < 5:
        return float("nan")
    n = len(xs)
    mx = sum(xs)/n
    my = sum(ys)/n
    return sum((a-mx)*(b-my) for a, b in zip(xs, ys))/sum((a-mx)**2 for a in xs)

def run_photon_r0(cfg, order, eta, b, r0=1.0e4, rexit=1.0e5, maxsteps=4000000):
    """Photon from the exact inbound state at r0 to r_exit outgoing.
    The in/out asymptotic velocity directions differ by the deflection itself,
    so delta = wrapped psi_v rotation + exact quadrature tails at both radii.
    Returns (delta, steps, crossings, absorbed, b_drift)."""
    step = STEPPERS[cfg]
    x, y, px, py = ic_photon_r(b, r0)
    k = shell_of(r0)
    psie = psi_v_of(x, y, px, py)
    ev = 0
    cr = 0
    for _ in range(maxsteps):
        x, y, px, py, k, dT, dev, dcr, ab = step(x, y, px, py, k, eta, order, True)
        if ab:
            return None, ev, cr, True, float("nan")
        ev += 1
        cr += dcr
        if x*x + y*y >= rexit*rexit:
            break
    psix = psi_v_of(x, y, px, py)
    dpsi = math.atan2(math.sin(psix - psie), math.cos(psix - psie))
    delta = dpsi + exact_tail(b, rexit) + exact_tail(b, r0)
    return delta, ev, cr, False, abs(b_of_state(x, y, px, py) - b)/b

def run_capture(L, cfg, order, eta, r0=100.0, maxsteps=400000, resc=350.0):
    """E=1 infall from r0 with angular momentum L -> absorbed/escaped/timeout."""
    step = STEPPERS[cfg]
    x, y, wx, wy = ic_e1_infall(L, r0)
    k = shell_of(r0)
    rmin = rmax = r0
    ev = 0
    for i in range(maxsteps):
        x, y, wx, wy, k, dT, dev, dcr, ab = step(x, y, wx, wy, k, eta, order, False)
        ev += 1
        if ab:
            return "absorbed", rmin, rmax, ev
        r = math.sqrt(x*x + y*y)
        if r < rmin:
            rmin = r
        if r > rmax:
            rmax = r
        if r > resc:
            return "escaped", rmin, rmax, ev
    return "timeout", rmin, rmax, ev
STEPPERS = {"C1": c1_step, "C2": c2_step, "C3": c3_step_pub}

def shell_of(r):
    return math.frexp(r)[1] - 1
