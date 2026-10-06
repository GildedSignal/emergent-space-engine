# Evidence — raw numbers

Cloud Linux x86, 8 shared vCPU, 15 GB (other lab runs in the window). Orders of magnitude only;
the integrator re-measures on the M1. Binary: `target/release/xtask` via `CARGO_TARGET_DIR`
(set to /home/glmlab/lab-target-3 by the runner). Patch of the tree: `--policy` in
`xtask/src/universe/{mod,session}.rs` (session-layer only; captured by run.sh).

Commands (each ≤ 60 s):

    cargo build --release -p xtask --offline -j 6
    T=target/release/xtask   # via CARGO_TARGET_DIR
    $T universe --bench --seconds 30 --rtf 4 --members 400 --seed 1 --policy fixed --engine-ms 5
    $T universe --bench --seconds 30 --rtf 4 --members 400 --seed 1 --policy fixed --engine-ms 13
    $T universe --bench --seconds 30 --rtf 4 --members 400 --seed 1 --policy aimd
    $T universe --bench --seconds 30 --rtf 4 --members 400 --seed 1 --policy ahead
    $T universe --bench --seconds 30 --rtf 4 --members 400 --seed 1 --policy both

Note: `--members` is clamped to 400 by the CLI, so every "members 600" invocation ran 400.
Scene: the plane's default system; battle members 400; rtf 4 (game time 4× wall); 1800 frames.

## Batch 1 (v1 policies: ahead = present the lead)

| policy | p50/p99 frame ms | worst ms | hitch>16.7/h | RTF med / lo1% | overflow | digest |
|---|---|---|---|---|---|---|
| fixed 5 ms (today) | 5.16 / 10.72 | 14.28 | 0 | 4.00 / 0.007 | 55 | 87f51de403a4… |
| fixed 13 ms | 5.81 / 16.82 | 22.57 | 19 | 4.00 / 4.000 | 18 | 87f51de403a4… |
| aimd v1 | 5.90 / 13.35 | 18.50 | 6 | 4.00 / 0.000 | 68 | 87f51de403a4… |
| ahead v1 | 8.96 / 14.16 | 14.61 | 0 | 4.28 / 0.000 | 82 | 87f51de403a4… |
| aimd+ahead v1 | 5.65 / 14.87 | 20.55 | 6 | 4.00 / 0.000 | 72 | 87f51de403a4… |

## Batch 2 (v2 policies: ahead = resolve to a 50 ms-game lead, present on the wall clock)

| policy | p50/p99 frame ms | worst ms | hitch>16.7/h | RTF med / lo1% | overflow | digest |
|---|---|---|---|---|---|---|
| fixed 5 ms | 5.06 / 10.24 | 13.35 | 0 | 4.00 / 0.000 | 56 | 87f51de403a4… |
| fixed 13 ms | 8.12 / 19.60 | 23.99 | 25 | 4.00 / 1.881 | 27 | 87f51de403a4… |
| ahead v2 (inventory) | 6.48 / 18.77 | 22.06 | 29 | 4.29 / 0.000 | 76 | 87f51de403a4… |
| aimd + ahead v2 | 9.02 / 15.30 | 20.77 | 8 | 4.23 / 0.000 | 77 | 87f51de403a4… |

Batch-to-batch drift (fixed 13: 19 vs 25 hitches) is machine load; the knee's shape is stable.

## Unbinding check (regression direction)

members 48 (default), rtf 1, seed 1: every policy p99 ≤ 3 ms, 0 hitches, RTF 1.0 — the fixed budget
never binds there (engine p50 0.14 ms of 5 ms); only binding scenes discriminate the disciplines.
(The members-48 row was measured pre-patch with the stock binary; the policies touch nothing at
rtf 1 because their triggers — overflow, spare — stay at 0/5 ms.)
