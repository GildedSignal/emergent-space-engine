#!/usr/bin/env python3
"""The 10^7 rung of the N ladder, composed from measured constants — CORRECTED RECORD.

Second-author run 20261018-1237-...-ef63 on 20261018-1126-library-686f (silver). The
checker found the original re-kick line divided a per-game-second rate by rtf where
wall-second rates need x rtf (ladder.txt's own conversion, line 143: "357 kicks a
game-second = 36,000 a wall second at rtf 100") -- an rtf^2 = 1e4 error. This file is
the original compose_rung.py with exactly those changes:

  1. re-kick = (N_del / T*(N)) * rtf * rekick_us, N_del the bodies carried by the
     delete (shipped rows have no delete, hence no add-back: 0 by construction);
  2. T*(N) from e29c's three frozen bars through the T* ~ N^(-1/4) law (verified
     in-script against all three bars; derivation in predictions.md P1), replacing the
     original's single stale constant T* = 3.37e7 held for every N;
  3. the 10^8 row (the decade the original skipped) and the pass/fail crossover;
  4. the deleted-stream cross-check (e29c's own published reading, a cost identity);
  5. the stale constant's reading kept in the output, so the record documents its own
     error rather than hiding it.

Every other constant, citation and column is byte-identical to the original run. The
calibration anchor stays the flown 5x10^5 wave point (the 10^6 wave was never flown --
flights stop at 5x10^5; the 10^6 row is the composition's own extrapolation)."""
import math

C = {
 # ladder.txt (artifacts/runs/nladder/ladder.txt, after 0f112b89/32e9e986, 14 Oct)
 "kick_us_wave": (30.0, "ladder.txt: 'the wave is N kicks at ~30 us'"),
 "kick_us_belt": (50.4, "kick-cadence 3570: belt kick p50 50.4 us (range band top)"),
 "budget": (0.72, "ladder.txt: '0.72 s of budget per wall second' (12 ms/frame, 60 fps)"),
 "window_gs": (1483.0, "ladder.txt: first belt kicks 13,051-14,534 game-s (one wave)"),
 "rtf": (100.0, "ladder.txt rung protocol; conversion at ladder.txt:143: '357 kicks a game-second = 36,000 a wall second at rtf 100'"),
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
 "rekick_us": (33.0, "library-directions f5bd: one sparse re-kick 29-37 us"),
 "rekick_cost_ratio": (0.6, "e29c bars.py: REKICK_COST = 0.6 of one fired kick (f5bd: 0.51-0.6x)"),
 "cadence_ev_B_gs": (3.55e-5, "e29c bars.py / f5bd: the belt's metronome stream rate, ev/(body.game-s)"),
 "ram_GB": (8.0, "the machine"),
 "rung_s": (60.0, "AGENTS.md: each test finishes within 60 s"),
 "gate_GiB": (4.0, "gate N1: under 4 GiB"),
 # calibration anchor (flown)
 "anchor_N": (5e5, "ladder.txt wave flight: 5x10^5"),
 "anchor_work_s": (15.0, "ladder.txt: 'at 5x10^5 it is ~15 s of work ... lags 0.45 s (frames stay within 12 ms)'"),
}

# e29c (gold, 20261017-2142-library-e29c) frozen bars: T*(q_view) in game-s by N.
# "never fires before the 8e6-gs horizon at any N <= 1e6"; at 1e9 k* = 213 carried
# kicks and cadence x T* = 3.55e-5 x 5.99e6 = 212.6 ~= 213 (the identity holds).
T_STAR_BARS = {1e5: 5.99e7, 1e6: 3.37e7, 1e9: 5.99e6}
T_STAR_LAW_EXP = -0.25  # q_view ~ N^-1/2 (e29c bars.py, uniform belt density) and
                        # drift ~ t^2 (f5bd's fence) => T* ~ q_view^(1/2) ~ N^-1/4

def v(k): return C[k][0]

def T_star(N):
    """The fence interval at N, anchored on e29c's 10^9 bar through the N^-1/4 law."""
    return T_STAR_BARS[1e9] * (N / 1e9) ** T_STAR_LAW_EXP

