#!/usr/bin/env python3
"""Assemble metrics.json for r5-starve from the harness rows in $1 (default rows/).

Coverage is per configuration, from that config's own rows (the 68e7 checker's note 3):
battle configs count distinct scenes with contacts > 0, epochs > 0 and a live carry; the
allocator config counts its own cells (each cell is one full starved scene run).
"""
import json, pathlib, sys

rows_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "rows")
rows = []
for p in sorted(rows_dir.glob("r5s*.json")):
    rows += [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def frac(cfg):
    rs = [r for r in rows if r["config"] == cfg]
    return (sum(bool(r["identical"]) for r in rs) / len(rs)) if rs else None


def covered(cfg):
    rs = [r for r in rows if r["config"] == cfg]
    if cfg == "alloc-sparse-starved":
        return sum(1 for r in rs if r["contacts"] > 0 and r["units"] > 0)
    return len({r["scene"] for r in rs if r["contacts"] > 0 and r.get("epochs", 0) > 0 and r.get("carried")})


out = {}
for cfg in ["cpu-pair-starved", "cpu-pair-loaded", "alloc-sparse-starved", "cpu-pair-starved-shifted", "cpu-pair-starved-late"]:
    rs = [r for r in rows if r["config"] == cfg]
    e = {"identical_fraction": frac(cfg), "covered_scenes": covered(cfg)}
    if cfg == "cpu-pair-starved":
        e["contacts_total"] = sum(r["contacts"] for r in rs if r["pair"] == "sparse-rand-vs-lockstep")
        e["starved_calls_total"] = sum(r.get("calls", 0) for r in rs)
        e["secs"] = round(sum(r.get("secs_a", 0.0) + r.get("secs_b", 0.0) for r in rs), 3)
    if cfg == "cpu-pair-loaded":
        e["slow_min"] = min(r.get("slow", 0.0) for r in rs)
        e["slow_median"] = sorted(r.get("slow", 0.0) for r in rs)[len(rs) // 2]
    if cfg == "alloc-sparse-starved":
        e["units_total"] = sum(r["units"] for r in rs)
        e["rollbacks_total"] = sum(r["rollbacks"] for r in rs)
    out[cfg] = e
json.dump(out, sys.stdout, indent=1)
print()
