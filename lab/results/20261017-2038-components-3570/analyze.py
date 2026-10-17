#!/usr/bin/env python3
"""Census of boundary vs kick events from BOUND_PROBE lines (20261017-2038-components-3570)."""
import sys, json, collections

def load(path):
    rows = []
    for line in open(path):
        if not line.startswith("EV "):
            continue
        p = line.split()
        d = {"what": p[1], "t": int(p[2]), "i": int(p[3])}
        for kv in p[4:]:
            k, v = kv.split("=")
            d[k] = int(v)
        rows.append(d)
    return rows

def pct(xs, p):
    if not xs:
        return 0
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int((len(xs) - 1) * p + 0.999999))]

rows = load(sys.argv[1])
B = [r for r in rows if r["what"] == "B"]
K = [r for r in rows if r["what"] == "K"]
out = {"events": len(rows), "boundaries": len(B), "kicks": len(K),
       "parity_B_over_K": round(len(B) / max(1, len(K)), 4)}

bs = [r for r in B if r["traj"] != 99]           # boundary reached its readout
noop = [r for r in bs if r["iv"] == r["iv0"] and r["st"] == r["st0"] and r["dead"] == 0]
out["boundary_noop_frac"] = round(len(noop) / max(1, len(bs)), 4)
out["boundary_dead"] = sum(r["dead"] and not r["dead0"] for r in bs)
out["boundary_step_change"] = sum(r["st"] != r["st0"] for r in bs)
out["boundary_interval_change"] = sum(r["iv"] != r["iv0"] for r in bs)
out["boundary_plan_grew"] = sum(r["pl"] != r["pl0"] for r in bs)

margin = lambda rs, k: collections.Counter(r[k] for r in rs)
out["ms_hist"] = dict(sorted(margin(bs, "ms").items()))
out["me_hist"] = dict(sorted(margin(bs, "me").items()))
deep_edge = sum(1 for r in bs if r["me"] <= -4)
near_surf = sum(1 for r in bs if r["ms"] <= 1)
out["me_le_-4_frac"] = round(deep_edge / max(1, len(bs)), 4)
out["ms_le_1_frac"] = round(near_surf / max(1, len(bs)), 4)
out["doll_hist"] = dict(sorted(collections.Counter(r["doll"] for r in bs).items()))
out["traj_hist"] = dict(sorted(collections.Counter(r["traj"] for r in bs).items()))

def walls(rs):
    ns = [r["ns"] for r in rs]
    return {"n": len(ns), "p50_us": round(pct(ns, 0.5) / 1000, 2), "p99_us": round(pct(ns, 0.99) / 1000, 2),
            "mean_us": round(sum(ns) / max(1, len(ns)) / 1000, 2)}
out["boundary_wall"] = walls(bs)
out["kick_wall"] = walls(K)
kb = out["kick_wall"]["p50_us"] / max(0.01, out["boundary_wall"]["p50_us"])
out["kick_over_boundary_p50"] = round(kb, 2)

# news-carrying boundaries: anything that changed state the previous plan did not already hold
news = [r for r in bs if r["iv"] != r["iv0"] or r["st"] != r["st0"] or (r["dead"] and not r["dead0"])]
out["news_frac"] = round(len(news) / max(1, len(bs)), 4)
# hypothetical: if all noop boundaries were deleted, boundary-CPU saved
bmean = out["boundary_wall"]["mean_us"]
out["saved_us_per_game_s"] = round(len(noop) * bmean / 270000, 1)  # 150s*1800 = 270k game-s
out["belt_cpu_saved_frac"] = round(len(noop) * bmean / max(1, (len(K) * out["kick_wall"]["mean_us"] + len(bs) * bmean)), 4)
print(json.dumps(out, indent=1))
