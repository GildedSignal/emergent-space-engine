# Dossier — 20261007-1334-second-20261007-1234-components-97bf-98e6

**Lens:** second author. **Parent:** `20261007-1234-components-97bf` (silver). This run does
the checker's named experiment to gold: close the overflow staleness corner, then measure a
mixed spread+storm workload in steady state at 2²⁰–2²⁴ and restate the gain per regime.

## Claim

With the overflow staleness corner fixed (staleness-aware top in `next_tick`, `deliver` and
`cascade`, ~30 lines), the bitmapped timing wheel delivers the **identical (tick, id-ascending)
stream everywhere** — 0 digest mismatches in 40+ heap/wheel pairs, including the quiet-region
workloads that silently diverged before — and in **steady state** the wheel is **2.2–2.4×
cheaper on the mixed spread+storm workload at 2²⁰–2²⁴** (2.2× at DRAM scale, 2²⁴) and
2.3–2.9× on pure spread; the **one regime where the heap wins is all-far quiet regions**
(every pending event beyond the horizon W: heap up to 2.3× faster at 2¹⁶, 1.35× at 2²⁰),
so the cost claim is now regime-bounded, not headline-bounded.

## Bottleneck

Same as the parent (PRINCIPLES #12/#14/#17: the calendar is the queue that replaces ticks;
its cost must not outcost the surprise). The parent's headline (2.2–4.5×) was storm-specific
and its correctness had a hole exactly where the lens looked away; both are closed here.

## Evidence

Binary: `work/calendar-bench` (parent's bench + this run's additions: the staleness fix,
cases E/F/S, a `corner` mode, and a warmup argument for steady-state timing; build:
`cd work/calendar-bench && cargo build --release`, binary at `$CARGO_TARGET_DIR/release/calendar-bench`).
Machine state in `results/machine.txt` (8 vCPU cloud box, shared, load 0.5–1.5 during the
sweep; floors on this box: seq 2.12 ns, chain 2.70 ns — orders match the parent's box).

**Correctness, before → after** (`results/prefix-failures.txt`, all commands inline there):

```
B=$CARGO_TARGET_DIR/release/calendar-bench
$B A 1 1 1 corner x          # pre-fix: FAIL wheel_next 3145728 vs heap 4194304; post-fix: OK
$B F 2 7 100000 diff x       # pre-fix: DIVERGE step 4 (wheel empty, stale overflow top)
$B F 16 7 100000 diff x      # pre-fix: DIVERGE step 39780; post-fix: all OK
for c in A B C D E F S; do for n in 4096 16384; do for s in 1 3 7; do $B $c $n $s 50000 diff x; done; done; done   # all OK post-fix
$B S 1048576 1 300000 diff x # OK (long sparse)
```

**The record regenerates** (the fix changes no path the old code got right; P3):
`A 262144 2 500000 clean heap|wheel` → digest 17500833722892154388, sets 499385 (stored row:
same); `C 4194304 1 500000 clean` → 9112003053027925743 / 498543 (same); `A 16777216 2 500000
clean` → 14321985119129707386 / sets 1 (same). The parent's `caseA-soa.jsonl` (checker: not
regenerable by any shipped mode) is not carried into this run's record.

**Steady-state sweep** (`results/steady.jsonl`; warmup deliveries before the clock, then ≥1M
measured; medians over seeds 1–3; heap/wheel digest pairs all match at equal stream length):

```
for s in 1 2 3; do for lg in 20 22 24; do for st in heap wheel; do
  $B E $((1<<lg)) $s 4000000 clean $st 2000000; done; done; done      # mixed, warmup 2M
for s in 1 2 3; do for st in heap wheel; do $B S 4194304 $s 3500000 clean $st 2500000; done; done
for s in 1 2 3; do for st in heap wheel; do $B S 16777216 $s 12000000 clean $st 11000000; done; done
for s in 1 2 3; do $B A 262144 $s 4000000 clean heap 2000000; $B A 262144 $s 4000000 clean wheel 2000000
  $B A 1048576 $s 4000000 clean heap 2000000; $B A 1048576 $s 4000000 clean wheel 2000000; done
for s in 1 2 3; do for lg in 16 18 20; do for st in heap wheel; do
  $B F $((1<<lg)) $s 200000 clean $st 50000; done; done; done
```

