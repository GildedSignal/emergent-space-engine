#!/usr/bin/env python3
"""Pure-float port of the inclined-Kerr six-constant compile (second author on
20261017-2038-scout-8dfb; the checker's named experiment).

What this adds over the original instrument:
  1. Every elliptic element is now a COUNTED Carlson kernel call (RF/RD/RJ) --
     K(m) = RF(0,1-m,1); E(m) = RF - (m/3) RD; Pi(n|m) = RF + (n/3) RJ;
     J(n|m) = Pi + n dPi/dn in closed form, machine-derived (sympy partial
     fraction of the total-derivative identity d/dtheta[s c/((1-n s^2)W)]),
     verified against 40-dps quadrature in selftest. No mpmath on the CF path.
  2. Kernel counts per key (raw and shared) priced at de99's measured ns
     (rf 50 / rd 78 / rj 152) -- the adoption number.
  3. A root-case census: prevalence of every real-root case over the parameter
     grid, the rp - r2 gap, and Lambda_r where 0below occurs; LOUD assert.

Fidelity and exactness arms, verbatim from the original run's falsifier.py
(imported by path, not copied): QD (30-dps quadrature) and cf_arm (ellipk/
ellipe + 40-dps mpmath dPi/dn). Usage: python3 port.py [--censusonly]
"""
import sys, time, importlib.util
import numpy as np
from scipy.special import ellipk, ellipe, elliprf, elliprj, elliprd
import mpmath as mp

_spec = importlib.util.spec_from_file_location(
    "orig_falsifier", __file__.replace("port.py", "orig-falsifier.py"))
orig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(orig)

mp.mp.dps = 30
NAMES = ["Lam_r", "Lam_th", "dPhi_r", "dPhi_th", "dt_r", "dt_th"]
KCNT = {"rf": 0, "rd": 0, "rj": 0}
MEMO = None   # when a dict, kernel calls are memoized by argument (price's shared count)
def _km(kind, args, f):
    if MEMO is not None:
        key = (kind, tuple(args))
        if key not in MEMO:
            MEMO[key] = f(*args)
        return MEMO[key]
    return f(*args)
def _rf(x, y, z): KCNT["rf"] += 1; return _km("rf", (x, y, z), elliprf)
def _rd(x, y, z): KCNT["rd"] += 1; return _km("rd", (x, y, z), elliprd)
def _rj(x, y, z, w): KCNT["rj"] += 1; return _km("rj", (x, y, z, w), elliprj)

def Kc(m):        return _rf(0.0, 1.0 - m, 1.0)
def Ec(m):        return _rf(0.0, 1.0 - m, 1.0) - (m / 3.0) * _rd(0.0, 1.0 - m, 1.0)
def Pic(n, m):    return _rf(0.0, 1.0 - m, 1.0) + (n / 3.0) * _rj(0.0, 1.0 - m, 1.0, 1.0 - n)
def Jc(n, m):
    """J(n|m) = int_0^{pi/2} dth / ((1-n sin^2 th)^2 sqrt(1-m sin^2 th))
    = Pi + n dPi/dn, closed form (sympy-derived; asserted in selftest):
    [Pi(2mn-3m-n^2+2n) + K(m-n) + nE] / (2(n-1)(m-n))."""
    assert abs(n - 1.0) > 1e-6 and abs(m - n) > 1e-6, (n, m)
    K = Kc(m); E = Ec(m); P = Pic(n, m)
    return (P * (2.0*m*n - 3.0*m - n*n + 2.0*n) + K * (m - n) + n * E) \
        / (2.0 * (n - 1.0) * (m - n))

