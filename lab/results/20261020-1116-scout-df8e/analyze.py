#!/usr/bin/env python3
"""Analyse the clock-phase flights: comb shape, era worst frames, determinism.
Usage: analyze.py <dir-with-csvs>"""
import sys, math
from pathlib import Path

d = Path(sys.argv[1])
BELT = 100000

def load(tag):
    rows = []
    for ln in (d / f"{tag}.csv").read_text().splitlines():
        p = ln.split(",")
        if len(p) != 6: continue
        rows.append((int(p[1]), float(p[2]), int(p[3]), float(p[4]), float(p[5])))
    return rows

def stats(rows, budget=12.0):
    late = [r for r in rows if r[0] >= 60]
    ms = sorted(r[1] for r in late)
    ev = sorted(r[2] for r in late)
    p = lambda v, q: v[min(len(v) - 1, int(q * len(v)))]
    return dict(n=len(late), p50=p(ms, .5), p99=p(ms, .99), worst=ms[-1] if ms else 0,
                over=sum(1 for x in ms if x > budget), ev_tot=sum(r[2] for r in late),
                ev_p99=p(ev, .99) if ev else 0, ev_max=ev[-1] if ev else 0,
                lag=max((r[4] for r in late), default=0.0))

def comb(rows, bin_gs=1500.0):
    """events binned by presented game-time: peak/mean, onset, share in the busiest 29%."""
    bins = {}
    for _, _, e, gs, _ in rows:
        if gs < 100: continue
        b = int(gs // bin_gs)
        bins[b] = bins.get(b, 0) + e
    if not bins: return None
    v = sorted(bins.values())
    mean = sum(v) / len(v)
    peak = max(v)
    lo = min(bins); span = max(bins) - lo + 1
    top = sorted(bins.items(), key=lambda kv: -kv[1])[:max(1, int(0.29 * span))]
    share = sum(x[1] for x in top) / sum(v)
    onset = max(bins, key=bins.get)
    return dict(bins=len(v), mean=mean, peak=peak, ratio=peak / mean if mean else 0,
                share_top29=share, peak_bin_gs=(onset + 0.5) * bin_gs,
                peak_bin_gse=onset * bin_gs, bin_gs=bin_gs)

def eras(rows, period=14000.0, width=None):
    """worst frame and events per 14k-gs era of presented time."""
    out = {}
    for r in rows:
        if r[3] < 100: continue
        e = int(r[3] // period)
        cur = out.get(e, (0.0, 0, 0.0))
        out[e] = (max(cur[0], r[1]), cur[1] + r[2], max(cur[2], r[4]))
    return {k: (round(v[0], 1), v[1], round(v[2], 1)) for k, v in sorted(out.items())}

for tag in ("off1", "off2", "on1", "on2", "half"):
    f = d / f"{tag}.csv"
    if not f.exists(): print(f"{tag}: MISSING"); continue
    rows = load(tag)
    s = stats(rows); c = comb(rows)
    print(f"\n== {tag}: frames {s['n']}, p50 {s['p50']:.2f} p99 {s['p99']:.2f} worst {s['worst']:.1f} ms, "
          f"over12 {s['over']}, events tot {s['ev_tot']} ({s['ev_tot']/BELT:.3f}/body), "
          f"ev/frame p99 {s['ev_p99']:.0f} max {s['ev_max']}, lag {s['lag']:.2f} s")
    if c:
        print(f"   comb: {c['bins']} bins of {c['bin_gs']:.0f} gs, peak/mean {c['ratio']:.2f}, "
              f"busiest-29% share {c['share_top29']:.2f}, peak bin at {c['peak_bin_gs']:.0f} gs")
    print("   eras (worst ms, events, lag):", eras(rows))

# determinism: byte-identity of the two ON flights
try:
    a = (d / "on1.csv").read_bytes(); b = (d / "on2.csv").read_bytes()
    print(f"\ndeterminism on1==on2: {a == b} ({len(a)} vs {len(b)} bytes)")
except FileNotFoundError:
    pass
