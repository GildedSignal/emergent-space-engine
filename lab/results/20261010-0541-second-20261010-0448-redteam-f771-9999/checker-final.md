Working...
Check complete. `check.md` written to the run folder; nothing else touched.

**Grade: gold.**

**Reproduced exactly** (clean scratch tree, shipped scripts, empty patch): `binet_probe.py` regenerates the shipped record line-for-line (2.8 s); `r1w_run.py` regenerates the output and `metrics.json` sha256-identically (`ad519e7b…`, stable across re-runs, 41 s / 38 MB); `controls.py` matches (4.81e-6 quadrature, −2.68/−2.70 slopes); quick tie-out matches the shipped row (4.45e-4 / 1.93e-2 / 246). Predictions.md timestamps precede the decisive run by ~20 min; 7/10 held, all three misses disclosed and in the safe direction.

**Six adversarial probes of mine, all supporting the claim:**
- Fresh draw Random(20261011): m16 kill reproduces (0.9766); m32 = 0.9961 with exactly 1 per-seed fail — the author's Fermi hedge, not draw-luck.
- m=70 at (7,0.99) measured: 9.785e-4 at 1070 crossings — the "0.1% per-seed needs ~2× the 512 budget" extrapolation is now a measurement and holds.
- Moderate-e r_p<6M hyperbolic periapsides (grid missed): all pass with margin.
- binet-m8 measured dead (0.918) — the author had only asserted it.
- Old landing nudge counterfactual: 50.1% deflection error — invariant 2 is real.
- Below the e-floor: m32 fails per-seed at e=0.005 — the floor is load-bearing (flagged as missed).

**Named gaps** (none touching the central result): m8 has no metrics despite being a draft config; long runs are 12 cycles, not r1's frozen 10⁴, while the draft says "unchanged"; river/square/tiltonly not re-run; no picture; one wrong controls.txt pointer. Gold is contingent, as the lab protocol requires, on the second blind checker agreeing, and the adoption step is the integrator freezing r1w and re-running it in the shipped harness.
