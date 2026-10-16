# Predictions (written before the decisive arms)

Baseline instrument (already run, N=10³ coast, budget-free, 20 s wall): event-per-frame peaks
~176–240, in **Home's doll (d2)**, boundary-dominated (k≈30, b≈110–143 per storm frame), storm
frames spaced ≈ 198.5 frames ≈ 331 game-s; alternate storm frames carry no body attribution
(suspected: the Armada fleet's hand-out lane, not the locals).

Hypothesis: the interval law anchors every planet-doll body to the **absolute** power-of-two grid
(`aligned`), and all ladder locals are born at one tick, so same-step bodies boundary and kick at
identical absolute ticks forever: a **standing, non-decaying comb** (unlike the belt wave, which is
a one-shot first-kick train that decays ×0.72 per wave). The one-step spread that cured the belt
wave persists there only because the clock law chains each kick's time from the previous kick; the
interval law instead re-locks to the absolute grid, so a one-shot offset is absorbed within one step.

Cases not tuned on (held out until after this file): the arms' behaviour at N=10⁴, the train beyond
6,000 game-s, and the fleet-lane storm frames.

Predictions:

- **P1 (structure).** The comb is standing: over ≥ 6,000 game-s (≥ 18 periods) the storm heights do
  not decay by more than ~10% per period (the belt wave decays ×0.72). Heights are N-independent for
  every N ≥ 600 (the locals are capped at 300), and at N=0 (no locals) the peak collapses to ≲ 60
  events/frame (917c's 51).
- **P2 (the one-shot spread is absorbed).** With `ES_LOCAL_STAGGER` (a planet-doll ship's first
  interval offset by a uniform id-derived fraction of its own step — the belt cure transposed), the
  comb re-forms: after at most one period the storm heights return to ≥ 80% of the baseline, and the
  total events per game-second are unchanged. The lever does NOT dephase the population.
- **P3 (a permanent per-body phase collapses it).** With `ES_LOCAL_PHASE` (each body's grid offset
  by a constant id-derived fraction of its own step), the d2 storm frames collapse toward the N=0
  floor (max d2-attributable events/frame ≤ ~60, ≥ 3× below baseline) and the train's periodicity
  disappears; total events per game-second unchanged within ~2% (the same work, spread); the digest
  at the canonical cut differs from the record (this is a law change: pair-shared boundaries are
  given up) — recorded, not judged here.
- **P4 (the other lane).** The empty-attribution storm frames stay empty and unchanged under both
  levers (they are the fleet's hand-outs, a different lane the levers do not touch).
- **P5 (identity control).** With no env flags, the patched binary's `ladder_digest` rows equal the
  record's (the patch is default-off; bit-identity of the OFF arm).

Kill criteria: if the baseline train decays like the belt wave (P1 false), the comb reading is wrong;
if `ES_LOCAL_STAGGER` does dephase (P2 false), direction 1 stands and the page's lever is adopted;
if `ES_LOCAL_PHASE` does not collapse the storms, the comb is not the mechanism.
