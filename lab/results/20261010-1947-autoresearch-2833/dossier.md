# Dossier — kick resolver: cache what the binding already knows

## Claim

Caching the tube's proper-time readout at its event on the `Binding` (and letting
`orbit_state` skip the integer word it never asked for) cuts the plane's pure kick
resolution by **9–10%** (45.6 → 41.1 µs median, seed 1) with **bit-identical outputs**
on every held-out case and the whole `emergent-space`/`emergent-universe` test suite green.

## Bottleneck

Board focus #1: "fewer kicks per orbit … kicks dominate the engine's cost". The metric
the lens pinned: `universe --kick-bench` `kick_us` median (pure resolver, replayed plane
kicks, digest-checked). Baseline on this box (21 reps): 45.59 / 44.88 / 44.12 µs (seeds 1/2/3).

Phase profile (temporary instrumentation, then reverted): per kick, `rebind` is ≈ 2/3 —
tau readout 9.6 µs (**two** full `orbit_state` decodes, one of them at a *fixed* tick),
fit_key 6.4, cycle compile 7.5, residual decode 5.2, at_radius 1.6; outside: readout 5.3,
secondaries 3.7, force 6.5.

## Evidence

Commands (each ≤ 60 s; Linux x86, orders of magnitude only):

```
cargo build --release -p xtask
python3 lab/results/20261010-1947-autoresearch-2833/measure.py 21   # seeds 1,2,3 × 21 reps
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 6 --seed 1
$CARGO_TARGET_DIR/release/xtask universe --describe | md5sum
cargo test --release -p emergent-space -p emergent-universe
```

| config | seed 1 | seed 2 (held out) | seed 3 (held out) | seconds 6 (held out) |
|---|---|---|---|---|
| baseline | 45.59 | 44.88 | 44.12 | 44.65 |
| + both changes | 41.12 | 40.63 | 39.98 | 41.30 |
| Δ | **−9.8%** | **−9.5%** | **−9.4%** | **−7.5%** |

- Digests identical everywhere: seed 1 `971e97d7…`, seed 2 `3dfe2862…`, seed 3
  `d9d33790…`, seconds-6 `293fceb4…`; `--describe` md5 `3d04f87d…` unchanged (A/B on a
  stashed clean tree).
- Tests: 74 passed, 0 failed (`emergent-space` + `emergent-universe`).
- Patch: `kick-cache.patch` in this folder (three files: `bind.rs`, `step.rs`, `universe.rs`).

The two kept changes:

1. **`proper_at_event: Scalar` on `Binding`.** `rebind`'s clock reading recomputed
   `old.orbit_state(old.event_time)` every kick — but that value is fixed for the
   binding's life, and `bind_in` had already computed it (`Bound.orbit`); every
   constructor now stores it. `bind_exact` gains one decode at creation (rare path) and
   becomes fallible (`Res<Binding>`, two call sites).
2. **`decode_orbit`.** `orbit_state` ran the full `decode`, built the integer word
   (`cartesian`), and threw it away (`.1`); the state-only path skips it.

## Predictions

`predictions.md` was written before the decisive runs. P1 (8–12%) **held** (−9.4 to −10.3%
with change 2). P2 (allocation reserve in the compile, 1–2 µs) was **not measurable** at
this protocol's ~4% noise floor — reverted; an unproven change is weight, not speed
(principle 1). P3 (Scalar fast path < 3%) untested, skipped on the same reasoning. P4
(~30 µs bit-identical floor): consistent with the profile — the remaining 41 µs is
fit_key + compile + forced decode + force, all load-bearing integer work. P5 held
(secondaries caching is outside the single-kick resolver this metric measures).

The loop stopped by the lens's rule: three rounds in a row gained < 10% (7.3%, ~3%, < 2%).

## What would make it wrong

Nothing in the bits: both changes only reuse values already computed from the same
inputs (digest-pinned). The *speed* claim is this box's; the integrator re-measures on
the M1. If a future law change stops `bind_in` from returning the event's orbit state,
change 1 degrades to one extra decode at creation — still correct.

## Cost of adopting, and fit

~24 net lines in three files, one field on `Binding` (a `Scalar`, 10 bytes with padding —
the law's per-body memory budget is the 16-byte tube, but the `Binding` is the resolver's
working record, not the stored state). Fit: principle 3, "compute only surprises … nothing
is evolved that can be derived when looked at" — the clock reading at a *past* event is
exactly such a derived quantity, and principle 14, "no work for no reason".

## The lens, and what it missed

Autoresearch on a working artifact finds local optima; the structural change this profile
points at is **not** more micro-caching: it is that a kick rebinds at all (0% memo hits on
distinct kicks, cycle recompile per kick ≈ 7.5 µs of the 41). The law already names the
answer (law.md line 35: exact-offset re-anchoring, ~0.05 compiles per kick) — that is the
10× lever, and it is a law change, not this run's. A blind spot of this lens: it cannot
see cross-body waste (every kick re-derives each secondary's state at the same tick); a
per-(doll, tick) secondary cache would cut the 3.7 µs `secondaries` term in *frame* cost,
invisible in single-kick `kick_us`.
