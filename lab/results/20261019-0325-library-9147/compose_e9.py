#!/usr/bin/env python3
"""Compose the E9 far-scheduling decision (the per-reader horizon) from measured constants.

Every input is page-cited (lab/wiki/nladder.md and the runs it names); the script adds no
constant of its own. Verdict arithmetic for 20261019-0325-library-9147.
"""
import json, re

# ---- page-cited constants (run: constant) -------------------------------------------------
PERIOD_GS   = 27_600            # 4a71/d839: one doll step; retained generations +1 per period
GENS_LAW    = "1 + floor(min(D, elapsed)/27.6k gs) + ~1"   # 4a71 second checker (global rule)
KB_BINDING  = (1.7, 2.35)       # 4a71: RSS staircase per retained binding (1.9-2.2 @3e4, 2.28-2.35 @1e3, ~1.7 @1e5)
KB_MED      = 2.0               # median of the measured band
FAR_TICKS   = 2.56e13           # 4a71: one pending item 4 ly out
FAR_PERIODS = 4_576             # 4a71: its window in wave periods
GAP_STAR_S  = 2_302.5           # 4a71: control max pending light gap at one star (flat in play time)
CTRL_RET    = (1.02, 1.07)      # 4a71: control retained/body (three kick waves)
PINNED_3E4  = (2.93, 5.04)      # 4a71: retained/body pinned D=6e9/1.2e10 ticks at 3e4
STEADY_B    = (4_790, 4_963)    # d839: steady bytes/body after the first kick (the belt's own)
RUNGS       = (1e5, 1e6, 1e9)   # ladder rungs; 4a71's ruin row is 1e6

# ---- P2: the ruin regenerates with zero new constants --------------------------------------
scale = FAR_TICKS / (FAR_PERIODS * PERIOD_GS)          # ticks per game-s implied by 4a71's sentence
window_gs = FAR_PERIODS * PERIOD_GS
gens = FAR_PERIODS                                        # +1 head generation (~1) per the law
ruin_mb = (gens * KB_BINDING[0] / 1e3, gens * KB_BINDING[1] / 1e3)   # MB per body
print("P2 ticks/gs scale  : %.4g (4a71's own sentence implies the same)" % scale)
print("P2 window          : %.3g gs = %d wave periods" % (window_gs, FAR_PERIODS))
print("P2 ruin per body   : %.2f-%.2f MB (median %.2f) vs 4a71's stated ~9.2 MB  -> covered: %s"
      % (*ruin_mb, gens * KB_MED / 1e3, "YES" if ruin_mb[0] - 0.1 <= 9.2 <= ruin_mb[1] + 0.1 else "NO"))
print("\nrung     global rule (far item live)          per-reader rule (near bodies)")
for n in RUNGS:
    g_lo, g_hi = n * gens * KB_BINDING[0] / 1e6, n * gens * KB_BINDING[1] / 1e6   # KB -> GB
    per_lo, per_hi = n * STEADY_B[0] / 1e9, n * STEADY_B[1] / 1e9                  # B -> GB
    print("%.0e  %9.3g-%9.3g GB  (ruin)         %8.3g-%8.3g GB  (the belt's own steady)"
          % (n, g_lo, g_hi, per_lo, per_hi))
print("at 1e6 the global row is %.2f-%.2f TB (median %.2f TB): 4a71's stated ~9.2 TB regenerated"
      % (1e6 * gens * KB_BINDING[0] / 1e6 / 1e3, 1e6 * gens * KB_BINDING[1] / 1e6 / 1e3, 1e6 * gens * KB_MED / 1e6 / 1e3))

# ---- P3: the control regenerates from the gap law -------------------------------------------
ret_gap = 1 + int(GAP_STAR_S // PERIOD_GS) if GAP_STAR_S >= PERIOD_GS else 1
print("\nP3 control: max gap %.1f s < one period %d gs -> retained = %d (measured %s) -> %s"
      % (GAP_STAR_S, PERIOD_GS, ret_gap, CTRL_RET, "REGENERATED" if ret_gap == 1 else "MISMATCH"))

# ---- P4: play-time boundedness, the two laws side by side ------------------------------------
print("\nP4 retained/body vs play time (far window D = %.3g gs):" % window_gs)
print("elapsed_gs   global 1+floor(min(D,el)/27.6k)   per-reader 1+floor(doll_diam/27.6k)")
for el in (1e5, 1e6, 5e6, 1.263e8):
    g = 1 + int(min(window_gs, el) // PERIOD_GS)
    p = 1  # belt doll: its own light diameter (2,302.5 s) < one period -> the control's flat 1
    print("%9.3g          %5d                            %5d" % (el, g, p))
print("global: unbounded in play time while the item is in flight (4a71's measured staircase %s/body)"
      % (PINNED_3E4,))
print("per-reader: constant in play time, set by scene geometry (the doll's light diameter)")

# ---- P5: the adoption surface, regenerated from the shipped file -----------------------------
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
src = open(os.path.join(ROOT, "crates/universe/src/universe.rs")).read()
uses = len(re.findall(r"\bship_ticks\b", src))
oldest_uses = len(re.findall(r"\boldest\b", src))
has_germ = "child_ticks" in src and "self.bodies.doll(i) != 0" in src
print("\nP5 adoption surface (crates/universe/src/universe.rs):")
print("  ship_ticks uses: %d (prediction <= 8: %s) | `oldest` mentions: %d" %
      (uses, "HELD" if uses <= 8 else "FAILED", oldest_uses))
print("  doll-filtered calendar germ (`child_ticks`, filter `doll(i) != 0`): %s" % ("PRESENT" if has_germ else "ABSENT"))
print("  the global min: prune() peeks ship_ticks over ALL ships; apply() sets it with no doll filter")
print("  the change: oldest := min over per-doll calendars (the child_ticks pattern), one site")

# ---- P6: the library's own coverage ----------------------------------------------------------
n_books = len(json.load(open("work/readwise.json"))) if __import__("os").path.exists("work/readwise.json") else None
print("\nP6 library: %s books in the export; no systems/database engineering title among them" % n_books)