# ---------------------------------------------------------------- selftest --
def selftest():
    worst = {"K": 0.0, "E": 0.0, "Pi": 0.0, "J": 0.0}
    _dps = mp.mp.dps; mp.mp.dps = 40
    def mpJ(n, m):
        f = lambda th: 1 / ((1 - n*mp.sin(th)**2)**2 * mp.sqrt(1 - m*mp.sin(th)**2))
        return mp.quad(f, [0, mp.pi/2])
    for m in (0.05, 0.2, 0.44, 0.7, 0.9, 0.99):
        worst["K"] = max(worst["K"], float(abs(Kc(m) - mp.ellipk(m)) / mp.ellipk(m)))
        worst["E"] = max(worst["E"], float(abs(Ec(m) - mp.ellipe(m)) / mp.ellipe(m)))
        for n in (0.1, 0.35, 0.6, 0.85):
            if abs(m - n) < 0.02 or abs(n - 1) < 0.02:
                continue
            worst["Pi"] = max(worst["Pi"], float(abs(Pic(n, m) - mp.ellippi(n, m)) / mp.ellippi(n, m)))
            q = mpJ(n, m)
            worst["J"] = max(worst["J"], float(abs(Jc(n, m) - q) / q))
    mp.mp.dps = _dps
    for k, v in worst.items():
        assert v < 2e-14, (k, v)
    print("== selftest PASS: pure-float K/E/Pi/J vs 40-dps mpmath, worst:",
          {k: f"{v:.1e}" for k, v in worst.items()})
# --------------------------------------------------------- pure-float arm --
def cf_pure(a, E, Lz, Q, r_hint=None, z=None, band=None):
    out = {k: np.nan for k in NAMES}
    # ---- polar (biquadratic; needs a != 0, Q > 0)
    A = a * a * (1.0 - E * E)
    if A > 1e-14 and Q > 1e-14:
        up2, ul2 = orig.u2_roots(a, E, Lz, Q, z)
        mth = up2 / ul2
        ul = np.sqrt(ul2)
        K_ = Kc(mth); E_ = Ec(mth); P_ = Pic(up2, mth)
        out["Lam_th"] = 4.0 * K_ / (np.sqrt(A) * ul)
        out["dPhi_th"] = 4.0 * (Lz * P_ - a * E * K_) / (np.sqrt(A) * ul)
        out["dt_th"] = 4.0 * a * ((Lz - a*E) * K_ + a*E*up2*(K_ - E_)/mth) / (np.sqrt(A) * ul)
    elif Q <= 1e-14:
        out["Lam_th"] = out["dPhi_th"] = out["dt_th"] = 0.0
    # ---- radial
    rp, ra = band if band is not None else orig.band_roots(a, E, Lz, Q, r_hint)
    K = (Lz - a*E)**2 + Q
    coeffs = [E*E - 1.0, 2.0, 2*E*(E*a*a - a*Lz) - K - a*a, 2*K,
              (E*a*a - a*Lz)**2 - a*a*K]
    roots = np.roots(coeffs)
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-8*(1+abs(r.real)))
    below = [r for r in real if r < rp - 1e-7]
    out["_case"] = f"{len(real)}real/{len(below)}below"
    out["_gap"] = (rp - max(below)) if below else float("nan")
    if len(below) != 2:
        # LOUD: the checker found the original silently returning NaN here.
        raise RuntimeError(
            f"root case {out['_case']} unhandled (4real/2below derived only); "
            f"roots={np.round(roots,6).tolist()} rp={rp:.6f} ra={ra:.6f} "
            f"gap(rhobar-r2)={out.get('_gap')}")
    r1, r2 = below
    n1 = -rp*(ra - r1); n2v = (ra - rp)*r1
    d1 = -(ra - r1);    d2v = (ra - rp)
    def r_of_s(s): return (n1 + n2v*s)/(d1 + d2v*s)
    assert abs(r_of_s(0.0) - rp) < 1e-8*(1+rp) and abs(r_of_s(1.0) - ra) < 1e-8*(1+ra)
    def Qtilde(r): return (r - r1)*(r - r2)*(r - rp)*(ra - r)
    def drds(s): return (ra - r1)*(ra - rp)*(rp - r1)/(d1 + d2v*s)**2
    m_cl = -(ra - rp)*(r2 - r1)/((rp - r2)*(ra - r1))
    C_cl = 4.0/((rp - r2)*(ra - r1))
    scale = -(E*E - 1.0)
    K_ = Kc(m_cl)
    nh = -d2v/d1
    assert abs(nh - 1.0) > 1e-6 and abs(m_cl - nh) > 1e-6, (nh, m_cl)
    def decomp(g2, g1, g0):
        D = d1*d1
        Np = np.array([n1, n2v])
        P = np.zeros(3)
        for arr in (g2*np.convolve(Np, Np),
                    g1*d1*np.convolve(Np, [1.0, -nh]),
                    g0*D*np.convolve([1.0, -nh], [1.0, -nh])):
            P[:len(arr)] += arr
        e0 = np.array([D, -2*D*nh, D*nh*nh])
        e1 = np.array([D, -D*nh, 0.0])
        e2 = np.array([D, 0.0, 0.0])
        A_, B_, Cc = np.linalg.solve(np.array([e0, e1, e2]).T, P)
        for s in (0.1, 0.4, 0.8):
            lhs = g2*r_of_s(s)**2 + g1*r_of_s(s) + g0
            rhs = A_ + B_/(1 - nh*s) + Cc/(1 - nh*s)**2
            assert abs(lhs - rhs) < 1e-8*(1 + abs(lhs)), "decomp assert"
        return A_, B_, Cc
    def radial_closed(g2, g1, g0, poles):
        val = 0.0
        if any(abs(x) > 0 for x in (g2, g1, g0)):
            A_, B_, Cc = decomp(g2, g1, g0)
            # 1/(1-nh s)^2 piece: J = Pi + nh dPi/dn, now pure float (Jc)
            val += np.sqrt(C_cl/scale)*(A_*K_ + B_*Pic(nh, m_cl) + Cc*Jc(nh, m_cl))
        for c_, r0 in poles:
            if c_ == 0.0:
                continue
            W = (n1 - r0*d1)/d1
            n0 = -(n2v - r0*d2v)/(n1 - r0*d1)
            for s in (0.1, 0.5, 0.9):
                assert abs((r_of_s(s) - r0) - W*(1 - n0*s)/(1 - nh*s)) < 1e-7*(1+abs(W))
            P0 = Pic(n0, m_cl)
            val += c_/W*np.sqrt(C_cl/scale)*(K_ + (n0 - nh)/n0*(P0 - K_))
        return 2.0*val
    rpm = 1.0 + np.sqrt(max(1 - a*a, 0.0)); rmm = 1.0 - np.sqrt(max(1 - a*a, 0.0))
    dpm = rpm - rmm
    apm_p = a*(2*E*rpm - a*Lz)/dpm
    apm_m = a*(2*E*rmm - a*Lz)/(-dpm)
    out["Lam_r"] = 2.0*np.sqrt(C_cl/scale)*K_
    out["dPhi_r"] = radial_closed(0.0, 0.0, a*E, [(apm_p, rpm), (apm_m, rmm)])
    cp = (2*E*rpm - a*Lz)/dpm; cm = (2*E*rmm - a*Lz)/(-dpm)
    g2 = E; g1 = cp + cm; g0 = E*a*a + cp*rpm + cm*rmm
    out["dt_r"] = radial_closed(g2, g1, g0, [(cp*(rpm*rpm + a*a), rpm),
                                             (cm*(rmm*rmm + a*a), rmm)])
    return out

