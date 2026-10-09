#!/usr/bin/env python3
"""The 10^9 steady-state budget, generator-native, ANCHORED on the shipped code at N >= 1e6.

Second-author run 20261009-0401 (checker's named experiment for 20261009-0208-fermi-fe6b).
Everything here regenerates from `cascade.jsonl`, which `run-bench.sh` produces from the
SHIPPED crates (`cargo run --release -p emergent-encounters -- kick` plus a path-dependent
bench that calls the crate's own Sorted/is_candidate/pair_events unchanged).

Constants (all measured this run, Linux/x86 shared runner, load 1.3-2.9, single thread;
orders of magnitude only — the integrator re-measures on the M1):
- M1/x86 factor 1.86 = shipped anchor us_per_kick on the M1 (4345.4, frozen kick.jsonl)
  over this run's same experiment (8071.9). Applied to every timing to state M1-implied
  cores; raw x86 numbers are in cascade.jsonl.
- The pairs-per-kick law (six global cases, <= 7% error, N up to 1e7):
      pairs/kick = 0.0346 * n * (1+X) / (2*(X-1)),  X = a_hi/a_lo,
  i.e. partners of a body at a are proportional to n*a/W_a; a belt's mean saturates at
  0.0173*n for very wide belts. The budget's 812.8 pairs/kick is a CELL constant
  (n_cell = 1e4, X = 1.5), not a belt-density convention: at 10^9 in ONE belt the same
  law gives 1.7e7-8.7e7 pairs/kick (measured anchor point: 86,332 at 1e6 fixed extent).
- Queue churn (Rust BinaryHeap, packed (u64 t, u32 id), depth 7.8e6 = 10^9/128 keys):
  176-188 ns per pop+push (139-147 ns at 2e6), load-dependent. The author's Python heapq 2.87 us/op was 15x off.
"""
import json, math, sys

N = 1e9          # bodies
P = 1.26e8       # s per orbit (4 yr, AU-scale belt) [game-seconds]
RTF = 100        # the plane's flying speed [B1/HANDOFF]
SKIN = 12.6      # slack-skin factor, board-adopted [B1 taste log 6 Oct]
K_AVG = 0.28     # orbit-averaged kicks per body per orbit [S3]
K_FULL = 32.0    # unaveraged [S3]
COMPILE_US = 3.4         # [F1, prior run, reproduced]
KICK_ARITH_S = 50e-9 + 0.05 * COMPILE_US * 1e-6  # 50 ns + 0.05 compiles/kick [S6]
ENC_PER_BODY_ORBIT = 0.04  # CORRECTED: scale.jsonl at the belt's own geometry (was 0.00586)
ENC_US = 1.0
REABSORB_PER_S_CORE = 5.7e6   # [F2, prior run, reproduced]
SCAR_BYTES = 24
KEY_BYTES = 12
N_CELL = 1e4      # the cell (program) size the pairs law anchors to
X_CELL = 1.5      # cell belt geometry (anchor)

# --- parse the run's own record ------------------------------------------------
rows = [json.loads(l) for l in open("cascade.jsonl") if l.startswith("{")]
anchor = [r for r in rows if r.get("exp") == "kick" and r.get("eps") == 1e-9][-1]
heap78 = [r for r in rows if r.get("exp") == "heap" and r["depth"] == 7_800_000][-1]
ver = [r for r in rows if r.get("exp") == "verify"][-1]
gl = {r["case"]: r for r in rows if r.get("exp") == "cascade" and r.get("mode") == "global"}
cel = {r["case"]: r for r in rows if r.get("exp") == "cascade" and r.get("mode") == "cells"}

PAIRS_ANCHOR = anchor["pairs_per_kick"]                 # 812.8, shipped code
US_PAIR_X86 = anchor["us_per_pair"]                    # 9.93, the shipped loop itself
US_KICK_SHIPPED_X86 = anchor["us_per_kick"]             # 8071.9
M1_FACTOR = 4345.4 / US_KICK_SHIPPED_X86                # frozen M1 anchor / this x86 run
US_PAIR_M1 = US_PAIR_X86 * M1_FACTOR                    # ~5.8: the M1 per-pair constant
CHANGED = anchor["changed_fraction"]                    # 0.0024 at tidal eps
SKIPS = anchor["slack_skippable_fraction"]              # 0.9458
NS_Q = heap78["ns_per_pop_push"]                        # 188
CELLS_TOUCHED = cel["c6W"]["blocks_per_kick"]           # 6.2 blocks scanned per kick
US_PAIR_CELL_M1 = cel["c6W"]["us_per_pair"] * M1_FACTOR # local-index per-pair, M1-implied

