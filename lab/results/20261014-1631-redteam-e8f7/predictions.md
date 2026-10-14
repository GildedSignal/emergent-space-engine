# Predictions (written before the decisive run)

Target premise: representation.md §1 "each doll orders events in its own far time … there is
no global clock", whose only measured-adoptable mechanism is the root-clock key (ae29/4e9c):
`key = doll tick + Σ_links sinh(ηᵢ)·(x̂ᵢ · offset)` — a **sum of per-link simultaneity shears**.
Measured: exact at depth 1 (±0.500 tick, β 0.5, P6) and at depth 2 *moon speed* (±0.49 tick).
Untested: depth 2 with both links relativistic (the handoff page's "fast grandchild" hole).

## What I expect (derived, not fitted)

For root ← doll1 (β₁ along x̂₁) ← doll2 (β₂ along v̂₂, angle θ), event at offset X_B in doll2
(t_B = 0), exact t_root from the composed Lorentz matrix:

- Key variant V1 (each link's shear at that link's own offset, the chain-tracking form):
  error = **(γ₁ − 1)·sinh(η₂)·(v̂₂·X_B)** exactly. (The γ₁ on the child's time channel is
  the one missed factor; the spatial projection term cancels.)
- Key variant V2 (shears frozen per entity, both evaluated at the grandchild offset):
  error = **[(γ₁−1)·sinh η₂ + sinh η₁·(γ₂−1)·cos θ]·(v̂₂·X_B)**.
- The t_B ≠ 0 channel: exact t_root carries γ₁γ₂·t_B; an additive key that carries the doll
  tick unscaled misses (γ₁γ₂ − 1)·t_B (33% of the tick at β₁ = β₂ = 0.5).

## Pre-registered cases (not tuned on)

1. **Controls (must pass):** β₂ = 0 → error 0 exactly (both variants, depth-1 reduction);
   depth 2 at moon speed β₂ = 10⁻⁵, β₁ = 0.5, d = 2·10³ ticks → error < 1 tick
   (reproduces the checker's ±0.49); exact-matrix oracle vs analytic V1/V2 formula → agree
   to ≤ 10⁻¹² (the oracle is validated).
2. **Kill cases (held-out regimes the game sells):**
   - player-group scale: β₁ = 0.3, β₂ = 0.3, d = 10³ ticks, θ = 90° → V1 ~ 25–50 ticks,
     V2 ~ 25–75 ticks (≥ 25× the 1-tick event granularity);
   - inspiral/binary-doll scale: β₁ = 0.5, β₂ = 0.5, θ = 0, d = 2·10³ → V1 ~ 180,
     V2 ~ 360 ticks;
   - high-γ grandchild: β₁ = 0.9, β₂ = 0.1, d = 10³ → V1 ≈ 130 ticks.
3. **Scaling law:** error/|X_B∥| is constant in d (linear in offset), and the measured
   coefficient matches the analytic form to ≤ 10⁻⁹ at every grid point.
4. **Depth 3** (β = 0.3 each, collinear-ish): strictly larger than depth 2 at the same
   terminal offset — the composition degrades monotonically with chain depth.

## Kill criterion

If any kill case shows ≥ 1 tick error while both controls hold, the additive-shear key is
falsified at depth ≥ 2 with relativistic links: the causal order of events across nested
dolls (the one queue, the light-cone partition) is broken at the 10²–10³-tick scale. If the
controls fail (depth 1 not exact, or the oracle disagrees with the analytic form), the probe
is broken and nothing is claimed.
