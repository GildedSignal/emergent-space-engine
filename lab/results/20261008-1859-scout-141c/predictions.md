# Predictions — 20261008-1859-scout-141c (written before the decisive run)

Question: how does the arrival rate of *distinguishable* news (force changes ≥ one quantum Q)
at one body grow with the light-cone radius R, for (a) the naive per-source cursor channel,
(b) the quantized+shell-aggregated channel?

All derived analytically on 8 October, before any sweep. Units G = c = 1; sources on Keplerian
orbits a^{-3/2}; surface density ρ fixed as R grows (the board's fixed-distribution scaling risk).

**Tuned case (calibration, smooth uniform disk, no events):**
- P1. Naive per-source channel: ν(R) converges as R grows (α ≈ 0 with a large constant), because
  per-source change rate ∝ Ω/a² ∝ a^{-7/2} and shells contribute ∫a^{-5/2}da. The constant is
  dominated by the innermost radii. This case does NOT separate the channels by exponent — smooth
  motion is what generators compile away; it is here to calibrate the harness (both channels finite,
  aggregate ≪ naive in absolute rate because shell vector sums cancel to the fluctuation dipole).

**Decisive case (Poisson surprise events, size s(a) = Gδ/a², rate λ per source):**
- P2. Naive channel (every event delivered as it crosses the cone): ν ∝ number of sources inside R
  ⇒ ν(R) ∝ R². Exponent α ≈ 2 over the top decade.
- P3. Quantum+aggregate channel (events with s < Q accumulate per log shell; a shell fires one
  arrival when its accumulator crosses Q): per-shell arrival rate = λ·N_shell·s_shell/Q, and
  N_shell·s_shell is radius-independent for multiplicative shells (N ∝ a², s ∝ a^{-2}) ⇒
  ν(R) = c₀ + c₁·(#shells) = c₀ + c₁·log₂(R/r_cut). Exponent α ≈ 0 over any decade; ν grows
  linearly in the shell count (factor 2 in R ⇒ +1 shell ⇒ additive constant).
- P4. The crossover radius r_cut = √(Gδ/Q) is where individual delivery stops; sweeping Q by
  10× moves r_cut by √10 and shifts the quantum channel's absolute rate by ~10× (accumulator
  fires 10× less often) but leaves BOTH exponents unchanged. If the quantum channel's exponent
  moves with Q, the aggregation is leaking (prediction fails).

**Held-out cases (not tuned on):**
- P5. Rare cataclysms (event size ≥ Q at all radii, total rate Λ over the disk): add ~Λ to both
  channels; bounded by the universe's own rate, independent of R. The naive channel stays α ≈ 2
  from the small events.
- P6. Coherent lopsided (m=1) disk, pattern speed Ω_p constant, amplitude per shell ∝ da/a:
  the aggregate field amplitude at the observer grows ∝ ln R, so its quantized TV rate grows
  ∝ ln R even in the aggregate channel. The log is a real physical channel (a lopsided universe
  pulls harder the bigger it is), not an artifact of the naive representation.

**What would kill the premise:** if the quantized+aggregated arrival rate in the decisive case
grows with a positive exponent in R (α > 0.5 over the top decade), aggregation does not bound
the news channel and the light-cone risk is a wall, not a budget choice.

**Game-scale Fermi (from the law, to be checked in the dossier):** ln(R_galaxy/r₀) ≈ 20–25
shell channels per direction; channels must be owned by cells (≈10⁷ cells × ~22 × 8 B ≈ 1.8 GB),
never per body (10⁹ × 22 × 8 B ≈ 176 GB > 8 GB).
