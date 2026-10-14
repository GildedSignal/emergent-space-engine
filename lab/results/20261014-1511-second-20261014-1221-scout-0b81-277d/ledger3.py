#!/usr/bin/env python3
"""Restate the ledger: gated = ungated x (surviving + f_r), with f_r from the
measured r_event (bench_r, x86 ns) amortized over true conjunctions per refresh
window, against 1738's composition constants (contiguous+averaged anchors
1.65e3-8.2e3 cores at flying pace, 5.35 us/pair M1-implied, skin-on)."""
import re, sys

import os
R_EVENT_X86_NS = 700.0     # fallback; overridden by the live bench-r.txt when present
try:
    for ln in open(__file__.replace("ledger3.py", "bench-r.txt")):
        if "r_event:" in ln:
            R_EVENT_X86_NS = float(ln.split()[1])
except Exception:
    pass
M1F = 0.597                # 1738's frozen M1 factor
US_PAIR_M1 = 5.35          # 1738's global per-pair cascade cost (M1-implied)
UNGT = (1.65e3, 8.2e3)     # contiguous wide/narrow, averaged, flying pace
K_REFRESH_PER_ORBIT = 0.28 # averaged cadence (H0190/90fb)
E_TRUE = 90.0              # true conjunctions per 10^3-orbit horizon (4AnH/(2pi)^2, A~0.14)
WINDOW_ORBITS = 1.0 / K_REFRESH_PER_ORBIT
EV_PER_WINDOW = E_TRUE * WINDOW_ORBITS / 1000.0

f_r_sched = R_EVENT_X86_NS * M1F * 1e-3 / US_PAIR_M1 * EV_PER_WINDOW   # event-scheduled wiring
f_r_every = R_EVENT_X86_NS * M1F * 1e-3 / US_PAIR_M1 * E_TRUE          # per-refresh full horizon (ruinous)

print(f"r_event {R_EVENT_X86_NS:.0f} ns x86 -> {R_EVENT_X86_NS*M1F:.0f} ns M1-implied")
print(f"events per refresh window (E_true={E_TRUE:.0f}/10^3 orbits, window {WINDOW_ORBITS:.1f} orbits): {EV_PER_WINDOW:.2f}")
print(f"f_r event-scheduled = {f_r_sched:.4f} | f_r per-refresh-full-horizon = {f_r_every:.1f} (killed)")
print()
txt = open(__file__.replace("ledger3.py", "run_decisive-out.txt")).read()
for line in txt.splitlines():
    m = re.search(r"belt mass (\S+) M_sun", line)
    if "DELETABLE" in line or (m and "==" in line and "variants" not in line):
        pass
surv = []
for line in txt.splitlines():
    mm = re.search(r"surviving ([0-9.e+-]+)", line)
    if mm:
        surv.append(float(mm.group(1)))
names = ["D[70m,470km] Ceres-top", "D[70m,300km]", "D[50m,300km]"]
print("gated ledger (flying pace, budget 4 cores), event-scheduled wiring:")
for nm, s in zip(names, surv):
    for u in UNGT:
        print(f"  {nm}: ungated {u:.2e} -> gated {u * (s + f_r_sched):.3g} cores"
              f"  (s={s:.2e}, f_r={f_r_sched:.4f}; ungated x (s+f_r_every) = {u*(s+f_r_every):.3g} under per-refresh wiring)")
