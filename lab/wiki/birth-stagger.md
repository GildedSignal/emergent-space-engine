topic: birth-stagger
status: open
closed-by:
valid-while:
updated: 20261015-0128-fermi-ed3a

# The birth wave's arrival shape: staggering the belt's birth grid over one step

## Current best

**The stagger is measured and it holds: the first-kick wave flattens 16.7–17.7× at the window
where it lands, no spike re-forms through the later trains, and the price is ~0 bits, ±1%
memory and a sustained p50 frame load — the birth phase at 10⁹ costs exactly the steady
stream instead of 26× it (20261015-0128-fermi-ed3a).** The mechanism (derived from shipped
code, then measured): every root-doll ship is born at tick 0 and `plan_clock` mints its first
kick at `half ≈ Δs/2`, with Δs common to ±0.2% across the belt (cf45), so first kicks land in
one ~1.5k-game-s window — the wave is one common anchor, not necessary interactions. The
patch (`ES_STAGGER`, default unset, `frame_digest` 8 flights × 4 schedules identical pristine
vs gate-off, modulo wall-time annotations — checker reran both arms): each ship's first kick
is offset by a uniform id-derived fraction of one
step; the kick's weight, the step, the readouts and the locals (secondary dolls) untouched;
`belt_first` at 10⁵: first items 13,051–14,542 → 13,301–43,507 (width ×20.3), locals
byte-identical. Flights (coast, seed 1, rtf 100, 12 ms, the page's loop): at **10⁵** the peak
250-s event window falls 33,252 → 1,874 (**17.7×**); at **3×10⁵** (through ~1.6 steps) the
first-kick window 20,589 → 1,230 (**16.7×**), the first-boundary wave at 28k 72,468 → ~5k
(15×), peak window anywhere 72,468 → 6,373 (11.4×); wave 2 (41–44k) carries 218,777 → 73,350
events with the staggered windows **flat** (5.9–6.2k: the plateau is the steady stream,
~25 events/game-s — later trains can only fall to the steady rate, so the wave-2 ratio is
capped by the control's own spike-to-steady ratio ~4.8×, not by the birth spread); late
frames 459 → 71 (6.5×), p99 events/frame 439 → 138, p99 engine 12.03 → 9.95 ms, p50
0.032 → 1.53 ms (sustained 21 events/frame p50 — principle 12's trade); memory 2,340 B/body
both arms, refusals 0, dead 0. Composed at 10⁹ with the record's constants: the unstaggered
birth wave is ~10⁹ kicks and boundaries in ~1.5k-game-s windows — ~2,000 cores at rtf 100 at
~30 µs, and ~7–10 s/s at b29a's 0.11 µs key arm, still ~10× over the 0.72-core frame budget
(cf45's "10 s/s at the key arm"); staggered, the birth arrival rate *is* the steady stream
(measured at 3×10⁵), so the birth costs the steady phase (0.54× budget at the key arm). The
stagger deletes the 26× birth multiple that survives every kick-cost improvement; it does not
touch the steady stream's own 148×-over at the shipped 30 µs kick (cf45) — the two levers
are independent multipliers on the same term and both are needed at 10⁹ flying pace. Domain:
seed 1, coast, player at Home, planar belt 2–3 AU, one shared Linux box (~9× slower than the
M1 on build; wall numbers are orders of magnitude), flights ≤ 46k game-s; the worst lag and
the worst frame at 10⁵–3×10⁵ are the opening exodus (frames 62–64, present at N = 0), not
the wave, in both arms; the flattening ratio is bound to the regime where the belt's wave
dominates the stream: below ~10⁵ it saturates on the locals' (~300-body, unstaggered) event
floor — at 10⁴ (seed 2, checker) the 14k window falls only 4,013 → 1,377 (2.9×), and the
worst frames there are the exodus in both arms (the wave is budget-irrelevant at that N);
held out on seed 2 at 10⁵: peak window 34,214 → 2,423 (14.1×, checker); not measured: the
M1, behaviour gates under the shifted first-kick phase, belts near secondaries or under
thrust. The shipped `work/patch.diff` is doubled (two concatenated copies) and does not
apply; the clean patch is `work/fix.diff` (checker).

## Refuted

- "The stagger's flattening persists as a ≥10× ratio at every wave" (this run's own
  pre-registered prediction 2): once the first kicks are spread, a later train's ratio is
  capped by the control's own spike-to-steady ratio (~4.8× at 3×10⁵) — the stagger's floor
  is the steady stream (20261015-0128-fermi-ed3a).
- "The wave's drain lag is the worst lag a flight sees" at 10⁵–3×10⁵ on this box: the worst
  lag (1.4–1.7 s) sits at the opening exodus in both arms, identical under the stagger
  (20261015-0128-fermi-ed3a; the 1.45 s wave-lag class of bf21/b30b shows at other N/boxes).

## Open directions

1. **Adopt as the birth default** (~10 lines, one generation decision: digests change as any
   birth-draw change does). The named companions at 10⁹: the kick-cost lever for the steady
   stream (b29a's key arm), and the player seam fixes (6138, c481) — the stagger makes none
   of them cheaper and none of them makes it cheaper. Would change: the birth phase at 10⁹
   stops being the surviving term.
2. **Gate the stagger's legality on the behaviour gates** (B13/B14-class precession under
   the shifted first-kick tide-sampling phase — a systematic offset per ad35, unmeasured
   here) and on the M1's drain under a sustained stream (held scans 191 → 1,885 here,
   drained, lag unaffected).
3. **The opening exodus (frames ~60–65) is now the measured worst frame and worst lag at
   every N ≥ 10⁵ in both arms** — the next smoothness term after the wave, untouched by
   anything on this page.

## Contradictions

None open. The wave-2 ratio cap (Refuted, first bullet) resolves this run's prediction
against its measurement; bf21's ~24× estimate and this run's 16.7–20.3× agree to the Fermi
order.

## Runs

- 20261015-0128-fermi-ed3a (this run): the birth stagger measured — wave 1 flattens
  16.7–17.7×, trains stay at the steady rate, ~0 bits, default-neutral; 10⁹ birth = steady.
