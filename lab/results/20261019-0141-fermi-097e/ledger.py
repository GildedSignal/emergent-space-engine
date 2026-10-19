#!/usr/bin/env python3
"""The board's interlocking 10^9 ledger, assembled on measured laws (page-cited).

Every constant below is either (a) measured by this run's probes (probe-n1e4/1e5.log,
shipped `nladder`, Linux/x86 — orders of magnitude only), or (b) page-cited from
lab/wiki/ with the run id. CPU is CPU-seconds per presented game-second at rtf 100
("cores"); the M1 budget is ~4 P-cores of useful throughput ("a few cores").
Memory is GB at N = 10^9 against the 8 GB unified budget.
"""
import json

N = 1_000_000_000
M1_BUDGET_CORES = 4.0
MEM_BUDGET_GB = 8.0

C = {}  # name -> (value, unit, source)

# ---- probe anchors (this run, shipped nladder, coast seed 1 rtf 100, 10 s wall) ----
C["b_per_body_1e4"] = (2464, "B", "probe-n1e4.log")
C["b_per_body_1e5"] = (2348, "B", "probe-n1e5.log")
C["p50_ms_1e4"] = (0.076, "ms", "probe-n1e4.log")
C["p50_ms_1e5"] = (0.078, "ms", "probe-n1e5.log")
C["kicks_per_body_gs_1e4"] = (2.134e-4, "1/body/gs", "probe-n1e4.log")
C["kicks_per_body_gs_1e5"] = (2.139e-5, "1/body/gs", "probe-n1e5.log")
# total kicks equal across a decade of N: rate x N is constant -> belt inert, player-only stream
C["total_kicks_ratio_1e5_over_1e4"] = (2.139e-5 * 1e5 / (2.134e-4 * 1e4), "x", "probes")

# ---- page-cited constants ----
C["kick_stream_composed"] = ((5.3, 8.4), "cores", "cd3b (wiki/encounters): split 8 x survival, M1")
C["kick_stream_shipped"] = (208.0, "cores", "cd3b: 2 ev/body/interval x 29.3 us M1")
C["churn_epoch_rule"] = ((2.8, 5.5), "cores", "08d0 (wiki/encounters): E=128..64, 9fd1 awaiting grade")
C["churn_wholesale"] = (355.0, "cores", "1a29 (wiki/encounters): Theta(n-1) re-arm")
C["mint_worst"] = (1.9, "cores", "cd3b: every Dohnanyi conjunction re-mints at 16.4 us")
C["view_due_form"] = (0.1, "cores", "e3a4 (wiki/view): <=250 repairs/frame x 100 ns")
C["view_serve_today_1e5"] = (35.8, "ms/frame", "e6c9: O(K) aggregate residue, running-sums unwired")
C["frame_budget_bound"] = (12.0 * 60 / 1000.0, "cores", "12 ms x 60 fps (the budget itself bounds it)")
C["fired_kick_rate"] = (3.6e-5, "1/body/gs", "a9d7 gold (wiki/memory-h-live), invariant in N")
C["live_bytes"] = (5100.0, "B", "HANDOFF scoreboard: ~5,100 B after first kick (every body live)")
C["soi_transits"] = (1.31e-2, "1/body/orbit", "4b55 gold (wiki/memory-h-live)")
C["orbit_gs"] = (3.52e8, "gs", "cd3b: own period 12,480 intervals")
C["belt_bits_selfstirred"] = ((1.7, 2.4), "B/body", "07b4 gold: real 10^9 belt never scars")
C["belt_bits_driven"] = (126.0 / 8.0, "B/body", "fc48/0820 gold: driven worst case 126.4 bits")
C["belt_bits_phaselocked"] = ((21.0 / 8.0, 40.0 / 8.0), "B/body", "HANDOFF scoreboard: compact store alone")

