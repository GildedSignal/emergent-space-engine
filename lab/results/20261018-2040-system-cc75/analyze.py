#!/usr/bin/env python3
"""Fold the bench reports and seen censuses into the run's metrics.json.

Inputs (made by regen.sh / the flights): work/bench{K}.json, work/seen{K}.txt for
K in 0, 1000, 10000, 100000, 300000. Output: metrics.json on stdout.
"""
import json, re, sys, pathlib

W = pathlib.Path(__file__).parent / "work"
FLOORS = {"8e-3": "sky pixel (800-px band)", "1e-3": "1-px full-circle ratchet",
          "1e-4": "10x ratchet", "1e-5": "100x ratchet"}

def report(k):
    p = W / f"bench{k}.json"
    if not p.exists() or p.stat().st_size == 0:
        return None
    try:
        r = json.loads(p.read_text())
    except json.JSONDecodeError:
        return None
    w = r["where_the_time_goes_ms"]
    return {
        "bodies": r["bodies"], "frames": r["frame_ms"]["p50"] and r.get("frames"),
        "frame_ms_p50": r["frame_ms"]["p50"], "frame_ms_p99": r["frame_ms"]["p99"],
        "view_gather_ms_p50": w["view_gather"]["p50"], "view_gather_share": w["view_gather"]["share"],
        "view_json_ms_p50": w["view_json"]["p50"], "view_json_share": w["view_json"]["share"],
        "wire_ms_p50": w["wire"]["p50"], "wire_share": w["wire"]["share"],
        "digest": r["digest"], "player_alive": r["player_alive"],
    }

def census(k):
    p = W / f"seen{k}.txt"
    if not p.exists():
        return None
    rows = []
    def parse(seg):
        d = {"floors": {}}
        for a, b in re.findall(r"(\w+)=(\S+)", seg):
            if ":" not in a:
                d[a] = b
        for fl, cells, alone in re.findall(r"f(\S+):cells=(\d+) alone=([\d.]+)", seg):
            d["floors"]["f" + fl] = {"cells": int(cells), "alone": float(alone)}
        return d
    for line in p.read_text().splitlines():
        m = re.match(r"frame=(\d+) seen=(\d+) wire_bytes=(\d+) FAR\[(.*)\] NEAR\[(.*)\]", line)
        if not m:
            continue
        rows.append({"frame": int(m.group(1)), "seen": int(m.group(2)),
                     "wire_bytes": int(m.group(3)), "far": parse(m.group(4)), "near": parse(m.group(5))})
    return rows

out = {"per_k": {}, "law": {}}
for k in [0, 1000, 10000, 100000, 300000]:
    rep, cen = report(k), census(k)
    if rep is None and cen is None:
        continue
    entry = {"report": rep, "census": cen}
    if cen:
        f30 = next((r for r in cen if r["frame"] == 30), cen[0])
        entry["headline"] = {
            "seen": f30["seen"], "wire_bytes_per_row": round(f30["wire_bytes"] / f30["seen"], 1),
            "far_rows": int(f30["far"]["n"]), "far_nu_p50_rad": float(f30["far"].get("nn_p50", "nan")),
            "far_cells_8e-3": f30["far"]["floors"]["f8e-3"]["cells"],
            "far_alone_8e-3": f30["far"]["floors"]["f8e-3"]["alone"],
            "far_cells_1e-3": f30["far"]["floors"]["f1e-3"]["cells"],
            "far_alone_1e-3": f30["far"]["floors"]["f1e-3"]["alone"],
            "far_cells_1e-5": f30["far"]["floors"]["f1e-5"]["cells"],
            "far_alone_1e-5": f30["far"]["floors"]["f1e-5"]["alone"],
            "near_rows": int(f30["near"]["n"]),
            "near_alone_1e-4": f30["near"]["floors"]["f1e-4"]["alone"],
        }
    out["per_k"][k] = entry

# The law: distinguishable far content vs paid far rows, per rung.
law = []
for k, e in out["per_k"].items():
    if "headline" in e:
        law.append({"k": k, "far_rows_paid": e["headline"]["far_rows"],
                    "sky_cells_occupied_8e-3": e["headline"]["far_cells_8e-3"],
                    "alone_frac_8e-3": e["headline"]["far_alone_8e-3"],
                    "alone_frac_1e-3": e["headline"]["far_alone_1e-3"]})
out["law"] = law
out["sky_capacity_8e-3"] = round(2 * 3.141592653589793 / 8e-3, 1)
json.dump(out, sys.stdout, indent=1)
print()
