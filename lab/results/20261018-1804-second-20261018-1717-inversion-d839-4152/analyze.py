#!/usr/bin/env python3
"""Analysis for 4152 (second author on d839): burn-through-2-steps + same-N rate.
Reads the probe lines and summary lines of the four flights in raw/."""
import re, sys

base = "lab/results/20261018-1804-second-20261018-1717-inversion-d839-4152/raw"

def probes(name):
    rows = []
    for line in open(f"{base}/{name}"):
        m = re.match(r"probe: f=(\d+) gs=(\S+) rss_mb=(\S+) hwm_mb=(\S+) bpb=(\d+) cat=(\d+) held=(\d+) kicks=(\d+) events=(\d+)", line)
        if m:
            rows.append(dict(f=int(m.group(1)), gs=float(m.group(2)), rss=float(m.group(3)),
                             hwm=float(m.group(4)), bpb=int(m.group(5)), cat=int(m.group(6)),
                             held=int(m.group(7)), kicks=int(m.group(8)), events=int(m.group(9))))
    return rows

def summary(name):
    lad = g = None
    for line in open(f"{base}/{name}"):
        if line.startswith("ladder:"):
            lad = dict(re.findall(r"(\w+)=(\S+)", line))
        elif line.startswith("game "):
            g = line.strip()
    return lad, g

def waves(rows, thr=4000):
    """belt-wide kick waves: probe-to-probe kick jumps > thr."""
    out, prev = [], None
    for r in rows:
        if prev and r["kicks"] - prev["kicks"] > thr:
            out.append((prev["gs"], r["gs"], r["kicks"] - prev["kicks"]))
        prev = r
    return out

name = sys.argv[1] if len(sys.argv) > 1 else "n30000_burn_760s.log"
rows = probes(name)
lad, g = summary(name)
print(f"== {name}: {len(rows)} probes, gs_end={rows[-1]['gs']:.0f}")
if lad:
    print(f"   ladder: gs~{lad.get('frames')} frames, rss {lad['foot_build_mb']}->{lad['foot_end_mb']} MB, "
          f"b_per_body={lad['b_per_body']}, p99={lad['p99_ms']} max={lad['max_ms']} over={lad['over']} "
          f"held_max={lad['held_max']} kicks/b/gs={lad['kicks_per_body_gs']} ev/b/gs={lad['events_per_body_gs']} wall={lad['wall_s']}s")
if g:
    print(f"   {g}")
print(f"   kick waves (thr {thr if (thr:=4000) else 4000}): {waves(rows)}")
# RSS/held trajectory in 2.5k-gs bins (the mint-channel instrument)
print("   gs : rss hwm bpb cat held kicks events")
for r in rows[::5]:
    print(f"   {r['gs']:6.0f} : {r['rss']:4.0f} {r['hwm']:4.0f} {r['bpb']} {r['cat']} {r['held']:4d} {r['kicks']:7d} {r['events']:7d}")
