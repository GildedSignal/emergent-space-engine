#!/usr/bin/env python3
"""Impact dose-response analysis for the plane bench (run 20261006-1101-quant-5457).

Burn pattern (script in xtask/src/universe/mod.rs): keys held while n % 240 < 20, n = 1..frames.
Decisions land at canonical ticks ≈ one per nominal frame, so wall frame n carries burn n%240<20.
"""
import json, sys

R = "lab/results/20261006-1101-quant-5457"
RUNS = ["coast", "L0", "L8", "L8b", "L15"]

def stats(xs):
    s = sorted(xs)
    def pct(q):
        return s[min(len(s) - 1, int(round((len(s) - 1) * q)))]
    return {"n": len(s), "mean": sum(s) / len(s), "p50": pct(0.5), "p99": pct(0.99), "max": s[-1]}

def load(name):
    return json.load(open(f"{R}/bench-{name}.json"))

def mask_burn(frames):
    return [n % 240 < 20 for n in range(1, frames + 1)]  # index 0 = frame 1

rows = []
for name in RUNS:
    d = load(name)
    N = d["series"]["frame_ms"].__len__()
    burn = mask_burn(N)
    # clean coast: not burn and >= 60 frames after any burn cluster ended
    clean = [not burn[i] and not any(burn[max(0, i - j)] for j in range(0, 60)) for i in range(N)]
    out = {"name": name, "N": N, "digest": d["digest"], "alive": d["player_alive"],
           "lost": d["lost_bodies"], "overflow": d["rtf"]["overflow_frames"],
           "rtf_med": d["rtf"]["median"], "rtf_low1": d["rtf"]["lowest_1pct"],
           "evps": d["events_per_second"], "inputs": d["decisions"]["taken"],
           "hitch_wall": d["hitch_counts"], "hitch_cpu": d["frame_cpu_ms"]["hitch_counts"] if "hitch_counts" in d["frame_cpu_ms"] else d["hitch_counts"],
           "worst_wall_ms": d["worst_hitch_ms"], "worst_at": d["worst_hitch_at_frame"],
           "parts_share": {k: v["share"] for k, v in d["where_the_time_goes_ms"].items()}}
    for key in ["cpu_ms", "engine_ms", "view_ms", "frame_ms"]:
        ser = d["series"][key]
        out[key] = {"burn": stats([ser[i] for i in range(N) if burn[i]]),
                    "coast": stats([ser[i] for i in range(N) if clean[i]])}
    # decay: mean cpu excess vs clean-coast mean, per frames-after-burn-end (cluster ends at n%240==19)
    coast_mean = out["cpu_ms"]["coast"]["mean"]
    dec = []
    for lag in range(0, 120):
        xs = []
        for i in range(N):
            n = i + 1
            if n % 240 == 20 + lag:  # lag frames after the cluster's last burn frame
                xs.append(d["series"]["cpu_ms"][i])
        if len(xs) >= 3:
            dec.append((lag, sum(xs) / len(xs) - coast_mean, len(xs)))
    out["decay_first_nonpositive_lag"] = next((l for l, e, _ in dec if e <= 0.02 * max(coast_mean, 1e-9)), None)
    out["decay_sample"] = dec[:12]
    # engine cost by kind (player row) and digest
    out["player_us_per_item"] = next((c["us_per_item"] for c in d["engine_cost_by_kind"] if c["kind"] == "player"), None)
    out["player_items"] = next((c["items"] for c in d["engine_cost_by_kind"] if c["kind"] == "player"), None)
    rows.append(out)

hdr = f"{'run':6} {'alive':5} {'ovfl':>5} {'rtfMed':>7} {'rtfLow1':>7} {'ev/s':>8} | {'cpu burn mean':>13} {'cpu coast mean':>14} {'ratio':>6} | {'eng burn':>9} {'eng coast':>9} | {'view burn':>9} {'view coast':>9} | {'wall p99.9':>10}"
print(hdr); print("-" * len(hdr))
for r in rows:
    cb, cc = r["cpu_ms"]["burn"]["mean"], r["cpu_ms"]["coast"]["mean"]
    print(f"{r['name']:6} {str(r['alive']):5} {r['overflow']:5} {r['rtf_med']:7.1f} {r['rtf_low1']:7.1f} {r['evps']:8.0f} | {cb:13.3f} {cc:14.3f} {cb/max(cc,1e-9):6.2f} | {r['engine_ms']['burn']['mean']:9.3f} {r['engine_ms']['coast']['mean']:9.3f} | {r['view_ms']['burn']['mean']:9.3f} {r['view_ms']['coast']['mean']:9.3f} | {r['frame_ms'] and 0 or 0:10.3f}")
print()
for r in rows:
    print(f"{r['name']:6} digest={r['digest'][:16]:16} worst_wall={r['worst_wall_ms']:.1f}ms@{r['worst_at']} hitches(wall 16.7/33/50)={r['hitch_wall']} hitches(cpu)={r['hitch_cpu']} decay_zero_lag={r['decay_first_nonpositive_lag']} player={r['player_us_per_item'] and round(r['player_us_per_item'],1)}us/item x{r['player_items']}")
    print(f"       cpu burn p99/max={r['cpu_ms']['burn']['p99']:.2f}/{r['cpu_ms']['burn']['max']:.2f}  coast p99/max={r['cpu_ms']['coast']['p99']:.2f}/{r['cpu_ms']['coast']['max']:.2f}  shares={ {k: round(v,3) for k,v in r['parts_share'].items()} }")
print()
print("decay (lag after burn end -> mean cpu excess ms):")
for r in rows:
    print(f"  {r['name']:6}", " ".join(f"{l}:{e:+.2f}" for l, e, _ in r["decay_sample"][:10]))
json.dump(rows, open(f"{R}/analysis.json", "w"), indent=1)
print("\nwrote analysis.json")
