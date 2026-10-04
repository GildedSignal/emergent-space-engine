# Predictions (written before the decisive experiment)

Context: `crates/space` ships `ShapeMemo` (exact shape key), `QuantizedMemo`/`MemoCode` (12+12-bit
quantized key, built for "the measured population path"), and `law.md` declares tubes keyed by
**quantized** (E, L) with the remainder carried. The plane's kick path
(`crates/universe` `Work::kick` → `bind` → `Rebinding::from_state` → `Orbit::compile`/`Passage::compile`)
refits the exact key and recompiles the quadrature shape on **every** kick, and uses none of the
memo machinery. Baseline on this container: kick median 40.4 µs, p99 66.9 µs
(`xtask universe --kick-bench --seed 7 --seconds 4`; 23 samples; 0 refusals).

## Held-out cases (not tuned on)

A stream of bound-orbit states (planet-like and ship-like keys in the plane's scales), each state
perturbed by a small velocity kick (relative sizes 2⁻²⁴…2⁻¹⁶ of local speed, 64 kicks per radial
cycle — the law's own cadence), plus one near-circular case and one eccentric case e = 0.6:

- **P1 (hit rate).** ≥ 90% of kicks leave the 12+12-bit `MemoCode` unchanged on the planet-like
  stream (weak field: shape collapses to the weak branch). I have NOT tuned on the eccentric
  strong-field stream; there I expect ≥ 50%.
- **P2 (cost split).** The rebind's cost is dominated by the compile (quadrature `OrbitShape::bound`),
  not the algebraic fit (`fit_key`): compile ≥ 50% of `Rebinding::from_state`.
- **P3 (memo cutover).** Replacing `Orbit::compile(key)` with `QuantizedMemo::get(key)` inside the
  same rebind (fit and residual bookkeeping unchanged, so the bound state stays bit-exact at the
  event by the remainder construction) cuts the rebind's median cost ≥ 10× on the same stream.
- **P4 (residual bound).** With the quantized memo, the fit residual stays bounded: no residual
  grows beyond O(one key quantum) over 10⁴ kicks with rebind-on-code-change (no drift term).
  If this fails, the cutover changes error *type*, and I report it held-failed.
- **P5 (blind-spot case, expected to hold badly).** Passages (unbound flybys, e ≥ 1) and
  near-parabolic keys: `MemoCode::encode` refuses non-periodic keys, so the memo cutover cannot
  help doll-crossing flybys at all — that population keeps paying full compile. I predict the
  periodic fraction of the plane's own kick replays is < 100% but > 80%.

## What would make the claim wrong

- Hit rates near 0% (kicks always move the quantized key): the memo is not a kick mechanism, and
  the 15 µs is irreducible without changing the law's bits.
- Residual growth under the quantized memo (P4 fails with a drift): error type degrades from
  bounded to random walk → the cutover is a bandaid, and I kill it myself.
