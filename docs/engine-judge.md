# Independent engine judge

`xtask engine-judge` judges Claude's frame and hooks through their public APIs. It changes no engine, lattice or space source. The initial judge source/tolerance freeze is `078ab968`; the numerical oracle was subsequently refined without changing cases, denominators or tolerance bands.

Run from the specialist worktree:

```sh
cargo build --offline --release -p xtask
./target/release/xtask engine-judge --prepare-mutants
```

Compilation prepares the scratch controls before the tests. Every gate has a hard 55 s watchdog. Exit 0 requires every selected gate to pass. Use `--gates E3` (or comma-separated IDs) for a reproducer; E6 requires the prepared mutant binary. Mutable outputs are in `artifacts/runs/engine-judge/`; sealed review evidence is under `artifacts/evidence/engine-judge-20260930/`.

| Gate | Frozen requirement |
|---|---|
| E1 | All 4,320 checkpoint digests equal: 24 scenes, four seeds, both orders, three insertion permutations, 1/4/8 kick threads; contacts and kicks must occur. Flat reduction also equals the bare lattice |
| E2 | Every member/sample in five independent release groups, both orders, one period: position within 3% of the nonlinear inverse-square oracle |
| E3 | Nine groups, both orders, ten periods: position and group shape within 1%; 3% at initial dr/R = 0.003 |
| E4 | Across 48 manual anchors, common-frame total momentum exactly equal; kinetic energy changes by at most one m*k² quantum |
| E5 | Handoff IDs unique, mass partition exact, active mask agrees with ledger, snapshots compose to the parent positions; two outliers leave in both orders |
| E6 | Scratch unmutated E1/E2/E8 controls pass; each of four isolated planted defects fails a gate. A timeout, panic or build failure is not a kill |
| E7 | Future state digests distinguish different frame clocks; an empty anchored scene remains legal |
| E8 | Independently accumulated sub-velocity-quantum drift settles exactly into per-body positions at seven arbitrary manual anchors, both orders |

The oracle is a symmetric composition of three velocity-Verlet maps, not RK4. Coefficients solve `2a+b=1`, `2a³+b³=0`; this cancels the cubic splitting error. Each case is computed at 1,024 and 2,048 substeps/sample. Their positions must differ by less than 1e-5 of each member's initial offset, and their centred group shapes by less than 1e-5 of the group radius. Failure of this check invalidates the behaviour verdict. Circular convergence and forward/backward reversibility controls are unit tests.

The E2/E3 position denominator is the larger of the oracle's current offset and the initial offset, with a one-unit floor. Shape compares deviations from independently mass-weighted group centres, divided by the oracle group's largest offset. Every case is retained in `behaviour-short.jsonl` or `behaviour-anchored.jsonl`. No 99% success threshold hides a failed case.

E4 reconstructs velocities in the pre-anchor axes, using the tube and the complete parent position. Angular-frame terms are exact in 2^-92 units; momentum uses those exact rational values. Energy rounds the reconstructed velocities once to 2^-48 and compares squared mass-weighted speeds in m*k² units. This is the free-fall model's kinetic invariant, not a claim of GR energy conservation. The check does not use `AnchorReport.dp` as its oracle.

The public World API requires strictly increasing IDs. Input permutations are inserted into an independent BTreeMap and normalized before construction; there is no engine insertion API to test. Different seeds are separate physical scenes: equality is required within each scene, not between different universes. The steppers are single-threaded; the thread gate exercises the frame's real kick threads.

Scratch mutations are prepared by `xtask/src/engine_judge/prepare_mutants.py`. Only the copied frame/anchor/sparse-hook sources are changed. The epoch setter is delayed only for EventCore; velocity rotation is removed while tide forcing stays; per-body drift flush is dropped; only the sparse kick hook's revision bump is removed. Child gate output is saved per mutant. Scratch controls run the same binary with the mutant environment removed.

Machine lines include uptime, power, thermal status and swap. The supplied sandbox denies sysctl swap/load/hardware access and thermal queries; the output preserves those denials. No thermal or target-device performance qualification follows from these runs.

The supplied sandbox makes the worktree administrative index read-only. Commits use the permitted common object/ref store and `GIT_INDEX_FILE=artifacts/runs/engine-judge/index`. The integrator should refresh the normal worktree index with `git reset --mixed HEAD` before working here; the branch commits hold the complete changes.
