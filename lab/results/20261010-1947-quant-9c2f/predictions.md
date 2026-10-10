# Predictions — run 20261010-1947-quant-9c2f

Written before the decisive experiment (the memory-curve computation on the dumped
streams). Already observed before this file (grounding only, both from the frozen gate
itself): `behave B12` on this Linux box fails `planted-bounded` at median exponent 0.353
(worst 1.471, worst err 1.27e-5) and `planted-compound` at 0.416 (worst 1.654, worst err
9.80e-7). The P2 ranking inversion (bounded 0.493 > compound 0.305, on the integrator's
machine) did NOT reproduce here: the exponent's verdict moves with the machine. Nothing
below has been tuned on any memory-curve output.

## The instrument under test

Per ship, from the law's own answers only (no reference): e(t) = (C_J(t) − C_J(0))/|C_J(0)|,
a(t) (semimajor axis in separations), n(t) (encounters: inside 3 R_H after outside).
The **memory curve** M(Δn): for pairs of samples with encounter separation ≈ Δn and
a-values matched to width w, the median |e(t₂) − e(t₁)|, extrapolated to zero a-separation
(intercept, so ε's gradient in a does not confound). A law whose error is a function of the
current state has M flat in Δn; a law whose error carries memory (a walk in the encounter
count) has M rising.

## Predictions

- **P1 (flat for state-only).** For echo and planted-bounded, the memory-curve log-log
  slope over Δn from 2 to the top bin is within ±0.15 of 0, and the intercept stays at or
  below the float floor scale (echo ≤ 1e-13; bounded: the curve may sit higher, but it does
  not rise with Δn).
- **P2 (rising for memory).** For planted-compound, the log-log slope is in [0.3, 0.7]
  (a random walk in n gives 0.5), and M at the top Δn bin is ≥ 4× its value at the bottom
  bin.
- **P3 (separation).** At the top Δn bin, M_compound ≥ 4 × M_bounded (two doublings).
- **P4 (slow leak at the requirement threshold — the case that killed the recurrence
  ratio).** A synthetic leak added to echo post hoc, with unit steps δ* chosen so the walk's
  spread reaches the gate's 1e-4 budget at the median ship's total encounter count
  (δ* = 1e-4/√N_max), is still flagged: memory slope ≥ 0.3 and top-bin M ≥ 4× echo's. If
  the instrument cannot see the leak that exactly spends the budget at the horizon, it has
  no teeth and the horizon must be derived longer — that calculus is the deliverable either
  way.
- **P5 (the classic alternative fails — negative control on the toolbox).** The
  variance-ratio / unit-root view of increments reads planted-bounded as a random walk too
  (VR(k) ∈ [0.7, 1.3] for both bounded and compound): the state-only error inherits the
  diffusion of a, so no unit-root statistic can separate them. Predicting the obvious
  econometric instrument fails is part of the claim that returns, not increments, are the
  right representation here.
- **P6 (no reference, no convergence filter).** Including the ships this run's reference
  excluded (all 16, not the 14 judged) changes no verdict in P1–P3: the statistic needs no
  machine-dependent reference.
- **P7 (correlation is not memory).** (a) A temporally correlated but memoryless error
  (AR(1), φ = 0.9, added to echo) keeps slope within ±0.15 of 0 at Δn ≥ 4. (b) A state-only
  error depending on a AND the eccentricity (ε = c·((a−a₀) + 0.5·(e−e₀))) keeps slope
  within ±0.15 of 0 at Δn ≥ 4 while sitting on a higher floor — the instrument tolerates
  state-only errors that live in more dimensions than the matching coordinate.

## Kill criteria

- Bounded's M(Δn) rises with log-log slope ≥ 0.25 ⇒ the a-matching does not isolate
  memory on this scene; instrument dead as built.
- Compound's top-bin M is within 2× of bounded's ⇒ no separation; instrument dead.
- P4 fails ⇒ right instrument, insufficient horizon; the dossier then derives the horizon
  the gate needs instead of claiming teeth it lacks.
