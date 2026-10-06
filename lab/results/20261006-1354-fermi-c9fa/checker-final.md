Working...
Check complete. `check.md` written to the run folder; nothing else there touched.

**Grade: gold.**

Summary of the check:

- **Reproduced** byte-identically from repo root (`budget.py`, 0.06 s); `work/patch.diff` is empty, matching the "no code" claim. `predictions.md` (14:02:02) precedes the decisive run (14:03:55–57).
- **Anchors all verified** against frozen evidence: 29 µs kick, 32.5 kicks/orbit and 114× averaging, 4 GiB cap, hits 0.0059/0.020 (re-derived from pair fields), 575–51,587 B/body r8 stores, 488 B/10⁶ convoy, shipmem reabsorption + `compact`. Hand-recomputed 175/153 cores and both S_live caps.
- **Predictions:** P1/P2/P4/P7 held; P3 partial (disclosed); P6 failed and honestly mined for the right invariant — I re-derived both scaling laws from the raw rows and they are correct.
- **My adversarial cases:** (1) per-body scar feed is uncertain 2× (`enc_per_body_orbit` = the pair product without the script's /2) — fill times halve to 0.84–2.9 d, no decision flips; (2) element-swap distinctions would flip memory to binding in ~0.5 h — anchored by the author but never exercised, the sharpest miss; (3) binding order flips to memory at 24-h orbits (8.4×10⁸ > 5.4×10⁸); (4) 100× density kills in 1.4 h full-population but bounded battle fractions return to baseline.
- **Novelty:** no prior compute-vs-memory sizing or S_live variable in HISTORY/docs; the run also independently confirms the board's ~190-core line at 175 (−8%).

Gold because it shows a premise wrong by an order of magnitude (the 10⁹ risk is kicks, not RAM, at the stated mix), is fully reproducible from frozen anchors, and adopts in one step as three sizing laws for B10/B18-at-10⁹ and the encounters design. The misses (2× constant, element-swap edge, 24-h flip) shift constants, not decisions.
