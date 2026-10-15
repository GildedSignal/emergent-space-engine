#!/usr/bin/env python3
"""Marginal cost per belt body from `nladder N coast` ladder lines (regen: work/marginal.py).

Reads stdin (or work/flights.txt): every `ladder:` line holds key=value pairs; we use
foot_build_mb (peak VmHWM at build end), b_per_body, view_ms. Prints the marginal
bytes/body between rungs and the 10^9 extrapolation against an 8 GB machine.
"""
import re
import sys

lines = [l for l in (open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin) if l.startswith("ladder:")]
rows = []
for l in lines:
    kv = dict(re.findall(r"(\w+)=([-\w.e+]+)", l))
    if "bodies" in kv:
        rows.append((int(kv["bodies"]), int(kv["n"]), float(kv["foot_build_mb"]),
                     float(kv.get("b_per_body", "nan")), float(kv.get("view_ms", "nan"))))
rows.sort()
print(f"{'bodies':>9} {'n_extra':>8} {'peak_MB':>8} {'b/body_end':>11} {'view_ms':>9}")
for b, n, mb, bb, v in rows:
    print(f"{b:>9} {n:>8} {mb:>8.0f} {bb:>11.0f} {v:>9.1f}")
print()
prev = None
for b, n, mb, bb, v in rows:
    if prev is not None and b > prev[0]:
        d = (mb - prev[1]) * 1e6 / (b - prev[0])
        print(f"marginal {prev[0]:>9}->{b:<9}: {d:>8.0f} B/body (build peak slope)")
    prev = (b, mb)
# 10^9 extrapolation from the two largest rungs
slope = (rows[-1][2] - rows[-2][2]) * 1e6 / (rows[-1][0] - rows[-2][0])
print(f"\nlargest-rung slope {slope:.0f} B/body; at 1e9 belt bodies: {slope*1e9/1e12:.2f} TB")
print(f"8 GB machine all-in budget: 8 B/body; over budget by {slope/8:.0f}x")
v_slope = (rows[-1][4] - rows[-2][4]) * 1e3 / (rows[-1][0] - rows[-2][0])
print(f"view gather slope {v_slope:.2f} us/body -> {v_slope*1e3:.0f} ms at 1e6 bodies, {v_slope*1e6/3.6e6:.2f} h at 1e9")
