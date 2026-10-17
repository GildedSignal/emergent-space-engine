topic: birth-stagger
status: open
closed-by:
valid-while:
updated: 20261017-1829-taleb-75d6

# The birth wave's arrival shape: staggering the belt's birth grid over one step

## Current best

**The legality gate is measured and ed3a's patch shape is killed on error class: the stagger as built
(a root-doll ship's first kick offset by a uniform id-derived fraction of one step, weight and interval
unchanged) leaves every quiet-belt body with a one-time element error 14–23× the shipped cadence's own
per-orbit band against the ref8 ladder — median |Δln a| 4.0×10⁻⁷ staggered against 1.7×10⁻⁸ at one belt
orbit; |Δe| 3.1×10⁻⁷ against 2.2×10⁻⁸ — unbiased (|z| ≤ 1.05, 128 bodies, both seeds), non-compounding
(per-body growth slope 0.35 vs shipped 0.41; the on−off differential flat, ratio 1.13, one → two orbits),
one marginal apsidal tail (a single body 3.8×10⁻⁴ at two orbits against a 1.7×10⁻⁴ line) — a bounded
one-time offset, not a growing tide-sampling drift
(20261017-1829-taleb-75d6, taleb; lean scene star + three planets + 128 ladder belt ships, settled to
1–2 belt orbits, exact-integer key readouts, controls: birth keys and planets bit-identical across arms,
patched-gate-off digest-identical to pristine on frame_digest's 9 flights × 4 schedules; criteria
pre-registered in predictions.md before the runs).** The cure's idea survives its first hour: the
symmetric variant — start the whole clock at `t + off` (first kick at `off + half`, first interval
[off, off + Δs) symmetric, the tube free until then) — keeps the wave spread and never creates the
asymmetry; that arm, not ed3a's, is the one to carry to the B13/B14-class gates, unmeasured (checker:
the per-body evidence does not establish the asymmetry as the term — see below).
Scope, from the held-out seed: on a resonance-dominated draw (seed 2) both arms sit ~2×10⁻⁴ from the reference and
are equal to three digits — the shipped cadence's own belt error under the Giant's resonances is 10⁴×
its quiet-band error (agreeing with kick-cadence's "no cadence certifies near commensurability"), so
this kill is measured on the quiet belt, where the instrument resolves the stagger's term.


**Checker (75d6, same instrument + a step_log2-9 arm and a same-tick rerun): the kill's direction is
over-determined, the 23× headline is not freezable, and the mechanism is unresolved.** Two instrument
defects the author missed: (i) every arm reads at its own `t_wave_end + m·P_min`, and the stagger moves
`t_wave_end` by 5.6×10⁹ ticks (3.6×10⁻⁴ of a belt orbit) by design, so cross-arm element comparisons carry
a readout-phase artifact of the belt's short-period oscillation — the on−off median falls 3.2×10⁻⁷ →
2.1×10⁻⁷ read at one common tick; (ii) the ref8 ladder shares tick-0 anchoring with the off arm: against a
4×-finer ref9 the off band is 8.7×10⁻⁸ (not 1.7×10⁻⁸) and K2 falls 22.9× → 4.8× (ref8-vs-ref9 6.8×10⁻⁹:
the ladder converges). The ref-free same-tick differential 2.1×10⁻⁷ still sits ~5–10× above any defensible
shipped band (ad35's law: 3×10⁻⁸), so the configuration kill stands. The per-body attribution to the
asymmetric first step fails its own predicted monotone test (Spearman ρ = 0.23; bodies with offset < 5% of
Δs and off-arm error ~10⁻⁹ pay the full 2–6×10⁻⁷ differential), so the symmetric variant is a hypothesis
to measure, not a held result. Checker's held-out seed 3 fires 86–200× on the same instrument — direction
confirmed, magnitude instrument-bound.

*[Prior best retained below.]*

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

**The exodus holds under burn** (the composition this page left open; 20261016-1319, print-only
`exodus_burn.rs`, pre-registered): a held level-8 forward burn through the opening changes no
outcome — leaver totals identical to coast (43/43 at 48, 361/361 at 400), per-leaver 555-637 us,
lag capped at one frame everywhere, at 12 ms and the served 5 ms — but it makes the player's own
thrust cadence the opening's dominant cost at the served 48-member fleet: 126.6 ms over f0-100,
4.8x the whole hand-out bill (at the 400-member cap the hand-outs still own the opening, 207 vs
130 ms, same order), every flush paying the same `bind_surface` fit a hand-out pays (~430 us/flush
by the prof call counter — ~290 extra fits carry the bill, the price of one hand-out bind;
checker), and it freezes the scan latch through the drain (plateau ~145 held scans at 5 ms —
69f3's latch inside the opening; encounters delayed, never lost, far under the 2048 cap; the 5-ms
plateau is the held cadence's steady state, not a drain-only artifact — it creeps to ~247 by f300
at N=0, checker2). The term is monotone in level, not proportional (2.7/28.5/72.4/132.6 ms at
L1/L4/L6/L8 at 48 — checker; steeper than linear below L6, flattening near L8's cadence cap;
checker2 at L12: 421 ms, hs 635, lag still capped) and at L4 invisible against the hand-out bill.
Checker2 held-out arms: seed 7 totals identical (348/348, cap and price invariant); belt 1e4 at
5 ms totals identical by f500 (43/43) with the wave stretched (11 of 43 by f100) and the latch
plateau ~3x the N=0 one. It sits on the same promotion lever — no new smoothness term, no new lever.

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
is offset by a uniform id-derived fraction of one step; the kick's weight, the step, the
readouts and the locals (secondary dolls) untouched; `belt_first` at 1e5: first items
13,051-14,542 -> 13,301-43,507 (width x20.3), locals byte-identical. Flights (coast, seed 1,
rtf 100, 12 ms, the page's loop): at **1e5** the peak 250-s event window falls 33,252 ->
1,874 (**17.7x**); at **3x1e5** (through ~1.6 steps) the first-kick window 20,589 -> 1,230
(**16.7x**), the first-boundary wave at 28k 72,468 -> ~5k (15x), peak window anywhere
72,468 -> 6,373 (11.4x); wave 2 (41-44k) carries 218,777 -> 73,350 events with the staggered
windows **flat** (5.9-6.2k: the plateau is the steady stream, ~25 events/game-s — later
trains can only fall to the steady rate, so the wave-2 ratio is capped by the control's own
spike-to-steady ratio ~4.8x, not by the birth spread); late frames 459 -> 71 (6.5x), p99
events/frame 439 -> 138, p99 engine 12.03 -> 9.95 ms, p50 0.032 -> 1.53 ms (sustained 21
events/frame p50 — principle 12's trade); memory 2,340 B/body both arms, refusals 0, dead 0.
Composed at 1e9 with the record's constants: the unstaggered birth wave is ~1e9 kicks and
boundaries in ~1.5k-game-s windows — ~2,000 cores at rtf 100 at ~30 us, and ~7-10 s/s at
b29a's 0.11 us key arm, still ~10x over the 0.72-core frame budget (cf45's "10 s/s at the key
arm"); staggered, the birth arrival rate *is* the steady stream (measured at 3x1e5), so the
birth costs the steady phase (0.54x budget at the key arm). The stagger deletes the 26x birth
multiple that survives every kick-cost improvement; it does not touch the steady stream's own
148x-over at the shipped 30 us kick (cf45) — the two levers are independent multipliers on the
same term and both are needed at 1e9 flying pace. Domain: seed 1, coast, player at Home,
planar belt 2-3 AU, one shared Linux box (~9x slower than the M1 on build; wall numbers are
orders of magnitude), flights <= 46k game-s; the worst lag and the worst frame at 1e5-3x1e5
are the opening exodus (frames 62-64, present at N = 0, now attributed above), not the wave,
in both arms; the flattening ratio is bound to the regime where the belt's wave dominates the
stream: below ~1e5 it saturates on the locals' (~300-body, unstaggered) event floor — at 1e4
(seed 2, checker) the 14k window falls only 4,013 -> 1,377 (2.9x), and the worst frames there
are the exodus in both arms (the wave is budget-irrelevant at that N); held out on seed 2 at
1e5: peak window 34,214 -> 2,423 (14.1x, checker); not measured: the M1, behaviour gates under
the shifted first-kick phase **[now measured on the elements: see the current best above]**,
belts near secondaries or under thrust. The shipped `work/patch.diff` is doubled (two
concatenated copies) and does not apply; the clean patch is `work/fix.diff` (checker).

## Refuted

- **"A pure time shift cannot change the error class, so the stagger needs no element-level gate"
  (this page's own direction 2, left unmeasured since ed3a): the shift moves the kick's time
  without moving its Strang interval, and the staggered arm sits 5–23× the shipped cadence's per-orbit
  error band above the shipped arm on the quiet belt (4.8× against a 4×-finer ladder, 14–23× against ref8 — checker; 20261017-1829-taleb-75d6).**
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

1. **Adopt the SYMMETRIC stagger, not ed3a's** (the successor the kill names): start the whole
   clock at `t + off` — first kick at `off + half`, first interval [off, off + Δs) symmetric,
   the tube drifting free until then — one line in `plan_clock`; the wave spread survives
   (ed3a's measurement stands: the spread is a property of the offset, not the asymmetry) and
   the asymmetric first step never exists. Judge it with 75d6's instrument and criteria
   (predictions.md's K1–K4 are reusable verbatim), then the B13/B14-class gates. The
   mechanism check the next run should add: correlate per-body error with the id-derived
   offset (75d6's CSVs carry `first_kick` per body; the asymmetric-first-step reading
   predicts monotone growth in the offset's distance from the interval's centre).
   **— done by 75d6's checker: it fails** (ρ = 0.23; near-zero-offset bodies pay the full
   differential), so measure the symmetric arm, do not assume it, and read every arm at one common
   absolute tick: the stagger moves `t_wave_end`, which sets each arm's readout tick, and the shipped
   mismatches carry a ~10⁻⁷ readout-phase artifact.
2. **Gate any surviving stagger's legality on the behaviour gates** (B13/B14-class precession)
   and on the M1's drain under a sustained stream (held scans 191 -> 1,885 at ed3a's box,
   drained, lag unaffected). The element-level class gate (direction 2 as written) is now
   measured and kills ed3a's shape on the quiet belt; a resonant draw hides the term
   entirely (seed 2: both arms 2×10⁻⁴ from the reference, equal to three digits — the shipped
   cadence's own resonance error, 10⁴× its quiet band, dominates; kick-cadence's page owns
   that regime), so a frozen gate must sample both regimes.
3. ~~The opening exodus~~ **Closed, attributed** (20261016-1207-taleb-f094): the fleet's own
   birth; the lever is the promotion price (b29a/e0f9/760f) or a scenario change (birth the
   scene's members as doll ships), not scheduling. ~~Open residue: the opening under burn~~
   **Closed** (20261016-1319): the burn composes at the page's fleets (the bound is real, see
   the 2000-member line above), the cadence bill joins the same lever. Residue: levels above
   L8 (the burst job's, gate T1), belt-N burn arms, fleet-2000-class arms at 12 ms, a
   keys-changing player inside the drain, and a possible second wave beyond ~5,000 game-s.

## Contradictions

None open. 75d6's kill and ed3a's wave measurement compose (the spread and the asymmetry are
separate properties of the same patch); the quiet-belt scope of the kill and seed 2's
resonance drowning are different regimes, each measured (cf. kick-cadence's commensurability
law), not in conflict.

## Runs
- 20261015-0128-fermi-ed3a (this run): the birth stagger measured — wave 1 flattens
- 20261016-1207-taleb-f094 (this run, awaiting grade): the exodus attributed — the fleet's
- 20261016-1319-second-20261016-1207-taleb-f094-8a40 (this run, awaiting grade): the exodus
- 20261017-1829-taleb-75d6 (this run, silver asked): the legality gate measured — ed3a's patch shape killed on error class (15-23×, one-time, unbiased); the symmetric clock start named as the adoptable arm.
