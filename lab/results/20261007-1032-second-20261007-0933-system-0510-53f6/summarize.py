#!/usr/bin/env python3
"""Aggregate the decisive runs: B vs A vs B2 on the compiled-frequency away set.

Verdict rules are the ones pre-stated in predictions.md (E1 refutation of B,
E2 rescue criterion for B2).  Usage: python3 summarize.py  (reads run-*.json,
writes verdict.json, prints the tables).
"""
import glob
import json
import math

import numpy as np

MU = 9.5455e-4
C0 = 5.5469  # printed by exp2.py; recomputed runs match to 4 decimals

WIDTHS = {"C_half": C0 / 2, "C0": C0, "C_2x": 2 * C0}


def pooled(recs, C):
    sq = C * math.sqrt(MU)
    away = [r for r in recs if r["min_detunit"] >= sq]


def stats(v):
    if not v:
        return None
    v = sorted(v)
    n = len(v)
    med = v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])
    p90 = v[min(n - 1, int(math.ceil(0.9 * n)) - 1)]
    return dict(n=n, med=round(med, 3), p90=round(p90, 3), max=round(v[-1], 3))


def block(recs, C):
    sq = C * math.sqrt(MU)
    away = [r for r in recs if r["min_detunit"] >= sq]
    fails = [r for r in recs if r["relerr_rate_B"] > 2]
    fails_ex = [r for r in fails if r["min_detunit"] < sq]
    return dict(
        n=len(recs), n_excluded=len(recs) - len(away),
        fails=len(fails), fails_excluded=len(fails_ex),
        rate_B=stats([r["relerr_rate_B"] for r in away]),
        rate_A=stats([r["relerr_rate_A"] for r in away]),
        wrongsign_B=sum(r["wrongsign_B"] for r in away),
        wrongsign_A=sum(r["wrongsign_A"] for r in away),
        env_B=stats([r["err_env_B"] for r in away]),
        env_A=stats([r["err_env_A"] for r in away]),
        cadence=stats([r["ev_per_orbit"] for r in away]),
    )


def main():
    runs = {}
    for f in sorted(glob.glob("run-*.json")):
        d = json.load(open(f))
        key = (d["seed"], d["memo"], d["law"])
        runs[key] = d

    out = {"per_seed": {}, "pooled": {}, "correlation": {}, "near_band": {}}
    print(f"{'seed':>9} {'cfg':>8} {'C':>6} {'nex':>4} {'fails/ex':>8} "
          f"{'B p90/max/ws':>20} {'A p90/max/ws':>20} "
          f"{'envB p90':>9} {'envA p90':>9} {'cad':>5}")

    for (seed, memo, law), d in sorted(runs.items()):
        belt = [r for r in d["results"] if r["idx"] < 30]
        cfg = f"{law}/{memo}"
        out["per_seed"][f"{seed}-{cfg}"] = {}
        for cname, C in WIDTHS.items():
            b = block(belt, C)
            out["per_seed"][f"{seed}-{cfg}"][cname] = b
            print(f"{seed:>9} {cfg:>8} {cname:>6} {b['n_excluded']:>4} "
                  f"{b['fails']}/{b['fails_excluded']:>4} "
                  f"{b['rate_B']['p90']:>8.2f}/{b['rate_B']['max']:>7.2f}/{b['wrongsign_B']:>2}"
                  f"{'':<2}"
                  f"{b['rate_A']['p90']:>8.2f}/{b['rate_A']['max']:>7.2f}/{b['wrongsign_A']:>2}"
                  f"{b['env_B']['p90']:>9.3f} {b['env_A']['p90']:>9.3f} "
                  f"{b['cadence']['med']:>5.3f}")
        # mechanism correlation on the unfiltered belt (law B only, memo off)
        if law == "B" and memo == "off":
            inv_e = [1.0 / r["e0"] for r in belt]
            rel = [r["relerr_rate_B"] for r in belt]
            dw = [math.log10(max(r["min_detunit"] / C0, 1e-6)) for r in belt]
            out["correlation"][str(seed)] = dict(
                pearson_log_inve=round(float(np.corrcoef(np.log10(inv_e), np.log10([x + 1e-3 for x in rel]))[0, 1]), 3),
                pearson_log_dw=round(float(np.corrcoef(dw, np.log10([x + 1e-3 for x in rel]))[0, 1]), 3),
            )
        # near-band (scan) behaviour
        scan = [r for r in d["results"] if r["idx"] >= 30]
        out["near_band"][f"{seed}-{cfg}"] = [
            dict(a=r["a"], detune=round(100 * r["detune"], 2),
                 excluded_C0=r["excluded_C"][1],
                 relerr=r["relerr_rate_B"], pump_ratio=r["pump_ratio_B"])
            for r in scan]

    # pooled belts across seeds
    for cfg_sel, tag in ((("off", "B"), "B/off"), (("off", "B2"), "B2/off"), (("on", "B"), "B/on")):
        pool = []
        for (seed, memo, law), d in runs.items():
            if (memo, law) == cfg_sel:
                pool += [r for r in d["results"] if r["idx"] < 30]
        out["pooled"][tag] = {cname: block(pool, C) for cname, C in WIDTHS.items()}

    print("\nPooled belts (90 particles, 3 seeds):")
    for tag in ("B/on", "B/off", "B2/off"):
        for cname in WIDTHS:
            b = out["pooled"][tag][cname]
            print(f"  {tag:>6} {cname:>6}: n_ex={b['n_excluded']:>2} "
                  f"rate_B med/p90/max = {b['rate_B']['med']}/{b['rate_B']['p90']}/{b['rate_B']['max']}, "
                  f"ws={b['wrongsign_B']} | rate_A med/p90/max = "
                  f"{b['rate_A']['med']}/{b['rate_A']['p90']}/{b['rate_A']['max']}, ws={b['wrongsign_A']} "
                  f"| env_B p90={b['env_B']['p90']} env_A p90={b['env_A']['p90']} "
                  f"cad={b['cadence']['med']}")

    # pre-stated rescue criterion for B2 (predictions.md item 8)
    verdicts = []
    for seed in (20261007, 20261008, 20261009):
        b2 = out["per_seed"][f"{seed}-B2/off"]["C0"]
        ok = (b2["rate_B"]["p90"] <= b2["rate_A"]["p90"] + 0.3
              and b2["wrongsign_B"] <= 1
              and b2["env_B"]["p90"] <= b2["env_A"]["p90"])
        verdicts.append((seed, ok, b2["rate_B"]["p90"], b2["rate_A"]["p90"],
                         b2["wrongsign_B"], b2["env_B"]["p90"], b2["env_A"]["p90"]))
    out["b2_rescue_criterion"] = [dict(seed=s, ok=bool(o), p90_B2=p, p90_A=q,
                                       wrongsign_B2=w, envB_p90=e1, envA_p90=e2)
                                  for (s, o, p, q, w, e1, e2) in verdicts]
    print("\nB2 rescue criterion (pre-stated):",
          "ALL SEEDS PASS" if all(v[1] for v in verdicts) else "FAILED",
          verdicts)

    json.dump(out, open("verdict.json", "w"), indent=1)
    print("\nwritten: verdict.json")


if __name__ == "__main__":
    main()
