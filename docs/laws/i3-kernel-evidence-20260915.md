# I3 memory-kernel / Volterra compression evidence — 15 September 2026

Not canonical gravity. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. `production_law` null.
Not I3 exit. Not I4–I6. Nested Charge `ledger_total` is the denominator.
Gates declared before this slice’s runs: `KERNEL_POS_BAND = 0.05`, `KERNEL_A_BAND = 0.05`, `KERNEL_RANK_MAX = 16`, `KERNEL_MEMORY = 1.0`, `KERNEL_STEP = 0.5`. None were widened after seeing results.

## What ran

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, parent `facf4a5`. Target `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`, `--offline --locked`, `--test-threads=1`.

| Command | Result |
|---|---|
| `cargo test -p emergent-law-lab --lib i3_ -- --test-threads=1` | PASS (9) |
| `cargo test -p emergent-law-lab --lib coupled_ -- --test-threads=1` | PASS (54) |

## Method

`compile_memory_kernel_response`: collocate a **fixed** bootstrap window `[0, KERNEL_MEMORY]` (two light-crossings of the circular `a=4` pair). Form the window Jacobian `K` of retarded GEM-a, take numerical SVD rank. Advance later windows at `KERNEL_STEP=0.5` (one light-crossing) with lookback **only** into that memory, without `interval_compile` over H. Not compact-after-the-fact of a finished H=4/H=6 collocation.

## Result: KEEP in the quiet two-body domain

| Case | Rank | Memory | Fill-in (`n²`) | Ledger | Δx | Δa |
|---|---|---|---|---|---|---|
| Circular `a=4` H=4 | 4 | 6 | 144 (`n=12`) | **1089** vs collocation **1551** | 0.00150 | 0.00122 |
| Circular `a=4` H=6 | 4 | 6 | 144 (`n=12`) | **1113** vs collocation **2057** | 0.00259 | 0.00122 |
| Eccentric H=6 | 4 | 6 | — | 1113 vs 2024 | 0.00177 | — |

Operator rank, Jacobian `n`, memory length and fill-in **do not grow with H**. Incremental horizon cost is +24 ledger (H=4→H=6) vs +506 collocation. Coarse marched samples still grow (18→26 functions vs collocation 30→46); that is the trajectory table, not pair-inverse fill-in.

## Failure cases (explicit fallback)

| Case | Outcome |
|---|---|
| Radial rest pair | Refused close-encounter (`\|v\|=0`) |
| Resonance / weak kicks | Refused; no guessed event table |
| Distant-tide entrant | Refused n-body |
| Tight pair `a=3` H=6 | Constructs (rank **12**, ledger 1679); rank rises with coupling, still ≤16 |

## I3 exit

Not proven. This is movement: matched GEM under predeclared 0.05 gates, cheaper nested cost, bounded operator. Bootstrap window still dominates the kernel ledger (~1089 of 1113). I3 exit still needs that keep to cover a horizon where sequential collocation would have dominated, including kicks/entrants, without dropping mass/causes/history.

## Next

Do not start I4–I6. Discriminating leftover: amortize the bootstrap over a longer quiet horizon, or an explicit recouple/collocation fallback path that consumes kicks without a guessed event. Interval-wide GEM authority remains missing.
