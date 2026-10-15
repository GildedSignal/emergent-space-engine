#!/usr/bin/env python3
"""Aggregate the trojan dwell arms and test the pre-registered predictions (P1-P5)."""
import json, math, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))

import re

_RUST_JSON = re.compile(r"(?<=:)(-?)inf\b")

def load(name):
    rows = []
    with open(os.path.join(HERE, name)) as f:
        for line in f:
            if line.strip():
                # serde_json emits bare `inf` for infinite f64 (invalid JSON);
                # Python's json accepts the spelling `Infinity`.
                rows.append(json.loads(_RUST_JSON.sub(r"\1Infinity", line)))
    return rows

def q(xs, p):
    if not xs:
        return float("nan")
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))]

def stats(rows):
    live = [r for r in rows if r["death"] is None]
    dead = [r for r in rows if r["death"] is not None]
    gave_up = [r for r in dead if r["death"] == "gave_up"]
    eps = [(s, l) for r in live for (s, l) in r["episodes"]]
    maxd = [max([l for _, l in r["episodes"]] or [0]) / 8.0 for r in live]  # in planet periods
    # censored, recomputed: the last episode covers the final sample (the file flag is off by one)
    cens = [r for r in live if r["episodes"] and r["episodes"][-1][0] + r["episodes"][-1][1] == r["samples"] + 1]
    never = [r for r in live if not r["episodes"]]
    return {
        "n": len(rows), "live": len(live), "dead": len(dead), "gave_up": len(gave_up),
        "died_P": sorted(round(r["death"], 1) for r in dead if isinstance(r["death"], float)),
        "episodes": len(eps), "never_entered": len(never),
        "max_p50": q(maxd, 0.5), "max_p90": q(maxd, 0.9),
        "ep_p50": q([l / 8.0 for _, l in eps], 0.5), "ep_p90": q([l / 8.0 for _, l in eps], 0.9),
        "ep_max": (max([l for _, l in eps], default=0)) / 8.0,
        "capped_frac": len(cens) / len(live) if live else float("nan"),
        # split: born inside the band vs outside
        "in_capped": (lambda ins: len([r for r in ins if r["episodes"] and r["episodes"][-1][0] + r["episodes"][-1][1] == r["samples"] + 1]) / len(ins) if ins else float("nan"))(
            [r for r in live if abs(r["du"]) < 1]),
        "out_capture": (lambda out: len([r for r in out if r["episodes"]]) / len(out) if out else float("nan"))(
            [r for r in live if abs(r["du"]) >= 1]),
    }

def main():
    arms = {n: stats(load(f"{n}.jsonl")) for n in ["float-12", "float-10", "plane-7", "plane-2"]}
    print(f"{'':12} " + " ".join(f"{k:>10}" for k in arms))
    for k in ["n", "live", "dead", "gave_up", "episodes", "never_entered", "max_p50", "max_p90",
              "ep_p50", "ep_p90", "ep_max", "capped_frac", "in_capped", "out_capture"]:
        print(f"{k:>12} " + " ".join(f"{arms[a][k]:>10}" if isinstance(arms[a][k], float) else f"{arms[a][k]:>10}"
              for a in arms))
    for a in arms:
        print(f"  {a} deaths(P):", arms[a]["died_P"])
    f12, f10, p7, p2 = (arms["float-12"], arms["float-10"], arms["plane-7"], arms["plane-2"])

    def ratio(x, y):
        return float("nan") if not y else x / y

    checks = [
        ("P1 pos ctl  float10 vs float12: capped within 2x", max(ratio(f10["capped_frac"], f12["capped_frac"]), ratio(f12["capped_frac"], f10["capped_frac"])) <= 2
         and max(f12["max_p90"] / f10["max_p90"], f10["max_p90"] / f12["max_p90"]) <= 1.5
         and abs(f10["dead"] - f12["dead"]) <= 3),
        ("P2 main     plane7  vs float12: capped within 2x and p90 within 1.5x",
         max(ratio(p7["capped_frac"], f12["capped_frac"]), ratio(f12["capped_frac"], p7["capped_frac"])) <= 2
         and max(p7["max_p90"] / f12["max_p90"], f12["max_p90"] / p7["max_p90"]) <= 1.5),
        ("P3 neg ctl  plane2  vs float12: must EXCEED a bound",
         ratio(p2["capped_frac"], f12["capped_frac"]) > 2 or ratio(f12["capped_frac"], p2["capped_frac"]) > 2
         or p2["max_p90"] / f12["max_p90"] > 1.5 or f12["max_p90"] / p2["max_p90"] > 1.5),
        ("P4 deaths   plane7 dead > float12 gave_up", p7["dead"] > f12["gave_up"]),
        ("P5 tail     p90 ratio further from 1 than p50 ratio (plane7 vs float12)",
         abs(math.log(max(p7["max_p90"], 1e-9) / max(f12["max_p90"], 1e-9))) >
         abs(math.log(max(p7["max_p50"], 1e-9) / max(f12["max_p50"], 1e-9)))),
    ]
    print()
    for name, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")

def classes(rows):
    """Full-ensemble outcome classes: captured (censored), escaped (live, not censored), dead."""
    cens = len([r for r in rows if r["death"] is None and r["episodes"] and r["episodes"][-1][0] + r["episodes"][-1][1] == r["samples"] + 1])
    dead = len([r for r in rows if r["death"] is not None])
    return {"captured": cens, "escaped": len(rows) - cens - dead, "dead": dead}


def extra():
    print()
    for a in ["float-12", "float-10", "plane-7", "plane-2"]:
        print(f"  {a} classes:", classes(load(f"{a}.jsonl")))
    f12 = load("float-12.jsonl")
    if "closest_R" in f12[0]:
        cs = sorted(r["closest_R"] for r in f12)
        print(f"  float-12 closest approach: min {cs[0]:.1f} Rp, p10 {cs[len(cs)//10]:.1f} Rp (P/8 sampling)")


if __name__ == "__main__":
    main()
    extra()
