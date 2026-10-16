"""Probe 4 (final): light deflection at b=10,30 vs oracle; capture near b=3*sqrt(3).

- Deflection: exact turning-point IC (forced by the metric: u_r = sqrt(2/r_min),
  |u| = 1; coordinate motion exactly tangential, angle pi/2), integrated out to
  r_exit = 400/800, measured with COORDINATE-velocity directions (v = u + beta).
  Half bend = psi_v(exit) - pi/2; the exact remaining rotation to infinity
  (quadrature; ~b^3/(4 r_e^4), NOT the Born-style 2b/r_e^2 which overcounts ~200x)
  is added analytically for the full deflection.
- The mandated step dt = eta*r^{3/2} gives light a fractional arc dt/r = eta*sqrt(r)
  growing with radius (massive bodies: v*dt/r ~ eta, safe at all r); a far-exit row
  (r_exit = 1e5) documents that failure mode.
- Capture rays start at r0 = 1000 on the exact geodesic, from the invariant
  b = r sinA/(1 - sigma cosA) (closed form; valid for plunging rays too).
"""
import math, time
from gv1 import (s2_phot, s4_phot, ic_photon_turning, deflection_gr, deflection_ode,
                 gauss_legendre, null_turning_radius, SQ2, PI)

BSL = 3.0*math.sqrt(3.0)

def exact_tail(b, r_e):
    """Remaining rotation of psi_v between r_e and infinity along the exact geodesic:
    (phi_inf - phi_e) - theta_e, tan(theta_e) = u_e/sqrt(g(u_e)), g = 1/b^2 - u^2 + 2u^3."""
    nodes = gauss_legendre(48)
    u0 = 1.0/r_e
    total = 0.0
    for x, w in nodes:
        u = 0.5*u0*(1.0 + x)
        total += 0.5*u0*w/math.sqrt(1.0/(b*b) - u*u + 2.0*u*u*u)
    th = math.atan2(u0, math.sqrt(1.0/(b*b) - u0*u0 + 2.0*u0*u0*u0))
    return total - th

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

def b_of_state(x, y, px, py):
    r = math.sqrt(x*x + y*y)
    pn = math.sqrt(px*px + py*py)
    Eph = pn + SQ2*(x*px + y*py)/(r*math.sqrt(r))
    Lph = abs(x*py - y*px)
    return Lph/Eph

def psi_v_of(x, y, px, py):
    """Direction angle of the coordinate velocity v = u + beta."""
    pn = math.sqrt(px*px + py*py)
    r = math.sqrt(x*x + y*y)
    rs = math.sqrt(r)
    f_ = -SQ2/(r*rs)
    return math.atan2(-py/pn + f_*y, -px/pn + f_*x)

def deflect(b, eta, order, rexit=800.0, maxsteps=200000):
    x, y, px, py = ic_photon_turning(b)
    sqrt = math.sqrt
    for i in range(maxsteps):
        r = sqrt(x*x + y*y)
        dt = eta*r*sqrt(r)
        if order == 2:
            x, y, px, py, ab = s2_phot(x, y, px, py, dt)
        else:
            x, y, px, py, ab = s4_phot(x, y, px, py, dt)
        if ab:
            return None, i, True, float("nan")
        if x*x + y*y >= rexit*rexit:
            break
    return 2.0*(psi_v_of(x, y, px, py) - 0.5*PI) + exact_tail(b, rexit), i, False, \
        abs(b_of_state(x, y, px, py) - b)/b

def capture(b, eta, order, r0=1000.0, maxsteps=400000):
    x, y, px, py = ic_photon_r(b, r0)
    sqrt = math.sqrt
    for i in range(maxsteps):
        r = sqrt(x*x + y*y)
        dt = eta*r*sqrt(r)
        if order == 2:
            x, y, px, py, ab = s2_phot(x, y, px, py, dt)
        else:
            x, y, px, py, ab = s4_phot(x, y, px, py, dt)
        if ab:
            return "absorbed", i
        r = sqrt(x*x + y*y)
        if r > 500.0:
            pn = math.sqrt(px*px + py*py)
            ur = -(x*px + y*py)/(r*pn)
            if ur > 0.1:
                return "escaped", i
    return "timeout", maxsteps

