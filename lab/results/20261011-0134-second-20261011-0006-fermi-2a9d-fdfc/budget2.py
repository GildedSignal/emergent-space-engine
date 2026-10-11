#!/usr/bin/env python3
"""The corrected 10^9 memory accounting (the checker's apples-to-oranges fix).

Both sides entropy-coded or both record-format, three encounter laws (G/T1/T2 from
totals.py), 3 walking element columns, M1 8 GB. Constants fit from totals.json over
t in [1024, 8192]: H(t) = slope*log2(t) + C (slope measured, not assumed 1/2).

Run: python3 budget2.py    (< 1 s, needs totals.json)
"""
import json
import numpy as np

N9 = 1e9
GB = lambda bits: bits * N9 / 8 / 1e9

d = json.load(open("totals.json"))
fits = {}
for run in d["runs"]:
    tt = np.array([p["t"] for p in run["points"] if p["t"] >= 1024], dtype=float)
    ff = np.array([p["frozen_scar_bits"] for p in run["points"] if p["t"] >= 1024])
    ll = np.array([p["label_perm_bits"] for p in run["points"] if p["t"] >= 1024])
    A = np.vstack([np.log2(tt), np.ones_like(tt)]).T
    (sl_f, C_f), *_ = np.linalg.lstsq(A, ff, rcond=None)
    (sl_l, C_l), *_ = np.linalg.lstsq(A, ll, rcond=None)
    last = run["points"][-1]
    fits[run["law"]] = dict(slope_f=sl_f, C_f=C_f, slope_l=sl_l, C_l=C_l,
                            frozen8192=last["frozen_scar_bits"],
                            label8192=last["label_perm_bits"],
                            floor9=3 * last["resid_262144_bits"] + 3 * 32 * 262144 / 2**30,
                            noRelabel9=3 * (last["resid_star_bits"] + last["label_perm_bits"]
                                            + last["prog_bits"][str(last["m_star"])]))
    f = fits[run["law"]]
    f["t_frozen_8GB"] = 2 ** ((64 / 3 - C_f) / sl_f)          # 3 cols reach 64 bits/body
    f["t_label16"] = 2 ** ((16 - C_l) / sl_l)                 # label hits 16 bits/col
print("fits (t in [1024,8192]): law  slope_frozen  C_frozen  slope_label  C_label")
for k, f in fits.items():
    print(f"  {k}: {f['slope_f']:.3f}  {f['C_f']:.2f}   {f['slope_l']:.3f}  {f['C_l']:.2f}")

print("\n-- 10^9 memory, 3 walking columns, t = 8192 orbits --")
rows = [("frozen, 62-bit record format (law.md line 13)", 3 * 62, "breaks at t=0 (the format)")]
for k in ("G", "T1", "T2"):
    rows.append((f"frozen, entropy-coded, law {k} (measured)",
                 3 * fits[k]["frozen8192"], ""))
for k in ("G", "T1", "T2"):
    rows.append((f"re-fit, NO relabelling, law {k} (resid*+label, measured)",
                 fits[k]["noRelabel9"], ">= frozen: refit alone bounds nothing"))
for k in ("G", "T1", "T2"):
    rows.append((f"re-fit + canonical relabelling, law {k} (resid@2.6e5 knots, prog free)",
                 fits[k]["floor9"], "flat in t: the adoptable floor"))
for name, bits, note in rows:
    v = GB(bits)
    print(f"  {name:60s} {bits:6.2f} b/body -> {v:5.2f} GB  "
          f"{'BREAKS' if v > 8 else 'fits':6s} {note}")

print("\n-- deadlines (fits above, 3 columns) --")
for k in ("G", "T1", "T2"):
    f = fits[k]
    print(f"  law {k}: entropy-coded frozen breaks 8 GB at t = {f['t_frozen_8GB']:.2e} orbits;"
          f"  label law deadline (16 b/col) at t = {f['t_label16']:.2e} orbits")
