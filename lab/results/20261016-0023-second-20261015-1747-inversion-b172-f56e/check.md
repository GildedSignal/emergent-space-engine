Grade: silver

**Abstract.** Claim: b172's record closed regenerably — depth inversion (1.014@20k → 26.07@32k → 29.26@48k, cap 4,096), mint bill scene-invariant and exact (270,979; "273,200" loose), angular reading killed (fills 616,250 invariant in w and K). Everything reproduces bit-exact (runner regen + my re-flights; patch = b172 verbatim + one +14/−5 knob hunk) and extends: seed 5@48k 14.77, 64k 27.34, razor 270,979/270,978 → 0/1 evictions, all price-law exact. But the mechanism half is refuted by the author's own named, unflown a-cell (flown here): continuous radius alone leaves fills exactly 616,250 and ratio 1.013 — the win is not bought by radius concentration; the belt's 1.66M/7.23 is the e×spread interaction (a-spread + belt e → hits 1,528,417 ≈ belt's 1,528,451). Adoption rule must re-scope from radius to e; one step.

## Reproduction

- The runner's `regen.sh` exited 0 ("anchors + identity OK"); `table.txt` regenerates all 23 arms, zero digest mismatches.
- I applied `work/patch.diff` myself and verified it against b172's published branch: `git diff` between the patches is **one scenario.rs hunk, +14/−5, the two knobs only** — "b172's patch verbatim" is exact. Knobs are env-gated, default-off, and the belt branch is untouched: form100 20k ctl digest `15fc19b1…` and belt 20k ctl `d3542eea…` equal b172's published digests.
- Re-flown with the author's binary: form100 48k cap 4,096 lands **bit-for-bit** (digest `7bb62936…`, 7,928,202/270,979, hits 1,486,660 — the b172 checker's probe to the digit, as claimed); belt 48k ctl digest `63ead741…` exact.
- Derived integers re-checked from the table: price law at 48k (7,657,223 = 7,657,223), e70 price law (90,616 = 90,616), 32k ratio 26.075, all fills figures. regen.sh's anchor block re-freezes the published record (1,528,451 / 7.226 / 1.014 / 132,278) — good practice.

## Predictions

Credible: P4's premise and P6a **failed and are reported against their forks** — the strongest pre-registration signal (mtime order is weakly consistent: build 25 m → scripts 23–21 m → predictions 19 m → flights → addendum; the runner's regen overwrote flight mtimes, so file times alone cannot prove order). P1/P2/P3/P5 held exactly; the failed sub-prediction (bills diverge at depth) is reported and its failure *is* the invariance finding. One fork was written as exhaustive and was not: see below.

## Adversarial (all outside the author's domain)

1. **Seed 5 at depth (48k, cap 4,096)** — the author's depth bracket was single-seed: ratio **14.77** (4,087,021/276,656; bill 276,656; price law exact 3,810,365 = 3,810,365). The inversion holds (≫3), but the constant is seed-dependent: 29.26 is seed 1's, not a law. The claim's sentence survives because it scopes to "no cap below the mint bill serves".
2. **Deeper than flown (64k, cap 4,096)**: ratio **27.34** (8,053,448/294,357; bill 294,357 = 2.94×N; price law exact 7,759,091 = 7,759,091; identity clean). The small cap stays dead past two recurrences; the ratio plateaus (~27–29), it does not compound.
3. **The mint-bill razor at depth**: cap 270,979 → hits = global's 9,143,883, promotions = demotions, **0 evictions**; cap 270,978 → **1 eviction**. The corrected bill is exact, and the b172 checker's "273,200 exactly" is confirmed loose. This run's correction is now razor-proven, not inferred.
4. **The a-draw cell — the author's named remaining edge ("~1 h more work; named as the remaining edge"), flown by this check** (a third knob on the same draw lane: `a` uniform over [2,3) AU, the belt's own lane-1 formula; everything else form-like). At 20k/cap 4,096: **ratio 1.0131, fills exactly 616,250, hits exactly 486,063** — identical to every form variant to the digit, digest-identical ctl/retain/cap. Neither branch of the author's registered fork ("holds 1.01 with belt-level fills → volume exonerated" / "reads ~7 → radius spread load-bearing") obtains: **the radius draw alone is inert on both axes.** The closure cell (a-draw + belt e, uniform angle) reads hits **1,528,417 ≈ the belt's 1,528,451** (Δ 0.002%, the angle-bit map differs). So: e alone (banded a) +146k fills and ratio 1.013→1.696; a-spread alone +0; e × a-spread together +1.04M fills and ratio → 3.00 (0757's belt@4,096). The complete 2×2 cube is measured.

Consequence: the dossier's mechanism sentence — "the intra-wave win is bought by the radius draw (locality dominant, volume a minority)" — and the adoption rule's sizing axis ("small cap for **radius-concentrated** episodes"; "the cap's sizing axis is the population's radius structure") are **wrong as stated**: a fully radius-diffuse, low-e population (uniform a over [2,3), uniform angle) holds the small cap at 1.013 with the formation's own fills, while a radius-concentrated population with belt e degrades to 1.696. The load-bearing axis is **e (radial excursions) in interaction with the radius spread**; radius concentration is neither necessary nor sufficient. The author's P4/P6a premise ("the belt's radial orbit crossings under σ 0.07" / "the a-draw is the volume driver") missed that the a-draw moves nothing without e.

## Novelty

Genuine continuation: the nladder page's open direction 5(a) named the depth arms and 5(b) the matched-fills control as unmeasured; f56e lands both regenerably and kills the angular reading (new). No HISTORY/wiki entry holds the depth bracket, the bill invariance, or the fills decomposition. The 20261006 co-orbital gold is a different bottleneck (encounter tiering).

## The page

Faithful on the depth, bill and angular findings; corrected in place where it overstates the mechanism (three edits: the "bought by the radius draw" clause, the Refuted "radius/e draw lanes" line, and open direction 5(c)'s "radius/e structure" sentence), each marked as the checker's a-cell bracket with the measured numbers.

## Goal fit

Moves the board's memory/live-bodies seam: the depth record and the exact scene-invariant mint bill are the decision inputs for any bounded-cap adoption at 10⁹, and the claim is honestly re-scoped to measurements. PRINCIPLES: "A failed expectation is not automatically a failed method: diagnose which one broke" — practised twice (P1 sub-prediction, P6a); "Measure before claiming" — the one cell not measured is the one that breaks the sentence, which is the lesson.

## The one experiment that would make it gold

Fly the a-draw cell in the run's own regenerable battery (this check's knob is 7 lines on the author's hunk) and re-scope the claim's mechanism half to what the full cube now shows: fills and the intra-wave cap win are invariant under angular spread, clump count **and radius spread** at formation e; the belt's 1.66M fills / 7.23 ratio are the e × radius-spread interaction; the small cap's sizing axis is the population's e structure (radial excursion/crossing), not its radius concentration. The measurements for this are already on record from this check; landing them in the battery and rewriting the sentence is the step.

## What the author missed

- **The a-draw cell** — named as the completing measurement, priced at ~1 h, left unflown while 23 arms flew; it overturns the mechanism half of the claim (above). The registered two-branch fork shared a false premise (that the a-draw must move fills), exactly the P6a failure mode repeated.
- The depth ratio is seed-dependent (29.26 → 14.77 at seed 5); the dossier flags single-seed as a limitation but the claim's numbers read as constants.
- Minor: the dossier's "checker: same 7,928,202" and "84.7/28.6" cite the b172 checker's box; my re-flight gives 86.3/29.1 — fine, but walls are order-of-magnitude only and could be said once.
