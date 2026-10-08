#!/usr/bin/env python3
"""Regenerates every number quoted in dossier.md from the saved CSV/JSON runs.

Usage: python3 analyze.py   (in this folder; prints the evidence block).
Runs were produced by the commands in dossier.md (xtask at this commit + the
FRAME_CSV patch, saved by run.sh as the run's diff).
"""
import json, csv, statistics

def load(tag):
    j = json.load(open(f"{tag}.json"))
    rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(open(f"{tag}.csv"))]
    return j, rows

def q(v, p):
    s = sorted(v)
    return s[min(len(s) - 1, int(round((len(s) - 1) * p)))]

# --- P1: view owns the frame at the flown point, fresh seeds ---
for tag in ["a-rtf100-s7", "a-rtf100-s20261008"]:
    j, rows = load(tag)
    w = j["where_the_time_goes_ms"]
    tot = sum(w[k]["share"] for k in w)
    print(f"{tag}: frames={len(rows)} frame p50/p99/p99.9={j['frame_ms']['p50']:.2f}/{j['frame_ms']['p99']:.2f}/{j['frame_ms']['p99.9']:.2f} ms "
          f"hitches>16.7ms={j['hitch_counts'][0]} overflow={j['rtf']['overflow_frames']}")
    print(f"  shares: view_gather={w['view_gather']['share']/tot:.1%} engine={w['engine']['share']/tot:.1%} "
          f"json={w['view_json']['share']/tot:.1%} wire={w['wire']['share']/tot:.1%}; view p50={w['view_gather']['p50']:.2f} ms")

# --- P2: unpaced rtf ladder (hot loop) never approaches the deadline; budget caps the engine ---
for r in [30, 100, 300, 1000]:
    j, rows = load(f"b-unpaced-rtf{r}")
    w = j["where_the_time_goes_ms"]
    print(f"unpaced rtf{r:>4}: frame p50/p99={j['frame_ms']['p50']:.2f}/{j['frame_ms']['p99']:.2f} engine p50/p99/max={w['engine']['p50']:.2f}/{w['engine']['p99']:.2f}/{w['engine']['max']:.2f} "
          f"view p50={w['view_gather']['p50']:.2f} events/s={j['events_per_second']:.0f}")

# --- the paced tax: same rtf, paced vs unpaced ---
jp, rp = load("a-rtf100-s7")
ju, ru = load("b-unpaced-rtf100")
for name, rows_ in [("paced  ", rp), ("unpaced", ru)]:
    v = [r["view_ms"] for r in rows_]; e = [r["engine_ms"] for r in rows_]
    c = [r["cpu_ms"] for r in rows_]; f = [r["frame_ms"] for r in rows_]
    print(f"{name} rtf100: view p50={q(v,0.5):.2f} engine p50={q(e,0.5):.2f} frame p50={q(f,0.5):.2f} cpu p50={q(c,0.5):.2f} (cpu~frame => compute, not stall)")
tax_v = q([r["view_ms"] for r in rp], 0.5) / q([r["view_ms"] for r in ru], 0.5)
tax_e = q([r["engine_ms"] for r in rp], 0.5) / q([r["engine_ms"] for r in ru], 0.5)
print(f"paced/hot p50 ratio: view {tax_v:.1f}x, engine {tax_e:.1f}x")

# --- P3: burst concentration + budget overshoot by single items ---
for tag in ["a-rtf100-s7", "a-rtf100-s20261008"]:
    j, rows = load(tag)
    e = sorted((r["engine_ms"] for r in rows), reverse=True)
    top10 = sum(e[:max(1, len(e)//10)]) / max(sum(e), 1e-9)
    hi = [r for r in rows if r["engine_ms"] > 6.0]
    print(f"{tag}: engine top10% frames carry {top10:.0%} of engine time; frames >6ms: {len(hi)}, "
          f"events on them p50={q([r['events'] for r in hi],0.5):.0f} (engine max={e[0]:.1f} ms vs 5.0 ms budget)")

# --- P4: an order's impact at real time ---
j, rows = load("c-rtf1")
n = len(rows)
burn = [i for i in range(n) if 0 < (i+1) % 240 < 20]
coast = [i for i in range(n) if i not in set(burn)]
for key in ["cpu_ms", "engine_ms"]:
    b = q([rows[i][key] for i in burn], 0.99); c = q([rows[i][key] for i in coast], 0.99)
    print(f"rtf1 {key}: burn p99={b:.2f} coast p99={c:.2f} ratio={b/max(c,1e-9):.2f}")
w = j["where_the_time_goes_ms"]; tot = sum(w[k]["share"] for k in w)
print(f"rtf1 shares: view={w['view_gather']['share']/tot:.1%} engine={w['engine']['share']/tot:.1%}; worst={j['worst_hitch_ms']:.1f} ms hitches={j['hitch_counts']}")

# --- P5: engine time by kind (paced, flown point) ---
c = json.load(open("a-rtf100-s7.json"))["engine_cost_by_kind"]
tot = sum(x["total_ms"] for x in c)
for x in c:
    if x["items"]:
        print(f"  {x['kind']:<7} {x['total_ms']:7.0f} ms ({x['total_ms']/tot:.0%}), {x['items']} items, {x['us_per_item']:.0f} us/item")

# --- machine state as recorded by the bench ---
print("load before/after (a-rtf100-s7):", json.load(open("a-rtf100-s7.json"))["uptime_before"], "|", json.load(open("a-rtf100-s7.json"))["uptime_after"])
