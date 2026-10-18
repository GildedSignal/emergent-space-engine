# Predictions — the circle ratchet's deceleration law (written before the deep run)

Instrument: `crates/space/examples/circle_ratchet.rs`, the seam map (compile → sample at a
true odd-eighth phase of the orbit's own period → cartesian at the doll word →
`Rebinding::from_state` → next key) chained on shipped pub APIs. Smoke at depth 64 already
reproduces the shipped record's exact constant for e = 1e-3 at p = 2²¹ M: −1 Q48 ulp per
crossing, every crossing. Doll word: position integers at ~2⁶¹ (the bank's convention),
velocity full-word 2⁻⁶².

The smoke (depth 64) shows: circles walk k one-signed negative, first step ~−2.9×10⁵ ulps,
decaying to ~−10⁴ by n = 64; e₀ = 1e-6 walks ~−50/crossing; e₀ = 1e-3 walks −1 exactly.
Rate falls steeply with the existing deficit — the two points (deficit 1.9e6 ulps → rate
1e4; deficit 2.8e8 ulps → rate 50) are close to reciprocal.

**P1 (the law): rate = C/D.** The per-crossing rate is a decreasing function of the minted
deficit D = 2⁴⁸ − k, close to reciprocal: rate ≈ C/D. Then D(n) ≈ √(2Cn) and rate(n) ~
n^(−1/2). Falsified if the windowed rate does not fall with growing D on log-log with
slope in [−0.75, −0.35], or if rate vs D is not monotone decreasing.

**P2 (state feedback, not history):** arms started at e₀ = 1e-6 and 1e-3 lie on the same
rate(D) curve as the minted-deficit circle arm (within 2×), so the deceleration is a
function of the state (deficit), not of the crossing count. Falsified if the e₀ arms hold
their initial rates while the circle arm's rate at the same D differs by > 2×.

**P3 (w stays a fair lottery):** the cumulative w path stays within 5× of the ±√(n)·σ
envelope of its own per-crossing increments (no w ratchet), and per-crossing |Δw| stays
O(0.1–1) turns (does not narrow with depth).

**P4 (radius invariant):** max |ln(r/r₀)| < 2⁻²⁰ through the deepest arm.

**P5 (no refusals):** zero `Range`/`NoBoundOrbit` refusals on any arm at odd-eighth phases
through depth 65536.

**P6 (the class):** the circle walk is neither a bounded attractor (D converging, β = 0)
nor a linear ratchet (β = 1) but a self-arresting walk D ~ n^β with β ∈ [0.4, 0.6] —
diffusive compounding. Under P1+P2 the crossings needed for D = 1% of k's range
(2.8×10¹¹ ulps) exceed 10¹² (against the record's linear price ~7×10⁸), and the price
grows quadratically in the target deficit.

**P7 (word):** the doll-word control (position integers at ~2⁴³ instead of ~2⁶¹) keeps the
class (sign census, β) and may move C by ≤ 10×.

Kill criteria for the rung: if the windowed rate flattens (slope ≥ −0.2 over the last
decade), P1/P6 die and the record's linear pricing stands; if the rate reaches 0 and D
converges, the circle walk is a fixed-point attractor and harmless outright. Either way
the deceleration law is measured, not assumed.
