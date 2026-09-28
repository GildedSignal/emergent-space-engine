#!/usr/bin/env python3
"""Independent Arb reference ("judge") for the step 2 gravity contract, es-lattice-gravity-v0.

Scope (docs/gravity-law.md, "Step 2 scope"): one static mass M at the origin, test bodies and
light rays in the equatorial plane, Painleve-Gullstrand (river) coordinates, lattice units
(X in quanta, T in chronons, c = Q, M = GM/c^2 in quanta).

Method, chosen to share nothing with crates/geodesic (Carlson integrals in Mino time):
- Exact integer preprocessing decides every symbolic case: T = T0, T < T0, radial motion
  (x0 x k0 = 0, the off-line coordinate of axis motion is exactly 0), exact turning points,
  exact circular orbits and exact E = 1.
- The first integrals E, L and the radial cubic R(u) = E^2 - eps + 2M eps u - L^2 u^2
  + 2M L^2 u^3 (u = 1/r, eps = 1 timelike, 0 null) are Arb balls. Real roots are certified
  by the interval Newton operator.
- The geodesic is followed in a uniformizing phase that passes smoothly through turning
  points: chi with u = m - h cos chi between two roots, a signed sigma with u = u_t + sigma^2
  from a root to the horizon or to infinity, the cycloid eta or w = sqrt(r) for radial
  motion. dT, dphi and dtau are integrated in that phase by rigorous Gauss-Legendre
  quadrature (acb.integral). The river-time integrand is rationalized exactly,
  dT/dtau = (E^2 + 2Mu(eps + L^2 u^2)) / (E - sqrt(2Mu) dr/dtau), so it is regular at the
  horizon and no divergent logarithm is ever formed.
- T -> phase is inverted by safeguarded Newton and certified by the interval Newton operator.
- A floor, a ceiling or a comparison is used only when its ball decides it. Otherwise the
  whole case is recomputed at the next precision (256, 512, 1024, 2048 bits); a case still
  undecided is UNSETTLED, never guessed.

Command line:
  geodesic_judge.py solve CASES.jsonl.gz OUT.jsonl.gz [--prec-index I] [--workers N]
  geodesic_judge.py one M Q t0 x y kx ky timelike|null T [T ...]
"""
import gzip
import json
import math
import os
import sys
import time

from flint import acb, arb, ctx

PRECS = (256, 512, 1024, 2048)
LIM = 2 ** 96          # coordinate range, per component
M_MAX = 2 ** 80
Q_MAX = 2 ** 40


class Undecided(Exception):
    """A ball could not decide something at the current precision."""


class Invalid(Exception):
    """The anchor violates the contract's construction rules."""


# ----------------------------------------------------------------------------------------
# Ball helpers


def sgn(x, what):
    if x > 0:
        return 1
    if x < 0:
        return -1
    raise Undecided(what)


def floor_int(x, what):
    if not x.is_finite():
        raise Undecided(what)
    lo = int(x.lower().floor().unique_fmpz())
    hi = int(x.upper().floor().unique_fmpz())
    if lo != hi:
        raise Undecided(what)
    return lo


def ceil_int(x, what):
    if not x.is_finite():
        raise Undecided(what)
    lo = int(x.lower().ceil().unique_fmpz())
    hi = int(x.upper().ceil().unique_fmpz())
    if lo != hi:
        raise Undecided(what)
    return lo


def exact(x):
    """An exact dyadic point of the ball x (its midpoint)."""
    return x.mid()


def fl(x):
    return float(x.mid())


def integ(f, a, b):
    """Rigorous integral of f from the exact point a to the exact point b."""
    if a.is_exact() and b.is_exact() and a == b:
        return arb(0)
    v = acb.integral(f, acb(a), acb(b))
    r = v.real
    if not r.is_finite():
        raise Undecided("quadrature")
    return r


def mv(f, z, zm):
    """Enclosure of the integral of f from the exact point zm to an unknown point of ball z
    that contains zm (mean value theorem)."""
    if z.is_exact() and z == zm:
        return arb(0)
    fz = f(acb(z), False).real
    if not fz.is_finite():
        raise Undecided("mean value")
    return fz * (z - zm)


class Prim:
    """Primitive of an integrand relative to an exact base point, with a cache of exact
    points so that successive evaluations integrate over short intervals."""

    def __init__(self, f, base):
        self.f = f
        self.base = fl(base)
        self.pts = [(base, self.base, arb(0))]

    def at(self, z):
        # Start from the nearest cached point lying between the base and z, so a value is
        # never derived from a larger one (whose absolute error would be inherited).
        zf = fl(z)
        lo, hi = min(self.base, zf), max(self.base, zf)
        best = min((p for p in self.pts if lo <= p[1] <= hi), key=lambda p: abs(p[1] - zf))
        if best[0] == z:
            return best[2]
        v = best[2] + integ(self.f, best[0], z)
        self.pts.append((z, zf, v))
        return v

    def at_ball(self, z):
        zm = exact(z)
        return self.at(zm) + mv(self.f, z, zm)


class LinPrim:
    def __init__(self, rate):
        self.rate = rate

    def at(self, z):
        return self.rate * z

    def at_ball(self, z):
        return self.rate * z


# ----------------------------------------------------------------------------------------
# Exact anchor data and symbolic decisions (integers only)


def isqrt_exact(n):
    r = math.isqrt(n)
    return r if r * r == n else None


def sign_int(v):
    return (v > 0) - (v < 0)


def sign_a_plus_b_sqrt_n(A, B, n):
    """Exact sign of A + B*sqrt(n) for integers, B >= 0, n >= 0."""
    if B == 0 or n == 0:
        return sign_int(A)
    if A >= 0:
        return 1
    return sign_int(B * B * n - A * A)


def timelike_E_is_one(M, Q, n, d, K):
    """Exact test of E == 1 for a timelike anchor (derivation in PROVENANCE.md).

    E = 1  <=>  A + B r0 = -4 M d Q sqrt(2 M r0), r0 = sqrt(n), with
    A = 2M(d^2 - Q^2 n), B = 4M^2 Q^2 + K n. Squaring twice with sign conditions."""
    A = 2 * M * (d * d - Q * Q * n)
    B = 4 * M * M * Q * Q + K * n
    lhs_sign = sign_a_plus_b_sqrt_n(A, B, n)
    if lhs_sign != -sign_int(d):
        return False
    D = 32 * M ** 3 * d * d * Q * Q - 2 * A * B
    if D <= 0:
        return False
    return (A * A + B * B * n) ** 2 == D * D * n


