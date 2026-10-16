# Dossier — 20261016-0023-quant-404b

## Claim

The birth rail's missing two-thirds is `Universe::start`'s tick-0 first-plan pass: at the ladder's
true belt keys, one belt body costs **42–44 µs/body to build on this box, of which draw+`add_body`
is 9.3–9.7 µs (22–24%) and the one-shot `replan`+`apply` loop inside `start` is 32.5–33.5 µs
(76–78%), flat in N from 10⁴ to 3×10⁵ and seed-stable — so the per-body birth CPU the 10⁷ rung
priced at "compile-dominated 28–31 µs" is in fact **first-plan-dominated**, and a compact-store
belt that never runs `start`'s plan pass deletes ~3.3× more birth CPU than the whole compile path.

## Bottleneck

Board item 1 (bodies in the flyable engine) and the ladder's named break #4 (the 10⁷ rung: build
28–31 µs/body, exponent 1.0). HANDOFF's scoreboard holds the birth rail inside "memory per body ~2,460 B
at birth"; the CPU twin was unpriced beyond the 28–31 µs headline. Expected gain of pricing it:
the fill at 10⁹ is ~8 M1-core-hours, and this split says ~6 of them are the plan pass — the exact
work a program-store birth (b29a's smallest promotion, 21–40 bits/body) provably never does, which
re-prices the compact store's CPU case (not just its memory case) by ~3×.

## Evidence

Machine: this box (i7-4790, 4C/8T, shared), load 3.3–3.6 during the runs, 1 thread, Rust release.
Cloud timings are Linux/x86: **orders and ratios only**; the M1 re-measure is the integrator's.

Instrument: `ES_BIRTH_SPLIT=1` — print-only, env-gated timers (the crate's `ES_*` pattern) around
(a) `plane_with_extra`'s ladder loop (draw + `add_body`) and (b) inside `Universe::start`: the
allocations, the `replan`+`apply` loop, requeue, fleet start, rekey. Off (`unset`/`0`/`""`): the
shipped path, no prints. Example `birth_rail` flies `plane_extra` (the ladder's own population
generator, seed 1 by default, `Order::Sparse`, 1 thread, members 48 — as the ladder flies), best
rep after one warm rep. All numbers regenerate (`regen.sh`, ~4 min).

| N (bodies) | build slope µs/body | draw+add_body | start plan pass | requeue+alloc+rekey |
|---|---|---|---|---|
| 10,028 | 41.9 | 9.31 | 32.46 | 0.09 |
| 100,028 | 43.1 | 9.68 | 33.18 | 0.09 |
| 300,028 | 44.2 | 9.66 | 33.48 | 0.09 |
| held-out seed 3, 100,028 | 42.6 | 9.54 | 33.02 | 0.08 |

- Flat: slope 41.9 → 44.2 µs/body across a 30× N range (+5%; exponent ≈ 1.0). The plan pass is
  flat per body (32.5 → 33.5): no cache cliff — the pass is compute, not misses.
- The 28-planet plane's own bodies: plan 25.8–29.9 µs/body (same order; heavier dolls).
- The draw alone is noise: `ladder_ship` + name push is inside the 9.3–9.7 µs with `add_body`
  (c4d3 measured the same path at 9.2 µs p50 on the M1: this box reads it at 9.3–9.7, so the
  compile path is near box-invariant — integer-bound — while the plan pass is the box-sensitive
  float/search side; the RATIO plan/add ≈ 3.4× is the portable number).
- Reproduces the ladder's own anchor: 42–44 µs here vs 28–31 µs on the M1 ≈ 1.4–1.5× box factor,
  consistent with the plane's other µs-scale ratios (kick 30 µs M1 vs ~40+ here at like-for-like).
- Digest identity: `ladder_digest` (13 scripted flights × 4 schedules) on the patched tree with
  `ES_BIRTH_SPLIT` unset vs a pristine stash-overlay build at the same commit: all 13 digests and
  all kick/encounter counters identical (`ld_patched.txt` vs `ld_pristine.txt`; the only textual
  difference is the per-case wall-time column). The patch prints only; it reads no engine state.

Commands (each ≤ 60 s where marked):
- `cargo build --release -p emergent-universe --example birth_rail --example ladder_digest`
  (note: `--examples` fails on this commit's `nladder`, which links the macOS-only
  `proc_pid_rusage` — pre-existing on main, not this run's breakage; first build ~4 min warm)
- `ES_BIRTH_SPLIT=1 REPS=3 <birth_rail> 0 10000 100000 300000` (~75 s)
- `SEED=3 REPS=2 ES_BIRTH_SPLIT=1 <birth_rail> 10000 100000` (~15 s)
- `python3 analysis.py run_main.log`
- `<ladder_digest>` (digest identity, ~3 min)

## Predictions

Pre-registered in `predictions.md` before any timed run:
- **P1 held:** slope 40–90 µs/body predicted, measured 41.9–44.2; flat ±30% and exponent ≤ 1.1
  predicted, measured +5% over 30×.
- **P2 held, sharply:** add_body ≤ 35% predicted → 22–24%; plan ≥ 40% predicted → 76–78%;
  requeue+alloc+rekey ≤ 10% predicted → 0.2%.
- **P3 held at the low edge:** first-plan per body = 0.3–0.4× one wave kick's CPU per body
  (predicted 0.3–3×; same class of work — one resolved event — but cheaper than a settle kick).
- **P4 held:** fill arithmetic: 42 µs/body × 10⁹ ≈ 11.7 core-hours this box ≈ 8 M1-core-hours,
  of which the plan pass is ~6 M1-core-hours — pure `start()` overhead a program-store fill
  never pays. Kill criteria did not fire (add_body never ≥ 60%; allocations never dominate).

## What would make it wrong

The plan pass could be cheap on the M1 in a way this box exaggerates (float/SIMD-sensitive); the
M1 re-measure must confirm the 3.4× plan/add ratio before the 10⁹ arithmetic is quoted. The pass's
interior (how much is `replan`'s event search vs `apply`'s walk) is unattributed — if a second
author finds it is one irreducible exact search per body, the number stands as the floor of
birth-on-the-shipped-law; if it is bookkeeping, part of the 33 µs is deletable and the claim
understates the lever. The 10⁹ fill arithmetic assumes the belt mix (a∈[2,3) AU, e≤0.4) — a
comet-heavy fill pays more per body (the plane's own 28 bodies: 25.8–29.9 µs plan).

## Cost of adoption, and PRINCIPLES fit

Nothing to adopt: this is a measurement that re-prices two standing decisions — (1) the compact
store's case is CPU (3.3× the compile path deleted) and not only memory (scoreboard row 4); (2) any
lazy-birth wiring (ladder break 4, b29a) must skip `start`'s plan pass for never-touched bodies,
which is also where its 10⁷-promotion ruin ("~250 s of compiles") gets 3.3× worse if implemented
as promote-then-plan. Fit: "Compute only surprises" (a body nothing touches is planned for
nothing) and "Store the generator, not the generated" — the plan pass is the generated part.
Cost: one M1 re-measure (minutes).

## The lens

Quant priced a latency budget per stage and checked it against an anchor measured by another
instrument (c4d3's 9.2 µs) on a different box — the cross-box near-equality of the integer path
is itself evidence the split is real, not an artifact of this harness. What the lens may have
missed: the plan pass's interior (a systems lens would attribute it further), and whether the
M1's efficiency cores change the ratio in flight. One instrument, one box; the checker should
re-fly at least one N and the digest identity.