def verify_T_star_law():
    """The law must reproduce all three frozen bars (else interpolation is unjustified)."""
    out = {}
    for N, bar in sorted(T_STAR_BARS.items()):
        rel = T_star(N) / bar - 1.0
        out[N] = rel
        assert abs(rel) < 0.02, f"T* law misses the {N:.0e} bar by {rel:+.2%}"
    return out

window_wall = v("window_gs") / v("rtf")        # 1483 gs at rtf 100 -> wall s
budget_s = v("budget") * window_wall           # engine work budget inside the window
law_err = verify_T_star_law()
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
    # re-kick add-back, CORRECTED (this run): one firing per body per fence interval
    # T*(N); a per-game-second rate becomes per-wall-second by x rtf (rtf = game-s per
    # wall-s; ladder.txt:143). The original divided by rtf -- the rtf^2 = 1e4 error.
    if deletions > 0.0:
        N_del = belt * deletions               # bodies carried by the delete
        firings_per_wall_s = (N_del / T_star(N)) * v("rtf")
        d["rekick_s_per_s"] = firings_per_wall_s * v("rekick_us") / 1e6
        # e29c's published reading, a cost identity: share = 0.6/(T* x cadence) of the
        # deleted stream's own cost (0.6 = re-kick cost vs one kick, f5bd 0.51-0.6x)
        del_stream_s = (N_del * v("cadence_ev_B_gs")) * v("rtf")
        share = v("rekick_cost_ratio") / (T_star(N) * v("cadence_ev_B_gs"))
        d["rekick_via_e29c_s_per_s"] = (share * del_stream_s * v("kick_us_wave") / 1e6,
                                        share * del_stream_s * v("kick_us_belt") / 1e6)
        d["rekick_pct_budget"] = d["rekick_s_per_s"] / v("budget")
    else:
        d["rekick_s_per_s"] = 0.0              # no delete -> nothing carried -> no add-back
        d["rekick_via_e29c_s_per_s"] = (0.0, 0.0)
        d["rekick_pct_budget"] = 0.0
    rows.append(d)

row("shipped", 1e6, 0.0, False)
row("shipped", 1e7, 0.0, False)
row("lazy birth only", 1e7, 0.0, True)
row("lazy + ES_SECULAR", 1e7, v("belt_deleted_plain"), True)
row("lazy + RES", 1e7, v("belt_deleted_res"), True)
row("lazy + RES", 1e8, v("belt_deleted_res"), True)   # the decade the original skipped
row("lazy + RES", 1e9, v("belt_deleted_res"), True)

# pass/fail crossover for the lazy+RES arm: wave work = the in-window budget
spare_frac = 1.0 - v("belt_deleted_res")
def crossover(cost_us):
    spared_needed = budget_s / (cost_us / 1e6)
    return (spared_needed - 1028.0) / spare_frac + 1028.0
cross_lo = crossover(v("kick_us_wave") + v("compile_us_lo"))   # cheapest reading
cross_hi = crossover(v("kick_us_belt") + v("compile_us_hi"))   # dearest reading

