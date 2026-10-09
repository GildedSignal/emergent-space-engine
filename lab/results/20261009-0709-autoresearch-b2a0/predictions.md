# predictions — run 20261009-0709-autoresearch-b2a0

Written before the first optimization lands. Baseline (tune set, this Linux box):
median 7.07 µs, p90 94.6 µs, max 132 µs per `Orbit::compile`; ~93% of instrumented
time is the panel quadrature (~766 ns/panel), cuts are ~7%.

Held-out set (never tuned on): p_exp ∈ {3,5,9,13,17,21} × e ∈ {0, 0.003, 0.05, 0.2, 0.35, 0.65, 0.8, 0.95, 0.99}.

Predictions:

1. **P1 (H1, word divisions in `fast_quad`):** the four u128/u128 software divisions
   per node dominate strong-field panels. Replacing them with the exact 128/64 word
   division (guarded fallback) keeps every bit identical and cuts strong-key compile
   time (p_exp ≤ 17) by ≥ 25%. Held-out strong keys (p_exp 3,5,9,13,17) gain the
   same fraction; weak keys (p_exp 21) gain ~0.
2. **P2 (H2, cut cost):** band cuts (`ratio_sqrt` = 126-bit isqrt + i128 division,
   `atan`) are per-band overhead; halving their cost moves total compile time by
   < 10% on high-e keys (they are 7% today), so H2 is expected to be a revert-or-
   minor candidate unless H1 makes panels so cheap that cuts exceed ~25%.
3. **P3 (tail shape):** compile cost at fixed e grows ~linearly in band count
   (log apoapsis/periapsis ratio); no change I plan affects the count, so the max/median
   ratio (~19×) stays within ±20% after H1.
4. **P4 (fingerprint):** every kept change leaves the 64-bit output fingerprint
   `f4bd77fc76c8b072` (tune) and the held-out fingerprint identical; any change that
   does not is reverted regardless of speed.
