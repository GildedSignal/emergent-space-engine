#!/usr/bin/env python3
"""Assemble metrics.json from run_*.json (B12's rules: median exponent over judged
seeds, floor 1e-12, err_max 1e-4; ensemble fit = window-wise median across seeds)."""
import json, math, statistics, sys
import changeover as ch

FLOOR = 1e-12
def analyze(scheme):
    seeds = json.load(open("truth.json"))["seeds"]
    runs = json.load(open(f"run_{scheme}.json"))["schemes"][scheme]
    per = []
    for sd, r in zip(seeds, runs):
        err = r["err"]
        g = ch.growth_exponent(err)
        judged = max(err) > FLOOR
        per.append(dict(k=sd["k"], grp=sd["grp"], passes=sd.get("passes", 0),
                        med_peri=sd.get("med_peri", float("inf")),
                        ok=r["ok"], expo=g, judged=judged, maxerr=max(err),
                        events=r["events"], ev_per_pass=r["events"]/max(sd.get("passes",1),1),
                        kicks_per_orbit=r["kicks"]/ch.PERIODS,
                        inner_per_pass=r["inner"]/max(sd.get("passes",1),1),
                        restarts=r["restarts"], nsteps=r["nsteps_done"]))
    ok_judged = [p for p in per if p["ok"] and p["judged"]]
    med_expo = statistics.median([p["expo"] for p in ok_judged]) if ok_judged else None
    med_expo_all = statistics.median([p["expo"] for p in per if p["ok"]]) if any(p["ok"] for p in per) else None
    worst_max = max((p["maxerr"] for p in per if p["ok"]), default=float("inf"))
    med_evpp = statistics.median([p["ev_per_pass"] for p in per if p["ok"] and p["passes"]>0])
    med_kpo = statistics.median([p["kicks_per_orbit"] for p in per if p["ok"]])
    med_inner = statistics.median([p["inner_per_pass"] for p in per if p["ok"] and p["passes"]>0])
    # ensemble fit: window-wise median across judged seeds
    mats = [p for p in per if p["ok"] and p["judged"]]
    if mats:
        n = len(mats[0] and ch.NSAMP and json.load(open(f"run_{scheme}.json"))["schemes"][scheme][0]["err"])
        ens = []
        M = [json.load(open(f"run_{scheme}.json"))["schemes"][scheme][i]["err"]
             for i,p in enumerate(per) if p["ok"] and p["judged"]]
        ens = ch.growth_exponent([statistics.median(col) for col in zip(*M)])
    else:
        ens = None
    # periapsis bins (judged+ok only)
    bins = {}
    for lo, hi in [(0.0,0.3),(0.3,1.0),(1.0,3.0),(3.0,1e9)]:
        sel = [p for p in per if p["ok"] and p["judged"] and lo <= p["med_peri"] < hi]
        bins[f"{lo}-{hi if hi<1e8 else 'inf'}"] = dict(
            n=len(sel),
            med_expo=statistics.median([p["expo"] for p in sel]) if sel else None,
            med_maxerr=statistics.median([p["maxerr"] for p in sel]) if sel else None)
    return dict(median_expo_judged=med_expo, median_expo_all_ok=med_expo_all,
                ensemble_expo=ens, worst_maxerr_ok=worst_max,
                med_events_per_pass=med_evpp, med_kicks_per_orbit=med_kpo,
                med_inner_fevals_per_pass=med_inner,
                n_ok=sum(1 for p in per if p["ok"]), n_judged=len(ok_judged),
                n_total=len(per), restarts_total=sum(p["restarts"] for p in per),
                bins=bins, per_seed=[{k:v for k,v in p.items() if k!="nsteps"} for p in per])

if __name__ == "__main__":
    schemes = sys.argv[1:]
    out = {}
    for s in schemes:
        try:
            out[s] = analyze(s)
            a = out[s]
            print(f"{s:11s} med_expo(judged)={a['median_expo_judged']} ens={a['ensemble_expo']} "
                  f"worst={a['worst_maxerr_ok']:.1e} ev/pass={a['med_events_per_pass']:.1f} "
                  f"kicks/orb={a['med_kicks_per_orbit']:.0f} inner/pass={a['med_inner_fevals_per_pass']:.0f} "
                  f"ok={a['n_ok']}/{a['n_total']} judged={a['n_judged']} restarts={a['restarts_total']}")
            for b, v in a["bins"].items():
                if v["n"]:
                    print(f"   peri {b:8s} n={v['n']:2d} med_expo={v['med_expo']} med_max={v['med_maxerr']:.1e}")
        except FileNotFoundError as e:
            print(s, "missing:", e)
    json.dump(out, open("metrics.json", "w"), indent=1)
