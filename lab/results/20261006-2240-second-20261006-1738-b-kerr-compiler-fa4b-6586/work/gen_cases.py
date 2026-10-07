#!/usr/bin/env python3
"""Second-author probe cases: (1) ISCO extremal scan, (2) whirls at the CYCLE_MAX cap.

Truths written from the metric-level radial potential (same source formulas as gen_tables.py,
independent of the Rust module): g(u) = (E^2-1) + 2u - (a^2 + x^2 + 2 a x E) u^2 + 2 x^2 u^3,
x = L - aE; dphi/du = (x + aP/Delta) / (sqrt(2)|x| sqrt((u-u1)(u2-u)(u3-u))) on [u1, u2].
Whirl truth: tanh-sinh in u (mpmath.quad, dps 40, two degrees must agree), NOT the module's
psi-trapezoid. All inputs written as exact f64 reprs (the module grid keeps f64 exactly).
"""
import json
from mpmath import mp, mpf, sqrt, cos as mcos, acos, pi, polyroots, findroot, re, im

mp.dps = 40

def isco_bardeen(a, s):
    z1 = 1 + (1 - a * a) ** (mpf(1) / 3) * ((1 + a) ** (mpf(1) / 3) + (1 - a) ** (mpf(1) / 3))
    z2 = sqrt(3 * a * a + z1 * z1)
    return 3 + z2 - s * sqrt((3 - z1) * (3 + z1 + 2 * z2))

def rph(a, s):
    return 2 * (1 + mcos((mpf(2) / 3) * acos(-s * a)))

def cubic_coeffs(a, E, x):
    return (2 * x * x, -(a * a + x * x + 2 * a * x * E), 2 * mpf(1), E * E - 1)

def roots_u(a, E, x):
    c = cubic_coeffs(a, E, x)
    return list(polyroots([mpf(v) for v in c], maxsteps=200, extraprec=300))

def real_roots_u(a, E, x, tol=25):
    rr = roots_u(a, E, x)
    if len(rr) == 3 and all(abs(im(z)) < mpf(10) ** -tol for z in rr):
        return sorted(re(z) for z in rr)
    return None

def dphi_du(a, E, L, u1, u2, u3):
    x = L - a * E
    def f(u):
        r = 1 / u
        delta = r * r - 2 * r + a * a
        P = E * (r * r + a * a) - a * L
        num = x + a * P / delta
        den = sqrt(2) * abs(x) * sqrt((u - u1) * (u2 - u) * (u3 - u))
        return num / den
    return f

def advance_truth(a, E, L, u1, u2, u3):
    f = dphi_du(a, E, L, u1, u2, u3)
    mid = (u1 + u2) / 2
    i1 = mp.quad(f, [u1, mid, u2], error=False)
    i2 = mp.quad(f, [u1, (3*u1+u2)/4, mid, (u1+3*u2)/4, u2], error=False)
    if abs(i2 - i1) > abs(i2) * mpf(10) ** -28:
        i3 = mp.quad(f, [u1 + (u2-u1)/64, u1, mid, u2, u2 - (u2-u1)/64][::-1], error=False)
        i2 = max(i2, i3, key=abs)
    return 2 * i2 - 2 * pi

# ---- ISCO extremal scan ----------------------------------------------------
isco_cases = []
spins = [mpf("0.5"), mpf("0.9"), mpf("0.998"), mpf("0.999"), mpf("0.9999"),
         1 - mpf(2) ** -30, 1 - mpf(2) ** -52, mpf(1)]
for a in spins:
    isco_cases.append({
        "a": repr(float(a)), "pro": float(isco_bardeen(a, 1)), "retro": float(isco_bardeen(a, -1)),
        "pro_x": mp.nstr(isco_bardeen(a, 1), 25), "retro_x": mp.nstr(isco_bardeen(a, -1), 25),
    })

