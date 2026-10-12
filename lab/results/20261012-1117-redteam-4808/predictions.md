# Predictions (written before the decisive runs)

Cases here are NOT tuned on; they are the held-out corner the rungs never sampled.

## P1 — Binet band stitching at e > 0.7 (premise 2)

r1's seeds are e ∈ [0, 0.7], p ≥ 6.5 + 2e (H0205). Held-out cases: p = 10 fixed
(safely bound), e ∈ {0.8, 0.9, 0.95, 0.98}. m = 16, M = G = c = 1, float64.

Prediction: precession relative error |Δφ_band − Δφ_GR|/Δφ_GR stays ≤ 1% at e = 0.8
but exceeds the 1% r1 bar somewhere in e ∈ [0.9, 0.98], growing roughly with the
periapsis band-sweep density. I predict error(e=0.98) is between 3× and 30× the
e = 0.5 error.

## P2 — multiply-add cycle updates near the separatrix (premise 3)

A cycle stores (Δφ, Δt, Δτ) and first derivatives; a kick updates it by one
multiply-add. Kepler/1PN: Δt ∝ (−2E)^{−3/2}, so ∂Δt/∂E ∝ (−E)^{−5/2} ∝ (1−e²)^{−5/2}.

Prediction (dimensionless gain g = |∂Δt/∂E|·|E|/Δt):
- e = 0.5: g ≈ 3
- e = 0.9: g ≈ 10²
- e = 0.99: g ≥ 10⁴ (formally g = (3/2)·2 /(1−e²)^{... } — grows ≈ (1−e²)^{−2} at
  fixed a; at e=0.99 that is ≈ 2.5·10⁻³⁻² ≈ 7.5·10³)

Prediction (truncation error, first-order vs exact Δt after one kick δE/|E| = 10⁻⁵):
- e = 0.5: relative error < 10⁻¹¹ (harmless)
- e = 0.95: relative error > 10⁻⁸ AND systematic (same sign every kick), so over
  10³ kicks the accumulated phase drift exceeds 10⁻⁵ cycles — i.e. the error per
  event is amplified by g, violating the design's "at most one floor unit per
  event, never compounds" budget, because one quantum of E error enters phase as
  g quanta.

## P3 — "each visible tube crosses the observer's past light cone once" (premise 5)

Emitter on a circular orbit (period P), observer flying by at β, Doppler factor
k = √((1+β)/(1−β)). One frame = 1/60 s observer time = k/60 s emitter time.
Prediction: number of past-light-cone crossings of the emitter's tube per frame
exceeds 1 once k·P < 2·frame (i.e. apparent orbit faster than ~2 revolutions per
frame at the screen's sampling): at β = 0.995 (k ≈ 20) and P = 0.1 s I expect
≥ 2 roots per frame routinely, so "crosses once" fails and the Newton seed from
the previous frame tracks a root that can vanish (caustic) → pops.

## What would make me wrong

P1: if band stitching passes 1% at all e < 0.99, premise 2 holds to the edge.
P2: if g stays < 10² or the truncation error is not systematic, the budget survives.
P3: if roots per frame stay = 1 at k·P spanning a full orbit, the gather holds.
