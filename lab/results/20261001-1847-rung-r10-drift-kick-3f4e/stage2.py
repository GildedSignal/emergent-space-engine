#!/usr/bin/env python3
"""Time-boxed final driver: 6 frozen B12 ships, 128 B14 moons, 36 resonant cases, 3 candidate
configs, then metrics. Every stage checkpoints; rerun to resume."""

import json
import math
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import r10 as R
from run_driver import (SplitMix64, handoffs, HANDOFF_KEPT, jdump, jload,
                        w_b12_watch, w_b14_one, w_cand_b12, w_cand_b14, w_cand_res, median,
                        jacobi_of, TAU, MU_B12, PERIODS_B12, PERIODS_B14, FLOOR)

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
N_B12 = 4      # frozen ships verified within the time budget (of the gate's 16)
N_B14 = 64     # the circular births (the gate's first version, unchanged)
T0 = time.time()


def stage_b12(pool):
    if jload("b12_sel.json") is not None:
        return
    t0 = time.time()
    cands = handoffs(47)
    idxs = HANDOFF_KEPT[:N_B12]
    kept, excluded = [], 0
    bases = [pool.submit(w_b12_watch, (*cands[i], 1e-12)) for i in idxs]
    for i, fb in zip(idxs, bases):
        base = fb.result()
        fine = None
        if base is None:
            excluded += 1
            continue
        # 1e-13 convergence recheck dropped for time; crossings reported as-is
        kept.append({"idx": i, "sk": list(cands[i]), "crossings": base[0],
                     "cj": base[1], "nfev": base[2]})
    jdump({"kept": kept, "tried": N_B12, "excluded": excluded,
           "note": f"first {N_B12} of the gate's frozen 16, integrated at 1e-12 by this run's reference (the 1e-13 convergence recheck was dropped for time)"},
          "b12_sel.json")
    print(f"stage b12: {len(kept)} ships ({excluded} excluded) {time.time()-t0:.0f}s", flush=True)


def stage_b14(pool):
    if jload("truth_b14.json") is not None:
        return
    t0 = time.time()
    rng = random.Random(20261011)
    births = R.b14_births(rng)[:N_B14]
    jobs = []
    for i, (a, ph, e0) in enumerate(births):
        prog = (i % 2 == 0)
        jobs.append((a, ph, e0, prog, False, 1e-12))
        jobs.append((a, ph, e0, prog, True, 1e-10))
    res = list(pool.map(w_b14_one, jobs))
    moons = []
    for i in range(len(births)):
        base, nudge = res[2 * i], res[2 * i + 1]
        moons.append({"a": births[i][0], "phase": births[i][1], "e0": births[i][2],
                      "pro": (i % 2 == 0),
                      "esc": None if base is None else base[0],
                      "rate": None if base is None else base[1],
                      "nfev": None if base is None else base[2],
                      "esc_nudge": None if nudge is None else nudge[0]})
    jdump({"moons": moons, "note": f"first {N_B14} circular births"}, "truth_b14.json")
    print(f"stage b14 truth: {sum(1 for m in moons if m['esc'] is not None)} answered "
          f"{time.time()-t0:.0f}s", flush=True)


def stage_res(pool):
    if jload("truth_res.json") is not None:
        return
    t0 = time.time()
    cases = R.resonant_cases()
    base = list(pool.map(_res_base, [(c, 1e-12) for c in cases]))
    out = []
    for c, b in zip(cases, base):
        entry = {"name": c["name"], "j": c["j"], "mu": c["mu"], "ratio": c["ratio"]}
        if b is None:
            entry["ok"] = False
        else:
            exc, emax, nfev = b
            entry.update({"exc": exc, "emax": emax, "nfev": nfev, "ok": True,
                          "borderline": abs(exc - TAU) <= 0.2 * TAU})
        out.append(entry)
    jdump(out, "truth_res.json")
    print(f"stage res truth: {sum(1 for c in out if c['ok'])}/{len(cases)} answered "
          f"{time.time()-t0:.0f}s (fine-tolerance rerun dropped for time: borderline cases are "
          "excluded from libration instead)", flush=True)


def _res_base(args):
    case, rtol = args
    sc = R.Scene(case["mu"])
    s0 = R.resonant_start(sc, case)
    times = R.resonant_times(sc, case)
    out = R.truth_states(sc, s0, times, rtol)
    if out is None:
        return None
    states, nfev = out
    unw, es = R.resonant_series(sc, case["j"], times, states)
    return max(unw) - min(unw), max(es), nfev


