Working...
Check complete. `check.md` written to `lab/results/20261008-2031-dynamics-87da/` (the only file touched there; all my scripts stayed in `/tmp/chk87da`; no git operations).

**Grade: lead.**

**What held under reproduction and attack:**
- All five `enc.py` stages reproduce **bit-for-bit** (seeded RNG), ≤ 90 s each.
- The exact-rotation identity is real — verified through my own dense time-propagation path: per-synodic-period minima = g̃ at exact period-start phases, max rel error **2.7×10⁻¹⁰** (6 pairs × 24 periods, minima to 5.9×10⁻⁴).
- The leak *pattern* (0% / 59% / 100% at e = 0.05/0.1/≥0.2) reproduces in shape.

**What fell:**
- **Never-certificates invert.** 97.8% of the belt ensemble geometrically crosses (tight: 100%); for any coplanar crossing pair min_θ g̃ = 0 exactly. My refined measurement: **7/12 random belt pairs below 10⁻⁴** (min 4.6×10⁻⁶) against the reported 0.4% — "95–98% certified never, candidate set shrinks 20–250×" is backwards; a certificate dropping ~98% of eventual encounters is the r8 v2 failure mode itself.
- **The leak is the equation of center.** Deep minima sit at Δλ_true ≈ 0.001 rad *always*; the author's "conjunction" aligns mean longitudes (M₂−M₁ = ϖ₁−ϖ₂), off true conjunction by the |f−M| ≈ 2e scale (medians 0.15/0.21/0.45/0.59 rad). It kills the author's own slice, not any design element — law.md's tier already ends in "an exact per-pair distance check".
- **Record:** `gtilde.json` and `fixups.json` (both headline tables) have no generating script; shipped `st_b` even contradicts the dossier (`time_path_agree: 0.0`); stage f used negative window widths; the g̃-min percentiles coincide with the uniform-sampling floor.

Honest process (predictions pre-registered, P5 falsified and reported, v1 bug disclosed) — but the load-bearing quantitative claims are artifacts, and the rotation/continued-fraction structure was already in the design.
