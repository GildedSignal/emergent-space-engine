#!/usr/bin/env python3
"""Fermi budget for 10^9 bodies on one 8 GB M1, RTF 1 (1 game-second = 1 s).
Every anchor is measured (repo M1 numbers, this run's x86 numbers, or the B9 red-team
gloss); nothing is tuned. Outputs the term table, the reconciliation of the 190-core
headline, the scene sweep, and the H_live statement.
"""
import json

# ---- machine (M1, from docs/HANDOFF.md) --------------------------------------
M1 = dict(cores=4, bw=60e9, ram_usable=5e9, frame_s=16.7e-3, ops=1e10)

# ---- anchors ------------------------------------------------------------------
A = dict(
    # per-kick cost, microseconds
    kick_m1_us=29.0,          # HANDOFF: plane kick, M1 (15 of them rebinding fit+compile)
    kick_made_x86_us=36.0,    # this run: universe --kick-bench, median, made bodies
    kick_leavers_x86_us=92.7, # this run: fleet members, median (p99 478)
    kick_floor_ns=24.0,       # this run: designed-kick arithmetic floor (i128 + memo probe)
    # cadences, kicks per orbit
    cad_b9_ceiling=512,       # B9 gate ceiling: crossings per cycle <= 2m*log2+8, m=16, e~0.9
    cad_h0190=32,             # H0190: kicks per orbit, un-averaged
    cad_avg=0.3,              # H0190: with orbit-averaged tides (adopted lever)
    # event cost target, microseconds (red-team B9 gloss)
    event_us=2.0,
    # memory, bytes
    tube_b=16,                # law.md: the 16-byte tube
    prog_bits=0.126,          # gold components-98bc: bits per body, belt program
    scar_b=24,                # 16 B tube + ~8 B Elias-Fano index (law.md populations)
    # O(N) per-item costs today, microseconds
    gather_item_us=180.0,     # 83% of a 16.7 ms frame at the plane's 76 emitters (M1)
    enc_item_us=190.0,        # HANDOFF: the player's encounter check, per item (M1)
    enc_setup_us=12.0,        # law.md: 2.5-24 us per candidate pair per element change
    # scenes
    T_orbit_adversarial=5400.0,   # 90 min (the headline's scene: ALL bodies)
    T_orbit_year=3.15e7,
)
N = 1e9

def cores(n, cad, cost_us, T):
    return n * cad / T * cost_us * 1e-6  # CPU-seconds per game-second = cores

out = {"anchors": {k: A[k] for k in A}}

# ---- term 1: kicks -------------------------------------------------------------
rows = []
for label, cad, cost in [
    ("headline arithmetic: B9 ceiling cadence at the 2 us event cost", A["cad_b9_ceiling"], A["event_us"]),
    ("today, honest pairing: H0190 cadence at the M1 kick cost", A["cad_h0190"], A["kick_m1_us"]),
    ("today, x86 fleet members (worst real)", A["cad_h0190"], A["kick_leavers_x86_us"]),
    ("designed: averaged cadence at the 2 us event target", A["cad_avg"], A["event_us"]),
    ("designed, arithmetic floor only (this run)", A["cad_avg"], A["kick_floor_ns"] / 1e3),
    ("designed + re-anchor jet (0.05 compiles/kick, compile 1-30 us)", A["cad_avg"], A["event_us"]),
]:
    c = cores(N, cad, cost, A["T_orbit_adversarial"])
    rows.append({"pairing": label, "cadence_per_orbit": cad, "cost_us": cost,
                 "cores_at_1e9": round(c, 4), "verdict": "PASS" if c < M1["cores"] else f"DEAD x{c/M1['cores']:.0f}"})
out["kicks"] = rows
# jet amortization, explicit
out["kicks"].append({"pairing": "re-anchor amortized add-on: 0.05 x compile(1..30 us)",
                     "cadence_per_orbit": A["cad_avg"], "cost_us": "0.05..1.5",
                     "cores_at_1e9": round(cores(N, A["cad_avg"], 0.05 * 30, A["T_orbit_adversarial"]), 4)})

