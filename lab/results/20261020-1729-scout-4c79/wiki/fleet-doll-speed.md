topic: fleet-doll-speed
status: open
closed-by:
valid-while:
updated: 20261020-1729-scout-4c79

# The fleet doll's interior tide law at the game's own speeds

## Current best

**NEW (4c79, scout — the page's od 3 (coefficient half) and od 4 closed by an exact
instrument, od 2's eigenvalue bar certified: the cure is
the exact transverse-periapsis law at every compactness and every speed, and the speed
axis of the legality rule is dead).** A separation-free instrument (exact float64
Riemann from analytic Christoffels, vacuum control 2.8×10⁻¹⁷, projected on the
boosted static orthonormal frame at periapsis — eigenvalues are Fermi-invariant, so
no finite difference and no offset enter; β = local static-frame speed) measures the
transverse-periapsis tide on the 7×7 grid r_p ∈ {6…300}M × β_p ∈ {0.25…0.999}:
**radial = γ²(2+β²)/2 × Newtonian to ≤ 7×10⁻¹⁵ at every point (β 0.999: ×749.875),
along-motion exactly 1.000000000, out-of-plane γ²(1+2β²) to ≤ 7×10⁻¹⁵ (od 4's
quoted form CONFIRMED; rival γ²|1−2β²| excluded 4.2× at β 0.9; 3D dolls carry
×148.75 at β 0.99), cross-terms 0.** **P4, the integrator's amendment (od 1): the
residual has NO M/r term — identical machine precision at r_p = 6M and 300M — the
speed amplification is purely kinematic and exact, so it leaves the weak-field error
budget entirely and the legality rule must gate on compactness alone.** At the
letter's own cap the Newtonian tensor errs by exactly 10.000% (series
1.5β²+1.875β⁴ = 10.107%) against its O(β²) = 6.25% budget line: the budget
misprices its own cap by the kinematic term it excludes. **The freeze bar (od 2,
"within 1% of γ²(2+β²)/2·2GM/r_p³") is certified at 10⁻¹⁵ through β 0.999** — the
earlier "FD probe and cure degrade together above β 0.9" (od 3) is settled as
instrument error, not law error. Second instrument (parallel-transported Fermi
frame, RK4, the Marck/Kubižňák construction) independently reproduces the same
periapsis eigenvalues (−3.0000, 1.0000, 2.0000 M/r³ at β 0.5; −14.789/1.0000/13.789
at β 0.9). **P5 (second order in ξ) remains open and sharpened:** naive member
congruences are not formations — a θ-offset member is not even a geodesic (it falls
back through the plane), and constant-(E,L) members carry ξ̇ = ∇_ξ u ≠ 0; the one
aligned case (radial offsets, β 0.9) shows true/ODE −0.136% at ξ₀/r_p = 10⁻⁴ →
−0.298% at 3×10⁻² (IC floor + slow growth). Named next: exponential-map member ICs
(20261020-1729-scout-4c79; float-only, empty patch).**

Checker (4c79, gold): reproduced bit-for-bit; a third, symbolic path (sympy Riemann +
boost, symbolic Ricci = 0) confirms all three forms identically; exactness extends a
decade in speed (β 0.999999; the along-motion channel's float cancellation floors at
1.1×10⁻⁴ there — instrument, not law) and below the compactness floor (r 2.5M, inside
the photon sphere). Scope: the closed forms are transverse-motion only — oblique 45° at
β 0.9 reads −8.39/+1.00/+7.39 M/r³ (in-plane amplification ≈ 1+(z−1)cos²α; the middle
eigenvalue is exactly 1 at every angle, so the cancellation is universal).

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
  [4c79: the ×74/×750 closed values are now MEASURED exact to 10⁻¹⁵ by the
  separation-free instrument — the "probe-biased above 0.99" caveat is closed as
  instrument error.]
- **A diagonal "boosted tide" cure (E_rr → γ²E_rr, E_θθ → γ²E_θθ): wrong — the
  along-motion channel is exactly Newtonian at any speed (the (1,1,1,1) cancellation;
  radial infall 0.9995); only the transverse channel amplifies
  (20261020-1002-redteam-288f, exact wedge algebra + FD).**
  [4c79: the along-motion 1× is confirmed at machine precision on the full grid.]
