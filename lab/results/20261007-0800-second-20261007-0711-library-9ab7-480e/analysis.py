#!/usr/bin/env python3
"""Tail analysis of the shipped plane's event stream (run ...480e).

Loads the 48-byte records written by probe/src/main.rs, pools per config, and prints
the decision numbers: order statistics of the demand stream (integers: judged
directly), Hill alpha-hat trajectories of the cost streams (continuous), the
bench-window vs hour hazard, seed-maxima stability (boundedness), and the
composition of the heaviest frames. Writes analysis.json.
"""
import glob
import json
import sys

import numpy as np

DT = np.dtype({
    "names": ["frame", "ev", "kicks", "opens", "boundaries", "handoffs", "slices",
              "decisions", "encounters", "leavers", "refused", "lost",
              "frame_ms", "items_us", "top1_us", "kind"],
    "formats": ["<u4", "<u4", "<u4"] + ["<u2"] * 9 + ["<f4", "<f4", "<f4", "u1"],
    "offsets": [0, 4, 8, 12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 44],
    "itemsize": 48,
})

def load(prefix):
    parts = sorted(glob.glob(prefix + ".*"), key=lambda p: int(p.rsplit(".", 1)[1]))
    return np.concatenate([np.fromfile(p, dtype=DT) for p in parts])

def qs(x, ps=(0.5, 0.99, 0.999)):
    return {"p50": float(np.quantile(x, ps[0])), "p99": float(np.quantile(x, ps[1])),
            "p999": float(np.quantile(x, ps[2])), "max": float(np.max(x))}

def hill(xs, fracs=(0.001, 0.003, 0.01, 0.03)):
    """alpha-hat of the Pareto tail at k = frac*n upper order statistics."""
    xs = np.sort(np.asarray(xs, dtype=float))
    n = len(xs)
    ln = np.log(xs)
    csum = np.cumsum(ln)
    out = {}
    for f in fracs:
        k = int(np.clip(f * n, 10, n // 2))
        s = csum[n - 1] - csum[n - k - 1] - k * ln[n - k - 1]
        out[f"k={k}({f:.1%})"] = round(float(k / s), 3) if s > 0 else None
    return out

def hill_traj(xs, npts=24):
    """alpha-hat over a log grid of k, for plateau reading."""
    xs = np.sort(np.asarray(xs, dtype=float))
    n = len(xs)
    ln = np.log(xs)
    csum = np.cumsum(ln)
    ks = np.unique(np.round(np.geomspace(30, max(n // 20, 60), npts)).astype(int))
    traj = []
    for k in ks:
        k = int(min(k, n // 2))
        s = csum[n - 1] - csum[n - k - 1] - k * ln[n - k - 1]
        traj.append((k, round(float(k / s), 3) if s > 0 else None))
    return traj

def bench_vs_hour(rec, window=3300, skip=300):
    """55-s bench windows at 60 fps: p99.9 per window vs the run's worst frame."""
    ev = rec["ev"][skip:].astype(float)
    nw = len(ev) // window
    if nw < 2:
        return None
    wp = np.array([np.quantile(ev[i * window:(i + 1) * window], 0.999) for i in range(nw)])
    return {
        "windows": int(nw),
        "bench_p999_median": float(np.median(wp)),
        "bench_p999_max": float(wp.max()),
        "hour_max": float(ev.max()),
        "hour_over_bench_median": float(ev.max() / max(np.median(wp), 1e-9)),
        "hour_over_bench_max": float(ev.max() / max(wp.max(), 1e-9)),
    }

def analyze(name, prefixes, window=3300):
    recs = {p: load(p) for p in prefixes}
    allr = np.concatenate(list(recs.values()))
    skip = 300
    body = allr[skip:]
    ev = body["ev"].astype(float)
    top = body["top1_us"].astype(float)
    top = top[top > 0]
    ms = body["frame_ms"].astype(float)
    ius = body["items_us"].astype(float)
    ius = ius[ius > 0]
    out = {
        "frames": int(len(allr)), "frames_body": int(len(body)), "seeds": len(prefixes),
        "items_total": int(allr["ev"].sum()),
        "items_us": qs(ius), "items_us_hill": hill(ius),
        "demand": qs(ev),
        "demand_per_seed_max": [int(r["ev"].max()) for r in recs.values()],
        "demand_pooled_max_over_p999": float(ev.max() / max(np.quantile(ev, 0.999), 1e-9)),
        "demand_max_over_p99": float(ev.max() / max(np.quantile(ev, 0.99), 1e-9)),
        "cost_top1": qs(top), "cost_top1_hill": hill(top), "cost_hill_traj": hill_traj(top),
        "cost_pooled_max_over_p999": float(top.max() / max(np.quantile(top, 0.999), 1e-9)),
        "cost_per_seed_max": [round(float(r["top1_us"].max()), 1) for r in recs.values()],
        "frame_ms": qs(ms), "frame_ms_pooled_max_over_p999": float(ms.max() / max(np.quantile(ms, 0.999), 1e-9)),
        "frame_ms_per_seed_max_over_p99": [round(float(r["frame_ms"].max() / max(np.quantile(r["frame_ms"], 0.99), 1e-9)), 2) for r in recs.values()],
        "items_us": qs(ius), "items_us_hill": hill(ius),
        "top_item_kinds": {n: int((body["top1_us"] > np.quantile(top, 0.99))[body[body["top1_us"] > 0]["kind"].argsort()[:0]].sum()) for n in ()},  # replaced below
        "bench_vs_hour_pooled": bench_vs_hour(allr, window),
    }
    # composition of the heaviest frames (top 0.1% by demand) and of the top 1% items' kinds
    thr = np.quantile(ev, 0.999)
    heavy = body[ev >= thr]
    out["heavy_frames"] = {
        "count": int(len(heavy)),
        "mean": {k: round(float(heavy[k].mean()), 3) for k in ("kicks", "opens", "boundaries", "handoffs", "slices", "decisions", "encounters", "leavers")},
    }
    out["all_frames_mean"] = {k: round(float(body[k].mean()), 4) for k in ("kicks", "opens", "boundaries", "handoffs", "slices", "decisions", "encounters", "leavers")}
    t1 = body[body["top1_us"] > 0]
    thr99 = np.quantile(t1["top1_us"], 0.99)
    kinds = t1[t1["top1_us"] >= thr99]["kind"]
    names = ["planet", "moon", "ship", "player", "fleet", "?"]
    out["top_item_kinds"] = {names[k]: int((kinds == k).sum()) for k in range(6) if (kinds == k).sum()}
    # event rate in thirds (does the stream die: battle over?)
    third = len(body) // 3
    out["ev_rate_thirds"] = [round(float(body[i * third:(i + 1) * third]["ev"].mean()), 3) for i in range(3)]
    return out

def main():
    res = {}
    res["A_rtf1_m48"] = analyze("A", [f"data/A_s{s}" for s in range(1, 16)])
    res["H_hour_s99"] = analyze("H", ["data/H_s99"], window=3300)
    res["B_rtf16_m48"] = analyze("B", [f"data/B_s{s}" for s in range(1, 5)])
    res["C_rtf1_m400"] = analyze("C", [f"data/C_s{s}" for s in range(1, 5)])
    json.dump(res, open("analysis.json", "w"), indent=1)
    for k, v in res.items():
        print(f"== {k}")
        for kk, vv in v.items():
            if kk not in ("cost_hill_traj",):
                print(f"  {kk}: {vv}")
        print(f"  cost_hill_traj (k, alpha_hat): {v['cost_hill_traj']}")

if __name__ == "__main__":
    main()
