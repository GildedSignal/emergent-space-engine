# Dossier — redteam 20261011-1234-6eae: the view's "once" premise

## Claim

The design's view premise — "each visible tube crosses the observer's past light cone once",
with lensing added by a single-valued memoized `deflection(b)` — is wrong by an integer
everywhere near a mass: a static emitter has ≥ 3 distinct sky images for **100% of emitter
positions** at every observer radius probed (100M down to 3.2M), 4 images for 99% at 3.2M,
and the count is unbounded (it grows with enumeration depth at every radius); no rung
exists that could catch this (r6 was never frozen), and the live view bakes exactly-once in
as a test invariant.

## Bottleneck

Not a cost bottleneck: a correctness hole in the plane's own measured bottleneck (the view
gather is 83% of a light frame, H0210) that widens exactly when the game's flagship content
(black holes; B19 rotating holes, Julien's next GR item) is on screen. What it deletes:
the "once" invariant and the single-sheet deflection memo, before r6 freezes criteria that
would enshrine them.

## Evidence

All numbers: `python3 view_images.py` in this folder (164 s; `python3 diag.py` shows the
curve structure in 4 s; `view_images.json` holds the full output). Float64, Schwarzschild
M=1, static observer at (r_o, φ=0), rays over sky angle ψ (one sky half; mirror images
added by symmetry: m_total(φ_e) = m(φ_e) + m(2π−φ_e)); emitters static on the circle r_e.
Images counted as level crossings of the unwrapped exit-azimuth curve Φ(ψ) at levels
φ_e + 2πℤ — density-independent; caustic folds count as distinct images.

**Controls.** Capture threshold: the least bent captured ray has b = 5.1973M vs b_c = 3√3 M
= 5.1962M (0.02%); no ray below b_c escapes. Flat (M=0): multiplicity exactly 1 on covered
azimuths (max 1). Weak-field bend over a [1000M, 1100M] arc: 0.0180 vs 0.02 asymptotic —
the deficit is the analytic tail beyond the arc; image counting uses only level topology,
never bend magnitudes. Two earlier instrument builds are recorded in the scripts' history:
v1 binned rays per azimuth (conflated density with multiplicity), v2's control launched
above its own escape cut; the numbers below are from the fixed v3 only.

**Multiplicity (total, both sky halves), static emitters:**

| r_o | r_e | ≥2 images | ≥3 | ≥4 | deepest bend resolved (uniform 32768 rays → corridor zoom 131072) |
|---|---|---|---|---|---|
| 100M | 200M | 100% | 100% | 0.7% | 9.45 → 14.7 rad (2.3 wraps) |
| 10M | 20M | 100% | 100% | 44% | 10.8 → 16.4 rad (2.6 wraps) |
| 5M | 20M | 100% | 100% | 64% | 11.4 → 17.0 rad (2.7 wraps) |
| 3.5M | 20M | 100% | 100% | 66% | 11.5 → 18.0 rad (2.9 wraps) |
| 3.2M | 20M | 100% | 100% | 99% | 12.5 → 17.7 rad (2.8 wraps) |

The count is a lower bound that grows with resolution at **every** r_o: the bend diverges
logarithmically as b → b_c⁺, so the branch set is infinite; a design must choose a cutoff,
and "once" plus a single-sheet memo cannot express the choice.

**The emitter exactly behind the hole (r_o = 10M, r_e = 20M, φ_e = π):** four images at
ψ = 141.1°, 152.3°, 207.7°, 218.9° (hole direction = 180°) — 26–39° apart on the sky, with
impact parameters 7.01M, 5.19M(≈b_c), and mirrors. The first secondary is far from the
critical parameter (not an exponentially demagnified relativistic image); magnification was
not measured (count only).

**What the code says today.** `crates/universe/src/view.rs`: "Each tube crosses the cone
once, and Newton's method finds the [crossing]"; the gather solves g(t) = t + |x(t)−X| − T
with Euclidean distance — no bending at all yet. `lifecycle.rs` asserts a ship is never
shown twice, i.e. exactly-once is a test invariant. `docs/law.md` line 53: "Lensing takes
deflection(b) from the doll's memo" — one bend per impact parameter, no winding index.
B16 (moving lenses) judges one deflection per seed against an oracle; nothing judges
multiplicity or branch continuity under observer motion. **No rung exists: r6 (view) is
listed as open in law.md line 88 and was never frozen.**

## Predictions (`predictions.md`, written before the runs)

- Case A (image counts): direction held, magnitudes split. Predicted frac_ge2 ≥ 0.10–0.40;
  measured 1.00 everywhere (under-predicted: the "Einstein cone" picture is wrong — wound
  families cover the whole circle). Predicted max images 2 at 10M rising to ≥6 at 3.2M;
  measured 4 at fixed 32768-ray resolution (over-predicted the max at fixed resolution;
  the zoom shows the cap is resolution, not physics).
- Case B (two-image band ≥ 0.3 rad): held and exceeded (whole circle).
- Case C (images O(θ_E) from the hole, bracketing it): held (141°/152°/208°/219° vs 180°).
- Case D (bands near separatrix): main prediction FAILED — the m16 band model survives at
  ≤ 0.53% error in the excluded regime; the jet part (≥10× derivative growth) is VOID.
- Controls: capture and flat passed; the weak-field bend control failed twice for
  instrument reasons (my control design, documented above) and passes with the finite-arc
  reading.

## Secondary probe: Binet bands where r1's sampler never goes (`bands.py`, 8 s, `bands.json`)

r1 drew p log-uniform in [10, 1000] with e ∈ [0, 0.7]; its guard "p ≥ 6.5 + 2e" (the
separatrix p_sep = 6 + 2e plus 0.5) is vacuous there (p_sep ≤ 7.9 < 10), so the frozen
rung says nothing about p < 10 or e > 0.7 — the zoom-whirl regime. v1 of this probe seeded
orbits with a wrong first integral (orbits crossed u = 0; both models ran on garbage) —
VOID, discarded. v2 (correct turning-point construction, 1/L² = 1/p − (3+e²)/p²):

- r1-domain control, 20 seeds: max precession error 0.015% (replicates r1's pass).
- Excluded domain, 12 seeds (e ∈ {0.8, 0.9, 0.95}, p − p_sep ∈ {0.1, 0.2, 0.5, 1.0}):
  all bound in model and exact, whirl cycles dφ = 12.2–19.3 rad, **max error 0.53%** —
  inside r1's 1% tolerance. The m16 band model is robust up to 0.1 above the separatrix.
  **This premise survives** where r1 never tested it; the rung's sampler, not the model,
  is what leaves the regime unverified (B9 already extends cost to e ≤ 0.99).
- Jet derivative (∂dφ/∂L, prediction D): probe VOID — the L ± hL perturbation at e = 0.9
  crosses the separatrix, where no bound orbit exists (complex root); a proper probe needs
  fixed-p variation or smaller hL. The v1 numbers (1.5×–2.1× growth) were computed on the
  garbage seeds and are withdrawn.

## What would make it wrong

The multiplicity table rests on static emitter and observer; a moving observer does not
reduce branch count (branches are created/destroyed at caustics — the Φ(ψ) folds measured
here — so motion makes the single-seed Newton tracking worse, not better). It would be
wrong if the game never puts an observer within ~100M of any compact mass — but black holes
are named in the goal and B19 is frozen. It would be irrelevant if the view is declared
non-physical (sprites, not physics) — but principle 30 makes the view's physics the point
("I want the player to feel what a human would feel in space").

## Cost of adoption, and fit with PRINCIPLES

The gather enumerates crossings per winding with an explicit magnification cutoff; the
doll's memo becomes multi-sheet (deflection per winding, or equivalent); Newton seeds per
branch. Cost: 2–4 crossings per emitter near a hole instead of 1 — the same order as the
design's own "Lensing adds crossings", now with the count named. This is representation,
not patching: principle 19 ("a fix signals the wrong representation"); principle 32
("under the right representation many symmetries can appear") — the multi-sheet deflection
is the photon region's symmetry, found rather than given. r6 must be frozen with
multiplicity and branch-continuity criteria before the view is built further — gates are
frozen before builds (AGENTS.md), and this red-team plus the probe is exactly the
pre-freeze evidence the lab owes (AGENTS.md: "Before any freeze, one GLM red-team and the
cheapest falsifying probe must have run").

Premises that survive, for the record: the two-body doll (r3 v3, B11 — ν only in the
energy map at 1PN); the Binet band model in the zoom-whirl regime (this run); undisturbed-
orbit cost ≈ 0 in its re-anchored-jet form (law.md line 35, redteam-df81) — already
adjudicated, nothing new added. The dense = sparse bit-identity (premise 4) remains
untested and unfrozen (r5 open): no float probe can touch an integer identity; it needs
its rung before it is load-bearing.

## The lens

A red-team lens overweights exotic cases; I ranked by player-likelihood and the finding
does not rest on the photon-sphere tail (frac ≥ 3 images is 100% already at 100M). What
the lens may have made me miss: cost-side attacks (I found a correctness hole and did not
measure the gather's added cost per branch), the moving-lens interaction (B16's aberration
machinery combined with multi-sheet branches, only sketched), and magnification cutoffs —
which images a player can actually see were not measured; count only.
