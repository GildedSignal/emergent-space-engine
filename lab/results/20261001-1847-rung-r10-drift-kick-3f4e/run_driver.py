#!/usr/bin/env python3
"""Drives rung r10: truth + three split integrators on B12/B14/r4v3 cases, then metrics."""

import json
import math
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import r10 as R

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
TAU = R.TAU
MU_B12 = 1e-3
PERIODS_B12 = 200
PERIODS_B14 = 50
FLOOR = 1e-12
CONFIGS = ["truth", "symba", "wh-fixed", "soi-switch"]


def jload(name):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def jdump(obj, name):
    with open(os.path.join(HERE, name), "w") as f:
        json.dump(obj, f)


# ---------------------------------------------------------------- workers (top level for pickling)


def w_b12_watch(args):
    """Reference on one candidate: crossings at P/256, coarse Jacobi at P/8, nfev."""
    side, k, alpha, rtol = args
    sc = R.Scene(MU_B12)
    s0 = R.b12_ship(sc, side, k, alpha)
    times = [j * sc.period / 256 for j in range(PERIODS_B12 * 256 + 1)]
    out = R.truth_states(sc, s0, times, rtol)
    if out is None:
        return None
    states, nfev = out
    inside = None
    crossings = 0
    cj = []
    for t, s in zip(times, states):
        now = sc.planet_distance(t, s) < sc.soi
        if inside is not None and now != inside:
            crossings += 1
        inside = now
        if abs((t / sc.period) * 8.0 - round((t / sc.period) * 8.0)) < 1e-9:
            cj.append(sc.jacobi(t, s))
    return crossings, cj, nfev

def w_b14_one(args):
    """Truth verdict on one moon: class (+ nudge class), apsidal rate, nfev; stops at escape."""
    a_hill, phase, e0, prograde, nudge, rtol = args
    sc = R.Scene(MU_B12)
    a = a_hill * (1.0 + (1e-6 if nudge else 0.0))
    s0 = R.b14_moon_state(sc, a, phase, e0, prograde)
    times = [j * sc.period / 64 for j in range(1, PERIODS_B14 * 64 + 1)]
    out = R.truth_states_escape(sc, s0, times, rtol, 1.5)
    if out is None:
        return None
    states, nfev, esc = out
    rate = None if esc else R.apsidal_rate(sc, times[:len(states)], states)
    return esc, rate, nfev
def w_res_one(args):
    """Truth on one resonant case: excursion of the unwrapped angle, e_max, nfev."""
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


def w_cand_b12(args):
    """One candidate config on one B12 ship: Jacobi error series at P/8, evals."""
    config, side, k, alpha = args
    sc = R.Scene(MU_B12)
    s0 = R.b12_ship(sc, side, k, alpha)
    times = [j * sc.period / 8 for j in range(1, PERIODS_B12 * 8 + 1)]
    out = R.run_candidate(sc, s0, config, times[-1], times)
    if out is None:
        return None
    samples, evals = out
    cj0 = sc.jacobi(0.0, s0)
    err = [0.0] + [abs(sc.jacobi(t, s) - cj0) / abs(cj0) for t, s in samples]
    return err, evals


def w_cand_b14(args):
    config, a_hill, phase, e0, prograde = args
    sc = R.Scene(MU_B12)
    s0 = R.b14_moon_state(sc, a_hill, phase, e0, prograde)
    times = [j * sc.period / 64 for j in range(1, PERIODS_B14 * 64 + 1)]
    out = R.run_candidate(sc, s0, config, times[-1], times)
    if out is None:
        return None
    samples, evals = out
    esc = False
    kept = []
    for t, s in samples:
        kept.append(s)
        if sc.planet_distance(t, s) > 1.5 * sc.hill:
            esc = True
            break
    rate = None if esc else R.apsidal_rate(sc, times[:len(kept)], kept)
    return esc, rate, evals


def w_cand_res(args):
    config, case = args
    sc = R.Scene(case["mu"])
    s0 = R.resonant_start(sc, case)
    times = R.resonant_times(sc, case)
    # detuned ratios are not commensurate with the planet grid: the case's own base step is
    # the ship period / 96, so every sample (P1/8) is exactly 12 steps
    p1 = TAU / (case["ratio"] * sc.omega)
    H = p1 / 96.0
    n_steps = int(round(times[-1] / H))
    idx = [int(round(t / H)) for t in times]
    r = R.Runner(sc, s0, config, H, n_steps)
    try:
        samples, evals = r.run(idx)
    except (RuntimeError, OverflowError, ValueError):
        return None
    out = (samples, evals)
    samples, evals = out
    unw, es = R.resonant_series(sc, case["j"], times, [s for _, s in samples])
    return max(unw) - min(unw), max(es), evals


