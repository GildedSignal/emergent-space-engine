Working...
**Grade: gold** — written to `check.md`. The check is complete; the tree is restored clean (only untracked `lab/results/`, no commits).

**What I verified:**

- **Reproduction, bit-level.** Applied `work/patch.diff` myself in a clean tree, built (10.9 s), flew 13 of my own flights plus the runner's 29-flight regen. Every digest pairs across all arms at every cell; off/on digests equal d31c's recorded lineage (`df20c524`/`be96cd53`/`d166a8da`), chaining the off arm to the shipped engine. The dossier table matches `out/grid.log` line-for-line; I recomputed every ratio: on/state 1.387–1.458 (never ≥1.5 — the split claim is exact), on/full 2.070–2.150, shipped→full 2.99–3.17.
- **Predictions.** `predictions.md` (03:58:18) predates the decisive grid (03:59:51). All five theses held; two band tops spilled ~1% (P2 17.0 vs 17.21; P3 2.95 vs 2.99) — disclosed numbers, mechanisms exact.
- **Adversarial.** Seed 42 (never flown); **N=3×10⁵** — a decade past the author's domain: 32.86→22.69→15.88→10.82, digests pairing, RSS 719 MB; a 12,000 s deep cut (18,416 kicks) proving no cache leakage past `start`; `stateonly` at 10⁵ composing exactly; planets-only suite with the new refuse-to-arm build: 77/0 (mine).
- **Code.** Off arm verbatim structurally; the constants-cache guards are exact by construction; the Err-seam fix d31c's checkers demanded is real (`PlanetsAt::build` now returns `Option` and disarms on any live `Err`) — diffed against d31c's own patch, this run adds only the two knobs, counters, cache, state path, and seam fix.
- **Page.** Fold-in faithful (one block + one Runs line); no correction needed.

**Gold rationale:** the components-4643/d31c precedent — checker 2's ≥1.5×-from-reads premise is killed (1.39–1.46×, pre-registered), replaced by the measured right representation (shared per-body recomputes) delivering 2.07–2.15× digest-identical, adoptable in one step, with d31c's adoption blocker closed in the same patch. Named misses: regen overwrites the author's per-flight `.txt` files (session survives in `grid.log`), 10⁶ unflown, and the sub-8 µs floor is Fermi, not measured.
