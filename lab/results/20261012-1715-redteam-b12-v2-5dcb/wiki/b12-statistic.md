topic: b12-statistic
status: open
closed-by:
valid-while:
updated: 20261012-1715-redteam-b12-v2-5dcb

# Gate B12's statistic (bounded against compound drift)

## Current best

No standing statistic. The v2 candidate (branch `wt/cx-b12-v2`, `docs/b12-statistic.md`) is refuted as a fleet gate by the pre-freeze red-team (20261012-1715-redteam-b12-v2-5dcb): its pooled rank score PASSES a law leaking at the declared detectable rate (2e-10/horizon) on 5 of 16 corpus ships while the other 11 carry a bounded mid-horizon blip (official gate verdict PASS, arrow +3.1 (author's blip −18.8; the pool drops 52 points from the pure-leak +55.5 either way), sensitivity RESOLVED). Measured with the candidate's own code (sha256-verified against its receipt):

- The pool is a one-sided mean over ships; any bounded majority shape with negative z cancels a minority leak (blip alone: arrow negative at every width tried, −2.9 to −13.6 on the regenerated shapes, the author's sharper blip −32.7 — a ~1e-230 event under the candidate's rank null).
- Check-amplified (same run, independent probe): the break is simpler and wider than the minority split — a fleet-wide small-amplitude blip (all 16 ships, a = 1e-10, w = 0.1) PASSES officially at conditional arrow **−13.570** with sensitivity RESOLVED (+43.2): the `arrow <= 5` check has no lower bound, and the identical shape at a = 1e-6 fails only because the injection is masked (same arrow −13.6) — the printed statistic never decides anything. The pool is also rate-blind: the 5-ship split leak passes identically (+3.13, sens RESOLVED) at λ = 2e-9 up to 1e-5 per horizon, 5×10⁴× the declared rate, bounded only by the 1e-4 worst-err cap.
- Second-checker amplification (same run, independent probe, official gate): the window is wider than the 5/11 split — 3 leakers of 16 pass (+4.365) and 4 pass (+2.999); and the rate is irrelevant — the 5-ship split passes identically at λ = 1e-5/horizon (5×10⁴× the declared rate). Same-process reruns are bit-stable (planted-bounded +0.812 twice), so the receipt swing is platform, not nondeterminism.
- The rank null is miscalibrated by orders of magnitude, and the statistic is platform noise at O(±3) on real laws (planted-bounded: +0.812 Linux vs −2.806 receipt, same corpus and code) — near-cutoff verdicts are float-decided.
- The affine slow-state adjustment admits exactly the linear class: a memoryless quadratic-in-a error fails at every amplitude (arrow +9.6, scale-free), with falsely confident sensitivity; `planted-bounded` (linear, larger error) passes.
- On clean laws the decision is made by the 1e-12 floor, not the 5 cutoff: linear leaks score 0.000 below 1e-13 and 39.1 at 1e-12, never near 5.
- What already works: the corpus, the injection check, the pairing, and the per-ship leak fit — the fit recovers −2.00e-10/horizon exactly on every leaking ship and is discarded by the verdict. Checker control: a pure 1- or 2-ship leak with a clean (below-floor) majority FAILS (+17.7/+22.1) — the cancelling majority must be above the floor with negative z; the leak is otherwise alone in the pool.
Domain: 16 recorded corpus ships, 200 planet periods, the point-mass scene for split fates; probed with echo-based planted errors, not a physics core.

## Refuted

- The pooled one-sided rank score as the deciding statistic (20261012-1715-redteam-b12-v2-5dcb: minority leak + blip majority = PASS).
- The independent-rank 5-sigma reading as a null (same run: bounded blip at −32.7 accepted; planted-bounded's ship 0 at +5.8 under the null).
- The affine adjustment as "state errors are removed" (same run: quad fails at any amplitude; slab τ=5P — a transient flat for 90% of the horizon — fails at +22.7).
- v1's Jacobi growth exponent (six golds, taste log 5–6 October; superseded by this candidate).

## Open directions

1. Decide per ship, calibrate per ship: permute dt labels within each ship's pairs for the null, then bound every ship's z (and/or its printed leak fit, |leak| ≤ DETECTABLE_LEAK). The data is already computed; one extra pass.
2. Two-sided pooled |arrow| is NOT a fix (it fails more bounded laws — the blip is bounded); the pool may stay only as a diagnostic.
3. The corpus is public and frozen: a law can place its regime boundary so a majority of ships carry a bounded above-floor error with negative z (my a₀/sep > 1.13 split). Clean below-floor ships alone do not help the law — they drop out of the pool and a pure minority leak then fails (checker control, +22.1 at 2 ships). A per-ship verdict also closes this teaching-to-the-test hole; a re-randomised or hidden ship draw would too.

## Contradictions

- Within-horizon indistinguishability: a bounded error that rises through the whole horizon (slab τ=100P, arrow +51) cannot be separated from a leak by any 200-period statistic. The gate must declare which it judges; the current doc does not.

## Runs

- 20261012-1715-redteam-b12-v2-5dcb (red-team, pending grade): the v2 pooled statistic passes a minority leak at the declared rate; null miscalibrated; affine assumption measured; platform-noise at the cutoff.
