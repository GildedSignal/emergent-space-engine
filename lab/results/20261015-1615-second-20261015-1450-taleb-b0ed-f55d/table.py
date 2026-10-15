#!/usr/bin/env python3
"""Burn-ladder table: knee vs N, working set, bill decomposition (dossier evidence).

Reads flights/*.txt written by regen.sh; every number in the dossier's burn section
comes from this table. Identity: per scene, every arm's digest must equal ctl's.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent


def parse(p: Path):
    t = p.read_text()
    parts = p.stem.split("_")
    arm, scene = parts[0], "_".join(parts[1:])
    d = {"arm": arm, "scene": scene, "f": p.name}
    d["digest"] = re.search(r"^digest (\S+)", t, re.M).group(1)
    m = re.search(r"demotions (\d+) promotions (\d+) promote_us p50 ([\d.]+) p99 ([\d.]+) max ([\d.]+) total_s ([\d.]+)", t)
    d["dem"], d["pro"], d["p50"], d["p99"], d["mx"], d["tot"] = m.groups()
    m = re.search(r"bodies (\d+) bytes_per_body (\d+) catalogue_live (\d+)", t)
    d["n"] = m.group(1)
    m = re.search(r"retain hits (\d+) retained_now (\d+)(?: evictions (\d+) cap (\d+))?", t)
    d["hits"], d["now"], d["ev"], d["cap"] = m.group(1), m.group(2), m.group(3) or "-", m.group(4) or "-"
    m = re.search(r"wall_s ([\d.]+) rss_mb (\d+) hwm_mb (\d+)", t)
    d["wall"], d["rss"], d["hwm"] = m.groups()
    m = re.search(r"arm N=(\d+) (\w+) cut=([\d.]+) seed=(\d+)", t)
    d["N"], d["flight"], d["cut"], d["seed"] = m.group(1), m.group(2), m.group(3), m.group(4)
    d["ratio"] = int(d["pro"]) / max(1, int(d["dem"]))
    return d


rows = []
for p in sorted(HERE.glob("flights/*.txt")):
    if p.name == "table.txt":
        continue
    try:
        rows.append(parse(p))
    except Exception as e:  # noqa: BLE001
        print(f"# parse fail {p.name}: {e}", file=sys.stderr)

# Global arm per scene = the reference bill (hits, retained plateau).
glob = {d["scene"]: d for d in rows if d["arm"] == "retain"}

hdr = ["scene", "arm", "N", "cap", "ratio", "hits", "hitfrac", "extra_pro", "retained_now", "dem", "pro",
       "prom_tot_s", "B/body", "rss_mb", "wall_s", "digest[:8]"]
print("\t".join(hdr))
for d in rows:
    g = glob.get(d["scene"])
    hf = f"{int(d['hits']) / int(g['hits']):.3f}" if g and int(g["hits"]) else "-"
    extra = int(d["pro"]) - int(d["dem"]) if d["arm"].startswith("bound") else 0
    print("\t".join([d["scene"], d["arm"], d["N"], d["cap"], f"{d['ratio']:.3f}", d["hits"], hf, str(extra),
                     d["now"], d["dem"], d["pro"], d["tot"], "-", d["rss"], d["wall"], d["digest"][:8]]))

print()
bad = 0
for scene in sorted({d["scene"] for d in rows}):
    arms = {d["arm"]: d["digest"] for d in rows if d["scene"] == scene}
    ref = arms.get("ctl")
    if ref is None:
        continue
    diff = [a for a, dg in arms.items() if dg != ref]
    if diff:
        bad += 1
    print(f"{scene}: identical-to-ctl {len(arms) - len(diff)}/{len(arms)}" + (f"  DIFFERING: {diff}" if diff else "  (all identical)"))
if bad:
    print(f"IDENTITY FAILURES: {bad}")
