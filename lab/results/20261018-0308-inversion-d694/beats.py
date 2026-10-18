#!/usr/bin/env python3
"""Beat-train analysis of nladder per-frame CSVs (frame,ms,events,lag_s,presented_game_s).

Prints, per CSV: the belt beat train (windows [13051,14534] + k*14070 game-s, the spacing
measured on this run's own record from the mass-band centers; belt_first on this scenario
gives the first-beat window), the standing comb between beats, and the whole-flight frame
letter. Usage: beats.py <csv1> [<csv2> ...]
"""
import csv
import statistics
import sys

B1LO, B1HI, T = 13051.0, 14534.0, 14070.0


def load(path):
    with open(path) as f:
        return [(float(r["presented_game_s"]), int(r["events"]), float(r["ms"])) for r in csv.DictReader(f)]


def in_band(t):
    return any(B1LO + k * T - 1200 <= t <= B1HI + k * T + 1200 for k in range(0, 8))


def summarize(path):
    ev = load(path)
    print(f"== {path}: {len(ev)} frames, presented 0..{ev[-1][0]:.0f} game-s ({ev[-1][0] / 86400:.2f} game-d)")
    print(f"## belt beat train, spacing {T:.0f} game-s (window [13051,14534] + k*T, +-1200)")
    masses, peaks, mss = [], [], []
    k = 0
    while B1LO + k * T < ev[-1][0]:
        lo, hi = B1LO + k * T - 1200, B1HI + k * T + 1200
        w = [(t, e, m) for t, e, m in ev if lo <= t <= hi]
        if w:
            mass = sum(e for _, e, _ in w)
            peak = max(e for _, e, _ in w)
            ms = max(m for _, _, m in w)
            ew = [t for t, e, _ in w if e >= 0.5 * peak]
            width = (max(ew) - min(ew)) if len(ew) > 1 else 0
            masses.append(mass)
            peaks.append(peak)
            mss.append(ms)
            print(f"  beat {k + 1} [{lo:7.0f},{hi:7.0f}]: mass {mass:6d}  peak {peak:4d}  max_ms {ms:6.2f}  crest_width {width:6.0f}")
        k += 1
    if masses:
        print(f"  -> {len(masses)} beats: mass first {masses[0]} last {masses[-1]} (min {min(masses)}, max {max(masses)}); peaks {min(peaks)}-{max(peaks)}; per-beat max_ms {min(mss):.2f}-{max(mss):.2f}")
    comb = [(t, e) for t, e, _ in ev if e >= 250 and not in_band(t)]
    sp = [b[0] - a[0] for a, b in zip(comb, comb[1:]) if b[0] - a[0] > 1000]
    if comb:
        print(f"## standing comb outside beat bands: {len(comb)} crest frames >=250 events; heights {min(e for _, e in comb)}-{max(e for _, e in comb)}; median spacing {statistics.median(sp):.0f} game-s" if sp else f"## standing comb: {len(comb)} crest frames, no >1000-s spacings")
    ms = sorted(m for _, _, m in ev)
    es = sorted(e for _, e, _ in ev)
    n = len(ms)
    print(f"## whole-flight letter: ms p50 {ms[n // 2]:.3f} p99 {ms[int(n * 0.99)]:.3f} max {ms[-1]:.3f}; frames>12ms {sum(m > 12 for m in ms)}; events/frame p99 {es[int(n * 0.99)]} max {es[-1]}")


for p in sys.argv[1:]:
    summarize(p)
