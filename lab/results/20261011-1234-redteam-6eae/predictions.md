# Predictions (written before the decisive runs)

Attacks ranked in `dossier.md`. Decisive falsifier: static Schwarzschild (M=1), null geodesics
u'' + u = 3u² integrated backward from a static observer at r_o, ray grid over sky angle ψ;
images of a static emitter at (r_e, φ_e) = distinct ψ whose ray passes the emitter's spatial
point at any winding. Nothing is tuned: M, the equation, and the counters are fixed up front.

## Held-out case A: image counts (r_e = 20M)

| r_o | predicted max images | predicted fraction of emitter azimuths with ≥ 2 images |
|---|---|---|
| 10M | 2 | ≥ 0.10 |
| 5M  | 3 | ≥ 0.15 |
| 4M  | 4 | ≥ 0.2 |
| 3.5M | ≥ 5 | ≥ 0.3 |
| 3.2M | ≥ 6 | ≥ 0.4 |

Counts are lower bounds (limited by ray-grid resolution); the true count diverges as r_o → 3M.
Rationale: the "extra" images are winding images; their impact parameters cluster at
b_c = 3√3 M within exponentially thin intervals, and the passing corridor in ψ shrinks as
r_o → 3M, so more windings fit inside it.

## Held-out case B: the multi-image sky is not measure-zero
At r_o = 10M the Einstein-cone estimate θ_E ≈ sqrt(4M·D_eff⁻¹), D_eff = r_o r_e/(r_e − r_o) = 20M
gives θ_E ≈ 0.45 rad. I predict the measured two-image region (emitters behind the hole) is a
contiguous band of emitter azimuths wider than 0.3 rad, i.e. lensing multiplicity is a
first-order sky feature near a hole, not a tail.

## Held-out case C: the secondary image is bright
For emitters just inside the Einstein cone (offset within 0.3·θ_E of the axis) the two images'
arrival angles differ by O(θ_E), not by a micro-correction: both are O(θ_E) from the hole
direction. (Checked as: the two image directions bracket the hole.)

## Controls (must pass or the instrument is broken)
1. Weak-field: a ray with b = 200M has total bend 4M/b = 0.020 rad within 1%.
2. Capture: no ray with b < b_c = 3√3 M reaches r = 200M; some ray with b just above does.
3. Flat control: with M = 0 (u'' + u = 0) every emitter azimuth has exactly 1 image.

## Held-out case D (secondary attack, Binet bands near the separatrix)
r1's sampler draws only e ≤ 0.7 with p ≥ 6.5 + 2e (separatrix p_sep = 6 + 2e, plus 0.5).
Predictions for the m=16 band model vs exact Binet, one radial cycle:
- r1-style seeds (e ≤ 0.7, p ≥ p_sep + 0.5): precession relative error ≤ 1% (replicates r1's pass).
- Excluded seeds (e ∈ {0.8, 0.9, 0.95}, p − p_sep ∈ {0.5, 0.2, 0.1}): at least one seed with
  p − p_sep ≤ 0.2 has error > 20% or flips class (model plunges where exact stays bound, or the
  reverse), because the band-quantized unstable radius moves the model's separatrix by O(band width)
  and the whirl phase responds like 1/√(distance to separatrix).
- The exact per-cycle Δφ and its ∂Δφ/∂E diverge as p → p_sep (jet derivative blow-up): I predict
  ∂Δφ/∂E grows by ≥ 10× from p_sep + 1.0 to p_sep + 0.1 at fixed e = 0.9.

## What would make the attacks wrong
A: max images stays 2 at all r_o ≤ 4M, or the two-image region is measure-zero-thin → the "once"
premise is nearly right and only a memo flag is missing. D: band model stays within 1% everywhere
→ the linearization is robust up to the separatrix and r1's exclusion is harmless.
