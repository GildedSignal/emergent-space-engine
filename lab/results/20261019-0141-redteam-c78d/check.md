Grade: gold

**Abstract.** Refuted: representation.md L59's "aggregates are one sample each" on the
occlusion channel — one predicate makes any fleet-scale eclipse all-or-nothing.
Reproduced byte-identical from regen.sh (21 s, <1 GB): 89.1%/99.0% mid-transit flux
error at R_f = 3/10·R_p (closed form 1−(R_p/R_f)²), f₁ = 0 while ≥ 88.9% of flux is
visible, blink width exactly 2·R_p, survives exact retardation + k⁴ at β 0.5; orthogonal
to 1885 (fails at β = 0, uniform). Checker extended it: taleb-09b5's arc formation errs
1.000, β 0.9 peaks 0.695/0.856, R_f = 30 reads 0.9991. Gain: deletes the rule before it
ships. Adopt: strike L59's first clause (doc edit) + freeze the aggregate eclipse-parity
arm (criterion in dossier; two freeze fixes and the closed-form cure's domain corrected
on the page).

## Reasons

1. **Reproduction.** `regen.sh` in the clean tree: exit 0, output byte-identical to the
   stored `regen-output.txt`, 21 s wall. `work/patch.diff` is empty (no tree edits — all
   numbers come from the run's own script, so nothing can fail to regenerate). My
   independent reimplementation of the β arm (retarded quadratic, segment-vs-disc, k⁴)
   reproduces f_true_min = 0.535 exactly. The letter is confirmed verbatim at
   docs/representation.md L59 and L116 ("The view ≤ 1 sample per pixel per frame").
2. **Pre-registration.** predictions.md (mtime 01:50:29) precedes results.json/regen
   output (02:00:25); run.log is empty, so ordering rests on mtimes — but the substance
   is decisive: 4 of 10 predictions missed *against* the author's thesis (P2 28.9% vs
   <5%, P5-peak 60.5% vs 30–50%, P6 0.109 vs ±10pp of 0.891, P10 6.7% vs >60%), each
   disclosed with the correct mechanism. You do not pre-register wrong numbers after
   seeing the data. The frozen kill criterion (peak > 5% with partial dimming at any
   R_f ≥ R_p) held in every such config, both orientations.
3. **Novelty.** The topic page's own direction 5 names "aggregate emitters (partial
   dimming, not row drops)" as unmeasured; 22d1 measured the *per-row* law only;
   1885 killed the same L59 sentence on the *dispersion* channel (needs σ_β > 0) and its
   belt control reads zero exactly where this run's failure lives (β = 0, uniform). No
   HISTORY entry mentions eclipse; grep confirms no file in lab/rungs/ mentions
   occlusion/eclipse. This is the missing half, measured.
4. **My adversarial cases** (four; two outside the author's swept ranges):
   - *The game's own fleet shape*: a 400-ship arc formation (r = 3·R_p, 60° — the
     taleb-09b5 formation the dossier itself cites as counter-evidence) errs **1.000**
     (centroid behind, every ship visible); a ring annulus likewise peaks at 1.000. The
     refutation is *stronger* in the formation case than in the swept disc case.
   - *Next decade of size*: R_f = 30·R_p → 0.9991 (law 0.9989).
   - *Next decade of speed*: β = 0.9, both orientations → peaks 0.695 (transit) / 0.856
     (sky), blink present in both (f₁ = 0 while f_true > 0.5).
   - *Mechanism*: at β 0.5 transit seen-mid, mean occluded weight 0.56 vs visible 0.54 —
     k⁴ is not the driver at β 0.5; geometry is, as the dossier's channel claim requires.
5. **Goal fit.** "Shows that a premise is wrong," adoptable within one step: a one-line
   amendment of L59 (direction 1) plus a freeze-ready rung arm (direction 2). Defends
   principle 28 ("the view is an instrument… it's a space clock literally" — an
   instrument that blinks out whole fleets carries no information) and principle 20
   (the blink is the tail, not the average); the cure is principle 3 (derivable ⇒ never
   evolved).
6. **Page.** The fold-in was faithful on every number I checked against the regen; I
   corrected it in place: restored the missing `## Current best` header (schema), bound
   the closed-form cure to its measured domain (uniform disc, β → 0: errs 11.1pp on the
   ring, 24.1pp on the arc, 10.4–31.3pp at β 0.9), marked the 690× compression as
   density-dependent, added the arc/β 0.9/R_f = 30 confirmations, and recorded two
   freeze fixes for the proposed criterion.

## What the author missed

- **The formation case is the strongest one and was not run**: discs only, despite the
  dossier's own counter-evidence paragraph naming taleb-09b5's fleet-on-one-orbit. The
  arc errs 1.000 and breaks the proposed closed-form cure (24.1pp).
- **The "cheapest cure" is domain-blind**: the circle–overlap closed form is licensed
  only for uniform discs at β → 0; judged at the criterion's own "player β" it fails
  (10.4–31.3pp at β 0.9). At player β the licensed cure is per-pixel exact predicates.
- **Two internal tensions in the freeze-ready criterion**: "≤ 150 samples" is
  R_f = 3-specific (R_f = 30 pays 11,677 at h = R_p/2), and "reproduce f_true_min ≥
  0.88" cannot survive "judged at player β" (the exact minima there are 0.535/0.815);
  bar it as within 5% of each arm's exact minimum.
- **Sparse aggregates invert the compression claim**: a 400-ship formation pays more
  per-pixel samples (145–1957) than per-ship predicates (400); and a sub-pixel fleet
  cannot pay pixels at all — the amendment should say which readout wins there
  (exact per-ship sums, or shape moments).
- run.log is empty; the pre-registration case rests on mtimes plus the disclosed
  adverse misses (sufficient here, but the process log should be captured).
