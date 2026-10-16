# Predictions (written before the decisive runs)

The run's question: is the belt's first-kick wave birth synchrony (deletable by a lawful
genesis clock-begin spread scoped to the belt) or physics (the tide's own structure)?
The patch: `ES_BELT_SPREAD=1` offsets each genesis doll-0 ship's clock begin by
`hash(id) mod Δs_doll` when its own radial period is ≥ 2³ doll-grid intervals (the belt:
period ~1e8 game-s vs grid ~2.8e4). The offset persists (clock bodies chain kick to kick,
no absolute re-anchor), no kick is moved relative to the body's own birth clock, and every
other population (secondary dolls, short-period battles, the player) keeps tick 0.

Cases I have not tuned on, and what I expect there:

- **P1 (the spread reaches the belt only).** `belt_first 1e5`: ON-arm belt first items
  spread ~uniformly over one doll-grid interval (~0-28,000 game-s, p01..p99 wide);
  the locals' first-item distribution bit-identical between arms (they are secondary-doll
  bodies, outside the scope by construction).
- **P2 (the wave flattens).** `nladder 1e5 coast` flown through the wave (200 s at rtf 100;
  the wave lands at 13,051-14,534 game-s): ON-arm events/frame max collapses from the
  OFF-arm's wave peak (expected ~700-9,000 from the record: 762 at 1e5 in ladder.txt,
  922 events/8,482 at 1e4/1e5 in system-e070) to the steady-stream level (O(10-100)),
  a ≥ 10x cut, and the wave's late frames (>12 ms) go to ~0 where the OFF arm pays them.
- **P3 (the falsifier: no law change where none is allowed).** B13 armed == B13 off
  (same judged count, same worst error to the digit): the scope must not touch flyby/assist
  bodies. `ladder_digest` cases with no belt (N=100 coast through the wave? every case has
  a belt share; the control is) — the OFF arm (env unset) must be bit-identical to pristine
  main on every case (the build-level control). N=0 flights: ON == OFF bit-identical if
  the plane's own 28 bodies hold no doll-0 long-period ship; if any lands in scope that is
  a leak to report, not a tuning knob.
- **P4 (cadence intact).** kick/b/game-s equal between arms to ~1e-3 relative over the same
  flight (the spread moves kick TIMES, not counts; no stubs: clock bodies chain). Belt-bearing
  digests DIFFER between arms (a law-level phase change, reported, not hidden).
- **P5 (composition, not measurement).** With the spread, the compact store's first-wave
  promotions (the ladder's named ruin: 10^7 promotions in ~one frame interval, ~250 s of
  compiles) become a stream of 10^7/28,141.5 ≈ 356 items/game-s ≈ 3-9 ms/game-s of promotion
  work at the measured 9.2-24 µs/promotion: smooth by construction.

Kill criterion (pre-registered): if the ON arm changes B13's verdict or moves any
non-belt body's first item, the configuration is dead (c840's lesson generalises) and the
run reports the kill, not a cure.
