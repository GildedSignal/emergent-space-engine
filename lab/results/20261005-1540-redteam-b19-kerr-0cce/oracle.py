#!/usr/bin/env python3
"""Independent equatorial-Kerr oracle for the B19 red-team (run 20261005-1540).

Everything is derived from the metric only (Boyer-Lindquist equatorial, G = c = M = 1, spin a = chi):
  g_tt = -(1-2/r), g_tphi = -2a/r, g_phiphi = r^2+a^2+2a^2/r, g_rr = r^2/Delta, Delta = r^2-2r+a^2.
Conventions here: ntt = -g_tt = 1-2/r, gtp = g_tphi (NEGATIVE), gpp = g_phiphi.
  E = -u_t = ntt u^t - gtp u^phi,   L = u_phi = gtp u^t + gpp u^phi,
  det of the 2x2 system = Delta, u^t = (E gpp + gtp L)/Delta  (Cramer; cross-checked against A(E-wL)/(r^2 Delta)).
Future-directed = u^t > 0 = positive ZAMO energy E - w L > 0, w = -g_tphi/g_phiphi = 2ar/A.
The decisive evidence is a raw Christoffel-symbol RK4 integration (no first integrals trusted).
"""
import numpy as np
from mpmath import mp, mpf, sqrt, findroot, cos, acos

mp.dps = 40
CHI = [mpf('0.5'), mpf('0.9'), mpf('0.998')]
CHIf = [0.5, 0.9, 0.998]
say_lines = []


def say(s=""):
    print(s)
    say_lines.append(s)


# ---------- mpmath metric machinery --------------------------------------------------------------------------
def met(a, r):
    return 1 - 2 / r, -2 * a / r, r * r + a * a + 2 * a * a / r  # (ntt, gtp, gpp)


def omega(a, r):
    _, gtp, gpp = met(a, r)
    return -gtp / gpp  # = 2ar/A


def lapse(a, r):
    _, _, gpp = met(a, r)
    return sqrt((r * r - 2 * r + a * a) / gpp)  # = sqrt(Delta Sigma^2 / A), A = r^2 g_phiphi


def utsolve(a, r, E, L):
    ntt, gtp, gpp = met(a, r)
    det = ntt * gpp + gtp * gtp  # = Delta (asserted)
    return (E * gpp + gtp * L) / det, (ntt * L - gtp * E) / det


def Pfun(a, r, E, L):
    return E * (r * r + a * a) - a * L


def Rfun(a, r, E, L, mu2):
    x = L - a * E
    return Pfun(a, r, E, L) ** 2 - (r * r - 2 * r + a * a) * (mu2 * r * r + x * x)


def zamo_state(a, r, vr, vphi):
    ntt, gtp, gpp = met(a, r)
    al, w = lapse(a, r), omega(a, r)
    g = 1 / sqrt(1 - vr * vr - vphi * vphi)
    L = sqrt(gpp) * g * vphi
    return al * g + w * L, L, g  # E, L, eps=gamma


def circ_den(a, r, s):
    Om = s / (r ** mpf('1.5') + s * a)
    ntt, gtp, gpp = met(a, r)
    return ntt - 2 * gtp * Om - gpp * Om * Om  # -(g_tt+2 g_tphi Om+g_phiphi Om^2)/u^t^2; photon orbit at 0


def circ(a, r, s):
    Om = s / (r ** mpf('1.5') + s * a)
    ntt, gtp, gpp = met(a, r)
    den = circ_den(a, r, s)
    ut = 1 / sqrt(den)
    return (ntt - gtp * Om) * ut, (gtp + gpp * Om) * ut, ut, den  # E, L, u^t, den


# ---------- P1: anchors ---------------------------------------------------------------------------------------
def bisect(f, lo, hi, it=300):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


