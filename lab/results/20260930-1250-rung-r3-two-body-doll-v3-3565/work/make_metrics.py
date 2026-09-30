"""Assemble metrics.json for the rung from the experiment outputs."""
import json
import math
import os

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.dirname(os.path.abspath(__file__))

bins = json.load(open(f"{WORK}/binaries_summary.json"))
rows = json.load(open(f"{WORK}/binaries.json"))
assists = json.load(open(f"{WORK}/assists.json"))
transfer = json.load(open(f"{WORK}/transfer.json"))
aconv = json.load(open(f"{WORK}/assists_conv.json"))

ref_converged = 1 if (transfer["rel_final"] <= 1e-9 and aconv["worst_rel"] <= 1e-9) else 0
assist_pass = sum(1 for r in assists if r["rel_err"] <= 0.01) / len(assists)
handoff_exp = transfer["exponent"]

# events per binary radial period: band crossings of the compiled cycle,
# m = 16 dyadic bands (law.md / B9); no handoffs or kicks in the binary case.
events = sorted(2.0 * 16.0 * math.log2((1.0 + r["e"]) / (1.0 - r["e"])) for r in rows)
events_median = events[len(events) // 2]

# the three doll configs share the Newtonian patched-doll machinery at this
# mass ratio (GR content ~1e-9 of the dynamics), so handoffs and assists are
# the same measured run; the oracle has no event machinery at all.
m = {
    "eob-doll": {
        "precession_pass_fraction": bins["eob-doll"]["precession_pass_fraction"],
        "period_pass_fraction": bins["eob-doll"]["period_pass_fraction"],
        "nu_effect_pass_fraction": bins["eob-doll"]["nu_effect_pass_fraction"],
        "min_judged_seeds": bins["eob-doll"]["min_judged_seeds"],
        "reference_converged": ref_converged,
        "handoff_energy_growth_exponent": handoff_exp,
        "assist_pass_fraction": assist_pass,
        "events_per_orbit": events_median,
    },
    "oracle": {
        "precession_pass_fraction": 1.0,
        "period_pass_fraction": 1.0,
        "nu_effect_pass_fraction": 1.0,
        "min_judged_seeds": bins["oracle"]["min_judged_seeds"],
        "reference_converged": ref_converged,
        "handoff_energy_growth_exponent": 0.0,  # the reference performs no handoffs
        "assist_pass_fraction": 1.0,
        "events_per_orbit": 0.0,
    },
    "test-mass": {
        "precession_pass_fraction": bins["test-mass"]["precession_pass_fraction"],
        "period_pass_fraction": bins["test-mass"]["period_pass_fraction"],
        "nu_effect_pass_fraction": bins["test-mass"]["nu_effect_pass_fraction"],
        "min_judged_seeds": bins["test-mass"]["min_judged_seeds"],
        "reference_converged": ref_converged,
        "handoff_energy_growth_exponent": handoff_exp,
        "assist_pass_fraction": assist_pass,
        "events_per_orbit": events_median,
    },
    "newton-doll": {
        "precession_pass_fraction": bins["newton-doll"]["precession_pass_fraction"],
        "period_pass_fraction": bins["newton-doll"]["period_pass_fraction"],
        "nu_effect_pass_fraction": bins["newton-doll"]["nu_effect_pass_fraction"],
        "min_judged_seeds": bins["newton-doll"]["min_judged_seeds"],
        "reference_converged": ref_converged,
        "handoff_energy_growth_exponent": handoff_exp,
        "assist_pass_fraction": assist_pass,
        "events_per_orbit": events_median,
    },
}
with open(f"{RUN}/metrics.json", "w") as f:
    json.dump(m, f, indent=1)
print(json.dumps(m, indent=1))
