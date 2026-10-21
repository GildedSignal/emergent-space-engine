# Predictions (written before the decisive two-seed flight to g = 145)

Tuning seen so far (NOT the decisive run): seed 1, N = 600 belt, g ≤ 8 — shear regime only
(span ∝ g exactly, var_due super-linear, excess64 ≈ +1.8 flat, step ledger changes on alternate
fires). The decisive run: `plane_extra` extra = 3,000 (belt 2,700, the a97f census size), seeds
1 and 2, g ≤ 145, W = 64 windows over each generation's dues, Monte-Carlo uniform floor of the
same n and W (4,000 draws).

- **P1 (the named od-4 question).** The engine's worst-window excess (maxmu64 − floor64) reaches
  the floor's p90 band or below (excess ≤ +0.25) at BOTH seeds by g ≤ 145; the frozen-step model
  (a97f) puts the floor at fire 100–120, so I predict the crossing at g ∈ [90, 130].
- **P2 (spread law).** var_due/step² grows faster than linear in g at every g (shear + growing
  step drift), local exponent β = d ln var/d ln g ∈ [1.0, 1.6] at g ≥ 40; a clean g¹ diffusion
  would read β → 1, and I predict it does NOT reach 1 by g = 145.
- **P3 (step ledger, walk vs ratchet).** The per-change |Δstep|/step grows with g (a97f read
  5×10⁻⁴ → 2.5×10⁻³ by g = 40) but saturates below 10⁻² by g = 145, and the SIGNED mean drift
  stays under 10% of drift_abs at every g ≥ 10 (no one-signed ratchet in the chained clock).
- **P4 (seed law).** Seed 2's endpoint excess ≤ seed 1's, and both end inside the floor band
  (a97f's split: seed 2 has no locked-pair part).
- **P5 (c50 endpoint).** p50 window count / mean sits in 0.93 ± 0.04 at g ≥ 120 (the uniform band).
- **P6 (span law).** span/step grows ≈ linearly in g throughout (span at g = 145 within 20% of
  g × its g = 10 rate): mixing is the within-span structure, not the span.

**Controls.** Positive: the MC floor itself (must sit at 1.35–1.45 at n = 2,700, W = 64 — the
a97f floor 1.375 is the anchor). Negative: the early shear regime must show excess64 ≥ +1.5 at
g ≤ 10 at N = 2,700 (if it does not, the instrument is blind and the run is VOID). An instrument
whose floor disagrees with 1.375 by more than ±0.05 at n = 2,700/W = 64 is miscalibrated → VOID.

**Kill criterion (pre-registered).** If P1 fails at both seeds (excess > floor p90 at g = 145),
the frozen-step floor-by-100–120 extrapolation is refuted on the shipped engine, and the 10⁹
worst-frame line may not quote Poisson windows outside the measured epoch — that becomes the
dossier's claim, and the model's decay constant is wrong by more than its stated window.
