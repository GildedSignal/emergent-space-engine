#!/usr/bin/env python3
"""Era analysis: is the arrival wave a recurring comb or a birth transient?
Reads escsv per-frame lines, bins arrivals by presented game-s, finds eras,
reports per-era arrivals/body, max_ms, over frames, delivered rtf, lag."""
import sys, re

def load(path):
    rows = []
    wall = 0.0
    for line in open(path):
        if line.startswith("escsv"):
            d = dict(kv.split("=") for kv in line.split()[1:])
            rows.append((int(d["f"]), float(d["ms"]), int(d["ev"]), int(d["k"]),
                         float(d["gs"]), float(d["lag"]), int(d["held"]), float(d["rss"])))
    return rows

def analyze(path, bodies, label):
    rows = load(path)
    print(f"== {label}: {len(rows)} frames, gs {rows[0][4]:.0f}..{rows[-1][4]:.0f}")
    gs_max = rows[-1][4]
    # 2k-gs bins on arrivals (events) and wall ms
    bins = {}
    for f, ms, ev, k, gs, lag, held, rss in rows:
        b = int(gs // 2000)
        e = bins.setdefault(b, [0, 0.0, 0, 0.0, 0.0])
        e[0] += ev; e[1] += ms; e[2] += 1
        e[3] = max(e[3], ms)
    print("bin_gs      ev/body   wall_ms    max_ms  frames  ev_total")
    for b in sorted(bins):
        ev, ms, n, mx, _ = bins[b]
        print(f"{b*2:>5}k  {ev/bodies:8.3f}  {ms:9.0f}  {mx:8.1f}  {n:5d}  {ev:8d}")
    # eras: contiguous bins with ev/body >= 0.05 separated by quieter bins
    mark = [b for b in sorted(bins) if bins[b][0] / bodies >= 0.05]
    eras = []
    for b in mark:
        if eras and b == eras[-1][-1] + 1:
            eras[-1].append(b)
        else:
            eras.append([b])
    print(f"\neras (>=0.05 ev/body per 2k-gs bin, contiguous): {len(eras)}")
    tot_ev = sum(bins[b][0] for b in bins)
    # wall-clock per era for delivered rtf: use cumulative ms
    cum = 0.0
    times = []
    for r in rows:
        times.append((r[4], cum, r[1]))
        cum += r[1]
    for i, era in enumerate(eras):
        g0, g1 = era[0]*2000, (era[-1]+1)*2000
        ev = sum(bins[b][0] for b in era)
        mx = max(bins[b][3] for b in era)
        over = sum(1 for r in rows if g0 <= r[4] < g1 and r[1] > 12.0)
        # wall time spent inside the era's frames
        w = sum(r[1] for r in rows if g0 <= r[4] < g1)
        # gap after this era until next era start
        if i + 1 < len(eras):
            h0 = g1; h1 = eras[i+1][0]*2000
        else:
            h0, h1 = g1, gs_max
        gapw = sum(r[1] for r in rows if h0 <= r[4] < h1)
        gapgs = sum(1 for r in rows if h0 <= r[4] < h1)
        # delivered rtf in the gap: presented-gs advanced / wall s
        gsgap = (h1 - h0)
        rtf = gsgap / (gapw / 1000.0) if gapw > 0 else float("nan")
        print(f"era {i+1}: gs {g0/1000:.0f}k-{g1/1000:.0f}k  ev/body {ev/bodies:.3f}  max_ms {mx:.1f}  over12 {over:4d}  era_wall {w/1000:6.1f}s | gap to next: {gsgap/1000:.0f}k gs, wall {gapw/1000:6.1f}s, delivered rtf {rtf:6.0f} gs/s")
    print(f"total events {tot_ev}, per body {tot_ev/bodies:.3f} over {gs_max:.0f} gs -> {tot_ev/bodies/gs_max*1e5:.2f}e-5/body/gs")
    # worst frames overall
    worst = sorted(rows, key=lambda r: -r[1])[:8]
    print("worst frames:", " ".join(f"(f{r[0]},gs{r[4]:.0f},{r[1]:.0f}ms,{r[2]}ev)" for r in worst))
    # rss and held trajectory
    print(f"held max {max(r[6] for r in rows)}, rss max {max(r[7] for r in rows):.0f} MB")
    print()
    return bins, eras

if __name__ == "__main__":
    analyze(sys.argv[1], int(sys.argv[2]), sys.argv[3])
