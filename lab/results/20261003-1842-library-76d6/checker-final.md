Working...
**Grade: silver** — written to `lab/results/20261003-1842-library-76d6/check.md`, nothing else in the run folder touched.

**Reproduction:** `python3 kicks.py` — all 81 rows bit-identical to `kicks-out.txt`, controls both sides (positive 1e-4, negative 0.1254), 61 s on the shared container. Oracle independently re-derived: ϖ̇ = Ω̇ + ω̇ = (3/2)nJ2(R/p)² at i=0 → the author's 3π form is correct; Vallado's 6π is the node-referenced singular limit. `predictions.md` (18:47) precedes the decisive output (18:52); patch.diff empty.

**My attacks (5):**
1. **Sub-grid gap — the decisive defect.** The author's grids skip below their first pass; contiguous sweep shows lf2 passes at **6** kicks/orbit at e=0.1 (not 8) and **29** at e=0.6 (not 32), stable across 100/200/400 orbits. The "directly adoptable compiled integer table" ships wrong integers; adopting 8 where 6 passes wastes a third of the low-e kick budget.
2. **Band sweep:** minima at 1e-2/1e-3/1e-4 — lf2 6/7/10 vs y4 18/24/24 vs y6 14/42/56. Ordering never flips; gap widens. Probe floor ~6.5e-5.
3. **e=0.9 extreme:** nothing passes ≤192 kicks/orbit — uniform stepping dead for all methods; probe validity is e ≲ 0.7, unstated in the dossier.
4. **Combined held-out e=0.6/J2=1e-2:** same ordering and ratios.
5. **Horizon stability** of corrected minima; noted y4's non-monotonic rel near the band edge.

**Why silver, not gold:** the held-out prediction P2 failed in direction (author-reported), and the shipped integers are wrong — though the direction of the claim (compositions need *more* kicks; the kill of "higher-order splits" under focus item 1) is robust and got stronger under attack. One experiment to gold: contiguous grids (6/29 already confirmed) plus the r9 averaged-tide kick layer, pre-registered. Novelty clean: no H entry tests composition order at equal kick counts; H0190 measured counts only.
