topic: fleet-doll-speed
status: open
closed-by:
valid-while:
updated: 20261020-1002-redteam-288f

# The fleet doll's interior tide law at the game's own speeds

## Current best

**The letter's interior law (representation.md L23, law.md L50, frame.rs L14–19: the
Newtonian tensor in the Fermi frame) is refuted on the transverse channel and exactly
right on the longitudinal one (20261020-1002-redteam-288f, float64 Schwarzschild
geodesics + parallel-transported Fermi axes, controls on both sides).** The exact law
at a transverse closest approach: **radial tide γ²(2+β²)/2 × Newtonian, along-motion
exactly 1× at any β** (the four-minus-ones cancellation E'₂₂ = w; derived exactly two
ways; radial infall measured 0.9995 — the amplification is transverse-only, the null
limit a plane-wave pulse; out-of-plane γ²(1+2β²), not the game's 2D). Measured by
Richardson FD on member geodesics: ×1.0988 at β 0.25 (closed 1.1000), ×1.5052 at β 0.5
(1.4963), ≥6.3 at β 0.9 (closed 7.348; scalar probe 8.3, probe-biased). Integrated:
at the shipped weak-field cap (n·R = c/4 exactly, r = 18 M) the letter errs **30%
(radial member) / 115% (along-track) per orbit** — its own budget line says O(β²) =
6.25% — and the contracted cure reads 0.23%/1.1%; at r = 100 M flybys the letter errs
4.3% (β 0.5) / 9.0% (β 0.9) exit separation and recovers 5% of the true formation
stretch at β 0.9 (truth ×1.105 vs letter ×1.005). **The legality collision:** frame.rs
`ORBIT_SPEED_DIV = 4` refuses every origin above c/4, so B15's own 0.9c fleet stream
(the letter's flagship scene) has no legal fleet doll, and the plane's γ 120 red line
sits at a ×2.2×10⁴ radial tide. The cure is the same O(1) integer kick with corrected
coefficients (the full Riemann contraction's t-row and E_tθ cross term are
load-bearing; a diagonal boost-only "cure" is wrong by O(γ²) along-motion); licensed
by this instrument to β 0.9 (above, the FD probe and the cure degrade together —
open). E9's frozen circular eigenvalue w(3γ²−1) equals this closed form identically
(the integrator already owns the circular case); no rung or gate judges a doll
interior at player speed (B15 is cost-only; r5's scenes are contact arms; E9's tubes
stop at ~0.5c periapsis and fail 10/21 for phase-1 reasons). Freeze-ready hyperbolic
arm in the run's dossier.

## Refuted

- **"Inside it, tides are linear to first order, with the Clohessy–Wiltshire closed
  form" extended to the game's speeds (representation.md L23 as shipped): the radial
  Fermi coefficient at transverse closest approach is γ²(2+β²)/2 × the Newtonian one —
  measured ×1.10 at the legality cap and ×1.50 at β 0.5 (FD); closed form gives
  ×7.4/×74/×750 at β 0.9/0.99/0.999 (probe-biased there: norm ≥6.3 at 0.9, polluted
  above 0.99); per-orbit member error 30%/115% at the cap; formation stretch
  understated 20× at
  β 0.9 (20261020-1002-redteam-288f).**
- **A diagonal "boosted tide" cure (E_rr → γ²E_rr, E_θθ → γ²E_θθ): wrong — the
  along-motion channel is exactly Newtonian at any speed (the (1,1,1,1) cancellation;
  radial infall 0.9995); only the transverse channel amplifies
  (20261020-1002-redteam-288f, exact wedge algebra + FD).**
- **"1PN terms are O((nR/c)²)" as the weak-field rule's error budget (frame.rs L83):
  at the rule's own cap the radial coefficient error is 1.5β² = 9.4% (closed 10.0%,
  measured 9.88%) and the per-orbit member error is 30%/115%, not 6.25%
  (20261020-1002-redteam-288f).**

## Open directions

1. The integrator's amendment: replace the interior tensor with the contracted E(u)
   (one line of coefficients; the same kick) and re-derive the weak-field rule around
   compactness (M/r), not speed — the speed term was hiding the wrong law.
2. Freeze the hyperbolic arm (criterion in the run's dossier): transverse-periapsis
   origin at β ∈ {0.5, 0.9}, radial eigenvalue within 1% of γ²(2+β²)/2·2GM/r_p³, exit
   within 5% of geodesic truth, Newtonian the negative, along-motion = 1× the
   cancellation control.
3. β ≥ 0.99 with a fatter instrument (the FD probe's offset rotation pollutes; the
   cure's integrated error degrades there — second-order-in-ξ not yet separated).
   Checker2: the boundary starts already at β 0.95 — exit cure 3.7% [r] but 16%
   [th], worse than the letter's 1.5% there (the letter's coefficient is still 12×
   off: |A|/|N| 12.7 vs closed 14.8) — and an oblique 45° β 0.7 flyby (br ≠ 0 at
   launch, off the author's axes, the only case exercising the cure's cross-term
   structure) confirms both the kill (letter matrix 152% wrong, exit [r] 16.3%) and
   the cure (matrix relerr 0.29, exit [r] 1.8%); r = 20 M at β 0.5 re-reads 1.511
   vs closed 1.496 (radius-independent, purely kinematic), and a mirrored member
   (−ξ) reproduces the +ξ rows to 0.3 pts.
4. The out-of-plane channel (3D scenes) γ²(1+2β²) — quoted exact, unmeasured here.

## Contradictions

None open. E9's circular eigenvalue and this run's closed form are the same algebra
in two notations; E9's standing FAIL (10/21, phase-1 units) is a different channel
(clock/axes conventions), not a conflict with these numbers.

## Runs
- 20261020-1002-redteam-288f (this run, awaiting grade): the fleet doll's Newtonian
  tide refuted on the transverse channel at player speed (×1.10 at the cap, ×7.4 at
  β 0.9), exactly right along-motion; cure = the full Riemann contraction, O(1)
  coefficients; legality collision with B15's 0.9c stream
