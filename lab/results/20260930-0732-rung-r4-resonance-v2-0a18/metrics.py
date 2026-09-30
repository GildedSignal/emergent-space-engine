#!/usr/bin/env python3
"""Assemble metrics.json for rung r4 v2 from the saved per-config summaries.

Metric definitions (frozen by the rung, operationalised here):
- e_pump_ratio_min/max: over the two resonant cases, min/max of
  (config max e1) / (truth-2400 max e1). Max e1 over the whole run, sampled
  50x per inner orbit in both truth and law.
- libration_ratio_min: min over resonant cases of
  (config resonant-angle concentration) / (truth-2400 concentration).
  Concentration = mean resultant length |mean(exp(i*phi))| of
  phi = 2*lam2 - lam1 - varpi1 sampled 50x per orbit.
- control_pass_fraction: fraction of the 3 controls whose secular e1 envelope
  matches truth-2400 within 20%: |max_l - max_t| <= 0.2*max_t AND
  |min_l - min_t| <= 0.2*max_t (scale-relative on the envelope top).
- dense_steps: 0 for every config by construction (candidates integrate no
  dynamics steps; the positive control reports 0 by the rung's convention).
- kicks_per_orbit: median over the 5 cases of (window ends)/(inner orbits).
"""
import json, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
RESONANT = ["r2-base", "r2-shift"]
CONTROLS = ["c-5.00", "c-2.55", "c-2.15"]

def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)

truth = load("truth2400.json")

def metrics_for(summ):
    pumps = [summ[c]["emax"] / truth[c]["emax"] for c in RESONANT]
    libs = [summ[c]["R"] / truth[c]["R"] for c in RESONANT]
    npass = 0
    for c in CONTROLS:
        mx_t = truth[c]["emax"]
        ok = (abs(summ[c]["emax"] - mx_t) <= 0.2 * mx_t and
              abs(summ[c]["emin"] - truth[c]["emin"]) <= 0.2 * mx_t)
        npass += ok
    kpo = [(s["windows"] or 0) / s["orbits"] for s in summ.values()]
    return {
        "e_pump_ratio_min": min(pumps),
        "e_pump_ratio_max": max(pumps),
        "libration_ratio_min": min(libs),
        "control_pass_fraction": npass / 3.0,
        "dense_steps": 0,
        "kicks_per_orbit": statistics.median(kpo),
    }

CRIT = [("e_pump_ratio_min", ">=", 0.8), ("e_pump_ratio_max", "<=", 1.25),
        ("libration_ratio_min", ">=", 0.8), ("control_pass_fraction", ">=", 1.0),
        ("dense_steps", "<=", 0), ("kicks_per_orbit", "<=", 8)]

def passes(m):
    return all((m[k] >= v if op == ">=" else m[k] <= v) for k, op, v in CRIT)

out = {}
for cfg in ("arc-g8", "arc-g16", "arc-g8-half", "averaged", "none"):
    out[cfg] = metrics_for(load(f"law-{cfg}.json"))
out["truth-1200"] = metrics_for(load("truth1200.json"))

with open(os.path.join(HERE, "metrics.json"), "w") as f:
    json.dump(out, f, indent=1)

print(f"{'config':12s} {'pump_min':>9s} {'pump_max':>9s} {'lib_min':>8s} "
      f"{'ctrl':>5s} {'dense':>6s} {'kicks':>7s}  verdict")
for cfg, m in out.items():
    v = "PASS" if passes(m) else "FAIL"
    print(f"{cfg:12s} {m['e_pump_ratio_min']:9.3f} {m['e_pump_ratio_max']:9.3f} "
          f"{m['libration_ratio_min']:8.3f} {m['control_pass_fraction']:5.2f} "
          f"{m['dense_steps']:6d} {m['kicks_per_orbit']:7.2f}  {v}")

# truth ladder convergence evidence for the dossier
for res in (600, 1200):
    t = load(f"truth{res}.json")
    dp = max(abs(t[c]["emax"] - truth[c]["emax"]) / truth[c]["emax"] for c in truth)
    dR = max(abs(t[c]["R"] - truth[c]["R"]) for c in truth)
    print(f"truth{res} vs truth2400: max |d emax| = {dp:.2e}, max |d R| = {dR:.2e}")
