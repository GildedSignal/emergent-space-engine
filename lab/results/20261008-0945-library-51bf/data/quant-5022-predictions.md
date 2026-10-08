# predictions.md — q-correctors (quant lens), run 20261004-0555-quant-5022

Written BEFORE the decisive (held-out) run. Tuned ONLY on T1 (0.55, e0.05, μ1e-3), T2 (0.70, e0.20, μ1e-3),
T3 (1.70, e0.05, μ1e-3). Variants tried on tuning seeds: kdk {2,4,8,16,32,64,512,1024,4096}, y4 {1,2,4,8} = 13
variants per seed (multiple-testing count, disclosed).

## Question

Fewer kicks per orbit at the same behaviour (board bottleneck 1): how far can the plane's kick cadence
(1/64 of the radial period, one rebind per kick) drop before behaviour breaks, and does a higher-order split
(Yoshida-4) buy anything at equal event count? Float prototype, faithful to crates/universe step.rs+force.rs in
the hierarchical regime (changeover never engages): exact Kepler drift in mean anomaly, midpoint impulse kick
of the planet's perturbation (direct+indirect), rebind per kick. Invariant J* = v²/2 − 1/r − μ/|r−r_p| − h_z
+ μ(r·r_p), verified conserved to 1e-13 by an independent RK4 on the raw ODE (rk4.c).

## Frozen gates (behaviour, not error size; controls on both sides)

- Reference per seed: kdk at 1024 events/orbit. (Cross-check y4-8 was tried and FAILED as a reference:
  its domdt is biased 7-57% low — that failure is itself a finding.)
- PASS(seed): |domdt − domdt_ref| ≤ 10% |domdt_ref| AND emax ≤ max(1.2·emax_ref, 1.2·e0+0.02)
  AND maxdJ ≤ 10×maxdJ(control kdk-64 on that seed).
- Positive control: kdk-64 must PASS every non-resonant held-out seed, else VOID.
- Negative control: kdk-4 on B1 (near 2:1) must FAIL (harness must be able to fail).
- Adoption bar (from the queue's intent, 10×-flavoured): one configuration passing ALL non-resonant
  held-out seeds with ≥ 8× fewer events than 64.
- A seed whose REFERENCE shows resonant e-pumping (emax_ref > 2×e0) is judged chaotic (B14 convention):
  excluded from cadence adoption, documented as the layer's boundary.

## Held-out seeds (never touched before this file)

- H1: a=0.62, e=0.30, μ=1e-3, M0=2.5  (near 2:1, strong conjunctions: min gap ≈ 0.19)
- H2: a=0.48, e=0.10, μ=3e-4, M0=1.0  (weak perturber, quiet)
- H3: a=1.95, e=0.20, μ=3e-3, M0=0.3  (exterior, strong, slow synodic beat)
- H4: a=0.80, e=0.10, μ=1e-3, M0=1.7  (tight interior, min gap ≈ 0.12)
- H5: a=0.55, e=0.60, μ=1e-3, M0=1.0  (high eccentricity)
- B1: a=0.6299, e=0.02, μ=1e-3, M0=1.0 (2:1 to ~1e-4 detuning; boundary probe)

## Predictions (frozen before the run)

1. H2 passes at 4 events/orbit (the weak-perturber regime is where cadence is cheapest); maybe even 2.
2. H1, H4, H5 need 64 (fail at 32): conjunction strength/eccentricity bind, not μ alone.
3. H3 needs 32 (16 fails on e-pumping, as T3 did).
4. B1 is judged chaotic (reference itself pumps e beyond 2×e0): excluded, boundary documented.
5. NO configuration reaches the 8× adoption bar across all non-resonant held-out seeds: the minimum
   uniform cadence is 32-64 events/orbit at μ~1e-3. Gain from plain cadence reduction: ≤ 2×.
6. y4 (higher-order split) is KILLED for this layer: at equal or fewer events its apsidal rate is
   biased far outside every gate (already visible in tuning: −8% at 24 events on T1, −57% on T2).
7. The J* error of the layer drifts linearly with horizon (alpha ≈ 1, rate ∝ μ·H·T) at every cadence
   tested, including 4096/orbit: the time-dependent midpoint kick is not extended-symplectic. The
   engine should expect a B12-style gate at μ~1e-3 over ≥10³ orbits to see ~1e-4..1e-3 of Jacobi walk
   (error type: compounding — principle 13), independent of cadence.
8. What would make the adoption story wrong in the OTHER direction: if H2 and H3 both pass at ≤ 8
   events, then a resonance-aware per-body cadence (dimensionless detuning + conjunction strength)
   is the live follow-up, not a uniform cadence.

Machine state: GitHub Actions cloud container, 2 vCPU x86, shared, 7 GB, ~1 GB used. Timings are not
the metric here: the cost metric is kick events per orbit (machine-independent, integer).
