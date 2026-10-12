# Predictions — run 20261012-1227-system-8685 (system lens)

Written before the decisive runs (two numbering corrections made before any run:
the sparse control is `u8`, not `u512` — the control must be sparser than the plane's
64, not finer; and `+avg` is implemented as `+seg8`, one midpoint kick per 8-step
segment outside windows, the practical stand-in for the engine's orbit-averaged kick).

Model: 2D test particle + one planet on a fixed circular orbit around a static star
(float replica of the WH split, not the engine). All variants share the same model,
the same seeds, and differ only in **when kicks happen**. Truth = the same DKD split
at a fine uniform step, convergence-checked one level finer.

Variants:
- `u64`: uniform kick every P_body/64 (the plane's rule; positive control — must pass);
- `u8`/`u16`/`u32`: uniform every P_body/N, N < 64 (count-matched, phase-blind controls);
- `w<W>`: kicks only inside synodic windows |wrapPi(λ_body − λ_planet)| < W, at the
  same local step P/64; no kicks outside windows (pure Kepler drift);
- `w<W>+seg8`: as `w<W>`, plus one midpoint kick per 8-step segment outside windows.

Configurations (planet μ_p = 1e-3 on a circular orbit):
- **ENCOUNTER**: body a=1.25, e=0.20 (pericentre crosses the planet's orbit; conjunction
  every ≈3.5 planet orbits). T = 1000 P_planet.
- **RESONANT 2:1**: body a=1.587, e=0.05. T = 1000 P_planet.
- **BELT-SMOOTH**: body a=1.0, e=0.05, planet at a=5.2 (the force varies only ±2×: the
  smooth secular regime — the lens's named hard case). T = 1000 P_planet.

16 seeds each; behaviours judged as ensemble distributions (median ϖ̇ and ė over
non-ejected seeds, ejection count) plus per-seed Jacobi-constant drift (chaos-robust).

## Held-out predictions

- **P1 (ENCOUNTER):** `w0.5` uses ≥8× fewer kick evals than `u64` while matching truth's
  ensemble ϖ̇, ė and ejection count at least as well as `u64` does (deviation ≤1.5×
  `u64`'s own). The count-matched `u8` (phase-blind, similar kick budget) misses
  ϖ̇ or ė by ≥2× `w0.5`'s deviation — the clock matters, not the count.
- **P2 (RESONANT 2:1):** `w0.5` holds the resonant e-pump within ~20% of truth's
  (per-conjunction phase is the r4 rule, native here). `u8` does not (it under-resolves
  conjunction phase) or pumps with a wrong libration spectrum.
- **P3 (BELT-SMOOTH, the hard case):** `w0.5` alone degrades ϖ̇ by ≥3× vs `u64`'s error
  (the secular precession lives between conjunctions); `w0.5+seg8` recovers to ≤1.5×.
  If `w0.5` alone holds instead, that is a held-out miss in the *favourable* direction
  and I will suspect the truth and re-check convergence before claiming it.
- **P4 (symplecticity of an event-scheduled cadence):** `w0.5`'s Jacobi drift stays
  within a small multiple (≤5×) of `u64`'s over T; it does not walk like a random walk
  (growth exponent ≤ ~0.5, vs `u64`'s own). If it walks, Calvo–Sanz-Serna kills
  adoption of variable event-scheduled steps and the dossier says so.
- **Kill criterion for the whole claim:** if count-matched uniform (`u8`) matches
  `w0.5` on P1 and P2, then the win is sparsity, not the interaction clock, and the
  unification of kick cadence with the encounter predictor is dead as a *cost* claim
  (it may still hold as structure).

## Fermi (before running)

ENCOUNTER: conjunction every 3.5 P_p; W=0.5 rad window ≈ 0.28 P_p; local step P_b/64
≈ 0.022 P_p → ≈13 kicks per window, ≈3.7 kicks per planet orbit ≈ 5.2 per body orbit,
vs 64: **~12× fewer**. The window setup the plane pays per kick (92% of per-kick
evals, gold 20261006-0737-components-4643) becomes the kick's own schedule: paid once
per window, not once per kick.

## Blind spot (named in advance)

Multiple sources: a body under S planets pays Σ_s windows; the win shrinks as S grows
(4 planets × ~13 ≈ 52 vs 64 — marginal). The strong cases are one-dominant-perturber
regimes (the belt under its shepherding planet, the fleet, flybys), which is where the
engine's scale story lives. The lens's own warning: elegant unification hiding a hard
special case = the smooth secular regime (P3) and the many-source regime; both are in
the grid, both could kill.