# ------------------------------------------------------------------ census --
def _quartic_real_below(a, E, Lz, Q, rp, tol):
    K = (Lz - a*E)**2 + Q
    coeffs = [E*E - 1.0, 2.0, 2*E*(E*a*a - a*Lz) - K - a*a, 2*K,
              (E*a*a - a*Lz)**2 - a*a*K]
    roots = np.roots(coeffs)
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-8*(1+abs(r.real)))
    below = [r for r in real if r < rp - tol]
    return real, below, roots

def _lam_r_fast(a, E, Lz, Q, rp, ra, r1, r2):
    m_cl = -(ra - rp)*(r2 - r1)/((rp - r2)*(ra - r1))
    C_cl = 4.0/((rp - r2)*(ra - r1))
    scale = -(E*E - 1.0)
    if m_cl >= 1.0 - 1e-12 or C_cl <= 0 or scale <= 0:
        return float("nan"), m_cl
    return 2.0*np.sqrt(C_cl/scale)*Kc(m_cl), m_cl
def census():
    rows = []
    for a in (0.1, 0.2, 0.3, 0.6, 0.9, 0.998):
        for p in (6.5, 6.8, 7.5, 8.0, 10.0, 12.0, 20.0):
            for e in (0.1, 0.3, 0.5, 0.7, 0.9):
                for th in (30.0, 60.0, 85.0):
                    rows.append((a, p, e, th))
    tally = {}
    ob_rows = []
    lam_handled_max = 0.0
    for (a, p, e, th) in rows:
        try:
            E, Lz, Q, z = orig.solve_ELQ(a, p, e, th, False)
        except Exception:
            tally["solve-fail"] = tally.get("solve-fail", 0) + 1
            continue
        rp, ra = p/(1+e), p/(1-e)
        real, below, roots = _quartic_real_below(a, E, Lz, Q, rp, 1e-7)
        nreal = len(real)
        case = f"{nreal}real/{len(below)}below"
        tally[case] = tally.get(case, 0) + 1
        if len(below) == 2 and nreal == 4:
            lam, _ = _lam_r_fast(a, E, Lz, Q, rp, ra, below[0], below[1])
            if np.isfinite(lam):
                lam_handled_max = max(lam_handled_max, lam)
        else:
            inband = [r for r in real if rp + 1e-7 < r < ra - 1e-7]
            rsign = float(np.sign(orig.Rpot(rp + 1e-6, a, E, Lz, Q)))
            ob_rows.append(dict(a=a, p=p, e=e, th=th, case=case,
                                nreal=nreal, nbelow=len(below),
                                inband=len(inband),
                                inband_r=inband[-1] if inband else float("nan"),
                                rsign=rsign))
    n = len(rows)
    print(f"== census: {n} rows, solve-fails {tally.get('solve-fail', 0)}")
    for c, k in sorted(tally.items(), key=lambda kv: -kv[1]):
        print(f"   {c:16s} {k:4d}  ({100.0*k/n:.1f}%)")
    if ob_rows:
        print("   rows NOT 4real/2below (mechanism):")
        for r in ob_rows:
            ib = f" at r={r['inband_r']:.4f}" if r["inband"] else ""
            print(f"     a={r['a']} p={r['p']} e={r['e']} th={r['th']}: "
                  f"{r['case']}, extra-roots-in-band={r['inband']}{ib}, "
                  f"sign(R(rp+eps))={r['rsign']:+.0f}")
    print(f"   max Lam_r over handled 4real/2below rows: {lam_handled_max:.3f}")
    return tally, ob_rows

