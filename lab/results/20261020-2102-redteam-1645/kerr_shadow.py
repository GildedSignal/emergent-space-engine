#!/usr/bin/env python3
"""Exact equatorial Kerr null geodesics (float oracle) for the view premise.

Instrument: Carter's first-order system, E=1, L=b signed (b>0 co-rotating).
  P(r) = E(r^2+a^2) - aL ;  R(r) = P^2 - Delta (L-aE)^2 ;  dphi/dr = Q/sqrt(R)
  with Q = (L-aE) + a P/Delta ;  Delta = r^2-2Mr+a^2 , M=1.
Flyby bend at infinity: Delta_phi = 2*int_{r_min}^{r_max} Q/sqrt(R) dr - pi,
turning point smoothed by r = r_min + u^2 (exact quadrature endpoint, Gauss-
Legendre in u; R(r_min)=0 cancels). Capture iff R<0 outside the horizon r+.
Shadow edges (static observer at r_o): alpha = asin(b*sqrt(1-2/r_o)/r_o),
b = b_c of each sense (Bardeen photon circular orbit), validated by spirals.
Controls: a=0 bend = 4/b + (15pi/4)/b^2; symmetric edges; spiral at b_c.
"""
import math

M = 1.0
GL4 = [(-0.8611363115940526, 0.34785484513745385), (-0.3399810435848563, 0.6521451548625461),
       (0.3399810435848563, 0.6521451548625461), (0.8611363115940526, 0.34785484513745385)]


def delta(r, a):
    return r * r - 2 * M * r + a * a


def pot(r, a, b):  # P
    return r * r + a * a - a * b


def rad(r, a, b):  # R
    p = pot(r, a, b)
    return p * p - delta(r, a) * (b - a) ** 2


def qfun(r, a, b):  # r^2 dphi/dlambda
    return (b - a) + a * pot(r, a, b) / delta(r, a)


def turning(a, b, rmax):
    """Flyby turning point: barrier's outer edge (largest r<rmax where R crosses
    + -> - scanning inward from rmax). None if allowed region reaches the
    horizon (plunge/capture). Returned root is biased to the R>=0 side."""
    lo = M + math.sqrt(max(M * M - a * a, 0.0))
    lo = lo * (1 + 1e-12) + 1e-9
    n = 32768
    lhi = min(rmax, 200.0)
    llo, lhi = math.log(lo), math.log(lhi)
    prev_r, prev_R = rmax, rad(rmax, a, b)
    for i in range(n - 1, -1, -1):
        r = math.exp(llo + (lhi - llo) * i / n)
        R = rad(r, a, b)
        if R < 0.0 <= prev_R:
            x0, x1, f1 = prev_r, r, R  # f(x0)>=0, f(x1)<0
            for _ in range(200):
                xm = 0.5 * (x0 + x1)
                fm = rad(xm, a, b)
                if fm < 0.0:
                    x1 = xm
                else:
                    x0 = xm
            return x0 * (1 + 1e-15)  # R>=0 side
        prev_r, prev_R = r, R
    return None  # no barrier: the ray plunges

def bend(a, b, rmax=200000.0, panels=40000):
    """Flyby bend at infinity (rad), or None if captured."""
    rmin = turning(a, b, rmax)
    if rmin is None:
        return None
    umax = math.sqrt(rmax - rmin)
    total = 0.0
    h = umax / panels
    for i in range(panels):
        u0 = i * h
        for x, w in GL4:
            u = u0 + (x + 1) * 0.5 * h
            r = rmin + u * u
            Rv = rad(r, a, b)
            if Rv > 0.0:
                total += w * qfun(r, a, b) / math.sqrt(Rv) * 2 * u
    return abs(2 * total * 0.5 * h) - math.pi


def photon_circular(a):
    rp = 2 * M * (1 + math.cos(2 / 3 * math.acos(-a)))
    rm = 2 * M * (1 + math.cos(2 / 3 * math.acos(+a)))
    return rp, rm


def bcrit(r, a):
    num = r ** 3 - 3 * M * r * r + a * a * r + a * a * M
    if a == 0:
        return math.sqrt(27) * M * (1 if r <= 3 * M + 1e-12 else -1)
    return -num / (a * (r - M))


def shadow(a, r_o):
    rp, rm = photon_circular(a)
    bpc, bmc = bcrit(rp, a), bcrit(rm, a)  # bpc>0 prograde, bmc<0
    if a == 0:
        bpc, bmc = math.sqrt(27) * M, -math.sqrt(27) * M
    f = math.sqrt(max(1 - 2 * M / r_o, 1e-300))
    scale = f / r_o

    def alpha(b):
        x = b * scale
        if x > 1: return None   # edge wraps past tangential: whole that side shadowed
        if x < -1: return None
        return math.asin(x)

    return bpc, bmc, alpha(bpc), alpha(bmc), rp, rm


def spiral_check(a, b, turns):
    """Bisection on winding: does the ray at this b wind > turns before escaping?"""
    return bend(a, b) is not None and bend(a, b) > 2 * math.pi * turns


