# Predictions (written before the decisive held-out runs)

Tuning instrument: `universe --kick-bench --rtf 10 --seconds 30 --seed 1` (median leaver kick 120–121 µs, digest `adc434a4…`).

The change: `OrbitShape::node()` (crates/space/src/orbit.rs) computes `cos(psi)` at its head, then calls `self.x(psi)` for the time component, which recomputes the same `cos(psi)` on the same `psi`. The change uses the already-computed `x` (identical i128 value, same bits) instead of `self.x(psi)`. It touches only the *general* quadrature path (11,861 of 117,809 panel integrations in the tuning run; the weak path takes 90%, the fast path 0%). It cannot change any output bit: `x(psi) == k + product(ONE-k, cos(psi)) == x` by construction.

## Held-out cases (not tuned on)

1. `--seed 2 --rtf 10 --seconds 30`
2. `--seed 7 --rtf 100 --seconds 55` (the player's flight speed)
3. `--seed 1 --rtf 1 --seconds 30` (real time)

## Predictions

- **P1 (digests):** every held-out digest is unchanged from the same run on the unmodified tree. The resolver is bit-identical. Any digest change is a KILL of the change, not a measurement.
- **P2 (gain, size):** the gain is small and confined to passage-heavy workloads. The duplicate `cos` is ~25 ns of a ~380 µs `Passage::compile`, 60 calls of 555 kicks: I predict **≤ 2%** on the leaver median at rtf 10 (passages are ~36% of kick time there; one cos of four nodes per panel of the general path). At rtf 100 (more, faster members) the passage share is higher, so the gain may reach 2–3%; at rtf 1 passages are rarer and the gain may vanish (< 0.5%).
- **P3 (no regressions):** `cargo test -p emergent-space` and `-p emergent-universe` stay green (the change is a pure substitution of an equal value).
- **P4 (the loop's honest stop):** with the attribution measured — rebind 87% of kick time; within it `OrbitShape` quadrature 57% and `Passage::compile` 36% of total kick time; kernels (`cos`, `atan`, `isqrt`, `div_word`) already on u64/u128 fast paths — no *micro* change I can see reaches 10% on this bench. The structural lever the data names is the number of compiles (shape memo hits 0% exact; the quantized memo would hit 83–94% but changes orbits — a law change, out of bounds for autoresearch). So I predict the loop stops after this round with a sub-10% gain, and the useful output is the attribution, not the patch.
