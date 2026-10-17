# Dossier — 20261017-1447-second-20261017-1330-redteam-68e7-506c (lens: second author)

**Claim.** The checker's named gold experiment is done: the two evaluation orders stay
bit-identical **under budget starvation and competing load** — rung `r5-starve`, frozen
before execution, **PASSES** (starved sparse at budget 1 and seeded 1..=97 ≡ unbounded
lockstep, starved lockstep ≡ unbounded sparse, cross-thread starved ≡ unstarved, the same
seeded stream under spinning hogs ≡ unloaded, and the allocator hosting `EventCore`
regions under its own least-slack schedule with one-event budgets, sabotage and 1/8
workers merging to exactly one `Chronon`), so representation.md §3's "identical bits" and
law.md's tie rule ("every schedule, budget and thread count pops the same sequence") are
now guarded on every axis this lab can reach; only the GPU arm remains M1-side.

**Bottleneck.** Not compute: the last unguarded half of a premise. The 68e7 checker
named this exact experiment as the one step to gold; this run deletes it. Expected gain:
none in speed; the premise moves from "guarded unstarved" to "guarded starved, loaded and
scheduled", and r5's adoption cost drops to committing two files plus one dev-dependency
line.

**Evidence.** All numbers regenerate with `regen.sh` (≈5 min: two full release executions
of both arms + verdict + lineage check). Machine: shared 8-vCPU Linux, 15 GB, ~3 GB free
at run time; every process stayed far under the 2 GB cap (the largest battle is 3500
bodies).

1. **The rung** (frozen at `r5-starve.md` before the decisive run; harness behind
   `work/patch.diff`): `R5S_OUT=… cargo test --release -p emergent-engine --test
   r5_starve -- --test-threads=2` → **11 passed** (91.3 s), and `… -p emergent-allocator
   --test r5_starve_alloc` → **3 passed**; `python3 lab/verdict.py r5-starve.md
   metrics.json` → **PASS; cpu-pair-starved, cpu-pair-loaded, alloc-sparse-starved passed
   every criterion** (positive passes, negative `fail ident`). The device: a `Starved<S>`
   wrapper answers every `advance` with budget 1 or a seeded xorshift budget in 1..=97,
   so `Battle`'s internal `run_to` drains the queue one event (sparse) or one chronon
   (dense) per call — 41,209,773 starved advance calls across the suite, up to
   11,954,478 in one battle (h3, budget 1): the slicing is real, not cosmetic.
2. **Coverage.** Eleven battle scenes — r5's frozen ladder verbatim (s0–s7, h1, h2) plus
   this run's held-out h3 (3500 bodies, q 1024, seed 13, scattered, div 16, k 10;
   23,987 contacts, 1,025 epochs, carries live) — and 27 allocator cells (islands1,
   galaxy, islands2 held out; workers {1,8} × sabotage × budgets {1, calibrated}, plus a
   loaded calibrated cell per scene: 3 spinning hogs, sabotage on, 8 workers).
   `identical_fraction` 1.0 / 1.0 / 1.0 (candidates), 1.0 (positive), 0.0 (negative);
   `covered_scenes` 11 / 11 / 27 — computed per config from its own rows (68e7's
   checker note 3 fixed).
3. **Lineage.** The starved sparse world digests equal the checker-verified 68e7 unstarved
   rows on 10/10 shared scenes (`reference-digests.json`; e.g. h1 `ca1a44203f8a`): same
   battles, same bits, one more axis starved.
4. **Load is real.** Loaded/unloaded wall ratio 1.18–1.68 across the suite (median
   ≈1.4–1.5 per execution; the range is per-execution wall variance on the shared box);
   the loaded starved call-count equals the unloaded same-seed call-count (e.g. h3
   633,511 = 633,511) — the budget stream itself is wall-clock-blind.
5. **The allocator arm, first for `EventCore`** (a 3-line dev-dependency addition, the
   run's only edit to a shipped file — additive, dev-only): 27/27 cells' merged
   world+log digests equal one `Chronon` over the scene union — including one-event
   budgets (1,562–2,360 units per cell), sabotage and the loaded calibrated cell.
   Rollbacks are racy at 8 workers (observed 1, 1 and 0 across this run's three
   executions); identity holds with and without them.
6. **The record regenerates.** A second full execution wrote byte-identical battle rows
   after dropping wall fields — every digest, counter and starved call-count, the
   1.2×10⁷-call streams included — and 27/27 allocator digests again with **0 digest
   flips**.

**Predictions** (`predictions.md`, written before the decisive run): P1–P4 and P6 held
(starved/cross-thread/loaded identity 1.0 everywhere; shifted agrees 11/11, late breaks
11/11). P5 held on its identity and starvation clauses (27/27 digests, 1,562–2,360-unit
budget-1 cells) and on its rollback clause in 2 of this run's 3 executions — the
rollback itself is racy at 8 workers (observed 1, 1, 0), which is the wall-fed-metadata
finding below, not a physics miss. **P7 held for the battle arm and half-held for the
allocator arm**, and the miss is the run's one new finding, diagnosed: allocator
*scheduler metadata* (units, merges, splits, rollbacks) varies across executions exactly
where the schedule is wall-clock-fed — calibrated-budget cells (the ops→time calibration
measures the box) and fixed-budget cells with 8 workers
(pick-order races) — while fixed budget + 1 worker is deterministic and the *digests never
move* (0 flips in 54 cell-executions). That is the shipped contract's own line
(allocator lib.rs: "Forecasts, sabotage and scheduling change speed, never results"):
the "never results" half is now bit-checked; the "speed" half is wall-dependent by
design, and no rung should ever gate on scheduler metadata as if it were canonical.

**What would make it wrong.** The rung judges `Outcome` equality (world+log+tide digests)
on the CPU arm; the GPU arm (`MetalChronon` under the same starved wrapper) stays
M1-side, specified in the rung file. The load arm spins 3 hogs — it contends (1.18–1.68×)
but does not exhaust the box; a harder starvation (budget 1 *and* hogs *and* 8 workers
together on the battle arm) is untested. The starved-random span is 97; a wider span or
per-call zero-budget probes are untested (budget 0 would need `advance` semantics
clarified — the trait promises progress, so it is out of scope). Cost of adopting: commit
`r5-starve.md` beside `r5-dense-order.md` into `lab/rungs/`, the two harness test files,
and the allocator dev-dependency line; zero law changes. Fit with PRINCIPLES: "a test
that cannot fail is a control" — the one-order-late negative breaks 11/11 through the
starved path, and the both-shifted positive still agrees, so the equality is about the
schedule, not a frozen law (principle 10, measure before claiming; the tie rule's budget
clause was claimed true and unguarded before this run).

**The lens.** A second author inherits the question and can over-trust the parent's
harness; the lineage check (10/10 digests) and the from-scratch second execution are the
guards used here. What this lens may have missed: the allocator arm's scenes are small
(256-scale, horizons 800–1200) — the merge/rollback machinery is exercised, but
giant-region scheduling under starvation (the `heavy_tail` scene class) is not; and the
GPU arm is untouched by construction.
