#!/usr/bin/env python3
"""The 10^7 rung of the N ladder, composed from measured constants.

Every constant is cited. No new measurement; the calibration anchor is the
flown 5x10^5 wave point. Verdicts are ratios against the single-threaded frame
budget (0.72 s of engine work per wall second, ladder.txt)."""
import json

C = {
 # ladder.txt (artifacts/runs/nladder/ladder.txt, after 0f112b89/32e9e986, 14 Oct)
 "kick_us_wave": (30.0, "ladder.txt: 'the wave is N kicks at ~30 us'"),
 "kick_us_belt": (50.4, "kick-cadence 3570: belt kick p50 50.4 us (range band top)"),
 "budget": (0.72, "ladder.txt: '0.72 s of budget per wall second' (12 ms/frame, 60 fps)"),
 "window_gs": (1483.0, "ladder.txt: first belt kicks 13,051-14,534 game-s (one wave)"),
 "rtf": (100.0, "ladder.txt rung protocol"),
 "steady_kicks_per_wall_s_1e7": (36000.0, "ladder.txt: 10^7 = 357 kicks/game-s = 36,000/wall-s (~1.4 cores)"),
 "build_us": (29.5, "ladder.txt: 28-31 us a body at birth (10^7 ~ 290 s)"),
 "birth_B": (2550.0, "ladder.txt: 2,407-2,700 B a body at birth (10^6 measured 2,407)"),
 # promotion.md (cbc5/8792: standalone mint 3.7-5.3 us; c4d3: shipped add_body 9.2 us p50)
 "compile_us_lo": (4.45, "promotion.md: mint = the compile, 3.7-5.3 us p50 on the flown store"),
 "compile_us_hi": (9.2, "promotion.md: shipped add_body promotion path 9.2 us p50 (c4d3)"),
 # memory: plateau after first kick (b30b via library-directions 6793)
 "plateau_B": (5060.0, "6793/b30b: live plateau 5,060 B after the first kick"),
 # compact row measured SOLO (HANDOFF scoreboard; shipmem built, not wired)
 "compact_bits_hi": (126.0, "HANDOFF scoreboard: 126 bits (driven belt, worst)"),
 # the delete law (nladder.md: 1a46 + checkers; f134/7fcf composed arm)
 "belt_deleted_plain": (274.0 / 712.0, "nladder.md: frozen exclusion deletes 274/712 of the belt"),
 "belt_deleted_res": (708.0 / 712.0, "nladder.md: RES deletes 434 more = 708/712 (checker2: tail bit-identical under RES)"),
 # the re-kick add-back (f5bd + e29c on library-directions)
 "T_star_gs": (3.37e7, "e29c's frozen bars: T*(q_view) = 5.99e7/3.37e7 gs at 10^5/10^6; zero firings below ~1e7-gs horizons; conservative arm holds the smaller for every N"),
 "rekick_us": (33.0, "library-directions f5bd: one sparse re-kick 29-37 us"),
 "ram_GB": (8.0, "the machine"),
 "rung_s": (60.0, "AGENTS.md: each test finishes within 60 s"),
 "gate_GiB": (4.0, "gate N1: under 4 GiB"),
 # calibration anchor (flown)
 "anchor_N": (5e5, "ladder.txt wave flight: 5x10^5"),
 "anchor_work_s": (15.0, "ladder.txt: 'at 5x10^5 it is ~15 s of work ... lags 0.45 s (frames stay within 12 ms)'"),
}

def v(k): return C[k][0]

window_wall = v("window_gs") / v("rtf")        # 1483 gs at rtf 100 -> wall s
budget_s = v("budget") * window_wall           # engine work budget inside the window
rows = []

