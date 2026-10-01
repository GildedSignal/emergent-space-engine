#!/usr/bin/env python3
"""Adds the 64 eccentric births (the rung's e0<=0.3 half) to B14: truth + 3 candidates,
appended in the same order to truth_b14.json and cand_*.json, then metrics recomputed."""
import json, math, random, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import r10 as R
import stage2 as S
from run_driver import w_b14_one, w_cand_b14, jdump, jload, TAU, MU_B12, PERIODS_B14

T0 = time.time()
rng = random.Random(20261011)
births = R.b14_births(rng)[128:192]   # the eccentric half, first 64; parity from index 128+k
jobs = []
for k, (a, ph, e0) in enumerate(births):
    prog = ((128 + k) % 2 == 0)
    jobs.append((a, ph, e0, prog, False, 1e-12))
    jobs.append((a, ph, e0, prog, True, 1e-10))

def add_ecc():
    moons = jload("truth_b14.json")["moons"]
    if len(moons) != 64:
        print("unexpected moon count", len(moons)); raise SystemExit(1)

with ProcessPoolExecutor(2) as pool:
    res = list(pool.map(w_b14_one, jobs))
    moons = jload("truth_b14.json")["moons"]
    for k in range(64):
        base, nudge = res[2 * k], res[2 * k + 1]
        moons.append({"a": births[k][0], "phase": births[k][1], "e0": births[k][2],
                      "pro": ((128 + k) % 2 == 0),
                      "esc": None if base is None else base[0],
                      "rate": None if base is None else base[1],
                      "nfev": None if base is None else base[2],
                      "esc_nudge": None if nudge is None else nudge[0]})
    jdump({"moons": moons, "note": "64 circular + 64 eccentric births"}, "truth_b14.json")
    print("ecc truth merged", f"{time.time()-T0:.0f}s", flush=True)
    sc = R.Scene(MU_B12)
    for config in ["symba", "wh-fixed", "soi-switch"]:
        cd = jload(f"cand_{config}.json")
        extra = list(pool.map(w_cand_b14, [(config, *b) for b in births]))
        cd["b14"] += [{"esc": (r[0] if r else None), "rate": (r[1] if r else None),
                       "evals": (r[2] if r else None)} for r in extra]
        cd["evals_per_orbit"] += [None if r is None else r[2] / (PERIODS_B14 * sc.period /
                                 (TAU * math.sqrt((b[0] * sc.hill) ** 3 / sc.mu)))
                                  for r, b in zip(extra, births)]
        jdump(cd, f"cand_{config}.json")
        print(f"ecc candidates {config}", f"{time.time()-T0:.0f}s", flush=True)

S.stage_metrics()
print(f"stage3 total {time.time()-T0:.0f}s")