# ---- CPU ledger at 10^9 (composed, rtf 100) ----
cpu = {}
cpu["kick_event_stream"] = {"cores": list(C["kick_stream_composed"][0]), "src": "cd3b"}
cpu["cert_churn_epoch_rule"] = {"cores": list(C["churn_epoch_rule"][0]), "src": "08d0/9fd1"}
cpu["key_mint_worst"] = {"cores": C["mint_worst"][0], "src": "cd3b"}
cpu["view_serve_due_form"] = {"cores": C["view_due_form"][0], "src": "e3a4"}
cpu["frame"] = {"cores": C["frame_budget_bound"][0], "src": "budget"}
lo = sum(v["cores"] if isinstance(v["cores"], float) else v["cores"][0] for v in cpu.values())
hi = sum(v["cores"] if isinstance(v["cores"], float) else v["cores"][1] for v in cpu.values())
cpu_total = {"cores": [round(lo, 1), round(hi, 1)], "over_budget_x": [round(lo / M1_BUDGET_CORES, 2), round(hi / M1_BUDGET_CORES, 2)]}
# conditional: the churn term if 9fd1's pooled epoch rule fails grading (wholesale re-arm)
cpu_total["if_epoch_rule_falls"] = {"cores": round(lo - C["churn_epoch_rule"][0][0] + C["churn_wholesale"][0], 0),
                                    "over_budget_x": round((lo - C["churn_epoch_rule"][0][0] + C["churn_wholesale"][0]) / M1_BUDGET_CORES, 0)}

# ---- memory ledger at 10^9 ----
mem = {}
mem["shipped_build"] = {"GB": round(min(C["b_per_body_1e4"][0], C["b_per_body_1e5"][0]) * N / 1e9, 2),
                        "over_x": round(min(C["b_per_body_1e4"][0], C["b_per_body_1e5"][0]) * N / (MEM_BUDGET_GB * 1e9), 0),
                        "src": "probes + dcf1/99da law"}
mem["wired_store_selfstirred"] = {"GB": [round(1.7 * N / 1e9, 2), round(2.4 * N / 1e9, 2)], "over_x": [round(1.7 * N / 8e9, 2), round(2.4 * N / 8e9, 2)], "src": "07b4"}
mem["wired_store_driven_worst"] = {"GB": round(126.4 / 8 * N / 1e9, 2), "over_x": round(126.4 / 8 * N / 8e9, 2), "src": "fc48/0820"}
mem["wired_store_phaselocked"] = {"GB": [round(21 / 8 * N / 1e9, 2), round(40 / 8 * N / 1e9, 2)], "over_x": [round(21 / 8 / 8, 2), round(40 / 8 / 8, 2)], "src": "scoreboard"}

# build/floor separation
build_floor_ratio = round(2348 / 2.4, 0)  # shipped B/body vs self-stirred floor B/body

# ---- the promotion residency dial (arithmetic) ----
prom = {}
rate_every_kick = C["fired_kick_rate"][0] * N          # promotions/gs if every fired kick promotes
n_live_at_8gb = MEM_BUDGET_GB * 1e9 / C["live_bytes"][0]
prom["every_kick"] = {"rate_per_gs": rate_every_kick, "tau_max_gs": n_live_at_8gb / rate_every_kick,
                      "orbit_fraction": n_live_at_8gb / rate_every_kick / C["orbit_gs"][0]}
rate_soi = C["soi_transits"][0] * N / C["orbit_gs"][0]  # promotions/gs, SOI transits only
prom["soi_only"] = {"rate_per_gs": rate_soi, "tau_max_gs": n_live_at_8gb / rate_soi,
                    "orbit_fraction": n_live_at_8gb / rate_soi / C["orbit_gs"][0]}
prom["orbit_scale_soi_GB"] = round(rate_soi * C["orbit_gs"][0] * C["live_bytes"][0] / 1e9, 1)

out = {"anchors": {k: {"value": v[0], "unit": v[1], "src": v[2]} for k, v in C.items()},
       "cpu_at_1e9": cpu, "cpu_total": cpu_total,
       "mem_at_1e9": mem, "build_over_floor_x": build_floor_ratio,
       "promotion_residency": prom,
       "not_composed": ["gravity at c (cursor + version ring: designed, not wired)",
                        "rotating holes (compiled, not in the resolver)",
                        "dispersed-fleet phase certificate (2373: quadratic in F)"]}
print(json.dumps(out, indent=1))
with open(__file__.replace("ledger.py", "ledger-out.json"), "w") as f:
    json.dump(out, f, indent=1)
