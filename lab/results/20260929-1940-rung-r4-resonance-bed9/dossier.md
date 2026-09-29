# Rung r4 — kicks keep resonances that averaging erases

## Claim
The design's event layer — exact Kepler cycles plus one analytic multipole tidal
kick per conjunction (the impulse of the truncated tidal field integrated over
one synodic window, evaluated at the conjunction's true phase) — reproduces
2:1 mean-motion-resonance behaviour (e₁ pumping within 5–18 %, phase-coherent ψ)
with ~0.58 kicks per orbit and **zero** dense-integration steps, while an
orbit-averaged layer and no-perturbation both fail: **PASS** on every frozen
criterion (`verdict.py`: conj-quad pass, conj-oct pass, averaged fail pump,ctrl,
none fail pump,ctrl).

## Bottleneck
Board #2 (stepping owned by cells, or no stepping) and #1 (what multipoles buy):
this rung is the red-team's named experiment making their silver gold — the
claim "kicks survive resonance" measured on the design's cheap path, not on a
dense integrator.

## Evidence (cloud container, Linux/x86, 4 vCPU, idle load; orders of magnitude only)
- Truth: 3-body float64 velocity Verlet, converged 600/1200/2400 steps per
  inner orbit — maxe1 and conc stable to <0.1 %; |dE/E| ≤ 1.4e-11 at 2400.
  R1 maxe1 0.15698 conc 0.4611; R2 maxe1 0.17350 conc 0.5136;
  C1 0.01030/0.0254, C2 0.01245/0.8186, C3 0.04414/0.8739.
- metrics.json (per config, frozen names): conj-quad pump 1.054–1.177,
  lib 1.630, ctrl 3/3, dense_steps 0, kicks/orbit 0.580; conj-oct pump
  1.053–1.070, lib 1.687, ctrl 3/3, dense_steps 0, kicks/orbit 0.567;
  averaged pump 0.058–0.064 (fails), ctrl 2/3; none pump 0.058–0.064 (fails),
  ctrl 2/3. The octupole term mainly buys accuracy on the phase-shifted case
  (R2: 1.18 → 1.07).
- Machinery checks: kick-integral quadrature GL24 = 4×GL48 to 8 digits;
  `averaged` precession on C1 = 9.0028e-5 vs classical quadrupole 9.0000e-5
  (truth 1.095e-4, i.e. +22 % — higher multipoles, as expected at a1/a2=0.34).
- Wall: <1.1 s for every config × all 5 cases (Python); truth 0.5 s (C).

Reproduce (each ≤ 60 s):
```
cd lab/results/20260929-1940-rung-r4-resonance-bed9
gcc -O2 -o truth truth.c -lm
python3 rung_r4.py truth      # writes data/, prints convergence
python3 rung_r4.py check      # quadrature + secular-precession checks
python3 rung_r4.py metrics    # writes metrics.json
python3 picture_util.py       # writes picture.svg
python3 ../../verdict.py ../../rungs/r4-resonance.md metrics.json  # -> PASS
```

## Predictions (predictions.md, written before the metric runs)
- Wrong: I predicted conj-quad over-pumps 1.4–2.2× (l=2 overweighting the m=2
  harmonic). Actual 1.05–1.18 — the truncation does not over-pump.
- Right: conj-oct in [0.8,1.35]; averaged/none fail pump (~0.06) with ctrl 2/3;
  C3 the risky control (it passed, 0.85); kicks/orbit ≈ 0.5; dense_steps 0;
  negatives fail as designed.
- Miss: both candidates pass — I gave the "conj-quad killed" outcome ~70 %.

## What would make it wrong
- The concentration metric is weak in both directions here: at exactly nominal
  2:1, `none` has a *frozen* ψ (conc 0.9999) and `averaged` drifts only −2.26
  rad over the run (conc 0.70) — both score lib ≥ 0.8 while failing the
  physics. The pump gate is what actually kills them. A frozen upper bound on
  libration_ratio would have caught over-concentration: the kick layer's ψ
  librates *more tightly* than truth (1.63–1.69×), and the controls' ψ
  phase-locking (truth conc 0.82/0.87 at ratios 2.55/2.15, forced-eccentricity
  locking) is **not** reproduced (0.10/0.19) even though the e₁ envelopes pass.
- Reconstruction caveat: the red-team's `e1_resonance.py` and exact ICs are not
  in this container; I reconstructed the cases from the rung text. R2 uses
  e₂=0.05, ϖ₂=4.0 (the reading where "w2" is meaningful); my truth conc is
  0.514, not the red-team's 0.867. Ratios are computed against my own truth.
- The kick integral is a fixed 24-node Gauss–Legendre evaluation of the
  analytic truncated field along exact Kepler arcs — no ODE is stepped
  (dense_steps = 0 literally), but a checker who counts quadrature nodes as
  "integration" would dispute the letter; the count is 24 evaluations per
  conjunction (~12 per inner orbit vs the truth's 2400 steps).
- 2D, coplanar, one perturber, μ=3e-3, 200 synodic periods; one seed per case.

## Cost of adoption, PRINCIPLES fit
The layer is exactly the design's cheap path: analytic generator + surprise
events, ~0.5 events per orbit per perturber, no stepping ("you don't advance a
ship tick by tick"; "no work for no reason, so no ticks"). Deleting the dense
integrator from the resonant regime is the 10× story: 2400 steps/orbit → 0.
It fits "Compute only surprises" and "Rough first, refine when a certificate
could break": the e₁ envelope is right to ~5–18 %, phase detail is not.

## The lens (what this lens may have missed)
Single-lens author, no adversarial case at higher μ or deeper in the resonance
where libration overlaps chaos; concentration-vs-drift ambiguity left inside
the frozen metric rather than attacked; the controls' phase-locking failure
(f Law ψ circulates where truth locks) sits below the gate and would surface
as wrong observed behaviour at ratios 2–2.6 — the next rung should freeze a
phase metric with an upper bound.