class Anchor:
    def __init__(self, M, Q, t0, x, k, null):
        M, Q, t0 = int(M), int(Q), int(t0)
        a, b = int(x[0]), int(x[1])
        kx, ky = int(k[0]), int(k[1])
        if not (1 <= M <= M_MAX):
            raise Invalid("M out of range")
        if not (1 <= Q <= Q_MAX):
            raise Invalid("Q out of range")
        if abs(a) > LIM or abs(b) > LIM:
            raise Invalid("x out of range")
        n = a * a + b * b
        if n <= 4 * M * M:
            raise Invalid("r <= 2M")
        if null and kx == 0 and ky == 0:
            raise Invalid("zero null direction")
        self.M, self.Q, self.t0, self.a, self.b, self.kx, self.ky = M, Q, t0, a, b, kx, ky
        self.null = bool(null)
        self.eps = 0 if null else 1
        self.n = n
        self.rn = isqrt_exact(n)
        self.d = kx * a + ky * b          # k . x
        self.c = a * ky - b * kx          # x cross k  (sign of L)
        self.K = kx * kx + ky * ky
        d, K = self.d, self.K
        # Exact sign of dr/dT at the anchor.
        if not null:
            self.rdot_sign = sign_int(d)
        elif d <= 0:
            self.rdot_sign = -1
        else:
            self.rdot_sign = sign_int(d ** 4 - 4 * M * M * K * K * n)
        self.radial = self.c == 0
        self.circular = False
        self.rprime_sign = None
        if not self.radial and self.rdot_sign == 0:
            # Exact sign of R'(u0): timelike sign(M/r0 - v^2), null sign(3M - r0).
            if not null:
                self.rprime_sign = sign_int(M * M * Q ** 4 - K * K * n)
            else:
                self.rprime_sign = sign_int(9 * M * M - n)
            self.circular = self.rprime_sign == 0
        self.E_one = (not null) and timelike_E_is_one(M, Q, n, d, K)

    def key(self):
        return (self.M, self.Q, self.t0, self.a, self.b, self.kx, self.ky, self.null)


# ----------------------------------------------------------------------------------------
# The geodesic at one precision


