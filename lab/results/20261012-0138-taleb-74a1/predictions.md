# Predictions (held-out cases, written before running them)

Already smoke-run before this file (disclosed): truth checks (D200 = 0 contacts, T200 = 199 contacts,
cert misses none) and the n ∈ {1000, 2000, 4000} dispersed-formation scaling (phase pairs 399,623 →
1,892,762 → 7,882,639; tier pairs 49,500 → 99,000 → 198,000). Held out below, predicted before running.

1. **ULP cliff.** Tight formation, e = 0.05 shared exactly: neighbours ≈ 2–4 per body (reach ≈
   angular ≈ 1.1e-4, spacing 6e-5). Same scene with ONE body's e one representable step higher:
   shared-shape fast path dies, reach jumps to ≈ 2·(e + 2 asin(e/(1+√(1−e²)))) ≈ 0.20 rad, which
   exceeds the arc → neighbours = n(n−1)/2 exactly. Prediction: n = 500 → ~500 vs ~124,750;
   n = 2000 → ~2,000 vs ~1,999,000. Cost is discontinuous in a 1-ULP input (convexity/fragility).
2. **Panic.** `group_events` on a co-orbital group containing one hyperbolic body (e = 1.5) panics
   on `assert!(x.e < 1.0)` in `Neighbours::new` — before the tree fallback is ever tried.
3. **n = 8000 continuation.** Phase path: reach ≈ 0.6 rad ≫ arc 0.1 → ~all pairs ≈ 3.2e7 visited,
   ≈ 18–22 s wall. Tier path: 80 shells × 4,950 = 396,000 pairs, ≈ 4 s. Fitted exponent of phase
   time over n ∈ {1000, 2000, 4000, 8000}: 1.9–2.1; tier exponent ≈ 1.0–1.3.
4. **Work follows dispersion, not encounters.** n = 2000 fixed, shell spacing da ∈ {5e-4, 2e-3,
   8e-3}: neighbours roughly ∝ da (ratio ≈ 16 from 5e-4 to 8e-3) while real contacts stay 0 at every
   da. The window is sized by (n_hi − n_lo)·H/2, i.e. by frequency spread and horizon, never by
   contact structure.
5. **Safety holds** (I could not break the derivation; `reach` covers contact-time true-longitude
   separation with sound bounds, seam handled): no missed contacts on any scene here. The failure
   mode of this build is cost, not misses — except the e ≥ 1 panic, which is a crash, not a miss.
