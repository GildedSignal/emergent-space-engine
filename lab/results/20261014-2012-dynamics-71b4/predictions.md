# Predictions — 20261014-2012-dynamics-71b4

Written before the decisive runs (32 bodies, horizon 400 parent orbits), after
calibration pilots on 8 bodies (machine verified: clock second-order, gate
replicates 54d9's walk). The decisive question: does the impulse-quantum
trigger (524e D) walk in a kernel whose clock control stays bounded (54d9's
midpoint machine)? The wiki's standing reading of 524e says no differential
walk; that was measured in a machine whose own clock compounds (×2.27 per
horizon doubling, 524e's checker).

- **P1 (control):** rule A (clock) stays bounded: slope median ≤ 0.05, p90 ≤ 0.2 at rates 2–8 kicks/body-orbit, H=400.
- **P2 (replication):** rule C (54d9's analytic gate) walks: slope median ≥ 0.5.
- **P3 (the discriminator):** rule Q (impulse quantum) walks in the bounded kernel: slope median ≥ 0.3 at rate ≈ 2/orbit, H=400, at BOTH sensor rates WS=128 and WS=512. A clean median at 100 orbits (WS=512 pilot) is a transient, gone by 400.
- **P4 (mechanism split):** Q's walk is modulated by the sensor's fire-time resolution (slope rises as WS coarsens), while C's is not (its interval is exact at any WS).
- **P5 (cost):** at matched kick rate, Q's D at H=400 exceeds the clock's by ≥ 10× (the trigger's error×kicks frontier does not hold at long horizon).
- **P6 (kill criterion for my own claim):** if Q's slope median ≤ 0.1 at H=400 at both WS with all 32 bodies, 524e's reading transfers to bounded kernels and the walk was my artifact — report as such and stop.
- **P7 (phase):** the gate's firing phases show higher circular concentration (lock) than the trigger's; the trigger walks without hard phase-locking (its increments' spread stays large while it walks), so the two walks are not the same fixed-point mechanism.
