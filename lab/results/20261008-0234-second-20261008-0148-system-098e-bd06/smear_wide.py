#!/usr/bin/env python3
"""Full-doll smear, in BOTH units (rebuild of the checker's uncommitted
smear_wide.py): sources in rings 0..30, receivers anywhere to ring 98, every
dspoke including diametric. The author's smear.py sampled only dk in +-5 rings
(r2/r1 <= 1.24), which made 'late by <= ~3.4 SOURCE-cell light-crossings at
every separation' true of the sample and false of the doll. Corrected
invariant candidate: never early; late by <= ~3 LARGER-cell light-crossings,
independent of distance. Cells are convex annular sectors (dtheta < pi), so
the exact max distance is at corners; boundary sampling gives dmin to ~1e-6 r.
"""
import numpy as np

M_RING, N_SPOKE = 16, 128
R0, R1 = 0.7, 50.0
K_MAX = int(np.floor(M_RING * np.log2(R1 / R0)))   # 98

def cell_corners(k, s):
    ra = R0 * 2 ** (k / M_RING); rb = R0 * 2 ** ((k + 1) / M_RING)
    t0 = s * 2 * np.pi / N_SPOKE; t1 = (s + 1) * 2 * np.pi / N_SPOKE
    th = np.linspace(t0, t1, 16)
    pts = [[ra * np.cos(t), ra * np.sin(t)] for t in th]
    pts += [[rb * np.cos(t), rb * np.sin(t)] for t in th]
    for rr in np.linspace(ra, rb, 6):
        pts += [[rr * np.cos(t0), rr * np.sin(t0)], [rr * np.cos(t1), rr * np.sin(t1)]]
    return np.array(pts)

def cw(k):  # radial width of ring k
    return R0 * 2 ** (k / M_RING) * (2 ** (1 / M_RING) - 1)

rng = np.random.default_rng(7)
rows = []
for _ in range(30000):
    k1 = int(rng.integers(0, 31)); k2 = int(rng.integers(0, K_MAX + 1))
    s1 = int(rng.integers(0, N_SPOKE)); ds = int(rng.integers(0, N_SPOKE))
    s2 = (s1 + ds) % N_SPOKE
    p1, p2 = cell_corners(k1, s1), cell_corners(k2, s2)
    d = np.linalg.norm(p1[:, None, :] - p2[None, :, :], axis=2)
    dmin, dmax = float(d.min()), float(d.max())
    if dmin <= 1e-12: continue
    lat = dmax - dmin
    big = cw(max(k1, k2))
    rows.append((dmin / cw(k1), lat / cw(k1), lat / big, lat / dmin))
A = np.array(rows)
print(f"{len(A)} cell pairs, full doll (sources rings 0-30, receivers 0-{K_MAX}, all dspoke)")
src, big, rel = A[:, 1], A[:, 2], A[:, 3]
print(f"lateness in SOURCE-cell crossings:   med {np.median(src):.2f} p90 {np.percentile(src,90):.2f} max {src.max():.1f}")
print(f"lateness in LARGER-cell crossings:   med {np.median(big):.2f} p90 {np.percentile(big,90):.2f} max {big.max():.2f}")
print(f"relative lateness (dmax-dmin)/dmin:  med {np.median(rel):.3f} p90 {np.percentile(rel,90):.3f}")
# the corrected bound vs separation (in larger-cell widths)
print(f"{'sep (larger-cell widths)':>24} {'n':>7} {'src med':>8} {'big med':>8} {'big max':>8}")
for lo, hi in [(0,1),(1,2),(2,3),(3,4),(4,6),(6,8),(8,12),(12,20),(20,60),(60,200),(200,1e9)]:
    m = (A[:, 0] >= lo) & (A[:, 0] < hi)
    if not m.any(): continue
    print(f"{lo:>10}-{hi:<13} {m.sum():>7} {np.median(A[m,1]):>8.2f} {np.median(A[m,2]):>8.2f} {A[m,2].max():>8.2f}")
# same-ring diametric (k1 == k2, opposite spokes): the wide-table caveat
print("same-ring diametric (ds=64): lateness / larger-cell crossings:")
vals = []
for k in range(4, K_MAX, 6):
    p1, p2 = cell_corners(k, 0), cell_corners(k, 64)
    d = np.linalg.norm(p1[:, None, :] - p2[None, :, :], axis=2)
    if d.min() <= 1e-12: continue
    vals.append((d.max() - d.min()) / cw(k))
print(f"  med {np.median(vals):.2f} max {np.max(vals):.2f} over {len(vals)} rings")