# ---- term 2: encounter setup (rides the kick cadence, k candidate pairs) -------
enc = []
for k in (1, 4):  # taleb-09b5 gold: real encounters lie within partner rank ~4
    for setup_us, tag in ((A["enc_setup_us"], "today's 12 us midpoint"),
                          (A["event_us"], "at the 2 us event target")):
        c = cores(N, A["cad_avg"] * k, setup_us, A["T_orbit_adversarial"])
        enc.append({"candidates_per_kick": k, "setup_us": setup_us, "tag": tag,
                    "cores_at_1e9": round(c, 4), "verdict": "PASS" if c < M1["cores"] else f"DEAD x{c/M1['cores']:.0f}"})
out["encounter_setup"] = enc

# ---- term 3: memory ------------------------------------------------------------
mem = []
for label, bpb in [("stored tubes (16 B each)", A["tube_b"]),
                   ("population programs (gold components-98bc)", A["prog_bits"] / 8)]:
    total = N * bpb
    mem.append({"form": label, "bytes_per_body": bpb, "GB_at_1e9": round(total / 1e9, 3),
                "verdict": "PASS" if total < M1["ram_usable"] else f"DEAD x{total/M1['ram_usable']:.1f}"})
# scars: live distinctions. f = actively-kicked fraction
for f in (1e-3, 1e-2, 1e-1, 1.0):
    total = N * f * A["scar_b"] + N * A["prog_bits"] / 8
    mem.append({"form": f"programs + scars, kicked fraction {f:g}", "GB_at_1e9": round(total / 1e9, 3),
                "verdict": "PASS" if total < M1["ram_usable"] else f"DEAD x{total/M1['ram_usable']:.1f}"})
out["memory"] = mem
out["max_live_distinctions"] = int(M1["ram_usable"] / A["scar_b"])  # scar cap at 24 B

# ---- term 4: bandwidth ---------------------------------------------------------
bw = []
for cad, cost_b in ((A["cad_b9_ceiling"], 128), (A["cad_avg"], 64)):
    bps = N * cad / A["T_orbit_adversarial"] * cost_b
    bw.append({"cadence": cad, "bytes_per_kick": cost_b, "GB_s": round(bps / 1e9, 3),
               "verdict": "PASS" if bps < M1["bw"] else f"DEAD x{bps/M1['bw']:.0f}"})
out["bandwidth"] = bw

# ---- term 5: view gather -------------------------------------------------------
g = []
for per_item, tag in ((A["gather_item_us"], "today's plane gather"),
                      (1.0, "a 1 us/item rewrite"),
                      (1e-3, "a 1 ns/item rewrite")):
    t = per_item * 1e-6 * N
    g.append({"tag": tag, "frame_seconds_at_1e9_items": t,
              "verdict": f"DEAD x{t/ (0.3*M1['frame_s']):.0f} vs 30% of one frame"})
# aggregated VISIBLE items, every frame
for V, per in ((1e4, 1.0), (1e5, 1.0), (1e6, 1e-3)):
    t = V * per * 1e-6
    g.append({"tag": f"aggregated to {V:g} visible at {per} us each, EVERY frame", "frame_seconds": t,
              "verdict": "PASS" if t < 0.3 * M1["frame_s"] else "DEAD"})
# the view is also surprise-driven: only CHANGED visible items re-gather per frame
kicks_s_designed = N * A["cad_avg"] / A["T_orbit_adversarial"]
t = (kicks_s_designed / 60.0) * 1.0e-6
g.append({"tag": "incremental: changed visible items per frame (933 at the designed kick rate) x 1 us",
          "frame_seconds": t, "verdict": "PASS" if t < 0.3 * M1["frame_s"] else "DEAD"})
out["gather"] = g