# ---- Whirls: separatrix-anchored (E, L) ------------------------------------
whirl_cases = []
for a_dec, s in [("0.998", 1), ("0.5", 1)]:
    a = mpf(a_dec)
    r_i, r_p = isco_bardeen(a, s), rph(a, s)
    # unstable circular radius with E_c ~= 0.95 (E crosses 1 between r_ph and r_isco; bound
    # whirls need E < 1, and nearer r_isco the orbit is less relativistic)
    def solve_circ(r_s):
        u_s = 1 / r_s
        def circ(E, x):
            g = (E * E - 1) + 2 * u_s - (a * a + x * x + 2 * a * x * E) * u_s ** 2 + 2 * x * x * u_s ** 3
            gp = 2 - 2 * (a * a + x * x + 2 * a * x * E) * u_s + 6 * x * x * u_s ** 2
            return g, gp
        last = None
        for guess in [(mpf("0.9"), mpf("0.5")), (mpf("0.6"), mpf("0.3")), (mpf("0.97"), mpf("1.2")),
                      (mpf("0.5"), mpf("0.1")), (mpf("0.8"), mpf("2.0"))]:
            try:
                E_c, x_c = findroot(circ, guess, tol=mpf(10) ** -30, maxsteps=60)
            except (ValueError, ZeroDivisionError):
                continue
            if 0 < E_c < 1 and x_c > 0:
                if last is None or E_c < last[0]:  # keep the lowest-energy branch
                    last = (E_c, x_c)
        if last is None:
            raise RuntimeError(f"no circular orbit at r_s={r_s}")
        return u_s, last[0], last[1]
    lo_f, hi_f = mpf("0.01"), mpf("0.99")  # fraction of (r_isco - r_ph); E decreases with f
    for _ in range(80):
        f = (lo_f + hi_f) / 2
        try:
            u_s, E_c, x_c = solve_circ(r_p + f * (r_i - r_p))
        except RuntimeError:  # near r_ph no E<1 circular orbit exists: treat as E > target
            E_c = mpf(2)
        if E_c > mpf("0.95"):
            lo_f = f
        else:
            hi_f = f
    r_s = r_p + hi_f * (r_i - r_p)
    u_s, E_c, x_c = solve_circ(r_s)
    L_c = x_c + a * E_c
    S = (a * a + x_c * x_c + 2 * a * x_c * E_c) / (2 * x_c * x_c)
    assert 0 < S - 2 * u_s < u_s, f"apoapsis root not physical at a={a_dec}"
    # bound side: perturb x, keep 3 real roots with u3 > u2 > u_s region
    side = None
    for sgn in (-1, 1):
        x_t = x_c * (1 + sgn * mpf(2) ** -20)
        E_t, L_t = E_c, x_t + a * E_c
        rr = real_roots_u(a, E_t, x_t)
        if rr is not None and rr[2] > rr[1] > rr[0] > 0:
            side = sgn
            break
    assert side is not None, "no bound side found"
    ks = list(range(8, 60, 4)) if a_dec == "0.998" else [30, 44, 56]
    for k in ks:
        x_k = x_c * (1 + side * mpf(2) ** -k)
        E_k, L_k = E_c, x_k + a * E_c
        Ef, Lf = float(E_k), float(L_k)   # exact f64; module grid keeps f64 exactly
        E_k, L_k, x_k = mpf(repr(Ef)), mpf(repr(Lf)), mpf(repr(Lf)) - a * mpf(repr(Ef))
        rr = real_roots_u(a, E_k, x_k)
        if rr is None:
            whirl_cases.append({"a": a_dec, "k": k, "E": repr(Ef), "L": repr(Lf),
                                "status": "no-3-real-roots", "sep_d": float(abs(L_k - L_c) / abs(L_c))})
            continue
        u1, u2, u3 = rr
        adv = advance_truth(a, E_k, L_k, u1, u2, u3)
        whirl_cases.append({"a": a_dec, "k": k, "E": repr(Ef), "L": repr(Lf), "status": "bound",
                            "u3mu2": float(u3 - u2), "advance": float(adv),
                            "advance_x": mp.nstr(adv, 20), "r_peri": float(1 / u2), "r_apo": float(1 / u1)})
    # exact separatrix point
    Ef, Lf = float(E_c), float(L_c)
    whirl_cases.append({"a": a_dec, "k": 0, "E": repr(Ef), "L": repr(Lf), "status": "separatrix",
                        "sep_d": 0.0, "r_s": float(r_s)})

