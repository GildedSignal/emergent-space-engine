#!/usr/bin/env python3
"""The FLOW arithmetic from the two probe logs: rates, per-scan pin, latch bound."""
import re, sys

def parse(path):
    rows = []
    for line in open(path):
        m = re.search(r"gs=\s*(\d+) live_B=\s*(\d+) live_n=\s*(\d+) peak_B=\s*(\d+) held_scans=\s*(\d+)", line)
        if m:
            rows.append(tuple(int(x) for x in m.groups()))  # ticks, liveB, liveN, peakB, held
    return rows

def gs_of(frames):  # 60 fps game-time x rtf 100: 5/3 game-s per frame; prints every 300 frames
    return frames * 5 / 3

base = sys.argv[1] if len(sys.argv) > 1 else "."
for name, path in [("quiet", f"{base}/flow_quiet.log"), ("load", f"{base}/flow_load.log")]:
    r = parse(path)
    if not r:
        print(f"{name}: no rows"); continue
    t0, t1 = r[0], r[-1]
    d_gs = gs_of(300 * (len(r) - 1))
    dB, dN, dH = t1[1] - t0[1], t1[2] - t0[2], t1[4] - t0[4]
    if dH <= 0:
        print(f"{name}: FLAT - held_scans {t0[4]}->{t1[4]}, no accumulation (idle time answers every scan)")
        continue
    per_scan_B = dB / dH
    per_scan_N = dN / dH
    print(f"{name}: live_B {t0[1]/1e6:.1f}->{t1[1]/1e6:.1f} MB over {d_gs:.0f} gs"
          f" = {(dB/d_gs)/1e3:.1f} kB/gs | held {t0[4]}->{t1[4]}"
          f" ({dH/d_gs*1000:.0f} scans/ks) | pin {per_scan_B/1e3:.0f} kB and {per_scan_N:.0f} allocs per held scan")
    print(f"  SCAN_BACKLOG latch bound at this pin: 2048 x {per_scan_B/1e3:.0f} kB = {2048*per_scan_B/1e9:.2f} GB")
    print(f"  latch ETA: 2048/{dH/d_gs:.2f} per gs = {2048/(dH/d_gs):.0f} gs (470f bulk-dropped at ~20,000 gs)")
