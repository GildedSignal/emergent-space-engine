Working...
Check complete — `lab/results/20261007-1106-inversion-e618/check.md` written, tree restored.

**Grade: gold.**

**Reproduced** (clean tree, `git apply work/patch.diff`): smoke and 8/9 sweep rows bit-for-bit on every counted field — headline row nc=12800 gives lon-rank>4 = **0.910** (p50/p99/max 34/97/114), occupancy 79.7/156, dist max 73; the decoupling row σ_e=0.01 gives dist gt4 = **0.000** vs lon gt4 = 0.546. Only timings differ. The 10⁶ arithmetic re-derives (k* ≈ 6.2×10³ → 448 GB vs the gold's 288 MB).

**Pre-registration verified:** predictions.md mtime 11:16:51 precedes both sweeps (11:18:42, 11:51:33), and contains a claim the data then broke (dist-rank ≤ 4; it hit 73) — genuine.

**Attacks, all confirming:** seed 8 (gt4 0.674, within the predicted ±0.15); σ_λ=0.005 — the direction the author ran out of time for (occupancy doubles to 40.3, gt4 0.829); isotropic ϖ (0.696 — mechanism is angular); and a new one: the gold never pinned the train's sort key, and in **mean-longitude order** (where overtakes/rebuilds actually live) partner rank is p50 223, gt4 = 0.991 at nc=3200 — the inversion survives every reading, conservatively. Solver split (`state` vs `state_halley`) is 1.1e-15 with zero rank disagreements.

**Why gold, not silver:** it falsifies the premise of an *adopted* gold (k=4 constant; the 300 MB store) at exactly the 10⁶ scale it was adopted for, with the mechanism measured (occupancy = nc·2ρ/λ-spread, linear in nc, 4 points) — and it lands before the pending `b-coorbital-cert` build, whose spec still says "rank 4". Adoption is one spec amendment: derive k from occupancy or order 2D.

**Author's misses** (in check.md): the gold's nc=800 evidence was uniform-λ — its bunched family was measured only at nc=200, so k=4 was already failing (8.6% > 4) at a scale the gold never ran bunched; sweep.log's occupancy numbers aren't regenerable by the shipped code (undisclosed iteration); "232 vs 233" was a different seed; the 10⁶ uniform-λ claim stays arithmetic, disclosed.