| regime (steady) | N | heap ns/op | wheel ns/op | ratio | wheel gain | cycling |
|---|---|---|---|---|---|---|
| E mixed spread+storm | 2²⁰ | 200 | 83 | 0.41 | 2.4× | 48k steps, burst ~83 |
| E mixed | 2²² | 306 | 126 | 0.41 | 2.4× | 1.6k steps, burst ~2.5k |
| **E mixed** | **2²⁴** | **325** | **146** | **0.45** | **2.2×** | 48 steps, burst ~84k |
| S pure spread | 2²⁰ | 202 | 89 | 0.44 | 2.3× | 27k steps |
| S spread (warmup 2.5M) | 2²² | 317 | 128 | 0.41 | 2.4× | 1.8k steps |
| S spread (warmup 11M) | 2²⁴ | 371 | 130 | 0.35 | 2.9× | 412 steps |
| A storm | 2¹⁸ | 252 | 127 | 0.51 | 2.0× | 594 steps, sets 4.0M |
| A storm | 2²⁰ | 341 | 159 | 0.47 | 2.1× | 154 steps |
| A storm, one-shot 2²⁴ | 16.8M | 7 321 | 1 223 | 0.17 | 6.0× | 1 step (cannot cycle) |
| F all-far quiet | 2¹⁶ | 235 | 535 | 2.28 | **0.44× (heap wins 2.3×)** | 149k steps, burst ~1.3 |
| F all-far | 2¹⁸ | 343 | 571 | 1.66 | 0.6× | |
| F all-far | 2²⁰ | 432 | 583 | 1.35 | 0.74× | |

The 97bf headline 4.5× was the one-shot mega-storm (0.17 here, 0.22 on the parent's box);
steady storm is 2.0–2.1×. The regime the parent never measured — all-far quiet regions, where
the wheel degenerates to its own overflow heap plus bitmap/cascade overhead — is the heap's:
the wheel loses up to 2.3×. The gold condition as named by the checker ("holds ≥2× at DRAM
scale with correctness closed" on a mixed spread+storm steady-state workload) **holds: 2.2×
at 2²⁴**, and pure spread does better (2.9×).

**Disclosed mid-run:** (1) my first steady sweep recorded S 2²²/2²⁴ rows with warmup too short
for a log-uniform fill (they measured the fill flash, bursts ~350k; those rows remain in
`steady.jsonl` at `delivered`=2M and are excluded from the table; the corrected rows carry
`delivered`=3.5M/12M). (2) My first extension build accidentally dropped `last_k = out.len()`,
silently disabling churn — caught by the P3 digest regression before any performance row was
recorded, fixed, and every performance row postdates the fix. (3) Tail percentiles still
sample `set()` only, as in the parent; not re-measured here.

## Predictions

`predictions.md` (written before any post-fix run, outcomes appended after): P1–P4, P6, P9
held; P5/P7/P8 partial in the disclosed directions (spread and storm slightly better than
predicted, the all-far heap win larger than predicted at 2¹⁶). The fix's failure mode named
in advance (liveness predicate wrong → diff divergence post-fix) never fired.

## What would make it wrong, cost, fit

- **Wrong if:** a workload exists where a body has two live-appearing overflow entries (the
  `loc`/`at` invariant forbids it; every diff battery here says none), or where the steady
  op-mix differs from these renewal models (e.g. adversarial correlated re-times). The gain
  also assumes the in-window fraction stays material: **if most pending events sit beyond W,
  the wheel is the wrong structure** — a quiet region wants the heap or a second wheel level.
- **Adoption cost:** the parent's ~150 lines + this fix (~30 lines, `over_pop_raw` +
  `over_top_live` + 3 call sites, no hot-path change when the wheel is non-empty — the
  regression digests prove the hot paths are untouched). The 24 B packet is 24 GB at 10⁹
  bodies (unchanged from the parent): adoption needs `shipmem`'s packing, and now also the
  regime rule (heap fallback for quiet regions, or W sized to the kick-epoch horizon so the
  in-window fraction stays high).
- **PRINCIPLES:** #12 ("the algorithm that allocates the work… p95/99") — the wheel's gain is
  now stated per regime with the losing regime named; #2 "Exact means deterministic and
  reproducible" — the record regenerates byte-identically; #9 — the parent's configuration
  had a corner hole; the fix kills that configuration's bug, not the method.

## The lens

The second-author lens trusts the checker's frame and may inherit its blind spots: the
"mixed" recipe (1/16 storm) is my choice, not derived from the engine's measured event mix —
a real workload could sit anywhere between S and A, all wheel-favoured, or in F, heap-favoured.
The F loss mechanism (bitmap + cascade overhead on the overflow path) suggests the fix for it
(a second wheel level, Varghese-style) was not tried; that is the next experiment if the
engine's real horizons turn out wider than W.

## Verdict sought

Gold per the parent's checker: the named experiment is done — correctness closed (identical
stream everywhere, including the corner), the record regenerates, the gain restated per
regime with the mixed workload ≥2× at DRAM scale.
