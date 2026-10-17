#!/usr/bin/env python3
"""Fold this run's result into the topic page (three hunks: header, Current best, Refuted, Runs)."""
import re

P = "lab/results/20261017-0238-inversion-470f/wiki/memory-h-live.md"
s = open(P).read()

s = s.replace("updated: 20261017-0005-system-efd4", "updated: 20261017-0238-inversion-470f", 1)

best = """**The play-time FLOW is bimodal and wall-path-dependent: peak memory is not a canonical
outcome.** At 400 fleet members the same flight (same seed, args, binary, quiet machine) either
peaks at ~44 MB or grows **~11 kB of live Rust allocations per game-second to 220.9 MB / 83,768
live allocations by 20,000 game-s, frees ~78k allocations in one bulk drop, and leaves peak RSS
at 206 MB forever** (allocator retention) — 5 of 15 seed-1 coast flights took the growing path
(~33%); every other arm was flat in every run (both burn arms, seed-2 coast, the shipped
48-member plane over 40,000 game-s, the 3,000-body belt). Every shipped counter is flat
throughout (bodies, catalogue_live, bytes_per_body at a constant 5.9 kB/body, the stats ledger,
slices frozen; settle +0 kB; mapping count constant — the growth is live allocations in the
main heap, seen only by a counting GlobalAlloc). The trigger is the wall-budget path, not the
game state. d3fe's clean ruin rate is otherwise dead on main: fleets dissolve by ~3,000 game-s
at every size flown, the fleet-slice bill is one-time (events 17.6→~2/gs at dissolution), and
the long-lived-battle case is unreachable by growing the fleet
(20261017-0238-inversion-470f, inversion; probe `ruin_probe.rs`, the player's own loop unpaced
at rtf 100, seeds 1–3, the bench's burn script as an arm; not an 8 GB ruin at this scene — a
4.7× path-dependent multiplier on any single-run memory-wall measurement, counter-invisible
until fenced). What reopens the clean refutation: a checker whose fresh runs never grow.

"""
anchor = "**The standing catalogue is a cache pretending to be state"
assert anchor in s
s = s.replace(anchor, best + anchor, 1)

claim = """A reachable ruin state remains: peak RSS grows ~0.2 kB per surviving member per
game-second through any battle that stays live, and both instruments were blind to
it (20261006-0030-taleb-d3fe, silver)."""
repl = """A reachable ruin state was claimed: peak RSS grows ~0.2 kB per surviving member per
game-second through any battle that stays live, and both instruments were blind to
it (20261006-0030-taleb-d3fe, silver) [re-measured 20261017-0238-inversion-470f: the rate as
stated is dead at shipped size, but a stochastic wall-path-dependent growth of the same kind
survives at 400 members — see Current best]."""
assert claim in s
s = s.replace(claim, repl, 1)

ref = """- "A reachable ruin state: peak RSS grows ~0.2 kB per surviving member per game-second
  through any battle that stays live" (d3fe, silver): at shipped size (48 members) and on the
  belt plane, dead on main at 4–7× the flown horizon — fleets dissolve by ~3,000 game-s, the
  slice bill is one-time, RSS +0.001 kB/gs over 40,000 game-s in every flat run. NOT refuted as
  a class: 5-of-15 runs at 400 members grow ~11 kB/gs of live allocations to a 221 MB peak
  (bulk-freed at 20,000 gs, peak RSS retained) with every shipped counter flat, trigger
  wall-path, un-isolated (20261017-0238-inversion-470f).

"""
marker = '## Refuted\n\n'
assert marker in s
s = s.replace(marker, marker + ref, 1)

runs = "- 20261017-0238-inversion-470f (this run): peak memory is wall-path-dependent, not canonical: 5-of-15 flights at 400 members grow ~11 kB/gs of live allocs to a 221 MB peak (bulk-freed at 20,000 gs, RSS retained) with every shipped counter flat; shipped size and belt flat; fleets dissolve by ~3,000 gs; slices one-time.\n"
s = s.rstrip("\n") + "\n" + runs
open(P, "w").write(s)
print("folded")