class Geo:
    def __init__(self, A, prec):
        self.A = A
        self.prec = prec
        ctx.prec = prec
        M = arb(A.M)
        Q = arb(A.Q)
        self.Mb, self.Qb = M, Q
        n = arb(A.n)
        r0 = arb(A.rn) if A.rn is not None else n.sqrt()
        self.r0 = r0
        s = (2 * M / r0).sqrt()
        d, c, K = arb(A.d), arb(A.c), arb(A.K)
        eps = A.eps
        if not A.null:
            gap = Q * Q - (K + 2 * Q * d * s / r0 + Q * Q * s * s)   # Q^2 - |k - beta|^2
            if sgn(gap, "timelike validity") < 0:
                raise Invalid("not below c relative to the flow")
            gam = (Q * Q / gap).sqrt()
            E = gam * (1 - s * d / (Q * r0) - s * s)
            L = gam * c / Q
            rdot = gam * d / (Q * r0)
            if A.E_one:
                E = arb(1)
        else:
            kn = K.sqrt()
            E = 1 - s * d / (kn * r0)
            L = c / kn
            rdot = -s + d / (kn * r0)
        if A.rdot_sign == 0:
            rdot = arb(0)
        self.E, self.L, self.rdot0 = E, L, rdot
        self.sL = sign_int(A.c)
        self.Lab = abs(L) if A.c != 0 else arb(0)
        self.eps = eps
        self.u0 = 1 / r0
        self.uh = 1 / (2 * M)
        self.info = {}
        self.period = False
        self.horizon = False
        self.escape = False
        self.zinf = None
        if A.radial:
            self._setup_radial()
        elif A.circular:
            self._setup_circular()
        else:
            self._setup_cubic()
        self._finish()

    # --- charts -------------------------------------------------------------------------

    def _setup_radial(self):
        A, M, E = self.A, self.Mb, self.E
        self.chart = "radial"
        if not A.null:
            if A.E_one:
                p2s = 0
            else:
                p2s = sgn(E * E - 1, "radial energy")
        if not A.null and p2s < 0:
            om = 1 - E * E                 # 2M / r_max
            rmax = 2 * M / om
            so = om.sqrt()
            self.info.update(kind="radial-bound", r_max=rmax)
            E2 = E * E

            def uz(z):
                c2 = (z / 2).cos()
                return 1 / (rmax * c2 * c2)

            def fT(z, an):
                c2 = (z / 2).cos()
                r = rmax * c2 * c2
                rdot = -so * (z / 2).tan()
                su = so / c2                  # sqrt(2M/r)
                dtau = r / so
                return (E2 + 2 * M / r) / (E - su * rdot) * dtau

            def ftau(z, an):
                c2 = (z / 2).cos()
                return rmax * c2 * c2 / so

            self.fT, self.ftau, self.fphi = fT, ftau, None
            self.uz = uz
            if A.rdot_sign == 0:
                self.z0 = arb(0)
            else:
                self.z0 = 2 * (-self.rdot0 / so).atan()
            self.zh = 2 * (E / so).atan()
            self.horizon = True
            self.turns = [arb(0)]            # r increases for z < 0, decreases for z > 0
            self.r_future_max = rmax if A.rdot_sign > 0 else self.r0
            return
        # w = sqrt(r); z = dirn * w increases with time.
        dirn = A.rdot_sign
        if dirn == 0:
            raise Undecided("radial static anchor with E >= 1")   # impossible for r > 2M
        s2M = (2 * M).sqrt()
        if A.null:
            self.info.update(kind="radial-null-out" if dirn > 0 else "radial-null-in")

            def fT(z, an):
                w = dirn * z
                return 2 * w * w / (w - dirn * s2M)

            ftau = None
        else:
            p2 = arb(0) if A.E_one else E * E - 1
            E2 = E * E
            self.info.update(kind="radial-unbound-out" if dirn > 0 else "radial-in")

            def ftau(z, an):
                w = dirn * z
                return 2 * w * w / (p2 * w * w + 2 * M).sqrt(analytic=an)

            def fT(z, an):
                w = dirn * z
                root = (p2 * w * w + 2 * M).sqrt(analytic=an)
                rdot = dirn * root / w
                dtau = 2 * w * w / root
                return (E2 + 2 * M / (w * w)) / (E - (s2M / w) * rdot) * dtau

        self.fT, self.ftau, self.fphi = fT, ftau, None
        self.uz = lambda z: 1 / (z * z)
        self.z0 = dirn * self.r0.sqrt()
        self.turns = []
        if dirn < 0:
            self.zh = -s2M
            self.horizon = True
            self.r_future_max = self.r0
        else:
            self.escape = True
            self.zinf = None                 # z -> +infinity
            self.r_future_max = None

    def _setup_circular(self):
        A, M = self.A, self.Mb
        self.chart = "circular"
        r0 = self.r0
        om = (M / (r0 * r0 * r0)).sqrt()
        self.info.update(kind="circular")
        self.omega = om
        self.tau_rate = arb(0) if A.null else (1 - 3 * M / r0).sqrt()
        self.r_future_max = r0

    def _setup_cubic(self):
        A, M, E, L = self.A, self.Mb, self.E, self.L
        eps = self.eps
        L2 = L * L
        bb = -1 / (2 * M)
        cc = arb(eps) / L2 if eps else arb(0)
        dd = arb(0) if A.E_one else (E * E - eps) / (2 * M * L2)
        self.bb, self.cc, self.dd = bb, cc, dd
        P = lambda u: ((u + bb) * u + cc) * u + dd
        dP = lambda u: (3 * u + 2 * bb) * u + cc
        disc = 18 * bb * cc * dd - 4 * bb ** 3 * dd + bb * bb * cc * cc - 4 * cc ** 3 - 27 * dd * dd
        nroots = 3 if sgn(disc, "cubic discriminant") > 0 else 1
        roots = self._roots(P, dP, nroots)
        if A.E_one:
            # u = 0 is an exact root; replace its (tiny) ball by exact 0.
            i = min(range(len(roots)), key=lambda j: abs(fl(roots[j])))
            if not roots[i].contains(0):
                raise Undecided("E=1 root")
            roots[i] = arb(0)
        self.roots = roots
        R0sign = 0 if A.E_one else sgn(E * E - eps, "E^2 - eps")   # sign of R(0)
        u0 = self.u0
        if A.rdot_sign == 0:
            rp = A.rprime_sign
            if nroots == 3:
                if rp < 0:
                    region, z0 = "A", arb.pi()          # u0 = u2 (periapsis)
                elif A.n > 36 * A.M * A.M:
                    region, z0 = "A", arb(0)            # u0 = u1 (apoapsis)
                else:
                    region, z0 = "B", arb(0)            # u0 = u3 (inner apoapsis)
            else:
                if rp <= 0:
                    raise Undecided("turning point inconsistent with one real root")
                region, z0 = "C", arb(0)
        else:
            z0 = None
            if nroots == 3:
                if u0 < roots[1]:
                    region = "A"
                elif u0 > roots[2]:
                    region = "B"
                else:
                    raise Undecided("region")
            else:
                region = "C"
        self.region = region
        s2M = (2 * M).sqrt()
        E2 = E * E
        Lab = self.Lab
        L2eps = arb(eps)

        def dTdtau(u, rdot, an):
            su = (2 * M * u).sqrt(analytic=an)
            return (E2 + 2 * M * u * (L2eps + L2 * u * u)) / (E - su * rdot)

        if region == "A":
            u1, u2, u3 = roots
            m = (u1 + u2) / 2
            h = (u2 - u1) / 2
            self.chart = "three-root"
            self.m, self.h, self.u3 = m, h, u3

            def uz(z):
                return u1 + 2 * h * (z / 2).sin() ** 2

            def fphi(z, an):
                u = u1 + 2 * h * (z / 2).sin() ** 2
                return 1 / (2 * M * (u3 - u)).sqrt(analytic=an)

            def ftau(z, an):
                u = u1 + 2 * h * (z / 2).sin() ** 2
                return 1 / (Lab * u * u * (2 * M * (u3 - u)).sqrt(analytic=an))

            def fT(z, an):
                u = u1 + 2 * h * (z / 2).sin() ** 2
                sq = (2 * M * (u3 - u)).sqrt(analytic=an)
                rdot = -Lab * h * z.sin() * sq
                return dTdtau(u, rdot, an) / (Lab * u * u * sq)

            if z0 is None:
                cz = (m - u0) / h
                sz = -self.rdot0 / (Lab * h * (2 * M * (u3 - u0)).sqrt())
                z0 = arb.atan2(sz, cz)
                if z0 < 0:
                    z0 = z0 + 2 * arb.pi()
                elif not z0 >= 0:
                    raise Undecided("anchor phase")
            self.turns = "periodic-pi"
            bound = (R0sign < 0) if eps else False
            if bound:
                self.period = True
                self.info.update(kind="bound")
                self.r_future_max = 1 / u1
            else:
                self.escape = True
                self.info.update(kind="unbound")
                if A.E_one:
                    self.zinf = 2 * arb.pi()
                else:
                    self.zinf = 2 * arb.pi() - 2 * ((-u1) / (2 * h)).sqrt().asin()   # u = 0
                self.r_future_max = None
        else:
            if region == "B":
                u1, u2, u3 = roots
                ut = u3
                self.chart = "three-root"

                def qf(u):
                    return (u - u1) * (u - u2)
            else:
                ut = roots[0]
                self.chart = "one-root"
                b1 = bb + ut
                c1 = cc + ut * b1

                def qf(u):
                    return (u + b1) * u + c1
            self.ut = ut

            def uz(z):
                return ut + z * z

            def fphi(z, an):
                u = ut + z * z
                return 2 / (2 * M * qf(u)).sqrt(analytic=an)

            def ftau(z, an):
                u = ut + z * z
                return 2 / (Lab * u * u * (2 * M * qf(u)).sqrt(analytic=an))

            def fT(z, an):
                u = ut + z * z
                sq = (2 * M * qf(u)).sqrt(analytic=an)
                rdot = -Lab * z * sq
                return dTdtau(u, rdot, an) * 2 / (Lab * u * u * sq)

            if z0 is None:
                z0 = -self.rdot0 / (Lab * (2 * M * qf(u0)).sqrt())
            self.turns = [arb(0)]
            ut_pos = (R0sign < 0) if region == "C" else True   # u3 > 0 always
            # sign(sigma0) = -sign(dr/dT), decided exactly from the integers.
            if ut_pos or A.rdot_sign < 0:
                self.horizon = True
                self.zh = (self.uh - ut).sqrt()
                self.info.update(kind="plunging")
                if A.rdot_sign >= 0:
                    self.r_future_max = 1 / ut
                else:
                    self.r_future_max = self.r0
            else:
                self.escape = True
                self.info.update(kind="unbound")
                self.zinf = arb(0) if A.E_one else -(-ut).sqrt()
                self.r_future_max = None
        self.fT, self.fphi, self.ftau, self.uz = fT, fphi, ftau, uz
        self.z0 = z0
        if self.eps == 0:
            self.ftau = None

    def _phase_of_u(self, u):
        """Chart A phase in [0, pi] where u(chi) = u1 + 2h sin^2(chi/2) equals u."""
        return 2 * ((u - self.roots[0]) / (2 * self.h)).sqrt().asin()

    def _roots(self, P, dP, nroots):
        """Certified enclosures of the real roots of the monic cubic, ascending."""
        bb, cc, dd = self.bb, self.cc, self.dd
        p = cc - bb * bb / 3
        q = 2 * bb ** 3 / 27 - bb * cc / 3 + dd
        shift = -bb / 3
        approx = []
        if nroots == 3:
            if not p < 0:
                raise Undecided("three roots with p >= 0")
            rad = 2 * (-p / 3).sqrt()
            arg = (3 * q / (2 * p)) * (-3 / p).sqrt()
            argm = arb(max(-1.0, min(1.0, fl(arg)))) if not arg.mid().is_finite() else exact(arg)
            if argm > 1:
                argm = arb(1)
            if argm < -1:
                argm = arb(-1)
            ph = argm.acos() / 3
            for kk in range(3):
                approx.append(exact(rad * (ph - 2 * arb.pi() * kk / 3).cos() + shift))
        else:
            disc = q * q / 4 + p ** 3 / 27
            sq = exact(disc).sqrt() if disc > 0 else arb(0)
            a1 = exact(-q / 2 + sq)
            a2 = exact(-q / 2 - sq)
            cbrt = lambda v: (v.root(3) if v > 0 else (-(-v).root(3) if v < 0 else arb(0)))
            approx.append(exact(cbrt(a1) + cbrt(a2) + shift))
        out = []
        for x in approx:
            x = self._polish(P, dP, x)
            out.append(self._certify_root(P, dP, x))
        out.sort(key=fl)
        for i in range(len(out) - 1):
            if not out[i] < out[i + 1]:
                raise Undecided("root separation")
        return out

    def _polish(self, P, dP, x):
        for _ in range(self.prec // 2 + 60):
            px = P(x)
            dpx = dP(x)
            if not dpx.is_finite() or dpx.contains(0):
                break
            nx = exact(x - px / dpx)
            if nx == x:
                break
            dx = nx - x
            x = nx
            if abs(dx) < abs(x) * arb(2) ** (-self.prec + 4):
                break
        return x

    def _certify_root(self, P, dP, x):
        scale = abs(x) + abs(self.bb)
        px = P(x)
        d0 = dP(x)
        if not d0.is_finite() or d0.contains(0):
            raise Undecided("root derivative")
        delta = 4 * abs(px).upper() / abs(d0).lower() + scale * arb(2) ** (-self.prec + 8)
        delta = exact(delta)
        for _ in range(10):
            Z = arb(x, delta)
            dz = dP(Z)
            if dz.is_finite() and not dz.contains(0):
                N = x - px / dz
                if Z.contains_interior(N):
                    return N
            delta = 16 * delta
        raise Undecided("root certification")

    def _finish(self):
        A = self.A
        if self.chart == "circular":
            self.Tprim = LinPrim(arb(1))
            self.Gprim = LinPrim(self.omega)
            self.Hprim = LinPrim(self.tau_rate)
            self.base = arb(0)
            self.F0z0 = arb(0)
            self.G0z0 = arb(0)
            self.H0z0 = arb(0)
            self.z0 = arb(0)
            return
        if self.period:
            base = arb(0)
        else:
            base = exact(self.z0)
        self.base = base
        self.Tprim = Prim(self.fT, base)
        self.Gprim = Prim(self.fphi, base) if self.fphi is not None else None
        self.Hprim = Prim(self.ftau, base) if self.ftau is not None else None
        self.F0z0 = self.Tprim.at_ball(self.z0)
        self.G0z0 = self.Gprim.at_ball(self.z0) if self.Gprim else arb(0)
        self.H0z0 = self.Hprim.at_ball(self.z0) if self.Hprim else arb(0)
        if self.period:
            tp = 2 * arb.pi()
            self.PT = self.Tprim.at_ball(tp)
            self.PG = self.Gprim.at_ball(tp)
            self.PH = self.Hprim.at_ball(tp) if self.Hprim else arb(0)
        if self.horizon:
            self.dTh = self.Tprim.at_ball(self.zh) - self.F0z0        # quanta
            self.dHh = (self.Hprim.at_ball(self.zh) - self.H0z0) if self.Hprim else arb(0)

    # --- phase <-> time ----------------------------------------------------------------

    def _F(self, k, z):
        """Time in quanta from the anchor to the point (k periods, exact phase z)."""
        v = self.Tprim.at(z) - self.F0z0
        if k:
            v = v + k * self.PT
        return v

    def _Fb(self, k, Z):
        v = self.Tprim.at_ball(Z) - self.F0z0
        if k:
            v = v + k * self.PT
        return v

    def _theta_b(self, k, Z):
        if self.Gprim is None:
            if self.chart == "circular":
                return self.sL * self.omega * Z
            return arb(0)
        v = self.Gprim.at_ball(Z) - self.G0z0
        if k:
            v = v + k * self.PG
        return self.sL * v

    def _tau_b(self, k, Z):
        if self.chart == "circular":
            return self.tau_rate * Z
        if self.Hprim is None:
            return arb(0)
        v = self.Hprim.at_ball(Z) - self.H0z0
        if k:
            v = v + k * self.PH
        return v

    def _u_b(self, Z):
        if self.chart == "circular":
            return 1 / self.r0
        return self.uz(Z)

    def solve(self, y):
        """(k, Z): the phase ball Z (k whole periods) where the time since the anchor is y."""
        ctx.prec = self.prec
        if self.chart == "circular":
            return 0, y
        if self.period:
            Y = self.F0z0 + y
            k = int(math.floor(fl(Y / self.PT)))
            yp = Y - k * self.PT
            lo, hi = arb(-1), exact(2 * arb.pi() + 1)
            Z = self._invert(lambda z: self.Tprim.at(z), yp, lo, hi)
            return k, Z
        yb = self.F0z0 + y
        if self.horizon:
            # T < T_h is established, so the root lies before the horizon phase.
            Z = self._invert(lambda z: self.Tprim.at(z), yb, exact(self.z0), exact(self.zh))
            return 0, Z
        return 0, self._invert_escape(yb)

    def _newton(self, F, y, lo, hi, Flo, Fhi, to_z, dzdv, v):
        """Safeguarded Newton on v with bracket [lo, hi]; returns an exact point z near the
        root of F(z) = y."""
        prec = self.prec
        z = to_z(v)
        for _ in range(400):
            Fz = F(z)
            D = Fz - y
            if D > 0:
                hi, Fhi = v, Fz
            elif D < 0:
                lo, Flo = v, Fz
            else:
                return z
            fz = self.fT(acb(z), False).real * dzdv(v)
            step = D.mid() / fz.mid()
            nv = exact(v - step)
            if not (nv > lo and nv < hi):
                nv = exact((lo + hi) / 2)
            if nv == v:
                return z
            tol = (abs(v) + 1) * arb(2) ** (-prec + 6)
            v = nv
            z = to_z(v)
            if abs(step) < tol:
                return z
        raise Undecided("inversion did not converge")

    def _invert(self, F, y, lo, hi):
        Flo = F(lo)
        Fhi = F(hi)
        if not (Flo <= y and y <= Fhi):
            raise Undecided("inversion bracket")
        # initial guess by linear interpolation
        t = (y - Flo) / (Fhi - Flo)
        v = exact(lo + t * (hi - lo))
        if not (v > lo and v < hi):
            v = exact((lo + hi) / 2)
        za = self._newton(F, y, lo, hi, Flo, Fhi, lambda v: v, lambda v: arb(1), v)
        return self._certify(F, y, za)

    def _invert_escape(self, y):
        F = lambda z: self.Tprim.at(z)
        z0 = exact(self.z0)
        Fz0 = F(z0)
        if self.zinf is None:
            # w chart: z = w -> infinity
            to_z = lambda v: v
            dzdv = lambda v: arb(1)
            lo = z0
            f0 = self.fT(acb(z0), False).real
            hi = exact(z0 + 2 * (y - Fz0) / f0 + 1)
            while True:
                Fhi = F(hi)
                if Fhi > y:
                    break
                hi = exact(2 * hi)
        else:
            zi = self.zinf
            zim = exact(zi)
            # xi = 1/(zinf - z); keep points strictly below zinf
            to_z = lambda v: exact(zim - 1 / v)
            dzdv = lambda v: 1 / (v * v)
            lo = exact(1 / (zim - z0))
            if not lo > 0:
                raise Undecided("escape start")
            f0 = self.fT(acb(z0), False).real / (lo * lo)
            hi = exact(lo + 2 * (y - Fz0) / f0 + 1)
            while True:
                zh = to_z(hi)
                if not zh < zi:
                    raise Undecided("escape step beyond infinity")
                Fhi = F(zh)
                if Fhi > y:
                    break
                hi = exact(2 * hi)
        Flo = Fz0
        v = exact((lo + hi) / 2)
        za = self._newton(F, y, lo, hi, Flo, None, to_z, dzdv, v)
        return self._certify(F, y, za)

    def _certify(self, F, y, za):
        D = F(za) - y
        f0 = self.fT(acb(za), False).real
        if not f0 > 0:
            raise Undecided("time derivative")
        delta = exact(4 * abs(D).upper() / f0.lower() + (abs(za) + 1) * arb(2) ** (-self.prec + 4))
        for _ in range(8):
            Z = arb(za, delta)
            fZ = self.fT(acb(Z), False).real
            if fZ.is_finite() and fZ > 0:
                N = za - D / fZ
                if Z.contains_interior(N):
                    return N
            delta = 8 * delta
        raise Undecided("interval Newton")

    # --- positions ----------------------------------------------------------------------

    def X_at(self, k, Z):
        """Ball position (X_x, X_y) at phase Z of period k."""
        A = self.A
        u = self._u_b(Z)
        th = self._theta_b(k, Z)
        f = 1 / (u * self.r0)
        if A.radial:
            X = (f * A.a if A.a else arb(0), f * A.b if A.b else arb(0))
        else:
            c, s = th.cos(), th.sin()
            X = (f * (A.a * c - A.b * s), f * (A.a * s + A.b * c))
        return X

    def tau_at(self, k, Z):
        return self._tau_b(k, Z) / self.Qb

    # --- range exit ---------------------------------------------------------------------

    def _pt_time(self, k, z):
        """Chronon ball of the exact phase point (k, z)."""
        return self.A.t0 + self._F(k, z) / self.Qb

    def _box_state(self, k, za, zb):
        """Enclosure of X over phases [za, zb] of period k, on which u and theta are monotone."""
        A = self.A
        ua, ub = self._u_b(za), self._u_b(zb)
        ta, tb = self._theta_b(k, za), self._theta_b(k, zb)
        U = ua.union(ub)
        TH = ta.union(tb)
        f = 1 / (U * self.r0)
        if A.radial:
            return (f * A.a if A.a else arb(0), f * A.b if A.b else arb(0))
        c, s = TH.cos(), TH.sin()
        return (f * (A.a * c - A.b * s), f * (A.a * s + A.b * c))

    def _exceeds_point(self, T):
        k, Z = self.solve(arb(self.A.Q * (T - self.A.t0)))
        X = self.X_at(k, Z)
        out = False
        for x in X:
            if x > LIM or x < -LIM:
                out = True
            elif not (x <= LIM and x >= -LIM):
                raise Undecided("range comparison")
        return out

    def _search_piece(self, k, za, zb, Tmax, depth=0):
        """First integer chronon in (t0, Tmax] within phases [za, zb] (period k) at which some
        coordinate exceeds the range, or None."""
        A = self.A
        ta = self._pt_time(k, za)
        tb = self._pt_time(k, zb)
        first = max(A.t0 + 1, int(ta.lower().ceil().unique_fmpz()))
        last = min(Tmax, int(tb.upper().floor().unique_fmpz()))
        if first > last:
            return None
        X = self._box_state(k, za, zb)
        inside = all((x <= LIM and x >= -LIM) for x in X)
        if inside:
            return None
        outside = any((x > LIM or x < -LIM) for x in X)
        if outside:
            # every point of the piece exceeds; the first integer is an exit if it lies in
            # the piece for certain, otherwise decide it pointwise.
            if ta < first and first <= tb:
                return first
        if last - first <= 3 or depth > 400:
            for T in range(first, last + 1):
                if self._exceeds_point(T):
                    return T
            return None
        zm = exact((za + zb) / 2)
        if zm == za or zm == zb:
            raise Undecided("exit search resolution")
        r = self._search_piece(k, za, zm, Tmax, depth + 1)
        if r is not None:
            return r
        return self._search_piece(k, zm, zb, Tmax, depth + 1)

    def _far_pieces(self):
        """Generator of (k, za, zb) in time order covering every future phase where r >= LIM
        may hold (u and theta monotone on each piece). Ends with a piece where the exit is
        certain for escaping orbits."""
        A = self.A
        uL = arb(1) / LIM
        up = lambda x: exact(x) + 2 * x.rad() + arb(2) ** (-self.prec + 20) * (abs(exact(x)) + 1)
        if self.chart == "circular":
            per = 2 * arb.pi() / self.omega
            step = exact(per / 8)
            k = 0
            z = arb(0)
            while True:
                yield (0, z, z + step)
                z = z + step
            return
        if A.radial and self.info["kind"] == "radial-bound":
            rmax = 1 / self.uz(arb(0))
            if not rmax > LIM:
                return
            es = 2 * ((LIM / rmax).sqrt()).acos()
            e_ = up(es)
            z0 = exact(self.z0)
            for a, b in ((-e_, arb(0)), (arb(0), e_)):
                a2 = a if a > z0 else z0
                if a2 < b:
                    yield (0, a2, b)
            return
        if self.escape and self.zinf is None:      # radial outward w chart
            z0 = exact(self.z0)
            wa = exact(arb(LIM).sqrt()) - 1
            wb = exact(arb(4 * LIM).sqrt()) + 1
            a = wa if wa > z0 else z0
            yield (0, a, wb)
            return
        if self.chart in ("three-root",) and self.region == "A":
            # unbound, chi in (chi_inf, 2pi - chi_inf)
            m, h = self.m, self.h
            z0 = exact(self.z0)
            al = self._phase_of_u(uL)            # r >= LIM for chi <= al (incoming side)        # r >= LIM for chi <= al (incoming side)
            zin = up(al)
            if z0 < zin:
                yield (0, z0, zin)
            twopi = 2 * arb.pi()
            za = exact(twopi - al) - arb(2) ** (-self.prec + 20)
            u97 = arb(1) / (4 * LIM)
            zb = exact(twopi - self._phase_of_u(u97))
            a = za if za > z0 else z0
            yield (0, a, zb)
            return
        # sigma charts
        ut = self.ut
        z0 = exact(self.z0)
        if not ut < uL:
            return
        sst = up((uL - ut).sqrt())
        if self.escape:
            u97 = arb(1) / (4 * LIM)
            zb = exact(-(u97 - ut).sqrt())
            a = -sst if -sst > z0 else z0
            if a < zb:
                yield (0, a, zb)
            return
        for a, b in ((-sst, arb(0)), (arb(0), sst)):
            a2 = a if a > z0 else z0
            if a2 < b:
                yield (0, a2, b)

    def first_exit(self, Tmax):
        """First integer chronon in (t0, Tmax] at which a coordinate exceeds +-2^96."""
        A = self.A
        if Tmax <= A.t0:
            return None
        rmax = self.r_future_max
        if rmax is not None and rmax <= LIM:
            return None
        if self.period:
            return self._first_exit_periodic(Tmax)
        for (k, za, zb) in self._far_pieces():
            za, zb = exact(za), exact(zb)
            if self.chart == "circular":
                if self._pt_time(0, za) > Tmax:
                    return None
            else:
                if self._pt_time(k, za) > Tmax:
                    return None
            r = self._search_piece(k, za, zb, Tmax)
            if r is not None:
                return r
        return None

    def _first_exit_periodic(self, Tmax):
        uL = arb(1) / LIM
        u1 = self.roots[0]
        if not u1 < uL:
            if u1 > uL:
                return None
            raise Undecided("apoapsis at the range")
        al = exact(self._phase_of_u(uL)) + arb(2) ** (-self.prec + 30)
        twopi = 2 * arb.pi()
        # periods are measured from phase 0 (apoapsis); the anchor sits at z0 in [0, 2pi).
        kk = 0
        while True:
            # excursion around apoapsis at phase 2pi*kk: [2pi kk - al, 2pi kk + al]
            # represent as (kk-1, [2pi - al, 2pi]) and (kk, [0, al]).
            pieces = []
            if kk >= 1:
                pieces.append((kk - 1, exact(twopi - al), exact(twopi)))
            pieces.append((kk, arb(0), al))
            for (k, za, zb) in pieces:
                if k == 0 and zb < self.z0:
                    continue
                if k == 0 and za < self.z0:
                    za = exact(self.z0)
                if self._pt_time(k, za) > Tmax:
                    return None
                r = self._search_piece(k, za, zb, Tmax)
                if r is not None:
                    return r
            kk += 1

    # --- the query ----------------------------------------------------------------------

    def query(self, T):
        ctx.prec = self.prec
        A = self.A
        if T < A.t0:
            return {"at": "Before"}
        if T == A.t0:
            return {"at": "Free", "x": [A.a, A.b], "tau": "0"}
        c_abs = None
        if self.horizon:
            c_abs = ceil_int(A.t0 + self.dTh / self.Qb, "absorption chronon")
        tmax = T if c_abs is None else min(T, c_abs - 1)
        c_exit = self.first_exit(tmax)
        if c_abs is not None and T >= c_abs and (c_exit is None or c_abs <= c_exit):
            return {"at": "Absorbed", "chronon": c_abs, "tau": self._tau_str(self.dHh / self.Qb)}
        if c_exit is not None and c_exit <= T:
            return {"at": "OutOfRange", "chronon": c_exit}
        y = arb(A.Q * (T - A.t0))
        k, Z = self.solve(y)
        X = self.X_at(k, Z)
        out = []
        for i, x in enumerate(X):
            if (A.a if i == 0 else A.b) == 0 and A.radial:
                out.append(0)
            else:
                if x > LIM or x < -LIM:
                    raise Undecided("exit missed")
                out.append(floor_int(x, "floor"))
        res = {"at": "Free", "x": out, "tau": self._tau_str(self.tau_at(k, Z))}
        res["dist"] = [self._dist(x) for x in X]
        return res

    def _tau_str(self, t):
        if self.A.null:
            return "0"
        return t.mid().str(30, radius=False)

    def _dist(self, x):
        """log2 of the distance from x to the nearest integer (diagnostic)."""
        if x.is_exact() and x == 0:
            return None
        v = x - x.mid().floor()
        dv = v if v < 1 - v else 1 - v
        dm = dv.mid()
        if not dm > 0:
            return -float(self.prec)
        return float(dm.log() / arb(2).log())

    # --- diagnostics --------------------------------------------------------------------

    def diagnostics(self):
        ctx.prec = self.prec
        A = self.A
        s = lambda v, d=40: v.mid().str(d, radius=False)
        out = {"chart": self.chart, "kind": self.info.get("kind"), "E": s(self.E),
               "L_quanta": s(self.sL * self.Lab) if not A.radial else "0"}
        M = self.Mb
        if self.chart in ("three-root", "one-root"):
            out["roots_u_times_M"] = [s(r * M) for r in self.roots]
        if self.period:
            u1, u2 = self.roots[0], self.roots[1]
            p = 2 / (M * (u1 + u2))
            e = (u2 - u1) / (u1 + u2)
            out["p_over_M"] = s(p, 80)
            out["e"] = s(e, 80)
            out["sep_margin"] = s((p - 6 - 2 * e) / p, 20)
            out["period_T_chronons"] = s(self.PT / self.Qb, 40)
            out["period_tau_chronons"] = s(self.PH / self.Qb, 40) if self.Hprim else None
            out["advance_rad"] = s(self.PG - 2 * arb.pi(), 40)
        if A.null and not A.radial:
            out["b_quanta"] = s(self.Lab / self.E, 80)
            out["b_over_M"] = s(self.Lab / (self.E * M), 80)
        if self.escape and self.chart == "three-root" and self.region == "A":
            # whole scattering orbit from infinity to infinity; periapsis 1/u2
            chi_inf = 2 * arb.pi() - self.zinf
            defl = self.Gprim.at_ball(self.zinf) - self.Gprim.at_ball(chi_inf) - arb.pi()
            out["deflection_rad"] = s(defl, 40)
            out["r_min_over_M"] = s(1 / (self.roots[1] * M), 40)
        if self.horizon:
            out["T_h"] = (A.t0 + self.dTh / self.Qb).mid().str(40, radius=False)
            out["tau_h"] = s(self.dHh / self.Qb, 30)
        if self.chart == "circular":
            out["clock_rate"] = s(self.tau_rate, 40)
            out["omega_per_chronon"] = s(self.omega * self.Qb, 40)
        out["static_clock_rate_r0"] = s((1 - 2 * M / self.r0).sqrt(), 40)
        return out


# ----------------------------------------------------------------------------------------
# Driver with the precision ladder


class Judge:
    def __init__(self, M, Q, t0, x, k, null, start=0):
        self.args = (M, Q, t0, x, k, null)
        self.start = start
        self.invalid = None
        try:
            self.A = Anchor(M, Q, t0, x, k, null)
        except Invalid as e:
            self.invalid = str(e)
        self.geos = {}

    def geo(self, i):
        if i not in self.geos:
            self.geos[i] = Geo(self.A, PRECS[i])
        ctx.prec = PRECS[i]
        return self.geos[i]

    def query(self, T):
        if self.invalid:
            return {"at": "Invalid", "why": self.invalid}
        last = None
        for i in range(self.start, len(PRECS)):
            try:
                g = self.geo(i)
                r = g.query(T)
                r["prec"] = PRECS[i]
                return r
            except Undecided as e:
                last = str(e)
            except Invalid as e:
                return {"at": "Invalid", "why": str(e)}
        return {"at": "UNSETTLED", "why": last}

    def diagnostics(self):
        if self.invalid:
            return {"invalid": self.invalid}
        for i in range(self.start, len(PRECS)):
            try:
                return self.geo(i).diagnostics()
            except Undecided as e:
                last = str(e)
            except Invalid as e:
                return {"invalid": str(e)}
        return {"unsettled": last}


def closed_form_infall_from_rest(M, Q, r0, prec=512):
    """Closed-form river time (chronons) from rest (dX/dT = 0) at r0 to the horizon.

    Cycloid r = r0 cos^2(eta/2); Schwarzschild t(eta) (MTW 31.10) plus the river correction
    f(r) = 2 sqrt(2Mr) + 2M ln((sqrt r - sqrt 2M)/(sqrt r + sqrt 2M)). The two logarithms
    diverge at the horizon; combined analytically their sum tends to 2M ln(1 - 2M/r0).
    Independent of the quadrature used by the judge."""
    ctx.prec = prec
    M, Q, r0 = arb(M), arb(Q), arb(r0)
    a = (r0 / (2 * M) - 1).sqrt()
    eh = 2 * a.atan()
    t_nl = 2 * M * a * (eh + r0 / (4 * M) * (eh + eh.sin()))
    s0, s2 = r0.sqrt(), (2 * M).sqrt()
    f0 = 2 * (2 * M * r0).sqrt() + 2 * M * ((s0 - s2) / (s0 + s2)).log()
    dT = t_nl + 2 * M * (1 - 2 * M / r0).log() + 4 * M - f0
    return dT / Q


def closed_form_flow_rest(M, Q, r0, prec=512):
    """River time (chronons) to the horizon for a body at rest in the flow (E = 1, radial):
    dr/dT = -sqrt(2M/r) gives (2 / (3 sqrt(2M))) (r0^(3/2) - (2M)^(3/2))."""
    ctx.prec = prec
    M, Q, r0 = arb(M), arb(Q), arb(r0)
    return 2 / (3 * (2 * M).sqrt()) * (r0 * r0.sqrt() - 2 * M * (2 * M).sqrt()) / Q


def _stringify(r):
    """Answers carry integers as decimal strings (they exceed 64 bits)."""
    if "x" in r:
        r["x"] = [str(v) for v in r["x"]]
    if "chronon" in r:
        r["chronon"] = str(r["chronon"])
    return r


def solve_case(case, start=0, diag=False):
    I = int
    j = Judge(I(case["M"]), I(case["Q"]), I(case["t0"]), [I(v) for v in case["x"]],
              [I(v) for v in case["k"]], case["motion"] == "null", start)
    out = []
    for T in case["T"]:
        r = _stringify(j.query(I(T)))
        r["T"] = str(T)
        out.append(r)
    res = {"id": case["id"], "answers": out}
    if diag:
        res["diag"] = j.diagnostics()
    return res


def _worker(args):
    lines, start, diag = args
    os.nice(10) if hasattr(os, "nice") else None
    res = []
    for line in lines:
        case = json.loads(line)
        t = time.time()
        r = solve_case(case, start, diag or case.get("diag", False))
        r["secs"] = round(time.time() - t, 3)
        res.append(json.dumps(r, separators=(",", ":")))
    return res


def r2_anchor_list():
    """R2 anchors: every valid timelike anchor with Q = 25, M = 1, t0 = 0, x in [-8, 8]^2,
    k in [-4, 4]^2, in lexicographic order of (x, y, kx, ky)."""
    out = []
    for a in range(-8, 9):
        for b in range(-8, 9):
            for kx in range(-4, 5):
                for ky in range(-4, 5):
                    try:
                        Geo(Anchor(1, 25, 0, (a, b), (kx, ky), False), 256)
                    except Invalid:
                        continue
                    out.append((a, b, kx, ky))
    return out


def _r2_worker(args):
    anchors, start = args
    if hasattr(os, "nice"):
        os.nice(10)
    res = []
    for (a, b, kx, ky) in anchors:
        j = Judge(1, 25, 0, (a, b), (kx, ky), False, start)
        ans = []
        for T in range(1, 9):
            r = j.query(T)
            if r["at"] == "Free":
                ans.append([int(r["x"][0]), int(r["x"][1])])
            elif r["at"] in ("Absorbed", "OutOfRange"):
                ans.append({"Absorbed": "A", "OutOfRange": "O"}[r["at"]] + str(r["chronon"]))
            else:
                ans.append(r["at"] + ":" + str(r.get("why")))
        res.append(json.dumps([a, b, kx, ky, ans], separators=(",", ":")))
    return res


def solve_r2(dst, start=0, workers=1):
    t = time.time()
    anchors = r2_anchor_list()
    print(f"R2 anchors {len(anchors)}, cases {8 * len(anchors)}", file=sys.stderr)
    chunks = [(anchors[i:i + 200], start) for i in range(0, len(anchors), 200)]
    with gzip.open(dst, "wt") as out:
        out.write(json.dumps({"rung": "R2", "M": 1, "Q": 25, "t0": 0, "T": list(range(1, 9)),
                              "format": "[x, y, kx, ky, [answer for T = 1..8]]; answer = [floor x, floor y] "
                                        "| 'A<chronon>' Absorbed | 'O<chronon>' OutOfRange",
                              "anchors": len(anchors), "start_prec": PRECS[start]}) + "\n")
        if workers > 1:
            import multiprocessing as mp
            with mp.Pool(workers) as pool:
                for res in pool.imap(_r2_worker, chunks):
                    for r in res:
                        out.write(r + "\n")
        else:
            for ch in chunks:
                for r in _r2_worker(ch):
                    out.write(r + "\n")
    print(f"R2 solved in {time.time() - t:.1f} s", file=sys.stderr)
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "one":
        M, Q, t0, x, y, kx, ky = map(int, argv[2:9])
        motion = argv[9]
        Ts = [int(v) for v in argv[10:]]
        case = {"id": "cli", "M": M, "Q": Q, "t0": t0, "x": [x, y], "k": [kx, ky],
                "motion": motion, "T": Ts}
        print(json.dumps(solve_case(case, 0, True), indent=1))
        return 0
    if len(argv) >= 3 and argv[1] == "r2":
        return solve_r2(argv[2], "--prec-index" in argv and int(argv[argv.index("--prec-index") + 1]) or 0,
                        int(argv[argv.index("--workers") + 1]) if "--workers" in argv else 1)
    if len(argv) >= 4 and argv[1] == "solve":
        src, dst = argv[2], argv[3]
        start = 0
        workers = 1
        if "--prec-index" in argv:
            start = int(argv[argv.index("--prec-index") + 1])
        if "--workers" in argv:
            workers = int(argv[argv.index("--workers") + 1])
        with gzip.open(src, "rt") as f:
            lines = [l for l in f if l.strip()]
        chunks = [(lines[i:i + 50], start, False) for i in range(0, len(lines), 50)]
        t = time.time()
        with gzip.open(dst, "wt") as out:
            if workers > 1:
                import multiprocessing as mp
                with mp.Pool(workers) as pool:
                    for res in pool.imap(_worker, chunks):
                        for r in res:
                            out.write(r + "\n")
            else:
                for ch in chunks:
                    for r in _worker(ch):
                        out.write(r + "\n")
        print(f"solved {len(lines)} cases in {time.time() - t:.1f} s", file=sys.stderr)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