say("# P1 anchors: my machinery vs BPT closed forms (worst relative difference per chi)")
for a in CHI:
    rh = 1 + sqrt(1 - a * a)
    worst = mpf(0)
    for s, lo, hi in [(1, rh * (1 + mpf('1e-6')), 8), (-1, 2.2, 9.5)]:
        # den = -(u.u)/u^t^2 of the circular orbit of this sense: <0 where none exists; r_ph is where it crosses
        den = lambda r, s=s: circ_den(a, r, s)
        if s > 0:  # prograde: den<0 just above the horizon (no circular timelike), >0 above r_ph
            rph = bisect(lambda r: -den(r), lo, hi)
        else:      # retrograde: den(2.2)<0, den(9.5)>0, single crossing at r_ph-
            rph = bisect(den, lo, hi)
        dE = lambda r, s=s: circ(a, r, s)[0] - circ(a, r + mpf('1e-7'), s)[0]
        risco = bisect(dE, rph * (1 + mpf('1e-6')), hi)
        Z1 = 1 + (1 - a * a) ** (mpf(1) / 3) * ((1 + a) ** (mpf(1) / 3) + (1 - a) ** (mpf(1) / 3))
        Z2 = sqrt(3 * a * a + Z1 * Z1)
        worst = max(worst, abs(risco / (3 + Z2 - s * sqrt((3 - Z1) * (3 + Z1 + 2 * Z2))) - 1),
                    abs(rph / (2 * (1 + cos((mpf(2) / 3) * acos(-s * a)))) - 1))
        say(f"  chi={float(a)} {'pro' if s>0 else 'retro'}: r_ph={float(rph):.12f} r_isco={float(risco):.12f}")
    r = mpf('4.3195')
    ntt, gtp, gpp = met(a, r)
    A = r * (r * r + a * a) + 2 * a * a
    d = r * r - 2 * r + a * a
    ident = [abs((ntt * gpp + gtp * gtp) / d - 1), abs(lapse(a, r) ** 2 / (ntt + gpp * omega(a, r) ** 2) - 1)]
    worst = max(worst, max(ident), abs(rh / (1 + sqrt(1 - a * a)) - 1))
    say(f"  chi={float(a)}: horizon={float(rh):.12f}; det/omega/lapse identities {float(max(ident)):.2e}; TOTAL {float(worst):.2e}")

worst_r = mpf(0)
for a in CHI:
    for (r, vr, vphi, mu2) in [(mpf('1.7'), mpf('0.3'), mpf('-0.5'), 1), (mpf('3.3'), mpf('-0.2'), mpf('0.8'), 1),
                               (mpf('2.7'), mpf('0.1'), mpf('-0.9'), 0), (mpf('1.45'), mpf('0'), mpf('-0.95'), 0)]:
        E, L, g = zamo_state(a, r, vr, vphi)
        ntt, gtp, gpp = met(a, r)
        # ZAMO split: spatial momentum squared p^2 = eps^2 - mu2 (m=1 timelike, 0 null); g_rr (u^r)^2 = p^2 - L^2/g_phiphi
        ur2 = (g * g - mu2) - L * L / gpp
        R = Rfun(a, r, E, L, mu2)
        worst_r = max(worst_r, abs(R / (r * r * (r * r - 2 * r + a * a) * ur2) - 1))
say(f"  radial polynomials vs metric (timelike and null, 40 digits): worst {float(worst_r):.2e}")
say()