def main():
    print("== controls (a=0) ==")
    for b in [100.0, 50.0, 20.0]:
        got = bend(0.0, b)
        want = 4 / b + 15 * math.pi / 4 / b ** 2
        print(f"bend a=0 b={b:7.1f}: {got:.9f} vs 4/b+15pi/4b^2 {want:.9f} rel={(got/want-1):+.2e}")
    bpc0, bmc0, ap0, am0, _, _ = shadow(0.0, 20.0)
    print(f"a=0 b_c=+-{abs(bpc0):.6f} (=3sqrt3 {math.sqrt(27):.6f})")
    for r_o in [20.0, 6.0, 3.2]:
        _, _, ap, am, _, _ = shadow(0.0, r_o)
        frac = (ap - am) / (2 * math.pi)
        print(f"a=0 r_o={r_o}: edges +-{ap:.4f} arc {100*frac:.1f}% (039d: 7.9/25.0/37.1... at 20/6/3.2M)")
    # spiral validation of bcrit
    for a in [0.0, 0.9]:
        rp, rm = photon_circular(a)
        for r, sgn, name in [(rp, 1, "pro"), (rm, -1, "retro")]:
            b = sgn * abs(bcrit(r, a))
            eps = 1e-6
            b_out = b * (1 + eps) if sgn > 0 else -abs(b) * (1 + eps)
            w = bend(a, b_out)
            print(f"spiral a={a} {name}: r_ph={r:.4f} b_c={b:+.5f} bend at b_c*(1+1e-6) = "
                  f"{('%.2f rad (%.1f turns)' % (w, w/(2*math.pi))) if w else 'CAPTURED'}")

    print("\n== shadow edges (static observer) vs the chi-blind law ==")
    for a in [0.5, 0.9, 0.998]:
        for r_o in [20.0, 6.0, 3.2]:
            bpc, bmc, ap, am, rp, rm = shadow(a, r_o)
            f = math.sqrt(1 - 2 / r_o)
            aS = math.asin(min(1.0, math.sqrt(27) * f / r_o))
            # exact edges (None = wrapped past tangential)
            ap_e = ap if ap is not None else math.pi / 2
            am_e = am if am is not None else -math.pi / 2
            frac = (ap_e - am_e) / (2 * math.pi)
            fracS = 2 * aS / (2 * math.pi)
            disp = (ap_e + am_e) / 2
            print(f"a={a} r_o={r_o}: b_c {bpc:+.3f}/{bmc:+.3f} r_ph {rp:.3f}/{rm:.3f} | "
                  f"edges [{am_e:+.4f},{ap_e:+.4f}] vs chi-blind [+-{aS:.4f}] | "
                  f"arc {100*frac:.1f}% vs {100*fracS:.1f}% | centre {disp:+.4f} rad ({math.degrees(disp):+.1f} deg)"
                  + ("  RETRO-EDGE WRAPS" if am is None or ap is None else ""))
            if am is not None:
                print(f"    edge error chi-blind: prograde {math.degrees(ap - aS):+.2f} deg, "
                      f"retrograde {math.degrees(am + aS):+.2f} deg")

    print("\n== bend(b) per sense vs chi-blind Schwarzschild (star-bearing error) ==")
    for a in [0.9, 0.998]:
        for b in [6.0, 10.0, 20.0]:
            kp, km, k0 = bend(a, b), bend(a, -b), bend(0.0, b)
            if kp is None or km is None:
                print(f"a={a} b={b:5.1f}: pro {'CAP' if kp is None else f'{kp:.6f}'} "
                      f"ret {'CAP' if km is None else f'{km:.6f}'} (captured side skipped)")
                continue
            print(f"a={a} b={b:5.1f}: pro {kp:.6f} ret {km:.6f} schw {k0:.6f} | "
                  f"err pro {math.degrees(kp - k0):+.3f} deg ret {math.degrees(km - k0):+.3f} deg "
                  f"asym {math.degrees(kp - km):+.3f} deg")

    print("\n== rim wall: log divergence per sense ==")
    for a in [0.0, 0.9]:
        rp, rm = photon_circular(a)
        for r, sgn, name in [(rp, 1, "pro"), (rm, -1, "retro")]:
            bc = abs(bcrit(r, a))
            vals = []
            for eps in [1e-3, 1e-4, 1e-5, 1e-6]:
                b = sgn * bc * (1 + eps)
                w = bend(a, b)
                vals.append((eps, w))
            if any(v[1] is None for v in vals):
                print(f"a={a} {name}: near-critical bend unresolved (grid)")
                continue
            A = (abs(vals[0][1]) - abs(vals[-1][1])) / math.log(vals[-1][0] / vals[0][0])
            gap = math.exp(-2 * math.pi / abs(A))
            print(f"a={a} {name}: A={abs(A):.3f} bend(1e-3)={abs(vals[0][1]):.2f} bend(1e-6)={abs(vals[-1][1]):.2f} "
                  f"| winding-image gap db/b = {gap:.2e} (memo key must resolve this)")


def oracle_vs_shipped():
    print("\n== oracle bends at the shipped sweep points (vs DEFL lines from cargo) ==")
    cases = [(0.0, [3.0, 3.2, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 8.0, 10.0, 20.0, 100.0]),
             (0.5, [4.5, 5.0, 6.5, 8.0, 10.0, 20.0, 100.0]),
             (0.9, [3.0, 3.2, 3.5, 4.0, 8.0, 10.0, 20.0, 100.0]),
             (0.998, [3.0, 3.2, 8.0, 10.0, 20.0, 100.0])]
    for a, bs in cases:
        for b in bs:
            for sgn in [1.0, -1.0]:
                w = bend(a, sgn * b)
                lab = f"{w:.9f}" if w is not None else "CAPTURED"
                print(f"ORACLE a={a} b={sgn*b:+.4f} phi={lab}")
        print(f"ORACLE a={a} bcrit {shadow_bc(a)}")


def shadow_bc(a):
    rp, rm = photon_circular(a)
    if a == 0:
        return f"+-{math.sqrt(27):.5f}"
    return f"+{bcrit(rp,a):.5f}/{bcrit(rm,a):.5f}"


if __name__ == "__main__":
    main()
    oracle_vs_shipped()