def row(name, N, deletions, lazy):
    """One arm of the rung. deletions = belt fraction deleted; lazy = compact birth."""
    belt = max(N - 1028.0, 0.0)                # ladder population: the rest is belt
    plane = min(N, 1028.0)
    spared = belt * (1.0 - deletions) + plane  # bodies whose first kick fires
    d = {"N": N, "arm": name}
    if lazy:
        d["birth_GB"] = N * v("compact_bits_hi") / 8.0 / 1e9
        d["build_s"] = 0.0                     # lazy birth defers the compile (bit-for-bit, ladder_digest's 13 cases)
    else:
        d["birth_GB"] = N * v("birth_B") / 1e9
        d["build_s"] = N * v("build_us") / 1e6
    wave_kick_s = spared * v("kick_us_wave") / 1e6
    wave_kick_s_hi = spared * v("kick_us_belt") / 1e6
    wave_compile_s = spared * v("compile_us_lo") / 1e6 if lazy else 0.0
    wave_compile_s_hi = spared * v("compile_us_hi") / 1e6 if lazy else 0.0
    d["wave_ratio"] = (wave_kick_s + wave_compile_s) / budget_s
    d["wave_ratio_hi"] = (wave_kick_s_hi + wave_compile_s_hi) / budget_s
    d["wave_live_GB"] = spared * v("plateau_B") / 1e9   # resident if nothing demotes
    per_s = v("steady_kicks_per_wall_s_1e7") * (N / 1e7) * (1.0 - deletions)
    d["steady_s_per_s"] = per_s * v("kick_us_wave") / 1e6
    d["steady_s_per_s_hi"] = per_s * v("kick_us_belt") / 1e6
    # re-kick add-back: every body one sparse re-kick per T*; conservative arm holds T*
    # at its smallest measured value for every N (e29c's q_view(N) only grows T* further).
    d["rekick_s_per_s"] = (N / v("T_star_gs")) / v("rtf") * v("rekick_us") / 1e6
    rows.append(d)

row("shipped", 1e6, 0.0, False)
row("shipped", 1e7, 0.0, False)
row("lazy birth only", 1e7, 0.0, True)
row("lazy + ES_SECULAR", 1e7, v("belt_deleted_plain"), True)
row("lazy + RES", 1e7, v("belt_deleted_res"), True)
row("lazy + RES", 1e9, v("belt_deleted_res"), True)

out = {
 "window_wall_s": round(window_wall, 2),
 "budget_in_window_s": round(budget_s, 2),
 "anchor_check": {
   "flown_work_s": v("anchor_work_s"),
   "composed_work_s": round(v("anchor_N") * v("kick_us_wave") / 1e6, 1),
   "flown_lag_game_s": 0.45,
   "note": "composition reproduces the flown wave work of the 5x10^5 anchor exactly (15 s vs 15.0 s); the flown verdict there was 'frames within 12 ms, presented time lags'"},
 "rows": rows,
 "constants": {k: {"value": C[k][0], "cite": C[k][1]} for k in C},
}
print(json.dumps(out, indent=1))
print()
hdr = f"{'arm':<20}{'N':>8}{'birth GB':>10}{'build s':>9}{'wave x-bud':>13}{'live GB':>9}{'steady s/s':>13}{'+re-kick':>9}"
print(hdr); print("-" * len(hdr))
for d in rows:
    print(f"{d['arm']:<20}{d['N']:>8.0e}{d['birth_GB']:>10.2f}{d['build_s']:>9.0f}"
          f"{d['wave_ratio']:>6.1f}-{d['wave_ratio_hi']:<6.1f}{d['wave_live_GB']:>9.2f}"
          f"{d['steady_s_per_s']:>6.3f}-{d['steady_s_per_s_hi']:<6.3f}{d['rekick_s_per_s']:>9.4f}")
print()
print(f"window {window_wall:.1f} wall s; budget in window {budget_s:.1f} s; frame budget {v('budget')} s/s; RAM {v('ram_GB')} GB; rung {v('rung_s'):.0f} s; gate {v('gate_GiB')} GiB")
print(f"delete fractions: plain {v('belt_deleted_plain'):.3f} (spare {1-v('belt_deleted_plain'):.3f}), RES {v('belt_deleted_res'):.4f} (spare {1-v('belt_deleted_res'):.4f})")
print("wave x-bud: wave work (first kicks + lazy promotions) as a multiple of the window's engine budget, low-high kick cost")