# ---------- P2/P3: the disputed states -------------------------------------------------------------------------
say("# P2/P3 the disputed states at r = (r_+ + 2)/2 (v_r = 0)")
EX = {}
for a in CHI:
    rh = 1 + sqrt(1 - a * a)
    r = (rh + 2) / 2
    al, w = lapse(a, r), omega(a, r)
    ntt, gtp, gpp = met(a, r)
    A = r * r * (r * r + a * a + 2 * a * a / r)  # Sigma^2 g_phiphi
    E, L, g = zamo_state(a, r, 0, mpf('-0.9995'))
    ut_c, up_c = utsolve(a, r, E, L)
    ut_A = A * (E - w * L) / (r * r * (r * r - 2 * r + a * a))  # A = r^2 gpp
    ut_z = g / al
    Rmid = Rfun(a, (r + rh) / 2, E, L, 1)
    Rh = Rfun(a, rh * (1 + mpf('1e-9')), E, L, 1)
    say(f"  chi={float(a)} r={float(r):.6f}: v_phi=-0.9995: E={float(E):.9f} L={float(L):.9f}")
    say(f"    u^t: cramer={float(ut_c):.12f} A(E-wL)/(r^2D)={float(ut_A):.12f} eps/alpha={float(ut_z):.12f}  "
        f"P={float(Pfun(a, r, E, L)):.6f}  R(mid to horizon)={float(Rmid):.4f} R(r_+)={float(Rh):.6f}")
    assert E < 0 and L < 0 and ut_c > 0 and ut_A > 0 and ut_z > 0
    assert max(abs(ut_c / ut_A - 1), abs(ut_c / ut_z - 1)) < mpf('1e-30')
    assert Pfun(a, r, E, L) > 0 and Rmid >= 0 and Rh > 0
    from mpmath import polyroots as _pr
    x_ = L - a * E
    _roots = _pr([(E**2 - 1), 2, a**2 * (E**2 - 1) - L**2, 2 * x_**2], maxsteps=300)
    real_roots = sorted(rr.real for rr in _roots if abs(rr.imag) < mpf('1e-30'))
    gaps = [float(rr) for rr in real_roots if rh < rr < r]
    say(f"    roots of R between r_+ and r: {gaps} (empty => the allowed arc reaches the horizon: it plunges)")
    EX[a] = (r, E, L)
    E0, L0, g0 = zamo_state(a, r, 0, mpf('0.6'))
    pph = L0 / sqrt(gpp)
    ef, eb = (g0 + pph) / 2, (g0 - pph) / 2
    lf, lb = ef * sqrt(gpp), -eb * sqrt(gpp)
    Ef, Eb = al * ef + w * lf, al * eb + w * lb
    utb, _ = utsolve(a, r, Eb, lb)
    Rb = Rfun(a, (r + rh) / 2, Eb, lb, 0)
    say(f"    split(v=0.6): E0={float(E0):.9f} Efwd={float(Ef):.9f} Eback={float(Eb):.9f} gain={float(Ef/E0):.6f} "
        f"consE={float(abs(Ef+Eb-E0)/abs(E0)):.1e} consL={float(abs(lf+lb-L0)/abs(L0)):.1e}")
    say(f"    back photon: eps={float(eb):.6f}>0 future, u^t={float(utb):.6f}>0, P={float(Pfun(a, r, Eb, lb)):.4f}>0, "
        f"L={float(lb):.4f}<0, R(mid)={float(Rb):.4f} -> plunges; null E<0 FUTURE-DIRECTED exists")
    assert eb > 0 and ef > 0 and Eb < 0 and Ef > E0 and utb > 0 and Pfun(a, r, Eb, lb) > 0
    E3, L3, _ = zamo_state(a, 3, 0, mpf('0.6'))
    al3, w3 = lapse(a, 3), omega(a, 3)
    _, _, gpp3 = met(a, 3)
    eb3 = ((E3 - w3 * L3) / al3 - L3 / sqrt(gpp3)) / 2
    Eb3 = al3 * eb3 - w3 * eb3 * sqrt(gpp3)
    say(f"    same split at r=3: Eback={float(Eb3):.9f} > 0 (no gain outside the ergosphere)")
    assert Eb3 > 0
    ref = [(float(rp), float(Rfun(a, mpf(rp), E, L, 1)), float(utsolve(a, mpf(rp), E, L)[0]))
           for rp in ['2.2', '3', '5', '8', '15', '30']]
    say("    forged outside (criterion 4b): " + "; ".join(f"r'={rr:.1f}:R={v:.3f},u^t={u:.3f}" for rr, v, u in ref))
    assert all(v < 0 or u < 0 for _, v, u in ref)
say()