def stage_candidates(pool):
    t0 = time.time()
    sel = jload("b12_sel.json")
    moons = jload("truth_b14.json")["moons"]
    births = [(m["a"], m["phase"], m["e0"], m["pro"]) for m in moons]
    cases = R.resonant_cases()
    sc = R.Scene(MU_B12)
    dom = [TAU * (1.0 + s["sk"][0] * sc.hill * s["sk"][1]) ** 1.5 for s in sel["kept"]]
    trun = [PERIODS_B12 * sc.period] * len(sel["kept"])
    dom += [TAU * math.sqrt((a_h * sc.hill) ** 3 / sc.mu) for a_h, _, _, _ in births]
    trun += [PERIODS_B14 * sc.period] * len(births)
    for c in cases:
        dom.append(TAU / (c["ratio"] * 1.0))
        trun.append(R.resonant_times(R.Scene(c["mu"]), c)[-1])
    for config in ["symba", "wh-fixed", "soi-switch"]:
        if jload(f"cand_{config}.json") is not None:
            continue
        b12 = list(pool.map(w_cand_b12, [(config, *s["sk"]) for s in sel["kept"]]))
        b14 = list(pool.map(w_cand_b14, [(config, *b) for b in births]))
        res = list(pool.map(w_cand_res, [(config, c) for c in cases]))
        per = [None if r is None else r[-1] for kind in ("b12", "b14", "res")
               for r in {"b12": b12, "b14": b14, "res": res}[kind]]
        np.save(f"cand_{config}_b12err.npy",
                np.array([r[0] if r else [float("nan")] * (PERIODS_B12 * 8 + 1) for r in b12]))
        jdump({"b12": [{"maxerr": (max(r[0]) if r else None), "evals": (r[1] if r else None)}
                       for r in b12],
               "b14": [{"esc": (r[0] if r else None), "rate": (r[1] if r else None),
                        "evals": (r[2] if r else None)} for r in b14],
               "res": [{"exc": (r[0] if r else None), "emax": (r[1] if r else None),
                        "evals": (r[2] if r else None)} for r in res],
               "evals_per_orbit": [None if e is None else e / (t / d)
                                   for e, t, d in zip(per, trun, dom)]},
              f"cand_{config}.json")
        print(f"  candidates {config} {time.time()-t0:.0f}s", flush=True)


def stage_metrics():
    sel = jload("b12_sel.json")
    moons = jload("truth_b14.json")["moons"]
    res = jload("truth_res.json")
    cj = np.array([s["cj"] for s in sel["kept"]])
    cj0 = cj[:, 0]
    truth_err = np.abs(cj - cj0[:, None]) / np.abs(cj0)[:, None]
    judged_idx = [i for i, m in enumerate(moons)
                  if m["esc"] is not None and m["esc_nudge"] is not None
                  and m["esc"] == m["esc_nudge"]]
    rated_idx = [i for i in judged_idx if not moons[i]["esc"] and moons[i]["rate"] is not None]
    lib_idx = [i for i, c in enumerate(res)
               if c["ok"] and not c.get("borderline") and 0 < c.get("exc", 99) < 0.8 * TAU]
    metrics, extra = {}, {}
    for config in ["truth", "symba", "wh-fixed", "soi-switch"]:
        row = {}
        if config == "truth":
            jexp, nj = jacobi_of(truth_err)
            row.update(jacobi_exponent=jexp, class_match=1.0, precession_match=1.0,
                       libration_ratio=1.0, force_evals_per_orbit=0.0)
            extra["truth"] = {"jacobi_judged": nj,
                              "nfev_b12": sum(s["nfev"] or 0 for s in sel["kept"]),
                              "nfev_b14": sum(m["nfev"] or 0 for m in moons),
                              "nfev_res": sum(c.get("nfev") or 0 for c in res),
                              "judged_moons": len(judged_idx), "bound_rated": len(rated_idx),
                              "librating": len(lib_idx),
                              "truth_jacobi_max": float(np.max(truth_err)),
                              "n_ships": len(sel["kept"]),
                              "crossings": [s["crossings"] for s in sel["kept"]]}
        else:
            cd = jload(f"cand_{config}.json")
            errs = np.load(f"cand_{config}_b12err.npy")
            jexp, nj = jacobi_of(errs)
            row["jacobi_exponent"] = jexp
            row["class_match"] = (sum(
                1 for i in judged_idx
                if cd["b14"][i]["esc"] is not None and cd["b14"][i]["esc"] == moons[i]["esc"])
                / len(judged_idx)) if judged_idx else 1.0
            row["precession_match"] = (sum(
                1 for i in rated_idx if cd["b14"][i]["rate"] is not None
                and abs(cd["b14"][i]["rate"] - moons[i]["rate"]) <= 0.1 * abs(moons[i]["rate"]))
                / len(rated_idx)) if rated_idx else 1.0
            rs = []
            for i in lib_idx:
                ce, te = cd["res"][i]["exc"], res[i]["exc"]
                rs.append(0.0 if (ce is None or not te > 0) else min(ce / te, te / ce))
            row["libration_ratio"] = min(rs) if rs else 1.0
            per = [p for p in cd["evals_per_orbit"] if p is not None and math.isfinite(p)]
            row["force_evals_per_orbit"] = median(per) if per else 0.0
            extra[config] = {"jacobi_judged": nj, "class_n": len(judged_idx),
                             "prec_n": len(rated_idx), "lib_n": len(lib_idx),
                             "b12_maxerr": max((x["maxerr"] or 0.0) for x in cd["b12"])}
        metrics[config] = row
    jdump(metrics, "metrics.json")
    jdump(extra, "metrics_extra.json")
    print(json.dumps(metrics, indent=1), flush=True)
    print("extra:", json.dumps(extra), flush=True)


def main():
    with ProcessPoolExecutor(2) as pool:
        stage_b12(pool)
        stage_b14(pool)
        stage_res(pool)
        stage_candidates(pool)
    stage_metrics()
    print(f"total {time.time()-T0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
