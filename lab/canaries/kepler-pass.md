# Rung canary: a Newtonian Kepler orbit at a fixed step (expected verdict PASS)

**The question.** Over 10^4 orbits at a fixed step of 1/200 of the period, which integrator keeps a Kepler orbit (e = 0.5) bound, without secular energy growth, at 200 steps per orbit?

**The case.** 2D, one test body, the central mass fixed at the origin, units GM = 1 and semi-major axis a = 1, float64. Start at periapsis: position (0.5, 0), velocity (0, sqrt 3). Fixed step h = T/200 with T = 2 pi, for 2,000,000 steps (10^4 orbits). Only this case. Every configuration is run on it.

**Oracle values (exact).** Specific energy E0 = -0.5; angular momentum L = sqrt(0.75) = 0.8660254037844386; period T = 2 pi; apoapsis radius 1.5, with speed L/1.5 = 0.5773502691896258; initial speed sqrt 3.

**Configurations.**
- leapfrog: kick-drift-kick velocity Verlet. Half kick, full drift, half kick.
- euler: forward Euler, x += h v and v += h a(x) both from the old state. It is a negative: a control that must fail.

**Metrics,** all computed from the state after every step, with E = |v|^2/2 - 1/|x| and dE = E - E0:
- energy_growth_exponent: take 20 windows with log-spaced edges from t = 0.1 t_end to t_end (the last 90% of the run). In each window take m = max |dE|, floored at 1e-16. The exponent is the least-squares slope of ln m against ln t, with t the geometric mid-time of the window. Secular linear drift gives 1, bounded oscillation gives 0.
- bound_fraction: the fraction of the run before the first step with E >= 0 (1.0 if there is none).
- steps_per_orbit: total integrator steps divided by the number of orbits (10^4), counting every substep.

```configs
leapfrog candidate
euler negative
```

```criteria
# id kind metric op threshold
E1 type energy_growth_exponent <= 0.2
B1 behaviour bound_fraction >= 1.0
C1 cost steps_per_orbit <= 256
```
