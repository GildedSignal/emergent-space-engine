#!/usr/bin/env python3
"""Parse the four anchor flights and compose the 10^9 steady-state belt bill.

Run from the repo root after the flights:  python3 lab/results/20261015-2041-fermi-99b5/compose.py
Prints the anchor table and the composition as JSON; every cited constant is named.
"""
import json, re, sys

def parse(path):
    """Pull the two flights (shallow then deep) out of one rung's output."""
    txt = open(path).read().split("=== deep")[0]
    deep = open(path).read().split("=== deep")[1]
    def one(t):
        g = lambda pat: float(re.search(pat, t).group(1))
        return {
            "bodies": g(r"rung N=\d+ \((\d+) bodies\)"),
            "gs": g(r"game ([\d.]+) s after the first second"),
            "kicks": g(r"kicks (\d+) \("),
            "events": g(r"events (\d+) \("),
            "foot_build_mb": g(r"peak footprint (\d+) MB at the build"),
            "foot_end_mb": g(r"(\d+) MB at the flight's end"),
            "birth_bpb": g(r"(\d+) B a body from the build"),
            "dash_bpb": g(r"dashboard bytes/body (\d+)"),
            "catalogue": g(r"catalogue (\d+) entries"),
            "held_max": g(r"held_max=(\d+)"),
            "lag_s": g(r"lag_s=([\d.]+)"),
            "p50_ms": g(r"p50_ms=([\d.]+)"),
        }
    return one(txt), one(deep)

R = {}
for n, f in (("n1e4", "work/n10000.txt"), ("n1e5", "work/n100000.txt")):
    sh, dp = parse(f"lab/results/20261015-2041-fermi-99b5/{f}")
    b = sh["bodies"]
    span = dp["gs"] - sh["gs"]
    R[n] = {
        "shallow": sh, "deep": dp,
        "shallow_kick_rate": sh["kicks"] / sh["gs"] / b,
        "deep_kick_rate_avg": dp["kicks"] / dp["gs"] / b,
        "depth_kick_rate_diff": (dp["kicks"] - sh["kicks"]) / span / b,
        "depth_event_rate_diff": (dp["events"] - sh["events"]) / span / b,
        "depth_bpb_gross": dp["foot_end_mb"] * 1e6 / b,
        "flight_growth_B_per_body_game_s": (dp["foot_end_mb"] - sh["foot_end_mb"]) * 1e6 / b / span,
    }

# ---- the law's cadence: the unthrottled rung (10^4: p50 3-4 ms < 12 ms budget), cross-checked
# at rtf 100 in artifacts/runs/nladder/ladder.txt (1.90e-4 at 10^4, 1.86e-4 at 10^3).
LAW = R["n1e4"]["depth_kick_rate_diff"]
LAW_X = {"rtf100_ladder_txt_n1e4": 1.90e-4, "rtf100_ladder_txt_n1e3": 1.86e-4, "this_rtf900_diff": LAW}

# ---- the throttle check: what fraction of the law does the 10^5 rung deliver, and does
# the 12 ms/frame budget predict it?  (60 fps x 12 ms = 0.72 s/s = 0.72 cores)
BUDGET_CORES = 0.012 * 60
KICK_US = 75e-6  # scoreboard mid (75-160 us); c01c measured 43-52.8 us
rtf5 = 3000.0
cores_needed_1e5 = LAW * 1e5 * rtf5 * KICK_US
delivered = R["n1e5"]["depth_kick_rate_diff"] / LAW
THROTTLE = {
    "cores_needed_at_1e5_rtf3000": cores_needed_1e5,
    "budget_cores": BUDGET_CORES,
    "predicted_delivery": BUDGET_CORES / cores_needed_1e5,
    "measured_delivery": delivered,
    "held_1e4_deep": R["n1e4"]["deep"]["held_max"],
    "held_1e5_deep": R["n1e5"]["deep"]["held_max"],
}

# ---- the 10^9 composition. Constants (sources in the dossier):
PROMO_CYCLE_US = 3.7e-6      # d6ba census: cycle promotion p50
READS_PER_DEM = 12.7         # f55d: reads per demotion with no retention
KICK_US_LOW, KICK_US_HIGH = 43e-6, 160e-6   # c01c; scoreboard upper
KICK_FLOOR_NS = 50e-9        # scoreboard floor
RECORD_BPB = (980.0, 1317.0) # d6ba bpb_engine at depth (engine accounting)
ARCS_SEAM_BPB = 8.6          # d6ba, belt at depth with the seam line
MEM_BUDGET_GB = 6.0          # HANDOFF scoreboard
M9, CORES_M1 = 1e9, 8.0

C = {
    "law_cadence_per_body_game_s": LAW,
    "at_1e9": {
        "kicks_per_game_s": LAW * M9,
        "kick_cores_c01c": LAW * M9 * KICK_US_LOW,
        "kick_cores_scoreboard": LAW * M9 * KICK_US_HIGH,
        "kick_cores_at_floor": LAW * M9 * KICK_FLOOR_NS,
        "remint_cores_cap_coast": LAW * M9 * PROMO_CYCLE_US,
        "remint_cores_nocap": LAW * M9 * READS_PER_DEM * PROMO_CYCLE_US,
        "cpu_cores_today_cap": LAW * M9 * (KICK_US_LOW + PROMO_CYCLE_US),
        "cpu_over_m1_x_cap": LAW * M9 * (KICK_US_LOW + PROMO_CYCLE_US) / CORES_M1,
        "mem_record_stack_tb": [RECORD_BPB[0] * M9 / 1e12, RECORD_BPB[1] * M9 / 1e12],
        "mem_arcs_seam_gb": ARCS_SEAM_BPB * M9 / 1e9,
        "mem_over_budget_x": RECORD_BPB[0] * M9 / (MEM_BUDGET_GB * 1e9),
    },
}
C["memory_binds_x_harder_than_cpu"] = C["at_1e9"]["mem_over_budget_x"] / C["at_1e9"]["cpu_over_m1_x_cap"]
# 0757's sentence: "~0.15 cores re-mint at 10^9" against the composed steady state
C["check_0757_remint_0p15_cores"] = {
    "composed_steady_cap": C["at_1e9"]["remint_cores_cap_coast"],
    "composed_steady_nocap": C["at_1e9"]["remint_cores_nocap"],
    "their_basis": "20k-cut promotion count (1.31/body avg) on rtf-paced 10^5 arms",
    "understates_cap_by_x": C["at_1e9"]["remint_cores_cap_coast"] / 0.15,
    "understates_nocap_by_x": C["at_1e9"]["remint_cores_nocap"] / 0.15,
}

out = {"anchors": R, "law_cross_checks": LAW_X, "throttle": THROTTLE, "composition": C}
json.dump(out, sys.stdout, indent=1)
print()
