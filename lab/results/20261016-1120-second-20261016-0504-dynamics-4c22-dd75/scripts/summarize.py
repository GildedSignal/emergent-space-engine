#!/usr/bin/env python3
"""The dossier's numbers, from the batch's row files — run 20261016-1120 (second author).

Same table as run 20261016-0504's summarize.py, but the lane split is computed from the FIXED
attribution instrument (one take per frame): worst-12 frames' mean events split into
d0 (the player's doll) / d2+d3 (the planets' dolls: Home, Giant) / residue (events the
first-item attribution never saw). The original run's split paired row i with frame i/2's
counters, which manufactured a phantom 'fleet lane'."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from analyze import load, d2

def top_envelope(rows, thirds=4):
    out = []
    n = len(rows)
    for i in range(thirds):
        seg = rows[i*n//thirds:(i+1)*n//thirds]
        best = sorted((r["ev"] for r in seg), reverse=True)[:5]
        out.append(round(sum(best)/len(best)))
    return out

def lane_split(rows):
    worst = sorted(rows, key=lambda r: -r["ev"])[:12]
    n = len(worst)
    tot = sum(r["ev"] for r in worst)/n
    d0 = sum(sum(r["att"].get(0, [0]*4)) for r in worst)/n
    pd = sum(d2(r) + sum(r["att"].get(3, [0]*4)) for r in worst)/n
    other = sum(sum(v for k, v in r["att"].items() if k not in (0, 2, 3)) for r in worst)/n
    return (round(tot,1), round(d0,1), round(pd,1), round(tot-d0-pd-other,1))

NAMES = ["base_n1e3_coast","base_n0_20s","base_n600_20s","base_n1e4_20s","base_n1e3_60s",
         "stag_n1e3_60s","phase_n1e3_60s","phase_n1e4_20s"]
for name in NAMES:
    try: rows = [r for r in load(name) if r["frame"] >= 60]
    except FileNotFoundError: continue
    evs = sorted(r["ev"] for r in rows)
    mss = sorted(r["ms"] for r in rows)
    gs = rows[-1]["gs"] - rows[0]["gs"]
    print(f"{name:18s} gs {gs:6.0f} med {evs[len(evs)//2]:3d} p99 {evs[int(0.99*(len(evs)-1))]:3d} max {evs[-1]:3d} "
          f"ev/gs {sum(evs)/gs:5.2f} ms_p99 {mss[int(0.99*(len(mss)-1))]:5.2f} mean_top10_ms {sum(mss[-10:])/10:5.2f} "
          f"envelope {top_envelope(rows)} worst12(tot,d0,planetdolls,residue) {lane_split(rows)}")
