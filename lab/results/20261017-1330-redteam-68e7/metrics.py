#!/usr/bin/env python3
"""Assemble metrics.json for r5 from the harness rows in $1 (default rows/)."""
import json, pathlib, sys

rows_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "rows")
rows = []
for p in sorted(rows_dir.glob("r5-*.json")):
    rows += [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def frac(cfg):
    rs = [r for r in rows if r["config"] == cfg]
    return (sum(r["identical"] for r in rs) / len(rs)) if rs else None


def covered():
    seen = {r["scene"]: r for r in rows if r["config"] == "cpu-pair" and r["threads"] == 1}
    return sum(1 for r in seen.values() if r["contacts"] > 0 and r["epochs"] > 0 and r["carried"])


cand = [r for r in rows if r["config"] == "cpu-pair"]
out = {
    "cpu-pair": {
        "identical_fraction": frac("cpu-pair"),
        "covered_scenes": covered(),
        "contacts_total": sum(r["contacts"] for r in cand if r["threads"] == 1),
        "secs_lockstep": sum(r["secs_lockstep"] for r in cand),
        "secs_sparse": sum(r["secs_sparse"] for r in cand),
    },
    "cpu-pair-shifted": {"identical_fraction": frac("cpu-pair-shifted"), "covered_scenes": covered()},
    "cpu-pair-late": {"identical_fraction": frac("cpu-pair-late"), "covered_scenes": covered()},
}
json.dump(out, sys.stdout, indent=1)
print()
