Grade: silver

**Abstract.** The thrust-cadence clamp (one rebind per 1/64 of |v|) pays 817–2,990 player items
per held burn for a readable state that cannot say "under thrust" — the one slot the view (7b86)
and gravity-news (7ab4) also re-derive. Measured on shipped code, the events buy neither accuracy
(end |v|/c 0.87–1.75% below the 1/1024 arm on every prograde flight) nor smoothness (paced lag
~1.6 s at any sampling; only deletion reaches 0.038 s), and deleting the clamp breaks at the
velocity word (prograde flushes refuse; envelope to 4.2e-2 c). Reproduced: regen exit 0; my
reruns bit-identical digests (f8 16 s), 6-digit end speeds (seeds 3, 7); the 32 s decade
confirms. Gain: prices a 19–204× event deletion. Cost: the carry is unbuilt, untested.

## Reasons

1. **Reproduction.** regen.sh exit 0 (runner); I applied `work/patch.diff` myself (clean, builds
   in 10 s). Deterministic quantities reproduce exactly: end |v|/c to 6 digits on every flight
   (8/16 s, seeds 1/3), refusal counts (0/1/35 and 1/1/73), coast digests identical across all
   arms (2f7697…, c1aa22…), ship≡unset equivalence digest (bd69…). Wall-dependent counts (pitems
   under the 12 ms budget, lag) match within a few percent.
2. **Predictions.** predictions.md (14:51) precedes every held-out artifact (heldout.txt 14:55,
   heldout_seed3.txt 14:56); the tuning artifacts (14:44–14:50) precede it; no f8 artifact exists
   before it. The kill criteria held: P1 everywhere in the tested range; P2 including the
   direction split the prediction missed (retrograde lands low without refusing). P3's
   quantitative clause (≈half the gap per halving) failed — convergence is superlinear — and P4
   held only at L8 (1.06× at L12/L15); both failures are disclosed in the dossier. P5's
   "identical counts" overstates: counts match within ±5 items (wall-dependent); end speeds are
   identical.
3. **Adversarial cases (three of my own; one outside the author's range).**
   - **32 s flights** (duration decade above the tested 8/16 s; ship and off, seed 1): the
     claim's structure holds — off collapses items (2,233→15 at L8, 3,159→310 at L15), lag(off)
     = 0.038 s at every flight, refusals grow monotonically (1/2/151 vs 1/1/73 at 16 s), every
     fault still `Refused("velocity outside the word")`. New, unreported: retrograde off lands
     **47.8% low** at 32 s (0.004723 vs 0.009044) — the 8→16 s improvement (6.6%→0.5%) is not a
     trend; and pburst(off) = 11–14 on retrograde/turn flights, so P1's "burst = 1" is
     prograde-only at longer durations. Both strengthen the deletion-is-broken half; the page
     now carries both.
   - **Seed 7** (8 s, both arms): counts and 6-digit end speeds identical to seeds 1/3 — the
     level-set claim confirmed on a third seed.
   - **f8 16 s** (the one arm regen.sh never re-ran): digests bit-identical to the author's
     held-out run (3fe8369e…, df79cc30…, 476e2c61…, b5f5d9b3…, 7f992ada…); end |v|/c
     0.004334/0.070298/0.492695 exact.
4. **Mechanism verified in code.** step.rs:51's comment states the velocity-word contract the
   dossier attributes to the clamp; step.rs:402 is the exact refusal site; `thrust::owed`
   (thrust.rs:134) is closed-form in rapidity, as the carry contract claims.
5. **Novelty.** The page already held the lever (carry the burn, don't spread — 174d; tide
   counterfactual 0–24 events — 0f2a). New here: the page's own open question ("the word-margin
   the thrust step protects must survive at readout") is answered by measurement — it does not;
   the refine alternative is dead (the lag is invariant to sampling, and ~1% error stands at any
   cadence); and the carry's contract is measured (exponent on the flushed word, ½aτ² in the
   readers' ramp, no re-anchor). Neither edge appears in any prior Runs line; no H entry covers
   them.
6. **Page.** The fold-in was faithful except four overstatements, corrected in place:
   "27–230×" (the tables source 19–204× prograde, 7–71× retrograde/turn), "4–8×" for the 16×
   refinement (4–14× across flights), the envelope quoted at 8 s only (4.2e-2 at 16 s), "7–10%
   low" (a single point, 6.6%), plus the 32 s non-monotonicity note.
7. **Goal fit.** frame-cost is a board-named bottleneck, and the run answers the view page's
   "one adoption, three bottlenecks" pricing ask. PRINCIPLES 19 is quoted aptly ("if you find
   yourself fixing things that's oftentimes a signal that it is the wrong representation") and
   principle 14's "we only care about changes": a held burn at constant α is one change, not
   2,990.

## Why silver, not gold

The run's own headline — the carry is right, "and this run prices its exact contract" — stops one
experiment short of itself. The contract's central clause (the flushed word can carry its own
exponent, i.e. step it instead of refusing) was testable in the same probe as a one-arm spike and
was not run; nor was any frozen gate asked whether the ~1% end-speed error or the owed-dv envelope
already fails it (PRINCIPLES 34: "the oracles are guards" — the run never consulted them, so "not
buying accuracy" is measured against the probe's own arm only). The 10×-class gain (19–204×
events, the L8+ lag class deleted) therefore remains priced, not demonstrated.

**The one experiment:** the exponent-stepping spike — `off` arm plus, on
`Refused("velocity outside the word")`, refitting the velocity word's exponent to hold the
flushed lump, then re-flying the same flights. If the burn lands at the fine limit with ≈coast
events and 0.038 s lag, the carry composes and the gain is demonstrated (gold); if the word
cannot step without a law change, the priced contract is wrong and the design must say so.

## What the author missed

- The spike above — the cheap, decisive test of the claim's own center.
- The duration decade: the retrograde error is non-monotone in T (6.6% → 0.5% → 47.8% at
  8/16/32 s) and pburst(off) ≠ 1 off-prograde at 32 s; both outside 8–16 s, both strengthen the
  claim, both unmeasured.
- No gate run on any arm (B-series/F1), so the ~1% error and the envelope are never judged
  against a frozen oracle.
- Minor numeric looseness in the dossier: "27–230×" (max ≈204×), "4–8×" (to 14×), "7–10% low"
  (one point, 6.6%), "identical counts" for seed 3 (±5), and "the ½aτ² the envelope measures"
  (the envelope is a dv envelope; ½aτ² is the position error it implies).
