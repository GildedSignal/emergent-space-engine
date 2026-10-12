Working...
Check complete. Verdict written.

**Grade: gold** — `lab/results/20261012-1621-second-20261012-1524-fermi-4b55-09a1/check.md`

**Reproduction**
- `soi_truth.py` re-run in a clean /tmp copy (45.8 s): `soi_truth_results.json` **bit-for-bit identical** to the stored record. Runner's regen.sh (exit 0) had already confirmed both original scripts regenerate bit-for-bit, including the superseded values (stale 54.40, sign-bug 5.985×10⁻³, stale headline 42,462 bits/s).
- The sign-flip diagnosis is correct calculus: residual `dth = λ_body − n_pp·t` has derivative `−dn`, so the shipped `t −= dth/dn` diverges from the conjunction root.
- Prediction ordering verified by mtimes: predictions.md 16:23:57 → instrument 16:25:16 → dossier/wiki 16:28.

**My adversarial cases** (6, several outside the author's domain)
- dt = 0.0375 (half their finest): **+0.31%** — truth converged.
- Hot belt σ_e = 0.05 (10×, untested by author): truth rises only ×1.3 → the 21 bits/s headline is robust in σ_e; but the Newton cross-check collapses to **0.34×** and the anchor to 4.0× — both cross-instruments are cold-belt-only (my Newton reproduces their 2380 exactly at cold settings, so this is a genuine regime limit, not transcription).
- μ = 10⁻⁴/10⁻²: smooth scaling (~∝ R_SOI^1.5); the k-secondaries extrapolation untouched.
- Occupancy-duration identity closes (2619 × 2.90 / 125.66 = 60.4 ≈ 60.5 inside) — no episode fragmentation.
- Belt sampler exact (uniform a, Rayleigh e); seeds 44/45 within ±2%; 10⁹ table arithmetic exact.

**Novelty/page**: no H_entry measures H_live; topic's first wiki page; every page number matches the JSON. I corrected the page in place (additions only): the cross-checks' cold-belt domain, and that 128 bits/rebind + ~10 bits/s player are assumptions bounding H_live ~11–100 bits/s.

Gold because it is exactly the experiment the first checker named as the one step to gold, done with controls the first checker never ran, on a record that now regenerates end-to-end from one code path — and my attacks confirm rather than break the headline. Nothing else in the run folder was modified; no git operations.
