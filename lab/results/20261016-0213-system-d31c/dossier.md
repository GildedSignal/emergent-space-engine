# dossier — 20261016-0213-system-d31c (whole-system lens)

## Claim

The birth plan pass's two planet-read paths are one readout (`Ctx::secondaries`' Cartesian states and
`ext::constants`' element reads), and sharing them (`PlanetsAt`, `ES_PLANETS_AT_T`, armed only inside
`Universe::start`) cuts the pass **32.8–33.9 → 22.5–25.5 µs/body (−31% at 10⁴, −28% at 10⁵, flat in N),
digest-identical on every flight** — but the element read itself measures **≤ 0.4 µs/body**, so the
unification's gain is already paid for by hoisting the Cartesian read alone, and the page's named
"≲ 13 µs/body" does not arrive: after both reads are shared the pass is per-body arithmetic, not reads.

## Bottleneck

The furthest-behind number on the board: real bodies in the flyable engine (10⁶ flown against 10⁹).
404b measured the birth rail at 42–44 µs/body, 76–78% of it `Universe::start`'s first-plan pass;
cfe5 hoisted the secondaries read to 22.8–23.2 and inferred a second, untimed read path through
`ext::constants`' `source()`, naming one shared readout for both paths at "≲ 13 µs/body". This run
builds that readout and measures what it actually buys. At 10⁹ the pass term was ~6 of ~8 M1-core-hours
of fill; this run and cfe5's hoist together take the pass from 33.4 to ~23 µs/body (lab-box), deleting
~2.9 of ~9.3 lab-box core-hours — an adoption step on the ladder (≈1.4×), not a gold-grade jump.

## Evidence (this box: Linux, 8 vCPU i7-4790-class, shared, load avg ~4 during the quiet grid; orders of magnitude only)

