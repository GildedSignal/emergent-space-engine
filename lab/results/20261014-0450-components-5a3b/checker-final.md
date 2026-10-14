Working...
Check complete. **Grade: silver**, written to `check.md`; the author's page corrected in place.

**What I did:**

1. **Reproduced**: applied `work/patch.diff` to a clean tree, re-ran `regen.sh` — every physics column bit-identical across all 45 keys (only µs timings wobble ±5%, which the dossier scopes to orders only). Verified the probe's integrand transcription line-by-line against the shipped `node()`/`quad()`/`EDGE`/`CAP`.

2. **Independently validated the oracle**: mpmath closed form (advance = 2(2K(m)/√(A+B) − π)) plus 40-dps brute quadrature agree with the probe and the shipped increments at four spanning keys; my probe at (7.801, 0.9) reproduces 81ca's recorded walk degradation to the digit — confirming the author's diagnosis that the p = 8 drift is the shipped walk's own error, not a transcription fault.

3. **Attacked beyond the domain**: one decade past the swept e (0.999999/0.9999999): N* = 34–39, ratio 9.4–10.5 — the O(1)-in-e premise flip survives. But at the true refusal edge (p → 6+2e, moderate e — the P4 regime the author's grid never reached, since their p = 4.5/6 keys hit the symbolic-circle branch), the ratio falls to **2.7–4.1×**, and the run's own (8, 0.94)/(8, 0.999) rows read 4.0/4.7. P4 half-holds; the headline "4.8–10.5× on the whole expensive band" overstates → corrected to 4.0–10.5× (p ≥ 20: 5.1–10.5×) on the page.

4. **Novelty confirmed**: the record's only named panel-count replacement was Carlson's closed forms; the floor itself was never measured. Carlson-table pricing confirmed sound.

**Why silver, not gold**: the headline range is contradicted by two rows of its own table plus the corner, and the floor was proven by per-key bisection against a GL16 reference — which cannot run per compile; the adoptable static edge rule (~1 geometric rung/octave + CAP + `cut()`) is asserted, not demonstrated. That demonstration is the one gold experiment, named in check.md and on the page.
