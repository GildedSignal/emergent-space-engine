#!/usr/bin/env python3
"""Wave analysis for the stagger run (lab/results/20261015-0128-fermi-ed3a).
Reads the stagger example's CSVs (frame,game_s,ms,events,lag_s), buckets events by
presented game-second (250-s windows), and reports the wave peaks, the flattening
ratio between arms, the worst-lag location, and the frame profile."""
import csv
import sys
from pathlib import Path

W = 250.0


def load(p):
    rows = []
    with open(p) as f:
        for r in csv.reader(f):
            if r[0] == "frame":
                continue
            rows.append((int(r[0]), float(r[1]), float(r[2]), int(r[3]), float(r[4])))
    return rows


def windows(rows):
    ws = {}
    for _, g, _, e, _ in rows:
        if g < 0:
            continue
        ws.setdefault(int(g // W), 0)
        ws[int(g // W)] += e
    return ws


def stats(rows, label):
    late = [r for r in rows if r[0] >= 60]
    ms = sorted(r[2] for r in late)
    ev = sorted(r[3] for r in late)
    lag = max(late, key=lambda r: r[4])
    ws = windows(rows)
    peak_w = max(ws, key=lambda w: ws[w])
    # waves: windows with >= 25% of the peak, merged into runs
    thr = 0.25 * ws[peak_w]
    hot = sorted(w for w, e in ws.items() if e >= thr)
    print(f"{label}: frames {len(late)}")
    print(f"  engine ms p50 {ms[len(ms)//2]:.3f} p99 {ms[int(len(ms)*0.99)]:.3f} max {ms[-1]:.3f}; "
          f"events/frame p50 {ev[len(ev)//2]} p99 {ev[int(len(ev)*0.99)]} max {ev[-1]}")
    print(f"  peak window [{peak_w*W:.0f},{peak_w*W+W:.0f}) game-s: {ws[peak_w]} events")
    print(f"  hot windows (>=25% peak): {[(f'{w*W:.0f}', ws[w]) for w in hot]}")
    print(f"  worst lag {lag[4]:.3f} s at game-s {lag[1]:.0f} (frame {lag[0]}, events {lag[3]}, ms {lag[2]:.1f})")
    return ws, ev[-1], ms[-1]


def main():
    files = sys.argv[1:]
    allws = {}
    for p in files:
        rows = load(p)
        allws[p] = stats(rows, Path(p).name)
    if len(allws) == 2:
        (a, b) = list(allws.items())
        wa, wb = a[1][0], b[1][0]
        pa, pb = max(wa.values()), max(wb.values())
        print(f"\nflattening (peak window {Path(a[0]).name} / {Path(b[0]).name}): {pa/pb:.1f}x "
              f"({pa} -> {pb} events per {W:.0f} game-s)")
        print(f"events/frame max ratio: {a[1][1]/max(b[1][1],1):.1f}x")


if __name__ == "__main__":
    main()
