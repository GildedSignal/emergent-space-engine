# Dossier — 20261020-1729-scout-4c79 (scout), topic fleet-doll-speed

## Claim

The fleet doll's transverse-tide cure (the contracted E(u)) is not a weak-field
approximation but the exact Schwarzschild law at every compactness and every speed:
measured to ≤ 7×10⁻¹⁵ against the closed forms γ²(2+β²)/2 (radial), 1 (along-motion)
and γ²(1+2β²) (out-of-plane, the page's quoted-but-unmeasured channel, here measured
and confirmed, rival form excluded 4.2×) — by an instrument with no separation
parameter, which settles the page's open β ≥ 0.99 hole as instrument error, and gives
the integrator's compactness amendment its missing number: the speed amplification has
**no M/r term at all** (residual ≤ 7×10⁻¹⁵ from r_p = 6M to 300M), so the legality
rule's error budget must gate on compactness, never on speed.

## Bottleneck

The board's flyable-engine line: the fleet doll is the frame every battle/fleet scene
runs in, and today it has **no legal doll at player speed** (frame.rs
`ORBIT_SPEED_DIV = 4` refuses every origin above c/4; B15's 0.9c fleet stream — the
letter's flagship — is refused; the plane's γ120 red line sits on a ×2.2×10⁴ radial
tide). The cure is already designed as the same O(1) integer kick with corrected
coefficients (288f); what blocked its freeze was the license: the FD instrument and
the cure "degrade together" above β 0.9, so nothing could certify the 1% freeze bar
there. This run is that certificate, machine-precision, to β 0.999 — it deletes the
speed axis of the legality rule (the error there is exactly known and exactly cheap:
one line of coefficients) and leaves only compactness to gate. No 10× CPU gain
claimed; the gain is scope: the doll's legal domain extends from β 0.25 to β 0.999 at
zero additional cost.

## Evidence (all commands ≤ 60 s; `python3 instrument.py grid` ≈ 0.2 s, `nonlin` ≈ 20 s)

