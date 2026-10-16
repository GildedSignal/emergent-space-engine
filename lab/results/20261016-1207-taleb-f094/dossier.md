# The opening exodus is the fleet's own birth: ~0.6 ms per member, one-time, N-flat

## Claim

The "opening exodus" — the measured worst frame and worst lag of every flight at every belt
N (birth-stagger's open direction 3, ed3a) — is the player's fleet being born: ~90% of the
battle scene's members cross out of Home's Fermi frame in the first ~100 game-s, and every
crossing pays one sticky promotion (a `resolve_handout`: `bind_surface` + first plan, **485-686 us
per leaver, 70-73% of it the exact tube fit**). The bill is one-time (0 leavers after frame
100), **identical from belt N = 0 to N = 1e5** (same 43 leavers, same frame, same lag), and
proportional to the fleet (~0.55 ms/member): 26 ms at the served 48 members, 240 ms and a
~1.5-s rtf slump at the page's 400-member cap, ~0.9 s of one-time work at 3cfc's 1,600
members — which attributes 3cfc's "one exodus item 0.6-1.5 s" to this wave. The budget
already caps the harm at one presented frame of lag (never more than 1.667 game-s in any
arm): the player sees an rtf dip, not a freeze — until the fleet is large enough that a
single battle slice overruns the frame (17.0 ms at 1,600 members). The lever is the
promotion price b29a/e0f9/760f already own, not the scheduler; or birthing the scene's
members as doll ships directly (a scenario decision).

## Bottleneck

Board line 1 ("bodies in the flyable engine: which term breaks first as the plane grows...
and the smallest promotion between a compact body and a live one"). This closes the
unattributed worst-frame term: it does **not** grow with N, so post-stagger the plane's
opening is bounded by the player's own fleet, and no smoothness work at 1e6 needs to touch
it. Gain: deletes "the opening exodus" as an open smoothness term (one named direction on
the birth-stagger page dies), and corrects ed3a's reading of the 1.4-1.7 s "worst lag":
that number is the one-frame present cap, not accumulating lag.

## Evidence

All numbers from `crates/universe/examples/exodus_attr.rs` (this run's print-only
instrument: per-frame wall ms, resolved events, `Stats` deltas and — behind `--features
prof` — the hand-out stage split; no engine line touched, outcomes unchanged by
construction). Commands: see `regen.sh` (full grid re-runs in < 2 min). Box: the lab's
shared Linux x86 (cloud timings are orders of magnitude; the M1 re-measures).

**Attribution (seed 1, rtf 100, 60 Hz, 12-ms budget, fleet 48, belt N = 0).** The worst
frame is f62: 11.1-11.9 ms, 31-32 events, presented lag 1.448 game-s, of which **25-26 are
`opens` and 25-26 `leavers`** (equal at every tooth: f9/f10 = 2+7, f62/f63 = 25-26 + 5-6);
11.3-11.7 ms of it in the fleet class. Whole opening: 43 leavers, 31.8 ms fleet-class on
leaver frames => **~600 us/leaver**. Prof split (same flight, `--features prof`):
hand-out 26.2-28.6 ms / 43 = 609-665 us = bind 70-73% + replan 24-27% + planets/moon pull
~0.1%. The battle's own advance (the lattice slices) is 4.1-4.6 ms over the same 100 frames
— an order below its hand-outs. Files: `out/fleet48-n0-f100.txt`,
`out/fleet48-n10000-f100.txt`, `out/fleet48-n100000-f100.txt`.

**N-flatness (prediction 2, held exactly).** Belt N in {0, 1e4, 1e5}: identical — 43
leavers, worst frame f62 (11.1/11.8 ms), worst lag 1.448 game-s, per-leaver 597-600 us (the
belt's first-kick wave at ~750 game-s is outside the 100-frame window; the f62 frame at
1e5 carries 53-54 events, still budget-capped). The fleet is built before the ladder's
`extra` bodies from separate RNG streams — structural, not lucky.

**Boundedness (prediction 4, held).** Frames 100-400 at N = 1e4: **0 leavers**, worst frame
after f100 is 6.8 ms (the belt/locals' own). One wave, then quiet; a restart (`restarted()`
builds a new universe) pays it again by construction.

**Fleet scaling (prediction 1, held on the count, missed on one magnitude).** Fleet
{48, 200, 400, 1600}, N = 0, 12 ms: leavers 43 / 168 / 357 / 298-by-f100 (still draining),
i.e. **~0.9 members leave per member**; fleet-class work on leaver frames 31.8 / 113.8 /
239.9 / 344.3 ms (slope 663 us/leaver); worst frame 11.6 / 11.8 / 12.0 (budget-capped) /
**17.0 ms at 1,600 (over budget: a single battle slice of a ~1,300-member frame)**; worst
presented lag 1.448 / 1.502 / 1.667 / 1.667 game-s — **never more than one frame's advance**
(the budget caps the harm at an rtf dip). Composed: 1,600 x 0.9 x 0.6 ms = 0.86 s of
one-time hand-out work — 3cfc's "one exodus item 0.6-1.5 s" is this wave, attributed. My
pre-registered "60-150 ms at 400" was 1.6x low (measured 240 ms): a miss, reported.

**Served budget (5 ms, the page's `ENGINE_BUDGET_MS`).** Fleet 48: worst frame 4.7-4.8 ms —
inside a 60-Hz frame, 4-6 drain frames (>= 2.5 ms): invisible as a hitch on this box. Fleet
400: **82-87 of 120 frames >= 2.5 ms, worst 5.2-6.2 ms** — a ~1.5-s opening at the budget
cap (an rtf slump to about half), no dropped frame. Belt N = 1e5, fleet 48: 15 drain
frames, worst 4.7-4.8 ms.

**Held-out seeds (2, 7; not in predictions.md, reported as extra).** Fleet 48: 42 leavers
both; fleet 400: 357 / 348; worst frames 7.8-12.1 ms, all inside the opening window (f12-
f67); `opens = leavers` exactly everywhere.

**Instrument honesty.** The budget is wall-time, so the per-frame hand-out split at the
drain boundary moves 1-2 items with box load (two back-to-back runs compared bit-identical
once and differed at the boundary once; `regen.sh` prints the check); the leaver totals
(43, or 42 on held-out seeds; 348-357 at fleet 400), the opening window, the worst-frame
tick and the lag cap are stable across every run and seed. Per-frame counts are
schedule-dependent, totals stable — the known canon rule (digests are taken at cuts, 40c0).

## Predictions

`predictions.md` was written before the scaling runs (the N=0 attribution was exploratory).
Held: N-flatness (exactly), opens = leavers, ~0.9 leavers/member, bounded one-time wave,
per-leaver 300-600 us (measured 485-686 — at/just over the top at small fleets). Missed:
the unbudgeted 400-member bill (predicted 60-150 ms, measured ~240 ms). Pre-registered kill
criterion (worst frame not the hand-out wave, or leavers growing with belt N) never fired.

## What would make it wrong

- **A second wave in long flights**: I flew to frame 400 (~670 game-s); a 46k-game-s flight
  could re-clump the battle and re-exodus (the 5 members still inside the frame at f100).
- **The M1 absolute numbers**: the box is ~2-9x slower than the M1; at M1 speeds the
  48-member opening (~26 ms here) is likely one served-budget frame — invisible. The
  400-member cap and the 1,600-member overrun are the regimes that survive.
- **A player decision inside the opening drain** competes with the hand-outs for the same
  budget (and the scan latch, 69f3, freezes below S = b/2): unmeasured here; the burn
  opening is the one composition I did not fly.
- **Adoption cost**: none demanded — no engine change proposed. The named levers: the
  promotion price (b29a's key-space arm 0.11 us / e0f9's rebuilt seam / 760f's 4.6-us
  compile — the same lever the kick's 75-160 us owns), or birthing the scene's members as
  doll ships (deletes the frame crossing itself; a scenario decision for the integrator).

## Fit with PRINCIPLES

- "the best part is no part" (17) and "Compute only surprises" (3): the exodus is the one
  moment the plane pays the full sticky price for bodies that were never going to stay in
  the frame — ~90% of the battle's members are born, promoted, and never return.
- "Errors never compound" (13) / ruin: the term is convex in the player's own fleet size
  (240 ms at the cap) but bounded, one-time and budget-capped — no ruin path at any belt N;
  the ruin-shaped case (1,600+) is off the served page.
- The budget's one-frame lag cap is the design working; the cost is the promotion price,
  not the scheduler.

## The lens (Taleb)

What this lens may have missed: the upside — a cheap-promotion hand-out would make the
exodus free *and* cut the kick path with the same lever; the Taleb instinct to fence the
worst case stops at "bounded" and under-prices that composition. Also unmeasured: the M1's
absolute rates, and the opening under burn (the player's first decision landing inside the
drain).
