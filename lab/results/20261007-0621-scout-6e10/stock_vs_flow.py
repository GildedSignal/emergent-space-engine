#!/usr/bin/env python3
"""P4 check: stock vs flow. The same 1% of belt bodies kicked by a fresh chaotic
kick every epoch: their scar (offset from the birth program) must stay bounded
(one state, log-growing spread), not accumulate 40 bits per kick."""
import numpy as np

rng = np.random.default_rng(20261007)
C2PI = 2 * np.pi
N = 1 << 20
QE = 0.6 * 2.0 ** -24

def dh(r, q):
    s = float(np.std(r))
    return 0.0 if s <= 0 else max(0.0, float(np.log2(s * np.sqrt(2 * np.pi * np.e) / q)))

A0, A1 = 2.0, 3.6
a = A0 + (A1 - A0) * rng.random(N)
e0 = 0.1 * np.sqrt(-2 * np.log(1 - rng.random(N)))
w0 = C2PI * rng.random(N)
h0 = e0 * np.cos(w0)
k0 = e0 * np.sin(w0)
hit = rng.random(N) < 0.01
zh, zk = h0.copy(), k0.copy()
for ep in range(1, 25):
    s = 0.03 * (rng.random(N) ** 2 + 0.02)
    zh[hit] += (s * np.cos(C2PI * rng.random(N)))[hit]
    zk[hit] += (s * np.sin(C2PI * rng.random(N)))[hit]
    if ep in (1, 2, 4, 8, 16, 24):
        bits = dh(zh[hit] - h0[hit], QE) + dh(zk[hit] - k0[hit], QE)
        print(f"epoch {ep:2d}: kicks/body={ep:2d}  scar stock={bits:6.2f} bits"
              f"  flow model 62*{ep}={62*ep:5d} bits  overcount={62*ep/bits:6.1f}x")