Instrument: exact float64 Schwarzschild Riemann (analytic Christoffels with analytic
dΓ/dr; Riemann by the standard formula; vacuum control max|Ric| = 2.8×10⁻¹⁷),
projected at periapsis on the boosted static orthonormal frame — eigenvalues are
invariant under the rotation to the Fermi frame, so **no finite difference and no
separation parameter enter** (288f's FD probe had both). Cross-terms measure
0.0–1.2×10⁻¹⁸ (channels decouple). β is the speed against the local static observer.

- **P1 radial (the freeze bar, od 2):** measured/closed = γ_p²(2+β_p²)/2 at every
  point of the 7×7 grid r_p ∈ {6, 8, 10, 20, 50, 100, 300}M × β_p ∈ {0.25, 0.5, 0.7,
  0.9, 0.95, 0.99, 0.999}; max |relerr| 7×10⁻¹⁵. At β 0.999 the radial tide is
  ×749.875 — the exact number the game's high-c feel rides on.
- **P2 along-motion:** exactly 1.000000000 at all 49 points (the four-minus-ones
  cancellation, independently reproduced).
- **P3 out-of-plane (od 4, quoted-never-measured):** γ²(1+2β²) confirmed to ≤
  7×10⁻¹⁵; the rival γ²|1−2β²| excluded 4.2× at β 0.9 (13.789 vs 3.263) and 3.0× at
  β 0.999. 3D dolls carry ×148.75 at β 0.99.
- **P4 radius independence (od 1's evidence):** the P1 residual shows **no M/r
  trend** — same ≤ 7×10⁻¹⁵ at r_p = 6M (two Schwarzschild radii off the horizon) as
  at 300M. The speed amplification is purely kinematic and exact; speed leaves the
  weak-field error budget entirely. What the legality rule must gate is compactness
  (where the seam's other terms — frame quantization, geodetic precession, second
  order in ξ — actually live).
- **P6 the letter's own cap:** at β 0.25 the Newtonian letter errs by exactly
  10.000% on the radial coefficient (series 1.5β²+1.875β⁴ = 10.107%) against its
  budget line O(β²) = 6.25%: the budget misprices its own cap by 1.6× — the
  mispricing is the kinematic term the budget excludes.
- **Second instrument, independent path:** a parallel-transported Fermi frame
  integrated along the true flyby geodesic (RK4, the Marck/Kubižňák construction,
  arXiv:0811.0012) reproduces the same eigenvalues at its detected periapsis
  (−3.0000, 1.0000, 2.0000)·M/r³ at β 0.5; −14.789, 1.0000, 13.789 at β 0.9;
  −149.35, 1.0000, 148.35 at β 0.99 (0.3% off closed there — the periapsis is
  detected at r = 20.0275M at h = 0.25M; the exact-periapsis instrument above is the
  primary). Two instruments, one algebra, agreement where they overlap.
- **P5 (second order in ξ, the other half of od 3) — NOT cleanly measured, and the
  miss is informative:** the naive member constructions are not formations. A
  θ-offset member with the same coordinate u is **not even a geodesic** (it falls
  back through the equatorial plane: Γ^θ_φφ(u^φ)² ≠ 0 — measured exit ratio 1.0008,
  a symmetry artifact, not physics), and constant-(E,L) members carry a nonzero
  initial Fermi relative velocity ξ̇ = ∇_ξ u that pollutes the comparison at the
  10⁻¹–10⁻³ level. The one aligned case (radial-offset members at β 0.9, S_ode
  0.99632): true/ODE stretch ratio −0.136% at ξ₀/r_p = 10⁻⁴ growing to −0.298% at
  3×10⁻² — an IC-mismatch floor plus slow growth, consistent with a small
  second-order term but not certifying it. **Named next experiment:** exponential-map
  ICs (member = exp_{x_o(τ)}(ξ^a e_a) with the ODE's ξ̇ from the same map) — the
  deviation ODE and the transported frame are built and verified; only the member
  IC construction is missing.

## Predictions

All in `predictions.md`, written before the decisive runs. **P1, P2, P3, P4, P6
held** (P1/P3 beyond their bars: machine precision, not 0.1%). **P5 failed to be
measured cleanly** — the prediction letter (3–10% at r_p/32) is neither confirmed
nor killed; the failure mechanism (non-geodesic θ-offset congruence; IC mismatch)
is itself the finding, and it is exactly the doll's hand-out question
(order-boundary's boundary spec): formation members must be handed out on Fermi ICs.

## What would make it wrong, adoption cost, fit

- **Wrong if:** the game's doll interiors ever feel a second mass's field (the
  projection is one-mass Schwarzschild exact; the two-mass 1PN regime is the
  gravity-law page's open rule), or a rotating parent (Kerr: the frame drags; the
  contraction gains frame-rotation terms), or if the integer quantization of the
  corrected coefficients loses the exactness in integers (not tested here — float
  only, no engine change; patch is empty).
- **Adoption:** none from this run beyond the freeze evidence — the cure itself is
  288f's design and the integrator's amendment. This run licenses it: the freeze
  criterion's "within 1% of γ²(2+β²)/2·2GM/r_p³" bar is certified at 10⁻¹⁵ through
  β 0.999 and down to r_p = 6M, and the legality rule can drop its speed axis.
- **PRINCIPLES:** #7 "Gravity is compiled into geometry held by cells" — the tide
  coefficient is geometry, exact, never stepped; #3 "Compute only surprises… clocks,
  redshift, views are derived, not evolved" — the speed term is derivable in closed
  form, so evolving it would be compute for no information; #2 "error type over
  error size" — the letter's error was of the wrong *type* (a kinematic term
  mistaken for a field error); #30 "we need to build towards GR that's the goal".
- **The lens (scout) may have missed:** literature-shaped closure bias — I certified
  the coefficient and left the build untouched; the oblique-approach and
  thrust-in-doll cases were 288f's checker's, not re-measured here; the FD probe's
  exact pollution mechanism is asserted from the frame-rotation record (ψ swings
  ≈ the geometric sweep, 2.9–3.1 rad over these flybys) but not decomposed. Prior
  art marked UNVERIFIED at source: Marck/Kubižňák (parallel frames, arXiv:0811.0012
  — verified to exist); Roshan & Haidey, PRD 103, 064081 (relativistic tidal
  accelerations, moving observers — title/abstract verified only); Aichelburg–Sexl
  as the β→1 plane-wave limit (288f already states the null limit; not re-derived
  here). Ranked candidates for the instrument: (1) exact Riemann projection on a
  boosted static frame — no separation parameter, machine precision, adopted;
  (2) parallel-frame deviation ODE — needed only for histories, kept as cross-check;
  (3) Richardson FD on member geodesics — 288f's, the polluted one, now explained.

## Commands

```
cd lab/results/20261020-1729-scout-4c79
python3 instrument.py grid     # the 49-row table, controls, P6 (~0.2 s)
python3 instrument.py nonlin   # Fermi frame, deviation ODE, member congruences (~20 s)
```

Outputs preserved: `grid_output.txt`, `nonlin_output.txt`. Empty patch: no engine,
docs or gate file was touched.
