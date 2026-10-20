Working...
Check complete. **Grade: gold** — written to `check2.md`, with one in-place correction to the author's wiki page.

**What I did (independent of the first checker):**

1. **Reproduction, exact.** `python3 kerr_shadow2.py` (12 s) byte-identical to the stored instrument output; regen's 14 assertions ALL PASS on my own regeneration; `work/patch.diff` applies cleanly; the cargo probe's 104 DEFL lines byte-identical to `shipped-defl.txt`. Predictions (22:15:46) predate the instrument (22:20:37); the P2 pre-run correction is disclosed.

2. **Independent physics attack.** Built the equatorial Kerr Hamiltonian from the textbook metric: null constraint H = 0 to 7e−13 with p_r = √R/Δ over 20k random states; tetrad launch algebra and φ̇ match to 1e−14 (my one mismatch was my own E-normalization bug — the instrument was right). A pure RK4 λ-integrator with no root logic agrees with the fate classifier on **1350/1350** classifiable bearings across 9 cases including the cap band and four rows outside the author's range (2.05M inside both rings, 2.1M, 3.3M, 4.2M). My own closed forms match the census at rim rows; at the α⁻-flipped row (χ=0.9, 2.1M) the general form (180°+α⁺+α⁻)/360 gives 80.87% vs census 80.89% while the author's |α⁻| variant gives 63.2% — its rim-only scoping is correct and necessary. Tangentiality boundary verified analytically: r_ph⁺(1/√2) = 2M exactly. No TRAPPED pockets anywhere.

3. **Page.** Faithful, under budget (10/15 current-best lines, 174/300 total), run-list de-duplication preserves all 22 unique ids. **Corrected line 12 in place:** "flips to under-cover" inverted the coverage direction — retro coverage is under-cover at both depths (at the rim the χ-blind law misses the entire 30.7° retrograde cap), and its fabrication is prograde-side, exactly 43.9° = the pro edge error.

**Faults recorded (none bar gold):** two inverted cover-direction glosses in the dossier text; the closed form's rim-only domain; the r15 negative bar "≥2.5°" needs per-row-max wording ((0.5, 20M) retro edge misses by 2.49°); a garbled P2 fragment in predictions.md; census equatorial-only (disclosed).
