#!/usr/bin/env python3
"""The 10^9 CPU ledger re-composed after 73b5 (the churn row's wholesale arm killed),
with the stream row's cost constant measured end-to-end on shipped main (this run).

Every constant: (a) measured by this run (probes.log, prof1e5.log — shipped `nladder`
+ `belt_first`, Linux/x86, orders of magnitude), or (b) page-cited with run id.
CPU is CPU-seconds per presented wall-second at rtf 100 ("cores"); M1 budget ~4 P-cores.
"""
import json

N = 1_000_000_000
RTF = 100.0
M1_BUDGET = 4.0
GS_PER_WALL = RTF  # game-s per wall-s presented

C = {}

# ---- this run's measurements (work/probes.log, work/prof1e5.log; prof build, 540 frames, N=1e5 coast) ----
C["kick_item_us_x86"] = (82.5, "us/call", "prof1e5: item: kick 286.8 us/frame / 3.48 calls/frame")
C["boundary_item_us_x86"] = (18.4, "us/call", "prof1e5: item: boundary 63.1/3.43")
C["apply_us_x86"] = (7.6, "us/call", "prof1e5: apply 53.2/6.99")
C["walk_us_x86"] = (7.0, "us/call", "prof1e5: root_state_raw 47.6/6.83")
C["engine_p50_ms_1e5"] = (0.046, "ms", "probes.log (097e same-day: 0.078)")
C["b_per_body_1e5"] = (2348, "B", "probes.log (= 097e)")
C["belt_first_p50_gs"] = (14071, "game-s", "probes.log belt_first 10000 (= cd3b to the digit)")
C["kicks_total_1e5_10s"] = (1920, "kicks", "probes.log: = kicks_total_1e4_10s -> belt inert, player-only stream")

# ---- page-cited ----
C["lambda_fired"] = (4.0e-5, "1/body/game-s", "0659 (wiki/budget-1e9): 3.6-4.3e-5, K-flat, p=1.0")
C["lambda_planned"] = (7.1e-5, "1/body/game-s", "cd3b: 2 ev/body/interval (belt_first 14071*2 gs)")
C["cost_cd3b_m1"] = (29.3, "us", "cd3b composition constant (M1)")
C["m1_over_x86_event"] = (208 / 355.0, "x", "cd3b: shipped 208 M1 = 355 x86")
C["split8_survival"] = (8.0 * 0.615, "x", "cd3b: split 8 (de7b, welded) x secular survival 0.615 (1a46)")
C["stream_composed_cd3b"] = ((5.3, 8.4), "cores M1", "cd3b letter")
C["churn_73b5"] = ((0.35, 1.4), "cores", "73b5 (gold, checker-corrected): 355/E_pair at E*=1024-256, leak-certified")
C["churn_old"] = ((2.8, 5.5), "cores", "08d0 (superseded by 73b5)")
C["mint_worst"] = (1.9, "cores", "cd3b: every Dohnanyi conjunction re-mints at 16.4 us")
C["view_due_form"] = (0.1, "cores", "e3a4")
C["frame_bound"] = (12.0 * 60 / 1000.0, "cores", "12 ms x 60 fps")
C["floor_write_ns"] = (50.0, "ns", "b063: the binding's output bits, 1-2 lines")
C["floor_arith_us"] = (6.0, "us", "a765: key 2.3 + Carlson compile <=2.9 (de99) + tail ~1")
C["kick_m1_cd6e_us"] = ((8.0, 19.0), "us", "cd6e: composed closed-form kick, lean-cold, flat in e")
C["kick_native_262f_us"] = (4.0, "us", "262f: native port projection at belt keys")

