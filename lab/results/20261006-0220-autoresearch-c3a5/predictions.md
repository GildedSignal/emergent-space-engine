# Predictions (written before the decisive runs)

Tuned on: seed 1 kick bench (30 s and 55 s), and one isolated leaver shape
(k = 29676364815277, weak/hyperbolic) whose ladder digest is c0192de9093e3d5b.

The change: in `OrbitShape::node`, the q == 0 weak Taylor shape takes provably
bit-identical shortcuts (sqrt(1)=1, 1/1=1, /2 = exponent shift, /1 = identity),
plus CSE of `product(ONE - k, cos)` which is computed twice per node.

Held-out cases (not tuned on) and what I expect:

1. **Kick bench, seed 7, 55 s** (a scene I never ran):
   - `kick_us_all` median drops by 25–45% (leaver passages dominate total time);
   - `kick_us` (the made population, bound weak orbits → `weak_quad`, untouched)
     changes by less than 10% (noise);
   - `kick_us_leavers` median drops by 35–50%;
   - `digest` and `replay_digest` are **bit-identical** to the same seed run on
     the unmodified tree (I will build both and compare).
2. **Full `cargo test --release -p emergent-space`**: passes, including
   `native_panels_obey_the_real_two_point_remainder_and_integer_rounding_allowance`
   and `witnessed_fit_keeps_the_full_search_key_at_kicks_and_boundaries`.
3. **`cargo test --release -p emergent-universe`** (the plane's own tests): passes.
4. Seed 1 digests unchanged from the baseline recorded in baseline.json
   (f6cff052…, replay da7430f1… for 30 s; 8283cbe3… / 989892a4… for 55 s).

If (1) digest differs or (2)/(3) fail, the run is void as a pure speedup.
