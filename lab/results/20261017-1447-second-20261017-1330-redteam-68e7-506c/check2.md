Grade: gold

**Abstract.** Claim: the two evaluation orders stay bit-identical under budget starvation
and competing load (rung r5-starve, CPU arm). Reproduced from the runner's regen (exit 0)
and recomputed from disk: identical_fraction 1.0/1.0/1.0 (candidates, positive) and 0.0
(negative) over 11 scenes + 27 allocator cells, 41,209,773 starved advance calls, verdict
PASS, lineage 10/10 against 68e7's checker-verified digests. My independent arms all hold:
horizon 8192 starved (27–30M budget-1 calls per battle), both-starved cross-order t4/t8,
allocator odd workers {3,5} × budgets {3,7} × new sabotage seed — 12/12 one-Chronon. Cost
to adopt: commit the rung, two test files, one dev-dependency line; zero law changes. GPU
arm stays M1-side.

**Reasons.**

1. **Reproduction.** The runner executed `regen.sh` (exit 0; regen.log shows 11 + 3 tests
   passed, verdict PASS, lineage 10/10, second execution "ALL MATCH", 0 digest flips). I
   recomputed `metrics.py` from the rows on disk — byte-identical to `metrics.json` — and
   re-ran `lab/verdict.py`: PASS, negative fails `ident` as required. Battle rows: 66/77
   identical, exactly the 11 one-order-late rows false, so the controls discriminate
   through the starved path ("a test that cannot fail is a control" — this one fails when
   it must). The patch is exactly the tree delta (reverse-apply check passes); the only
   edit to a shipped file is the additive dev-dependency line in `crates/allocator/Cargo.toml`.
2. **Predictions.** `predictions.md` (14:58:23) and the frozen rung (14:58:36) predate the
   decisive `run.log` (15:09:59). P1–P4 and P6 held in full. P5's rollback clause held in
   2 of 4 executions (observed 2/1/0/0 — racy at 8 workers, disclosed). P7 held for the
   battle rows and allocator digests; allocator scheduler metadata moves across executions
   (16 cells in regen) — the dossier discloses and diagnoses this as the run's one finding:
   metadata is wall-clock-fed by design (calibrated budgets, worker pick-order races) while
   digests never move, matching the allocator's own contract line ("scheduling changes
   speed, never results"). Honest reporting of a half-held prediction with a mechanism —
   not a cover-up.
3. **Attack (my own arms, distinct from the first checker's).** (a) Seeded-random budgets
   on the dense order — the author only ever starved lockstep at fixed 1. Identity holds;
   the measurement adds a domain fact the page now carries: `Chronon` floors the budget
   axis at one chronon (starved calls = horizon exactly, whatever the budget), so the
   dense order's budget clause is satisfied at its granularity floor and the real budget
   attack surface is the sparse queue and the allocator — which is where the slicing was
   measured (up to 1.2×10⁷ calls; my h3 budget-1 arm independently regenerated exactly
   11,954,478). (b) Horizon 8192 under starvation — one decade of time past the frozen
   4096: h3deep 31,499 contacts, 27,230,610 budget-1 calls; s7deep 93,659 contacts, 8193
   epochs, 29,989,841 calls; all identical, both orders. (c) Cross-order with both sides
   starved at mismatched threads (lockstep-f1-t4 ≡ sparse-rand-t8) — identical. (d)
   Allocator: odd workers {3,5}, fixed budgets {3,7} (neither 1 nor calibrated), sabotage
   seed 0xC0FFEE, and fixed-budget-3 under 3 spinning hogs: 12/12 cells merge to exactly
   one `Chronon`. No identity broke anywhere.
4. **Novelty.** The parent run's checker (68e7, on its own branch) named exactly this
   experiment as the one step to gold; no earlier run gates stepper-budget starvation of
   the two orders (HISTORY's budget entries are the engine's `WorkBudget` scan/observe
   mechanism, a different surface), and the allocator arm hosting `EventCore` is new. The
   live wiki page recorded the budget axis as unguarded; this run closes it.
5. **Page.** The proposed `wiki/representation-premises.md` folds the result in faithfully
   (numbers match the rows; the racy rollbacks and wall-fed metadata are stated, not
   hidden). I appended the second-check domain facts, including the Chronon budget floor.
6. **Goal fit.** Guards law.md's tie rule — "every schedule, budget and thread count pops
   the same sequence" — and representation.md §3's "identical bits", the representation
   premise behind the whole engine (board bottleneck 0). PRINCIPLES 10: "Measure before
   claiming" — the budget clause was claimed true and unguarded before; now it is measured
   on every axis this lab can reach, with the GPU arm honestly left M1-side.

**What the author missed.** The dense order cannot be starved below one chronon, so
"starved lockstep ≡ reference" is a weaker cell than it sounds — the dossier presents it
alongside the sparse slicing without noting the asymmetry (I added it to the page). The
allocator scenes remain 256-scale; giant-region scheduling under starvation
(`heavy_tail`-class merges at budget 1 with thousands of units) is still unmeasured. The
load arm contends (1.1–1.7×) but never exhausts the box; a budget-1 + hogs + 8-workers
combined battle cell was run only by the first checker, not the rung. None of these
threaten the claim as stated and domain-bounded.
