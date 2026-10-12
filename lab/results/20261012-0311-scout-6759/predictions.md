# Predictions (written before the decisive run)

Cases I have NOT tuned on. Kill criteria pre-registered.

- **P1 — instrument control.** With the perturber off, the same code path must
  produce exactly zero distinctions (all quantized deltas identically 0 across
  all epochs). If not, the instrument leaks (integrator/round-trip noise) and
  every other number is VOID until the leak is below the quanta.
- **P2 — shuffle control.** Permuting deltas among bodies (destroying the
  a-correlation) must drop the absorbed fraction to ~0 (trend removes almost
  nothing on shuffled data). If the trend still "absorbs" > 10%, the
  absorbed-fraction estimator is broken.
- **P3 — cold belt shared fraction.** Off-resonance, at least 90% of per-kick
  delta entropy is absorbed by a smooth degree-9 polynomial in a (secular
  theory: precession rates are smooth in a; Lyapunov time 1e3–1e4 yr ≫ window).
- **P4 — resonant contrast.** The 3:1 belt (a ≈ 2.50 AU) has per-body residual
  entropy at least 5× the cold belt's, because resonant kicks depend on the
  resonant phase, which decorrelates from a.
- **P5 — growth law.** Cold-belt residual *stock* (cumulative scar after trend
  removal) grows sub-linearly in 8 orbits (closer to logarithmic/diffusive);
  the resonant belt grows measurably faster per orbit (toward linear mixing).
- **P6 — budget.** Cold belt: extrapolated breach of 34.4 bits/body lies beyond
  1e5 orbits (i.e. not a session problem; reabsorption never urgent off
  resonance). Resonant belt: breach within 1e3–1e4 orbits (consistent with
  Lyapunov times ~1e3 yr), so resonance-skinned populations need reabsorption
  or their own program family. Both extrapolations flagged as such.

If P3 fails (shared fraction < 90% off resonance), the population-program
representation is in trouble at belt scale and the dossier says so — that is
the interesting kill.

## Addendum (pre-registered before the tensor-basis repair run)

First pass result (already measured, not tuned on): the per-kick delta field is
NOT smooth in a (or a+e) alone — absorbed fraction ~0%, raw entropy saturated
at the N-ceiling (~4 x log2 N per kick: every body's delta is distinct, the
zero-order entropy measures phase spread, not information). Diagnosis: the
shared structure is the deformation over the FULL initial state (a, e, omega,
M), which is what a recompiled program is; the a-only basis was the wrong
instrument, not the physics (H0183).

- **P3b — tensor basis.** With Chebyshev tensor products over scaled
  (a, e, omega, M) at degree 3 each (256 columns), the off-resonance cold belt
  absorbs >= 90% of the per-kick delta field; the resonant belt absorbs
  markedly less.
- **P2b — shuffle control.** Permuting deltas among bodies and refitting the
  same tensor basis must absorb ~0 (estimator validity).
- **P5b — stock law.** The tensor-residual *stock* (true per-body scar floor)
  grows at most logarithmically in orbits off resonance, and the per-body scar
  word cost (log2 of scar magnitude) stays under ~24 bits per element within
  8 orbits.