# ---------- the raw integration falsifier (float64 Christoffel RK4) -------------------------------------------
def integrate(a, y0, tau_max=60.0, dtau=0.01):
    def f(y):
        t, r, ph, ut, ur, up = y
        d = r * r - 2 * r + a * a
        ntt, gtp, gpp = 1 - 2 / r, -2 * a / r, r * r + a * a + 2 * a * a / r
        grr = r * r / d
        dntt, dgtp, dgpp = 2 / r**2, 2 * a / r**2, 2 * r - 2 * a * a / r**2
        dgrr = -2 * r * (r - a * a) / d**2
        gtt_, gtp_, gpp_ = -gpp / d, gtp / d, ntt / d  # g^{tt}=-g_phiphi/Delta, g^{tphi}, g^{phiphi}=ntt/Delta
        Grrr = 0.5 * (d / (r * r)) * dgrr
        Gtt = 0.5 * (d / (r * r)) * dntt          # Gamma^r_tt = -1/2 g^rr (g_tt)' = +1/2 g^rr ntt'
        Gtph = -0.5 * (d / (r * r)) * dgtp        # Gamma^r_tphi = -1/2 g^rr gtp'
        Gpp = -0.5 * (d / (r * r)) * dgpp         # Gamma^r_phiphi
        Htt = 0.5 * (gtt_ * (-dntt) + gtp_ * dgtp)   # Gamma^t_{tr} = 1/2(g^{tt} g_tt' + g^{tphi} gtp')
        Htph = 0.5 * (gtt_ * dgtp + gtp_ * dgpp)     # Gamma^t_{r phi}
        Ktt = 0.5 * (gtp_ * (-dntt) + gpp_ * dgtp)   # Gamma^phi_{tr}
        Ktph = 0.5 * (gtp_ * dgtp + gpp_ * dgpp)     # Gamma^phi_{r phi}
        dut = -2 * Htt * ut * ur - 2 * Htph * ur * up
        dur = -Grrr * ur * ur - Gtt * ut * ut - 2 * Gtph * ut * up - Gpp * up * up
        dup = -2 * Ktt * ut * ur - 2 * Ktph * ur * up
        return np.array([ut, ur, up, dut, dur, dup])

    y = np.array(y0, float)
    n = int(tau_max / dtau)
    hist = []
    for i in range(n):
        k1 = f(y)
        k2 = f(y + 0.5 * dtau * k1)
        k3 = f(y + 0.5 * dtau * k2)
        k4 = f(y + dtau * k3)
        y = y + dtau * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        if not np.isfinite(y).all():
            break
        hist.append(y.copy())
        if y[1] < (1 + sqrt(1 - a * a)) * (1 + 2e-3):  # reached the horizon (stop before the coordinate blow-up)
            break
        if y[1] > 200:
            break
    return y, np.array(hist)


def consts(a, y):
    t, r, ph, ut, ur, up = y
    ntt, gtp, gpp = 1 - 2 / r, -2 * a / r, r * r + a * a + 2 * a * a / r
    return ntt * ut - gtp * up, gtp * ut + gpp * up


say("# raw RK4 integration from the Christoffel symbols (no first integrals used inside the integrator)")
for a in CHI:
    af = float(a)
    rh = float(1 + sqrt(1 - a * a))
    r = float(EX[a][0])
    al, w = float(lapse(a, mpf(r))), float(omega(a, mpf(r)))
    ntt, gtp, gpp = 1 - 2 / r, -2 * af / r, r * r + af * af + 2 * af * af / r
    # the P2 exhibit: v_phi = -0.9995 in the ZAMO frame
    v = -0.9995
    gam = 1 / np.sqrt(1 - v * v)
    ut0 = gam / al
    up0 = gam * w / al + gam * v / np.sqrt(gpp)  # u = eps n + p e_phi; n^phi = +omega/alpha
    y0 = [0, r, 0, ut0, 0.0, up0]
    y, hist = integrate(af, y0, tau_max=1.0, dtau=(1e-5 if af > 0.95 else 5e-5))
    E0, L0 = consts(af, y0)
    Ef, Lf = consts(af, y)
    drE = abs((Ef - E0) / E0)
    min_ut = hist[:, 3].min() if len(hist) else float('nan')
    end = "PLUNGED (r -> r_+)" if y[1] < rh * (1 + 1e-3) else f"r_final={y[1]:.4f}"
    say(f"  chi={af}: v_phi=-0.9995 body: E0={E0:+.6f} L0={L0:+.6f} -> {end}; u^t min={min_ut:.4f} "
        f"(future throughout: {min_ut > 0}); dE/E along path={drE:.1e}; dL/L={abs((Lf-L0)/L0):.1e}")
    assert E0 < 0 and min_ut > 0 and drE < 1e-3
    # the split's backward photon: v_phi = -1 along phihat in the ZAMO frame (null)
    ut0 = 1 / al
    up0 = w / al - 1 / np.sqrt(gpp)  # photon along -phihat in the ZAMO frame
    y, hist = integrate(af, [0, r, 0, ut0, 0.0, up0], tau_max=1.0, dtau=5e-5)
    E0, L0 = consts(af, [0, r, 0, ut0, 0.0, up0])
    Ef, _ = consts(af, y)
    min_ut = hist[:, 3].min()
    end = "PLUNGED (r -> r_+)" if y[1] < rh * (1 + 1e-3) else f"r_final={y[1]:.4f}"
    say(f"  chi={af}: backward split photon: E0={E0:+.6f} L0={L0:+.6f} -> {end}; u^t min={min_ut:.4f}; dE/E={abs((Ef-E0)/E0):.1e}")
    assert E0 < 0 and min_ut > 0
