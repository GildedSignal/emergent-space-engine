# predictions.md — 20261003-1842-library-76d6

Written before the decisive run. Tuning happens only on the base case (e=0.1).
Held-out cases: e=0.6 (the r9/taste-log control) and J2=10x stronger (e=0.1).

Experiment: Wisdom–Holman style motion — exact Kepler drift + J2 impulse kicks,
uniform step, equatorial orbit. GM=1, a=1, R=0.05. Behaviour oracle: analytic
apsidal precession  Δϖ/orbit = 6·π·J2·(R/p)², p=a(1−e²). Pass band: relative
precession error ≤ 1% AND |Δe| ≤ 1e-4 over 200 orbits. Decision variable: kicks
per orbit (integer). Methods: lf2 (symmetric kick–drift), y4 (Forest–Ruth), y6
(Yoshida order 6) — all built from the SAME two operators, kicks counted per orbit.

Pre-registered:

- P1 (base, e=0.1, J2=1e-3): lf2 needs ≥ 32 kicks/orbit for the band; y4 passes at
  ≥ 4× fewer kicks than lf2; y6 at least as good as y4.
- P2 (held-out, e=0.6): all methods need more kicks (pericenter), the y4/y6 gain
  over lf2 shrinks but y4 stays ≥ 2×; y6 falls below y4 (its 7 kicks/step pay for
  order the coarse grid cannot use at pericenter).
- P3 (held-out, J2=1e-2, e=0.1): relative precession error is ε-independent to
  first order, so the pass-band kick counts are within 2× of P1 for every method.
- P4 (control): lf2 at 4 kicks/orbit fails the band (else the band is too loose and
  the run is void).
- P5 (error type): all three hold energy error bounded (no walk) over 200 orbits at
  their pass-band k, including y4's negative middle step (exact drift makes
  negative substeps free and reversible).