# ---- the 190-core reconciliation ----------------------------------------------
r = cores(N, A["cad_b9_ceiling"], A["event_us"], A["T_orbit_adversarial"])
today = cores(N, A["cad_h0190"], A["kick_m1_us"], A["T_orbit_adversarial"])
out["reconciliation"] = {
    "headline": "0.19 core/M x 1000 = 190 cores",
    "its_arithmetic": f"{A['cad_b9_ceiling']} events/orbit x {A['event_us']} us / 5400 s x 1e9 = {r:.0f} cores",
    "today_honest": f"{A['cad_h0190']} kicks/orbit x {A['kick_m1_us']} us = {today:.0f} cores (x86 members: {cores(N, A['cad_h0190'], A['kick_leavers_x86_us'], A['T_orbit_adversarial']):.0f})",
    "note": "the headline pairs the gate-ceiling cadence with the cheap event cost; today's real pairing is the reverse (16x better cadence, 14.5x worse cost); the two errors cancel to within 10%",
    "designed": f"{A['cad_avg']}/orbit x {A['event_us']} us = {cores(N, A['cad_avg'], A['event_us'], A['T_orbit_adversarial']):.2f} core",
}

# ---- scene sweep (P5): bill ~ 1/T_orbit ----------------------------------------
sweep = []
for label, n, T in [("adversarial: all 1e9 on 90-min orbits", N, A["T_orbit_adversarial"]),
                    ("goal-shaped: 1e7 in fleets (90 min) + rest on >= year orbits", 1e7, A["T_orbit_adversarial"]),
                    ("goal-shaped: the 9.9e8 remainder", 9.9e8, A["T_orbit_year"])]:
    c = cores(n, A["cad_avg"], A["event_us"], T)
    sweep.append({"scene": label, "cores_kicks_only": round(c, 5)})
out["scene_sweep"] = sweep

# ---- designed-scene total, adversarial scene ------------------------------------
out["designed_total"] = {
    "kicks": round(cores(N, A["cad_avg"], A["event_us"], A["T_orbit_adversarial"]), 3),
    "encounter_setup_k4_12us": round(cores(N, A["cad_avg"] * 4, A["enc_setup_us"], A["T_orbit_adversarial"]), 3),
    "encounter_setup_k4_2us": round(cores(N, A["cad_avg"] * 4, A["event_us"], A["T_orbit_adversarial"]), 3),
    "gather_incremental": round((kicks_s_designed / 60.0) * 1e-6 * 60, 4),  # CPU-s per game-s
    "of_4_cores": "PASS with 1.4x margin at k=4 x 12 us; 13x at k=4 x 2 us",
    "binding_term": "encounter setup (5-48x the designed kick cost at today's 2.5-24 us per candidate pair)",
}

# ---- lever ranking ---------------------------------------------------------------
out["levers"] = [
    {"lever": "cadence 32 -> 0.3 (orbit-averaged tides, adopted H0190)", "gain": "107x", "status": "banked in the design"},
    {"lever": "kill the rebind in the kick (29 -> 14 us)", "gain": "2x", "status": "Sol's wt/kick, measured share 15/29; x86 bench here: 97% of kicks rebind"},
    {"lever": "kick arithmetic 14 us -> 2 us event target (floor measured here at 24 ns)", "gain": "7x (80x above floor)", "status": "compiler work, not a physics bound"},
    {"lever": "encounter setup 12 us -> 2 us per candidate pair", "gain": "6x", "status": "the un-banked lever: it is 5-48x the designed kick cost"},
    {"lever": "gather aggregation + incrementality", "gain": ">= 1e5 x", "status": "mandatory: O(N) gather is dead by 5-7 orders even at 1 ns/item"},
    {"lever": "scar reabsorption", "gain": "unbounded session length", "status": "0.9 MB/s of distinction bits = 3.3 GB/h if never reclaimed"},
]

# ---- H_live (lens question 2) -----------------------------------------------------
hl = kicks_s_designed * 128 / 8
out["h_live"] = {
    "kicks_per_game_second_adversarial": kicks_s_designed,
    "raw_distinction_MB_per_game_second": round(hl / 1e6, 3),
    "one_hour_accumulation_GB_if_never_reabsorbed": round(hl * 3600 / 1e9, 2),
    "scar_cap_from_5GB": out["max_live_distinctions"],
    "statement": "the instantaneous footprint passes, but an unreabsorbed 0.9 MB/s of distinction bits is 3.3 GB/h: scar reclamation must run at >= the distinction rate, or every long session dies regardless of N",
}

print(json.dumps(out, indent=1))
