# Dossier — 20261001-2353-q-changeover-e04a (the changeover near a secondary)

## Claim

On close passes of a Jupiter-like secondary (0.1–3 Hill radii), no float changeover at the
plane's step budget (64 kicks/orbit) reaches B12's Jacobi growth exponent of 0.2 in this
replica: the smooth SyMBA mechanism sits at 0.41 (median judged seed), and MERCURIUS's
Heaviside handoff to an accurate interior matches it (0.47) at ~600x fewer switch events
(1.7 vs 1024 per pass) but pays ~1400 inner force evaluations per pass; TRACE is killed
twice over (its roundtrip check is vacuous on a self-adjoint split, and its informative
Jacobi check cannot separate baseline from encounter at this budget: 2M retries and still
max error 0.02–13); and the answer to the lens's reversibility question is measured: a
switch may depend on the state only through positions, evaluated at the step's symmetric
mid-state — then it is exactly bit-reversible in integers even as a branch selector — but
a velocity-dependent branch breaks bit-reversibility at the first crossing, and a
position-only branch selector is bit-reversible while still drifting in its invariant
(30x worse than the smooth law): reversibility and bounded error are different properties,
and only a changeover baked into the splitting (smooth in position, no branch) buys both.

## Bottleneck

Board focus item 2: "the changeover near a secondary, reversible and integer (TRACE,
JANUS)". The measured trade is switch events against exponent and max error. What it lets
us delete: if a Heaviside handoff to the doll's compiled interior is as good as the smooth
cascade at 1.7 events/pass, the engine's changeover can be one handoff event on the doll
queue instead of a recursive kick cascade; and TRACE-retry is deletable at this budget.

## Evidence

Model: the plane's (star fixed at its doll's origin, planet mu=1e-3 prescribed circle,
test particle, no indirect term; exact invariant C = v²/2 − (1−mu)/r − mu/|x−xp| − Omega·Lz).
Judge: B12's rule ported exactly (xtask/src/behave/handoff.rs, fit.rs): err at P/8 over
200 periods, windowed log-log exponent, floor 1e-12, median over judged seeds, err_max 1e-4.
32 seeds: 16 B12-recipe circular (k = da/R_H in U[1.5,3]) and 16 eccentric crossings
(a = 1±2R_H, e in U[0.03,0.15]), median periapses 0.17–2.35 R_H, 7–33 passes each.
Truth (positive control): DOP853 rtol 1e-13 in planet-relative coordinates, |dC/C| ≤
2e-11 over all 32 seeds — the invariant and judge are sound.

| scheme | med exponent (judged) | ensemble | worst max err | events/pass | kicks/orbit | inner fevals/pass | ok/32 |
|---|---|---|---|---|---|---|---|
| symba (smooth, 4 levels) | 0.41 | 0.59 | 1.2 (chaotic seed) | 1024 | 180 | 0 | 18 |
| mercurius (Heaviside+DOP853) | 0.47 | 0.40 | **2.3e-5** | **1.7** | 62 | 1375 | 29 |
| soi-switch (events3) | 0.42 | 0.94 | 1.4e-3 | 1.0 | 64 | 0 | 30 |
| trace (vacuous roundtrip check) | 0.74 | 0.73 | 0.95 | 0.1 | 64 | 0 | 16 |
| trace (Jacobi check, eps 1e-6) | — | — | 0.02–13 (3 seeds) | 2e6 | 2e4 | 0 | 0 |
| wh-fixed (negative) | 0.46 | 0.53 | 3.7e-1 | 0 | 64 | 0 | 15 |
| wh-dense P/512 (negative) | 6.1* | 9.4 | 1.8 | 0 | 512 | 0 | 11 |

*wh-dense's fitted exponent is the slope of an error walking from float noise to 1e-1;
its point is that 512 kicks/orbit without a changeover still fails (worst 1.8).

Controls both ways: truth passes (2e-11, flat); wh-fixed fails on max error (0.37), and
soi-switch reproduces events3's kill shape (ensemble 0.94, max 1.4e-3).

