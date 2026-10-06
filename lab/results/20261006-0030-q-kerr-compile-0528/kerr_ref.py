#!/usr/bin/env python3
"""Equatorial Kerr reference compiler, in the crate's own representation.

Units M = c = 1 (report in units of M). Equatorial plane theta = pi/2.

Representation (crates/space/ENVELOPE.md):
    x = R/r = k + (1-k) cos(psi),  k = 1/(1+e),  q = M/R (R = periapsis radius)
    u = 1/r = x/R = (1 + e cos psi) * u_p,   u_p = 1/R
Mino time sigma with d(sigma) = u^2 d(lambda)  (lambda = proper time, mu = 1;
affine for photons). Then (derived in derivation.md, verifying the Opus memo):

    (du/dsigma)^2 = (E^2-mu^2) + 2 mu^2 u - (L^2 - a^2(E^2-mu^2)) u^2
                    + 2 (L-aE)^2 u^3                     [M=1]
  i.e. Schwarzschild's cubic with  L^2 -> L^2 - a^2(E^2-mu^2),
                             2ML^2 -> 2M(L-aE)^2.

Parameter s (the crate's clock): d(sigma) = ds / |L - aE|  (M=1), so

    (du/ds)^2 = 2 (u - u_1)(u_p - u)(u_3 - u),   u_1 = (1-e)/p <= u_p < u_3,
    (dpsi/ds)^2 = 2 (u_3 - u)          (universal: bound e<1, unbound e>1)

  dphi/dpsi = [(L-aE) + a (E - a(L-aE) u^2)/(1-2u+a^2 u^2)] / (|L-aE| sqrt(2(u_3-u)))
  dt/dpsi   = [a(L-aE) + (1+a^2 u^2)(E - a(L-aE) u^2)/(u^2(1-2u+a^2 u^2))]
              / (|L-aE| sqrt(2(u_3-u)))
  dtau/dpsi = 1/(u^2 |L-aE| sqrt(2(u_3-u)))            (mu = 1; photons: none)

At a = 0 these reduce bit for bit (float-level) to ENVELOPE.md's
  g = 1/sqrt(1-qA), dt/dpsi/R^{3/2} = sqrt(k(1-2q)(1+2q(1-2k))) g/((1-2qx)x^2),
  dtau/dpsi/R^{3/2} = sqrt(D) g/x^2,  D = k - q(3k^2+(1-k)^2), A = 6k+2(1-k)cos psi
(see selftest_schwarzschild).
"""

from mpmath import (mp, mpf, sqrt, cos, sin, pi, acos, findroot, polyroots,
                    fabs)

# ---------------------------------------------------------------- GL machinery
_gl_cache = {}