- **"1PN terms are O((nR/c)²)" as the weak-field rule's error budget (frame.rs L83):
  at the rule's own cap the radial coefficient error is 1.5β² = 9.4% (closed 10.0%,
  measured 9.88%) and the per-orbit member error is 30%/115%, not 6.25%
  (20261020-1002-redteam-288f).**
  [4c79: exact 10.000% independently; and the amplification carries no M/r term at
  all — the budget's speed axis is a category error, not a size error.]
- **The rival out-of-plane form γ²|1−2β²| (the sign-algebra alternative this run's
  author could not exclude by hand): excluded 4.2× at β 0.9, 3.0× at β 0.999
  (20261020-1729-scout-4c79).**

## Open directions

1. ~~The integrator's amendment: replace the interior tensor with the contracted E(u)
   (one line of coefficients; the same kick) and re-derive the weak-field rule around
   compactness (M/r), not speed — the speed term was hiding the wrong law.~~
   **Evidence complete (4c79): the speed amplification is exact and M/r-independent
   (≤ 7×10⁻¹⁵ from 6M to 300M), so the re-derived rule gates on compactness alone;
   the build (integer coefficients in frame.rs) is the integrator's.**
2. ~~Freeze the hyperbolic arm (criterion in the run's dossier): transverse-periapsis
   origin at β ∈ {0.5, 0.9}, radial eigenvalue within 1% of γ²(2+β²)/2·2GM/r_p³, exit
   within 5% of geodesic truth, Newtonian the negative, along-motion = 1× the
   cancellation control.~~ **The eigenvalue bar is certified at 10⁻¹⁵ through β 0.999
   and down to r_p = 6M (4c79); the exit-within-5% half is 288f's integrated
   measurement; the freeze is the integrator's call.**
3. β ≥ 0.99 with a fatter instrument: ~~the FD probe's offset rotation pollutes; the
   cure's integrated error degrades there — second-order-in-ξ not yet separated~~.
   **The coefficient half is closed (4c79: separation-free instrument, exact). What
   remains is the second-order-in-ξ half: member geodesics need exponential-map ICs
   (naive θ-offsets are not geodesics; constant-(E,L) members carry ξ̇ ≠ 0) — the
   named next experiment.**
   Checker2: the boundary starts already at β 0.95 — exit cure 3.7% [r] but 16%
   [th], worse than the letter's 1.5% there (the letter's coefficient is still 12×
   off: |A|/|N| 12.7 vs closed 14.8) — and an oblique 45° β 0.7 flyby (br ≠ 0 at
   launch, off the author's axes, the only case exercising the cure's cross-term
   structure) confirms both the kill (letter matrix 152% wrong, exit [r] 16.3%) and
   the cure (matrix relerr 0.29, exit [r] 1.8%); r = 20 M at β 0.5 re-reads 1.511
   vs closed 1.496 (radius-independent, purely kinematic), and a mirrored member
   (−ξ) reproduces the +ξ rows to 0.3 pts.
4. ~~The out-of-plane channel (3D scenes) γ²(1+2β²) — quoted exact, unmeasured here.~~
   **Measured (4c79): confirmed to ≤ 7×10⁻¹⁵ on the full grid; 3D scenes carry
   ×148.75 at β 0.99.**
5. (from 4c79) The exponential-map member ICs for the second-order-in-ξ question:
   member = exp_{x_o(τ)}(ξ^a e_a) with matched ξ̇, judged against the built deviation
   ODE at ξ₀ up to the extent bound r_p/32; the frame-rotation record (ψ ≈ the
   geometric sweep, 2.9–3.1 rad on these flybys) is the FD probe's de-rotation
   missing term.

## Contradictions

None open. E9's circular eigenvalue and this run's closed form are the same algebra
in two notations; E9's standing FAIL (10/21, phase-1 units) is a different channel
(clock/axes conventions), not a conflict with these numbers.

## Runs
- 20261020-1002-redteam-288f (this run, awaiting grade): the fleet doll's Newtonian
  tide refuted on the transverse channel at player speed (×1.10 at the cap, ×7.4 at
  β 0.9), exactly right along-motion; cure = the full Riemann contraction, O(1)
  coefficients; legality collision with B15's 0.9c stream
- 20261020-1729-scout-4c79 (awaiting grade): the cure certified exact by a separation-free
  instrument (machine precision, β to 0.999, r_p to 6M); out-of-plane confirmed; no
  M/r term — the legality rule's speed axis dead; second-order-in-ξ sharpened to
  exponential-map ICs