def law_pairs(n, X):
    return 0.0346 * n * (1.0 + X) / (2.0 * (X - 1.0))
G7 = "g7W" in gl  # the 1e7 case exceeded 300 s/kick on the loaded shared runner; optional
kicks_s = N * K_AVG / P * RTF          # 222/s
kicks_s_full = N * K_FULL / P * RTF
enc_s = N * ENC_PER_BODY_ORBIT / P * RTF

out = []
r = out.append
r(("M1/x86 factor (frozen M1 anchor 4345.4 us / this run 8071.9 us)", f"{M1_FACTOR:.2f}"))
r(("pairs/kick law check: a4/g5w/g5W/g6w/g6W/g6Wd measured vs 0.0346*n*(1+X)/(2(X-1))",
   " / ".join(f"{gl[k]['pairs_per_kick']:.0f}~{law_pairs(gl[k]['n'], gl[k]['a_hi']/gl[k]['a_lo']):.0f}"
              for k in ("a4", "g5w", "g5W", "g6w", "g6W", "g6Wd"))))
if G7:
    r(("pairs/kick at 1e7, X=1500 (measured / law)", f"{gl['g7W']['pairs_per_kick']:.0f} / {law_pairs(1e7, 1500):.0f}"))
    r(("us_per_pair x86 at 1e4 / 1e6[1,150] / 1e7[1,1500] / cells-1e6",
       f"{US_PAIR_X86:.1f} / {gl['g6W']['us_per_pair']:.1f} / {gl['g7W']['us_per_pair']:.1f} / {cel['c6W']['us_per_pair']:.1f}"))
    r(("scanned/pairs: X=1.5 / 15 / 150 / 1500 global; cells[1,150]",
       f"{gl['a4']['scanned_per_kick']/gl['a4']['pairs_per_kick']:.1f} / {gl['g5W']['scanned_per_kick']/gl['g5W']['pairs_per_kick']:.1f} / "
       f"{gl['g6W']['scanned_per_kick']/gl['g6W']['pairs_per_kick']:.1f} / {gl['g7W']['scanned_per_kick']/gl['g7W']['pairs_per_kick']:.1f}; "
       f"{cel['c6W']['scanned_per_kick']/cel['c6W']['pairs_per_kick']:.1f}"))
else:
    r(("1e7 case", "not run to completion (>300 s/kick, loaded runner); law extrapolates 1.7e5 pairs/kick"))
r(("cells soundness (exact candidate-set equality vs global, kicks with mismatches)",
   f"{ver['kicks']} kicks, {ver['mismatches']} mismatches"))

casc_pair = PAIRS_ANCHOR * US_PAIR_M1 * 1e-6
casc_skin = casc_pair / SKIN
casc_phase = 4 * US_PAIR_M1 * 1e-6
r(("kick arithmetic (incremental + 0.05 compiles/kick)", f"{kicks_s * KICK_ARITH_S:.2e} cores"))
r((f"cascade per CELL of n={N_CELL:.0e}, two-tier, no skin (M1-implied)", f"{kicks_s * casc_pair:.3f} cores"))
r((f"cascade per cell, + slack skin {SKIN}x", f"{kicks_s * casc_skin:.4f} cores"))
r(("cascade per cell, phase-neighbour rank-4", f"{kicks_s * casc_phase:.2e} cores"))
_loc = gl['g6W']['us_per_pair'] / cel['c6W']['us_per_pair']
r((f"local cell index: per-pair gain at equal geometry (n=1e6, X=150: {gl['g6W']['us_per_pair']:.2f} -> {cel['c6W']['us_per_pair']:.2f} us x86)",
   f"{_loc:.2f}x -> skin cascade {kicks_s*casc_skin/_loc:.4f} cores"))
