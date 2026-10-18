#!/usr/bin/env python3
"""Same-convention ladder analysis for the 10^6-gap slice (second author on 2403).

The second checker's convention nit fixed here: the burn/coast multiplier is
distinct/distinct, BOTH sides restricted to the same window (game time >= 150 s,
the birth transient cut), and both sides flown under this run's own harness at the
same wall seconds and budget.

Inputs per arm: out/lad-<arm>.txt (nladder stdout; the `ladder:` line carries
footprints, p99, held_max, truncation) and out/mint-lad-<arm>.err (MINT t= cls= held=
lines from the ES_MINT probe). Output: out/analysis2.json plus a printed table.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"
TICK_S = 4.9252467e-6  # view::TICK_SECONDS
CUT = 150.0  # game-s birth transient, the page's convention
MINT = re.compile(r"MINT t=(-?\d+) cls=(\w) held=(\d+)")
KV = re.compile(r"(\w+)=(\S+)")


def probe(name):
    rows = []
    for line in (OUT / f"mint-lad-{name}.err").read_text().splitlines():
        if m := MINT.match(line):
            rows.append((int(m.group(1)), m.group(2), int(m.group(3))))
    return rows


def ladder_line(name):
    lad = None
    budget = None
    for line in (OUT / f"lad-{name}.txt").read_text().splitlines():
        if line.startswith("ladder:"):
            lad = {k: v for k, v in KV.findall(line)}
        if m := re.search(r"engine budget (\d+(?:\.\d+)?) ms", line):
            budget = float(m.group(1))
    if lad is None:
        raise KeyError(name)
    lad["budget_ms"] = budget
    return lad


def arm(name):
    rows = probe(name)
    lad = ladder_line(name)
    census_all = {"t": 0, "L": 0, "0": 0}
    census = {"t": 0, "L": 0, "0": 0}  # after the cut
    held_max = 0
    t_max = max((t for t, _, _ in rows), default=0) * TICK_S
    for t, cls, held in rows:
        census_all[cls] += 1
        held_max = max(held_max, held)
        if t * TICK_S >= CUT:
            census[cls] += 1
    window = max(0.0, t_max - CUT)
    distinct = census["t"] + census["L"]
    f = lambda v: float(lad[v])
    return {
        "arm": name, "n": int(lad["n"]), "budget_ms": lad["budget_ms"],
        "game_s_window": round(window, 1),
        "entries_all": len(rows), "entries_after_cut": sum(census.values()),
        "distinct_after_cut": distinct, "census_after_cut": census,
        "lam_entries": round(sum(census.values()) / window, 4) if window else 0,
        "lam_distinct": round(distinct / window, 4) if window else 0,
        "held_max_probe": held_max, "held_max_engine": int(lad["held_max"]),
        "truncated": lad["truncated"], "wall_s": f("wall_s"),
        "build_s": f("build_s"), "foot_build_mb": f("foot_build_mb"), "foot_end_mb": f("foot_end_mb"),
        "b_per_body": f("b_per_body"), "p99_ms": f("p99_ms"), "over": int(lad["over"]),
        "lag_s": f("lag_s"), "alive": None,  # filled from the stdout line below
    }


def alive_flag(name):
    for line in (OUT / f"lad-{name}.txt").read_text().splitlines():
        if "alive(player)" in line:
            return "true" in line.split("alive(player)")[1]
    return None


def main():
    arms = ["n100k-coast20", "n100k-coast", "n100k-burn", "n100k-burn-b24", "k650-coast", "k650-burn", "k650-burn-b24", "k650-burn-b5"]
    res = []
    for a in arms:
        try:
            r = arm(a)
            r["alive"] = alive_flag(a)
            res.append(r)
        except FileNotFoundError:
            pass
    by = {r["arm"]: r for r in res}
    out = {"arms": res, "ratios": {}, "extrapolation": {}}
    for k, lo, hi in [("n100k", "n100k-coast", "n100k-burn"), ("k650", "k650-coast", "k650-burn")]:
        if hi in by and lo in by:
            out["ratios"][k] = {
                "same_convention_distinct": round(by[hi]["lam_distinct"] / by[lo]["lam_distinct"], 2) if by[lo]["lam_distinct"] else None,
                "entries": round(by[hi]["lam_entries"] / by[lo]["lam_entries"], 2) if by[lo]["lam_entries"] else None,
            }
    # The 10^6 wall under burn, from the measured burn lambda and acf2's byte law
    # bytes/mint = (K+38)*224 B, against an 8 GB budget (the M1's memory).
    for k, pref in [("n100k", "n100k-burn"), ("k650", "k650-burn")]:
        if pref in by:
            lam = by[pref]["lam_distinct"]
            out["extrapolation"][k] = {
                "measured_K": by[pref]["n"], "lam_distinct_burn": lam,
                "wall_s_at_1e6_game_s": round(8e9 / (lam * (1_000_000 + 38) * 224), 1) if lam else None,
                "foot_build_1e6_gb": round(by[pref]["b_per_body"] * 1e6 / 1e9, 2),
            }
    (OUT / "analysis2.json").write_text(json.dumps(out, indent=1))
    for r in res:
        print(json.dumps(r))
    print(json.dumps(out["ratios"], indent=1))
    print(json.dumps(out["extrapolation"], indent=1))


if __name__ == "__main__":
    main()
