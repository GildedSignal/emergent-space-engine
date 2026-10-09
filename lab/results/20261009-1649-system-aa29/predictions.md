# Predictions (held out)

Frozen before any evaluation of the held-out files. Calibration = `calib.json`
(mu 1e-3, e0 0.02, T 512). Detector: one CF pass; FLAG iff some convergent p/q
(q<=12, order=p-q<=4) has q*|alpha-p/q| < K_order, K = {1: 0.08, 2: 0.045,
3: 0.015, 4: 0.01} at mu=1e-3. Labels: LOCK = conjunction phase clusters after
linear detrend (lockrms < 1.0 rad); FAIL_pump = secular e-pump > 2.5x local
20th-percentile baseline; chaos = a_drift > 0.05 (overlap zones, excluded from
the pairwise claim and counted separately).

Held-out runs (already simulated, not yet evaluated in any form):
`ho_mu3e4.json` (mu 3e-4), `ho_mu3e3.json` (mu 3e-3), `ho_e005.json` (e0 0.05).

1. **Structure.** Detector vs LOCK agreement >= 90% on non-chaotic seeds, in all
   three held-out runs. (The detector computes the near-return structure; if it
   cannot read lock vs circulation, the unification dies.)
2. **Behaviour.** Detector vs FAIL_pump >= 80% on non-chaotic seeds, and the
   disagreement is dominated by detector-flagged seeds that are locked but not
   yet pumping (island interiors: window-blind pump), not by misses.
3. **Width law.** At mu = 3e-4 and 3e-3, rescaling K by (mu/1e-3)^(2/3) (B17's W
   scaling) beats plain K on LOCK agreement by >= 3 points. If plain K wins or
   the gap is < 3 points, mu^(2/3) is falsified as the gate's width law at this
   regime and the width is set by the cusp response, not the libration island.
4. **Blind spot.** The chaos fraction (a_drift > 0.05) at mu = 3e-3 is at least
   double that at mu = 1e-3 (overlap zones widen with mu). The pairwise gate has
   no answer there by construction.

What would make the claim wrong: if LOCK and the detector disagree broadly (P1
fails), the conjunction structure does not carry the resonance gate and law.md's
separate compiled-frequency detector earns its keep.