out = {
 "window_wall_s": round(window_wall, 2),
 "budget_in_window_s": round(budget_s, 2),
 "anchor_check": {
   "flown_work_s": v("anchor_work_s"),
   "composed_work_s": round(v("anchor_N") * v("kick_us_wave") / 1e6, 1),
   "flown_lag_game_s": 0.45,
   "note": "composition reproduces the flown wave work of the 5x10^5 anchor exactly (15 s vs 15.0 s); the flown verdict there was 'frames within 12 ms, presented time lags'"},
 "T_star_law": {
   "exp": T_STAR_LAW_EXP,
   "bars": {f"{N:.0e}": bar for N, bar in sorted(T_STAR_BARS.items())},
   "fit_error_per_bar": {f"{N:.0e}": f"{e:+.2%}" for N, e in law_err.items()},
   "identity_cadence_x_Tstar_1e9": v("cadence_ev_B_gs") * T_STAR_BARS[1e9],
   "e29c_k_star": 213.0,
   "T_star_1e7_gs": T_star(1e7), "T_star_1e8_gs": T_star(1e8),
 },
 "crossover_N": {"lo": cross_lo, "hi": cross_hi,
   "note": "the lazy+RES wave equals the in-window budget at N in [cross_hi, cross_lo]; below it the arm passes, above it fails"},
 "stale_constant_reading": {
   "T_star_gs": 3.37e7,
   "rekick_1e9_s_per_s": (9.9438e8 / 3.37e7) * v("rtf") * v("rekick_us") / 1e6,
   "note": "the ORIGINAL run's constant (T* frozen at the 10^6 bar for every N, and its 'q_view only grows T*' cite contradicted by e29c's own bars, which SHRINK: 5.99e7 -> 3.37e7 -> 5.99e6). This is the reading the checker named (0.098); the fence's own 10^9 bar is the honest one."},
 "rows": rows,
 "constants": {k: {"value": C[k][0], "cite": C[k][1]} for k in C},
}
import json
print(json.dumps(out, indent=1))
print()
hdr = f"{'arm':<20}{'N':>8}{'birth GB':>10}{'build s':>9}{'wave x-bud':>13}{'live GB':>9}{'steady s/s':>13}{'+re-kick':>10}{'e29c ratio':>13}{'%bud':>6}"
print(hdr); print("-" * len(hdr))
for d in rows:
    lo, hi = d["rekick_via_e29c_s_per_s"]
    print(f"{d['arm']:<20}{d['N']:>8.0e}{d['birth_GB']:>10.2f}{d['build_s']:>9.0f}"
          f"{d['wave_ratio']:>6.1f}-{d['wave_ratio_hi']:<6.1f}{d['wave_live_GB']:>9.2f}"
          f"{d['steady_s_per_s']:>6.3f}-{d['steady_s_per_s_hi']:<6.3f}{d['rekick_s_per_s']:>10.4f}"
          f"{lo:>8.3f}-{hi:<4.3f}{d['rekick_pct_budget']*100:>5.1f}%")
print()
print(f"window {window_wall:.1f} wall s; budget in window {budget_s:.1f} s; frame budget {v('budget')} s/s; RAM {v('ram_GB')} GB; rung {v('rung_s'):.0f} s; gate {v('gate_GiB')} GiB")
print(f"delete fractions: plain {v('belt_deleted_plain'):.3f} (spare {1-v('belt_deleted_plain'):.3f}), RES {v('belt_deleted_res'):.4f} (spare {1-v('belt_deleted_res'):.4f})")
print(f"T* law N^{T_STAR_LAW_EXP}: fit error per bar " + ", ".join(f"{N:.0e}:{e:+.2%}" for N, e in law_err.items()) + f"; T*(1e7)={T_star(1e7):.3e} gs, T*(1e8)={T_star(1e8):.3e} gs; identity cadence x T*(1e9) = {v('cadence_ev_B_gs')*T_STAR_BARS[1e9]:.1f} ~= k* 213")
print(f"lazy+RES crossover (wave = budget): N in [{cross_hi:.2e}, {cross_lo:.2e}] -- the 1e7 pass is rung-exact; 1e8 fails")
print(f"STALE original constant (T* = 3.37e7 held for every N): 1e9 add-back {(9.9438e8/3.37e7)*v('rtf')*v('rekick_us')/1e6:.3f} s/s -- the checker's 0.098; honest 10^9 bar (5.99e6 gs): {rows[-1]['rekick_s_per_s']:.3f} s/s")
print(f"1e9 one-thread total: spared stream {rows[-1]['steady_s_per_s']:.3f}-{rows[-1]['steady_s_per_s_hi']:.3f} + re-kick {rows[-1]['rekick_s_per_s']:.3f} = {rows[-1]['steady_s_per_s']+rows[-1]['rekick_s_per_s']:.3f}-{rows[-1]['steady_s_per_s_hi']+rows[-1]['rekick_s_per_s']:.3f} s/s against {v('budget')} (memory: birth {rows[-1]['birth_GB']:.2f} GB, live {rows[-1]['wave_live_GB']:.2f} GB -- both over the {v('ram_GB')} GB machine; partitioned per doll)")
print("wave x-bud: wave work (first kicks + lazy promotions) as a multiple of the window's engine budget, low-high kick cost")
print("+re-kick: (N_del/T*(N)) x rtf x 33 us, the checker's named formula; e29c ratio: 0.6/(T* x cadence) of the deleted stream at kick 30-50.4 us")
