Working...
Check complete. Verdict written to `lab/results/20261010-2052-library-2d94/check.md` — nothing else in the run folder touched (reproduction ran in a `/tmp` copy since the dossier's command overwrites `metrics.json`).

**Grade: silver.**

What held under attack:
- **Bit-for-bit reproduction** (metrics + run.out identical, 6.0 s); predictions.md timestamped 80 s before the decisive run; all 7 library quotes verbatim in the export; Δt² fixed-error scaling and both-end controls verified.
- **The steep-tide case** (10× perturber, e=0.9): certificate holds, win ~2.1× — no burst.
- **The sleep term** (0 kicks at zero tide) — untouched by any attack.

What broke:
- **Clairvoyance.** The trigger reads the RK4 truth. Oracle-free with a naive tide integral, the band overshoots 4–13×w. It survives only with a linearized-deviation estimator (tide + Kepler gravity-gradient) — 5.7 kicks/orbit at 1.016×w vs the clairvoyant 5.8 — a form the dossier never specifies.
- **The certificate claim dies in a truth-free closed loop.** At the author's own 10-orbit horizon: band 5.7 kicks at 5.3e-3 error vs fixed j=4's 3.9 kicks at 6.8e-3 — the band *loses*; at 100 orbits error is ~500×w for both. Anchor residuals compound (principle 13), so the 2.8–6.7× headline is an open-loop upper bound and "gates judge a stated bound" does not transfer to the engine.
- Minor: the printed ratio rule ("equal-or-better") wasn't the one used for 2 of 6 headline numbers (all conservative, none inflated), and the run silently coarsened truth from the pre-registered T/16384 to T/8192.

The named gold experiment: band trigger inside a truth-free loop on the engine's orbit-averaged kick layer, ≥100 orbits, multi-seed — my first-order probe fails it, so adoption before that run would be premature.
