#!/usr/bin/env python3
"""Truth convergence: is the ladder's top cadence (512) converged w.r.t. the
behaviour tolerances? 400-body subset of belt A, 512 vs 1024 kicks/orbit."""
import numpy as np
import cadence as C

s0, a0, e0 = C.make_belt(1024, 2.0, 3.6, 0.05, 11)
s0 = s0[:400]
e512, _ = C.run(s0, 120, 512)
e1024, _ = C.run(s0, 120, 1024)


def scal(e):
    return e.mean(axis=0), e.std(axis=0), e.max(axis=0)


m1, s1, x1 = scal(e512)
m2, s2, x2 = scal(e1024)
d_m = np.abs(m1 - m2) / np.maximum(0.10 * m2, 2e-3)
d_s = np.abs(s1 - s2) / np.maximum(0.15 * s2, 1.5e-3)
d_x = np.abs(x1 - x2) / np.maximum(0.10 * x2, 3e-3)
print("max normalized deviation 512-vs-1024:", d_m.max(), d_s.max(), d_x.max())
print("fraction of bodies with any term > 0.5:", ((d_m > .5) | (d_s > .5) | (d_x > .5)).mean())
np.savez("out_conv.npz", d_m=d_m, d_s=d_s, d_x=d_x)
