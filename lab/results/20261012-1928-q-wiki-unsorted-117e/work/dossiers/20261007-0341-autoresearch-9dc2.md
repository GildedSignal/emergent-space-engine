# dossier.md — 20261007-0341-autoresearch-9dc2

**Claim.** The plane's kick cost is not arithmetic width: a bit-identical replacement of the
quadrature's four `u128/u128` divisions by hardware 128÷64 division gains exactly 0%, because
97% of a kick is the rebind, 79% of that is the trajectory compile, and 75% of the compile is
**how many quadrature panels the EDGE band walk emits** (~70 panels and ~70 `cut`s per
bound-orbit compile, growing with eccentricity; ~150 panels per passage) — the lever is panel
count, not per-panel cycles.

**Bottleneck.** Board focus #1, "fewer kicks per orbit at the same behaviour: kicks dominate
the engine's cost" — the per-event-cost half ("cheaper events"). Expected gain if the
arithmetic hypothesis had held: ~1.3× on every kick. What the attribution deletes instead:
any future micro-optimum on `fast_quad`'s integer ops, and `isqrt`/`__udivti3` chasing
(the falsified hypothesis cost one 45-s build-and-measure cycle to kill).

**Evidence** (Linux/x86 shared runner, loadavg 0.2, 8 vCPU; spread ~1% over 3 runs;
orders of magnitude only — M1 numbers are the integrator's):

- Baseline `xtask universe --kick-bench --rtf 100 --members 400 --seconds 8`:
  4918 distinct kicks, median 83.6–84.9 µs, p99 386–390 µs, `replay_digest 14d14cd4…`,
  `digest 57c91487…`, identical across runs (the bench is deterministic).
- Phase probe (per-kick totals): rebind 787.6 ms of ~810 ms = **97%** (avg 80.9 µs, max 667 µs);
  read 2.0, ctx 3.6, field 0.4 µs. Sub-probe: `Orbit/Passage::compile` **66.5 µs = 79% of kick**
  (10,437 compiles: ~9,945 Cycles ≈ 52 µs each; 492 Passages ≈ 374 µs each — the p99).
- Compile internals: quad **776,786 panels, 457.7 ms, 0.589 µs/panel = 75%**; `cut` 774,516 ×
  0.197 µs = 25%; 74,136 knots over 492 passages. ⇒ ~70 panels per bound-orbit compile:
  `OrbitShape::append` emits ≥1 CAP panel per EDGE band, and the band count grows with
  log((1+e)/(1−e)).
- Round 1 (the decisive experiment, predictions pre-registered in `predictions.md`):
  `fast_quad`'s four wide divisions → guarded `div_word`, bit-identical by `div_word`'s tested
  contract (quotient equal whenever it fits u64; exact `(n >> 64) < d` guard, wide fallback).
  Result: digests unchanged, median 91.7–91.9 µs vs 85–91 µs baseline, `quad` avg 0.580 vs
Reproduce (each ≤ 60 s): `cargo build --release -p xtask &&`
`/home/glmlab/lab-target-2/release/xtask universe --kick-bench --rtf 100 --members 400 --seconds 8`
(baseline + digests); the probe/hdiv build is `git apply evidence/probe-and-hdiv.diff` then the
same command (adds `phases`, `subphases`, `cprobe*` fields); saved JSONs in `evidence/`
(`round1-hdiv.jsonl` is the with-change run; the three `heldout-*.json` the pristine reruns).

**Predictions.** `predictions.md` P1 (20–35% median drop) **failed** — that is the result;
P4 (digests unchanged, tests pass) **held**; P2/P3 untestable at 0% (no kept change); P5 held
(p99/median ratio unchanged). The honest miss: I predicted the divisions were the kernel; the
panel-count structure was.

**What would make it wrong.** A per-panel cost that only shows on the M1 (different divider
latency): then `hdiv` could pay there while paying 0% here — cheap to re-test by applying
`evidence/probe-and-hdiv.diff`. Also, a workload whose orbits are all near-circular (few EDGE
bands) would shrink the panel count and could re-expose arithmetic as the kernel.

**Cost of adoption.** None: nothing kept; the tree is pristine (`git status` clean except
`lab/results/`). The falsification is the deliverable.

**Fit with PRINCIPLES.** "Measure before claiming" and "the simplest falsifying test first":
the cheapest kill of the arithmetic hypothesis ran first and killed it. "A failed experiment
kills that configuration, never the method" — the configuration (wide-division micro-optimum
on `fast_quad`) is dead; the method (digest-locked autoresearch on the kick bench) worked,
with ~1% measurement spread and exact digest locks. Via negativa: nothing adopted, nothing
left behind.

**The lens.** Autoresearch optimizes what exists; the real lever it found is structural —
`append` must not pay one panel per EDGE band for eccentric orbits (a shape-table change that
alters knots, hence NOT bit-identical: it belongs to the encounters/cadence line, judged by
behaviour gates, not by this digest lock). The next rung should size that: panels per compile
as a function of e, against the G-gates.

**Grade sought:** lead (nothing adopted; one configuration killed with tight attribution and
a re-appliable instrument).
