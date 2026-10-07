# Dossier — 20261007-1032-spacex-3d04: the plane's time-zoom envelope, mapped to breaking

## Claim

The shipped plane is CPU-flat to ~300× real time and hitch-free as played at 100×, but its fast-forward ceiling is ~3–4×10³ game-seconds per wall second with the full live population (~3.4×10⁴ once the fleet is gone), set by the single-threaded live surprise rate (~2–7×10³ resolved events/s, 42–180 µs all-in per event) — never by frame cost (cpu p99 ≤ 8.4 ms at every rtf up to 10⁶) — and the 5 ms engine budget, not engine cost, is what first binds at 10⁴× (a 50 ms budget removes all deferral for +6% p50).

## Bottleneck

Board focus item 1 (kicks dominate the engine's cost) and the smoothness claim ("flying at 100× and more with no hitch in CPU time"), under the board's top scaling risk (work must track real surprises). The measured lever: per-event all-in cost ~4×10⁻⁵ s on the shipped engine; the slack-skin build (b-encounter-skin, 12.6× on setups) and q-cadence should re-run this exact envelope as their gate — if their items dominate the ~7×10³ events/s, the ceiling moves by their ratio.

## Evidence

Seed 1, one star system (28 bodies + 48 fleet members, 4 dolls; `describe.txt`), Linux x86 shared (load 0.8–3.4 during runs) — orders of magnitude only; the integrator re-measures on the M1. Full table: `analysis.csv`; raw reports: `bench-*.json`.

| rtf target | rtf median | worst 1% | overflow | cpu p50/p99 ms | engine share | ms CPU per game-s | events/s | player |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.0 | 1.0 | 1/1200 | 0.63/0.97 | 4.6% | 38.0 | 61 | alive |
| 10 | 10 | 10 | 3/1200 | 0.93/2.32 | 7.1% | 5.55 | 93 | alive |
| 100 | 100 | 100 | 3/1200 | 0.94/2.44 | 20% | 0.565 | 338 | alive |
| 10³ | 1000 | 1000 | 4/1200 | 1.65/5.33 | 26% | 0.099 | 552 | dead |
| 10⁴ | 10⁴ | 1428 | 132/1200 | 3.10/6.84 | 56% | 0.018 | 2679 | dead |
| 10⁵ | 3.36×10⁴ | 1239 | 600/600 | 6.55/7.39 | 77% | 0.011 | 7093 | dead |
| coast 10³ | 1000 | 619 | 27/1200 | 2.27/6.88 | 50% | 0.136 | 645 | **alive** |
| coast 10⁵ | 4271 | 93 | 600/600 | 7.18/7.84 | 73% | 0.10 | 2166 | **alive** |

1. **Smoothness as played:** paced rtf 100, 20 s: 0 hitches above 16.7 ms per gameplay hour, worst frame 12.0 ms, cpu p99 10.7 ms.
2. **CPU cost per game-second falls 3,400×** from rtf 1 (38 ms) to rtf 10⁵ (11 µs): the compiled orbits cash in; time-zoom is nearly free per game-second until the live surprise rate saturates the budget.
3. **Determinism is bit-exact under load and policy:** paced = unpaced = engine-ms 5 = engine-ms 50 give digest `6ce636fa…` at cut 406,050,894 (rtf 100); at rtf 10⁴, ms 5 and ms 50 give the same digest `d0a37c3f…` while deferral differs (132→0 overflow frames). The budget converts cost into lag and never moves a decision — confirmed past the point where it bites.
4. **Budget binds before cost at 10⁴:** `--engine-ms 50` removes all deferral (worst 1%: 1428→9999) for +6% p50 CPU (3.10→3.28 ms).
5. **The player death at rtf ≥ 10³ is a script artifact:** the scripted burn's *game* duration scales with rtf (31.7 s at 10², 317 s at 10³); coasting, the player is alive at 33,333 game-s and at 10⁶ game-s. First probe (`--level 0`) was invalid — level 0 is the default base throttle, not off — hence the `--coast` patch (below). Digests are input-sensitive (coast `64255c32…` ≠ burn `99d27789…` at the same cut).
6. **The ceiling:** saturated rtf median 3.36×10⁴ (fleet dead) vs 4.3×10³ (full population, coast) game-s per wall second, single thread; a coasted week (10⁷ game-s, rtf 10⁶ × 10 s) does not settle within 100 s. Engine ~300 ms CPU per wall second over 2.2–7.1×10³ events/s ⇒ 42–180 µs per resolved event, roughly rtf-independent.
7. **Instrument holes found:** (a) the bench could not express a burn-less flight — fixed by a 55-line bit-neutral patch (`coast-flag.patch`, adds `--coast`; default digests unchanged, verified against the pre-patch binary: `6ce636fa…` at rtf 100); (b) a mid-run player loss aborts the bench with **no report** (`error: no view: the player is lost`, rtf 10⁶ default and rtf 10⁵ with ms 50) — reported, unfixed: the loss is data and should degrade, not kill, the run.

**Reproduce** (each ≤ 60 s except the two whose timeout *is* the measurement):

```
cargo build --release -p xtask
X=$CARGO_TARGET_DIR/release/xtask
$X universe --describe
for r in 1 10 100 1000 10000; do $X universe --bench --seed 1 --rtf $r --seconds 20 --unpaced; done
$X universe --bench --seed 1 --rtf 100000 --seconds 10 --unpaced          # ceiling, fleet dead
$X universe --bench --seed 1 --rtf 100 --seconds 20                       # paced, as played
$X universe --bench --seed 1 --rtf 10000 --seconds 20 --unpaced --engine-ms 50   # budget vs cost
# with the patch applied (git apply coast-flag.patch):
$X universe --bench --seed 1 --rtf 1000 --seconds 20 --unpaced --coast    # player survives
$X universe --bench --seed 1 --rtf 100000 --seconds 10 --unpaced --coast  # full-population ceiling
timeout 100 $X universe --bench --seed 1 --rtf 1000000 --seconds 10 --unpaced --coast  # does not settle
```

## Predictions

`predictions.md` was written before the sweep. Held: the flat region (≤300×), the bite between 10³ and 10⁵ (first at 10⁴), monotone engine share (4.6→77%), determinism bit-exact at the extremes, the engine (not the view) as the binding subsystem, and the burn-artifact death (confirmed via `--coast`). Missed, reported as held: CPU p99 does not grow linearly past rtf₀ — the budget caps it (≤8.4 ms) and converts cost into lag (the designed behaviour, which I under-modelled); view gather exceeds 2× at the top (2.6×, then saturated ~1.8 ms); my first death discrimination (`--level 0`) was invalid and was replaced by the `--coast` instrument.

## What would make it wrong

Timings from a shared Linux box (order-of-magnitude only; the M1 re-measure decides); a 76-body scenario — the *cause* (live surprise rate saturates the budget) generalises, the *ceiling's value* does not; `events_per_second` counts resolved calendar items (read from `Advanced.events`/`dash.rs`), so the per-event attribution shifts if that counter mixes cheap and dear items; `--threads` defaults to 1 (the shipped default), so the ceiling is a one-thread ceiling — threads > 1 untested here.

## Cost of adoption, PRINCIPLES fit

Adoption: the 55-line `--coast` patch (bit-neutral, proven), plus a suggested small fix so player loss degrades the bench instead of aborting it; zero engine, law or gate changes. Fit: "We need also to map how things break, think in extremes" (CL 09-27 09:08, principle 10) is this run's mandate; "Compute only surprises" (principle 3) is confirmed in the shipped engine by the 3,400× fall in CPU per game-second; "i care about the p95/99 results" (principle 12) — zero hitches at 100× as played; exact means deterministic (principle 2) — bit-equal digests across pacing and budget past the bite.

## The lens

SpaceX hunts the cliff in the shipped article and an idiot index; it may over-weight the fast-forward ceiling if the game never asks a live week in one jump (the player's light cone may cap useful rtf long before the engine does), and it fixed the instrument before asking whether the coast case matters to the design. One lens, one thread: the envelope here is the single-thread envelope.

## Grade (author's own, for the checker)

Silver: reproduced by exact commands, predictions pre-registered with honest misses, one named experiment from gold — re-run this envelope after the slack skin lands (or with threads > 1); if the ceiling moves ≥ 10×, that run is the gold.
