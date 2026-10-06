# Dossier — 20261006-0737-autoresearch-8d6e

**Claim.** On the plane's own kick replay, the kick's median cost is bound by secondary tube readouts
(~10 × 3.2 µs) plus a 13–25 µs cycle rebind, while the p99 tail is passage rebinds whose
`Passage::compile` costs 330–2000 µs, scales with log₂(doll-edge/periapsis), and consumes 86% of all
rebind microseconds at 19% of rebind calls; the one bit-identical arithmetic lever found
(`div_word` for `fast_quad`'s wide divisions, proven output-identical) is below the lab machine's
noise floor, so nothing is adopted.

**Bottleneck.** Board item "a kick costs 29 µs, 15 in rebinding fit and compile" (plane bottleneck 3).
Expected gain of the *structural* fix named below: 10× on the kick tail (p99), which is the
smoothness number Julien gates on ("i care about the p95/99"). What it deletes: most of the
~500–1500 quadrature panels per passage rebind.

**Evidence.** All commands ≤ 60 s unless noted; CARGO_TARGET_DIR=/home/glmlab/lab-target-4.
- Baseline bench: `xtask universe --kick-bench --seconds 15 --seed 1` → median 45.4 µs, p99 61 µs,
  replay_digest 50b705f1…; `--seconds 55 --seed 3` → median 46.7, p99 908 µs, memo exact_hit 0%.
- Dump of the plane's own `bind` inputs (env-gated hook, off by default, 14 lines in
  `crates/universe/src/bind.rs`): `KICK_DUMP=/tmp/d.jsonl xtask universe --kick-bench --seconds 55 --seed 1`
  → 72 inputs, 14 passages.
- Replay harness (this folder, `prof/`): `cargo run --release -- /tmp/d.jsonl 300`
  → per-input bind/readout/compile times; passages 330–2022 µs (compile 307–658), cycles 13–146 µs
  (compile ≈ 0.57 µs/knot), cycle readout 3.2 µs, passage readout 7.3 µs.
- Division micro-bench: `cargo run --release --bin divbench` (in `prof/`) → u128/u128 23.8 ns,
  `div_word` 18.1 ns (1.32×).
- Bit-identity of the reverted swap: replay `output_hash` 95fafd8590f8f8ee before = after, all 72
  inputs; bench digest unchanged after revert.

**Predictions.** `predictions.md` was written before the decisive run. P4 (digests identical) held;
P1 (passage compile −8–18%) could not be resolved: repeat runs of the *unchanged* binary moved
20–50% (co-tenant load on the shared runner), wider than the effect. P2 (<5% on cycles) consistent
with measurement. P3 untested — the swap was reverted before a bench A/B, per the pre-written kill
criterion. Held-out seeds: 1, 3 benched; 2 not reached (time).

**What would make it wrong.** The attribution rides one 55 s seed-1 dump (72 binds) plus seed-3
percentiles; a scene with no deep passages (no fleet hand-outs) would not show the tail, and the
median split (readouts vs bind) is inferred from part-times, not a forced regression. If the M1's
division latencies differ enough, the `div_word` swap could clear 10% there — the lab cannot see it.

**Cost of adoption / fit.** Nothing adopted. The `div_word` swap is safe (hash-proven identical),
3 lines, and may be worth taking on the M1 where the integrator re-measures; the dump hook is
measurement scaffolding for reproducing this attribution. PRINCIPLES fit: "Compute only surprises"
and "Errors never compound" — both paths keep integer outputs bit-identical; "Measure before
claiming" — the gain was not claimable on this machine, so it was not claimed.

**Lens.** Autoresearch found a local optimum's map, not a win: the structural change that beats it —
compile passages out to a trajectory-relative radius (or tier them by log₂(endpoint)) instead of the
doll constant `2·edge` — changes bindings, i.e. it is a law decision (docs/law.md, the changeover
question), not this run's to make. Second structural lever for the median: the ~10 secondary
readouts per kick are re-solved from scratch per body; a per-frame shared readout at equal `t`
(same integers, engine-level cache with application-triggered invalidation) would cut the median
roughly with the number of kicks sharing a tick — an engine question, flagged for the plane's
next step, not attempted here.
