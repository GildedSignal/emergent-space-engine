# Rung r5-starve: the two orders stay identical under budget starvation and load (CPU arm)

Frozen by lab run 20261017-1447-second-20261017-1330-redteam-68e7-506c before its decisive
execution. This is r5's budget axis, the half the premise census left unguarded and the
checker of 20261017-1330-redteam-68e7 named as the one experiment to gold: design
[docs/representation.md](../../../../docs/representation.md) §3 ("Two evaluation orders of
the same event graph, with identical bits"); law.md's tie rule — "every schedule, budget
and thread count pops the same sequence" — is exactly the clause a starved schedule
attacks. r5 (dense ≡ sparse unstarved, PASSES) is the parent rung; this rung adds
starvation and competing load on the same harness and scenes.

**Question.** The same battle as r5 (free-fall frame, lattice contacts, integer tide kicks
at epochs, carries live), evaluated lockstep (`Chronon`) and sparse (`EventCore`): when
every `advance` does one starved unit — budget fixed at 1, or a seeded pseudo-random
budget in 1..=97, in either order — and when the seeded starved sparse stream runs under
spinning hog threads competing for the cores, do the world, log and tide digests
(`Outcome`) stay identical to the unbounded reference? And does the allocator's own
least-slack schedule, hosting `EventCore` regions with fixed budgets of one event,
sabotaged forecasts and 1/8 workers (plus a loaded calibrated cell), merge to exactly one
`Chronon` over the whole scene?

**Configurations.**
- `cpu-pair-starved` (candidate): r5's frozen scenes (s0–s7, h1, h2) plus this run's
  held-out h3 (3500 bodies), horizon 4096, four starved pairs per scene: sparse-random and
  sparse-fixed-1 against the lockstep reference, starved lockstep against the sparse
  reference, and sparse t4 starved against lockstep t1 (cross-thread under starvation).
- `cpu-pair-loaded` (candidate): the same seeded starved sparse stream (budgets 1..=97)
  run under 3 spinning hog threads, against the unloaded unbounded lockstep reference.
- `alloc-sparse-starved` (candidate): three allocator scenes (islands1, islands2 held out,
  galaxy), workers {1, 8} × sabotage off/on × budgets {1, calibrated}, plus one loaded
  cell per scene (calibrated budget re-measured under 3 hogs, sabotage on, 8 workers):
  27 cells, each the union of every region's world plus the merged log against one
  `Chronon` over the scene union.
- `cpu-pair-starved-shifted` (positive): both orders starved with the kick one chronon
  late (`with_epoch_shift(1)`). Shifted together they must still agree — a changed law,
  not a changed schedule.
- `cpu-pair-starved-late` (negative): starved lockstep unshifted against starved sparse
  shifted. It must disagree.

**Metrics** (`metrics.py` assembles them from the harness rows, one set per configuration;
coverage is computed from each config's own rows):
- `identical_fraction`: the fraction of that config's rows with equal digests.
- `covered_scenes`: battle configs — distinct scenes with contacts > 0, epochs > 0 and a
  live carry, from the config's own rows; the allocator config — cells with contacts > 0
  and units > 0 (each cell is one full starved scene run).

**Output.** `metrics.json`, plus the harness rows (`rows/r5s-*.json`, `rows/r5sa.json`).

**M1 extension (not executable in this lab).** The GPU arm (`MetalChronon`) under the same
starved wrapper on an M1; identical criteria. Out of scope here by construction.

```configs
cpu-pair-starved candidate
cpu-pair-loaded candidate
alloc-sparse-starved candidate
cpu-pair-starved-shifted positive
cpu-pair-starved-late negative
```

```criteria
ident behaviour identical_fraction >= 1
cover behaviour covered_scenes >= 11
```
