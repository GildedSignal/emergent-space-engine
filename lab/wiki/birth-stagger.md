topic: birth-stagger
status: open
closed-by:
valid-while:
updated: 20261016-1207-taleb-f094

# The birth wave's arrival shape: staggering the belt's birth grid over one step

## Current best

**The exodus is attributed and it is not a birth-wave term at all: the worst frame and worst
lag of every flight at every belt N is the player's own fleet being born — ~90% of the
battle scene's members cross out of Home's Fermi frame in the first ~100 game-s and each
crossing pays one sticky promotion (`resolve_handout`: `bind_surface` 70-73% + first plan
24-27%, **485-686 us a leaver**), a one-time, **N-flat** (identical 43 leavers, same f62,
same 1.448-game-s lag at belt N = 0, 1e4 and 1e5), fleet-proportional bill (~0.55 ms a
member: 26 ms at the served 48 members, 240 ms and a ~1.5-s rtf slump at the 400-member
page cap, ~0.9 s at 3cfc's 1,600 — attributing frame-cost's "one exodus item 0.6-1.5 s"),
and the budget caps the harm at one presented frame of lag (never more than 1.667 game-s in
any arm), so the player sees an rtf dip, not a freeze, until a single battle slice overruns
the frame (17.0 ms at 1,600 members) (20261016-1207-taleb-f094, print-only instrument
`exodus_attr.rs`, no engine line touched; seeds 1 + held-out 2/7). Checker2's boundary: the
cap is one tick and scales with rtf (16.667 game-s at rtf 1000); the 0.9-leaver/member
asymptote is pinned only at ≤ 400 members — at 4,800 the drain holds 0.64/member by f700 on
a long tail (so the 1,600 composition is an extrapolation, inside 3cfc's band either way) —
and above ~1,600 the worst frames are single battle slices mid-drain (42-50 ms at 4,800),
not hand-out frames; the cap and the per-leaver price (~0.5 ms) hold throughout.**
Consequence: this
page's direction 3 is closed — the exodus grows with the player's fleet, never with the
universe, so no smoothness work at 1e6 needs to touch it; the lever is the promotion price
b29a/e0f9/760f already own (the same `bind_surface` the kick path pays), or birthing the
scene's members as doll ships directly (a scenario decision). ed3a's "worst lag 1.4-1.7 s"
is the one-frame present cap, not accumulating lag. The leaver wave is bounded (0 leavers
after frame 100 at N = 1e4); a restart pays it again by construction (checkers: flown to
f1500 and f3000 at N = 0 — the tail past the wave is a 5-member trickle at f1190, 48/48
total leavers, worst late frame 3.6 ms: bounded, no second wave through ~5,000 game-s).

**The stagger is measured and it holds: the first-kick wave flattens 16.7-17.7x at the window
where it lands, no spike re-forms through the later trains, and the price is ~0 bits, ±1%
memory and a sustained p50 frame load — the birth phase at 1e9 costs exactly the steady
stream instead of 26x it (20261015-0128-fermi-ed3a).** The mechanism (derived from shipped
code, then measured): every root-doll ship is born at tick 0 and `plan_clock` mints its first
kick at `half ≈ Δs/2`, with Δs common to ±0.2% across the belt (cf45), so first kicks land in
one ~1.5k-game-s window — the wave is one common anchor, not necessary interactions. The
patch (`ES_STAGGER`, default unset, `frame_digest` 8 flights x 4 schedules identical pristine
vs gate-off, modulo wall-time annotations — checker reran both arms): each ship's first kick
is offset by a uniform id-derived fraction of one
step; the kick's weight, the step, the readouts and the locals (secondary dolls) untouched;
`belt_first` at 1e5: first items 13,051-14,542 -> 13,301-43,507 (width x20.3), locals
byte-identical. Flights (coast, seed 1, rtf 100, 12 ms, the page's loop): at **1e5** the peak
250-s event window falls 33,252 -> 1,874 (**17.7x**); at **3x1e5** (through ~1.6 steps) the
first-kick window 20,589 -> 1,230 (**16.7x**), the first-boundary wave at 28k 72,468 -> ~5k
(15x), peak window anywhere 72,468 -> 6,373 (11.4x); wave 2 (41-44k) carries 218,777 -> 73,350
events with the staggered windows **flat** (5.9-6.2k: the plateau is the steady stream,
~25 events/game-s — later trains can only fall to the steady rate, so the wave-2 ratio is
capped by the control's own spike-to-steady ratio ~4.8x, not by the birth spread); late
frames 459 -> 71 (6.5x), p99 events/frame 439 -> 138, p99 engine 12.03 -> 9.95 ms, p50
0.032 -> 1.53 ms (sustained 21 events/frame p50 — principle 12's trade); memory 2,340 B/body
both arms, refusals 0, dead 0. Composed at 1e9 with the record's constants: the unstaggered
birth wave is ~1e9 kicks and boundaries in ~1.5k-game-s windows — ~2,000 cores at rtf 100 at
~30 us, and ~7-10 s/s at b29a's 0.11 us key arm, still ~10x over the 0.72-core frame budget
(cf45's "10 s/s at the key arm"); staggered, the birth arrival rate *is* the steady stream
(measured at 3x1e5), so the birth costs the steady phase (0.54x budget at the key arm). The
stagger deletes the 26x birth multiple that survives every kick-cost improvement; it does not
touch the steady stream's own 148x-over at the shipped 30 us kick (cf45) — the two levers
are independent multipliers on the same term and both are needed at 1e9 flying pace. Domain:
seed 1, coast, player at Home, planar belt 2-3 AU, one shared Linux box (~9x slower than the
M1 on build; wall numbers are orders of magnitude), flights <= 46k game-s; the worst lag and
the worst frame at 1e5-3x1e5 are the opening exodus (frames 62-64, present at N = 0, now
attributed above), not the wave, in both arms; the flattening ratio is bound to the regime
where the belt's wave dominates the stream: below ~1e5 it saturates on the locals' (~300-body,
unstaggered) event floor — at 1e4 (seed 2, checker) the 14k window falls only 4,013 -> 1,377
(2.9x), and the worst frames there are the exodus in both arms (the wave is budget-irrelevant
at that N); held out on seed 2 at 1e5: peak window 34,214 -> 2,423 (14.1x, checker); not
measured: the M1, behaviour gates under the shifted first-kick phase, belts near secondaries
or under thrust. The shipped `work/patch.diff` is doubled (two concatenated copies) and does
not apply; the clean patch is `work/fix.diff` (checker).

## Refuted

- "The opening exodus is an unexplained smoothness term that might grow with the plane"
  (this page's own direction 3): it is the fleet's opening hand-out wave, N-flat from 0 to
  1e5, bounded (one wave), and owned by the promotion price — no belt-scale smoothness term
  hides in it (20261016-1207-taleb-f094).
- "The stagger's flattening persists as a >=10x ratio at every wave" (ed3a's own
  pre-registered prediction 2): once the first kicks are spread, a later train's ratio is
  capped by the control's own spike-to-steady ratio (~4.8x at 3x1e5) — the stagger's floor
  is the steady stream (20261015-0128-fermi-ed3a).
- "The wave's drain lag is the worst lag a flight sees" at 1e5-3x1e5 on this box: the worst
  lag (the exodus's, 1.448-1.667 game-s) sits at the opening in both arms, identical under
  the stagger (20261015-0128-fermi-ed3a; 20261016-1207: that lag is the one-frame present
  cap, not accumulating drain).

## Open directions

1. **Adopt as the birth default** (~10 lines, one generation decision: digests change as any
   birth-draw change does). The named companions at 1e9: the kick-cost lever for the steady
   stream (b29a's key arm), and the player seam fixes (6138, c481) — the stagger makes none
   of them cheaper and none of them makes it cheaper. Would change: the birth phase at 1e9
   stops being the surviving term.
2. **Gate the stagger's legality on the behaviour gates** (B13/B14-class precession under
   the shifted first-kick tide-sampling phase — a systematic offset per ad35, unmeasured
   here) and on the M1's drain under a sustained stream (held scans 191 -> 1,885 here,
   drained, lag unaffected).
3. ~~The opening exodus~~ **Closed, attributed** (20261016-1207-taleb-f094): the fleet's own
   birth; the lever is the promotion price (b29a/e0f9/760f) or a scenario change (birth the
   scene's members as doll ships), not scheduling. Open residue: the opening under burn (a
   player decision inside the drain competes for the same budget, and the scan latch freezes
   below S = b/2), and a possible second wave in 46k-game-s flights (the author flew to
   frame 400; checkers to f1500 and f3000: only a 5-member trickle — a true second wave
   beyond ~5,000 game-s stays open).

## Contradictions

None open. The wave-2 ratio cap (Refuted, first bullet) resolves ed3a's prediction
against its measurement; bf21's ~24x estimate and ed3a's 16.7-20.3x agree to the Fermi
order. The exodus attribution composes with ed3a's reading (the exodus was present in both
stagger arms because the stagger touches root-doll ships only, never the fleet's hand-outs).

## Runs
- 20261015-0128-fermi-ed3a (this run): the birth stagger measured — wave 1 flattens
- 20261016-1207-taleb-f094 (this run, awaiting grade): the exodus attributed — the fleet's