# ---- the stream row, one instrument (fired rate x measured cost), M1-adjusted ----
ev_per_wall = C["lambda_fired"][0] * N * GS_PER_WALL          # events per wall-s at 1e9, rtf 100
cost_m1_measured = C["kick_item_us_x86"][0] * C["m1_over_x86_event"][0]
stream = {}
stream["shipped_measured_m1"] = ev_per_wall * cost_m1_measured * 1e-6
stream["shipped_cd3b_letter_m1"] = ev_per_wall * C["cost_cd3b_m1"][0] * 1e-6
stream["composed_measured_m1"] = stream["shipped_measured_m1"] / C["split8_survival"][0]
stream["composed_cd3b_letter_m1"] = stream["shipped_cd3b_letter_m1"] / C["split8_survival"][0]
# floor ladder at the SAME fired rate
stream["at_write_floor"] = ev_per_wall * C["floor_write_ns"][0] * 1e-9
stream["at_arith_floor_shipped_cadence"] = ev_per_wall * C["floor_arith_us"][0] * 1e-6
stream["at_arith_floor_split8"] = stream["at_arith_floor_shipped_cadence"] / C["split8_survival"][0]
stream["at_cd6e_composed_split8"] = ev_per_wall * C["kick_m1_cd6e_us"][0][0] * 1e-6 / C["split8_survival"][0]
# closure bar: max cost/event that fits 4 cores with split8+survival
stream["closure_cost_us"] = M1_BUDGET / (ev_per_wall / C["split8_survival"][0]) * 1e6

# ---- the corrected 10^9 CPU ledger (post-73b5) ----
def row(lo, hi): return [round(lo, 2), round(hi, 2)]
led = {}
led["stream_composed"] = {"today_cost": row(stream["composed_measured_m1"], stream["composed_measured_m1"]),
                          "cd3b_letter_cost": list(C["stream_composed_cd3b"][0]),
                          "src": "this run x cd3b"}
led["cert_churn"] = {"cores": list(C["churn_73b5"][0]), "src": "73b5 (replaces 2.8-5.5)"}
led["key_mint_worst"] = {"cores": [0.0, C["mint_worst"][0]], "src": "cd3b (0 with efd4 intern)"}
led["view_serve"] = {"cores": [C["view_due_form"][0]] * 2, "src": "e3a4"}
led["frame"] = {"cores": [C["frame_bound"][0]] * 2, "src": "budget"}
tot_today = [sum(v["cores"][0] if isinstance(v["cores"], list) else v["cores"][0] for k, v in led.items() if k != "stream_composed") + stream["composed_measured_m1"],
             sum(v["cores"][1] if isinstance(v["cores"], list) else v["cores"][0] for k, v in led.items() if k != "stream_composed") + stream["composed_measured_m1"]]
tot_letter = [tot_today[0] - stream["composed_measured_m1"] + C["stream_composed_cd3b"][0][0],
              tot_today[1] - stream["composed_measured_m1"] + C["stream_composed_cd3b"][0][1]]
total = {"today_cost": row(*tot_today), "today_over_budget": row(tot_today[0] / M1_BUDGET, tot_today[1] / M1_BUDGET),
         "cd3b_letter_cost": row(*tot_letter), "letter_over_budget": row(tot_letter[0] / M1_BUDGET, tot_letter[1] / M1_BUDGET),
         "pre_73b5_letter": [10.8, 16.6], "stream_share_today": row(stream["composed_measured_m1"] / tot_today[0],
                                                                   stream["composed_measured_m1"] / tot_today[1])}

out = {"measured": {k: {"value": v[0], "unit": v[1], "src": v[2]} for k, v in C.items()},
       "events_per_wall_s_at_1e9_rtf100": ev_per_wall,
       "stream_row": {k: (round(v, 2) if isinstance(v, float) else v) for k, v in stream.items()},
       "cpu_ledger_post_73b5": {k: (v if k != "stream_composed" else v) for k, v in led.items()},
       "total": total}
print(json.dumps(out, indent=1))
with open(__file__.replace("ledger.py", "ledger-out.json"), "w") as f:
    json.dump(out, f, indent=1)
