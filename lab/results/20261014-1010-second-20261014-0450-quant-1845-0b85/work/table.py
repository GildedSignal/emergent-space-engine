#!/usr/bin/env python3
"""Summarise the A/B arms: one prof binary, ES_IMP_WARM off/on, five arms (+ smoke + identity).

Reads every <arm>-off.json / <arm>-on.json in this folder and prints the dossier's table:
per arm, the fired kick (P_KICK) and its impact search (K_IMP), the warm counters, the hand-out,
and the digest identity. Identity files (<arm>-plain.json = patched plain build with warm on,
<arm>-pristine.json = unpatched HEAD) are checked against each other when present.
"""
import json, re, sys
from pathlib import Path

W = Path(__file__).parent
STAGES = {
    "kick": "item: kick (Wisdom-Holman)",
    "kicksub": "item: kick at a changeover level",
    "kimp": "  next_impact bisection",
    "kterm": "  plan_terminal (terminal/impact search)",
    "kwarm": "  warm impact search (gallop from the retired crash tick)",
    "kfb": "  warm gallop fallback (reached the cold bracket's edge)",
    "kping": "  impact predicate evaluations (the searches' readouts)",
    "hbind": "  hand-out: bind (the member as a tube)",
    "hreplan": "  hand-out: first plan (replan)",
    "fit2": "  fit again: the coarser word (bind_surface)",
    "rowf": "  orbit_state/readout family (decode, all callers)",
}

def load(name):
    p = W / f"{name}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    st = {k: s for k, s in STAGES.items()}
    prof = {p["stage"]: p for p in d.get("prof_stages", [])}
    out = {"digest": d["digest"], "cut": d["cut_tick"]}
    for k, s in st.items():
        p = prof.get(s)
        out[k] = (p["calls"], p["us_per_call"]) if p else (0, 0.0)
    out["kick_items"] = out["kick"][0]
    m = re.search(r"kicks: (\d+)", d["stats"])
    out["stats_kicks"] = int(m.group(1)) if m else 0
    m = re.search(r"leavers: (\d+)", d["stats"])
    out["leavers"] = int(m.group(1)) if m else 0
    m = re.search(r"overflow_frames: (\d+)", json.dumps(d))
    out["overflow"] = int(m.group(1)) if m else 0
    out["fleet_us"] = next((k["us_per_item"] for k in d["engine_cost_by_kind"] if k["kind"] == "fleet" and k["items"] > 0), 0.0)
    return out

def fmt(t):
    return f"{t[1]:.1f}µs×{t[0]}" if t[0] else "—"

ARMS = sys.argv[1:] or ["m4000-s3", "m1500-s3", "m4000-s7", "m400-s3-f", "m16000-s3"]
print(f"{'arm':<10} {'digest off=on':<13} {'fired kick off→on':<20} {'K_IMP off→on':<22} {'warm/fb':<14} {'hand-out replan off→on':<24}")
for arm in ARMS:
    off, on = load(arm + "-off"), load(arm + "-on")
    if not off or not on:
        print(f"{arm:<10} missing")
        continue
    same = "YES" if off["digest"] == on["digest"] else "NO!"
    kick = f"{off['kick'][1]:.1f}→{on['kick'][1]:.1f}" if off["kick"][0] else "no fired kicks"
    if off["kick"][0]:
        kick += f" ({100 * (on['kick'][1] / off['kick'][1] - 1):+.0f}%)"
    kimp = f"{off['kimp'][1]:.1f}→{on['kimp'][1]:.1f} ({off['kimp'][0]}/{on['kimp'][0]})"
    wfb = f"{on['kwarm'][0]}/{on['kfb'][0]}"
    ho = f"{off['hreplan'][1]:.1f}→{on['hreplan'][1]:.1f}" if off["hreplan"][0] else "—"
    print(f"{arm:<10} {same:<13} {kick:<20} {kimp:<22} {wfb:<14} {ho:<24}")
    print(f"{'':<10} kick calls {off['kick'][0]}/{on['kick'][0]}, stats kicks {off['stats_kicks']}/{on['stats_kicks']}, "
          f"leavers {off['leavers']}/{on['leavers']}, pings {off['kping'][0]}→{on['kping'][0]}, "
          f"fleet item {off['fleet_us']:.1f}→{on['fleet_us']:.1f}µs, digest {on['digest'][:16]}")

print("\nidentity (plain patched warm-on vs pristine HEAD, prof off):")
for arm in [a for a in ARMS if (W / f"{arm}-plain.json").exists() or (W / "m400-s3-plain.json").exists()]:
    pl, pr = load(arm + "-plain"), load(arm + "-pristine")
    if pl and pr:
        print(f"  {arm}: {'IDENTICAL' if pl['digest'] == pr['digest'] else 'DIFFER!'} {pl['digest'][:16]}")
    elif pl:
        print(f"  {arm}: plain digest {pl['digest'][:16]} (pristine missing)")