# ---------------------------------------------------------------- stages


M64 = (1 << 64) - 1
HANDOFF_KEPT = [1, 2, 12, 14, 15, 19, 22, 23, 25, 30, 31, 32, 35, 39, 45, 46]


class SplitMix64:
    """Port of sample.rs Rng (Steele, Lea and Flood 2014)."""

    def __init__(self, seed):
        self.s = seed & M64

    def nxt(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & M64
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
        return z ^ (z >> 31)

    def unit(self):
        return (self.nxt() >> 11) / float(1 << 53)


def handoffs(n):
    """(side, k, alpha) exactly as xtask/src/behave/sample.rs handoffs()."""
    rng = SplitMix64(20261002)
    out = []
    for _ in range(n):
        side = 1.0 if (rng.nxt() >> 63) == 1 else -1.0
        k = 1.5 + 1.5 * rng.unit()
        alpha = math.radians(30.0 + 300.0 * rng.unit())
        out.append((side, k, alpha))
    return out


def stage_b12_select(pool):
    """The frozen ships: SplitMix64(20261002) draws, the gate's frozen HANDOFF_KEPT indices.
    Each ship is verified by this run's reference (crossings counted, 1e-12 vs 1e-13
    convergence checked); non-converged ships are excluded and counted."""
    t0 = time.time()
    cands = handoffs(47)
    kept, excluded = [], 0
    for group in range(0, len(HANDOFF_KEPT), 4):
        idxs = HANDOFF_KEPT[group:group + 4]
        bases = [pool.submit(w_b12_watch, (*cands[i], 1e-12)) for i in idxs]
        fines = [pool.submit(w_b12_watch, (*cands[i], 1e-13)) for i in idxs]
        for i, fb, ff in zip(idxs, bases, fines):
            base, fine = fb.result(), ff.result()
            if base is None:
                excluded += 1
                continue
            converged = False
            if fine is not None and len(fine[1]) == len(base[1]):
                c0 = base[1][0]
                converged = all(abs(b - a) / abs(c0) <= 1e-9
                                for a, b in zip(base[1], fine[1]))
            if converged:
                kept.append({"idx": i, "sk": list(cands[i]), "crossings": base[0],
                             "cj": base[1], "nfev": base[2]})
            else:
                excluded += 1
        print(f"  b12 select: {len(kept)}/{len(HANDOFF_KEPT)} converged "
              f"({time.time()-t0:.0f}s)", flush=True)
    jdump({"kept": kept, "tried": 47, "excluded": excluded,
           "crossings": [k["crossings"] for k in kept]}, "b12_sel.json")
    print(f"stage b12 select: {len(kept)} ships, excluded {excluded}, {time.time()-t0:.0f}s",
          flush=True)


def stage_b14_truth(pool):
    t0 = time.time()
    rng = random.Random(20261011)
    births = R.b14_births(rng)
    jobs = []
    for i, (a, ph, e0) in enumerate(births):
        prog = (i % 2 == 0)
        jobs.append((a, ph, e0, prog, False, 1e-12))
        jobs.append((a, ph, e0, prog, True, 3e-11))
    res = list(pool.map(w_b14_one, jobs))
    moons = []
    for i in range(len(births)):
        base, nudge = res[2 * i], res[2 * i + 1]
        moons.append({
            "a": births[i][0], "phase": births[i][1], "e0": births[i][2], "pro": (i % 2 == 0),
            "esc": None if base is None else base[0],
            "rate": None if base is None else base[1],
            "nfev": None if base is None else base[2],
            "esc_nudge": None if nudge is None else nudge[0],
        })
    jdump({"moons": moons}, "truth_b14.json")
    print(f"stage b14 truth: {sum(1 for m in moons if m['esc'] is not None)} answered, "
          f"{time.time()-t0:.0f}s", flush=True)


def stage_res_truth(pool):
    t0 = time.time()
    cases = R.resonant_cases()
    base = list(pool.map(w_res_one, [(c, 1e-12) for c in cases]))
    fine = list(pool.map(w_res_one, [(c, 1e-13) for c in cases]))
    out = []
    for c, b, fn in zip(cases, base, fine):
        entry = {"name": c["name"], "j": c["j"], "mu": c["mu"], "ratio": c["ratio"]}
        if b is not None:
            exc, emax, nfev = b
            entry.update({"exc": exc, "emax": emax, "nfev": nfev,
                          "ok": bool(fn is not None and abs(fn[1] - emax) <= 1e-3
                                     and abs(fn[0] - exc) <= 0.01 * exc)})
        else:
            entry["ok"] = False
        out.append(entry)
    jdump(out, "truth_res.json")
    print(f"stage res truth: {sum(1 for c in out if c['ok'])}/{len(cases)} converged, "
          f"{time.time()-t0:.0f}s", flush=True)


def stage_candidates(pool):
    t0 = time.time()
    sel = jload("b12_sel.json")
    moons = jload("truth_b14.json")["moons"]
    births = [(m["a"], m["phase"], m["e0"], m["pro"]) for m in moons]
    cases = R.resonant_cases()
    sc = R.Scene(MU_B12)
    # per-body dominant periods and run lengths, for the cost metric
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
        per = []
        for kind, runs in (("b12", b12), ("b14", b14), ("res", res)):
            for r in runs:
                per.append(None if r is None else r[-1])
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
        print(f"  candidates {config}: {time.time()-t0:.0f}s", flush=True)
    print(f"stage candidates done: {time.time()-t0:.0f}s", flush=True)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def jacobi_of(errmat):
    """(median exponent over ships above the floor, how many were judged)."""
    exps = []
    for row in errmat:
        row = list(row)
        if any(not math.isfinite(e) for e in row):
            exps.append(10.0)
            continue
        if max(row[1:], default=0.0) <= FLOOR:
            continue
        g = R.growth_exponent(row)
        exps.append(10.0 if math.isnan(g) else max(g, 0.0))
    return (median(exps) if exps else 0.0), len(exps)


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
    lib_idx = [i for i, c in enumerate(res) if c["ok"] and c.get("exc") is not None
               and c["exc"] < (1 - 0.2) * TAU]

    metrics, extra = {}, {}
    for config in CONFIGS:
        row = {}
        if config == "truth":
            jexp, nj = jacobi_of(truth_err)
            row.update(jacobi_exponent=jexp, class_match=1.0, precession_match=1.0,
                       libration_ratio=1.0, force_evals_per_orbit=0.0)
            extra["truth"] = {
                "jacobi_judged": nj,
                "nfev_b12": sum(s["nfev"] or 0 for s in sel["kept"]),
                "nfev_b14": sum(m["nfev"] or 0 for m in moons),
                "nfev_res": sum(c.get("nfev") or 0 for c in res),
                "judged_moons": len(judged_idx), "bound_rated": len(rated_idx),
                "librating": len(lib_idx), "truth_jacobi_max": float(np.max(truth_err))}
        else:
            cd = jload(f"cand_{config}.json")
            errs = np.load(f"cand_{config}_b12err.npy")
            jexp, nj = jacobi_of(errs)
            row["jacobi_exponent"] = jexp
            n_ok = sum(1 for i in judged_idx
                       if cd["b14"][i]["esc"] is not None and cd["b14"][i]["esc"] == moons[i]["esc"])
            row["class_match"] = n_ok / len(judged_idx) if judged_idx else 1.0
            n_ok = sum(1 for i in rated_idx if cd["b14"][i]["rate"] is not None
                       and abs(cd["b14"][i]["rate"] - moons[i]["rate"]) <= 0.1 * abs(moons[i]["rate"]))
            row["precession_match"] = n_ok / len(rated_idx) if rated_idx else 1.0
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
    print(json.dumps(metrics, indent=1))
    print("extra:", json.dumps(extra))


def main():
    t0 = time.time()
    with ProcessPoolExecutor(2) as pool:
        if jload("b12_sel.json") is None:
            stage_b12_select(pool)
        if jload("truth_b14.json") is None:
            stage_b14_truth(pool)
        if jload("truth_res.json") is None:
            stage_res_truth(pool)
        stage_candidates(pool)
    stage_metrics()
    print(f"total {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
