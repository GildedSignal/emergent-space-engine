# Predictions (written before the decisive sweep)

Question restated: how long does the encounters certificate's premise ("the pair's timing is
an exact integer circle rotation ... valid until a kick", law.md; `crates/encounters` models
fixed `pom`, no apsidal advance) survive the law's own compiled apsidal precession, which is
O(0.35–0.55 rad/orbit) in the strong-field scenes the law targets (B17's original scene)?

Model: each body on a uniformly precessing conic (the tube's float form: radial cycle exact,
period P = 2π/n; apsidal advance δ = Ω·P per cycle). Truth = brute-force distance minima of
the pair; certificate = the same pair with elements frozen at t = 0 (as the crate does),
proposal = predicted local minimum < 1.2·ρ (the crate's safety-scaled window). A MISS is a
true minimum < ρ with no proposal within ±0.4 synodic spacings. H = time of first miss.

Cases I did NOT tune on (controls and held-out scaling):

1. **Controls.** (a) Ω_i = Ω_j = 0 (pure Kepler): 0 misses over 100 synodic periods for
   e ∈ {0.05, 0.3, 0.7} — else the instrument is broken. (b) Equal precession Ω_i = Ω_j = 0.3
   rad/orbit (large, differential = 0): **0 misses** — a rigid rotation of the pair is an
   exact symmetry, so precession per se is harmless; only differential precession can age the
   certificate.
2. **Drift is linear, not a walk.** The per-conjunction miss prediction error |Δd| grows ∝ t
   (fit exponent 1.0 ± 0.15) and ∝ Δϖ̇ (exponent 1.0 ± 0.15): the attractor of the error is a
   slow linear drift in the pair's relative Binet angle Δϖ, not noise.
3. **Horizon.** At fixed geometry, H ∝ Δϖ̇^(−1) (fit exponent −1 ± 0.2) over ≥ 2 decades of
   Δϖ̇. Both failure modes (arc geometry drift and miss-level drift) are linear in Δϖ·t.
4. **Resonance shelf.** At fixed Δϖ̇, detuning the synodic rotation number α away from a
   small-denominator rational: the first-hit passage index l* grows ∝ 1/|α − p/q|, so the
   drift has longer to accumulate before the certificate's prediction pays; I predict H
   shrinks by ≥ 3× when |α − 5/1| ≤ 10⁻³ relative to a 10⁻² detuning. (If it instead grows,
   the drift does not couple to the shelf and the shelf is safe.)
5. **Engine translation (held-out numbers).** With the fitted constant C (H ≈ margin/(C·Δϖ̇))
   and Schwarzschild δ = 6πM/p per orbit: at p ≈ 50 M with a belt of relative width 0.1
   (Δϖ̇ ≈ 0.038 rad/orbit) I predict H < 10³ orbits, i.e. forced per-pair re-setup in the
   strong field unless sections are cut in the pair's co-precessing frame; at the weak-field
   B12–B14 scene (p ≈ 5×10⁸ M) H ≥ 10⁷ orbits (irrelevant there).

Kill criteria: if prediction 1b fails, precession per se breaks the certificate (a stronger
kill than claimed). If 3 fails (H ∝ Δϖ̇^−1 ± 0.2), the aging mechanism is not the linear Binet
drift and this dossier reports the measured law instead of the story above.
