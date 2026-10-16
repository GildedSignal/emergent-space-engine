# Predictions (written before the decisive flight matrix)

The decisive experiment (the checker's named one for e7ef's gold): the measured levers composed
into the shipped ladder — the 8× regime split of the belt clock (`BELT_SPLIT`, constants-only bulk
test at ≥ 4 Hill radii of band separation), the genesis stagger (`STAGGER_GENESIS`, f82a), and
b583's windowed crash-search guess (tick-exact, unconditional) — flown against shipped at 10⁵ and
3×10⁵, rtf 1800–7200, with 9e75's freeze instrument. Cases I have not tuned on (the 1e4 smokes
at rtf 600/3600 tuned nothing decisive; the belt never fired at rtf 600, and at 1e4 the locals
dominate the stream 4:1):

- **P1 (the split's belt rate).** At 3×10⁵ the belt term of the kick stream falls to
  **0.125 ± 0.02** of shipped (÷8 for ≥ 99% of belt bodies; a tail of high-e outer-belt bodies
  inside 4 Hill radii of Giant stays at the shipped cadence). Measured as (total kicks − the
  1e4-measured non-belt term) per game-s, composed vs shipped at matched delivered game-time.
- **P2 (the freeze at matched pace).** Shipped 3×10⁵ rtf 1800 spells **19–26 s** (9e75 measured
  20.9–23.5; the positive control of the failure mode). The composed arm at the same N and pace,
  flown past the staggered crest's arrival (~112.6 k game-s ≈ 63 s wall), spells **≤ 2 s**
  (deficit ≤ 10% of shipped's). At 36× the player's pace (rtf 3600) the composed arm still holds:
  spell ≤ 5 s, because its total demand (belt ÷ 8 + locals ≈ 2.9–4.2 events/game-s × rtf) stays
  under the 0.72/Ĉ ceiling.
- **P3 (the composed ceiling exists — the control that must fail).** Composed 3×10⁵ at rtf 7200
  (72× the player's pace) exceeds the ceiling (≈ 20.7 k events/s demanded against ≈ 14.4 k/s at
  Ĉ ≈ 50 µs) and spells **≥ 3 s**. If no arm of the composed build can be made to spell, the
  instrument, not the law, is broken.
- **P4 (b583's term is absent from the belt).** The impact-guess counters fire **identically**
  on shipped and composed belt-scale arms (≈ the 1e4 count ± 10%: the searches are the locals'
  and the fleet's, never the belt's — the belt's periapsis ≥ 1.2 AU never crosses the star's
  surface, so `next_impact` is never called for it). And per-event cost Ĉ (spell µs/ev) moves
  **< 10%** between `IMPACT_GUESS=0` and `=1` on a belt-dominated arm. Consequence: the named
  composition's kick-cost term is empty for the 10⁹ population — if P1–P3 hold, the freeze cure
  is delivered but the **10⁹ average does not close**: 1e9 × 4.44e-6 × Ĉ × 100 ≈ 22 cores x86 /
  13 M1 without the delete, ≈ 8.7 / 5.1 with 1a46's 61% — over 4 on both anchors.
- **P5 (health).** Refusals 0, dead bodies ≈ the shipped arm's (a law change may move lost-at-
  surface counts by individual cases, not classes), player alive, memory < 1.5 GB at 3×10⁵.

What would make me wrong: P1 failing (the bulk test misclassifying — then the measured rate ratio
names the misclassification); P2's composed arm spelling like shipped (then the split does not
compose with the stagger and the crest survives at 8× coarser cadence); P4's counters firing on
the belt (then b583's halving does act and the closure arithmetic must be redone with the halved
Ĉ — the outcome the checker expected); Ĉ at 3×10⁵ far from 50 µs (then every ceiling above moves
with it — the ceilings are stated in the measured Ĉ, not the prior).

10⁶ is not flown: its build (2.34 GB, 9e75's measurement) busts this container's 2 GB process
cap; the crest's N-linearity (9e75, ratio 3.08–3.09 at 3×) carries the scale-up. This is the
named limit of the matrix, said here rather than hidden.