`ES_BIRTH_SPLIT` timers (print-only, 404b's knob) aboard both arms; the OFF arm is the shipped path
(env unset). `ES_PLANETS_AT_T` arms `PlanetsAt::build` once before the pass; a read at any other tick
misses and falls back to the live path bit for bit.

| N, seed | pass OFF | pass ON | replan OFF→ON | constants OFF→ON | project OFF→ON | secondaries OFF→ON |
|---|---|---|---|---|---|---|
| 10⁴, s1 | 33.08 | 22.65 | 28.81→18.48 | 5.20→4.98 | 15.44→5.48 | 10.06→0.04 |
| 10⁴, s7 | 33.06 | 22.69 | 28.77→18.52 | 5.21→4.98 | 15.35→5.51 | 9.95→0.04 |
| 10⁴, s11 (held out) | 32.90 | 22.65 | 28.71→18.50 | 5.21→5.00 | 15.36→5.50 | 10.00→0.04 |
| 3×10⁴, s1 (held out) | 33.94 | 23.35 | 29.61→19.10 | 5.44→5.22 | 16.00→5.76 | 10.29→0.04 |
| 10⁵, s1 | 33.71 | 25.49 | 29.38→20.70 | 5.41→5.61 | 15.93→6.31 | 10.23→0.05 |
| 10⁵, s7 | 32.76 | 22.51 | 28.55→18.41 | 5.28→5.06 | 15.47→5.58 | 9.93→0.04 |
| 10⁵, s11 (held out) | 33.35 | 24.81 | 29.07→20.14 | 5.35→5.48 | 15.78→6.14 | 10.11→0.05 |

- **The record reproduces**: pass OFF 32.8–33.9 flat in N (404b: 32.5–33.5), secondaries 9.9–10.3 = 30%
  (cfe5: 9.75–10.23), project 15.4–16.0 (cfe5: 15.4–16.0), draw+add 9.9–10.8 (c4d3: 9.2; 404b: 9.3–9.7).
- **The cut**: pass ON 22.5–25.5, matching cfe5's secondaries-only hoist (22.8–23.2) within noise — the
  element read adds ≤ 0.4 µs/body of saving (`constants` is flat OFF→ON; it is per-source Hill arithmetic,
  cbrt+div+add over ~8 sources, not a read).
- **Identity**: digests after `settle` to a 3,000 game-s canonical cut are bit-identical OFF↔ON at all
  seven flights (held-out seed 11 and N=3×10⁴ included; `out/grid_quiet.log`), and the crate suite is
  green with the memo OFF (77 tests, 0 failed) and with `ES_PLANETS_AT_T=1` (77 tests, 0 failed,
  `out/suite_on.txt`).
- **Attribution of the ON pass** (~18.5 µs replan + 4.2 apply at 10⁴): constants arithmetic 5.2 (28%),
  project arithmetic+its readout 5.5 (30%), plan_clock's two own-state readouts 6.9 (37%), plan/ticks
  math ~0.9 (5%); shared-state reads: 0.04 µs (0.2%). No shared-state term remains in the pass.

Commands (each ≤ 60 s where possible):
- `bash lab/results/20261016-0213-system-d31c/grid.sh` (the table above; writes `out/`)
- `cargo test --release -p emergent-universe --tests` and `ES_PLANETS_AT_T=1 cargo test …` (suites)
- `regen.sh` regenerates everything from the patch.

## Predictions (predictions.md, written before the grid)

- **P1 (pass ON 11–16 µs/body): FAILED** — 22.5–25.5. The mechanism is now measured: the element read
  is ≤ 0.4 µs/body (I predicted 6–11), so unifying the paths cannot reach 13. cfe5's "≲ 13" dies with it.
- **P2 (both read paths < 5% of pass): half-held** — the reads are 0.2% (secondaries 0.04, the element
  read bounded by constants' flatness), but `constants` stays 23–28% because it is arithmetic, not a
  read; my P2 mis-located the read inside `constants`. No third read path exists (P2's intent holds).
- **P3 (identity): HELD** — bit-identical digests at all flights incl. held-out cases; suites green.
- **P4 (flat in N): HELD** — ON 22.7 (10⁴) → 24.0 (10⁵ median), +6% over a decade of N, the same
  flatness as OFF.

## What would make it wrong

The pass numbers are one quiet pass each on a shared box (seed-to-seed spread < 7%; the box's ±10% load
noise bounds them); the M1 re-measure is the integrator's, as always. The identity claim rests on the
settle digest and the suite: a read at t ≠ 0 inside `start` would fall back live (the tick guard) and
stay exact, so the digest cannot by itself prove the element table hits — but `secondaries` at
0.04 µs/body proves the shared table is armed and served, and the ≤0.4 µs bound on the element read
holds whether it hits or not (constants OFF≈ON). If `apply`'s 4.2 µs/body share amortizes differently
at a real 10⁹ fill, the ON-pass projection shifts by that share, not more.

## Fit with PRINCIPLES

"Less is more. The cheapest compute is compute not done" — one readout per pass instead of one read per
body per path; and the negative result serves the same principle: the second path was already nearly
free, so the next compute-not-done must come from the arithmetic or from not planning bodies at birth
at all (b29a's program-store promotion, the pass's true alternative). "Store the generator, not the
generated": the table stores each source's one read, not N copies. "A fix signals the wrong
representation": the ≲13 prediction treated the pass as reads; it is arithmetic — the question is now sharp.

## The lens

What the whole-system view may have missed: I unified the *reads*; the pass's real weight (own-state
readouts 6.9 + kepler/Hill arithmetic ~11 µs/body) is per-body math that no sharing touches, and the
hard special case is the locals (up to 300 bodies in Home's doll, whose `open`/`tide` paths the timers
do not separate from the clock's). The next rung the numbers name: `plan_clock`'s two own-state
`readout` calls (6.9 µs/body, 37% of the ON replan — one state is computed and thrown away twice),
then the Hill/cbrt block — or the deletion: the program-store birth that never runs this pass.
