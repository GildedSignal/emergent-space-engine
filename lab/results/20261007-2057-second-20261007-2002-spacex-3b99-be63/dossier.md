# Dossier — second author on 20261007-2002-spacex-3b99: the record now regenerates, and the time-to-ceiling is re-anchored on measured premises — the forcing channel is an embedded Pluto-class body, not the N-scaled mutual walk

## Claim

The silver's ceiling stands — a belt's live distinguishing information saturates at its own element entropy (39.0/51.0/63.0 bits measured against 39.2/51.2/63.2 caps at scar widths 2⁻¹⁶/⁻²⁰/⁻²⁴), so per-body identity scars bust 32 bits/body at any width finer than 2⁻¹³·⁶ and shipmem must split H_live by identity class — and with the record now bitwise regenerable by the shipped code, the re-anchored rate says the split is forced not by the mutual walk (at fixed belt mass 2×10⁻⁷ M\*, a 10⁹-body belt needs 4.3×10¹² orbits ≈ 1.3×10¹³ game-years to reach the ceiling; the original "~9 orbits" held per-body mass fixed, i.e. a 0.1 M\* disk, which the test-particle premise forbids) but by any embedded massive body: one 10⁻⁷ M\* perturber carries the belt to ≥ 90% of the ceiling in 32 orbits (97 game-years) at every N — H_live ≈ 1.7×10⁻⁸ bits/body/game-second — and an embedded Pluto-class body (6.9×10⁻⁹ M\*) busts the 32-bit budget within a 30-game-year session.

## Bottleneck

The board's unmeasured risk "distinctions created per game-second (H_live) decide the 10⁹-in-8-GB fit". The checker blocked gold on two named items; both are done here: (1) every stored number now regenerates from shipped code, (2) the time-to-ceiling is anchored on a stated, measured belt-mass premise with the ceiling claim unchanged. Plus one new measured finding the re-anchoring forced: the σ instrument itself needed a physical b-floor (below).

## Evidence

All in this folder; each command reproduces its data file.

