#!/usr/bin/env python3
"""Premise red-team falsifier v2 (fast): quadrature, no ODEs.

Premise under attack (representation.md S2 / law.md line 53):
  "Each visible tube crosses the observer's past light cone once; Newton's method
   finds the crossing. Lensing adds crossings, from each doll's memoized deflection(b)."

Oracle: exact equatorial null geodesics, M = G = c = 1.
(du/dphi)^2 = P(u) = 1/b^2 - u^2 + 2u^3  (Schwarzschild photon).
Construction (most charitable reading): flat retarded direction + point-lens equation
beta = theta - (D_ls/D_s)*alpha(b(theta)), flat trig distances, alpha = the EXACT
two-point deflection from the oracle. Any error is composition error.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.interpolate import PchipInterpolator
import json, time

BCRIT = 3.0 * np.sqrt(3.0)

def periastron(b, u_o, u_s):
    """Turning point: smallest real root of P above both endpoint u's.
    None = plunge, or b unlaunchable from an endpoint."""
    if (1.0/b**2 - u_o**2 + 2*u_o**3) < 0 or (1.0/b**2 - u_s**2 + 2*u_s**3) < 0:
        return None
    r = np.roots([2.0, -1.0, 0.0, 1.0 / b**2])
    r = [x.real for x in r if abs(x.imag) < 1e-11]
    good = [u for u in r if u > max(u_o, u_s) and u < 0.5 - 1e-9]
    return min(good) if good else None

def _Q(b, u):
    """P(u)/(u_max - u) = (1-2*u_max)(u_max+u) - 2u^2, valid for u <= u_max."""
    um = _Q.cache_um
    return (1 - 2*um)*(um + u) - 2*u*u
_Q.cache_um = None

def sweep(b, r_o, r_s):
    """Azimuth swept from radius r_o to periastron to radius r_s; inf on plunge."""
    u_o, u_s = 1.0/r_o, 1.0/r_s
    um = periastron(b, u_o, u_s)
    if um is None:
        return np.inf
    _Q.cache_um = um
    def half(u_end):
        s_end = np.sqrt(um - u_end)
        f = lambda s: 2.0 / np.sqrt(max(_Q(b, um - s*s), 1e-300))
        val, _ = quad(f, 0.0, s_end, limit=400)
        return val
    return half(u_o) + half(u_s)

def travel_time(b, r_o, r_s):
    """Coordinate time along the same path."""
    u_o, u_s = 1.0/r_o, 1.0/r_s
    um = periastron(b, u_o, u_s)
    if um is None:
        return np.inf
    _Q.cache_um = um
    def half(u_end):
        s_end = np.sqrt(um - u_end)
        f = lambda s: 2.0 / (b * (um - s*s)**2 * (1 - 2*(um - s*s)) * np.sqrt(max(_Q(b, um - s*s), 1e-300)))
        val, _ = quad(f, 0.0, s_end, limit=400)
        return val
    return half(u_o) + half(u_s)

def dphi_flat(b, r_o, r_s):
    return np.arccos(b / r_o) + np.arccos(b / r_s)

def alpha_table(r_o, r_s, n=600):
    """Two-point deflection indexed by the gather's own variable b_flat = r_o sin(theta):
    alpha(bf) = exact sweep of the path with relativistic b = bf/sqrt(1-2/r_o),
    minus the flat sweep at bf. The construction is fed the TRUE bend of the TRUE
    path at each screen angle, so only composition error can remain."""
    f = 1.0 - 2.0/r_o
    bfs = np.linspace(BCRIT*np.sqrt(f)*1.0002, r_o*0.9999, n)
    alphas = np.full(n, np.inf)
    for i, bf in enumerate(bfs):
        d = sweep(bf/np.sqrt(f), r_o, r_s)
        if np.isfinite(d):
            alphas[i] = d - dphi_flat(bf, r_o, r_s)
    ok = np.isfinite(alphas)
    return PchipInterpolator(bfs[ok], alphas[ok], extrapolate=False)

def exact_b_for_sweep(target, b_lo=BCRIT*1.0000001, b_hi=None):
    """sweep(b) is decreasing in b; find b with sweep = target."""
    if b_hi is None:
        b_hi = R_O / np.sqrt(1.0 - 2.0/R_O) * 0.999999  # launchable from r_o
    f = lambda b: sweep(b, R_O, R_S) - target
    if f(b_hi) > 0:
        return None
    return brentq(f, b_lo, b_hi, xtol=1e-12, rtol=1e-14)

def kerr_photon_orbits(a):
    """Closed-form equatorial circular photon orbits (Bardeen 1973):
    r_ph = 2[1 + cos((2/3) arccos(s*a))] (s=-1 prograde); b from the
    square-root branch of R=0: b = (r^2+a^2+a*sqrt(Delta))/(a+sqrt(Delta))."""
    out = {}
    for name, sign in (("pro", -1), ("retro", +1)):
        r_ph = 2.0*(1.0 + np.cos((2.0/3.0)*np.arccos(np.clip(sign*a, -1, 1))))
        D = r_ph*r_ph - 2.0*r_ph + a*a
        b = (r_ph*r_ph + a*a + a*np.sqrt(D)) / (a + np.sqrt(D)) if abs(a + np.sqrt(D)) > 1e-12 else 2.0
        out[name] = (r_ph, b)
    return out

R_O, R_S = 10.0, 50.0  # module-level current case (for exact_b_for_sweep closure)

def exact_images(r_o, r_s, Phi, windings=(0, 1)):
    global R_O, R_S
    R_O, R_S = r_o, r_s
    out = []
    for fam, base in (("ccw", Phi), ("cw", 2*np.pi - Phi)):
        for k in windings:
            target = base + 2*np.pi*k
            b = exact_b_for_sweep(target)
            if b is None:
                continue
            psi = np.degrees(np.arcsin(min(1.0, b*np.sqrt(max(0.0, 1 - 2/r_o))/r_o)))
            out.append({"b": b, "psi": psi if fam == "ccw" else -psi, "fam": fam, "k": k})
    return out

def construction(r_o, r_s, Phi, alpha_interp):
    S = np.array([r_s*np.cos(Phi), r_s*np.sin(Phi)]); O = np.array([r_o, 0.0])
    D_s = np.linalg.norm(S - O); D_ls = r_s
    dsrc = (S - O)/D_s
    beta = np.degrees(np.arctan2(dsrc[1], -dsrc[0]))  # angle from hole direction (-x)
    bmax = min(r_o, r_s) * 0.999999
    th_hi = np.arcsin(bmax/r_o)
    imgs = []
    def eq(theta):
        b = r_o*np.sin(theta)
        a = alpha_interp(b)
        if a is None or not np.isfinite(a):
            return np.nan
        return theta - (D_ls/D_s)*a - np.radians(beta)
    g = np.linspace(1e-6, th_hi - 1e-9, 8000)
    v = np.array([eq(t) for t in g])
    for i in np.where(np.sign(v[:-1])*np.sign(v[1:]) < 0)[0]:
        try:
            imgs.append(+brentq(eq, g[i], g[i+1], xtol=1e-13))
        except ValueError: pass
    def eq_neg(tn):
        t = abs(tn)
        b = r_o*np.sin(t)
        a = alpha_interp(b)
        if a is None or not np.isfinite(a):
            return np.nan
        return -t + (D_ls/D_s)*a - np.radians(beta)
    vn = np.array([eq_neg(t) for t in g])
    for i in np.where(np.sign(vn[:-1])*np.sign(vn[1:]) < 0)[0]:
        try:
            imgs.append(-brentq(eq_neg, g[i], g[i+1], xtol=1e-13))
        except ValueError: pass
    return beta, sorted(imgs)

def run_case(name, r_o, r_s, betas_off_deg):
    atab = alpha_table(r_o, r_s)
    rows = []
    for off in betas_off_deg:
        Phi = np.pi - np.radians(off)
        ex = exact_images(r_o, r_s, Phi)
        beta, con = construction(r_o, r_s, Phi, atab)
        prim = [e for e in ex if e["k"] == 0]
        pos = sorted([e["psi"] for e in prim if e["psi"] > 0])
        neg = sorted([e["psi"] for e in prim if e["psi"] < 0])
        cpos = sorted([np.degrees(t) for t in con if t > 0])
        cneg = sorted([np.degrees(t) for t in con if t < 0])
        row = dict(off_deg=off, beta_deg=round(beta, 4), n_exact=len(ex),
                   n_exact_k0=len(prim),
                   psi_exact_pos=[round(p, 3) for p in pos[:2]],
                   psi_exact_neg=[round(p, 3) for p in neg[:2]],
                   psi_con=[round(c, 3) for c in cpos + cneg])
        if pos and cpos:
            err = abs(cpos[0] - pos[0])
            row["err_prim_deg"] = round(err, 3)
            row["err_prim_frac"] = round(err/pos[0], 4) if pos[0] else None
        if neg and cneg:
            row["err_sec_deg"] = round(abs(cneg[0] - neg[0]), 3)
        rows.append(row)
    return rows

def kerr_bcrit(a):
    return kerr_photon_orbits(a)

def kerr_alpha(b_signed, a, r_o, r_s):
    Delta = lambda r: r*r - 2*r + a*a
    Rf = lambda r: ((r*r + a*a) - a*b_signed)**2 - Delta(r)*(b_signed - a)**2
    rp = 1 + np.sqrt(max(0.0, 1 - a*a))
    rg = np.linspace(rp + 1e-9, min(r_o, r_s) - 1e-9, 200000)
    Rv = Rf(rg)
    idx = np.where(np.sign(Rv[:-1])*np.sign(Rv[1:]) < 0)[0]
    if len(idx) == 0:
        return np.inf
    r0 = brentq(Rf, rg[idx[-1]], rg[idx[-1]+1], xtol=1e-13)
    def dphidr_raw(r):
        return abs((b_signed - a) + a/Delta(r)*((r*r + a*a) - a*b_signed))/np.sqrt(max(Rf(r), 1e-300))
    s1, _ = quad(lambda t: 2*t*dphidr_raw(r0 + t*t), 0.0, np.sqrt(r_o - r0), limit=400)
    s2, _ = quad(lambda t: 2*t*dphidr_raw(r0 + t*t), 0.0, np.sqrt(r_s - r0), limit=400)
    return (s1 + s2) - (np.arccos(abs(b_signed)/r_o) + np.arccos(abs(b_signed)/r_s))

def main():
    t0 = time.time()
    out = {}
    out["weak_control"] = run_case("weak", 5000.0, 20000.0, [0.001, 0.005, 0.02, 0.1])
    out["r_o50_r_s200"] = run_case("mid", 50.0, 200.0, [0.02, 0.1, 0.5, 1, 2, 4, 8, 15, 25, 40])
    out["r_o10_r_s50"] = run_case("near", 10.0, 50.0, [0.02, 0.1, 0.5, 1, 2, 4, 8, 15, 25, 40])

    kerr = {}
    for a in (0.5, 0.9, 0.998):
        bc = kerr_photon_orbits(a)
        kerr[f"a={a}"] = dict(r_ph_pro=round(bc["pro"][0], 4), b_pro=round(bc["pro"][1], 4),
                              r_ph_retro=round(bc["retro"][0], 4), b_retro=round(bc["retro"][1], 4),
                              ratio=round(bc["retro"][1]/bc["pro"][1], 4))
    for bm in (6.0, 8.0, 12.0):
        ap = kerr_alpha(+bm, 0.9, 50.0, 200.0)
        ar = kerr_alpha(-bm, 0.9, 50.0, 200.0)
        kerr[f"a=0.9_|b|={bm}"] = dict(alpha_pro=round(ap, 4) if np.isfinite(ap) else None,
                                       alpha_retro=round(ar, 4) if np.isfinite(ar) else None,
                                       delta=round(abs(ap-ar), 4) if (np.isfinite(ap) and np.isfinite(ar)) else None)
    out["kerr"] = kerr

    p4 = []
    for v, r_o, r_s in ((0.5, 10.0, 15.0), (0.5, 10.0, 50.0), (0.5, 50.0, 200.0)):
        Phi = np.pi - 0.05
        ex = [e for e in exact_images(r_o, r_s, Phi) if e["k"] == 0 and e["psi"] > 0]
        if not ex:
            continue
        b = ex[0]["b"]
        t_ex = travel_time(b, r_o, r_s)
        S = np.array([r_s*np.cos(Phi), r_s*np.sin(Phi)])
        t_flat = np.linalg.norm(S - np.array([r_o, 0.0]))
        dt = t_ex - t_flat
        atab = alpha_table(r_o, r_s)
        beta, con = construction(r_o, r_s, Phi, atab)
        disp = ex[0]["psi"] - beta
        p4.append(dict(v=v, r_o=r_o, r_s=r_s, psi=round(ex[0]["psi"], 3),
                       shapiro_M=round(dt, 2), pos_err_deg=round(np.degrees(v*dt/t_flat), 4),
                       lens_disp_deg=round(disp, 3),
                       ratio=round(np.degrees(v*dt/t_flat)/disp, 4) if disp else None))
    out["p4_shapiro"] = p4

    # negative control: alpha = 0 => construction must equal the flat direction
    Phi = np.pi - 0.5; r_o, r_s = 10.0, 50.0
    class ZeroAlpha:
        def __call__(self, b): return 0.0
    beta, con = construction(r_o, r_s, Phi, ZeroAlpha())
    out["negative_control"] = dict(beta_deg=round(beta, 5),
                                   roots_deg=[round(np.degrees(t), 5) for t in con])
    out["oracle_selfcheck"] = dict(alpha_b100_weak=round(
        sweep(100.0, 500.0, 2000.0) - (np.arccos(100/500) + np.arccos(100/2000)), 6),
        weak_expect_ge_4_over_b=0.04)

    out["runtime_s"] = round(time.time() - t0, 2)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
