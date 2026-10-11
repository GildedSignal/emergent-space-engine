# Predictions — run 20261011-1917-redteam-fb64

Written BEFORE the decisive sweep. Tuned on NOTHING below: the only case run so
far is the weak-field calibration scene (r_e = 10,000 M), used to fix my own
instrument (deflection rotation sign, the finite-u_start correction to
delta_inf, and the form of the per-doll bend memo — disclosed in the dossier).
The numbers below come from the analytic estimate
err_phase ~ Omega(r_e) * Delta_t_Shapiro * (r_e / D), Omega = r_e^-1.5,
Delta_t_Shapiro ~ 2M ln(4 r_e r_o / b^2), D ~ 3 r_e, and were written down
before `python3 attack.py sweep` was executed.

Held-out cases: r_e in {6, 8, 20, 60, 200, 1000} M (r_o = 4 r_e, 16 frames per
scene spanning one orbit, primary image, MEDIANS over frames with roots).
Player floor for reference: one pixel at 1080p over a 90-degree FOV is
1.5e-3 rad.

- P1  r_e = 6:    err_phase in [2e-3, 0.2] rad (estimate ~0.04).
- P2  r_e = 8:    err_phase in [1e-3, 0.15] rad (estimate ~0.03).
- P3  r_e = 20:   err_phase in [2e-4, 0.05] rad (estimate ~8e-3).
- P4  r_e = 60:   err_phase in [5e-5, 8e-3] rad (estimate ~1.5e-3).
- P5  r_e = 200:  err_phase in [1e-5, 1e-3] rad (estimate ~2e-4).
- P6  r_e = 1000: err_phase < 1e-4 rad (estimate ~1e-5).
- P7  The one-pixel floor (1.5e-3 rad) is crossed between r_e = 20 and
      r_e = 200 (medians).
- P8  err_fix < 1e-4 rad at r_e >= 20, and err_fix < err_phase / 10 at every
      r_e <= 20: the Shapiro delay is the dominant error term, and correcting
      only the arrival time collapses the error.
- P9  err_design (as-written design, generous per-doll bend memo) stays within
      ~2x of err_phase at r_e >= 60 (the memo is accurate in weak lensing) and
      may exceed it at r_e <= 20 (strong-lensing family ambiguity).
- P10 Newton survivor: zero failures and max <= 12 iterations on the flat cone
      in every scene; uniform closing bodies at beta up to 0.999: zero
      failures, mean <= 6 iterations; the frozen-seed negative control at
      beta = 0.999 fails at least one frame (the detector can see staleness).
- P11 Image multiplicity >= 2 at r_e <= 20 in >= 25% of frames (lensing adds
      crossings, as the design says; nothing gates image switching).

KILL CRITERION FOR MY OWN ATTACK (pre-registered): the premise SURVIVES and I
report that, if median err_phase < 1.5e-3 rad at every r_e >= 6, OR if
err_fix is not >= 10x below err_phase at r_e <= 20 (the delay is then not the
dominant error and the "missing arrival delay" story is wrong).
