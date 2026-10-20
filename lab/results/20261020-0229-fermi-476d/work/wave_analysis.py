#!/usr/bin/env python3
"""Wave-excess analysis: sustained onset, windowed excess, tail structure, local exponents."""
import sys, math, glob

BUDGET = 12.0

def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            if line.startswith("csv ") and not line.startswith("csv frame"):
                parts = line[len("csv "):].strip().split(",")
                if len(parts) != 4:
                    continue
                fr, ms, ev, lag = parts
                rows.append((int(fr), float(ms), int(ev), float(lag)))
    return rows

def sustained_onset(rows, need=5, within=60):
    overs = [r[0] for r in rows if r[1] > BUDGET]
    for f0 in overs:
        n = sum(1 for f in overs if f0 <= f < f0 + within)
        if n >= need:
            return f0
    return None

def excess(rows, lo, hi):  # sum of over-budget ms over [lo, hi)
    return sum((ms - BUDGET) for f, ms, _, _ in rows if lo <= f < hi and ms > BUDGET)

def ebb(rows, lo, hi):
    return sum((BUDGET - ms) for f, ms, _, _ in rows if lo <= f < hi and ms < BUDGET)

def main():
    files = sorted(glob.glob("lab/results/20261020-0229-fermi-476d/work/flights/k*.csv.err"))
    arms = {}
    for p in files:
        name = p.split("/")[-1].replace(".csv.err", "")
        rows = [r for r in load(p) if r[0] >= 60]
        arms[name] = rows
        on = sustained_onset(rows)
        end = max(f for f, *_ in rows)
        ex = excess(rows, on, end + 1) if on else 0.0
        eb = ebb(rows, 60, on) if on else 0.0
        # cumulative excess curve at fixed offsets from onset
        curve = []
        c = 0.0
        for f, ms, _, _ in rows:
            if on and f >= on:
                c += max(0.0, ms - BUDGET)
                if (f - on) in (9, 19, 39, 79, 131):
                    curve.append((f - on, round(c, 1)))
        # events in crest window
        crest_ev = sum(ev for f, _, ev, _ in rows if on and on <= f < on + 40)
        crest_ms = sum(ms for f, ms, _, _ in rows if on and on <= f < on + 40)
        print(f"{name}: onset={on} end={end} excess_all={ex:.1f} ebb_pre={eb:.1f} "
              f"cum={curve} crest40: ms={crest_ms:.0f} events={crest_ev} "
              f"coverage={eb/ex if ex else float('inf'):.4f}")

    print()
    # matched windows at the smallest common post-onset length
    print("matched-window ratios (window = [onset, onset+W)):")
    for W in (40, 80, 132, 10**9):
        vals = {}
        for name, rows in arms.items():
            on = sustained_onset(rows)
            if on:
                vals[name] = excess(rows, on, on + W)
        ks = sorted(vals)
        line = f"  W={W}: " + " ".join(f"{k}={v:.0f}" for k, v in vals.items())
        if len(vals) >= 2 and "k300000_s10" in vals:
            # local exponents between consecutive rungs present
            import re
            def k_of(n):
                b = n[1:].split('_')[0]
                return int(float(b)) if 'e' in b else int(b)
            pairs = [(a, b) for a in ks for b in ks if k_of(b) > k_of(a)]
            for a, b in pairs:
                rk = k_of(b) / k_of(a)
                r = vals[b] / vals[a]
                alpha = math.log(r) / math.log(rk)
                line += f" | {k_of(a)}->{k_of(b)}: ratio={r:.3f} alpha={alpha:.3f}"
        print(line)

if __name__ == "__main__":
    main()