out = {"isco": isco_cases, "whirl": whirl_cases,
       "meta": {"a_0998": {"E_c": mp.nstr(E_c, 25), "L_c": mp.nstr(L_c, 25), "r_s": mp.nstr(r_s, 25),
                            "side": "L*(1+2^-k)" if side > 0 else "L*(1-2^-k)"} }}
with open("lab/results/20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586/work/cases.json", "w") as fh:
    json.dump(out, fh, indent=1)

# Rust probe body
lines = []
lines.append("// GENERATED by gen_cases.py -- do not edit by hand. Truths: Bardeen BPT; tanh-sinh in u.")
lines.append("use emergent_space::kerr as spin;")
lines.append("use emergent_space::scaled::Scalar;")
lines.append("#[allow(dead_code)] fn q(x: f64) -> Scalar {")
lines.append("    let exponent = x.abs().log2().floor() as i32;")
lines.append("    Scalar::raw((x * 2f64.powi(60 - exponent)).round() as i128, exponent - 60).unwrap()")
lines.append("}")
lines.append("#[allow(dead_code)] fn d(x: Scalar) -> f64 { x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62) }")
lines.append("#[test] fn isco_extremal() {")
lines.append("    let cases: &[(f64, f64, f64)] = &[")
for c in isco_cases:
    lines.append(f"        ({c['a']}, {c['pro']!r}, {c['retro']!r}),")
lines.append("    ];")
lines.append("    for &(a, tpro, tretro) in cases {")
lines.append("        match (spin::isco(q(a), true), spin::isco(q(a), false)) {")
lines.append("            (Ok(mp_), Ok(mr)) => println!(\"ISCO a={a:e} module pro={} retro={} | truth pro={tpro:e} retro={tretro:e} | rel pro={:.3e} retro={:.3e}\",")
lines.append("                d(mp_), d(mr), ((d(mp_)-tpro)/tpro).abs(), ((d(mr)-tretro)/tretro).abs()),")
lines.append("            (r, _) => println!(\"ISCO a={a:e} REFUSED (expected at a>=1): {:?}\", r),")
lines.append("        }")
lines.append("    }")
lines.append("}")
lines.append("#[test] fn whirl_cap() {")
lines.append("    let cases: &[(f64, f64, f64, f64)] = &[ // (a, E, L, truth advance)")
for c in whirl_cases:
    if c["status"] == "bound":
        lines.append(f"        ({c['a']}, {c['E']}, {c['L']}, {c['advance']!r}),")
lines.append("    ];")
lines.append("    for &(a, e, l, t) in cases {")
lines.append("        match spin::cycle(q(a), q(e), q(l)) {")
lines.append("            Ok(c) => println!(\"WHIRL a={a} E={e:e} L={l:e} adv={} rel={:.3e}\", d(c.advance), ((d(c.advance)-t)/t).abs()),")
lines.append("            Err(r) => println!(\"WHIRL a={a} E={e:e} L={l:e} ERR {:?}\", r),")
lines.append("        }")
lines.append("    }")
lines.append("    let edge: &[(f64, f64, f64)] = &[")
for c in whirl_cases:
    if c["status"] == "separatrix":
        lines.append(f"        ({c['a']}, {c['E']}, {c['L']}),")
lines.append("    ];")
lines.append("    for &(a, e, l) in edge {")
lines.append("        match spin::cycle(q(a), q(e), q(l)) {")
lines.append("            Ok(c) => println!(\"SEP a={a} E={e:e} L={l:e} UNEXPECTED OK adv={}\", d(c.advance)),")
lines.append("            Err(r) => println!(\"SEP a={a} E={e:e} L={l:e} Err {:?}\", r),")
lines.append("        }")
lines.append("    }")
lines.append("}")
with open("crates/space/tests/second_probe.rs", "w") as fh:
    fh.write("\n".join(lines) + "\n")
print("cases:", len(isco_cases), "isco,", len(whirl_cases), "whirl")
for c in whirl_cases:
    if c["status"] == "bound":
        print(f"  a={c['a']} k={c['k']:2d} u3-u2={c['u3mu2']:.3e} adv={c['advance_x']}")
    else:
        print(f"  a={c['a']} k={c['k']:2d} {c['status']}")