# control: an ordinary bound retrograde orbit at chi=0.9 (from the circular machinery, r=12)
a = mpf('0.9')
E0, L0, ut0, _ = circ(a, mpf(12), -1)
af, r = 0.9, 12.0
ut0 = float(ut0)
up0 = ut0 * float(-1 / (mpf(12) ** mpf('1.5') - a))
y, hist = integrate(af, [0, r, 0, ut0, 0.0, up0], tau_max=800, dtau=0.5)
E1, L1 = consts(af, [0, r, 0, ut0, 0.0, up0])
Ef, Lf = consts(af, y)
say(f"  control chi=0.9 retrograde circular at r=12: r_final={y[1]:.4f} (stays out), dE/E={abs((Ef-E1)/E1):.1e}")
assert abs(y[1] - 12) < 0.3
say()

# ---------- vectorized scans (float64) ------------------------------------------------------------------------
def cubic_real_roots(c3, c2, c1, c0):
    """Real roots (n,3 ascending) of c3 x^3 + c2 x^2 + c1 x + c0, arrays; count of real roots."""
    b, c, d = c2 / c3, c1 / c3, c0 / c3
    p = c - b * b / 3
    q = 2 * b**3 / 27 - b * c / 3 + d
    disc = q * q / 4 + p**3 / 27
    three = disc <= 0
    m = 2 * np.sqrt(np.maximum(-p / 3, 0))
    arg = np.clip(3 * q / (p * m + 1e-300) / 2 * np.sqrt(np.maximum(-3 / p, 0)), -1, 1)
    th = np.arccos(arg)
    roots = np.stack([m * np.cos(th / 3 - 2 * np.pi * k / 3) - b / 3 for k in range(3)], -1)
    roots.sort(-1)
    return roots, np.where(three, 3, 1)


def omf(a, r):
    return 2 * a / (r * (r * r + a * a + 2 * a * a / r))  # -g_tphi/g_phiphi


say("# P5 sign equivalence on allowed states: sign(u^t) = sign(E - wL) = sign(P)")
mism_utP = mism_utw = n_allowed = 0
maxdiff = 0.0
for a in CHIf:
    rh = 1 + np.sqrt(1 - a * a)
    rs = np.exp(np.linspace(np.log(rh * (1 + 1e-6)), np.log(40), 70))
    Es = np.concatenate([-np.logspace(-2, 1, 50), [0.0], np.logspace(-2, 1, 50)])
    Ls = np.concatenate([-np.logspace(-1, 2.5, 45), [0.0], np.logspace(-1, 2.5, 45)])
    Eg, Lg, Rg = np.meshgrid(Es, Ls, rs, indexing='ij')
    x = Lg - a * Eg
    P = Eg * (Rg**2 + a * a) - a * Lg
    R = P**2 - (Rg**2 - 2 * Rg + a * a) * (Rg**2 + x * x)
    scale = P**2 + (Rg**2 - 2 * Rg + a**2) * (Rg**2 + x * x)
    ok = R >= 1e-9 * scale
    n_allowed += ok.sum()
    A = Rg * (Rg**2 + a**2) + 2 * a**2
    ut = A * (Eg - omf(a, Rg) * Lg)  # numerator of u^t; denominator r^2 Delta > 0
    mism_utP += (ok & (np.sign(ut) != np.sign(P))).sum()
    mism_utw += (ok & (np.sign(ut) != np.sign(Eg - omf(a, Rg) * Lg))).sum()
    maxdiff = max(maxdiff, np.abs((Eg * (Rg * (Rg**2 + a**2) + 2 * a**2 / Rg * Rg) + (-2 * a / Rg) * Lg) * 0)  # placeholder
                 if False else maxdiff)
