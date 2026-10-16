#!/usr/bin/env python3
"""The dossier's numbers, from the batch's row files."""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from analyze import load, d2

def top_envelope(rows, thirds=4):
    """mean of the top 5 frames per equal time-slice: does the comb's top decay?"""
    out = []
    n = len(rows)
    for i in range(thirds):
        seg = rows[i*n//thirds:(i+1)*n//thirds]
        best = sorted((r["ev"] for r in seg), reverse=True)[:5]
        out.append(round(sum(best)/len(best)))
    return out

def lane_split(rows):
    worst = sorted(rows, key=lambda r: -r["ev"])[:12]
    tot = sum(r["ev"] for r in worst)/len(worst)
    att = sum(d2(r) + sum(r["att"].get(3, [0]*4)) for r in worst)/len(worst)
    return round(tot,1), round(att,1), round(tot-att,1)

for name in ["base_n0_20s","base_n600_20s","base_n1e3_20s" ,"base_n1e3_coast","base_n1e4_20s","base_n1e3_60s","stag_n1e3_20s","stag_n1e3_60s","phase_n1e3_20s","phase_n1e3_60s","phase_n1e4_20s"]:
    try: rows = [r for r in load(name) if r["frame"] >= 60]
    except FileNotFoundError: continue
    evs = sorted(r["ev"] for r in rows)
    mss = sorted(r["ms"] for r in rows)
    gs = rows[-1]["gs"] - rows[0]["gs"]
    mean_top10_ms = sum(mss[-10:])/10
    print(f"{name:20s} gs {gs:6.0f} med {evs[len(evs)//2]:3d} p99 {evs[int(0.99*(len(evs)-1))]:3d} max {evs[-1]:3d} "
          f"ev/gs {sum(evs)/gs:5.2f} ms_p99 {mss[int(0.99*(len(mss)-1))]:5.2f} mean_top10_ms {mean_top10_ms:5.2f} "
          f"envelope(4 slices) {top_envelope(rows)} worst12_lane(tot,planetdolls,fleet) {lane_split(rows)}")
