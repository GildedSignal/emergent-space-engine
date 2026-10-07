# Predictions (written before the adversarial plants run; the baseline table already regenerated)

The prior run's statistic (pooled Kendall z of |residual| vs pair gap, state-adjusted) reads ONE
channel: the Jacobi constant's error. My lens says: C_J is a first integral, constant along each
orbit; an error that displaces the ship ALONG its own orbit (a clock/phase error) lives in the
kernel of that functional and should be invisible to the whole gate — while compounding without
bound in the channel the game actually plays (encounter timing = synodic phase).

Cases (not tuned on; all my constructions are new):

- P1 Clock 1e-4: law = the exact conserving reference evaluated at t(1+1e-4). Phase error grows
  linearly to 0.02 orbit (about 2 R_H along-track) at the 200P horizon. Predicted: PASS,
  |z_pool| < 3. worst_err: bounded, no arrow — circular ships at integrator noise (~1e-12);
  eccentric ships possibly a bounded phase-locked oscillation orders larger (states are inertial,
  so a time-shifted state misses the primaries' rotation); must stay under the 1e-4 cap.
- P2 Clock 1e-3: same, 10x: 0.2 orbit (about 18 R_H) along-track at horizon. Predicted: PASS,
  |z_pool| < 3; worst_err bounded as in P1 (about 10x larger, still under 1e-4).
- P3 PhaseWalk: time offset delta(t) random-walks by +/-0.01 P per sphere-of-influence entry
  (the dual of planted-compound, which walks C_J by SOI entries and is caught at z = +27.65).
  Predicted: PASS, |z_pool| < 3; worst_err bounded as in P1 (oscillatory, under 1e-4);
  along-track error grows ~ sqrt(#entries), reaching several R_H.
- P4 AntiWalk: planted-compound's steps made anti-persistent (AR(1) increments, phi = -0.9,
  matched stationary variance). Effective leak shrinks ~(1-phi)/(1+phi) = 19x, but the rank
  test is scale-free. Predicted: FAIL, z_pool > 10 (anti-persistence does NOT hide compounding).
- P5 Step 95P: bounded permanent Jacobi offset 3e-9 switched on at t = 95 P (time-localized,
  then constant). Genuinely bounded -> must pass. Predicted: PASS, |z_pool| < 3.
- P6 (observation, already in hand): periodic 1e-7 passes at z_pool = -14.40: the null's
  exchangeability is violated 14 sigma in the decay direction; the gate's one-sidedness is
  load-bearing, not conservative decoration.

Quantifier channel (from the same runs): median and max along-track |x_law - x_echo| / R_H over
the first quarter (0-50 P) vs the last quarter (150-200 P) of samples, pooled over judged ships.
Predicted: for Clock/PhaseWalk the last-quarter median exceeds the first by > 10x (compounding),
while the gate's own worst_err stays bounded; for echo and planted-bounded both quarters sit at
their own bounded level (echo ~0; bounded: state-dependent, both quarters comparable).

Kill criterion for my claim (that the channel is gameable): if Clock or PhaseWalk FAILS the gate
through z_pool > 5 or worst_err > 1e-4, the arrow statistic survives my attack and the finding is
a negative result (report it as such).
