# Predictions (written before the decisive run)

Harness: my own CR3BP scene (Jupiter: mu 1e-3, sep 5.27e8, R_SOI = sep*mu^0.4, R_H = sep*(mu/3)^(1/3)),
12 chaotic ships on circular orbits at sep*(1 ± (1.5–3)*R_H/sep), >= ~20 SOI hits on the coarse P/8 grid,
200 planet periods, 1601 samples per ship. Reference = DOP853 rtol 1e-13. The judge series is the law's own
Jacobi drift e_j = |C(t_j) - C(0)|/|C(0)|, as in handoff.rs.

Statistics compared:
- EXP: faithful port of xtask fit::growth_exponent (window max, 16 log windows, first 10% dropped). The frozen gate's statistic.
- VR(tau) = Var(e_{t+tau}-e_t) / (tau * Var(de_t)): the persistent share of error increments (Lo–MacKinlay
  variance ratio; bounded -> 0 at large tau, walk -> 1, drift -> grows with tau). Decision at derived tau*,
  threshold 1/2 = midpoint of the two model values (not fitted), margins in pooled standard errors.

Held-out predictions (none of these series has been generated yet):

P1 (inversion reproduces). On chaotic ships, EXP(planted-bounded) > EXP(planted-compound), both in
    [0.2, 0.6] — the wrong way round (law.md documents 0.49 vs 0.31 on the frozen ships).
P2 (the float reference compounds). DOP853 at rtol 1e-11 and 1e-12: EXP in [0.4, 1.2] and VR(tau*) in
    [0.6, 1.3] — the reference itself fails at every tolerance (redteam-b12-stat's finding, on my box).
P3 (VR separates where EXP inverts). Median-ship VR(tau*): planted-bounded and iid-noise(1e-11) < 0.15;
    planted-compound > 0.8; separation across the 1/2 line >= 3 pooled se.
P4 (the leak sits at the floor). A drift leak of 1e-12 per period (2e-10 total) under a bounded chaotic
    error of amplitude ~1e-11: VR(tau*) lands in [0.25, 0.75] — marginal, because drift detection has an
    amplitude/horizon floor; the larger planted-drift (1e-10 total) fails clearly (VR > 1).
P5 (the floor's shape). Sweeping drift rate over 1e-13..1e-11 per period at bounded amplitude 1e-11, the
    fail/pass boundary crosses between 3e-13 and 3e-12 per period, and scales ~ amplitude/horizon when the
    bounded amplitude is doubled (boundary moves by ~2x).
P6 (machine independence). A one-ulp nudge of every ship's initial state changes no verdict of the VR rule
    (EXP verdicts may flip: its bounded-vs-compound ordering is ulp-fragile per the redteam).
P7 (kick is gross). planted-kick (planetocentric v x1.001 per SOI entry): VR rises with tau (multiplicative
    compounding), EXP >= 0.8; fails everything.
P8 (sample complexity). Pooled se of median VR(tau*) over 12 ships in [0.08, 0.25]; if > 0.17, 16 ships
    (the gate's count) are needed for a 3-sigma 0-vs-1 separation, and I say so.

Kill criterion for this run: if VR(tau*) does not separate planted-bounded from planted-compound by >= 3
pooled se on my ships, the persistence statistic dies on this scene and the dossier says so (a failed
configuration, not a failed method: the next candidate is the KPSS-style stationarity test).
