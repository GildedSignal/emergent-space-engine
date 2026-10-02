# Predictions (written before the decisive run, 2026-10-02)

Bottleneck: fewer kicks per orbit at the same behaviour (board focus #1; today the plane
takes 64 kicks per radial period, `crates/universe/src/step.rs`; a kick ~24-29 µs on M1).

Candidates: **Gauss-node Picard collocation of the kick layer** (GP-sxm: m windows per
orbit, s Gauss-Legendre nodes each, impulses iterated to a fixed point, warm-started;
order 2s per window, within-window phase feedback) and **Yoshida-4 triple jump**
(Y4: 3 kicks per macro step; its extra and negative drifts are free because the drift is
the exact tube). Drifts stay free in both, as in the plane. Accounting: GP's kicks per
orbit = s x m x mean sweeps (every tide read is charged; drifts are not).

Tuned on: nothing (no free parameters). Case M1 (moon e0=0.05, 0.3 R_H, 12 orbits,
truth LF-512 cross-checked against dense RK4) is smoke/debug only; it is where the
first configuration died (below). All other cases are held out from any tuning.

## Original predictions (pre-smoke)

- M2 (moon e0=0.3, 0.3 R_H): LF-64 precession error < 2%; GP 1-window < 2% at <=9
  kicks/orbit; LF-8 > 10% (B14 fails). Jacobi bounded for all symplectic-family schemes.
- M3 (0.6 R_H), F1 (flyby), R1/R2 (2:1 resonance): GP keeps B13/B17 behaviours at
  >= 4x fewer kicks; confidence 60% on resonance (the window spans half the synodic
  period; under-resolved conjunction would under-pump like r4's fixed-arc kicks).
- Expected failure mode: sharp tides inside one fixed window (close encounters) — the
  changeover's (SyMBA) job, not the collocation's.

## What the smoke actually did (recorded before the decisive run)

- **GP with one window per orbit is killed** (principle 9: a configuration, not the
  method): precession error 101%, e off by 0.17 after one orbit. The tide along the
  orbit oscillates at the orbital frequency; a full-period window aliases low-order
  Gauss nodes.
- GP-3x4 (4 windows/orbit) matched LF-64's 0.61% at 49 kicks/orbit: a 1.3x cut only.
- Y4-12 (12.25 kicks/orbit): 1.22% precession, e_dev 2.6e-2, Jacobi oscillation 3.9e-4
  (vs LF-64: 0.61%, 2.4e-3, 3.4e-5) — 5x fewer kicks at 2x the error, both far under
  the 10% B14 gate; the Jacobi oscillation is a B12-size risk, flagged not hidden.

## Revised predictions for the decisive suite (M2, M3, R1, R2, F1)

- M2/M3: Y4-12 precession error < 5% (gate 10%) at ~5x fewer kicks than LF-64; LF-8
  > 10% (fails); Y4-6: 3-15% (uncertain). Y4 Jacobi oscillation up to ~1e-3 without
  secular growth.
- GP-3x8 / GP-4x8: precession error < 2% at 24-32 kicks/orbit (2x cut, below gold bar).
- Resonance R1/R2: LF-8 leaves B17 (pump ratio or regime); GP-4x2 and GP-3x4 keep pump
  ratio in [0.8, 1.25] and match the regime. Y4 is not run there: long macro steps near
  resonance are the r4 lesson (no within-window phase feedback).
- Flyby F1: GP-4 single window (~16 tide reads/passage) matches LF-64's dE/dL within
  0.5% at 4x fewer kicks; the tide is smooth over the passage, so the interesting
  number is kicks per passage, not accuracy.
- If Y4-12 holds M2/M3 and the resonance GP prediction fails, the scout answer is:
  higher-order splits with free drifts for the smooth regime, GP collocation inside
  passages, correctors left to the directed `q-correctors` lens.

Cloud Linux/x86 float replica; orders of magnitude only.
