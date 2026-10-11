# Predictions (written before the optimization loop)

Artifact: the shipped per-kick path in `crates/space` — `readout -> parent tide -> bind`
(`events::handoff::bind` → `Rebinding::from_state` → `Orbit::compile` → `TubeEvent::bind`).
The plane rebinds on ~99% of kicks, so ns/kick here is ns/event for the engine's dominant event
(board bottleneck: "kicks dominate the engine's cost").

Metric: ns per kick, best of 5 × 64 kicks per scene, on the 4 tuned scenes
(weak-circle-p1e8, weak-ecc-p1e8-e0.5, strong-ecc-p1e5-e0.5, deep-ecc-p40-e0.5).
Behaviour constraint: the blake3 digest of the full TubeEvent stream (tube key, angle,
periapsis time, residual) must be unchanged, and `cargo test -p emergent-space` green.

Baseline (best of 5, load ~0.4, this machine):
weak-circle 18.6 µs/kick (bind 16.0), weak-ecc 36.1 (bind 32.0),
strong-ecc 49.8 (bind 46.0), deep-ecc 49.4 (bind 46.0).
Bind = 86–94% of the kick; compile-only = 3.5/19.2/30.5/31.0 µs (6/27/27/27 knots).
fast_quad is the quad path for all ecc scenes (q ≠ 0, delta ≥ 2^-30).

## Hypotheses for the loop

H1 (division width): fast_quad's four `u128 / u128` divisions per node have divisors that
provably fit u64 with `(n >> 64) < d`, so `num::div_word` (two native u64 divisions) returns
the identical floor. Expect compile −20–35%, kick −15–25% on the three ecc scenes.

H2 (redundant state solves in bind): `TubeEvent::bind` decodes the tube at the event time a
second time although `fit.decoded_event()` already produced the identical state (same function,
same inputs). Reusing it is bit-identical. Expect bind −5–10% on all scenes.

H3 (whatever the next profile names; likely cos/product chains or the fit's cubic bisection):
expect <10%; will revert unless it clears 10% with identical digests.

## Held-out set (not tuned on; run once at the end, `kickbench heldout`)

- p=2e8, e_q48 = 1<<45 (e≈0.97): many bands, wide apoapsis dwell
- p=1e5, e_q48 = 1<<43 (e≈0.99): extreme, near the word_root regime boundary
- p=1e7, e_q48 = 1<<46 (e≈0.5): mid weak/strong boundary (q = 2^-23.3, fast path)
- p=80, e_q48 = 1<<47: deep, mild

Predictions on the held-out set:
1. Digests identical to the baseline build on every held-out scene (the changes are
   width-equal arithmetic and dead recompute removal, both bit-identical by construction).
2. Gains track the tuned scenes: kick −10–25% where e is moderate (the same fast_quad
   division work), and smaller (<10%) on p=1e5 e0.99 if its cost shifts into the CAP/band
   structure or the fit's bisection rather than per-node arithmetic.
3. No scene gets slower by more than measurement noise (±5%); div_word only replaces
   divisions whose precondition is checked, with the u128 division kept as fallback.
