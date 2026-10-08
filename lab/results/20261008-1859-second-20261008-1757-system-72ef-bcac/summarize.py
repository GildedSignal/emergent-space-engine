#!/usr/bin/env python3
"""Summarise the second-author decisive runs into dossier numbers."""
import json

import numpy as np

BUDGET = 8 * 2 ** 33 / 1e9 - 0.126  # bits/body, 8 GiB at 1e9 bodies


def q_star(level_at_1e6, budget=BUDGET):
    """Common-quantum that fits the budget, given the level at q=1e-6
    (level(q) = level(1e-6) + 5*log2(1e-6/q), 16.6 bits/decade)."""
    return 1e-6 * 2 ** ((level_at_1e6 - budget) / 5.0)


def main():
    out = {}

    lj = json.load(open("scars2-long.json"))
    ep = lj["epochs"]
    out["final_matches_stored_long"] = lj.get("final_matches_stored_long")
    rows = [(e["step"], e["level_total"], e["level_joint_total"],
             e["plugin_total"], e.get("level_sec_total"),
             e.get("level_sec_joint_total")) for e in ep]
    out["epoch_table_step_level_joint_plugin_sec_secjoint"] = rows
    st = np.array([r[0] for r in rows], float)
    lv = np.array([r[1] for r in rows], float)
    lg = np.log2(st)
    A = np.vstack([lg[-6:], np.ones(6)]).T
    slope_tail = float(np.linalg.lstsq(A, lv[-6:], rcond=None)[0][0])
    out["tail_slope_bits_per_octave_last6"] = round(slope_tail, 3)
    out["growth_main_to_long_decade"] = round(float(lv[-1] - lv[np.argmin(
        np.abs(st - 4500))]), 2)
    fin = ep[-1]
    out["final_level_total"] = fin["level_total"]
    out["final_level_joint_total"] = fin["level_joint_total"]
    out["final_level_sec_total"] = fin.get("level_sec_total")
    out["final_level_sec_joint_total"] = fin.get("level_sec_joint_total")
    out["secular_savings_bits"] = round(fin["level_total"]
                                        - fin["level_sec_total"], 2)
    out["secular_savings_joint_bits"] = round(fin["level_joint_total"]
                                              - fin["level_sec_joint_total"],
                                              2)
    out["q_star_raw"] = float(q_star(fin["level_total"]))
    out["q_star_sec"] = float(q_star(fin["level_sec_total"]))
    out["q_star_sec_joint"] = float(q_star(fin["level_sec_joint_total"]))
    out["gib_raw_1e9_q1e-6"] = round(fin["level_total"] * 1e9 / 2 ** 33, 2)
    out["gib_sec_1e9_q1e-6"] = round(fin["level_sec_total"] * 1e9 / 2 ** 33, 2)
    out["per_channel_final"] = fin["level"]
    out["per_channel_sec_final"] = fin.get("level_sec")

    mj = json.load(open("level-main.json"))
    out["main_horizon_level_raw5_q1e-6"] = mj["level_raw5"]["1e-06"]
    out["main_horizon_q_star_raw"] = mj["q_star_raw5"]["q_star"]

    try:
        bj = json.load(open("scars2-bign.json"))
        out["bign_prefix_identical"] = bj["prefix_identical_to_main"]
        out["bign_plugin_final"] = bj["plugin_final"]
        out["bign_plugin_total"] = bj["plugin_final_total"]
        out["bign_level_final"] = bj["level_final"]
        out["bign_level_total"] = bj["level_final_total"]
        out["bign_wall_total"] = bj["wall_total"]
        out["bign_heldout"] = bj["heldout"]
        out["bign_heldout_max_excess"] = max(
            v["excess"] for v in bj["heldout"].values())
    except FileNotFoundError:
        out["bign"] = "not finished"

    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
