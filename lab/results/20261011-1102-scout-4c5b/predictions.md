# Predictions — written before the decisive run (2026-10-11, ~11:20 UTC)

Cases are held out: I have not run the generator on them. My analytic estimates use Peters'
circular closed forms and my hand algebra for the wall (a_wall^{5/2} = (128π/5)·ν·F̃(e)·3/(2ε_bar),
F̃ = (1+73e²/24+37e⁴/96)/(1−e²)^{7/2}) and the separatrix logic (pericenter reaches the unstable
family). The run decides.

## Wiring (must hold, or the harness is broken)

- **P1.** Numerical quadrupole-formula average over a Newtonian ellipse equals the Peters–Mathews
  closed form f(e) to better than 1e-5 relative for e ∈ {0.1, 0.3, 0.5, 0.7, 0.9}.
- **P2.** Circular generator (flux balance on E, geometry-projected L) reproduces Peters' closed
  form a(t) = a₀(1 − t/t_c)^{1/4}, t_c = 5a₀⁴/(256ν), to better than 1e-9 relative.
- **P3.** Circular separatrix (handoff) fires at a = 6M ± 0.01M (the ISCO — this is a property of
  the geometry, not of the flux).

## Held-out behaviour (the run decides; my ranges are honest guesses)

- **P4 (separatrix vs eccentricity, ν = 0.25, a₀ = 100M).** e₀ = 0.6: handoff at a* ∈ [15, 40]M
  with e* ∈ [0.2, 0.55]; e₀ = 0.9: a* ∈ [40, 150]M with e* ∈ [0.5, 0.85]. (Eccentric binaries
  plunge from apastron at much larger a than circular: the pericenter hits the unstable family
  while the orbit is still wide.)
- **P5 (the wall at ε_bar = 1e-3, ν = 0.25, a₀ = 100M).** e₀ = 0: a_wall ≈ 62M (analytic; counts
  as wiring). e₀ = 0.6: a_wall ∈ [100, 200]M (F̃(0.6) ≈ 10.2 pushes it out). e₀ = 0.9: a_wall ∈
  [300, 900]M (F̃(0.9) ≈ 1240). So for eccentric births the 0.1%-bar wall sits far outside the
  separatrix.
- **P6 (wall–separatrix coincidence at the 1% bar).** At ε_bar = 1e-2, ν = 0.25: a_wall/a_sep ≤ 2
  for e₀ ∈ {0, 0.6}; and at ν = 1e-3 the wall meets the separatrix even at ε_bar = 1e-3
  (a_wall(1e-3) ∈ [6, 8]M vs a_sep = 6M) — the EMRI regime, where adiabatic evolution is known to
  survive to the strong field.
- **P7 (total re-keys, the calendar load).** From a₀ = 1000M to the wall at ε_bar = 1e-2,
  ν = 0.25, e₀ = 0.3: total re-keys = ln(P₀/P_wall)/ε_bar ∈ [300, 900] over ~10⁵–10⁶ orbits
  (≪ 1/orbit; the generator is free until the strong field).
- **P8 (1PN flux deficit).** With the standard circular 1PN(+tail) flux correction
  (−(1247/336 + 35ν/12)/a + 4π/a^{3/2}), merger time from a₀: from 100M: 4–8% longer than
  Newtonian-flux; from 20M: 20–35%; the 1% bar breaks at a₀ ≈ 400–700M. Consequence if it holds:
  inside B11's domain the Newtonian-flux generator misses a 1% merger-time bar almost everywhere;
  the 1PN circular coefficient is mandatory, and the eccentric 1PN flux (Junker–Schäfer class) is
  the real adoption cost.
- **P9 (spurious eccentricity).** The exact-family circular projection keeps e ≡ 0; if instead
  both (E, L) drift by Peters' two fluxes on the exact orbit, a spurious e appears at the O(M/a)
  level of the Newtonian↔exact map mismatch: max e ∈ [1e-4, 1e-2] over an inspiral from 100M.
  (Error-type datum: which of the two wirings the law should use for circular.)

## Kill criteria

- If P1 or P2 fails: harness VOID (wiring), fix and rerun.
- If the wall at ε_bar = 1e-2 sits ≥ 5× outside the separatrix for ν ≥ 0.01 (all e), the adiabatic
  generator is NOT self-consistent at any game bar: the "chirp regime" is not a tail but most of
  the observable inspiral, and the generator needs a different strong-field core (osculating
  kicks, Gair–Bond–Hobbs style). That kills "Peters' a(t) as its generator" as stated for
  comparable-mass binaries.
- If the separatrix handoff never fires (roots break by drifting through the discriminant
  irregularly), the plunge-tube changeover has no clean surface: integration continues into
  garbage.
