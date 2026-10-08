#!/usr/bin/env python3
"""Smear geometry of the ring lattice's light cone (rings m=16, N=128 spokes).

For pairs of cells of the doll's lattice (r0*2^(k/16) rings, 128 spokes over
0.7-50 AU), the causality-safe lag is max-distance/c and the exact lag is the
true point-pair distance; both lie between min-distance and max-distance
between the two cells. The SMEAR (max-min) is the timing quantization error a
cell-owned lag table accepts. Output: relative smear vs separation in cell
widths, and the lag error in cell light-crossings.
"""
import numpy as np

M_RING, N_SPOKE = 16, 128
R0, R1 = 0.7, 50.0
K_MAX = int(np.floor(M_RING * np.log2(R1 / R0)))
print(f"rings k=0..{K_MAX} ({K_MAX+1} rings), {N_SPOKE} spokes, "
      f"{(K_MAX+1)*N_SPOKE} cells")

def cell_corners(k, s):
    ra = R0 * 2 ** (k / M_RING); rb = R0 * 2 ** ((k + 1) / M_RING)
    t0 = s * 2 * np.pi / N_SPOKE; t1 = (s + 1) * 2 * np.pi / N_SPOKE
    th = np.linspace(t0, t1, 16)
    pts = [[ra * np.cos(t), ra * np.sin(t)] for t in th]
    pts += [[rb * np.cos(t), rb * np.sin(t)] for t in th]
    for rr in np.linspace(ra, rb, 6):
        pts += [[rr * np.cos(t0), rr * np.sin(t0)], [rr * np.cos(t1), rr * np.sin(t1)]]
    return np.array(pts)

rng = np.random.default_rng(11)
rows = []
for _ in range(240):
    k1 = int(rng.integers(20, K_MAX - 20))
    s1 = int(rng.integers(0, N_SPOKE))
    p1 = cell_corners(k1, s1)
    r_lo, r_hi = R0 * 2 ** (k1 / M_RING), R0 * 2 ** ((k1 + 1) / M_RING)
    cw = r_hi - r_lo                      # radial width of the source cell
    for dk in (-5, -3, -2, -1, 0, 1, 2, 3, 5):
        k2 = k1 + dk
        if not (0 <= k2 <= K_MAX): continue
        # spoke differences that keep separation in a few cell widths
        for dsf in (0, 1, 2, 3, 5, 8, 13, 21):
            for sgn in (1, -1):
                s2 = (s1 + sgn * dsf) % N_SPOKE
                p2 = cell_corners(k2, s2)
                d = np.linalg.norm(p1[:, None, :] - p2[None, :, :], axis=2)
                dmin, dmax = d.min(), d.max()
                if dmin <= 1e-12: continue          # touching cells
                rows.append((dmin / cw, (dmax - dmin) / dmin, (dmax - dmin) / cw))
A = np.array(rows)
print(f"{len(A)} cell pairs sampled")
print("Invariants: lateness = (dmax-dmin)/c with the never-early rule; "
      "in units of the SOURCE cell's light-crossing (cw/c).")
print(f"absolute lateness (source-cell light-crossings): med {np.median(A[:,2]):.2f} "
      f"p90 {np.percentile(A[:,2],90):.2f} max {A[:,2].max():.2f}")
print(f"relative lateness ((dmax-dmin)/dmin) vs separation s (cell widths): "
      f"fits ~2/s")
# bin by separation in cell widths
bins = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 6), (6, 8), (8, 12), (12, 20), (20, 60)]
print(f"{'sep (cell widths)':>18} {'n':>6} {'rel med':>8} {'rel p90':>8} {'abs(cw) med':>12}")
for lo, hi in bins:
    m = (A[:, 0] >= lo) & (A[:, 0] < hi)
    if not m.any(): continue
    rel = A[m, 1]
    print(f"{lo:>7}-{hi:<10} {m.sum():>6} {np.median(rel):>8.3f} "
          f"{np.percentile(rel, 90):>8.3f} {np.median(A[m,2]):>12.2f}")
