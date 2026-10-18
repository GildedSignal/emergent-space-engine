#!/usr/bin/env python3
"""Summarize the nladder probe logs: RSS/HWM slope per game-second, held-scan trajectory,
mint-arrival lower bounds (positive held deltas between consecutive probe lines), frame stats.
Orders of magnitude only (Linux/x86). Usage: analyze.py <log...>"""
import re, sys

TICKS_PER_GAME_S = None  # derived from the log pair (now deltas vs the printed game s)
TICK_S = 4.925490947e-6  # view.rs: seconds in one tick (G·M_sun/c³)
def one(path):
    rows = []  # (frame, ms, ev, held, now, rss_mb, hwm_mb)
    for line in open(path):
        m = re.match(r"probe f=(\d+) ms=([\d.]+) ev=(\d+) held=(\d+) now=(\d+) rss=(\d+) hwm=(\d+)", line)
        if m:
            rows.append(tuple(int(x) if i != 1 else float(x) for i, x in enumerate(m.groups())))
    if not rows:
        print(f"{path}: no probe lines"); return
    first, last = rows[0], rows[-1]
    gs = (last[4] - first[4])  # ticks; game-s = ticks * TICK_SECONDS
    # TICK_SECONDS from view.rs: printed game-s in summary vs tick delta; use 1/4096 known constant fallback
    game_s = gs * TICK_S
    d_held = [max(0, rows[i][3] - rows[i-1][3]) for i in range(1, len(rows))]
    arrivals_lb = sum(d_held)
    slope = (last[6] - first[6]) / game_s if game_s > 0 else 0.0  # HWM slope, MB per game-s
    rss_slope = (last[5] - first[5]) / game_s if game_s > 0 else 0.0
    ms = sorted(r[1] for r in rows)
    over12 = sum(1 for r in rows if r[1] > 12.0)
    print(f"{path.split('/')[-1]:24s} frames {len(rows):4d} game_s {game_s:7.1f} p50 {ms[len(ms)//2]:6.2f} p99 {ms[int(len(ms)*0.99)]:6.2f} over12 {over12:3d} "
          f"held_max {max(r[3] for r in rows):4d} arrivals_lb {arrivals_lb:4d} "
          f"hwm {first[6]:5d}->{last[6]:5d} MB  hwm_slope {slope:8.3f} MB/game-s  rss_slope {rss_slope:8.3f}")

for p in sys.argv[1:]:
    one(p)