- **Record regenerates bitwise (gold blocker 1).** `hlive.py` now carries the hot case's variance-preserving Poisson thinning (rate/50, kicks ×√50, same RNG stream) that the original run applied off-file. `python3 hlive.py` (67 s) regenerates `hlive_results.json` **bitwise identical** to the original branch's stored record — all 5 cases × 2 seeds, every checkpoint float and conjunction count (hot included: sim 31,668,064 = the stored count; `hlive_results_ORIG.json` kept for comparison). `python3 measure_sig.py` (73 s) regenerates `hlive_sig.json` bitwise (md5 `c4f01db2e1cff9cc5a6a92af86560e8a` = `hlive_sig_ORIG.json`). Hot flux check (sim×50/analytic) = 1.000026 / 0.999938.
- **N-scaling measured, not assumed (`rescale2.py`, 170 s → `rescale2_results.json`).** Floored instrument (below), cold belt, t=30: fixed-m scan slope of log₂σ vs log₂n = **+0.50** and fixed-total-mass slope = **−0.45** over n = 1000→10⁴ (n=2000 anchor included); σ·√n constant within 12% (2-seed point at 10⁴). Perturber-channel σ at fixed per-body rate is n-stable within 5.6% over n = 1000→10⁴ (λ_p = 0.1475 has no n in it). Prediction file `predictions.md` (written first) plus `predictions-addendum.md` for the second round.
- **Re-anchored game-scale numbers (floored anchors).** Fixed total belt mass 2×10⁻⁷ M\*: t_ceiling(10⁹) = 4.3×10¹² orbits = 1.3×10¹³ game-years — never inside a game; H_live(mutual) ≈ 1.2×10⁻¹⁹ bits/body/game-second. Perturber channel (N-independent): bits(30 orbits) = 46.0 of 51.2; 90% of ceiling at 32 orbits = 97 game-years; 50 bits at 195 orbits; H_live(pert, 90%) = 1.7×10⁻⁸; the 32-bit bust within a 30-game-year session happens at m_pert = 6.9×10⁻⁹ M\* = 1.06 Pluto masses. The original's fixed-m extrapolation (9.1 orbits, 27.7 yr, H_live 5.9×10⁻⁸) is retained only as the inadmissible premise it is (belt = 0.1 M\*).
- **New finding: the σ instrument needed a physical floor.** Pre-registered predictions 1–3 of `predictions.md` **failed**: unfloored, the population σ grows with n even at fixed per-body kick rate (pert channel: 4.2×10⁻³ → 1.3×10⁻² over n = 100→10⁴; `rescale.py`, 98 s → `rescale_results_unfloored.json`). Cause, localized: dv = 2Gm/(b·v_rel) with b = √U·b_max has p(dv) ∝ dv⁻³ (log-divergent variance), so the empirical σ is an order statistic of the closest approach ever drawn — IQR of the same walk is n-stable (+7%) while p99 grows +88% and max ×9.7. With b floored at the pair's mutual Hill radius (where the no-collision impulse premise ends and the exact-encounter subsystem, m-meso-motion/r8, begins; floored events keep the law's maximum impulse — an upper bound), stability returns. Consequence for `b-h-live`: quantile-based or Hill-floored σ; the original's saturation numbers are unaffected (histogram entropy's integral converges for these tails), its pre-saturation σ-based per-field bits carry this noise.
- **Carried from the original, unchanged:** caps 2·log₂(W/q)+log₂(1/q) = 39.22/51.22/63.22; 39.0/51.0/63.0 measured (cold m=10⁻⁸, t=300); reabsorption 0.0102σ (refit removes < 0.2% of scar bits); 32-bit bust width q = 2⁻¹³·⁵⁹; multiset floor log₂(eM/n) ≈ 22 bits at 2⁻²⁰ (21.8 with the belt's honest L-range W/2, 22.8 with W).

## Predictions

`predictions.md` was written before `rescale.py`; its items 1–3 failed and the failure was the finding (σ order-statistic instability, above); items 4–5's regeneration halves held and were exceeded (hot row bitwise too), the re-anchor halves held on the floored instrument (fixed-M ceiling ≫ 10⁶ orbits; pert ≥ 90% within ~10² orbits; Pluto-class threshold within 40% of the predicted 5×10⁻⁹). `predictions-addendum.md` (before `rescale2.py`): A1's IQR/tail localization held, its first-100-bodies sub-test was uninformative (a 100-sample σ under these tails swings tens of percent — disclosed as a design miss); A2 held (5.6% at n ≥ 1000; the n=100 point sits 14% low, the estimator's small-sample bias); A3 held via the slopes (+0.50/−0.45 at n ≥ 1000) with the n=100 point unusable; A4 held in full.

## What would make it wrong

The MC's max-entropy kick geometry (random direction, uniform anomaly) still overestimates scar entropy versus correlated conjunction geometry, and resonant locking (r4's regime) would slow the walk; the N-scaling is validated over two decades of n inside one model whose λ ∝ surface-density premise is kinetic-theory standard (flux validated to 0.004% at n=2000) but not simulated at 10⁹ itself; the Hill-floor keeps the impulse law's own maximum for sub-Hill encounters, so perturber rates are upper bounds — a collision-law treatment there could only lower them; the Pluto-class threshold scales with the floor convention by ~1.5× (order-of-magnitude statement); the multiset floor is computed, not implemented; whether an occupancy multiset can carry the replay contract (taleb-c271) remains untested and is the real hole — deleting per-body identity is exactly where exact replays live.

## Cost of adoption, fit with PRINCIPLES

Same as the silver's, now on honest premises: `shipmem`/`b-h-live` splits H_live by identity class — identity scars only where identity is law (named ships, families, the player's consequences, small N), occupancy/program representations for anonymous multitudes ("Store the generator, not the generated"; "The memory floor is information-theoretic"), keeping "every body real, never averaged" (an occupancy multiset stores every body exactly). New instrumentation requirement for `b-h-live`: field spreads from Hill-floored σ or ≥10⁴-sample histograms, never raw population σ of an unfloored 1/b walk. The rate table it will measure against: mutual ≈ 10⁻¹⁹ (fixed mass, 10⁹), embedded-perturber ≈ 2×10⁻⁸ bits/body/game-second.

## The lens

The second-author lens risked grading my own fixes too kindly; the guard was pre-registering both prediction files and keeping the failed-unfloored run as data. What it may have missed: the replay-contract question stayed out of scope (the checker named it as the follow-up, not the gold blocker — it is the next run); the Hill floor's upper-bound reading of sub-Hill encounters; and the small-n σ̂ bias (n=100 unusable) shrinks the measured scaling range to one decade plus anchor, where the original's checker accepted two decades of analytic scaling.

## Reproduce (≤ 173 s each)

```
python3 hlive.py        # 67 s  -> hlive_results.json (bitwise = original record)
python3 measure_sig.py  # 73 s  -> hlive_sig.json     (bitwise = original record)
python3 rescale.py      # 98 s  -> rescale_results_unfloored.json (failed-pred record)
python3 rescale2.py     # 170 s -> rescale2_results.json (diagnostics + floored re-anchor)
```