say(f"  allowed states sampled: {n_allowed}; sign(u^t)!=sign(P): {mism_utP}; sign(u^t)!=sign(E-wL): {mism_utw}")
neg_out = 0
for a in CHIf:
    rh = 1 + np.sqrt(1 - a * a)
    rs = np.exp(np.linspace(np.log(rh * (1 + 1e-6)), np.log(40), 70))
    Es = -np.logspace(-3, 1, 40)   # E < 0 only
    Ls = -np.logspace(-3, 2.5, 40)  # L < 0 only
    Eg, Lg, Rg = np.meshgrid(Es, Ls, rs, indexing='ij')
    x = Lg - a * Eg
    P = Eg * (Rg**2 + a * a) - a * Lg
    R = P**2 - (Rg**2 - 2 * Rg + a**2) * (Rg**2 + x * x)
    scale = P**2 + (Rg**2 - 2 * Rg + a**2) * (Rg**2 + x * x)
    ok = (R >= 1e-9 * scale) & (Rg >= 2.0) & (Eg - omf(a, Rg) * Lg > 0)
    neg_out += ok.sum()
say(f"  future-directed E<0 allowed states at r>=2: {neg_out} (prediction: 0)")

say()
say("# P4 the disputed claim: bound (two-turning-point) pockets with E<0, fully future-directed?")
for a in [0.01, 0.1, 0.5, 0.9, 0.998, 0.9999]:
    rh = 1 + np.sqrt(1 - a * a)
    es = np.logspace(-4, np.log10(0.99999), 260)
    lams = np.logspace(-3, 3, 850)
    tot = futP = futW = 0
    margin = -1e9
    for e in es:
        E, L = -e, -lams
        x = L - a * E
        c3 = np.full_like(lams, E**2 - 1)
        c2 = np.full_like(lams, 2.0)
        c1 = a**2 * (E**2 - 1) - L**2
        c0 = 2 * x**2
        roots, nreal = cubic_real_roots(c3, c2, c1, c0)
        s1, s2 = roots[..., 2], roots[..., 1]  # ascending; pocket [s2, s1] (leading coeff < 0)
        rm = 0.5 * (s1 + s2)
        Pm = E * (rm**2 + a**2) - a * L
        Rm = Pm**2 - (rm**2 - 2 * rm + a**2) * (rm**2 + x**2)
        ok = (nreal == 3) & (s2 > rh) & (s1 < 1e3) & (Rm > 0)
        pA = E * (s1**2 + a**2) - a * L          # builder's test: P at the apoapsis (binding, P decreasing)
        futP += int((ok & (pA > 0)).sum())
        futw = ok & (-e + omf(a, s1) * lams > 0)  # the true test: future at the apoapsis
        futW += int(futw.sum())
        if futw.any():
            margin = max(margin, float(np.max(-e + omf(a, s1) * lams[futw])))
        tot += int(ok.sum())
    say(f"  chi={a}: timelike bound E<0 pockets: {tot}; fully future by the builder's P test: {futP}; "
        f"by the true u^t test: {futW}" + (f"  MARGIN={margin:.3e}" if futW else ""))
say()
say("# P4 null: bound pockets with E<0 (E=-1, L=-lam)?")
for a in [0.1, 0.5, 0.9, 0.998, 0.9999]:
    rh = 1 + np.sqrt(1 - a * a)
    lams = np.logspace(-2, 4, 1500)
    E, L = -1.0, -lams
    x = L - a * E
    c3 = np.ones_like(lams)
    c2 = np.full_like(lams, 2.0)
    c1 = a**2 - lams**2
    c0 = 2 * x**2
    roots, nreal = cubic_real_roots(c3, c2, c1, c0)
    s3, s2 = roots[..., 0], roots[..., 1]  # pocket [s3, s2] (leading coeff > 0)
    rm = 0.5 * (s3 + s2)
    Pm = E * (rm**2 + a**2) - a * L
    Rm = Pm**2 - (rm**2 - 2 * rm + a**2) * x**2
    ok = (nreal == 3) & (s3 > rh) & (Rm > 0) & (s2 < 1e4)
    pA = E * (s2**2 + a**2) - a * L
    futw = ok & (-1 + omf(a, s2) * lams > 0)
    say(f"  chi={a}: null bound E<0 pockets: {int(ok.sum())}; future by P test: {int((ok & (pA > 0)).sum())}; "
        f"by true test: {int(futw.sum())}")
say()

