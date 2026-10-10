#!/usr/bin/env python3
"""Sorted-microstate floor of the belt (any exact encoding of a generic state),
from the state saved by hlive.py. Convergence across coarse-grain B is the
uncapped-entropy check (values must agree across B once B is fine enough that
occupancy per cell > 1)."""
import numpy as np

d = np.load("final_state.npz")
N = len(d["a"])
Q_A = 2 * 1.2**2 / (6 * 2**32)
qe = (np.sqrt(1.5) - np.sqrt(0.75)) / 2**32 / np.sqrt(1.2)  # L-quantum in e-units

def ent2(x, y, B):
    kx = np.round(x / (qe * B)).astype(np.int64)
    ky = np.round(y / (qe * B)).astype(np.int64)
    _, c = np.unique(kx * (1 << 26) + ky, return_counts=True)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum() + 2 * np.log2(B))

h, _ = np.histogram(d["a0"], bins=1 << 10, range=(1.0, 1.5))
p = h.astype(float); p = p[p > 0] / p.sum()
H_a = float(-(p * np.log2(p)).sum() + np.log2(0.5 / (1 << 10) / Q_A))  # ~32.1

for tag, ex, ey in [("birth", d["ex0"], d["ey0"]), ("final", d["ex"], d["ey"])]:
    for B in (1 << 20, 1 << 22, 1 << 24, 1 << 26):
        print(f"{tag} B=2^{int(np.log2(B))}: H_e2d = {ent2(ex, ey, B):.1f} bits")
    fl = H_a + ent2(ex, ey, 1 << 24) - np.log2(N) + np.log2(np.e)
    print(f"{tag}: floor = {fl:.1f} bits/body = {fl/8:.2f} GB at 1e9 bodies\n")
