Working...
Check complete. `check2.md` written to the run folder; nothing else there touched, no git operations.

**Grade: gold** (blind second check, 45-min window).

**Reproduced** — in a clean scratch tree, rebuilt from the current bench source:
- All six global pair counts, both cell cases, both verifies, and the 2×10⁶ heap: **bit-identical** to the stored `cascade.jsonl`. Shipped anchor: 812.8 / 0.0024 / 0.9458 exact. `budget.py` regenerates every structural row (1.0e5 / 2.1e4 single-belt cores, 0.0767 skin cascade, 110 cores, 12/16 GB, 5.2 TB); timings move 1–6% with load.
- Frozen M1 anchor 4,345.4 µs verified in the original run's `kick.jsonl` (commit e0650db); the window-queue arithmetic cross-checks against the first checker's Python-heapq finding (0.52 ÷ 16.3 = 0.032 ✓).

**Adversarial** — the claims survived:
- Law off-calibration: +5.3% (X=4), +9.8% (σ_e/5), +8.8% (ρ×10); breaks only outside its stated domain (σ_e=0.1 → 0.47×).
- Cells soundness under stress (σ_e=0.1, X=1.2, 100 kicks, 177k pairs/kick; ρ=10⁻³): **0 mismatches**; the union-extrema bound is provably a superset.
- Clustered near-now heap keys: **591 ns/op, 3.2× dearer** than the run's uniform model → window-key term 0.107 cores, *above* the skin cascade — the keying rule is more load-bearing than claimed.
- 10⁷ corner: no completion in 170 s / 2 kicks — matches the author's skip.

**Named blemishes** (kept it from being clean, not from gold): the dossier's headline anchor timings (8,072 µs / 0.54) contradict the stored log (7,181.2 / 0.61) — stale prose, M1-implied 5.35 µs/pair unchanged; `main.rs` edited after the results file was written (my rebuild proves immaterial); prediction 4's [1,15] bracket missed 4× but was filed under "Held"; the cell-key row mixes 128-body and 10⁴-body granularities.
