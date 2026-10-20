Working...
Check complete. **Grade: gold** — written to `check.md`, with one page correction and a budget trim.

**What I did:**

1. **Reproduced** — `sh regen.sh` exit 0 in ~12.5 s, every dossier number asserted (ALL PASS); `instrument-out.txt` byte-identical on my independent rerun; probe payload byte-identical to `work/patch.diff`; tree clean after.

2. **Verified the physics independently** — the load-bearing new claim (the retrograde cap is dark, census ≠ α⁺−α⁻ arc inside the ring) checked three ways: hand tetrad derivation from the metric, hand root-structure analysis of R(r) at two rim rows (reproduces 46.2%/42.95%), and an independent λ-integrator of Carter's radial equation — **0 fate mismatches on 2000+ random bearings** including 32 cap-band spotlights.

3. **Attacked outside the author's domain** — (0.9, 2.1M): census 80.86% matches my hand derivation exactly but the closed form (180°+α⁺−|α⁻|)/360 gives 63.2% — the closed form is a rim-row fact, not a law (breaks where α⁻ flips prograde-side); (0.3, 3.4M) outside the ring confirms the old convention is right there (scope correct); (0.998, 3.998M) confirms cap→0 continuity at r_ph⁻; the √2/2 ergosphere boundary is exact (r_ph⁺(√2/2) = 2.000000M).

4. **Novelty** — read the parent run's check.md off its branch: the first checker used exactly the α⁺−α⁻ arc this run kills. This run executed the checker's named gold experiment in full, and the decisive held-out prediction (P3 census) held exactly.

5. **Page** — corrected the closed-form overstatement in place (added where it fails), trimmed Current best from ~50 lines to 10 (page now 174 lines); all new numbers verified against the instrument record.

**One risk flagged for the integrator:** r15 must reference the census, never the closed form — and the χ-blind negative is carried by the edge arm, not the arc arm (which it passes at χ=0.5/3.2M).
