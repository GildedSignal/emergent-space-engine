#!/usr/bin/env python3
"""Parse nladder probe lines into window slopes and channel attribution.
Usage: analyze.py <log> [<log> ...]  — one summary block per log."""
import sys

def windows(rows, w=5000.0):
    """(lo, hi, rss_slope MB/1k gs, first_rss, last_rss) per gs window."""
    out = []
    lo = 0.0
    while True:
        sel = [r for r in rows if lo <= r["gs"] < lo + w]
        if not sel:
            if lo > (rows[-1]["gs"] if rows else 0):
                break
            lo += w
            continue
        hi = lo + w
        if len(sel) >= 2:
            first, last = sel[0], sel[-1]
            dg = last["gs"] - first["gs"]
            slope = (last["rss"] - first["rss"]) / (dg / 1000.0) if dg > 0 else 0.0
            out.append((lo, hi, slope, first["rss"], last["rss"],
                        sel[-1]["held"], sel[-1]["gt1"], sel[-1]["total"], sel[-1]["gap"]))
        if hi > (rows[-1]["gs"] if rows else 0):
            break
        lo = hi
    return out

for path in sys.argv[1:]:
    rows = []
    guard = None
    for line in open(path):
        if line.startswith("probe: gs="):
            f = dict(kv.split("=", 1) for kv in line.strip().split() if "=" in kv)
            rows.append({
                "gs": float(f["gs"]), "rss": float(f["rss_mb"]), "hwm": float(f.get("hwm_mb", 0)),
                "held": int(f.get("held", 0)), "bpb": int(f.get("bpb", 0)),
                "gt1": int(f.get("hist_gt1", 0)), "total": int(f.get("hist_total", 0)),
                "hmax": int(f.get("hist_max", 0)), "gap": float(f.get("gap_s", 0)),
            })
        elif line.startswith("probe: guard"):
            guard = line.strip()
    print(f"== {path}")
    if not rows:
        print("  (no probe lines)")
        continue
    print(f"  probes={len(rows)} gs=[{rows[0]['gs']:.0f}..{rows[-1]['gs']:.0f}] rss=[{rows[0]['rss']:.0f}..{rows[-1]['rss']:.0f}] MB  {guard or ''}")
    print(f"  held: first={rows[0]['held']} last={rows[-1]['held']} max={max(r['held'] for r in rows)}")
    print(f"  gap_s: max={max(r['gap'] for r in rows):.1f} last={rows[-1]['gap']:.1f}")
    print(f"  census: gt1 {rows[0]['gt1']}->{rows[-1]['gt1']}  total {rows[0]['total']}->{rows[-1]['total']}  hmax {rows[0]['hmax']}->{rows[-1]['hmax']}")
    print(f"  rss/held MB: {rows[0]['rss']/max(rows[0]['held'],1):.2f} -> {rows[-1]['rss']/max(rows[-1]['held'],1):.2f}")
    print("  window slopes (MB per 1k gs):")
    for (lo, hi, s, r0, r1, held, gt1, tot, gap) in windows(rows):
        print(f"    [{lo:6.0f},{hi:6.0f})  {s:7.2f}   rss {r0:7.0f}->{r1:7.0f}  held~{held:5d} gt1={gt1:6d} tot={tot:8d} gap={gap:8.1f}")
    # ladder line tail for counts
    for line in open(path):
        if line.startswith("ladder:"):
            print("  " + line.strip()[:400])
