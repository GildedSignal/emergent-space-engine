# Dossier — run 20261004-1525-scout-2098 (scout lens)

## Claim
Plain fixed-phase DKD (exact compiled drift + one tide kick per step) already
holds B14's apsidal-precession behaviour at **4–6 kicks per moon orbit** through
at least 0.4 Hill radii — a 6–8× cut from the current 32 — while WH-style
symplectic correctors and 4th-order compositions do **not** extend that
frontier; the frontier is set by aliasing with the parent's synodic phase, so
the correctors direction (queued `q-correctors`) is the wrong lever.

## Bottleneck
Board focus 1 ("fewer kicks per orbit at the same behaviour; kicks dominate the
engine's cost"). Expected gain ~6–8× fewer tide kicks for every satellite
regime away from resonance; deletes nothing structural but redirects the
planned corrector work. What it lets us delete: 5/6 of all kick events at
current behaviour.

## Evidence
Planar circular restricted three-body (test-particle moon, μ = m_sun/m_planet
= 10⁶, e₀ = 0.10, exact analytic Kepler drift = the tube stand-in, tide kick
at a fixed step in the drift's phase). Reference = plain DKD at 512
kicks/orbit (agrees with 1024 to 1e-4). Horizon 20 planet orbits (137–388
moon orbits); criterion B14's 10% on the fitted precession rate. Correctors
are a faithful port of WHFast's published Z operators and coefficients
(rebound `src/integrator_whfast.c`), applied at start/end/outputs with the sun
frozen in time inside Z, as the time-independent theory requires.

| f = a/R_H | plain: worst relerr at frontier | avg (r9 control) |
|---|---|---|
| 0.2 | 0.8% @ nk=4 (breaks at 3: 306%) | 7.5% (passes) |
| 0.3 | 1.0% @ nk=4 (breaks at 3: 175%; nk≤2 escapes) | 20.7% (fails) |
| 0.4 | 0.75% @ nk=6 (breaks at 4: 30%; nk≤3 escapes) | 38.9% (fails) |

- Correctors: at fine steps they win (nk=32, f=0.3: 8.1e-5 vs plain 3.0e-4,
  3.7×), but the ≤10% frontier does not move: at f=0.3 corr3 breaks at nk=4
  (123%) where plain holds (0.97%); at f=0.4 corr3/corr5 escape at nk≤4–6
  where plain holds 0.75%. At equal force-evals/orbit plain always wins.
- Forest–Ruth 4th order (4 evals/step): never better than plain at equal
  evals/orbit anywhere (P3 held).
- Robustness: frontier unchanged at the full B14 horizon of 50 planet orbits
  (nk=4: 0.74%) and with a second sun-phase seed (nk=4: 5.5%).
- Reproduce: `python3 lab/results/20261004-1525-scout-2098/falsifier.py`
  (53 s on this container, 2 vCPU; data in `results.json`, log in
  `decisive.log`).

## Predictions
`predictions.md` was written before the decisive sweep (calibration had seen
only f=0.3, nk ≥ 8). Held: P2 (correctors do not extend the frontier; they
beat plain only at nk ≥ 16), P3 (compositions never pay at equal cost), P4
(averaging passes at 0.2 R_H, fails beyond — r9's kill and threshold
reproduced independently). Partially held: P1 (frontier at nk=4–6, predicted
2–3 at f≤0.3 — off by one kick-step, the direction was right), P5 (the cliff
is a mix of rate blow-up and e-pumping/escape, not cleanly one or the other).
P6 (slope ≈ −2 for plain) held within noise.

## What would make it wrong
- The tide here is a single moving perturber with a fixed circular orbit;
  many-source multipoles, eccentric parents, or inclined orbits could alias
  differently and move the 4–6 frontier.
- Single e₀ = 0.1, two seeds, test particle; B14's retrograde and e₀ ≤ 0.3
  births untested.
- The corrector kill is for time-dependent B (moving source). For a static
  neighbour's moments (B time-independent), the standard corrector theory
  applies again and may still pay; that case is unmeasured. UNVERIFIED
  whether anyone has derived correctors for explicitly time-dependent B.
- Mechanism note (checked numerically, not from the literature): the planar
  double average of the tide is exactly constant (2D circular average of the
  Coulomb potential carries only the n=0 multipole for r < a_s), so any
  planar averaged tide is necessarily a single average that keeps the evection
  angle — which is why r9's method fails precession beyond ~0.2 R_H.

## Cost of adoption
Near zero: the kick cadence per doll changes from 32/orbit to a
dimensionless-number-selected 4–6/orbit away from resonance; fixed-phase
steps and integer kicks are already the law's structure (r2: increments are
exact at any width). Risk: the cliff below the frontier is violent
(escapes, >100% precession errors), so the cadence rule must be conservative
or certificate-driven, not tuned to the edge.

## PRINCIPLES fit
- 22, "the simulation tells us what next not us": the binding constraint is
  the parent's synodic phase, not the moon's own phase — the kick schedule
  should follow the sources' phases, which is a representation change in the
  scheduler, not a higher-order kick.
- 2/20: judged on behaviour (precession, class, e) across seeds and horizons,
  never trajectory identity.
- 26, steal from skin in the game: the WH corrector is the field's best — and
  it does not transplant to a moving perturber; the cheap win was already in
  the plain map.

## The lens
The scout lens trusts published mechanisms; the transplant failed exactly
where the literature's assumptions end (time-independent B). It also framed
the question as "which integrator" when the data says the question is "which
sampling schedule". The named gold experiment: lock the kick grid to the
synodic phase (or continued-fraction conjunction timing, the same machinery
as r8 v3's skin) and measure whether the frontier drops below 1 kick per
moon orbit at 0.2–0.4 R_H.

Self-grade: **silver** — reproduced, predictions largely held, moves a live
bottleneck ~6–8× and redirects a queued run; gold needs the synodic-matched
schedule experiment.
