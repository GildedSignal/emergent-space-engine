Grade: gold

Reproduced end to end in a clean tree (patch applied by me; bases bit-identical; data rows of my arms
byte-identical to the record where horizons overlap). The checker-named experiment is done and decisive:
the symmetric clock start pays the identical per-body bill (ρ(on−off, sym−off) = 0.904/0.898/0.902;
ref-free medians 2.09 vs 2.08 ×10⁻⁷), the corrected class ratio is 2.5–3.0× (ω fires 3.02/3.03 at the
3× bar), and 75d6's seed-2 "drowning" is proven an instrument bug (its regen read arms at +2·P_min, ref
at +1·P_min; the off arm's own one-orbit drift reproduces its stored numbers to four digits:
2.004×10⁻⁴, 6.23×10⁻⁴, 7.73×10⁻³). Cost to adopt: none measured blocks ed3a's 17× compute claim; the
integrator's question becomes "which bar" (a B13/B14-class gate at ≤3× passes both shapes, ≤2× kills
both). Gain: deletes the stagger-shape search, types the bill (one-time, unbiased, ~2×10⁻⁷).

## Reproduction (everything I reran matched)

- Bases s1/s2 bit-identical to `ticks.txt`; all arms of a seed read at one identical tick (verified in
  every horizon row and the settle digests).
- s1 h1 (my own runs, my own analysis code): K2 on 2.809/2.538/3.022, sym 2.463/2.435/3.031 (lna/e/om);
  off−ref9 band 6.483×10⁻⁸; ref-free medians on 2.087×10⁻⁷, sym 2.082×10⁻⁷; K5 ρ 0.904/0.898/0.902;
  descriptive ρ(|on−off|, offset) 0.556; C1 0/128; P5 alive, refusals 0. All equal `analysis.json` to
  the last digit.
- s2 h1: K2 ω 3.818/3.913, e 3.942/3.695, lna 2.985/2.799; ρ 0.784/0.833/0.856; ref-free
  1.872/1.649×10⁻⁷; off−ref9 5.498×10⁻⁸ — seed 2 is as quiet as seed 1 at a common tick, as claimed.
- C4 from the record's mech CSVs: off 128/128 lead == first_kick; on 128/128; sym |lead − off's first
  kick| ≤ 506,580 ticks = 9.3×10⁻⁵ of a step. The patch's construction is what it claims
  (`plan_clock_at` clears and re-derives the plan at t+off; the offset draw is shared verbatim).
- Determinism: my s2 CSVs' data rows are byte-identical to the record's; s1 differ only by the
  author's extra h2 rows (I ran h1 only).

## Adversarial (three, one outside the author's range)

1. **Seed 3 — never tested by the author; fires harder.** K2 e 4.31/4.34, ω 3.24/3.33, lna 3.36/2.85;
   ρ = 0.967–0.976; ref-free differentials 1.1–1.5×10⁻⁷. The shared-term mechanism and the ≥3× class on
   e and ω generalize beyond the tested domain (the s1 ω marginality, 3.02 by 0.7%, is not the edge the
   bar rests on).
2. **Horizon 4 orbits (author stopped at 2):** the differential decays further — lna 2.09/2.08×10⁻⁷ →
   1.10/1.35×10⁻⁷ (ratio 0.53/0.65), e and ω likewise (≈0.7–0.8). The one-time typing holds a decade
   past the measured range; no late growth appears.
3. **The horizon bug, measured:** 75d6's regen (its branch) reads `off 2 … 2` / `on 2 … 2` and
   `ref 2 … 1`. My off-arm s2 run at +2·P_min vs +1·P_min drifts by med |Δln a| 2.004×10⁻⁴,
   |Δe| 6.23×10⁻⁴, |Δω| 7.73×10⁻³ — exactly 75d6's stored "resonance drowning" (2.004×10⁻⁴, 6.228×10⁻⁴,
   7.727×10⁻³). One orbit of real evolution, identical in every arm: instrument bug, not physics.

## Predictions

`predictions.md` predates `dossier.md`/`analyze.py` (file order; the author's original CSV mtimes were
overwritten by the runner's regen, so strict time-proof is impossible — but P1 and P7 failed, in the
direction of the findings, and are disclosed: nobody fabricates misses). Held: P2 (sym fires), P3
(ρ ≥ 0.7), P5, P6, P8, P9. Wrong: P1's band (4.8× was still tick-inflated), P7 (the drowning).

## Novelty and the page

`docs/HISTORY.md` has no stagger entries; the published page explicitly left the symmetric variant "a
hypothesis to measure, not a held result" — this run measures it. Not a repetition. The proposed page
folds the result in faithfully (refuted entries carry the run id; prior bests retained; direction 1
correctly rewritten from "adopt the symmetric" to "price the trade"; the seed-2 scope paragraph is
corrected on the evidence). One understatement, not overstatement: "e 2.4–2.5×" covers seed 1 only —
seed 2's e fires 3.70/3.94 (left as is). Not three gold runs on this topic (75d6 silver; ed3a/f094/8a40
ungraded here): the page stays open; do not close it.

## Goal fit

PRINCIPLES #9 "A failed experiment kills that configuration, never the method" — the symmetric-shape
configuration dies, the measurement hands the decision to the gates; #13 "types of errors and not just
errors" — the term is typed (one-time, unbiased, non-compounding, shared), which is what makes it
priceable; #2 — judged against the same law's finest ladder at identical ticks. Board: the legality
gate was what blocked the birth-wave cure at the 10⁹-bodies gap; this closes the shape search and
leaves a one-step pricing decision.

## What the author missed

- No ref10 arm: the ω criterion's ladder-convergence margin at exactly the 3× line is unmeasured (the
  author names it; my seed 3 de-risks the bar itself but not the s1 marginal row).
- The "any per-body-grid-shifting shape" generalization rests on two shapes plus the mechanism; the
  third shape (offset quantised to the kick's own sub-grid) is untested — correctly kept open on the
  page, but the dossier's claim sentence reads stronger than n=2 shapes.
- ref8_s1 was not independently rerun by me; its role (the anchoring line) is secondary and rides the
  same deterministic pipeline I verified on nine arms.
- K1's largest bias (|z| = 2.59, s2 lna) is under the bar but the closest call in the record; a frozen
  gate should watch it.

For silver there would be an experiment to name; there is not — the one named (ref10 before freezing a
3× gate on ω) is already the page's open direction 1.
