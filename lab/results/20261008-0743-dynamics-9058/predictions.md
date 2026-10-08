# Predictions — run 20261008-0743-dynamics-9058 (kick cadence as a dynamical system)

Written BEFORE the decisive sweeps, after the instrument passed its controls
(pure-Kepler model-vs-truth 1e-10; truth matches scipy DOP853 to 2e-11; truth Jacobi drift 1e-12).

Question: the orbital kick layer (compiled Kepler drift + tide/secondary kicks, docs/law.md
"Perturbed motion", H0190: 32 kicks/orbit, 0.3 with averaging) — is its error a bounded
attractor or does it compound, as a function of (a) kicks per orbit K, (b) cadence
phase-locked to the orbit (K rational) vs golden-detuned, (c) kick flavor: frozen-at-centre
(F, the shipped Fermi-frame flavor) vs exact window integral (W, H0190's averaging)?

Scenes: A = background (a=0.3846, n_p/n_J=4.19, no low-order MMR), B = exact 3:1 (a=3^(-2/3)),
C = off resonance (a=0.486). Judge: Jacobi-constant error growth exponent (B12-style gate ≤ 0.2),
e-error, pericentre drift rate. 10^3 Jupiter orbits for the sweep, 10^4 for the decisive few.

Held-out predictions (none of these K/detunings tuned on):

- **P1 (locking compounds).** Flavor F at exactly integer K (1 or 2 kicks per orbit),
  scene A: Jacobi/e error grows ~linearly in t (log-log exponent near 1, above the B12 gate 0.2),
  while the same K golden-detuned stays bounded (exponent ≤ 0.2). Mechanism: locked kick
  phases sample the perturbation response coherently (second order in mu, but always the
  same sign each orbit); a badly-approximable cadence equidistributes the phase and the
  response error averages to a bounded oscillation.
- **P2 (windowed flavor safe below 1).** Flavor W at K = 0.3 (H0190's number), scene A,
  either mode: bounded (exponent ≤ 0.3) but with amplitude 10-100x the K=32 level;
  the cheapest K meeting a 1e-4 relative Jacobi bound at 10^3 orbits is between 2 and 8.
- **P3 (frozen flavor dies below K ~ 4).** Flavor F's bounded error grows like
  (n_J * tau)^2 (the perturber's motion inside the frozen window), so F degrades ~1/K^2:
  at K = 0.3 its error is orders above W's (prediction: > 100x); the freeze is only usable
  at high cadence. (This is the quantitative version of H0190's averaging insight.)
- **P4 (detuning heals, with a transient).** Flavor F, K = 1 - eps, scene A: the compounding
  rate falls monotonically with eps; by eps = 0.1 the run is bounded; and at eps = 0.01 the
  error first tracks the locked run then flattens after roughly ~1/eps kicks (the resonant
  packet), a transient that can still ruin a frame (the lens's blind spot).
- **P5 (resonance is the true kill zone).** Both flavors on scene B (exact 3:1) at any K:
  e-pumping diverges from truth by O(1) (r4/B17 known); on scene C (detuned) both behave.
  Control both ways: the instrument can fail and can pass.
- **P6 (wrong frequency, not compounding, off resonance).** For every bounded case the
  pericentre error grows ~linearly in t (a wrong averaged precession rate: modified-Hamiltonian
  signature) while e oscillates: error type is a wrong rate, bounded amplitude, no divergence.
  If instead ANY off-resonance case shows e growing without bound, that is compounding and
  the claim flips to "cadence choice is a stability question".

If P1 fails (locked = detuned everywhere), the honest result is: the kick layer is an
attractor at every cadence off resonance; the floors are the window error (W, ~1/K^2) and
the freeze error (F, ~1/K^2 with a bigger constant), and the cheapest safe cadence is the
measured K* — still a decisive input to q-cadence, graded on the numbers, not on P1.
