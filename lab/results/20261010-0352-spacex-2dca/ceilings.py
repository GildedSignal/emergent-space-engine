#!/usr/bin/env python3
"""H_live ceilings: distinctions per body per game-second -> the 10^9-in-8GB feasibility numbers.

Inputs are the measured constants from raw/measurements.jsonl (this machine, release build):
  r      = hits per body per orbit at optical depth 1x (n=1000, rho=1e-4, annulus [1,1.5], sigma_e=1e-2)
  c      = candidate-pair conjunctions per body per orbit (same point)
  p      = candidate pairs per body (cone tier)
  s_pair = full setup per candidate pair; k_pair = re-setup+queries per pair per kick (horizon 1000 orbits)
  slack  = fraction of kick re-certification a stored slack certificate skips (eps=1e-9), violations 0

Anchors: 10^9 bodies at the same optical depth (annulus scaled), belt at a=2.5 AU (T_orbit=1.246e8 s),
M1: 4 performance cores, ~60 GB/s unified bandwidth, 8 GB. Cloud x86 orders of magnitude only.
"""
import json, pathlib

raw = [json.loads(l) for l in pathlib.Path(__file__).parent.joinpath("raw/measurements.jsonl").read_text().splitlines() if l.strip()]
st = {k: v for k, v in [(d.get("n"), d.get("rho"), ) and (f"{d['n']}:{d['rho']}", d) for d in raw if d["exp"] == "steady" and d["orbits"] == 50]}
base = st["1000:0.0001"]
kicks = [d for d in raw if d["exp"] == "kick"]
k9 = [d for d in kicks if d["eps"] == 1e-9][0]

r_body_orbit = base["hits_per_body_orbit"]            # distinctions
c_body_orbit = base["element_sort_swaps_per_body_orbit"]  # candidate conjunctions
p_body = base["cone_pairs"] / base["n"]
s_pair_us = base["ns_per_pair_setup_and_run"] / 1e3
k_pair_us = k9["us_per_pair"]
slack = k9["slack_skippable_fraction"]

# consistency: the optical-depth law r ~ n * rho (controls)
law = [(st[k]["hits_per_body_orbit"] / (int(k.split(":")[0]) * float(k.split(":")[1]))) for k in st]
spread = (max(law) - min(law)) / min(law)

N = 1e9
T_ORBIT = 1.246e8   # s at a = 2.5 AU
CORES, BW = 4.0, 60e9
SCAR_B = 20         # bytes: Elias-Fano ordinal ~3-7 bits + a packed delta row (shipmem program.rs)

pairs_kick_1x = p_body * 2 * 1.96  # 813 measured at 10x density -> ~2x pair count per body (both sides+reach)
kick_us_1x = pairs_kick_1x * k_pair_us
kick_us_slack = kick_us_1x * (1 - slack)

# cores needed at RTF R for a per-event cost in microseconds and a per-body-per-orbit rate
def cores(R, cost_us, rate=r_body_orbit):
    return N * rate * cost_us * 1e-6 / T_ORBIT * R


out = {
  "measured": {
    "r_body_orbit": r_body_orbit, "c_body_orbit": c_body_orbit, "pairs_per_body": round(p_body, 1),
    "full_setup_us_per_pair": round(s_pair_us, 2), "kick_rescan_us_per_pair": round(k_pair_us, 2),
    "slack_skip_fraction": slack, "slack_violations": k9["slack_skip_violations"],
    "optical_depth_law_spread": round(spread, 3),
    "bookkeeping_over_physics": round(c_body_orbit / r_body_orbit),
    "kick_us_1x_noslack": round(kick_us_1x), "kick_us_1x_slack": round(kick_us_slack, 1),
  },
  "per_game_second_at_RTF1": {
    "distinctions_per_s": N * r_body_orbit / T_ORBIT,
    "conjunctions_per_s": N * c_body_orbit / T_ORBIT,
  },
  "cores_at_RTF": {f"{R:.0e}": {
      "encounters_noslack": round(cores(R, kick_us_1x), 2),
      "encounters_slack": round(cores(R, kick_us_slack), 2),
      "conjunction_stream_at_500ns": round(N * c_body_orbit / T_ORBIT * R * 500e-9, 2),
      "conjunction_stream_at_50ns": round(N * c_body_orbit / T_ORBIT * R * 50e-9, 2),
      "conjunction_stream_naive_setup": round(N * c_body_orbit / T_ORBIT * R * s_pair_us * 1e-6, 2),
  } for R in (1e2, 1e4, 1e6)},
  "rtf_ceilings_4cores": {
    "encounters_noslack": 4 / (N * r_body_orbit * kick_us_1x * 1e-6 / T_ORBIT),
    "encounters_slack": 4 / (N * r_body_orbit * kick_us_slack * 1e-6 / T_ORBIT),
    "conjunctions_500ns": 4 / (N * c_body_orbit / T_ORBIT * 500e-9),
    "conjunctions_50ns": 4 / (N * c_body_orbit / T_ORBIT * 50e-9),
  },
  "memory": {
    "program_bits_per_body": 0.126, "program_store_MB": 0.126 * N / 8 / 1e6,
    "scar_write_GBps_at_RTF1e6": N * r_body_orbit / T_ORBIT * 1e6 * SCAR_B / 1e9,
    "scar_steady_state_GB_at_1pct": 0.01 * N * SCAR_B / 1e9,
    "conjunction_GBps_at_RTF1e6_per_64B_line": N * c_body_orbit / T_ORBIT * 1e6 * 64 / 1e9,
  },
}
print(json.dumps(out, indent=1))
