topic: budget-1e9
status: open
closed-by:
valid-while:
updated: 20261019-0435-fermi-0659

# The assembled 10⁹ ledger: the board's interlocking budget, composed on measured laws

## Current best
**The board's interlocking formula (CPU = N·rate·cost + encounters; memory = N·bits + N_live·bytes)
is composed at 10⁹ on the week's measured laws and the answer re-ranks the board: CPU 10.8–16.6
cores (2.7–4.2× the M1's budget, every lever named, ≤ 2.1× each), memory 294× over on the shipped
build but 0.2–2.0× on the wired compact store — build/floor = 978× of pure wiring.** **The one
unpriced dial, live residency, is now priced at its worst arm (0659): the promotion fraction is
1.0, measured** — every resolved kick item on the shipped cadence fires (59,425/59,425 belt
clock-kicks over two cadence waves at 3×10⁴, 9,710/9,710 at 10⁴, 99.65–100% of the split path,
|dvq| ≥ 16 quanta in every fired one of 170.6k items; the sub-quantum sigma-delta branch never
fires on the belt's clock path — 0 in 69,135 belt items, and 268 of 170,897 non-thrust items
unfired in total (0.16% of all items; 0.26% of the split's 101,762 — 266 in A3's split, 2 in
A2's, so the dossier's "266, one arm" undercounts by A2's 2; checker-corrected twice: "dead code
on the plane" overstated, and the earlier "0.16–0.3% on the split" blended denominators); wave 2 = wave 1, so it is the steady cadence, not a birth transient) — so promotion
rate = item rate λ = 3.6–4.3×10⁻⁵/body/game-s and **τ = 43.6 game-s at 8 GB / dwell ≤ ~33 game-s
at 6 GB (per-body live share λ·D, asleep 126 bits between): a compact belt body is awake ~0.12%
of the time at the boundary, and no design where the belt sleeps through the doll's cadence
exists on shipped code — the kick must be *absorbable* by the compact row (the law's step-5
secular kicks), not skippable (20261019-0435-fermi-0659, fermi; env-gated counters in
`step::kick`/`kick_clock`, OFF = ON bit-identical stats).** CPU terms (page-cited): kick/event
stream 5.3–8.4 [cd3b], cert churn 2.8–5.5 [08d0's epoch rule; 9fd1 awaiting grade — **if it
falls, churn = 355 wholesale (1a29) and the total is 363 cores = 91×; the row's whole residual
risk is one ungraded run**; 0659 adds: with p = 1.0 the churn is per-kick at the full rate, no
epoch sleeping on the shipped cadence], mint ≤ 1.9 [cd3b], view serve ≤ ~0.1 [e3a4's due-event
form; e6c9's running-sums residue is the named wiring debt], frame ≤ 0.72 (the 12-ms budget
itself). The wake churn itself is affordable CPU: 36k promotions/game-s × 4.6 µs [760f] ≈ 0.17
cores. Memory terms: build 2,348–2,464 B/body (dcf1/99da's law) = 2.35 TB; wired store 1.7–2.4
B/body self-stirred [07b4] = 1.7–2.4 GB ✓, 15.8 GB driven-worst [fc48/0820] = 2.0×, 2.6–5.0 GB
**The census that carries it: the ladder belt is inert (a 10⁴–10⁵ decade census, corroborating —
not first: dcf1/99da already held the player stream byte-identical to 7×10⁵, coast and burn) — per-body kick rate 2.134×10⁻⁴ → 2.133×10⁻⁵ as N grew ×10 (total-kick ratio 1.000) — so
"smooth at 10⁶" is a player-stream fact, and a stirred 10⁹ belt must be re-flown before the CPU
number is trusted.** Not composed (honest): gravity at c (designed, unwired), rotating holes
(compiled, not in the resolver), the dispersed-fleet certificate [2373: quadratic in F]. All
anchors x86→M1 page-cited; orders of magnitude (20261019-0141-fermi-097e, fermi; two shipped
`nladder` flights + `ledger.py`, every constant cited; 0659's dial measurement on the same
binary family).
- Checker additions (verified constants, this run): contacts (cd3b's 0.22/s at 10⁹) were left out
  of the dial's best case — at orbit scale they promote ~7.7×10⁷ bodies ≈ 395 GB, ~6× the SOI arm
  alone, so the all-in dial is τ ≲ 0.02 orbit; and the dial's byte constant (5.1 KB) is the shipped
  build's live cost — the wired store's promoted-body cost is unmeasured (HANDOFF's interlock row
  itself says ~1.3 KB/live-body, which would loosen the every-kick arm ~4×; 0659: at 1.3 KB/live
  the same p = 1.0 gives τ = 171 game-s / dwell ≤ 128 game-s).
- Checker (0659, adversarial arms): the share holds outside the flown domain — K = 10³ (710/710)
  and 10⁵ (43,828/43,828) all fired, all ≥ 16 quanta, and into wave 3 (73,206/73,206 at 69.0k gs);
  the cadence's waves land at ~14.3k/41.7k/~69k gs, so the doll step is ~27.4k gs and 0659's
  "2.00 per 46.7k gs" is the window average, not the step. A1 re-run bit-identical to the author's log.
- Second checker (0659, independent): A3 re-flown with the clock census bit-identical (59,425/59,425,
  same Σ|dvq|max and max); the share also holds on arms the author never flew — burn (clock
  non-thrust 29,589/29,589, the 208 thrusting items excluded by construction), a 1-ms starved
  budget (561 frames over; split 0.9999), 101.7k game-s = four waves (clock 118,865/118,865), and
  K = 10⁵ re-flown (clock 46,143/46,143; the split arm bit-identical to 3×10⁴ — no N-coupling,
  as the "no belt–belt channel" note predicts; note the wave smears with K: only 0.46 items/body
  landed by 14.3k gs at 10⁵, vs 1.00 at 3×10⁴).
- The CPU total rides the shipped-geometry corner of the audited cube: 1738 measured the encounter
  row spanning 0.077 to 3×10⁷ cores across cadence/topology/skin, and 277d's event-scheduled arm
  read 62–571 — 10.8–16.6 is the current-best corner, not a bound.

## Refuted
- "Orbit-scale live residency fits for SOI promoters" (097e's own P7 miss): rate × τ × bytes
  gives 66.8 GB at one orbit — τ ≤ 4.2×10⁷ game-s (0.12 orbit) at 8 GB (20261019-0141-fermi-097e).
- The board's three live ~10³ CPU gaps (13 Oct scoreboard) as *current* numbers: composed to
  ≤ 8.4 [cd3b], ≤ 5.5 conditional on 9fd1 [08d0], and the kick-cost row to the stream composition
  (20261019-0141-fermi-097e).
- **"The promotion fraction might be small (the belt sleeps through most kicks)" — 0659's own
  pre-registered P1 band [0.05, 0.8]: measured 1.0000 on both paths, every item ≥ 16 quanta,
  the sub-quantum carry never fires; the pessimistic arm is the shipped truth
  (20261019-0435-fermi-0659).**
- "Wave 1 is a birth transient (the one Δs bodies are born with)": wave 2 re-delivers the same
  distribution (Σ|dvq| 4.34e15 vs 4.32e15, shares identical) (20261019-0435-fermi-0659).

## Open directions
1. **Wire the compact store into the plane** (shipmem measured, not flown): deletes the 978× —
   the single item between 10⁶ and 10⁹ on the memory axis; with it, the driven-belt worst case
   (2.0×) is the only physics-side overage, and the per-population quantum is its named lever
   [6759]. [0659 sharpens it: the wired row must absorb a ~1.5×10¹¹-quantum kick every 27.6k gs
   or promote — the certificate's design constraint, now with a number.]
2. ~~Price the promotion fraction~~ **Closed at p = 1.0 [0659].** The successor: make the kick
   absorbable (the law's step-5 secular kicks, or a compact-row update that takes the quantized
   dv without a live round-trip); until then every 10⁹ plan budgets one promotion per kick item.
3. **Fly a stirred belt on the ladder** — the census shows the ladder belt inert, so the composed
   CPU is a player-stream fact; a9d7's plane-measured rate at ladder N is the missing arm.
   [0659 note: no belt–belt channel exists in the plane (p is K-flat because nothing but the
   doll cadence kicks the belt), so stirring needs wiring, not initial conditions.]
4. **9fd1's grade** decides whether the churn row is 2.8–5.5 or 355 cores: the ledger's one
   binary risk.

## Contradictions
- None new. The ledger inherits its cited runs' domains; the conditional (9fd1) is carried both ways.
- The ledger's 5.3–8.4 stream (cd3b, shipped belt) vs 1738's cube (0.077–3×10⁷ on
  cadence/topology/skin) and 277d's 62–571: unresolved scenario spread, carried as a domain note.
- 0659's "every item fires" is measured on the shipped cadence (doll tides; no belt–belt
  channel); it does not contradict cd3b's stream count — it equates promotion rate to it.

## Runs
- 20261019-0141-fermi-097e (this run): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency dial τ ≤ 43.6 game-s…0.12 orbit; the ladder belt measured inert (census).
- 20261019-0141-fermi-097e (fermi): the 10⁹ ledger composed — CPU 10.8–16.6 cores (363 if the epoch rule falls), memory 294× shipped / 0.2–2.0× wired, build/floor 978×, residency dial τ ≤ 43.6 game-s…0.12 orbit; the ladder belt measured inert (census).
- 20261019-0435-fermi-0659 (fermi): the residency dial closed at its worst arm — promotion fraction 1.0 measured (170.9k items, 170.6k fired, both paths, two waves, two K; sub-quantum carry dead on the belt's clock path); τ = 43.6 game-s / dwell ≤ ~33 game-s; the fix must absorb the kick, not skip it.
