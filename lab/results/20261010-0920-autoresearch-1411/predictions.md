# Predictions (written before the decisive experiments; held-out cases are never tuned on)

Artifact: `crates/lattice-event` (`EventCore`, the plane's contacts engine).
Metric: wall ns per op on fixed worlds (`examples/bench.rs`), behaviour frozen by world+log digests.

## Held-out set (`bench --heldout`; not used for any keep/revert decision)

| Case | World | Expectation |
|---|---|---|
| h-gas-mid | gas 40k, fill 0.05, vmax 64, seed 99, h=768 | ns/op drops by the same fraction as the tuning gas worlds (within 3 points); digest identical to baseline |
| h-mixed | mixed 8192, Q 512, seed 77, h=2048 | smaller relative gain (denser contacts, more batch work share); digest identical |
| h-crowded | crowded_axes 8k, Q 1024, seed 88 | gain at least as large as tuning `crowded` (prediction-dominated, zero events); digest identical |
| h-gas-hot | gas 5k, fill 0.20, Q 2048, vmax 256, seed 123, h=512 | this is the stress case for the i64 fast path: Q=2048 → reach=4096=2^12, vmax 256=2^8, so pair products stay under 2^63; prediction: fast path taken >99.9% of calls, gain holds; digest identical |

## Predictions proper

1. **Where the time is:** prediction upkeep + gather/scan carry ≥80% of wall time on all worlds; rebuild ≤5%.
2. **First hypothesis (checked i64 fast path for `hit`/`first_hit`, exact i128 fallback):** total ns/op drops ≥15% on gas/crowded/random tuning worlds; the fast path is taken >99% of predicate calls in all bench worlds (cell neighbours have |d|,|w|,reach ≤ 2^15 there).
3. **Digests:** every world's world+log digest is bit-identical to baseline after every kept change; the lattice law's own test suite still passes (`cargo test -p emergent-lattice-event` and `-p emergent-lattice` green).
4. **No gain from:** calendar sift micro-tuning (already a 4-ary heap with inline keys) — if a round shows <10% for three consecutive rounds, the loop stops there.
5. **Held-out honesty:** if any held-out digest differs, the run reports it and the change is reverted, whatever the speed.

Structural change that would beat the local optimum (blind spot): prediction currently re-scans all 3×3 neighbours on every re-predict; a per-cell "no pair can ever hit while both keep velocity and cells" certificate (miss distance vs combined drift) would delete most first_hit calls outright instead of making each one cheaper.
