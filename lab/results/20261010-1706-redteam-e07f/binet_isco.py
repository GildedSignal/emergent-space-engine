#!/usr/bin/env python3
"""Falsifier: does the Binet band quantization misplace the ISCO?

Design premise (docs/representation.md §1, rung r1): inside band k the orbit obeys
u" + (1 - 6*u_k) u = 1/h^2 - 3 u_k^2  ->  stability is the sign of (1 - 6 u_k),
i.e. a property of the BAND. True Schwarzschild: stability is the sign of
(1 - 6 u(r)), a property of the body. M = 1, exact Binet oracle u" + u = 1/h^2 + 3u^2.
"""
import math

M = 1.0

def band_of(r, m, r0=1.0):
    """band index k such that r in [r0*2^(k/m), r0*2^((k+1)/m))"""
    k = math.floor(m * math.log2(r / r0))
    return k

def edges(k, m, r0=1.0):
    lo = r0 * 2.0 ** (k / m)
    hi = r0 * 2.0 ** ((k + 1) / m)
    return lo, hi

def u_centre(k, m, r0=1.0):
    lo, hi = edges(k, m, r0)
    return 1.0 / math.sqrt(lo * hi)          # r1 frozen convention: geometric centre

def u_inner(k, m, r0=1.0):
    lo, _ = edges(k, m, r0)
    return 1.0 / lo                          # inner-edge convention

def band_stable(r, m, conv, r0=1.0):
    k = band_of(r, m, r0)
    uk = u_centre(k, m, r0) if conv == "centre" else u_inner(k, m, r0)
    return 1.0 - 6.0 * M * uk > 0.0

def true_stable(r):
    return 1.0 - 6.0 * M / r > 0.0

def strip(m, conv, r0=1.0, lo=5.0, hi=7.2, n=200000):
    """misclassified [a,b) interval around r=6"""
    bad = [r for i in range(n) for r in (lo + (hi - lo) * i / n,)
           if band_stable(r, m, conv, r0) != true_stable(r)]
    if not bad:
        return None
    return min(bad), max(bad), len(bad) / n * (hi - lo)

# ---------- exact and band Binet integrators (RK4 in phi) ----------
def step(u, up, dphi, acc):
    """one RK4 step of u" = acc(u)"""
    def f(u_, up_):
        return up_, acc(u_)
    a1, b1 = f(u, up)
    a2, b2 = f(u + dphi / 2 * a1, up + dphi / 2 * b1)
    a3, b3 = f(u + dphi / 2 * a2, up + dphi / 2 * b2)
    a4, b4 = f(u + dphi * a3, up + dphi * b3)
    return (u + dphi / 6 * (a1 + 2 * a2 + 2 * a3 + a4),
            up + dphi / 6 * (b1 + 2 * b2 + 2 * b3 + b4))

def run_exact(r0c, eps=1e-3, phimax=250.0, dphi=1e-3):
    uc = 1.0 / r0c
    ih2 = uc * (1 - 3 * M * uc)               # circular: 1/h^2 = u(1-3Mu)
    u, up = uc * (1 + eps), 0.0
    acc = lambda u_: ih2 + 3 * M * u_ * u_ - u_
    n = int(phimax / dphi)
    umin = umax = u
    for _ in range(n):
        u, up = step(u, up, dphi, acc)
        umin, umax = min(umin, u), max(umax, u)
        if u >= 0.5:
            return "plunge", u, umin
    return "bound", umin, umax

def run_band(r0c, m, conv, r0=1.0, eps=1e-3, phimax=250.0, dphi=1e-3):
    uc = 1.0 / r0c
    ih2 = uc * (1 - 3 * M * uc)
    u, up = uc * (1 + eps), 0.0
    umin = umax = u
    n = int(phimax / dphi)
    for _ in range(n):
        k = band_of(1.0 / u, m, r0)
        uk = u_centre(k, m, r0) if conv == "centre" else u_inner(k, m, r0)
        acc = lambda u_, uk=uk: ih2 - 3 * M * uk * uk - (1 - 6 * M * uk) * u_
        u, up = step(u, up, dphi, acc)
        umin, umax = min(umin, u), max(umax, u)
        if u >= 0.5:
            return "plunge", u, umin
    return "bound", umin, umax

