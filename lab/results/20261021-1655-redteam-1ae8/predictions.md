# Predictions (written before the decisive run)

Target: representation.md L67 — "Perturbations (tides, neighbours, inspiral by Peters' formula) are
kicks on E and L", applied once per radial cycle (the cycle is the certificate; the kick is the
letter's mechanism). Truth: the same Peters rates (da/dt, de/dt, Peters 1964, with the enhancement
factors) integrated continuously (RK4, dt = P/512). This isolates the kick-vs-generator question
from the multiply-add channel already killed by df81/6164/ee08.

Cases NOT tuned on: the whole (p, e) start plane is held out; I tuned nothing. Predictions:

- P1 (circular control): at e0 = 0 the integrator must reproduce the closed-form merger time
  t = (5/256)·a0⁴/(μM³) to better than 1e-9 relative (positive control; if not, instrument broken).
- P2 (quasi-circular far field): at p0 = 10⁴M, e0 = 0, per-cycle kicks match truth to < 0.1% in
  merger time (the letter survives far out; this is the "both sides" control).
- P3 (circular strong field): at p0 = 15M, e0 = 0 the letter's per-cycle ZOH LAGS the truth
  (uses the stale, weaker rate while a shrinks): merger-time error > 1%, sign = late.
- P4 (high eccentricity at the doll's licensed edge): at p0 = 65M, e0 = 0.9 the enhancement
  factor makes Δa/a per cycle ≳ 1%; the letter now merges EARLY (the stale-orbit error is
  dominated by F(e) collapsing as e circularizes: the held rate is too strong). Error > 5%.
- P5 (adiabaticity law): the per-cycle quantum Δa/a = (128π/5)·ν·(M/p)^{5/2}·F(e) (p = semi-latus);
  the letter's error tracks this: error becomes "by type" (no uniform step exists) once
  Δa/a per cycle ≳ 0.01 — i.e. inside roughly p ≲ 65M·(ν/0.25)^{0.4}·F(e)^{0.4}, and no
  rung in lab/rungs/ gates any inspiral arm (r1/r3 are conservative-only).
- P6 (cycle count): cycles to merger from p0 = 20M, e0 = 0 is O(10³), so a > 1% merger-time
  error there is ~10 wrong orbits at the spectacle the player watches (the last plunge).
- P7 (frequency channel): the letter's cycles-to-merger differs from truth by more than the
  merger-time relative error alone would suggest when e0 is high (circularization rate held
  stale compounds in the period, which enters both the clock and the GW phase).

What would make the letter survive: if P3/P4 errors land under ~0.5% everywhere p ≥ 65M at all e,
the kick mechanism is licensed in the doll's own domain and the attack collapses to a domain note.
