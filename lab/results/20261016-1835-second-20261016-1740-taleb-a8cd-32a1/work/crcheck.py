#!/usr/bin/env python3
"""CR-check (mpmath) of glibc's sin/cos/powf on the exact handoff seed values where the
census found glibc != musl (candidates 70, 83, 88, 106, 138), replicating xtask's
splitmix64 draws and the scene arithmetic bit for bit."""
import math, struct
import mpmath as mp

mp.mp.dps = 80
MASK = (1 << 64) - 1

class Rng:
    def __init__(self, s): self.s = s & MASK
    def next(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & MASK
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return z ^ (z >> 31)
    def unit(self):
        return (self.next() >> 11) / float(1 << 53)

def handoffs(n):
    rng = Rng(20261002)
    out = []
    for _ in range(n):
        side = 1.0 if (rng.next() >> 63) == 1 else -1.0
        k = 1.5 + 1.5 * rng.unit()
        alpha = math.radians(30.0 + 300.0 * rng.unit())
        out.append((side, k, alpha))
    return out

sep, mu = 5.27e8, 1e-3
hill = sep * math.cbrt(mu / 3.0)

def cr(x):  # correctly-rounded double of the true value
    return mp.mpf(x)

def ulps(a, b):
    ia, ib = struct.unpack('<q', struct.pack('<d', a))[0], struct.unpack('<q', struct.pack('<d', b))[0]
    return ib - ia

draws = handoffs(160)
for i in [70, 83, 88, 106, 138]:
    side, k, alpha = draws[i]
    r = sep * (1.0 + side * hill / sep * k)
    calls = {
        "sin(a)": (math.sin(alpha), mp.sin(cr(alpha))),
        "cos(a)": (math.cos(alpha), mp.cos(cr(alpha))),
        "pow(r,-.5)": (math.pow(r, -0.5), mp.power(cr(r), mp.mpf(-0.5))),
    }
    parts = []
    for name, (got, true) in calls.items():
        want = mp.mpf(mp.nstr(true, 80))
        want_d = mp.mpf(struct.unpack('<d', struct.pack('<d', float(mp.nint(want * (1 << 53)) / (1 << 53))))[0]) if False else None
        # round the exact value to nearest double:
        f = float(true)
        # recompute precisely: mpmath -> nearest double via mpf->float is round-to-nearest
        d = ulps(got, f)
        parts.append(f"{name}: glibc {d:+d} ulp vs CR")
    print(f"#{i}: r={r!r} alpha={alpha!r} | " + " | ".join(parts))
