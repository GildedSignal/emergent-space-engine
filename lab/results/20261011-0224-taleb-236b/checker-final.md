Working...
Check complete. **Grade: gold** — written to `lab/results/20261011-0224-taleb-236b/check.md`.

**Basis:**
- **Reproduced:** `python3 probe.py [R]` gives bit-identical metrics (ex-timing) at all three contact radii, 26 s each.
- **Independently re-derived** S1/S4 on the author's exact fleets with my own Kepler solver, contact finder, and rank instrument (as the dossier itself invited): S1 exact (80 contacts, 2.5% at rank ≤4, median 869/1600); S4 structurally identical (928 vs 871 contacts — my denser sampling catches ~6% more; frac 3.45% vs 3.33%).
- **Adversarial:** fresh seed 777 → 0.0% at rank ≤4; trigger boundary (cone 0.61) → still 95% beyond rank 4, so the cone trigger cannot gate rank-4 vs pairwise; shear control at 10× horizon → max rank 3 (no strawman). Also checked the mean-longitude ordering variant analytically — the non-locality is ordering-insensitive.
- **Predictions:** written 02:38:26, before all metrics (02:39+). P1/P4/P5/P6 held; P2/P3's quantitative sub-bounds missed and were honestly disclosed, none load-bearing.
- **Novelty/goal fit:** no prior coverage in HISTORY.md, the board, or the build lens `b-coorbital-cert.md` (which tests only shear-regime scenes); this is the pre-freeze falsifying probe for the board's top scaling risk, adoptable in one step (amend the build lens before it runs).

**One discrepancy found:** the side claim "59 conjunction pairs in S4 miss by 0.02–0.33" is not reproducible (natural definition: 10,077 pairs, misses 1.04e-4–0.54) — but its conclusion survives independently (smallest conjunction miss still exceeds R), so the grade stands. Also noted for the integrator: the trigger's separation is less sharp than claimed at the boundary, and the S4 truth slightly undercounts.
