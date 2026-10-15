"""Calibration (tuning, before predictions): find the L4 tadpole island's extent
per angle on the float oracle, and lay the sticky ensemble in the thin chaotic
band just beyond it (the original run's protocol, transplanted).
"""
import json
import time

import numpy as np

from oracle import TWO_PI, L4, corot_ic, dwell

NANG, NRAD = 24, 56
RMAX = 0.56
SCAN_CAP = 128.0  # periods
BAND_W, BAND_N = 0.03, 8

angles = np.linspace(0.05, TWO_PI - 0.05, NANG)
radii = np.geomspace(0.02, RMAX, NRAD)

qx = L4[0] + np.outer(radii, np.cos(angles)).ravel()
qy = L4[1] + np.outer(radii, np.sin(angles)).ravel()
ics = corot_ic(qx, qy)
t0 = time.time()
d, _ = dwell(ics, SCAN_CAP)
print(f"[scan] {len(ics)} ICs, {time.time()-t0:.1f}s")
D = d.reshape(NRAD, NANG)
reg = D >= SCAN_CAP - 1e-9
r_reg = np.full(NANG, np.nan)
for j in range(NANG):
    col = np.where(reg[:, j])[0]
    if len(col):
        r_reg[j] = radii[col].max()
print("[r_reg per angle]")
for j in range(NANG):
    print(f"  {np.degrees(angles[j]):6.1f}deg  r_reg={r_reg[j]:.4f}" if np.isfinite(r_reg[j]) else
          f"  {np.degrees(angles[j]):6.1f}deg  no regular core")

ok = np.isfinite(r_reg)
print(f"[island] {ok.sum()}/{NANG} angles with a regular core, "
      f"r_reg range {r_reg[ok].min():.3f}..{r_reg[ok].max():.3f}")

bx, by, meta = [], [], []
for j in np.where(ok)[0]:
    for r in np.linspace(r_reg[j] + BAND_W / BAND_N, r_reg[j] + BAND_W, BAND_N):
        bx.append(L4[0] + r * np.cos(angles[j]))
        by.append(L4[1] + r * np.sin(angles[j]))
        meta.append({"angle_deg": float(np.degrees(angles[j])), "r": float(r)})
bx, by = np.array(bx), np.array(by)
ens = corot_ic(bx, by)
json.dump({"ics": ens.tolist(), "meta": meta,
           "r_reg": r_reg.tolist(), "angles_deg": np.degrees(angles).tolist(),
           "scan_cap": SCAN_CAP},
          open("ensemble.json", "w"))
print(f"[ensemble] {len(bx)} ICs written to ensemble.json")
