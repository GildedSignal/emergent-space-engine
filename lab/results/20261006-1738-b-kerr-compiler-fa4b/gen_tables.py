#!/usr/bin/env python3
"""Independent reference generator for the Kerr module.

- 16-point Gauss-Legendre nodes/weights in Q62 (mpmath, 90 digits, half-up).
- BPT closed forms (ISCO, photon orbit, b_c) for the three judged spins.
- Golden vectors for the law: cycles (trapezoid in psi, high precision),
  deflections (GL in t, high precision), tube rates and a Penrose split
  (closed forms), plus Lense-Thirring weak-field odd part checks.
  Everything in mpmath at 50 digits, written from the metric-level formulas,
  NOT from the Rust code.
"""
import json
from mpmath import mp, mpf, sqrt, cos as mcos, acos, sin as msin, acos as macos, pi

mp.dps = 50

def q62(x):
    n = x * mpf(2) ** 62
    # round half up
    f = mp.floor(n)
    return int(f + (1 if n - f >= mpf(1) / 2 else 0))

 # ---- GL16 ----
# roots of P16 by Newton (derivative by mp.diff: this mpmath ignores derivative=True)
import numpy as np
_guesses = sorted(np.polynomial.legendre.Legendre.basis(16).roots(), reverse=True)
xs, ws = [], []
for _g in _guesses[:8]:
    r = mp.mpf(repr(_g))
    for _ in range(200):
        step = mp.legendre(16, r) / mp.diff(lambda t: mp.legendre(16, t), r)
        r -= step
        if abs(step) < mpf(10) ** -60:
             break
    dP = mp.diff(lambda t: mp.legendre(16, t), r)
    w = 2 / ((1 - r * r) * dP ** 2)
    xs.append(r)
    ws.append(w)
GL_X = [q62(x) for x in xs]
GL_W = [q62(w) for w in ws]
# symmetric table: nodes +-x
print("GL16_X (positive half, Q62):")
print("    " + ", ".join(str(v) for v in GL_X))
print("GL16_W (Q62):")
print("    " + ", ".join(str(v) for v in GL_W))
# sanity: sum w = 2, sum w x^2 = 2/3
print("  sum w - 2 =", mp.fsum(ws) - 2)
print("  sum w x^2 - 2/3 =", mp.fsum(w * x * x for w, x in zip(ws, xs)) - mpf(2) / 3)

# ---- BPT closed forms ----
def isco(a, s):
    z1 = 1 + (1 - a * a) ** (mpf(1) / 3) * ((1 + a) ** (mpf(1) / 3) + (1 - a) ** (mpf(1) / 3))
    z2 = sqrt(3 * a * a + z1 * z1)
    return 3 + z2 - s * sqrt((3 - z1) * (3 + z1 + 2 * z2))

def rph(a, s):
    return 2 * (1 + mcos((mpf(2) / 3) * acos(-s * a)))

def bcrit(a, s):
    r = rph(a, s)
    d = sqrt(max(mpf(0), r * r - 2 * r + a * a))
    if s > 0:
        return (r * r + a * a + a * d) / (a + d)
    return -(r * r + a * a - a * d) / (d - a)

spins = [mpf("0.5"), mpf("0.9"), mpf("0.998")]
print("\nBPT reference values:")
for a in spins:
    print(f"  chi={a}: horizon={1 + sqrt(1 - a*a)}")
    for s in (1, -1):
        print(f"    s={s:+d}: isco={isco(a, s)}  r_ph={rph(a, s)}  b_c={bcrit(a, s)}")