def lt_control():
    """Weak-field frame-dragging control on the port itself (the checker's
    anchor): |Om_phi - Om_th| per azimuthal revolution vs Lense-Thirring
    4*pi*a/p^1.5. Sign convention: my Om_th counts u's libration positive, so
    the difference prints positive while the physical node regresses."""
    a, p = 0.2, 30.0
    lt = 4*np.pi*a/p**1.5
    for (e, th) in ((0.1, 45.0), (0.1, 75.0), (0.3, 45.0)):
        E, Lz, Q, z = orig.solve_ELQ(a, p, e, th, False)
        cf = cf_pure(a, E, Lz, Q, r_hint=p/(1+e), z=z)
        Om_phi = cf["dPhi_r"]/cf["Lam_r"] + cf["dPhi_th"]/cf["Lam_th"]
        Om_th = 2*np.pi/cf["Lam_th"]
        nodal = abs(Om_phi - Om_th)*2*np.pi/Om_phi   # per azimuthal revolution
        print(f"   a={a} p={p} e={e} th={th}: |Om_phi-Om_th|/orbit={nodal:.4e} "
              f"vs LT={lt:.4e} ratio={nodal/lt:.3f}")
GRID = orig.GRID; CONTROL = orig.CONTROL; DEGEN = orig.DEGEN; HELDOUT = orig.HELDOUT

def one_row(row):
    a, p, e, th, retro, tag = row
    E, Lz, Q, z = orig.solve_ELQ(a, p, e, th, retro)
    hint = p/(1+e)
    for k in KCNT: KCNT[k] = 0
    cf = cf_pure(a, E, Lz, Q, r_hint=hint, z=z)
    counts = dict(KCNT)
    qd = orig.qd_arm(a, E, Lz, Q, r_hint=hint, z=z)
    cfo = orig.cf_arm(a, E, Lz, Q, r_hint=hint, z=z)
    print(f"[{tag}]  E={E:.12f} Lz={Lz:.10f} Q={Q:.10f} case={cf.get('_case')}")
    worst_qd = worst_or = 0.0
    for k in NAMES:
        q_, c_, o_ = qd[k], cf[k], cfo[k]
        dq = abs(c_ - q_)/max(abs(q_), 1e-30) if np.isfinite(c_) else float("nan")
        do = abs(c_ - o_)/max(abs(o_), 1e-30) if np.isfinite(c_) and np.isfinite(o_) else float("nan")
        worst_qd = max(worst_qd, dq); worst_or = max(worst_or, do)
        print(f"   {k:8s} PURE={c_:20.13f} QD={q_:20.13f} ORIG={o_:20.13f}"
              f" |PURE-QD|={dq:9.2e} |PURE-ORIG|={do:9.2e}")
    print(f"   worst |PURE-QD|={worst_qd:.2e}  |PURE-ORIG|={worst_or:.2e}  "
          f"kernels: rf={counts['rf']} rd={counts['rd']} rj={counts['rj']} "
          f"total={counts['rf']+counts['rd']+counts['rj']}")
    return worst_qd, worst_or, counts