def gauss_legendre(n):
    """Gauss-Legendre nodes/weights on [-1,1] at current mp.dps (n even)."""
    if n % 2 == 1:
        n += 1
    key = (n, mp.dps)
    if key in _gl_cache:
        return _gl_cache[key]
    xs, ws = [], []
    for i in range(n // 2):
        # initial guess (Tricomi style)
        x = cos(pi * (mpf(4 * i + 3) / (4 * n + 2)))
        dp = None
        for _ in range(100):
            p0, p1 = mpf(1), x
            for j in range(2, n + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < mpf(10) ** (-(mp.dps + 4)):
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    xs = xs + [-v for v in reversed(xs)]
    ws = ws + [w for w in reversed(ws)]
    _gl_cache[key] = (xs, ws)
    return xs, ws



# ---------------------------------------------------------------- Kerr kernel
def cubic_coeffs(E, L, a, mu=1):
    """(du/dsigma)^2 = c0 + c1 u + c2 u^2 + c3 u^3, M=1."""
    c0 = E * E - mu * mu
    c1 = 2 * mu * mu
    c2 = -(L * L - a * a * (E * E - mu * mu))
    c3 = 2 * (L - a * E) ** 2
    return c0, c1, c2, c3


def radial_roots(E, L, a, mu=1):
    """Real roots (u_1, u_p, u_3) of the cubic, u_1 <= u_p <= u_3.

    Returns None if the cubic does not have three real roots in the
    bound/scattering/unbound-with-turning configuration (fully plunging).
    """
    c0, c1, c2, c3 = cubic_coeffs(E, L, a, mu)

    def R(u):
        return ((c3 * u + c2) * u + c1) * u + c0

    def verify(rs):
        return all(abs(R(r)) < mpf(10) ** (-mp.dps + 8) * max(1, abs(r)) ** 3
                   for r in rs)

    rs = sorted(r.real for r in polyroots([c3, c2, c1, c0], maxsteps=300,
                                          extraprec=2 * mp.dps))
    if len([r for r in rs if abs(r.imag if hasattr(r, 'imag') else 0) < mpf(10) **
            (-mp.dps + 8)]) != 3 or not verify([mpf(r) for r in rs]):
        # robust fallback: bracket real roots by sign scan + bisection
        rs = []
        hi = max(4.0, 4 * horizon_u(a) + 4)
        lo = -hi
        n = 3000
        prev_u, prev_R = None, None
        for i in range(n + 1):
            u = lo + (hi - lo) * i / n
            # nonuniform: denser where roots live is unnecessary at n=20000
            Ru = R(u)
            if prev_R is not None and prev_R * Ru <= 0:
                a_, b_ = prev_u, u
                fa = prev_R
                for _ in range(200):
                    m = (a_ + b_) / 2
                    fm = R(m)
                    if fa * fm <= 0:
                        b_ = m
                    else:
                        a_, fa = m, fm
                rs.append((a_ + b_) / 2)
            prev_u, prev_R = u, Ru
        rs = sorted(rs)
    return [mpf(r) for r in rs]


def classify(E, L, a, mu=1):
    """Family of the orbit from the root structure.

    'bound'   : 0 < u_1 <= u_p < u_3 < u_horizon   (radial cycle exists)
    'unbound' : u_1 < 0 = u_a, u_p > 0, u_3 > u_p  (one scattering pass)
    'photon'  : mu == 0 variant of the above (E rescaled out; b = L/E)
    'plunge'  : single outer turning point, falls through the horizon
    """
    if mu == 0:
        return "photon"
    rs = radial_roots(E, L, a, mu)
    if len(rs) != 3:
        return "plunge"
    u1, u2, u3 = rs
    uh = horizon_u(a)
    if 0 < u1 and u3 < uh:
        return "bound"
    if u1 < 0 < u2 and u3 < uh:
        return "unbound"      # u_a = 0 reached only at infinity
    return "plunge"


def horizon_u(a):
    """u_+ = 1/r_+ (outer horizon) for M=1."""
    return 1 / (1 + sqrt(1 - a * a))


def integrands(E, L, a, mu=1):
    """Returns (dphi_dpsi, dt_dpsi, dtau_dpsi) as functions of u, plus (u1, up, u3)."""
    rs = radial_roots(E, L, a, mu)
    if len(rs) != 3:
        raise ValueError("no three real roots: fully plunging orbit")
    u1, up, u3 = rs
    Lp = L - a * E                      # L'
    aLp = a * Lp

    def dphi(u):
        return ((Lp + a * (E - aLp * u * u) / (1 - 2 * u + a * a * u * u))
                / (fabs(Lp) * sqrt(2 * (u3 - u))))

    def dt(u):
        den = u * u * (1 - 2 * u + a * a * u * u)
        num = (1 + a * a * u * u) * (E - aLp * u * u)
        return ((aLp + num / den) / (fabs(Lp) * sqrt(2 * (u3 - u))))

    def dtau(u):
        return 1 / (u * u * fabs(Lp) * sqrt(2 * (u3 - u)))

    return dphi, dt, dtau, (u1, up, u3)


def increments(E, L, a, mu=1, n=200, psi_end=None, dps=None):
    """Per-radial-cycle increments by Gauss-Legendre in Darwin's psi.

    Integrates psi in [0, psi_end] and mirrors (all integrands are functions
    of u(psi) only, and u is even in psi). psi_end = pi covers a bound cycle;
    for a finite endpoint radius r_end use psi_end = acos((p*u_end-1)/e).

    Returns dict dphi, dt, dtau (dtau None for mu=0), and shape context.
    """
    old = mp.dps
    if dps:
        mp.dps = dps
    try:
        dphi, dt, dtau, (u1, up, u3) = integrands(E, L, a, mu)
        e = (up - u1) / (up + u1)
        p = 0.5 * (up + u1) * (1 + e) / 1  # u = (1+e cos psi)/p -> p = (1+e)/up
        p = (1 + e) / up
        if psi_end is None:
            psi_end = pi
        xs, ws = gauss_legendre(n)
        half = mpf(psi_end) / 2
        Sphi = St = Sta = mpf(0)
        for x, w in zip(xs, ws):
            psi = half * (x + 1)
            u = (1 + e * cos(psi)) / p
            fac = w * half
            Sphi += fac * dphi(u)
            if mu != 0:
                St += fac * dt(u)
                Sta += fac * dtau(u)
            else:
                St += fac * dt(u)
        out = {"dphi": 2 * Sphi, "dt": 2 * St,
               "dtau": (2 * Sta) if mu != 0 else None,
               "u1": u1, "up": up, "u3": u3, "e": e, "p_slr": p}
        return out
    finally:
        mp.dps = old


def increments_converged(E, L, a, mu=1, tol=None, n0=48, psi_end=None):
    """increments() with n doubled until stable to 5 ulp-ish relative."""
    old = mp.dps
    mp.dps = 34
    try:
        tol = tol or mpf(10) ** (-mp.dps + 6)
        prev = increments(E, L, a, mu, n0, psi_end)
        n = n0
        for _ in range(14):
            n *= 2
            cur = increments(E, L, a, mu, n, psi_end)
            ok = True
            for key in ("dphi", "dt", "dtau"):
                if cur[key] is None:
                    continue
                if abs(cur[key] - prev[key]) > tol * max(abs(cur[key]), mpf(1)):
                    ok = False
            if ok:
                cur["n_nodes"] = n
                return cur
            prev = cur
        cur["n_nodes"] = n
        return cur
    finally:
        mp.dps = old


# ------------------------------------------------- plunge quadrature (in u)
def plunge_increments(E, L, a, u_start, n=400, dps=None):
    """Increments from u_start (outer turning point) down to the horizon.

    Boyer-Lindquist dt diverges logarithmically at the horizon; we return the
    finite (dphi, dtau) and dphi/dt -> Omega_H context. dt is returned as None.
    """
    old = mp.dps
    if dps:
        mp.dps = dps
    try:
        c0, c1, c2, c3 = cubic_coeffs(E, L, a, 1)
        Lp = L - a * E
        aLp = a * Lp
        uh = horizon_u(a)

        def R(u):
            return c3 * u ** 3 + c2 * u * u + c1 * u + c0

        def dphi(u):
            return ((Lp + a * (E - aLp * u * u) / (1 - 2 * u + a * a * u * u))
                    / (fabs(Lp) * sqrt(2 * (u3 - u))))

        rs = radial_roots(E, L, a, 1)
        if len(rs) != 3:
            raise ValueError("plunge with <3 real roots not handled")
        u1, up, u3 = rs
        u_end = 1 / ((1 / uh) * (1 + mpf(10) ** (-9)))  # match direct

        # integrate in Mino sigma: dX = (dX/dsigma) du / sqrt(cubic)
        def dphi_dsigma(u):
            return Lp + a * (E - aLp * u * u) / (1 - 2 * u + a * a * u * u)

        def dtau_dsigma(u):
            return 1 / (u * u)

        xs, ws = gauss_legendre(n)
        Sphi = Sta = mpf(0)
        h = (u_end - u_start) / 2
        for x, w in zip(xs, ws):
            u = u_start + h * (x + 1)
            fac = w * h / sqrt(R(u))
            Sphi += fac * dphi_dsigma(u)
            Sta += fac * dtau_dsigma(u)
        return {"dphi": Sphi, "dt": None, "dtau": Sta,
                "u1": u1, "up": up, "u3": u3, "u_end": u_end}
    finally:
        mp.dps = old


# ------------------------------------------------------ (k,q,chi) <-> (E,L)
def EL_from_shape(k, q, chi, sense="pro", mu=1, dps=None, seed=None):
    """Solve for (E, L) given shape (k, q=M/R) at spin chi (M=1).

    Robust route (derivation.md section 6): the three root identities give
        Sigma_pairs = q^2(2k-1) + 2 q k u_3      =>  L'^2 = mu^2 / Sigma_pairs
        E   = [L'^2 (4qk + 2u_3 - 1) - a^2 mu^2] / (2 a L')
        E^2 = mu^2 - 2 L'^2 q^2 (2k-1) u_3
    a single equation in u_3, bisected on (u_p, u_h) for each sign of L'.
    At a = 0 the closed Schwarzschild form seeds a 2-D Newton instead.
    """
    old = mp.dps
    if dps:
        mp.dps = dps
    try:
        a = mpf(chi)
        k, q = mpf(k), mpf(q)
        up = q
        ua = q * (2 * k - 1)
        sgn = 1 if sense == "pro" else -1

        def try_branch(sign_Lp):
            def EL_of_u3(u3):
                Sp = q * q * (2 * k - 1) + 2 * q * k * u3
                if Sp <= 0:
                    return None
                Lp2 = mu * mu / Sp
                Lp = sign_Lp * sqrt(Lp2)
                E = (Lp2 * (4 * q * k + 2 * u3 - 1) - a * a * mu * mu) / (2 * a * Lp)
                L = Lp + a * E
                return E, L

            def f(u3):
                ELv = EL_of_u3(u3)
                if ELv is None:
                    return None
                E, L = ELv
                Sp = q * q * (2 * k - 1) + 2 * q * k * u3
                Lp2 = mu * mu / Sp
                E2_target = mu * mu - 2 * Lp2 * q * q * (2 * k - 1) * u3
                return E * E - E2_target

            # f can have more than one root (E^2 is sign-blind): scan for all
            # sign changes, bisect each, and let the caller's shape
            # verification pick the physical branch.
            lo0, hi0 = up * (1 + mpf(10) ** -15), horizon_u(a) * (1 - mpf(10) ** -12)
            cands = []
            nscan = 96
            prev_u, prev_f = None, None
            for i in range(nscan + 1):
                u3 = lo0 + (hi0 - lo0) * i / nscan
                # denser near u_h where the weak-field root lives
                w = mpf(i) / nscan
                u3 = lo0 + (hi0 - lo0) * (w * w * (3 - 2 * w))
                fv = f(u3)
                if fv is None:
                    prev_u, prev_f = u3, None
                    continue
                if prev_f is not None and prev_f * fv <= 0:
                    lo, hi, flo = prev_u, u3, prev_f
                    for _ in range(200):
                        mid = (lo + hi) / 2
                        fm = f(mid)
                        if fm is None:
                            hi = mid
                            continue
                        if flo * fm <= 0:
                            hi = mid
                        else:
                            lo, flo = mid, fm
                    ELv = EL_of_u3((lo + hi) / 2)
                    if ELv is not None:
                        cands.append(ELv)
                prev_u, prev_f = u3, fv
            return cands

        out = None
        if abs(a) > mpf(10) ** -14:
            for sign_Lp in (1, -1):
                for cand in try_branch(sign_Lp):
                    E, L = cand
                    if not (0 < E < 1) or sgn * L <= 0:
                        continue
                    rs = radial_roots(E, L, a, mu)
                    if len(rs) != 3:
                        continue
                    u1, u2, u3 = rs
                    if not (0 < u1 <= u2 < u3 < horizon_u(a)):
                        continue
                    if abs(u1 - ua) > mpf(10) ** -10 * max(1, up) or \
                       abs(u2 - up) > mpf(10) ** -10 * max(1, up):
                        continue
                    out = cand
                    break
                if out is not None:
                    break
        if out is None and abs(a) <= mpf(10) ** -14:
            D = k - q * (3 * k * k + (1 - k) ** 2)
            if D <= 0:
                return None
            u3_0 = mpf(1) / 2 - 2 * q * k
            if u3_0 <= up:
                return None
            L2 = mu * mu / (q * D)
            E2 = mu * mu - 2 * L2 * q * q * (2 * k - 1) * u3_0
            if E2 <= 0:
                return None
            out = (sqrt(E2), sgn * sqrt(L2))
        if out is None:
            return None
        E, L = out
        rs = radial_roots(E, L, a, mu)
        if len(rs) != 3:
            return None
        u1, u2, u3 = rs
        if not (0 < u1 <= u2 < u3 < horizon_u(a)):
            return None
        # shape check (increments use the actual roots, so this only guards
        # against landing on the wrong branch)
        if abs(u1 - ua) > mpf(10) ** -10 * max(1, up) or \
           abs(u2 - up) > mpf(10) ** -10 * max(1, up):
            return None
        return E, L
    finally:
        mp.dps = old


# ------------------------------------------------- circular / separatrix scan
def circular_EL(r, chi, sense="pro", mu=1):
    """Exact (E, L) of the circular equatorial orbit at radius r (M=1)."""
    a = mpf(chi)
    s = 1 if sense == "pro" else -1   # upper signs prograde in BPT formulas
    num_E = 1 - 2 / r + s * a / r ** 1.5
    den = 1 - 3 / r + s * 2 * a / r ** 1.5
    if den <= 0 or num_E < 0:
        return None, None
    E = num_E / sqrt(den)
    L = s * sqrt(r) * (1 - 2 * s * a / r ** 1.5 + a * a / (r * r)) / sqrt(den)
    return E, L


def isco(chi, sense="pro"):
    """Bardeen ISCO radius (M=1)."""
    a = mpf(chi)
    s = 1 if sense == "pro" else -1
    Z1 = 1 + (1 - a * a) ** (mpf(1) / 3) * ((1 + a) ** (mpf(1) / 3)
                                             + (1 - a) ** (mpf(1) / 3))
    Z2 = sqrt(3 * a * a + Z1 * Z1)
    return 3 + Z2 - s * sqrt((3 - Z1) * (3 + Z1 + 2 * Z2))


def r_mb(chi, sense="pro"):
    """Marginally-bound circular radius (E = 1), by bisection on E_circ.

    The unstable E = 1 circular orbit lies between r_ph and r_ISCO; E_circ
    diverges at r_ph (returns None below) and E < 1 on (r_mb, r_ISCO).
    """
    lo = horizon_u and (1 + sqrt(1 - mpf(chi) ** 2)) * (1 + mpf(10) ** -9)
    hi = isco(chi, sense)
    for _ in range(300):
        mid = (lo + hi) / 2
        Em, _ = circular_EL(mid, chi, sense)
        if Em is None or Em > 1:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def separatrix_curve(chi, sense="pro", n=400):
    """Scan the unstable-circular radius r_w from ISCO (e=0) to r_mb (e=1).

    The separatrix (zoom-whirl) orbit has its double root at the PERICENTER:
    u_w is the whirl radius, u_s = Lt^2/(2 L'^2) - 2 u_w the simple root
    (apocenter side). e = (u_w - u_s)/(u_w + u_s), k = (1-e)/(1+e), q = u_w.
    Schwarzschild check: p_sep = 6 + 2e exactly.
    """
    out = []
    r_i, r_b = isco(chi, sense), r_mb(chi, sense)
    for i in range(n + 1):
        f = mpf(i) / n
        r_w = r_i + (r_b - r_i) * f
        E, L = circular_EL(r_w, chi, sense)
        if E is None:
            continue
        a = mpf(chi)
        Lp = L - a * E
        Lt2 = L * L - a * a * (E * E - 1)
        u_w = 1 / r_w
        u_s = Lt2 / (2 * Lp * Lp) - 2 * u_w
        if u_s <= 0 or u_w <= 0:
            e = mpf(1)
        else:
            e = (u_w - u_s) / (u_w + u_s)
        k = (1 - e) / (1 + e)
        out.append((k, u_w))
    return out


def q_sep_of_k(k, chi, sense="pro"):
    """Separatrix q for given k: solve u_s/u_w = 2k-1 along the curve."""
    a = mpf(chi)

    def g(r_w):
        E, L = circular_EL(r_w, chi, sense)
        if E is None:
            return None
        Lp = L - a * E
        Lt2 = L * L - a * a * (E * E - 1)
        u_w = 1 / r_w
        u_s = Lt2 / (2 * Lp * Lp) - 2 * u_w
        return u_s / u_w - (2 * k - 1)

    if k >= 1:
        return 1 / isco(chi, sense)
    rlo = r_mb(chi, sense) * (1 + mpf(10) ** -12)
    rhi = isco(chi, sense) * (1 - mpf(10) ** -10)
    if rhi <= rlo:
        return None
    if g(rlo) is None or g(rhi) is None:
        return None
    if g(rlo) * g(rhi) > 0:
        return None
    for _ in range(200):
        mid = (rlo + rhi) / 2
        gm = g(mid)
        if gm is None:
            rhi = mid
            continue
        if g(rlo) * gm <= 0:
            rhi = mid
        else:
            rlo = mid
    r_w = (rlo + rhi) / 2
    E, L = circular_EL(r_w, chi, sense)
    Lp = L - a * E
    Lt2 = L * L - a * a * (E * E - 1)
    return 1 / r_w


# ------------------------------------------------------------------ photons
def photon_shape(b, chi, sense="pro"):
    """(k, q, E, L-scale) for a photon of impact parameter b (M=1).

    The null cubic (mu=0) with E=1, L=b: c0 = 1, c1 = 0,
    c2 = -(b^2 - a^2), c3 = 2(b-a)^2. Returns roots and e/p shape.
    """
    a = mpf(chi)
    E = mpf(1)
    L = mpf(b)
    rs = radial_roots(E, L, a, 0)
    if len(rs) != 3:
        return None
    u1, up, u3 = rs
    if not (u1 < 0 < up < u3):
        return None
    e = (up - u1) / (up + u1)
    p = (1 + e) / up
    return {"u1": u1, "up": up, "u3": u3, "e": e, "k": (1 - e) / (1 + e),
            "q": up, "E": E, "L": L}


def photon_bc(chi, sense="pro"):
    """Critical impact parameter (double root of the null cubic), M=1.

    Closed form (Bardeen): r_ph = 2(1+cos((2/3) arccos(-+a))), and
    b_c = -[r^3 - 3r^2 + a^2 r + a^2] / (a (r - 1)) for a != 0, else 3 sqrt 3.
    """
    a = mpf(chi)
    if sense == "pro":
        r = 2 * (1 + cos((mpf(2) / 3) * acos(-a)))
    else:
        r = 2 * (1 + cos((mpf(2) / 3) * acos(a)))
    if abs(a) < mpf(10) ** -12:
        return 3 * sqrt(3)
    return -(r ** 3 - 3 * r * r + a * a * r + a * a) / (a * (r - 1))


# ------------------------------------------------------ selftests (Schw.)
def envelope_integrands(k, q):
    """ENVELOPE.md's Schwarzschild integrands as functions of psi (M=1)."""
    A = lambda psi: 6 * k + 2 * (1 - k) * cos(psi)
    x = lambda psi: k + (1 - k) * cos(psi)
    g = lambda psi: 1 / sqrt(1 - q * A(psi))
    D = k - q * (3 * k * k + (1 - k) ** 2)
    dphi = lambda psi: g(psi)
    dt = lambda psi: (sqrt(k * (1 - 2 * q) * (1 + 2 * q * (1 - 2 * k)))
                      * g(psi) / ((1 - 2 * q * x(psi)) * x(psi) ** 2))
    dtau = lambda psi: sqrt(D) * g(psi) / x(psi) ** 2
    return dphi, dt, dtau


def selftest_schwarzschild(k=None, q=None, n=64):
    """Kerr integrands at a=0 equal ENVELOPE.md's, to rounding."""
    if k is None:
        k = mpf(3) / 4
    if q is None:
        q = mpf(1) / 40
    # shape -> (E, L) at chi = 0 (closed form)
    D = k - q * (3 * k * k + (1 - k) ** 2)
    u3_0 = mpf(1) / 2 - 2 * q * k
    L2 = 1 / (q * D)
    E2 = 1 - 2 * L2 * q * q * (2 * k - 1) * u3_0
    E, L = sqrt(E2), sqrt(L2)
    dphi, dt, dtau, (u1, up, u3) = integrands(E, L, 0, 1)
    R = 1 / q  # periapsis radius = 1/u_p
    ep, et, eta = envelope_integrands(k, q)
    up_ = q
    e = (up - u1) / (up + u1)
    p = (1 + e) / up
    worst = 0
    for i in range(13):
        psi = pi * i / 12
        u = (1 + e * cos(psi)) / p
        xx = R * u
        worst = max(worst, abs(dphi(u) - ep(psi)) / abs(ep(psi)))
        worst = max(worst, abs(dt(u) / R ** 1.5 - et(psi)) / abs(et(psi)))
        worst = max(worst, abs(dtau(u) / R ** 1.5 - eta(psi)) / abs(eta(psi)))
    return worst


if __name__ == "__main__":
    mp.dps = 40
    print("selftest Schwarzschild reduction, worst rel diff:",
          selftest_schwarzschild())
    # circular-orbit closed forms vs our increments at k=1
    for chi in (0, 0.5, 0.9, 0.998):
        for sense in ("pro", "retro"):
            r = isco(chi, sense)
            print(f"isco chi={chi} {sense}: {r}")
    for chi in (0.5, 0.9, 0.998):
        for sense in ("pro", "retro"):
            print(f"b_crit chi={chi} {sense}: {photon_bc(chi, sense)}")
