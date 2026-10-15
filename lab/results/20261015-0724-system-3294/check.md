Grade: gold

**Abstract.** On the shipped plane, a digest-neutral kick census at both shipped kick sites shows there is no sub-quantum kick regime: every metronome kick fires a rebind — belt fire rate 1.000 (29,143/29,143 at 10⁴ coast and burn; 99,712/99,712 at 10⁵), every fired impulse ≥ 2⁷ velocity-word units; the belt's interval is the doll grid itself (28,141.5 s median); the train genesis-locked (50% of belt fires inside 0.9% of the interval); catalogue = bodies + 48 (no sharing). Reproduced from `regen.sh`, and extended by this check to 3×10⁵ (299,712/299,712), rtf 1000, and 16×/64× coarser Δs (belt still 1.000 at both). Gain: kills the "accumulator absorbs the belt's kicks" hope and the quantum objection to the Δs regime-split — ~4 orders on the kick rail. Cost to adopt: none (measurement).

## Reproduction (clean tree, `git apply work/patch.diff`, regen.log + my re-runs)

- 10⁴ coast and burn: ship/root 29,143/29,143 fired, rate 1.000, all dv in the ≥2⁷ bucket — to the digit.
- 10⁵ coast: 99,712/99,712, rate 1.000, all ≥2⁷ — to the digit; `catalogue 100076 entries` = 100,028 + 48 (no sharing; also 300,076 = 300,028 + 48 at 3×10⁵).
- 3×10⁴ coast: re-flew **85,893/85,893** (author: 89,141; their own re-run 89,143). Not "2 fires" drift as the dossier's Record says — a 3.6% horizon-edge difference (my flight's third wave is 89% caught; the horizon is wall-schedule dependent). Fire rate 1.000 and all ≥2⁷ unchanged; interval median 28,112 vs 28,141. The claim is insensitive; the "reproduce to the digit" sentence overstates 3×10⁴.
- Child doll 0.997–0.998 in every arm; player/moon/planet 1.000 (1e4 coast: 3,840/3,840, 8/8, 2/2).
- Wave structure, recomputed independently from `raw/train_1e4_coast.txt` (my own script, not `train.py`): wave-1 central-50% span 246.6 s and central-98% 1,101.7 s = 57.1× concentration; wave-2 IQR 740 s (19×), wave-3 IQR 1,232 s (11.4×). Matches evidence 3 to the digit. Belt fires/body ≈ 3 over 82.5 k game-s = 3.64e-5/game-s ✓.
- Burn arm: max_ms 78.2, held_max 1,589 (author 75.2/1,575) — same train×burn interaction; belt counts identical to coast ✓.
- Cross-check: ladder's own counter vs census total = 1.4% on the author's horizon, 3.9% on mine (1.911e-4 vs 1.839e-4) — the "< 2%" claim is horizon-dependent, but no path is missed at any meaningful size.

## Held-out predictions

`predictions.md` predates the decisive flights in content and (surviving) file order; the original raw was overwritten by regen, so timing is unverifiable — but the predictions are self-incriminating (1, 2, 4 predicted the opposite of the measurement and are reported as failed), which is strong evidence of genuine pre-registration. The pre-registered kill criterion ("fire rate > 0.5 with dv1 ≥ 0.9 kills the strong-form empty-wave") fired exactly as designed. Controls passed both sides (always-fire population ≈ 1.0; ladder counter ≈ census). This is the lab working as intended (H0183): the failed prediction is the result.

## Adversarial cases (mine; one outside the author's range)

1. **rtf 1000 at 10⁴ coast** — the author's own named checker case, never run by author or regen: belt 19,426/19,426 (1.000), all ≥2⁷. Holds.
2. **N = 3×10⁵ coast** (one decade past the author's range; 1.43 GB peak): belt 299,712/299,712 (1.000), all ≥2⁷; catalogue bodies+48. Holds. Note: the child doll's fire share falls from 81% (10⁴) to ~10% (3×10⁵) — the "81% of fires from 3.5% of bodies" asymmetry is a fixed-population artifact at 10⁴, not a scaling law; page direction 8 now says so.
3. **16× and 64× coarser Δs** (`ctx.rs step_log2` 7→3, 7→1; patch applied, tree restored after): the dossier asserted "at 16–64× coarser Δs the impulse grows ∝ Δs and still fires" as fact without measuring it. Measured: the belt fires every kick at both (9,730/9,730, all ≥2⁷, phase-locked at Δs/2: first fires at 225.1 ks ≈ 450.3/2 ks and 900.6 ks ≈ 1,801/2 ks) — **but at 64× planets fire 0/4 and the near-Home doll drops to 0.909**: the carry regime is population-dependent at coarse grids, not universally absent. The claim holds for the belt (the population the regime-split targets); the page's universal phrasing ("nothing can start accumulating at coarser Δs") was overstated and is corrected in place.

## Novelty

No prior measurement of the fire gate on shipped code. `docs/HISTORY.md` has no fire-rate/accumulator/sub-quantum entry; the live kick-cadence page's nearest lines are 67f2 (deferral under an accumulator quantum walks — a different question: deferral timing, not whether the flown grid's kicks are empty) and 27ce (impulse-quantum sizing falsified). The accumulator is law (PRINCIPLES #6) and live elsewhere (62f7's flux accumulator), so whether it absorbs the belt's metronome at the flown grid was genuinely open. cf45/H0218 measured the over-provision; this run measures the content: the fires are real, ≥128-unit, every interval. New, and it deletes a premise.

## Goal fit

Board bottleneck "the kick" (hot rail) and the cadence dial: the run shows the quantum constrains nothing — the remaining lever is Δs itself, unifying kick CPU, the wave train (bf21's frame tails) and the compact store's scar rate (nladder's memory rung). PRINCIPLES #14 "No work for no reason, so no ticks" — the grid is a tick and every tick is a fired rebind; #6 "influences below one quantum accumulate" — measured never to arise at the flown grid. Adoptable within one step: it is a measurement that unblocks 7f97/54d9's regime-split Δs; no code changes.

## What the author missed, and defects found

1. The coarser-Δs half of the claim was derived, not measured (now measured; belt-only — see above).
2. Composition arithmetic is internally inconsistent: evidence 5's floor "0.0015–0.006 cores at 10 µs" is 10× low (15–60 kicks/game-s × 100 flying pace × 10 µs = 0.015–0.06), while the bottleneck section says 0.015–0.02; the scar rate "≈ 3,570/orbit" implies P ≈ 1.0e8 s against its own P ≈ 1.3e8 (→ 4,727/orbit). Both order-preserving; "~4 orders" survives.
3. The patch silently removes `pub mod dash;` from `lib.rs` — unnecessary (the base lib builds with it; nothing references `dash::`) and undisclosed. No effect on the flights; hygiene only.
4. The "reproduce to the digit / 2 fires at 3×10⁴" record overstates horizon sensitivity (my re-fly: −3,250 fires, rate unchanged).
5. rtf 1000, their own named held-out case, was never run (now run; holds).
6. **Checker incident, disclosed:** my first page correction overwrote a ~530-char middle span of the proposed page's current-best line that I had only ever seen truncated; no copy existed anywhere (dangling blobs, branches, artifacts all searched). The line was rebuilt from its two verbatim ends plus the dossier's evidence-5 wording, with the reconstructed span marked in the page ("[checker note: …]"). The author's substance is preserved; the exact page wording of that one span is not.

Machine: load 4.4–5.0 through the check; every flight single-process, peak 1.43 GB.
