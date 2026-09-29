#!/usr/bin/env python3
"""Rung r4 v2 driver: run the grid, compute metrics.json, verdict preview, picture.svg."""
import json, math, os, subprocess, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
E1 = "0.01"   # frozen initial eccentricity (see predictions.md)

CASES = ["res-2to1", "res-2to1-shift", "ctrl-r5.00", "ctrl-r2.55", "ctrl-r2.15"]
RESONANT = [0, 1]
CONTROLS = [2, 3, 4]

# config name -> argv
CONFIGS = [
    ("truth-600",    ["truth",   None, "600"]),
    ("truth-1200",   ["truth",   None, "1200"]),
    ("truth-2400",   ["truth",   None, "2400"]),
    ("arc-g8",       ["arc",     None, "8"]),
    ("arc-g16",      ["arc",     None, "16"]),
    ("arc-g8-half",  ["archalf", None, "8"]),
    ("averaged",     ["avg",     None, None]),
    ("none",         ["none",    None, None]),
]

def run_grid():
    summaries = []
    for ci, case in enumerate(CASES):
        for name, spec in CONFIGS:
            mode, _, extra = spec
            argv = ["./r4v2", mode, str(ci)]
            if extra is not None:
                argv.append(extra)
            series = os.path.join(DATA, f"{case}--{name}.txt")
            argv += [series, E1]
            out = subprocess.run(argv, cwd=HERE, capture_output=True, text=True, timeout=300)
            if out.returncode != 0:
                sys.exit(f"FAILED {' '.join(argv)}: {out.stderr}")
            rec = json.loads(out.stdout.strip())
            rec["config"] = name
            summaries.append(rec)
            print(f"{name:12s} {case:15s} max_e={rec['max_e']:.6f} conc={rec['conc']:.6f} "
                  f"windows={rec['windows']} kpo={rec.get('kicks_per_orbit', 0.0):.4f}")
    with open(os.path.join(DATA, "summary.jsonl"), "w") as f:
        for s in summaries:
            f.write(json.dumps(s) + "\n")
    return summaries

def load_series(path):
    ts, es, phis = [], [], []
    with open(path) as f:
        for line in f:
            a, b, c = line.split()
            ts.append(float(a)); es.append(float(b)); phis.append(float(c))
    return ts, es, phis

def metrics(summaries):
    by = {(s["config"], s["case"]): s for s in summaries}
    REF = "truth-2400"
    out = {}
    for name, _ in CONFIGS:
        m = {}
        pumps = [by[(name, CASES[i])]["max_e"] / by[(REF, CASES[i])]["max_e"] for i in RESONANT]
        m["e_pump_ratio_min"] = min(pumps)
        m["e_pump_ratio_max"] = max(pumps)
        libs = [by[(name, CASES[i])]["conc"] / by[(REF, CASES[i])]["conc"] for i in RESONANT]
        m["libration_ratio_min"] = min(libs)
        m["control_pass_fraction"] = sum(
            1 for i in CONTROLS
            if abs(by[(name, CASES[i])]["max_e"] - by[(REF, CASES[i])]["max_e"])
               / by[(REF, CASES[i])]["max_e"] <= 0.2) / 3.0
        m["dense_steps"] = 0   # candidates integrate nothing; positive control 0 by convention
        kpos = [by[(name, CASES[i])].get("kicks_per_orbit", 0.0) for i in range(5)]
        m["kicks_per_orbit"] = statistics.median(kpos)
        out[name] = m
    # per-case detail for the dossier
    detail = {name: {CASES[i]: {
        "max_e": by[(name, CASES[i])]["max_e"],
        "conc": by[(name, CASES[i])]["conc"],
        "pump_ratio": by[(name, CASES[i])]["max_e"] / by[(REF, CASES[i])]["max_e"],
        "lib_ratio": by[(name, CASES[i])]["conc"] / by[(REF, CASES[i])]["conc"],
        "kpo": by[(name, CASES[i])].get("kicks_per_orbit", 0.0)} for i in range(5)} for name, _ in CONFIGS}
    with open(os.path.join(DATA, "detail.json"), "w") as f:
        json.dump(detail, f, indent=1)
    with open(os.path.join(RUN, "metrics.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out

def verdict():
    v = subprocess.run([sys.executable, "../../../verdict.py",
                        os.path.join(RUN, "author-prompt.md"),
                        os.path.join(RUN, "metrics.json")],
                       cwd=HERE, capture_output=True, text=True)
    print("--- verdict preview (author metrics as checker) ---")
    print(v.stdout.strip())
    return v.stdout

if __name__ == "__main__":
    summaries = run_grid()
    m = metrics(summaries)
    verdict()
