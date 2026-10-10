Grade: silver

**Abstract.** Claim: on the shipped plane one kick = one full orbit compile, and the compile's uncounted interior (allocations, key search, i128 panels) — not its ~2,300 counted `Scalar` ops — holds most of the ~86 µs event; so the per-event lever is the re-anchored jet, not arithmetic or layout. Reproduced from the patch on a clean tree: per-kick add 992/mul 1011/div 254/sqrt 46, ~182 panels, exact memo reuse 0 of 5,438, quantized 246 shapes (22:1), digests bit-identical to the unmodified build, fit 60 %/forces 30 % on the clock path; adversarial 4×-density, sparse and near-idle cases hold. Nothing to adopt in code: it is a decision input closing the counted-arithmetic door (≈3–5 µs) and pricing the jet ≈20× on the compile share.

## Reproduction

- Applied `work/patch.diff` to the clean tree, built, ran `repro.sh`'s commands myself. Seeds 1 and 23: op counts, panel counts, rebinds, memo shape counts and both digests **bit-identical** to `kb1.json`/`kb23.json`; medians within noise (87.7 vs 87.8 µs). `predictions.md` (09:27:57) precedes the decisive JSONs (09:37:22); baselines measured before predictions, disclosed.
- **Digest control held:** reverted the patch, rebuilt, ran seed 1 unmodified — same `replay_digest` (103336b5…) and `digest` (7162d382…). Instrumentation overhead ≈8 % on the leaver median (80.8 → 87.7 µs), far under the pre-registered 1.5× kill line.
- Whole-plane cross-check on the unmodified build: engine 31.8 %, view_gather 53.6 %, ships 65.8 µs/item, fleet 37.1, player 2075 µs/item (31.5× a ship), 2067 events/s. All match the dossier.
- Arithmetic in the dossier checks against the JSONs (stage shares 59.6/30.1/8.2/0.7/1.4 %; op mix 43.9 % mul; 5438/246 = 22.1).

## Adversarial cases

1. `--members 1600` (4× fleet, seed 5): bound 0.963/kick, ~2,130 ops, 183 panels, exact reuse 0.0, p99/median 5.1×. Holds.
2. `--members 100` (sparse, seed 5): bound 0.978, ~2,090 ops, 221 panels, exact reuse 0.0. Holds; note the leaver median is workload-dependent (113.6 µs), so "85–94 µs" is the five-seed range, not a constant — orders of magnitude only, as the dossier scopes it.
3. Negative control (`--seconds 1 --rtf 1 --members 4`): zero leaver-path ops, 23 made samples only. The counters stay quiet outside kicks.

## Predictions

Written before the decisive runs and adjudicated honestly: P1 held on the clock path only (flagged by the author), P2 missed by a hair, P3 wrong in mechanism (correctly re-attributed to compile volume), P4 held and sharpened, P5 verified by me on kb11/kb23 (shares within ±5 pp). This is the pre-registration discipline the lab asks for.

## Novelty

Partially new. Known already: exact memo never hits on distinct kicks (H0213's correction; the 5 October taste log), quantized reuse ≈95 % but a law change (law.md "Not adopted"; components-4643), the jet priced at ~0.05 compiles/kick (law.md, graded gold by one checker). New here: the event-interior pricing — counted `Scalar` ops ≈3–5 µs against an ~80–88 µs event, ~180 panels/kick, the `kick_clock` stage split, and the player's event at ~30× a ship's. No prior entry prices the kick's interior or the player event; I searched HISTORY.md and the docs.

## Goal fit

Prices board focus 1 ("kicks dominate the engine's cost") one level down and closes a door: no counted-arithmetic or layout fix reaches 10× when the counted arithmetic is <20 % of the event — "the cheapest compute is compute not done" (§1), "measure before claiming" (§10), and the churn finding feeds "we need to be deeply aware of von-neumann bottleneck and memory" (§17). Counters are integers; digests prove work identity.

## Why not gold

The claim names the residual "**memory churn** (allocation, key search, i128 panels)" as the holder of ~80 % of the event, but nothing measures that split. The panels are counted, not priced; i128 panel arithmetic is compute, not churn, and could hold a large share of the 80 µs — which would soften "no arithmetic fix reaches 10×" even though the jet conclusion (delete the whole compile) survives either way. Second, the stage timing covers only `kick_clock` — 8.8 % of made samples on seed 1 and 0 % of the leaver path (97 % of samples); "fit 60 %" is 60 % of a small slice. Third, "bound = 1.00 per kick on both paths" is rounded up: 0.963–0.983 on leavers across all five seeds and my adversarial runs (2–4 % of leaver kicks take an uncharacterized early path). None of these breaks the decision input; together they leave the headline mechanism one experiment short of measured.

## The experiment that would make it gold

Instrument the leaver path (`fn kick`) with the same five-stage split, and inside `OrbitShape::bound` count allocations (a global allocator hook), `fit_key` search steps, and i128 panel mul-adds separately. If churn (allocation + key search) holds the bulk of the ~80 µs, the claim is gold as stated; if i128 arithmetic holds it, the claim's mechanism is corrected and the "no arithmetic fix" door narrows. One build, one run, ≤15 s of bench.

## What the author missed

- The i128 panel math is arithmetic wearing churn's clothes; the lens read "uncounted" as "overhead" (the author's own lens note points at the quantized-reuse temptation but not this).
- The made-path "stage split" silently averages over the 91 % of made samples that never enter `kick_clock`; per-event staged time for actual clock kicks is ~71 µs (6.2 µs ÷ 0.088), i.e. clock kicks are the expensive tail of made, not its median — invisible in the presented averages.
- The near-idle negative control cannot be read from the JSON (inter-sample counters are discarded by the `take()` before each sample); it is asserted, not observed.
- Seed 7's median is 94.95 µs, so "85–94" rounds down by a hair; trivial, but the checker's job to say it.