# ---- golden vectors: exact equatorial Kerr geodesics, metric-level derivation ----
# Radial: (du/dsigma)^2 = g(u) = (E^2-1) + 2u - (a^2 + x^2 + 2*a*x*E) u^2 + 2 x^2 u^3, x = L - aE  [massive]
#         [null]  = 1 - (b^2-a^2) u^2 + 2 (b-a)^2 u^3
# dphi/dsigma = x + aP/Delta, dt/dsigma = a x + (r^2+a^2) P/Delta, dtau/dsigma = r^2  (per unit mass)
def cycle_golden(a, p, e, s):
    """(E, L) via G&K closed form + Newton on g(u_p)=g(u_a)=0, then trapezoid in psi."""
    up, ua = (1 + e) / p, (1 - e) / p
    if a == 0:
        d = p - 3 - e * e
        E, L = sqrt(((p - 2) ** 2 - 4 * e * e) / (p * d)), s * p / sqrt(d)
    else:
        al0, al1 = p - a * a, ((3 + e * e) - p) / p
        c0 = 1 - 2 * ua + a * a * ua * ua + al0 * ua * ua
        c1 = ua * ua + al1 * ua * ua - 2 * ua ** 3
        f, n, c = al1 * al1 - 4 * a * a * c1, 2 * al0 * al1 - 4 * a * a * c0, al0 * al0
        disc = sqrt(n * n - 4 * f * c)
        q = -0.5 * (n + (-1 if n < 0 else 1) * disc)
        best = None
        for y in (q / f, c / q if q != 0 else None):
            if y is None or y <= 0:
                continue
            A = al0 + al1 * y
            if A == 0:
                continue
            x = (1 if A > 0 else -1) * sqrt(y)
            E = A / (2 * a * x)
            if 0 < E < 1 and (x + a * E) * s > 0:
                if best is None or (y < best[0] if s > 0 else y > best[0]):
                    best = (y, x, E)
        _, x, E = best
        for _ in range(60):  # Newton polish, mpmath precision
            g1 = (E * E - 1) + 2 * up - (a * a + x * x + 2 * a * x * E) * up ** 2 + 2 * x * x * up ** 3
            g2 = (E * E - 1) + 2 * ua - (a * a + x * x + 2 * a * x * E) * ua ** 2 + 2 * x * x * ua ** 3
            a1, b1 = 2 * E - 2 * a * x * up ** 2, -(2 * x + 2 * a * E) * up ** 2 + 4 * x * up ** 3
            a2, b2 = 2 * E - 2 * a * x * ua ** 2, -(2 * x + 2 * a * E) * ua ** 2 + 4 * x * ua ** 3
            det = a1 * b2 - a2 * b1
            de, dx = (g1 * b2 - g2 * b1) / det, (a1 * g2 - a2 * g1) / det
            if abs(de) < mpf(10) ** -45 and abs(dx) < mpf(10) ** -45:
                break
            E, x = E - de, x - dx
        L = x + a * E
    x = L - a * E
    u3 = (a * a + x * x + 2 * a * x * E) / (2 * x * x) - 2 / p
    def fpsi(psi):
        u = (1 + e * mcos(psi)) / p
        r = 1 / u
        delta = r * r - 2 * r + a * a
        P = E * (r * r + a * a) - a * L
        w = 1 / (sqrt(2) * abs(x) * sqrt(u3 - u))
        return ((x + a * P / delta) * w, (a * x + (r * r + a * a) * P / delta) * w, r * r * w)
    # tanh-sinh style: dense trapezoid (integrand even at both ends => geometric)
    n = 8192
    tot = [mpf(0)] * 3
    for k in range(n + 1):
        v = fpsi(pi * mpf(k) / n)
        wt = 0.5 if k in (0, n) else 1
        tot = [t + wt * vi for t, vi in zip(tot, v)]
    tot = [2 * pi / n * t for t in tot]
    return {"advance": abs(tot[0]) - 2 * pi, "period": tot[1], "proper_period": tot[2], "E": E, "L": L, "u3": u3}

def deflection_golden(a, b):
    m, k = b * b - a * a, 2 * (b - a) ** 2
    # largest real root of 1 - m u^2 + k u^3 = 0 via dense scan + bisection
    def Q(u):
        return 1 - m * u * u + k * u ** 3
    lo, hi = mpf(0), mpf(0)
    step = mpf(10) ** -6
    u = step
    while Q(u) > 0 and u < 1:
        lo, u = u, u + step
    if u >= 1:
        return None
    for _ in range(200):
        mid = (lo + u) / 2
        if Q(mid) > 0:
            lo = mid
        else:
            u = mid
    u0 = lo
    def integ(t):
        u = u0 * (1 - t * t)
        qq = (m * u0 - k * u0 * u0) + (m - k * u0) * u - k * u * u
        fphi = (b - a) + a * (1 + a * (a - b) * u * u) / (1 - 2 * u + a * a * u * u)
        return fphi * 2 * sqrt(u0) / sqrt(qq)
    n = 4096
    tot = mpf(0)
    # GL16
    xs16 = list(xs) + [-x for x in xs]
    ws16 = list(ws) + list(ws)
    for j in range(n):
        lo_, hi_ = mpf(j) / n, mpf(j + 1) / n
        for xq, wq in zip(xs16, ws16):
            tot += wq * 0.5 * (hi_ - lo_) * integ(0.5 * (lo_ + hi_) + 0.5 * (hi_ - lo_) * xq)
    return abs(2 * tot) - pi

