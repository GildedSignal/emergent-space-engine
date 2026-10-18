#!/usr/bin/env python3
"""Compose the kick bottleneck's decision table from published constants only.
Every input is page-cited; no flight. Prints the numbers the dossier claims."""
# --- inputs, all page-cited ---------------------------------------------------
belt_kick_p50_us   = 50.4   # kick-cadence 3570, shared box, N=10^4 coast
belt_compile_us    = 4.45   # c4d3: 4.4-4.5 p50 at true belt keys
belt_read_us       = 4.0    # cd6e/6701: shipped read 2.5-9.2 flat in e (belt end ~4)
carlson_all3_us    = 2.9    # de99: all-three channels <= 2.9 us (paper-verbatim)
plane_rebind_lo, plane_rebind_hi = 62.6, 75.4   # a765 mean band
plane_compile_lo, plane_compile_hi = 52.8, 65.3 # a765: 82-87% of rebind
plane_arith_floor  = 6.0    # a765: key 2.3 + Carlson <=2.9 + tail ~1
composed_lo, composed_hi = 8.0, 19.0            # cd6e: composed closed-form kick lean-cold
req_kick_us        = 23.0   # e7ef: required kick cost to fit 10^9 rtf100
tau_carry          = 0.17   # 5ade: fired kick -17% digest-identical
apply_walk         = 0.10   # 9c67/d65c: wave CPU -9..-11% (midpoint)
live_plateau_b     = 5060   # b30b 4.85-5.06 kB/B
knot_table_b       = 43 * 88  # HANDOFF scoreboard: ~43 knots x 88 B
wall_gb            = (6.0, 8.0)  # memory-h-live / 6793's wall

# --- P2: the wiring's population split ----------------------------------------
save_lo = belt_compile_us - carlson_all3_us                 # compile-only swap
save_hi = belt_compile_us + belt_read_us - carlson_all3_us   # compile+read composed (upper)
print("P2  wiring CPU, belt/10^9      : save %.2f-%.2f us of %.1f us = %.1f-%.1f%%"
      % (save_lo, save_hi, belt_kick_p50_us, 100*save_lo/belt_kick_p50_us, 100*save_hi/belt_kick_p50_us))
cs = 100*(plane_compile_lo+plane_compile_hi)/2/((plane_rebind_lo+plane_rebind_hi)/2)
print("P2  wiring CPU, plane          : compile %.1f-%.1f us of %.1f-%.1f us rebind = %.0f%% share"
      % (plane_compile_lo, plane_compile_hi, plane_rebind_lo, plane_rebind_hi, cs))
print("P2  compile term               : %.1f-%.1f -> <=%.1f us = %.0f-%.0fx; whole rebind -> %.0f-%.0f us = %.1f-%.1fx"
      % (plane_compile_lo, plane_compile_hi, carlson_all3_us,
         plane_compile_lo/carlson_all3_us, plane_compile_hi/carlson_all3_us,
         composed_lo, composed_hi, plane_rebind_lo/composed_hi, plane_rebind_hi/composed_lo))

# --- P3: belt kick after every landed deletion --------------------------------
for save, tag in ((save_lo, 'compile-only'), (save_hi, 'compile+read')):
    k = belt_kick_p50_us * (1-tau_carry) * (1-apply_walk) - save
    print("P3  belt kick composed (%s): %.1f*%.3f*%.3f-%.2f = %.1f us vs req %.0f -> %.2fx over"
          % (tag, belt_kick_p50_us, 1-tau_carry, 1-apply_walk, save, k, req_kick_us, k/req_kick_us))

# --- P4: the knot table as the live plateau's majority (same wall both sides) --
share = knot_table_b / live_plateau_b
ratio = live_plateau_b / (live_plateau_b - knot_table_b)
print("P4  knot table %.0f B of %.0f B plateau = %.0f%%; wall per GB: %.2fM -> %.2fM live = %.2fx (6793: 3.9x)"
      % (knot_table_b, live_plateau_b, 100*share,
         1e9/live_plateau_b/1e6, 1e9/(live_plateau_b-knot_table_b)/1e6, ratio))
print("P4  wall %.0f-%.0f GB         : %.2f-%.2fM -> %.2f-%.2fM live"
      % (wall_gb[0], wall_gb[1], wall_gb[0]*1e9/live_plateau_b/1e6, wall_gb[1]*1e9/live_plateau_b/1e6,
         wall_gb[0]*1e9/(live_plateau_b-knot_table_b)/1e6, wall_gb[1]*1e9/(live_plateau_b-knot_table_b)/1e6))

print("FLOORS: plane rebind %.1f-%.1f -> %.0f-%.0f us vs %.1f us arithmetic floor; write floor 42-56 ns never binds (e7ef: at the floor even shipped cadence fits, 0.17 cores)"
      % (plane_rebind_lo, plane_rebind_hi, composed_lo, composed_hi, plane_arith_floor))
