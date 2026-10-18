Working...
**Grade: gold** — written to `check2.md`, with two scope corrections folded into the author's `wiki/calendar.md`.

**What I verified:**

1. **Reproduction** — applied `work/patch.diff` to the clean tree; my own `train shipped` run is bit-identical to `raw-train.txt` (every census line, 503,014 kicks, max=17 at g=3, C50 58.2→2.2×), and `rule.py` rerun reproduces both dossier tables digit for digit. Controls pass everywhere (refactor IDENTICAL, 4/4 + 300/300 on-grid, refused 0).
2. **Predictions** — `predictions.md` (23:36) predates all outputs (23:50+); P2 held (58.2× vs "within factor 2 of 57×"), P5 held, misses honestly reported. The patch saved 8 s after the dossier is behavior-neutral: the runner's regen on it reproduces the earlier smoke outputs exactly.
3. **The artifact** — confirmed at the source: b4a8's `calendar.rs:152` prints steps as `2^{ilog2}`, so the true min 5.2995×10⁹ became the "4.3×10⁹" low end of the page's "[4.3, 5.9]×10⁹" spread.
4. **Adversarial (4 fresh arms, GENS=12)** — `c1e1` (one exact circular orbit): **2,700 distinct steps, battalion 1, every generation** — the od-4 premise dead at its limit; its σ=3.9% is the pure-angle U_P term at fixed radius, and its birth wave is the *strongest* (C50 82.5×). `seed2`: wave reproduces (57.3×→2.1×). `wide15` ([1,5) AU, outside the author's band): **σ jumps to 28.5%** — "draw-invariant 8–10%" is the [2,3) band's property, not the law's (still no battalions). `e300` (σ_e×4.3): σ 7.0% — the e-draw is no dial either. slope/σ = 0.26–0.42 across all arms: shear tracks the spread, so "spread-independent lifetime" holds only across the sweep's narrow σ range — decision unchanged.
5. **Novelty & fit** — first measurement of the page's open od 4 and the checker-named census; premise shown wrong, adoptable in one step, no code cost. Tree restored to the runner's clean state.