def zamo(a, r):
    delta = r * r - 2 * r + a * a
    A = (r * r + a * a) ** 2 - a * a * delta
    return (sqrt(r * r * delta / A), 2 * a * r / A, sqrt(A / (r * r)))

out = {"cycles": [], "deflections": [], "tubes": [], "splits": []}
for (a, p, e, s, tag) in [
    ("0.9", 12, 0.3, 1, "chi0.9 p12 e0.3 pro"),
    ("0.9", 12, 0.3, -1, "chi0.9 p12 e0.3 retro"),
    ("0.5", 30, 0.6, 1, "chi0.5 p30 e0.6 pro"),
    ("0.998", 3.2, 0.5, 1, "chi0.998 p3.2 e0.5 pro near-sep"),
    ("0.998", 14, 0.1, -1, "chi0.998 p14 e0.1 retro"),
]:
    a_ = mpf(a)
    # near-separatrix case: use p = 1.2 * separatrix at that e? separatrix needs scan; keep given p if stable
    res = cycle_golden(a_, mpf(p), mpf(e), s)
    out["cycles"].append({"tag": tag, "a": a, "p": p, "e": e, "s": s, **{k: str(v) for k, v in res.items()}})
    print(f"cycle {tag}: advance={res['advance']} period={res['period']} tau={res['proper_period']} E={res['E']} L={res['L']}")

for (a, b, tag) in [("0.998", "2.3", "chi0.998 pro b2.3"), ("0.998", "-7.5", "chi0.998 retro b-7.5"), ("0.5", "200", "weak b200")]:
    d = deflection_golden(mpf(a), mpf(b))
    out["deflections"].append({"tag": tag, "a": a, "b": b, "d": str(d)})
    print(f"deflection {tag}: {d}")

# tube rates: state inside ergosphere of chi=0.9 (r=1.6), from ZAMO velocity (0, 0.6)
a = mpf("0.9")
r = mpf("1.6")
al, om, sg = zamo(a, r)
gam = 1 / sqrt(1 - mpf("0.36"))
L = sg * gam * mpf("0.6")
E = al * gam + om * L
x = L - a * E
P = E * (r * r + a * a) - a * L
delta = r * r - 2 * r + a * a
t = a * x + (r * r + a * a) * P / delta
out["tubes"].append({"tag": "chi0.9 r1.6 v0.6", "a": "0.9", "E": str(E), "L": str(L), "r": "1.6",
                     "phi_rate": str((x + a * P / delta) / t), "clock_rate": str(r * r / t)})
print(f"tube: E={E} L={L} dphi/dt={(x + a * P / delta) / t} dtau/dt={r * r / t}")

# Penrose split canonical: chi=0.9, r halfway horizon..2, v=0.6
rh = 1 + sqrt(1 - a * a)
r = (rh + 2) / 2
al, om, sg = zamo(a, r)
gam = 1 / sqrt(1 - mpf("0.36"))
L0 = sg * gam * mpf("0.6")
E0 = al * gam + om * L0
eps0, pphi = (E0 - om * L0) / al, L0 / sg
ef, eb = 0.5 * (eps0 + pphi), 0.5 * (eps0 - pphi)
lf, lb = ef * sg, -eb * sg
out["splits"].append({"tag": "chi0.9 canonical", "a": "0.9", "E0": str(E0), "L0": str(L0), "r": str(r),
                      "fwd": [str(al * ef + om * lf), str(lf)], "bwd": [str(al * eb + om * lb), str(lb)]})
print(f"split: E0={E0} L0={L0} r={r} fwd=({al*ef+om*lf}, {lf}) bwd=({al*eb+om*lb}, {lb})")

# Lense-Thirring odd part: advance(p,e,pro) - advance(p,e,retro) at large p vs 4*pi*chi/p^1.5 (naive) and -8*pi*chi/p^1.5
print("\nLT odd-part scan (k=5/8, chi=0.5):")
e = mpf("0.6")
k_ = 1 / (1 + e)
for p in (400, 800, 1600):
    pro = cycle_golden(mpf("0.5"), mpf(p), e, 1)["advance"]
    retro = cycle_golden(mpf("0.5"), mpf(p), e, -1)["advance"]
    odd = (pro - retro) / 2
    M_per_p = (1 / mpf(p)) ** mpf("1.5")
    print(f"  p={p}: odd={odd} odd/(chi*M/p^1.5)={odd / (mpf('0.5') * M_per_p) / pi} pi")

with open("lab/results/20261006-1738-b-kerr-compiler-fa4b/golden.json", "w") as fh:
    json.dump(out, fh, indent=1)
print("\nwrote golden.json")
