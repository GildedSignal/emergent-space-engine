# Predictions — run 20261012-1227-dynamics-bd4e

Written before any run of the probe (`cargo test --release -p xtask b12_error_type -- --ignored --nocapture`,
in this tree, controls and plane in one process; nothing below was tuned on these traces).

**Instrument.** For each of B12's 16 frozen ships and each law, take the SIGNED relative Jacobi
error e(t) at the gate's own samples (200 periods, 8 per period). Compute:

- `beta`: slope of ln D(tau) vs ln tau over the top decade of lags, where D(tau) = mean_k
  (e(t_k+tau) − e(t_k))². A bounded/stationary error gives beta -> 0 (D saturates at 2 var), a
  random walk 1 (D ∝ tau), a ballistic drift 2 (D ∝ tau²).
- `z`: t-statistic of the mean increment over the second half of the trace, |mean δ|·sqrt(n)/std(δ).
  z > 3 says the increments have a systematic sign (drift), not just dispersion.
- `exponent`: the current B12 statistic (`fit::growth_exponent` on |e|), for contrast.

**Classification, frozen now:** per ship, drift if z > 3; else diffusive leak if beta > 0.65;
else bounded (no compounding). A law's verdict is the median class over judged ships.

**Why the classes must separate here (the physics I commit to):** Echo holds the Jacobi constant
exactly, so on these co-orbital chaotic ships the zero-velocity surfaces bound every state function
of the trajectory: planted-bounded's error is a function of a bounded observable, so its D must
flatten within the 200-period horizon (beta well under 1) even though its window maxima wander
enough to fool the exponent (0.49). planted-compound adds an unbounded random walk in the number of
encounters: nothing pulls it back, so beta ≈ 1.

**Predictions on cases not tuned on:**

| Law | exponent (today's statistic) | beta | z | class |
|---|---|---|---|---|
| echo | ≤ 0.3 or below floor; on Linux possibly > 0.2 (the reported echo failure) | < 0.4 | < 3 | bounded |
| planted-bounded | ≈ 0.4–0.5 (the known miscalibration) | 0.15–0.6 | < 3 | **bounded (must pass)** |
| planted-compound | > 0.5 | 0.8–1.15 | < 3 | **diffusive leak (must fail)** |
| planted-drift (DP, unconstrained) | ≈ 1 | 1.0–1.7 | > 3 on at least half the ships | **drift leak (must fail)** |
| plane (step default) | ≈ 1.03 (known) | **the open question** | ? | ? |

**My prediction for the plane, committed:** the error compounds, but as a DIFFUSIVE leak, not the
linear growth the exponent 1.03 suggests: median beta in [0.7, 1.2], z > 3 on fewer than 8 of 16
ships. (P3' shows the register moves 6e5–2e8 quanta per kick; I read those as geometry-dependent,
sign-varying per-handoff errors, i.e. a random walk in handoff count.) If instead median beta ≥ 1.5
or z > 3 on most ships, the plane has a systematic per-handoff Jacobi bias — a different and worse
defect, pointing at the handoff shear's sign, not the register's size. If median beta ≤ 0.65, the
plane's error is state-carried and B12's exponent alone convicted an innocent law: the gate, not the
plane, is broken, and the instrument passes both P2 controls.

**Failure modes I accept in advance:** if planted-bounded's beta lands above 0.65 (state diffusion
not saturating inside 200 periods), the trace-only instrument inherits B12's disease and this run is
a lead, not an answer — I will report it as such, not move the threshold.
