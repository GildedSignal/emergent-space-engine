#!/usr/bin/env python3
"""Exact equatorial Kerr null geodesics (float oracle) + the EXACT static-
observer sky map. Second-author instrument for 20261020-2102-redteam-1645.

The author's edge map a = asin(b*sqrt(1-2M/r_o)/r_o) is Schwarzschild's
static formula with Kerr b_c substituted. The exact static observer in Kerr
equatorial BL has g_tphi != 0, so the phi-leg of their tetrad tilts:

  e0 = d/dt / sqrt(1-2M/r),  e3 = (d/dphi - (g_tphi/g_tt) d/dt)/sqrt(G),
  G = g_phph - g_tphi^2/g_tt   (g_tt<0),  sin a = (p.e3)/(-p.e0)
    = (b + 2aM/(r_o(1-2M/r_o))) * sqrt(1-2M/r_o)/sqrt(G)      [b-form]
    = sqrt(G)*Q/r_o^2 * sqrt(1-2M/r_o),  Q=(b-a)+aP/Delta      [Q-form]
    |sin a|^2 = 1 - R(r_o)(1-2M/r_o)/(r_o^2 Delta)            [null identity]

All three routes are checked against each other. The sky is then decided
WITHOUT the map by an exact fate classifier: R(r) = r*(r^3 + c2 r + c1)
factors (c0 = 0 identically), the exterior roots of the cubic are taken in
closed form (Cardano), and a photon at r_o lives in the allowed interval
between consecutive roots: bottom interval (horizon, r_1) => PLUNGE, top
interval (r_n, inf) => ESCAPE, no exterior roots => depends on launch
hemisphere. The classifier bisects the true shadow edges and censuses the
dark fraction of the sky circle — it, not any convention, decides the arc.

Geodesic machinery (Carter first-order system, GL quadrature in r = r_min+u^2)
is carried over verbatim from the author's kerr_shadow.py so the controls,
the oracle battery, the shipped-law comparison and the rim wall regenerate.
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
    """Flyby turning point (author's numeric scan; cross-checks Cardano)."""
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
            x0, x1, f1 = prev_r, r, R
            for _ in range(200):
                xm = 0.5 * (x0 + x1)
                fm = rad(xm, a, b)
                if fm < 0.0:
                    x1 = xm
                else:
                    x0 = xm
            return x0 * (1 + 1e-15)
        prev_r, prev_R = r, R
    return None


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


# ---------------------------------------------------------------- tetrad ---
def gtt(r):
    return -(1 - 2 * M / r)


def gtph(r, a):
    return -2 * a * M / r


def gpp(r, a):
    return r * r + a * a + 2 * M * a * a / r


def Gstat(r, a):
    return gpp(r, a) - gtph(r, a) ** 2 / gtt(r)


def sin_a_b(b, r_o, a):
    """b-form: sin(alpha) for the photon with impact parameter b at r_o."""
    return (b + 2 * a * M / (r_o * (1 - 2 * M / r_o))) * math.sqrt(1 - 2 * M / r_o) \
        / math.sqrt(Gstat(r_o, a))


def sin_a_Q(b, r_o, a):
    """Q-form."""
    return math.sqrt(Gstat(r_o, a)) * qfun(r_o, a, b) / (r_o * r_o) * math.sqrt(1 - 2 * M / r_o)


def sin_a_id(b, r_o, a):
    """Radial null identity p0^2 = p_r^2 + p_3^2 (magnitude; sign from b-form)."""
    s2 = 1.0 - rad(r_o, a, b) * (1 - 2 * M / r_o) / (r_o * r_o * delta(r_o, a))
    return math.copysign(math.sqrt(max(s2, 0.0)), sin_a_b(b, r_o, a))


def alpha_deg(b, r_o, a):
    """Edge angle in degrees, or None if |sin|>1 (cannot happen for R(r_o)>=0)."""
    s = sin_a_b(b, r_o, a)
    if abs(s) > 1.0:
        return None
    return math.degrees(math.asin(s))


def author_alpha_deg(b, r_o, a):
    """The author's (Schwarzschild static) map, for the bias column."""
    x = b * math.sqrt(1 - 2 * M / r_o) / r_o
    if abs(x) > 1.0:
        return None
    return math.degrees(math.asin(x))


def chi_blind_deg(r_o):
    """The chi=0 law (what a chi-blind gather places), same at a=0 either way."""
    return math.degrees(math.asin(math.sqrt(27) * M * math.sqrt(1 - 2 * M / r_o) / r_o))


# ------------------------------------------------------- fate classifier ---
def horizon(a):
    return M + math.sqrt(max(M * M - a * a, 0.0))


def exterior_roots(a, b):
    """Real roots of R in (r_+, inf), ascending. R = r*(r^3 + c2 r + c1):
    the cubic is solved exactly (Cardano/trig)."""
    c2 = 2 * a * a - 2 * a * b - (b - a) ** 2
    c1 = 2 * (b - a) ** 2
    p, q = c2, c1
    disc = (q / 2) ** 2 + (p / 3) ** 3
    if disc > 0.0:
        s = math.sqrt(disc)
        u = math.copysign(abs(-q / 2 + s) ** (1 / 3), -q / 2 + s)
        v = math.copysign(abs(-q / 2 - s) ** (1 / 3), -q / 2 - s)
        roots = [u + v]
    else:
        m = 2 * math.sqrt(-p / 3)
        t = math.acos(max(-1.0, min(1.0, 3 * q / (p * m))))
        roots = [m * math.cos((t + 2 * math.pi * k) / 3) for k in range(3)]
    rh = horizon(a) * (1 + 1e-12)
    out = sorted(r for r in roots if r > rh)
    # numeric hygiene: merge near-duplicates (double roots at exactly b_c)
    merged = []
    for r in out:
        if not merged or r > merged[-1] * (1 + 1e-12):
            merged.append(r)
    return merged


def fate(a, b, r_o, outward):
    """Exact fate of the photon at r_o with this b: PLUNGE / ESCAPE / NONE.
    The allowed interval of r_o decides: bottom interval -> PLUNGE, top ->
    ESCAPE, no exterior roots -> hemisphere decides (walks bounce in place)."""
    if rad(r_o, a, b) < 0.0:
        return "NONE"
    roots = exterior_roots(a, b)
    if not roots:
        return "PLUNGE" if not outward else "ESCAPE"
    idx = sum(1 for r in roots if r < r_o)
    if idx == 0:
        return "PLUNGE"
    if idx == len(roots):
        return "ESCAPE"
    return "TRAPPED"  # pocket between two forbidden bands: not expected


def psi_to_b(psi, r_o, a):
    """Impact parameter of the photon launched at bearing psi (static frame)."""
    return math.sin(psi) * math.sqrt(Gstat(r_o, a) / (1 - 2 * M / r_o)) \
        - 2 * a * M / (r_o * (1 - 2 * M / r_o))


def dark(a, r_o, psi):
    return fate(a, psi_to_b(psi, r_o, a), r_o, math.cos(psi) > 0) == "PLUNGE"


def census(a, r_o, n=3600):
    """Dark fraction of the sky circle, by the fate classifier alone."""
    k = sum(1 for i in range(n)
            if dark(a, r_o, -math.pi + (i + 0.5) * 2 * math.pi / n))
    return k / n


def bisect_edge(a, r_o, psi0, halfwin=math.radians(6)):
    """Bisect the dark/lit flip nearest bearing psi0; return flip in radians."""
    n = 480
    prev = None
    flips = []
    for i in range(n + 1):
        psi = psi0 - halfwin + 2 * halfwin * i / n
        d = dark(a, r_o, psi)
        if prev is not None and d != prev:
            lo, hi = psi - 2 * halfwin / n, psi
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if dark(a, r_o, mid) == d:
                    hi = mid
                else:
                    lo = mid
            flips.append(0.5 * (lo + hi))
        prev = d
    if not flips:
        return None
    return min(flips, key=lambda f: abs(f - psi0))


# ------------------------------------------------------------------ main ---
def validation_block():
    print("== instrument validation ==")
    grid = [(a, r_o) for a in [0.3, 0.5, 0.9, 0.998, 0.9999] for r_o in [20.0, 10.0, 6.0, 3.2]]
    dq = di = 0.0
    for a, r_o in grid:
        rp, rm = photon_circular(a)
        bpc, bmc = (math.sqrt(27) * M, -math.sqrt(27) * M) if a == 0 else (bcrit(rp, a), bcrit(rm, a))
        for b in [bpc, bmc, 0.7 * bpc, 1.1 * bmc, 0.0]:
            s1, s2, s3 = sin_a_b(b, r_o, a), sin_a_Q(b, r_o, a), sin_a_id(b, r_o, a)
            dq = max(dq, abs(s1 - s2))
            di = max(di, abs(s1 - s3))
    print(f"formula triple agreement over grid: max|b-form - Q-form| = {dq:.2e}, "
          f"max|b-form - identity| = {di:.2e}  (P1a: <= 1e-13)")
    # a=0 reduces to the author's map
    dm = max(abs(sin_a_b(b, r_o, 0.0) - b * math.sqrt(1 - 2 * M / r_o) / r_o)
             for r_o in [20.0, 10.0, 6.0, 3.2] for b in [-6.0, -5.196, -1.0, 2.0, 4.0, 4.56])
    print(f"a=0: max |exact map - author map| = {dm:.2e}  (P1b: <= 1e-15)")
    # tangential launches: sin(a)=+-1 exactly at the R(r_o)=0 roots
    worst = 0.0
    for a, r_o in grid:
        for sgn in (1.0, -1.0):
            # b with sin(psi)=sgn*1: psi_to_b at psi = +-pi/2
            b_t = psi_to_b(sgn * math.pi / 2, r_o, a)
            worst = max(worst, abs(rad(r_o, a, b_t)) / max(1.0, abs(b_t)))
    print(f"tangential consistency: max |R(r_o)|/|b| at sin(psi)=+-1 = {worst:.2e}  (P1c: ~0)")
    # Cardano roots vs the author's numeric scan, and fate vs turning/bend
    for (a, b) in [(0.5, -6.2), (0.9, -6.9), (0.998, 3.5), (0.3, 4.7), (0.0, 5.5)]:
        cr = exterior_roots(a, b)
        nr = turning(a, b, 200.0)
        ok = "n/a" if nr is None else f"{abs(nr - max(cr)):.2e}" if cr else "MISSING"
        esc = fate(a, b, 20.0, False) if rad(20.0, a, b) >= 0 else "NONE"
        via_bend = "ESCAPE" if bend(a, b, rmax=200.0) is not None else "PLUNGE"
        print(f"roots a={a} b={b:+.2f}: cardano {[f'{r:.6f}' for r in cr]} vs scan {ok} | "
              f"fate(inward@20)={esc} vs bend-to-200 {via_bend}")
    # fate-classifier: no pocket (TRAPPED) anywhere on the probed skies
    print("census trap check: any TRAPPED on probed skies = "
          f"{any(fate(0.5, psi_to_b(psi, 3.2, 0.5), 3.2, True) == 'TRAPPED' for psi in [-1.2, -0.9, 0.0, 1.9])}")
def a0_controls():
    print("\n== controls (a=0; original battery, unchanged) ==")
    for b in [100.0, 50.0, 20.0]:
        got = bend(0.0, b)
        want = 4 / b + 15 * math.pi / 4 / b ** 2
        print(f"bend a=0 b={b:7.1f}: {got:.9f} vs 4/b+15pi/4b^2 {want:.9f} rel={(got/want-1):+.2e}")
    bpc0, bmc0 = math.sqrt(27) * M, -math.sqrt(27) * M
    print(f"a=0 b_c=+-{abs(bpc0):.6f} (=3sqrt3 {math.sqrt(27):.6f})")
    for r_o in [20.0, 6.0, 3.2]:
        ap = alpha_deg(bpc0, r_o, 0.0)
        frac = census(0.0, r_o)
        print(f"a=0 r_o={r_o}: edges +-{ap:.4f} census {100*frac:.2f}% "
              f"(039d: 7.9/25.0/46.6 at 20/6/3.2M)")
    for a in [0.0, 0.9]:
        rp, rm = photon_circular(a)
        for r, sgn, name in [(rp, 1, "pro"), (rm, -1, "retro")]:
            b = sgn * abs(bcrit(r, a))
            eps = 1e-6
            b_out = b * (1 + eps) if sgn > 0 else -abs(b) * (1 + eps)
            w = bend(a, b_out)
            print(f"spiral a={a} {name}: r_ph={r:.4f} b_c={b:+.5f} bend at b_c*(1+1e-6) = "
                  f"{('%.2f rad (%.1f turns)' % (w, w/(2*math.pi))) if w else 'CAPTURED'}")
    # inside-photon-sphere controls (P3): exactly half the sky at r=3M, more below
    for r_o in [3.0, 2.9]:
        frac = census(0.0, r_o, n=7200)
        sc = math.degrees(math.asin(min(1.0, math.sqrt(27) * math.sqrt(1 - 2 / r_o) / r_o)))
        print(f"a=0 INSIDE r_o={r_o}: census {100*frac:.2f}% "
              f"(predicted 50.00 at 3.0, ~51.9 at 2.9; lit cone half-angle {sc:.2f} deg)")


def corrected_table():
    print("\n== THE CORRECTED TABLE (exact static tetrad; edges deg; census = dark fraction by fate) ==")
    rows = [(a, r_o) for a in [0.5, 0.9, 0.998] for r_o in [20.0, 10.0, 6.0, 3.2]]
    rows += [(a, r_o) for a in [0.3, 0.9999] for r_o in [20.0, 10.0, 6.0, 3.2]]
    rows += [(0.1, 3.2)]
    print("chi    r_o   b_c+     b_c-    | exact edges [a-,a+] | chi-blind | err pro/retro |"
          " centre | arc(a+-a-) census | cap")
    for a, r_o in rows:
        rp, rm = photon_circular(a)
        bpc, bmc = (math.sqrt(27) * M, -math.sqrt(27) * M) if a == 0 else (bcrit(rp, a), bcrit(rm, a))
        ap_, am_ = alpha_deg(bpc, r_o, a), alpha_deg(bmc, r_o, a)
        aS = chi_blind_deg(r_o)
        epro, eret = ap_ - aS, am_ + aS
        centre = 0.5 * (ap_ + am_)
        arc = (ap_ - am_) / 360.0
        cen = census(a, r_o)
        cap = "CAP" if r_o < rm else ""
        print(f"{a:6.4f} {r_o:5.1f} {bpc:+7.3f} {bmc:+7.3f} | [{am_:+7.2f},{ap_:+7.2f}] |"
              f"   +-{aS:5.2f}   | {epro:+6.2f}/{eret:+6.2f} | {centre:+6.2f} |"
              f"   {100*arc:5.1f}%   {100*cen:5.1f}%  {cap}")
    print("author-map bias (author - exact, deg), for the checker's quoted ranges:")
    for a in [0.5, 0.9, 0.998]:
        for r_o in [20.0, 6.0, 3.2]:
            rp, rm = photon_circular(a)
            bpc, bmc = bcrit(rp, a), bcrit(rm, a)
            wrapped_p = author_alpha_deg(bpc, r_o, a) is None
            wrapped_m = author_alpha_deg(bmc, r_o, a) is None
            aa_p = 90.0 if wrapped_p else author_alpha_deg(bpc, r_o, a)
            aa_m = -90.0 if wrapped_m else author_alpha_deg(bmc, r_o, a)
            star = "*" if (wrapped_p or wrapped_m) else " "
            print(f"  chi={a} r_o={r_o}: bias pro {aa_p - alpha_deg(bpc, r_o, a):+6.2f}, "
                  f"retro {aa_m - alpha_deg(bmc, r_o, a):+6.2f} {star}"
                  + ("(wrap forced to +-90)" if star != " " else ""))

def edge_bisection_block():
    print("\n== fate-bisected sky edges vs the tetrad formula (P1d) ==")
    print("(the physical flip nearest a formula edge sits at bearing psi or its mirror 180-psi;")
    print(" both share sin(psi); the flip is bisected from the fate classifier alone)")
    worst = 0.0
    for a in [0.5, 0.9, 0.998, 0.3, 0.9999]:
        for r_o in [20.0, 6.0, 3.2]:
            rp, rm = photon_circular(a)
            bpc, bmc = (math.sqrt(27) * M, -math.sqrt(27) * M) if a == 0 else (bcrit(rp, a), bcrit(rm, a))
            for b, name in [(bpc, "pro"), (bmc, "retro")]:
                af = math.radians(alpha_deg(b, r_o, a))
                cands = [af, math.pi - af]
                best = None
                for cand in cands:
                    flip = bisect_edge(a, r_o, cand)
                    if flip is not None:
                        d = abs(math.sin(flip) - math.sin(af))
                        if best is None or d < best[0]:
                            best = (d, flip)
                if best is None:
                    print(f"  a={a} r_o={r_o} {name}: NO FLIP near either bearing of {math.degrees(af):+.2f} deg")
                    continue
                worst = max(worst, best[0])
                print(f"  a={a} r_o={r_o} {name}: formula edge {math.degrees(af):+7.3f} deg, "
                      f"flip at bearing {math.degrees(best[1]):+8.3f} deg, "
                      f"|sin(flip)-sin(formula)| = {best[0]:.2e}")
    print(f"max |sin(flip) - sin(formula edge)| = {worst:.2e}  (P1d: <= 5e-3)")


def tangentiality_block():
    print("\n== tangentiality (P6): |sin alpha| = 1 exactly at r_o = r_ph, never past ==")
    print("(static observers exist only at r_o > 2M: the scan domain)")
    for a in [0.3, 0.5, 0.9, 0.998, 0.9999]:
        rp, rm = photon_circular(a)
        for r_ph, b_c, name in [(rm, bcrit(rm, a), "retro"), (rp, bcrit(rp, a), "pro")]:
            lo = max(2.0 * (1 + 1e-4), horizon(a) * (1 + 1e-3))
            best_s, best_r = 0.0, None
            for i in range(20000):
                r_o = lo * (20.0 / lo) ** (i / 19999)
                s = abs(sin_a_b(b_c, r_o, a))
                if s > best_s:
                    best_s, best_r = s, r_o
            if r_ph <= lo:
                print(f"chi={a:6.4f} {name}: r_ph={r_ph:.6f} INSIDE the static domain's floor "
                      f"({lo:.4f}); max|sin| over the domain = {best_s:.9f} at its edge "
                      f"r_o={best_r:.4f} (no static observer can sit at the tangential point)")
            else:
                at = abs(sin_a_b(b_c, r_ph, a))
                print(f"chi={a:6.4f} {name}: r_ph={r_ph:.6f}  max|sin| over r_o scan = {best_s:.12f} "
                      f"at r_o={best_r:.6f} (|argmax-r_ph|={abs(best_r-r_ph):.2e}); "
                      f"|sin| at exactly r_ph = {at:.15f}")



def weak_chi_block():
    print("\n== weak-chi floor (P5): max |edge error| vs chi-blind, deg ==")
    print("chi      20M        6M")
    pts = {20.0: [], 6.0: []}
    for a in [0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]:
        row = []
        for r_o in [20.0, 6.0]:
            rp, rm = photon_circular(a)
            bpc, bmc = bcrit(rp, a), bcrit(rm, a)
            aS = chi_blind_deg(r_o)
            mx = max(abs(alpha_deg(bpc, r_o, a) - aS), abs(alpha_deg(bmc, r_o, a) + aS))
            pts[r_o].append((a, mx))
            row.append(f"{mx:8.3f}")
        print(f"{a:5.2f} {row[0]} {row[1]}")
    for r_o in [20.0, 6.0]:
        for bar in [1.0, 2.5]:
            xs = None
            for (a1, m1), (a2, m2) in zip(pts[r_o], pts[r_o][1:]):
                if m1 < bar <= m2:
                    xs = a1 + (a2 - a1) * (bar - m1) / (m2 - m1)
                    break
            print(f"r_o={r_o}: max error crosses {bar} deg at chi ~ {xs if xs else '>0.5' if bar==2.5 else 'in range'}")


def unchanged_blocks():
    print("\n== bend(b) per sense vs chi-blind Schwarzschild (star-bearing error; unchanged) ==")
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

    print("\n== rim wall: log divergence per sense (unchanged) ==")
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
        rp, rm = photon_circular(a)
        bcs = "+-" + f"{math.sqrt(27):.5f}" if a == 0 else f"+{bcrit(rp,a):.5f}/{bcrit(rm,a):.5f}"
        print(f"ORACLE a={a} bcrit {bcs}")


def r15_reference():
    print("\n== r15 reference values (freeze-ready, exact static tetrad + fate census) ==")
    for a in [0.5, 0.9, 0.998]:
        rp, rm = photon_circular(a)
        bpc, bmc = bcrit(rp, a), bcrit(rm, a)
        parts = [f"chi={a}: b_c {bpc:+.4f}/{bmc:+.4f}, r_ph {rp:.4f}/{rm:.4f}"]
        for r_o in [20.0, 6.0, 3.2]:
            ap_, am_ = alpha_deg(bpc, r_o, a), alpha_deg(bmc, r_o, a)
            parts.append(f"r_o={r_o}: edges [{am_:+.3f},{ap_:+.3f}] census {100*census(a, r_o):.2f}%")
        print("; ".join(parts))
    print("chi-blind arcs: " + "; ".join(f"r_o={r_o}: {2*chi_blind_deg(r_o)/3.6:.2f}%"
                                         for r_o in [20.0, 6.0, 3.2]))
    print("controls: chi=0 census " + "; ".join(f"r_o={r_o}: {100*census(0.0, r_o):.2f}%"
                                                for r_o in [20.0, 6.0, 3.2]) + " (039d: 7.9/25.0/46.6)")


if __name__ == "__main__":
    validation_block()
    a0_controls()
    corrected_table()
    edge_bisection_block()
    tangentiality_block()
    weak_chi_block()
    unchanged_blocks()
    oracle_vs_shipped()
    r15_reference()
