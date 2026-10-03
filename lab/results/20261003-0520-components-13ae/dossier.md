# Dossier — 20261003-0520-components-13ae (lens: first principles, one component at a time)

## Claim

The kick layer that carries a parent's tide on a stable doll member is
truncation-limited, not method-limited: the classical double average (r9
`kick-avg`'s law) is 14–127% wrong on apsidal precession at e₀ = 3–6% … 30%
everywhere in the Hill regime, and keeping ONE slow harmonic — the evection
term, as a single-averaged quadrupole generator compiled to a slow flow — buys
4–14× accuracy at ~0.2–1.2 events per moon orbit (vs the design's 32 kicks:
27–83× fewer events, each a closed-form drift-level step instead of a tide
evaluation), holding the 10% precession gate out to a ≈ 0.2–0.25 R_H
(τ ≈ 0.005–0.01) where the double average never holds it at e₀ ≥ 0.15.

## Bottleneck

Focus item 1 ("fewer kicks per orbit at the same behaviour: kicks dominate the
engine's cost"; a kick costs 29 µs on the M1 — HANDOFF bottleneck 3). For the
hierarchical bulk of a moon system (every satellite population with a/R_H
≲ 0.25), the tide's event floor is ~0.2–1.2 slow events per moon orbit instead
of 32 kicks. What it deletes there: the per-orbit kick machinery for the
parent's tide (secondaries, neighbours' moments and the resonant regime keep
theirs, r4 v2/v3).

## Evidence

All in `work/`; one command per number: `python3 one.py a/R_H e0 s [T_orb]`
(≤ 40 s/seed); the grid is `python3 grid.py` (43 seeds, ~11 min, 3–45 s each);
`python3 analyze.py` (~3 s) prints every table below and writes
`fig-error.png`, `fig-kickfloor.png`. Setup: planar circular restricted 3-body,
µ_p = 10⁻³ (r9/B14's family), planetocentric, DOP853 rtol 10⁻¹² (1e-13 control:
1.3×10⁻¹⁰), 30 planet orbits (40 held-out), µ_p = 10⁻³, R_H = (µ_p/3)^{1/3}D.
The quadrupole closed forms match numerical double averaging to 5 digits.

Main grid (fixed phases, e₀ = 0.3; relative apsidal-precession error):

| a/R_H | 2Q pro | 1Q pro | 2Q retro | 1Q retro |
|---|---|---|---|---|
| 0.10 | 14.4% | **1.0%** | 16.9% | **1.2%** |
| 0.14 | 22.8% | **2.5%** | 29.3% | **3.5%** |
| 0.18 | 31.5% | **5.0%** | 45.5% | **7.8%** |
| 0.22 | 40.1% | **8.4%** | 66.0% | 15.4% |
| 0.26 | 48.5% | 12.8% | 92.3% | 27.7% |
| 0.30 | 56.0% | 17.7% | 126.7% | 46.7% |

Held-out (random phases, T = 40): e₀ = 0.15: 1.9% (0.12), 7.1/13% (0.20),
16/29% (0.25), 36/114% (0.35); e₀ = 0.6: 1.2% (0.12), 5.3/6.1% (0.20),
5.2/12.5% (0.25), 12/44% (0.35). avg1Q also tracks the e-oscillation
(truth e_max 0.3525 vs 0.3335 at 0.22 R_H). Kick floor (current shape, DKD,
fixed phase step): 10% needs N ≈ 4–8/orbit in the interior, N ≳ 64 at 0.30 R_H;
error ≈ N⁻¹. avg1Q's own truncation budget at 0.30 R_H: octupole+hexadecapole
single-average residual is only 4–5% of the evection term, so its 12–18% error
there is the missing second-order (Lie) term — the named next experiment.

## Predictions

`predictions.md` written before the grid (tuned only at 0.12 R_H). Outcome:
P1 held (2Q is truncation-limited: 14% already at 0.10 R_H, e₀ = 0.3, growing
steeply; r9's τ₀ = 0.0036 tracks its e₀-mix, not a method boundary — with
e₀ = 0.15 the double average fails 10% at τ ≈ 5×10⁻⁴). P2 **missed**: avg1Q
holds ≤ 10% only to a ≈ 0.20–0.25 R_H (2–3% through 0.14, 8.4% at 0.22 pro),
not ≤ 3% through 0.30 as predicted; held as a boundary, reported. P3 partial:
10% at N = 4–8 in the interior (predicted 8–16), but at 0.30 R_H even 64 kicks
sit at 8.8%. P4 held (e₀ = 0.6 degrades gracefully, several × under 2Q; 0.35
retrograde breaks: 114%). P5 held (multipole residual ≤ 7×10⁻⁴, three orders
under the gap — multipoles were never the missing term). P6 overestimated: the
measured event count is 0.39/1.17/2.92 per moon orbit (0.10/0.18/0.30 R_H) at
rtol 10⁻¹⁰, ~5× fewer at behaviour tolerance → 27–83× fewer events than 32
kicks (up to ~400× at 0.10 R_H and behaviour tolerance), not 300–1300× flat.

## What would make it wrong

- avg1Q is quadrupole + evection only: beyond ~0.25 R_H its own truncation
  shows (12–47%), and the missing piece is the second-order averaged term
  (Lie/Deprit), not multipoles (measured 3–5% of the evection amplitude).
  The named experiment: second-order generator, or a changeover to kicks near
  the boundary (which is focus item 2's TRACE/JANUS changeover anyway).
- Circular births: every first-order averaged generator holds e ≡ 0 and misses
  the forced eccentricity, which the truth grows to 2–8% by 0.22–0.30 R_H. If a
  gate needs forced e at e₀ = 0, that observable needs the second-order term or
  sparse kicks; precession there is undefined even in the truth (apse crosses
  zero), as in r9.
- Scope: parent's tide only, planar, µ_p = 10⁻³, non-resonant (n/n_p ≈ 10–55,
  detuned by construction). Secondaries, neighbours' moments, resonance (r4)
  and inclination are outside. Float exploration on 2 vCPU cloud Linux:
  orders of magnitude only; the integrator re-measures on the M1.

## Fit with PRINCIPLES

- #3 "Compute only surprises": the fast average is a symmetry of the
  representation (#32); only the slow evection libration is computed.
- #19 "A fix signals the wrong representation": r9's τ₀ read a truncation
  boundary as a method boundary; the single average is the water for this fish.
- #26 "Steal what works… compute-deprived… skin in the game": the evection term
  is classical lunar theory (Delaunay, Hill) — pre-compute-era machinery.
- #14 "No work for no reason": events per orbit ~ m = n_p/n_moon → 0 for tight
  hierarchies, instead of a flat 32.

## The lens

Idiot index measured (design over floor): 32 kicks vs 0.08–1.2 slow events per
moon orbit across 0.10–0.30 R_H → 27–400×, plus each event is a closed-form
derivative pair rather than a tide evaluation + Kepler round-trip (29 µs/kick
measured on M1). What this lens may have missed: cost moved into generator
compilation and memoization (per-(a,e), fits the cycle-memo pattern); the
neighbour components (secondaries' kicks) were not re-measured; inclined orbits
(Kozai–Lidov) should ride the same slow flow at zero extra event cost —
asserted, not measured.