if __name__ == "__main__":
    t0 = time.perf_counter()
    # construction check: inbound state at r0 must reproduce the exact turning radius
    for b in (10.0, 30.0, BSL*1.005):
        x, y, px, py = ic_photon_r(b, 1000.0)
        bchk = b_of_state(x, y, px, py)
        rmin = 1e9
        for _ in range(200000):
            r = math.sqrt(x*x+y*y)
            dt = (1/2048)*r*math.sqrt(r)
            x, y, px, py, ab = s2_phot(x, y, px, py, dt)
            if ab:
                break
            r = math.sqrt(x*x+y*y)
            if r < rmin:
                rmin = r
            if r > 1000.0 or r < 2.5:
                break
        rt = null_turning_radius(b) if b > BSL else float("nan")
        print(f"IC check b={b:.4f}: b_state={bchk:.6f}  r_min={rmin:.4f} "
              f"(exact turning {rt:.4f})" + ("" if b > BSL else "  [plunging]"))
    print("tail sizes:", {r: f"{exact_tail(30.0, r):.2e}" for r in (400.0, 800.0)})
    print("== probe 4a: deflection vs oracle (r_exit=800, exact tail) ==")
    print(f"{'b':>6} {'eta':>7} {'ord':>3} {'alpha_law':>12} {'alpha_GR':>12} "
          f"{'rel_err':>10} {'b_drift':>10}")
    for b in (10.0, 30.0):
        agr = deflection_gr(b)
        for eta in (1/64, 1/128, 1/256):
            for order in (2, 4):
                al, st, ab, bdr = deflect(b, eta, order)
                rel = abs(al - agr)/agr
                print(f"{b:6.1f} {eta:7.4f} {order:3d} {al:12.6f} {agr:12.6f} "
                      f"{rel:10.2e} {bdr:10.2e}")
    print("== mandated rule at large r (r_exit=1e5): documented failure ==")
    for order in (2, 4):
        al, st, ab, bdr = deflect(30.0, 1/128, order, rexit=1.0e5)
        print(f"b=30 eta=1/128 order={order}: alpha={al:.4f} (GR 0.1482) "
              f"b_drift={bdr:.1e}")
    print(f"== probe 4b: photon capture near b_c={BSL:.6f}, r0=1000 ==")
    print(f"{'b':>9} {'expect':>9} {'eta':>7} {'ord':>3} {'result':>9} {'steps':>7}")
    for d in (0.01, 0.005):
        for sgn in (-1, 1):
            b = BSL*(1.0 + sgn*d)
            expect = "absorbed" if b < BSL else "escaped"
            for eta in (1/64, 1/128):
                for order in (2, 4):
                    res, st = capture(b, eta, order)
                    ok = "OK" if res == expect else "WRONG"
                    print(f"{b:9.4f} {expect:>9} {eta:7.4f} {order:3d} {res:>9} "
                          f"{st:7d}  {ok}")
    print("== bisection of b* (r0=1000) ==")
    for (eta, order) in [(1/128, 2), (1/128, 4), (1/256, 2)]:
        lo, hi = BSL*0.995, BSL*1.005
        if capture(lo, eta, order)[0] != "absorbed" or capture(hi, eta, order)[0] != "escaped":
            print(f"eta={eta:.4f} order={order}: bracket failed")
            continue
        for _ in range(18):
            mid = 0.5*(lo + hi)
            if capture(mid, eta, order)[0] == "absorbed":
                lo = mid
            else:
                hi = mid
        bstar = 0.5*(lo + hi)
        print(f"eta={eta:.4f} order={order}: b* = {bstar:.6f}  "
              f"|b*-bc|/bc = {abs(bstar-BSL)/BSL:.2e}")
    print(f"wall: {time.perf_counter()-t0:.1f} s")
