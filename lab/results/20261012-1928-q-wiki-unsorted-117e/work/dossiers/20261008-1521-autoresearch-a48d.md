# Dossier — run 20261008-1521-autoresearch-a48d

## Claim

One line deleted from the kick path — the rebind's second trajectory decode, computed only to
build a residual the kick then throws away — cuts the plane's pure kick resolve by **~38%
(72.3 → 45.0 µs median, like-for-like quiet runs; min-of-3 72.1 → 42.1, −42%)** with
**bit-identical replays** (digest `dac49af3…` on all six runs, pre and post).

## Bottleneck

Board focus line 1: "fewer kicks per orbit… kicks dominate the engine's cost"; bottleneck 3:
"cheaper events". Metric: µs per pure kick resolve (`xtask universe --kick-bench`, the
deterministic replay of the plane's own pending kicks — the artifact that works). The stage
attribution (new bench `a48d_bench`, this run) put the rebind (`bind`) at ~46% of a kick:
from_state 11.1 µs (compile 3.3, fit ~5.2, decoded_event ~2.6), bind_in's own decode ~3.8,
own readout 3.3, secondaries 3.3, tide 3.3, force 0.8.

## Evidence (Linux x86, shared 8-vCPU box, orders of magnitude only)

- Attribution: `a48d_bench` (kept at `crates/universe/examples/a48d_bench.rs`, patch).
- Held-out workload `xtask universe --kick-bench --seconds 2`, 3 runs per tree:
  - baseline (HEAD): medians **72.08 / 73.41 / 72.27** µs (p99 92.8/105.3/92.7)
  - change: medians **42.06 / 63.37* / 44.99** µs (p99 55.2/88.0/72.3; *one contended run)
  - `replay_digest` identical (`dac49af387662466…91327bb96`) in every run; `refused: 0`.
  - Stage bench (orbiter about a planet, Cycle fit): full kick 32.64 → **29.48 µs** (−9.6%).
- Why the held-out gain (−38%) exceeds the stage-bench gain (−9.6%): the kick-bench population
  is mostly fleet members, whose fits resolve to `Trajectory::Passage`; one `decoded_event`
  (a `Passage::state` solve) costs far more there than the Cycle case the stage bench samples.
  The deleted work is per-kick constant, so p99 falls with the median (96.7 → 55–72).
- Reproduce (each ≤ 60 s once built): `cargo build --release -p xtask` then
  `xtask universe --kick-bench --seconds 2` (compare `kick_us_all.median` and `replay_digest`).
- Change: `crates/space/src/binding.rs` — `Rebinding::from_state` split; `fit_only` returns the
  fit with a zero residual; `from_state` = `fit_only` + `Residual::between(state, decoded_event())`
  (handoff and engine callers unchanged). `crates/universe/src/bind.rs` — `bind_in` calls
  `fit_only`. Tests: `cargo test --release -p emergent-space -p emergent-universe -p emergent-engine`
  — **all green, 0 failures** (160 tests, 1 pre-existing ignored), run after the change.

## Predictions

`predictions.md` was written before the decisive run. P1 (stage bench −7–10%: hit, 29.48 vs
predicted 29.5–30.5). P2 (digests identical, suites green: both hit). P3 (kick_bench −6–9% absolute 2–3 µs: **miss — conservative**; the real gain is
−27 µs median because fleet members' deleted decode is a Passage solve, not the Cycle solve I
had measured). P4 (handoff unchanged: `from_state` untouched in behavior). The P3 miss is a
measurement-of-the-wrong-population error, in the change's favour; the direction and mechanism
were as predicted.

## What would make it wrong

If any caller of `Rebinding` reads `residual` after `fit_only` (only `bind_in` uses `fit_only`;
it provably reads trajectory/periapsis_time/periapsis_angle/clockwise only — verified by grep
and by the identical digests). If a future change makes `bind_in` want from_state's residual,
the split still stands (it would call `from_state`). Adoption cost: ~20 lines, no API break.

## Fit with PRINCIPLES

#1 "The cheapest compute is compute not done. Delete before optimizing" — this is a delete, not
an optimization; the arithmetic is untouched, so "any faster implementation must return the same
bits" (num.rs) holds trivially. #13: nothing new compounds; the residual the tube carries is
unchanged. #11: one home — the invariant "the tube's own decode defines the carried remainder"
now has one implementation instead of two competing ones.

## The lens (autoresearch) and its blind spot

Local search kept the first change that measurement justified and stopped (time-boxed window;
one round). Blind spot: a local optimum — the next structural cut is not in `bind` at all but in
the *number* of decodes per kick: `readout`, `secondaries` and `tide` each decode a trajectory at
the same tick (≈ 3.3 µs each, ~30% of the post-change kick). A per-(doll, tick) read-only decode
cache shared by the three would beat this round's gain — but it is an architecture change (the
memo lesson on the board says such caches must prove their keys distinct first). Second candidate,
logged in `log.md`: float-seeding `fit_key`'s exact bisection (−2–3 µs/kick), needs a
differential corpus before it can be kept.

## Grade request

Gold: suites green (160/160, above), reproduced bit-exact on the held-out workload, ~1.6× on
the engine's dominant event, adoptable in one step (a two-file patch).