say("# P6 planted laws vs the row's criteria")
a = 0.998
rh = 1 + np.sqrt(1 - a * a)
r = 0.5 * (rh + 2)
gpp = r * r + a * a + 2 * a * a / r
al = np.sqrt((r * r - 2 * r + a * a) / gpp)
w = 2 * a / (r * gpp)  # -g_tphi/g_phiphi
v = -0.9995
gam = 1 / np.sqrt(1 - v * v)
L = np.sqrt(gpp) * gam * v
E_kerr = al * gam + w * L
E_nodrag = al * gam  # law (a): omega := 0
ut_n = gam / al  # no-drag normalization
Omega_nodrag = (L / gpp) / ut_n
say(f"  (a) no frame dragging: at r={r:.4f}, v_phi=-0.9995: kerr E={E_kerr:+.6f} vs law E={E_nodrag:+.6f} (>0: no negative-energy tube -> fails 4a); "
    f"law dphi/dt={Omega_nodrag:+.6f} (<0 inside the ergosphere -> fails criterion 3)")
assert E_nodrag > 0 and Omega_nodrag < 0
say(f"  (b) Schwarzschild fudged to the ISCO: b_c = 3*sqrt(3) = {3*np.sqrt(3):.6f} both senses;")
for aa in CHIf:
    rph = {}
    for s, tag in [(1, 'pro'), (-1, 'retro')]:
        # circular photon: solve -(g_tt + 2 g_tph Om + g_pph Om^2) = 0 by bisection on r
        lo, hi = (1 + np.sqrt(1 - aa**2)) * 1.000001, 3 if s > 0 else 2.2
        if s < 0:
            lo, hi = 3, 9
        for _ in range(200):
            rm = 0.5 * (lo + hi)
            Om = s / (rm**1.5 + s * aa)
            den = -(1 - 2 / rm) + 2 * (-2 * aa / rm) * Om + (rm * rm + aa**2 + 2 * aa**2 / rm) * Om**2  # g_tt+2 g_tphi Om+g_pph Om^2
            # den = -(u.u)/u^t^2 ; photon circular where den = 0; den<0 between horizon and r_ph (no timelike), >0 above
            if den > 0:   # +(u.u)/u^t^2 > 0 below the photon orbit of this sense: root above rm
                lo = rm
            else:
                hi = rm
        rm = 0.5 * (lo + hi)
        Om = s / (rm**1.5 + s * aa)
        ntt, gtp, gppp = 1 - 2 / rm, -2 * aa / rm, rm * rm + aa**2 + 2 * aa**2 / rm
        b = (gtp + gppp * Om) / (ntt - gtp * Om)
        rph[tag] = b
        assert abs(rm - float({'pro': 2.347296355334 if aa==0.5 else 1.557854627423 if aa==0.9 else 1.073909257680,
                               'retro': 3.532088886238 if aa==0.5 else 3.910267939103 if aa==0.9 else 3.998221892848}[tag])) < 1e-5, (tag, aa, rm)
    bdis = 0.5 * (abs(rph["retro"]) + 3 * np.sqrt(3))  # between Kerr's retrograde edge and Schwarzschild's
    kerr_cap = abs(bdis) < abs(rph["retro"])
    fudge_cap = bdis < 3 * np.sqrt(3)
    say(f"      chi={aa}: b_pro={rph['pro']:+.4f}, b_retro={rph['retro']:+.4f}; retro b={-bdis:.4f}: "
        f"kerr {'captures' if kerr_cap else 'scatters'} vs fudge {'captures' if fudge_cap else 'scatters'}"
        + (" -> MISCLASSIFIED (fails 2d/5)" if kerr_cap != fudge_cap else " -> agrees here"))
E0v = al / np.sqrt(1 - 0.36)
L0v = np.sqrt(gpp) / np.sqrt(1 - 0.36) * 0.6
g0v = 1 / np.sqrt(1 - 0.36)
ebv = (g0v - L0v / np.sqrt(gpp)) / 2
Ebv = al * ebv - w * ebv * np.sqrt(gpp)
ulp = 8 * 2.2e-16 * (abs(E0v) + abs(L0v))
say(f"  (c) non-conserving split at chi=0.998 r={r:.4f}: true E_back={Ebv:+.6f} (<0); a law returning |E_back|, "
    f"E_fwd=E0+|E_back| breaks conservation by {2*abs(Ebv):.6f} = {2*abs(Ebv)/ulp:.1e}x the 8-ulp bound -> fails 4c")

with open("findings.txt", "w") as f:
    f.write("\n".join(say_lines) + "\n")
say()
say("done")
