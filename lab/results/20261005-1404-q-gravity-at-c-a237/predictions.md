# Predictions — gravity-at-c (run 20261005-1404-q-gravity-at-c-a237)

Written before the decisive matrix. Tuned so far (machinery + floors only): inst energy
floors on binary/system/flyby/thrust, news machinery exactness at t=0, one news sanity
run on the circular binary at c=10 and c=3.333 (bound, a=1.0006/1.0016, drift 5.6e-4/1.6e-3),
flyby seed geometry, thrust threshold. Nothing below has been measured.

Notation: β = v/c of the relevant orbit (binary: relative speed 1, so β = 1/c;
inner planet: β = 1/c). 1PN apsidal oracle per orbit: Δϖ_1PN = 6πGM/(a(1−e²)c²).

## P1 — naive retarded binary spirals outward, as Laplace said
Scene `binary`/`binary_e3`, ret config. I predict:
- β=0.1 (c=10): outward spiral; a grows by an e-fold in 1/(2πβ) ≈ 1.6 orbits, unbound
  (a>4 or a<0) within 2–8 orbits; energy drift O(1).
- β=0.3 (c=3.333): unbound within ~1–3 orbits.
- β≈3.3e-3 (c=300, "realistic" for tight binaries): measurable growth, a-growth slope
  per orbit ≈ 2πβ·k with k of order 1 (0.01–0.03), unbound within the 300-orbit run.
- Sign: a grows (outward), from the tangential component of the force on the retarded,
  lagging position.

## P2 — news keeps the binary bound and precession below the 1PN oracle
Scene `binary_e3`, news, β=0.1 and β=0.3. I predict:
- bound for the full 300 orbits; a within 0.3% of a0; max|dE| < 3e-3.
- spurious apsidal precession |⟨Δϖ⟩| ≤ 1e-3 rad/orbit at β=0.1, below the 1PN oracle
  6π/(1·0.91·100) = 0.21 rad/orbit by more than two orders; naive retarded's precession
  or spiral exceeds the oracle.
- news energy drift comes mostly from the delayed-force integrator (not symplectic):
  halving dt halves it roughly quadratically. (Not yet measured — dt study is part of
  the matrix.)

## P3 — system scene: news ≈ instantaneous for every orbital behaviour
Star + planet A (a=1, moon at 0.30 r_H) + planet B (a=2.2, e=0.1), 95 planet orbits.
- news vs inst: same bound/escape classes for all bodies; moon Jacobi drift within a
  factor ~3 of inst's; max|dE| within a factor ~10 of inst's floor (1e-8 × perturbation
  delays), i.e. < 1e-4 at β=0.3.
- naive retarded at β=0.3: the moon escapes or collides early (< 30 planet orbits),
  and/or system max|dE| > 1e-2, vs both other configs ≪ that.
- At β=0.1 news's Jacobi error growth exponent ≤ 0.2 (B12's bar), measured as the
  envelope slope.

## P4 — flyby through the Hill sphere: news matches inst's scattering
16 seeds, dt=2.5e-4. I predict: per seed, |v∞_out(news) − v∞_out(inst)| / |v∞| < 2% at
β=0.3 (the planet's own deviations from Kepler during the light time are the only news
corrections); naive retarded off by > 10% on at least half the seeds (encounter velocity
comparable to v∞ inside the sphere). Jacobi error: news within ~3× of inst, ret ≫.

## P5 — a struck source's news arrives at light-travel time, exactly
Thrust scene, Δv=0.06 at t_e=8, watcher at a=6, c=3.333 (light distance ≈ 5).
- news: watcher's field residual is exactly 0 (bit-identical twin runs) until the
  exact light-arrival t_arr = t_e + |x_w(t_arr) − x_A(t_e)|/c ≈ 9.5, then switches
  within one step (measured onset − exact < dt = 0.004).
- inst (today's plane): the residual departs from 0 immediately at t_e (onset
  detected at t ≈ 8.0–8.3), violating causality by the full light time (1.5 time units).
- naive ret: same causality violation direction as inst? No — I predict ret also reacts
  early (it uses the source's true retarded position, which includes the impulse as soon
  as t_ret > t_e, i.e. from t_e) — early by the light time as well.

## P6 — cost per kick and tube memory
- Cost per pair-kick: inst ≈ 30–60 ns; ret ≈ 3–4× inst (3 retarded iterations, each a
  tube evaluation); news ≈ 1.2–1.5× ret (one extra tube evaluation to now). All linear
  in N (measured at N = 64, 256, 1024).
- Memory: one version per source per kick epoch within the longest light window:
  versions = (D_max/c)/Δt_cadence. At c=3.33, D_max=9, dt=0.005: ≈ 541 versions ×
  104 B/ver ≈ 55 kB per source (probe's f64 tube); in the plane a version is the
  16-byte tube + epoch, and cadence is 32/orbit, so memory ≈ 16 B × 32 × (light time in
  orbits); for an outer-planet pair (light time ~ 1 orbit) ≈ 512 B per source.

## What would make news wrong
If P2 fails (news precession > 1PN oracle or unbound), the tube-extrapolated-present
representation is wrong at β=0.1 already — kill it. If P5 fails (arrival not at light
time), causality is not expressed — kill. If P3/P4 show news diverging from inst beyond
the stated margins, the "news = instantaneous in the tight limit" claim is wrong.