r(("SINGLE BELT at 1e9, X=1.5 (law 8.66e7 pairs/kick): cascade", f"{kicks_s * law_pairs(N, 1.5) * US_PAIR_M1 * 1e-6:.1e} cores"))
r(("SINGLE BELT at 1e9, wide (law 1.75e7 pairs/kick): cascade", f"{kicks_s * law_pairs(N, 150) * US_PAIR_M1 * 1e-6:.1e} cores"))
r(("cascade per cell, UNAVERAGED k=32, +skin / no skin", f"{kicks_s_full * casc_skin:.2f} / {kicks_s_full * casc_pair:.0f} cores"))

# --- the queue term (the author's gap), measured ------------------------------------------------
upd_cell = 1.0 + CELLS_TOUCHED          # own cell key + touched cells (a changed pair in a
# touched cell is near-certain at ~2.5e3 pair-windows per touched cell and changed=0.0024)
upd_window_noskin = PAIRS_ANCHOR        # every re-derived window re-queued
upd_window_skin = PAIRS_ANCHOR * (1.0 - SKIPS)
q = lambda upd: kicks_s * upd * NS_Q * 1e-9
r((f"event queue, WINDOW-level keys, no skin ({upd_window_noskin:.0f} pop+push/kick @ {NS_Q:.0f} ns)",
   f"{q(upd_window_noskin):.4f} cores"))
r(("event queue, window-level, with skin", f"{q(upd_window_skin):.4f} cores"))
r((f"event queue, CELL-level keys ({upd_cell:.1f} updates/kick)", f"{q(upd_cell):.2e} cores"))
r(("queue memory: per-body keys / cell keys (1 per 128-body block)", f"{N*KEY_BYTES/1e9:.1f} GB (>8) / {N/128*KEY_BYTES/1e6:.0f} MB"))
r(("queue depth at cell keys (1e5 cells) / window keys (per pair)",
   f"{N/N_CELL:.0e} / {law_pairs(N,1.5)*N/2:.1e} windows (does not fit; even cell-partitioned: {N/N_CELL*law_pairs(N_CELL,X_CELL)*N_CELL/2:.1e} x 12 B = {N/N_CELL*law_pairs(N_CELL,X_CELL)*N_CELL/2*12/1e9:.1f} GB)"))

r(("encounter handling (0.04/body/orbit, corrected)", f"{enc_s * ENC_US * 1e-6:.2e} cores"))
r(("program memory", f"{N * 0.126 / 8 / 1e6:.1f} MB"))
for f in (0.01, 0.1, 0.33):
    r((f"scars at live fraction {f:.0%} (24 B each)", f"{f * N * SCAR_BYTES / 1e9:.2f} GB"))
r(("global U-index, shipped Sorted layout (16 B/body)", f"{N * 16 / 1e9:.1f} GB  (> 8 GB — cell-local indexes, built on demand, 0.07 s per 1e6 measured)"))
r(("scar creation vs reabsorption", f"{kicks_s:.0f}/s vs {REABSORB_PER_S_CORE:.1e}/s/core ({REABSORB_PER_S_CORE/kicks_s:.0e}x slack)"))

for name, k, cost in (("averaged + skin", K_AVG, casc_skin),
                      ("averaged, no skin", K_AVG, casc_pair),
                      ("averaged + phase-neighbour", K_AVG, casc_phase)):
    per_rtf = N * k / P * cost
    r((f"max rtf on 4 cores: {name}", f"{4/per_rtf:,.0f}"))

board_190 = N * K_FULL / P * RTF * casc_pair
r(("re-derivation of board's '190 cores' (k=32, no skin, rtf 100, per cell)", f"{board_190:.0f} cores"))

print("| Term | value |")
print("|---|---|")
for name, val in out:
    print(f"| {name} | {val} |")
json.dump({"rows": [dict(name=n, val=v) for n, v in out],
           "constants": dict(pairs_anchor=PAIRS_ANCHOR, us_pair_x86=US_PAIR_X86,
                             us_pair_m1=US_PAIR_M1, m1_factor=M1_FACTOR, ns_queue=NS_Q,
                             changed=CHANGED, skips=SKIPS, cells_touched=CELLS_TOUCHED,
                             law_k=0.0346)},
          open("budget.json", "w"), indent=1)
