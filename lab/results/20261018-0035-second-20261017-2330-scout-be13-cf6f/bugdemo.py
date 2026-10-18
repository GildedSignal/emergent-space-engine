#!/usr/bin/env python3
"""Demonstrate that control C2 (cell-count equality) catches be13's bug 3
mechanically: reproduce the SHIPPED bugged com_program binning (radial extent
hi = gal.R_MAX instead of np.log(gal.R_MAX)) and show the count mismatch it
created, which the shipped record carried silently (confirm.out.be13:
geom 221937 vs COM 148599 cells at 256x1024)."""
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location("gal", "galprogram.py")
gal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gal)

N = 1_000_000
n_r, n_phi = 256, 1024
xy = gal.sample_smooth(N, gal.RNG_SEED + N)
mass = 1.0 / N
r = np.hypot(xy[:, 0], xy[:, 1])
lr = np.log(np.clip(r, 1e-6, None))
ip = ((np.arctan2(xy[:, 1], xy[:, 0]) % (2 * np.pi)) / (2 * np.pi) * n_phi).astype(int)

lo = np.log(0.02)
for tag, hi in [("SHIPPED (bug: hi=R_MAX)", gal.R_MAX), ("FIXED    (hi=log R_MAX)", np.log(gal.R_MAX))]:
    ir = ((lr - lo) / (hi - lo) * n_r).astype(int)
    ok = ir < n_r
    used = len(set(np.maximum(ir, 0)[ok] * n_phi + ip[ok]))
    print(f"{tag}: extent={hi:.4f} log-width={hi-lo:.4f} cells_used={used}")
print("C2 (assert g_used == c_used) fires on the shipped row; be13 shipped it silently.")