def price(counts_list):
    RF_NS, RD_NS, RJ_NS = 50.0, 78.0, 152.0   # de99's measured prices
    rf = max(c["rf"] for c in counts_list); rd = max(c["rd"] for c in counts_list)
    rj = max(c["rj"] for c in counts_list)
    # measured shared count: distinct kernel calls PER KEY (memo reset per row)
    global MEMO
    srf = srd = srj = 0
    for row in (GRID + CONTROL + DEGEN + HELDOUT):
        a, p, e, th, retro, _ = row
        try:
            E, Lz, Q, z = orig.solve_ELQ(a, p, e, th, retro)
            MEMO = {}
            cf_pure(a, E, Lz, Q, r_hint=p/(1+e), z=z)
            srf = max(srf, sum(1 for k in MEMO if k[0] == "rf"))
            srd = max(srd, sum(1 for k in MEMO if k[0] == "rd"))
            srj = max(srj, sum(1 for k in MEMO if k[0] == "rj"))
        except Exception:
            pass
    MEMO = None
    us_raw = (rf*RF_NS + rd*RD_NS + rj*RJ_NS)/1000.0
    us_sh = (srf*RF_NS + srd*RD_NS + srj*RJ_NS)/1000.0
    print(f"\n== price at de99 kernel ns (rf {RF_NS:.0f}/rd {RD_NS:.0f}/rj {RJ_NS:.0f}):")
    print(f"   per six-constant key, raw: rf x{rf} + rd x{rd} + rj x{rj} = {us_raw:.2f} us")
    print(f"   per key, memoized distinct kernels (worst key): rf x{srf} + rd x{srd} "
          f"+ rj x{srj} = {us_sh:.2f} us   <-- the adoption number")
    print("   anchors: shipped belt compile 4.4 us p50 (c4d3); plane mix 5-256 us "
          "p50 76 (cd6e); rebind floor ~6 us (a765); lean read ~4 us (de99)")
    return us_raw, us_sh

def timing():
    a, p, e, th, retro, _ = GRID[0]
    E, Lz, Q, z = orig.solve_ELQ(a, p, e, th, retro)
    rp, ra = orig.band_roots(a, E, Lz, Q, p/(1+e))
    n = 3000
    t0 = time.perf_counter()
    for _ in range(n):
        cf_pure(a, E, Lz, Q, z=z, band=(rp, ra))
    t = (time.perf_counter()-t0)/n*1e6
    print(f"\n== timing (python, orders of magnitude only; band scan excluded -- "
          f"the engine receives rp,ra from the quartic solver): six-constant "
          f"pure-float compile {t:.2f} us/key")

def main():
    census_only = "--censusonly" in sys.argv
    selftest()
    if census_only:
        census(); return
    allrows = GRID + CONTROL + DEGEN + HELDOUT
    w_qd = w_or = 0.0
    counts_list = []
    for row in allrows:
        dq, do, cnt = one_row(row)
        w_qd = max(w_qd, dq); w_or = max(w_or, do); counts_list.append(cnt)
    print(f"\n== WORST over {len(allrows)} rows x 6 constants: "
          f"|PURE-QD|={w_qd:.2e}  |PURE-ORIG|={w_or:.2e}")
    price(counts_list)
    timing()
    print("\n== root-case census ==")
    census()
    print("\n== Lense-Thirring control (weak field, p=30) ==")
    lt_control()

if __name__ == "__main__":
    main()
