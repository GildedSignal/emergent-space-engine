# Predictions (held out before the decisive run) — run 20261010-0920-scout-e5f5

Question: does gravity-as-news stay O(surprise) in work and memory at fixed density, and does
quantum-gated cell accumulation (principle 6 applied to news) hold the deferral error below the
receiver quantum?

Toy: 2D disk, surface density σ = 1 body/unit², c = 1. News events = Poisson, λ = 1 per body per
time unit (r8 measured 1.1 real events per body per orbit), strengths log-uniform [0.005, 0.5]
(mean ≈ 0.07). Receiver quantum q = 0.01 (finer control q = 0.001). Leaf cells k = 16 bodies.
Schemes: **naive** (every body processes every news front when its light cone arrives — R5's
cursor taken literally), **gated** (direct delivery within r_q = √(s/q); beyond, strengths
accumulate in nested-cell accumulators that flush as one aggregated news when the pending field
at the nearest receiver would cross q), **drop** (negative control: sub-quantum news discarded).

## Cost (analytic layer + patch MC validation)

1. Naive: deliveries per news event = N (fitted exponent 1.0 in N at fixed density); total
   ∝ N². This is the positive control for the cost instrument — if the instrument does not read
   exponent 1.0, VOID.
2. Gated: deliveries per news event at fixed density = O(1) (direct ring) + emission annuluses;
   per-body per-time work = (3π/4)·λ·s̄/(q·k)·log₄ N ≈ 6 delivery-units per body per time at
   N = 10⁶ (q = 0.01), against naive λN = 10⁶. **Prediction: gated/naive ratio ≥ 10⁵ at N = 10⁶;
   gated total-work exponent ≤ 1.05 in N (linear because news ∝ N), per-event exponent ≤ 0.3.**
   KILL gated if per-event work exponent > 0.3.
3. Coherent-fleet adversarial case (K = 10⁴ simultaneous news in one region, N = 10⁶): naive
   pays K·N = 10¹⁰ deliveries; gated pays O(K + aggregated emissions), independent of N beyond
   the aggregate's own news radius. **Prediction: ≥ 10³× cheaper.**

## Memory (analytic)

4. Naive in-flight fronts per body at fixed density ∝ √N (the growing light cone made concrete:
   each front lives up to 2R, R = √(N/π)). **Prediction: exponent 0.5.** R5's literal
   (body, source) cursors are N² words — reported, not simulated (10¹⁸ at 10⁹ bodies).
5. Gated: accumulators = (4/3)/k words per body ≈ 0.083 (k = 16), plus in-flight aggregated
   fronts. **Prediction: exponent ≈ 0 in N for accumulators; in-flight aggregated fronts
   per body ∝ 1/√N (frontier length R against N bodies) — total in-flight ∝ R, the honest
   residue of Julien's "there will always be a point where we cannot handle the universe".**

## Error type (patch MC, exact sequential routing, exact all-fronts reference)

6. Gated deferral error |a_gated − a_exact| at receivers ≤ L·q worst case (L = hierarchy levels
   ≈ 6 in the patch; each un-flushed accumulator contributes < q by the flush rule), typically
   ≪ q. **Prediction: max ≤ 6q at every sampled time; no growth in t.** KILL gated if max > 6q
   or grows with t.
7. Drop control: error grows ∝ t (news discarded, not deferred). **Prediction: exceeds 6q by
   T = 6 and keeps growing; at q = 0.001 it grows ~10× faster.** If drop also stays bounded at
   both quanta, the "accumulation is load-bearing" claim dies at these parameters.
8. Smoothness: per-body deliveries per time bin, gated: **p99/median ≤ 10.** Flag (not kill)
   if > 100.

## What I did not tune on

Exponents, the error bound, the fleet case, and the drop control are all stated before the
first run of the decisive configurations. The closed form (3π/4)·λ·s̄/(q·k)·log₄ N was derived
before the patch MC; if MC and closed form disagree by more than ~2×, the analytic layer is
wrong and I report it.
