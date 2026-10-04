# Predictions (written before the decisive run)

Model: planar circular restricted three-body problem, parent fixed at origin (mass 1),
secondary mass μ on a circular orbit of radius 1, n = sqrt(1+μ). Test bodies at
a/a_sec ∈ [0.30, 0.85], e ∈ {0, 0.05, 0.20}, phases spread. RK4, 128 steps per body
orbit, tangent vector renormalized every 8 steps. FTLE λ from 200 body orbits
(λ reported per body orbit: λ·P). Cases I did NOT tune on: μ = 0.05 and μ = 0.10
(binary-doll regime), the e = 0 web, and the μ-scaling exponent.

## P1 — resonance web positions
Peaks of the FTLE field sit at the interior mean-motion resonances (p+q):p,
a/a_sec = (p/(p+q))^{2/3}: 2:1 → 0.630, 3:2 → 0.763, 4:3 → 0.825, 3:1 → 0.481,
5:3 → 0.654, 4:1 → 0.397, 5:4 → 0.878. Predicted within ±0.01 in a/a_sec.

## P2 — the web needs eccentricity
At e = 0, eccentricity-type resonances vanish: the FTLE field is at the floor
(λ·P < 10⁻⁴) everywhere outside the immediate Hill zone (a/a_sec > 0.95).
At e = 0.05 the first-order (q=1) web appears; at e = 0.20 second-order and
overlap widen it. Chaotic fraction (λ·P > 10⁻³ over 200 orbits) at μ = 0.0123:
e = 0: under 2%; e = 0.05: 5–15%; e = 0.20: 15–35% of the a-range.

## P3 — width scaling with μ
The measure of the set {a : λ·P > 10⁻³} at e = 0.05 scales as μ^α with
α ∈ [0.4, 0.7] (first-order widths ∝ √μ give α = 0.5; Wisdom-style overlap
gives 2/3). Held-out: μ = 0.05 and 0.10 exceed 60% and 80% (the r4/r9
"one representation: the rotating binary doll" regime), extrapolating the fit.

## P4 — intermittency (the blind spot)
For bodies with mean λ·P > 10⁻³, surprise arrives in bursts: the fraction of
5-orbit windows with windowed λ·P below 10⁻⁴ (laminar duty) exceeds 50% for
at least half of those bodies. If instead λ is stationary, a fixed cadence per
body is right and only the classification matters.

## P5 — the KS floor vs the uniform schedule
Sum of positive FTLEs over a belt (the scene's information rate) is orders of
magnitude below the uniform kick schedule's implied rate: at μ = 0.0123, e = 0.05,
the surprise-informed total (full kicks only on the chaotic set, averaged
elsewhere at 1/114 the rate per H0190) is at least 10× less work than uniform
32 kicks/orbit on every body.