print("=== A. ISCO strip: band stability vs true stability (r0=1) ===")
for m in (16, 32, 64):
    for conv in ("centre", "inner-edge"):
        s = strip(m, conv)
        if s:
            a, b, w = s
            print(f"m={m:2d} {conv:11s}: misclassified r in [{a:.4f}, {b:.4f}) "
                  f"width {w:.4f} M = {w/6*100:.2f}% of 6M; "
                  f"effective ISCO {b if conv=='inner-edge' else a:.4f} "
                  f"({'+' if (b if conv=='inner-edge' else a) > 6 else '-'}"
                  f"{abs((b if conv=='inner-edge' else a)-6)/6*100:.2f}%)")
        else:
            print(f"m={m:2d} {conv:11s}: no misclassification")
print()
print("=== B. doll ring phase r0=1.3, m=16, centre ===")
for r0p in (1.0, 1.3):
    s = strip(16, "centre", r0=r0p)
    print(f"r0={r0p}: strip [{s[0]:.4f}, {s[1]:.4f}) width {s[2]:.4f} M "
          f"= {s[2]/6*100:.2f}% of 6M")
print()
print("=== C. exact Binet vs band dynamics (RK4, dphi=1e-3) ===")
for r0c, m, conv in ((5.95, 16, "centre"), (6.05, 16, "inner-edge"),
                     (5.95, 32, "centre")):
    kind, u1, u2 = run_exact(r0c)
    kband, b1, b2 = run_band(r0c, m, conv)
    print(f"r={r0c}: exact->{kind:6s} (u range [{u1:.4f},{u2:.4f}]) | "
          f"band m={m} {conv:11s}->{kband:6s} (u range [{b1:.4f},{b2:.4f}])"
          + ("   <-- DISAGREE" if kind != kband else ""))
print()
print("=== D. r1's frozen ISCO probes are blind ===")
for r0p in (7.0, 5.5):
    tc = band_stable(r0p, 16, "centre")
    te = band_stable(r0p, 16, "inner-edge")
    tt = true_stable(r0p)
    print(f"r={r0p}: true={'stable' if tt else 'unstable'}; "
          f"band(centre)={'stable' if tc else 'unstable'}; "
          f"band(edge)={'stable' if te else 'unstable'}  "
          f"-> isco_correct criterion {'passes' if tc == tt == te else 'FAILS'}")
print()
print("=== E. epicyclic frequency staircase ===")
worst = (0, 0); worstjump = (0, 0, 0)
for i in range(1, 400):
    r = 6.17 + (7.0 - 6.17) * i / 400
    k = band_of(r, 16)
    wk = math.sqrt(max(1 - 6 * u_centre(k, 16), 0))
    wt = math.sqrt(1 - 6 / r)
    if wt > 0 and abs(wk - wt) / wt > worst[0]:
        worst = (abs(wk - wt) / wt, r)
for i in range(1, 400):
    r = 6.0 + (6.6 - 6.0) * i / 400
    k1, k2 = band_of(r - 0.001, 16), band_of(r + 0.001, 16)
    if k1 != k2:
        w1 = math.sqrt(max(1 - 6 * u_centre(k1, 16), 0))
        w2 = math.sqrt(max(1 - 6 * u_centre(k2, 16), 0))
        if w1 > 1e-9 and abs(w2 - w1) / w1 > worstjump[0]:
            worstjump = (abs(w2 - w1) / w1, r, (w1, w2))
print(f"max |w_band-w_true|/w_true over (6.17,7.0): {worst[0]*100:.1f}% at r={worst[1]:.3f}")
print(f"max adjacent-band jump over (6.0,6.6): {worstjump[0]*100:.1f}% at r={worstjump[1]:.3f} "
      f"({worstjump[2][0]:.3f} -> {worstjump[2][1]:.3f})")
print(f"true w_r at 6.05M: {math.sqrt(1-6/6.05):.4f}; first stable band (centre, m=16) "
      f"gives {math.sqrt(1-6*u_centre(band_of(6.17,16),16)):.4f} -- cliff, no smooth ->0")
print()
print("=== F. view at high c: Doppler sweep factor k = 1/(gamma(1-beta)) ===")
for b in (0.5, 0.9, 0.99, 0.999):
    g = 1 / math.sqrt(1 - b * b)
    print(f"beta={b}: k = {1/(g*(1-b)):.1f}")
