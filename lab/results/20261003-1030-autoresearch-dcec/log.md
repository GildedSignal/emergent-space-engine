# Autoresearch log — run 20261003-1030-autoresearch-dcec

Artifact: `crates/lattice` CPU chronon reference (`Chronon::step`). Metric: ns per
body-chronon, median of 3 (5 for close calls), tuning config
`n=100000 fill=0.1 q=1024 vmax=256 seed=1 steps=100`. Constraint on every round:
`outcome()` digests bit-identical; predicates/ops counters identical; crate tests green;
`xtask lattice-check` EQUAL vs the independent integer reference.

Baseline 486 ns/body-chronon. Section split at baseline: detect 78% of the chronon,
and inside detect the `ranges` HashMap **build** was ~34 ms of ~46 ms (100k SipHash
inserts + a fresh ~2.5 MB map every chronon); key+sort ~5 ms; the neighbour pair loop
only ~2–4 ms; advance+walls ~0.8 ms; respond ~0.8 ms.

| # | Hypothesis | Change | ns/body | Verdict |
|---|---|---|---|---|
| R1 | The per-chronon hash structures, not the physics, dominate | counting sort over linearized cell index replaces sort + `ranges` HashMap (hashed path kept as fallback) | 486 → 144 (3.4×) | KEPT (digests+predicates exact) |
| R2 | SipHash lookup per visited pair is the next tax | FxHash-style hasher for the `consumed` map (pure lookup container) | 144 → 134 (7%) | KEPT |
| R3 | Each unordered cell pair is walked twice (second visit only to be skipped) | walk each cell pair once: forward neighbours + triangular self-cell, min/max for body order (predicate symmetric) | first attempt 92 but WRONG (predicates 18.3M vs 23.5M, digest changed — cell-direction filter drops pairs whose smaller body sits forward); fixed → 110 (18%) | KEPT after fix |
| R4 | Double keying pass + empty-span walk | reuse linear keys; walk an occupied-cell list, not the span | 110 → 97.7 (11%) | KEPT |
| R5 | Per-cell div/mod + bounds checks in the 3×3 walk | ghost-ring padding: linearize over (span+2)², no bounds checks, no div/mod | 97.7 → 95.3 (2.5%) | KEPT |
| R6 | `occupied.clone()` per chronon | iterate by immutable borrow, no clone | 95.3 → 92.5 (~3%, within noise) | KEPT (also simpler) |

Stop: R5 and R6 both under 10%; the two remaining identified changes (advance/walls
fusion ~3%; an i64 fast path inside `law::hit` ~8–12%, touching the shared law) are each
under 10% or out of this run's scope. No round was tuned on any held-out case.

Held-out, run once (`heldout-final.txt`): digests identical on all five, but cold-sparse
(seed 11) regressed 0.84× against a predicted ≥3×. Diagnosis: span 7.5M > TABLE_CAP 2²²
→ hashed fallback + the new key pre-pass. Fix (on proxy `n=150000 fill=0.03 vmax=32
seed=23`, not the held-out case): cap by the measured break-even span/n ≈ 50 (cap
span ≤ 64n, hard cap 2²⁴), proxy 327 → 93 with identical digests. Held-out re-run once
(`heldout-final2.txt`): 4.7× / 2.1× / 3.5× / 4.8× / 3.0×, all digests identical.
Both held-out runs are reported; the second includes one post-miss fix.

Final tuning config: 92.5 ns/body-chronon = **5.3×**. Guards on the final code:
19/19 crate tests, `lattice-check` EQUAL (3 cases), `emergent-lattice-event` 10/10.
