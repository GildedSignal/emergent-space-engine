#!/usr/bin/env python3
"""Summarise the second-author ladder; emit the table, the bracket, and rung metrics.json."""
import json, statistics, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)

def row(name):
    d = load(name)
    r = d["rtf"]; fm = d["frame_ms"]; w = d["where_the_time_goes_ms"]
    return {
        "run": name.replace(".json", ""),
        "low1": r["lowest_1pct"], "med": r["median"], "overflow": r["overflow_frames"],
        "p50": fm["p50"], "p99": fm["p99"], "worst": d["worst_hitch_ms"],
        "over16": d["hitch_counts"][0],
        "gather_share": w["view_gather"]["share"], "gather_max": w["view_gather"]["max"],
        "engine_max": w["engine"]["max"], "ev_s": d["events_per_second"], "bodies": d["bodies"],
        "digest": d["digest"][:16], "cut": d["cut_tick"], "seed": d["seed"],
    }

SEEDS = [1, 7, 13]
MEMBERS = [48, 96, 192, 384]
rows = {}
for m in MEMBERS:
    for s in SEEDS:
        n = f"m{m}-s{s}.json"
        if os.path.exists(os.path.join(HERE, n)):
            rows[(m, s)] = row(n)

hdr = ["run", "low1", "med", "overflow", "p50", "p99", "worst", "over16", "gather_share",
       "gather_max", "engine_max", "ev_s", "bodies", "digest"]
print(" | ".join(h[:12] for h in hdr))
for (m, s), r in sorted(rows.items()):
    print(" | ".join(
        f"{r[h]:.3f}" if isinstance(r[h], float) else str(r[h]) for h in hdr))

print("\n== per-members median-of-seeds ==")
med = {}
for m in MEMBERS:
    lows = [rows[(m, s)]["low1"] for s in SEEDS if (m, s) in rows]
    if lows:
        med[m] = statistics.median(lows)
        print(f"m{m:3d}: rtf_low1 median {med[m]:9.4f}  seeds {[round(x,4) for x in lows]}")

print("\n== gather share across all ladder runs ==")
shares = [r["gather_share"] for r in rows.values()]
print(f"min {min(shares):.3f} max {max(shares):.3f}")
gmax = [r["gather_max"] for r in rows.values()]
print(f"gather max ms: min {min(gmax):.2f} max {max(gmax):.2f}")

print("\n== digest invariance (unpaced 15 s twins, same seed, same cut) ==")
inv = {}
for tag, a, b in [("m48-s1", "inv-m48-s1-e05.json", "inv-m48-s1-e50.json"),
                  ("m192-s13", "inv-m192-s13-e05.json", "inv-m192-s13-e50.json"),
                  ("m384-s13", "inv-m384-s13-e05.json", "inv-m384-s13-e50.json")]:
    pa, pb = os.path.join(HERE, a), os.path.join(HERE, b)
    if os.path.exists(pa) and os.path.exists(pb):
        da, db = load(a), load(b)
        same = da["digest"] == db["digest"] and da["cut_tick"] == db["cut_tick"]
        inv[tag] = same
        print(f"{tag}: digest {da['digest'][:16]} vs {db['digest'][:16]} cut {da['cut_tick']}=={db['cut_tick']} -> {'SAME' if same else 'DIFFER'}"
              f" ; overflow {da['rtf']['overflow_frames']}/{da['rtf']['overflow_frames'] and 900} vs {db['rtf']['overflow_frames']}")

# regen check against the original record
print("\n== regeneration vs the original record ==")
orig = {"digest": "77d106d9d172d7b6b5e068714d6875e9b4bf9a491af229df4263f1659c0345dd", "low1": 0.0,
        "cut": 609076340, "bodies": 212}
if os.path.exists(os.path.join(HERE, "regen-m192-s1.json")):
    d = load("regen-m192-s1.json")
    ok = (d["digest"] == orig["digest"] and d["cut_tick"] == orig["cut"]
          and d["bodies"] == orig["bodies"])  # canonical fields only; low1 is wall-sampled
    print(f"regen-m192-s1: digest {d['digest'][:16]} cut {d['cut_tick']} bodies {d['bodies']} (low1 {d['rtf']['lowest_1pct']:.3f}, non-canonical) -> {'REGENERATED' if ok else 'MISMATCH'}")

# rung metrics.json (author side)
metrics = {
    "plane-1x": {"rtf_low1_median": med.get(48, 0.0), "digest_invariant": 1.0 if inv.get("m48-s1") else 0.0},
    "plane-4x": {"rtf_low1_median": med.get(192, 0.0), "digest_invariant": 1.0 if inv.get("m192-s13") else 0.0},
    "plane-8x": {"rtf_low1_median": med.get(384, 0.0), "digest_invariant": 1.0 if inv.get("m384-s13") else 0.0},
}
with open(os.path.join(HERE, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=1)
print("\nmetrics.json:", json.dumps(metrics))
