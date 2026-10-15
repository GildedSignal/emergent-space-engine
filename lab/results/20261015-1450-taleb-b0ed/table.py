#!/usr/bin/env python3
"""Summarize the bounded-retention flights into one table (dossier evidence)."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROWS = []


def parse(p: Path):
    t = p.read_text()
    arm = p.stem.split("_")[0]
    scene = "_".join(p.stem.split("_")[1:])
    d = {}
    d["arm"] = arm
    d["scene"] = scene
    d["digest"] = re.search(r"^digest (\S+)", t, re.M).group(1)
    m = re.search(r"demotions (\d+) promotions (\d+) promote_us p50 ([\d.]+) p99 ([\d.]+) max ([\d.]+) total_s ([\d.]+)", t)
    d["dem"], d["pro"], d["p50"], d["p99"], d["mx"], d["tot"] = m.groups()
    m = re.search(r"bodies (\d+) bytes_per_body (\d+) catalogue_live (\d+)", t)
    d["bpb"] = m.group(2)
    m = re.search(r"retain hits (\d+) retained_now (\d+)(?: evictions (\d+) cap (\d+))?", t)
    d["hits"], d["now"], d["ev"], d["cap"] = m.group(1), m.group(2), m.group(3) or "-", m.group(4) or "-"
    m = re.search(r"wall_s ([\d.]+) rss_mb (\d+) hwm_mb (\d+)", t)
    d["wall"], d["rss"], d["hwm"] = m.groups()
    d["ratio"] = f"{int(d['pro']) / max(1, int(d['dem'])):.3f}"
    return d


for p in sorted(HERE.glob("flights/*.txt")):
    try:
        ROWS.append(parse(p))
    except Exception as e:  # noqa: BLE001
        print(f"# parse fail {p.name}: {e}", file=sys.stderr)

hdr = ["scene", "arm", "demotions", "promotions", "pro/dem", "hits", "retained_now", "evictions", "cap",
       "p50us", "p99us", "maxus", "prom_tot_s", "B/body", "rss_mb", "wall_s", "digest[:8]"]
print("\t".join(hdr))
for d in ROWS:
    print("\t".join([d["scene"], d["arm"], d["dem"], d["pro"], d["ratio"], d["hits"], d["now"],
                     d["ev"], d["cap"], d["p50"], d["p99"], d["mx"], d["tot"], d["bpb"],
                     d["rss"], d["wall"], d["digest"][:8]]))

# Digest identity per scene: every arm must match that scene's ctl digest (lazy arms) —
# seam/retain/bound are outcome-free, so ONE digest per scene.
print()
for scene in sorted({d["scene"] for d in ROWS}):
    arms = {d["arm"]: d["digest"] for d in ROWS if d["scene"] == scene}
    ref = arms.get("ctl")
    if ref is None:
        continue
    same = [a for a, dg in arms.items() if dg == ref]
    diff = [a for a, dg in arms.items() if dg != ref]
    print(f"{scene}: identical-to-ctl {len(same)}/{len(arms)}" + (f"  DIFFERING: {diff}" if diff else "  (all identical)"))
