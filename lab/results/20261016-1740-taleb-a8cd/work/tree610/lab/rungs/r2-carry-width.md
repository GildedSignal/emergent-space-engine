# Rung r2: how narrow stored numbers can be, with noise-shaped carries

Frozen by the integrator on 29 September 2026, before any run. Design: [docs/representation.md](../../docs/representation.md) §4.

**Question.** A memoized orbit advances by constant increments each cycle: Δφ, Δt, Δτ. Tidal kicks nudge the invariants E and L. How few bits can these be stored in, as integers with sigma-delta (error-feedback) carries, while behaviours stay right over long runs?

**Truth.** The increments are those of the Schwarzschild oracle: `periapsis_elliptic` and `bound_period_quad`, ported from `xtask/src/gr_oracle*.rs`. Each is scaled so that its stored integer uses the configuration's width, with a shared per-quantity exponent (block floating point). Kicks are a stream of small signed nudges to E and L. Their magnitudes are drawn log-uniform between 10⁻¹⁰ and 10⁻⁶ of the value; their signs are biased so that the true secular drift is +10⁻⁸ per kick. The reference is float64 with exact summation (`math.fsum`).

**Configurations.**
- `sd16`, `sd24`, `sd32`: integer storage at 16, 24 or 32 bits. Each accumulated quantity keeps a sigma-delta carry of the same width; the author chooses first order or second order and states which.
- `trunc16` (negative): 16 bits, truncation, no carry. It must fail.
- `round16` (negative): 16 bits, round-to-nearest, no carry. It must fail.

**Cases** (sampler: Python `random.Random(20261001)`).
- **Phase runs:** 64 seeds with p log-uniform in [10, 1000] and e uniform in [0, 0.7], each advanced 10⁶ cycles.
- **Conjunctions:** 64 pairs of bodies whose periods differ by a factor log-uniform in [10⁻⁶, 10⁻²]. Over 10⁴ synodic periods, record the order of their conjunctions.
- **Kick runs:** 64 seeds, each with 10⁶ kicks.

**Metrics,** one set per configuration:
- `phase_error_growth_exponent`: the worst seed's fitted exponent of |φ_stored − φ_true| against cycle count, over log-spaced windows on the last 90%.
- `conjunction_order_fraction`: the fraction of pairs whose conjunction order matches the reference exactly.
- `kick_drift_pass_fraction`: the fraction of kick runs whose accumulated secular change in E and in L is within 1% of the reference change.
- `kick_residual_growth_exponent`: the worst seed's growth exponent of |stored − reference| for E and L.
- `bits_per_body`: stored bits for (Δφ, Δt, Δτ, E, L) plus their carries.

**Output.** `metrics.json`, plus one picture: phase error against cycles on log–log axes, one curve per configuration.

```configs
sd16 candidate
sd24 candidate
sd32 candidate
trunc16 negative
round16 negative
```

```criteria
phase type phase_error_growth_exponent <= 0.2
order behaviour conjunction_order_fraction >= 1.0
drift behaviour kick_drift_pass_fraction >= 0.99
kickgrow type kick_residual_growth_exponent <= 0.2
bits cost bits_per_body <= 320
```
