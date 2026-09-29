# Predictions (written before the decisive run)

Mechanism chosen (stated): first-order sigma-delta. Per quantity, per body: one shared
exponent (block floating point) and two registers — a value word and a carry word — which
together are one 2w-bit fixed-point accumulator at unit F = q·2^(1−w). For the increments
(Δφ, Δt, Δτ, constant per body) the pair holds the increment once and the wide per-body
phase counter advances by exact integer adds; for E and L the pair accumulates the kick
stream, inputs gridded at F with round-half-even. trunc/round16 store a single w-bit word
at q, no carry.

Ex-ante expectations on the held-out cases (I have not run them):

1. **sd32 increments are exact.** A float64 increment has ≤ 53 significant bits; a 32+32
   pair with a power-of-two exponent aligned to the value holds it exactly. So
   phase_error_growth_exponent = 0 exactly (error identically 0, not just flat), and
   conjunction orders match the reference exactly at every width ≥ 32 (fraction 1.0).
2. **sd24 and sd16 phase walks linearly.** The 2w-bit pair truncates the float64
   generator; the residue is a constant per body, so |φ_stored − φ_true| = N·ρ exactly
   linear: fitted exponent ≈ 1.0 for both. Magnitudes: sd24 ≲ 10⁻⁸ rad over 10⁶ cycles
   (invisible, wrong type); sd16 ≈ 10⁻³ rad.
3. **Conjunction order:** sd16 has Ω relative error ~2·2^(1−2·16) ≈ 10⁻⁹; conjunction
   times drift ~10⁻⁵ synodic periods by the end. I expect at least a few of the 64 pairs
   to flip an adjacent (conjunction, periapsis) pair, so sd16 fraction < 1.0. sd24 ≈ 10⁻¹⁴
   relative: fraction 1.0. trunc/round16 (~3×10⁻⁵ relative): many flips, fraction ≪ 1.
4. **Kick drift survives at every SD width** (bounded/quantization-residual error ≪ 1% of
   the 10⁻² secular change): sd16/24/32 pass; trunc16 and round16 lose every kick below
   the 16-bit LSB (all of them: max kick ≈ 0.03 LSB), ΔE = 0, fail.
5. **Kick residual is the open question.** The float64 kick stream carries ~85 bits of
   information per accumulated value; the 2w-bit pair cannot grid it exactly at any tested
   width. I expect |stored − reference| to grow as a random walk of the input-graining
   residues: fitted exponent ≈ 0.5 for sd16, sd24 AND sd32 (magnitudes ~10⁻⁷, 10⁻¹²,
   10⁻¹⁷ of E). If so, the kickgrow ≤ 0.2 criterion kills every configuration under this
   accounting, and the only mechanism that could pass it is kicks gridded at the source
   (integer kicks on the pair's grid, as the engine's cells would deliver them) — I will
   run that variant as a diagnostic, not as the canonical truth.
6. **Negative controls** trunc16/round16 fail phase (exponent ≈ 1.0, error up to ~30 rad),
   conjunction order, drift, and kick residual (linear, exponent ≈ 1.0).

Predicted verdict: negatives killed as required; sd32 passes phase/order/drift/bits and
fails only kickgrow if prediction 5 holds; sd16/sd24 fail phase (type: linear walk) and
kickgrow. The width answer splits: 32 bits for exactness; the kick gate unpassable by any
width against a float64 stream.
