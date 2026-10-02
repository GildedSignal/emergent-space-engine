Grade: silver

**Abstract.** The E9 red-team the handoff asked for. Claim: phase 2's tide kernel is not phase 1's — the Newtonian-form tensor is O(1)-wrong and even the Riemann-projected tensor misses a γ²-scale radial factor. Fully reproduced (decisive JSON bit-identical, 90 s; kernel numbers 2.29/21.9 and 1.56/23.6 match). My attack confirms the direction and resolves the author's own hedge: probe.py's Riemann template has R_{r̂φ̂r̂φ̂} = +M/r³; the true −M/r³ gives radial tide −w(3γ²−1) (−2w×1.50 at 6M, ×16.0 at 3.1M), matching the geodesic measurement as window→0. The quoted 23.6 carries 47% window leakage; the γ²·7/6 fit is wrong. With the sign fixed, member errors halve and the epoch-rule finding survives (2395 vs 16081). One re-derivation from gold; cost to adopt: a corrected kernel table.

## Reproduction

- `python3 eeff.py` (10.9 s): naiveFrac 2.2873 / 21.8971 (r = 6 / 3.1), Eeff radial 1.5598 / 23.58, einsum 1.1665 / 6.00 — all match the dossier.
- `python3 probe.py --only all --out /tmp/check-fermi2/probe-check.json` (90 s): **zero** field differences against `probe-decisive.json` (kernel, epochs, τ₁₀, refits, every L1/L2/L3 error), and the table equals `decisive.log`.
- Ordering: probe.py 06:02:49, eeff.py 06:11:16, `predictions.md` 06:12:38, decisive.log + JSON 06:18:20. Predictions were written first. Honest reporting: P1/P2 failed and are said so.

## Adversarial cases (4)

1. **Analytic eigenvalue check.** probe's einsum E equals {−w(γ²+1), +w} to 9 decimals at 7 radii — but the geodesic-measured tide converges elsewhere: as window h→0 (h₀, h₀/2, /4, /8), Eeff radial → −2w×1.5006 (r=6) and −2w×16.12 (r=3.1), invariant under all three launch conventions I tried (author's U=u, Ω-matched normalized, cubic-refit). Two robust constructions disagreed; one had to be broken.
2. **Root cause.** Direct Christoffel computation: R^r_{φrφ} = −M/r ⇒ R_{r̂φ̂r̂φ̂} = −M/r³ (vacuum + spherical symmetry force the same). probe.py's `_BASE {(1,2,1,2): +1.0}` has the sign flipped. With −1.0, the einsum equals the closed form −w(3γ²−1), +w to machine precision at both radii **and** the geodesic measurement: 1.5000 vs 1.5006; 16.0000 vs 16.119. The author's oracle was right; their einsum was the broken side — exactly the hedge they left open ("unresolved which side errs").
3. **Window leakage in the oracle itself.** The author's full-window values are inflated: 1.56 vs true 1.50 (+4%), 23.6 vs 16.0 (+47%). Their proposed closed form γ²·7/6 fits r=6 only by coincidence (it gives 12.8, not 16, at r=3.1). Correct: −w(3γ²−1), γ² = f/(1−3M/r).
4. **Corrected-kernel re-run** (circ-r6, circ-r3.1, L1 only): rad-0.018 err_max 0.335→0.171 (r=6), 0.653→0.238 (r=3.1). Part of the claimed "member harness floor" was the broken kernel; a floor ~0.17 remains, so P1 fails even with the true kernel. Epochs at r=3.1: naive axis 16081 vs tensor-rate 2395 (6.7×; was 6.3×) — F4 survives. At r=6 the corrected true-axis count is 4017 (still phase-1 band; the tensor rule, 2877, is cheapest) — P5 survives.

## Novelty and fit

HANDOFF: "E9 is built but unfrozen, waiting for its red-team… its failing radius sets the Fermi phase 2." No HISTORY entry measures the Fermi-frame Schwarzschild tide (H0203 was the law's red-team; H0021–H0024 are compact predicates). Direct hit on board focus item 4. Principle 22 ("fermi is there to spot issues early not an oracle"; oracles are guards): K2 — validate any phase-2 kernel against geodesic pair differences, never against its own formula — is vindicated in the most literal way: the author's own formula was wrong and only their geodesic construction caught it. That, plus the closed-form kernel (eigenvalues −w(3γ²−1), +w, Marck axis), is E9's positive and negative control, ready to freeze.

## Why silver, not gold

- Held-out predictions did not hold (P1, P2 failed; P3, P4 partial — honestly reported; same bar that kept the law's red-team at silver).
- The delivered numbers are inflated up to 47% (no h→0 convergence test on the decisive measurement) and the delivered closed form is wrong; the member-level L1 tables — the evidence for "no safe radius" — are contaminated by the same template bug, since L1 was never the true projected law.
- The adoptable artifact (corrected kernel, corrected member/epoch tables, frozen E9 controls) is one experiment away, and that experiment is now fully specified.

**The experiment that would make it gold:** re-run the decisive table with the template sign fixed (or the closed form −w(3γ²−1), +w + Marck axis), with Eeff windows pushed to h→0; freeze E9's controls: the naive kernel must FAIL, the corrected projected tensor must PASS against geodesic pair differences at r = 6 and 3.1M.

## What the author missed

- The root cause was one Christoffel symbol away (R_{rφrφ} = −M/r) and one convergence test away; they hedged correctly but did not resolve, and fitted a wrong closed form to an inflated number.
- The L1 law ("the premise") was built from the broken tensor, so its member errors measured the bug, not the premise; the harness-floor and kernel-error confounding was not separated.
- Out-of-plane structure (admitted): for any future 3D work, R_{θ̂φ̂θ̂φ̂} = +2M/r³, not +M/r³ — the 2D slice's third component differs from naive expectations.
- The "×21.9 at the photon sphere" headline mixes normalizations (‖·‖ relative to the small naive norm); relative to the true tide the naive kernel is O(1)-wrong everywhere with a wrongly rotating axis — the surviving, cleaner statement.
