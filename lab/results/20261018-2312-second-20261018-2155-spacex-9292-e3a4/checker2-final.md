Working...
Check complete — `check2.md` written, grade **gold**, tree restored to clean (`?? lab/results/` only, as at start).

**Verification performed:**
- **Reproduction**: applied `work/patch.diff` myself in a clean tree, built, and verified the runner's regen logs line-by-line against the dossier. Anchors land on 9292-checker's broken windows (arm A: 2.9226 %/0.3564 % vs checker 2.9227/0.3569); warp 0 repairs at stock through all arms; deltas are load noise (the engine adapts to its 12-ms budget), none load-bearing.
- **Source-level physics check**: `Seen::offset` is the root-frame retarded offset, `direction` is `aberration(toward, vo)` with current velocity — the probe's warp serve recomposes exactly the shipped row math, so the measured residual is the honest minimum.
- **Predictions**: `predictions.md` pre-dates the arms (file times); P1–P6 held, P2's KILL bar never approached; P4's unreached clause honestly reported.
- **Three adversarial arms, one outside the tested grid**: 3000 frames at β→0.87 (warp 0 at stock in 2.9×10⁶ pairs; drift *saturates* at max 1.25×10⁻³, so the stock estimate is conservative); 10× floor at full length (warp 2.8×10⁻⁵/row-frame; at the 100× floor 30× the 1/θ scaling — noted as a correction); seed 3 identical. All hold.
- **Novelty**: the displacement warp existed only as 9292's unmeasured design sentence; e6c9 flew coast only. This is the first flight, and it correctly narrows the checker's K-scaling tier to the naive store.
- **Page**: faithful to the evidence; appended my checker2 extension paragraph with the saturation and 100×-floor-scaling findings.

Gold stands: the checker-named experiment is done, survived both blind checkers' out-of-domain attacks, and its adoption is one design sentence (store offsets, compose the warp per frame) with no new mechanism.
