Working...
Check complete. `check.md` written: **Grade: silver.**

**What was verified**
- **Reproduction, bit-exact:** my own flights on the runner's patched binary — K=0 and K=10⁴ seed 1 digests (`1b801358…`, `c9d83738…`) identical to the regen's; every census integer matches across three independent flights (author's, regen's, mine). Print-only confirmed; gather share 0.878–0.901 at 10⁴.
- **Predictions:** written before the flights (file order holds); kill criteria none fired; P2/P5 held with margin — but P1's constant (predicted K+61, measured K+76) and P3's near count (~61 predicted, 358 measured) missed without disclosure.
- **Three attacks, all held:** seed 7 at 10⁴ (786 FULL, alone 0.0006), at 10⁵ (786 and 6,284 FULL, alone 0.0000 both floors), and at 3×10⁵ — the top rung on a seed the author never flew (786/6,284 FULL, nn_p50 1.363e-5 vs seed 1's 1.357e-5, near 358 flat, RSS 1.57 GB < budget). Poisson cross-check: measured occupancy matches the uniform-angle law within 3% — the saturation is the scene geometry, not an artifact.
- **Novelty:** the wire-side census, capacity law (cells = 2π/θ_f exact), crossing rung (10³–10⁴) and ∝1/K law are new; 62c1 was canvas-side, 2df1 already built the deletion, no prior sky-saturation result in HISTORY.

**Why silver, not gold:** nothing was deleted or sped — the display-exact row-set deletion already exists (2df1) and the one-record unification is a design claim whose adoption (view far rows served from 687c's record) is unflown, with the formation/concentration regime unmeasured by the author's own admission. Gold experiment named: fly that record-served gather at fitted zoom, or close the concentration hole.

**Page correction (in place):** the author's `wiki/view.md` bracket claimed the record unification "is the one measured above" — restated as a design claim from built halves, with my seed-7 confirmations noted. Tree left clean; no commits made.