Reproduce (each <= 60 s except the full run, ~6 min on 2 vCPU):
- `python3 changeover.py` (all schemes, 32 seeds, writes run_*.json, truth.json)
- `python3 analysis.py symba mercurius trace wh-fixed wh-dense soi-switch` -> metrics.json
- `python3 janus.py` (integer reversibility, ~6 s) -> janus.json
Everything lives in this folder; scripts are standalone Python (numpy/scipy only for truth).

## Predictions (predictions.md, written before the decisive run)

Held: mercurius exponent in [0.2,0.7] (0.47) with 2 handoffs/pass (1.7) and hundreds of
inner evals (1375); wh-fixed fails (max 0.37); soi-switch 0.6–1.0 ensemble (0.94, median
0.42); truth flat (2e-11); trace roundtrip floor far below eps (2e-14 measured).
Missed, and why: (1) I predicted symba <= 0.1 and trace <= 0.2 — neither holds in this
replica; symba lands 0.41. My replica stacks all level kicks at the step's midpoint
(no drifts interleaved between layer kicks), and steps in time, not in the drift's phase,
so it is a lower bound on the shipped plane's quality (the plane's own Jacobi number is
4.5e-5 bounded over 100 periods on its seeds) — the mechanism comparison is still
apples-to-apples because every scheme here shares the same core. (2) The trace roundtrip
check turned out vacuous (a self-adjoint DKD roundtrip is the identity in exact
arithmetic; only roundoff 2e-14 shows), which my prediction did not anticipate; the fix
(Jacobi per-step check) then degenerated as described. Both misses are reported as held
and measured, not tuned away.

## What would make it wrong

The seeds are harder than B12's (eccentric crossings, median periapses down to 0.17 R_H),
and my symba replica is one implementation of the mechanism (midpoint-stacked layers,
time steps, LEVELS=4 to reach below the plane's capture radius at SOI/4). If the shipped
plane's sub-cycled, phase-stepped cascade reaches 0.2 on these same seeds, the incumbent
stands and this run only kills TRACE and ranks the handoff. The mercurius result depends
on an interior integrator at rtol 1e-12 (~1400 fevals/pass): an interior at the plane's
integer budget would degrade its max error toward soi-switch's 1.4e-3. The JANUS demo
uses an integer leapfrog core (free-flight drifts), not WH: the reversibility argument is
independent of the drift's form, but the error floors are not the plane's.

## Fit with PRINCIPLES

- "errors never compound" (13): the exponent table is exactly the error-type measurement
  the law's gates demand; none of the float changeovers reaches bounded (0) here.
- "less is more" (1) / events are the only work: mercurius's 1.7 switch events per pass
  against symba's 1024 is a 600x cut in machinery events on the doll queue, if its
  interior cost can be paid inside the doll (compiled two-body + tide, not DOP853).
- "compute only surprises" (3): retries that fire everywhere are the anti-pattern; trace's
  degeneration is the measured proof.
- "a switch may depend on the state": the law.md line "a state-selected switch at the
  sphere of influence is not [symplectic]" is refined, not contradicted: state-selection
  through positions at the symmetric mid-state keeps exact reversibility (measured,
  bit-level) but still loses the shadow bound; smooth-in-position keeps both. Velocity-
  or time-dependent selection must be banned outright.

## The lens

The changeover lens asked for ship AND moon passes; the moon (massive, full three-body)
case was not run — the run spent its window on getting the ship case's judge exact and on
the two trace kills. The next run should take the massive three-body energy-error case
and the shipped-plane cascade on these same 32 seeds (both scripts here extend directly).

## What this lens may have missed

I compared changeover mechanisms at fixed step budget and judge quality, not the plane's
phase-stepped implementation, so the absolute exponents are pessimistic for the incumbent;
and all schemes share my DKD core, so a core defect (e.g. in the time-dependent midpoint
kick) would move all of them together — the truth control bounds this at 2e-11.
