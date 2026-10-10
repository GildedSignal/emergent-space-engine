#!/usr/bin/env python3
"""Addendum: plunge timing at r=5.95 (exact Binet), and what the wrongly-unstable
band does to a truly circular orbit at r=6.05 (inner-edge conv): eject upward."""
import math
M = 1.0

def band_of(r, m, r0=1.0):
    return math.floor(m * math.log2(r / r0))
def edges(k, m, r0=1.0):
    return r0 * 2.0 ** (k / m), r0 * 2.0 ** ((k + 1) / m)
def u_centre(k, m, r0=1.0):
    lo, hi = edges(k, m, r0); return 1.0 / math.sqrt(lo * hi)
def u_inner(k, m, r0=1.0):
    lo, _ = edges(k, m, r0); return 1.0 / lo

def step(u, up, dphi, acc):
    a1, b1 = up, acc(u)
    a2, b2 = up + dphi/2*b1, acc(u + dphi/2*a1)
    a3, b3 = up + dphi/2*b2, acc(u + dphi/2*a2)
    a4, b4 = up + dphi*b3, acc(u + dphi*a3)
    return (u + dphi/6*(a1+2*a2+2*a3+a4), up + dphi/6*(b1+2*b2+2*b3+b4))

def run(r0c, eps=1e-3, phimax=400.0, dphi=5e-4, m=None, conv=None):
    uc = 1.0/r0c; ih2 = uc*(1-3*M*uc); u, up = uc*(1+eps), 0.0
    phi = 0.0; n = int(phimax/dphi); umin=umax=u
    for _ in range(n):
        if m is None:
            acc = lambda u_: ih2 + 3*M*u_*u_ - u_
        else:
            k = band_of(1.0/u, m)
            uk = u_centre(k, m) if conv=="centre" else u_inner(k, m)
            acc = lambda u_, uk=uk: ih2 - 3*M*uk*uk - (1-6*M*uk)*u_
        u, up = step(u, up, dphi, acc); phi += dphi
        umin, umax = min(umin,u), max(umax,u)
        if u >= 0.5:
            return f"plunge at phi={phi:.1f} ({phi/(2*math.pi):.1f} orbits)"
    return f"bound to phi={phimax:.0f}; r in [{1/umax:.3f}, {1/umin:.3f}]"

print("r=5.95 exact        :", run(5.95))
print("r=5.95 band m16 ctr :", run(5.95, m=16, conv="centre"))
print("r=5.95 band m32 ctr :", run(5.95, m=32, conv="centre"))
print("r=6.05 exact        :", run(6.05))
print("r=6.05 band m16 edge:", run(6.05, m=16, conv="inner-edge"))
print("r=6.02 band m32 ctr :", run(6.02, m=32, conv="centre"), " (strip [6.0,6.0367))")
print("r=5.98 band m64 ctr :", run(5.98, m=64, conv="centre"), " (strip [5.9716,6.0))")
# per-band wrong-strip summary the m-sweep actually gives
for m in (16, 32, 64, 128):
    k6 = band_of(6.0 - 1e-9, m)
    lo, hi = edges(k6, m)
    print(f"m={m:3d}: band containing 6M = [{lo:.4f}, {hi:.4f}), width {hi-lo:.4f}; "
          f"strip width {abs(6.0-lo):.4f} below / {abs(hi-6.0):.4f} above")
