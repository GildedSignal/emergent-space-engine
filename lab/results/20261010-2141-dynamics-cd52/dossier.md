# Dossier: run 20261010-2141-dynamics-cd52 (lens: dynamics and attractors)

**Claim (one sentence):** On the law's own cheap path (exact Kepler drift + fixed shared
kick step) a cold belt has **no clean operating point**: conjunctions with impact parameter
below the step's resolution radius b ≲ √(m·dt) — a 1-D tail of count ~N²·√(μ·dt)/ē — corrupt
it from the first orbit at every cadence tested (8–128/orbit) and every horizon (5–200
orbits), manufacturing λ ≈ 2–14/orbit of fake chaos on top of a derivable, algebraic
Kepler-shear floor of 2.303e-2/orbit; the belt's surprise rate (H_live's floor) is therefore
measurable only behind the changeover/encounter tier, which at 2²⁰ bodies carries the
encounter population itself, not a tail.

## Bottleneck

H_live ("distinctions created per game-second … decides whether a billion bodies fit",
docs/plane.md) has a physical floor nobody has measured: the rate at which belt trajectories
stop being derivable from stored programs. From the dynamics lens this is the belt's surprise
rate — its largest Lyapunov exponent and its growth law — against kick cadence and N at fixed
belt mass. It sets (a) how often the belt program must be scarred, (b) whether the kick layer
at the plane's cadence manufactures distinctions the true universe never creates, (c) whether
per-body surprise grows or shrinks as the belt is refined.

## Instrument (the design's cheap path, in miniature)

`belt_lyap.c`: Wisdom–Holman belt — exact per-body Kepler drift about the star (the compiled
generator), one kick per step carrying everything else (mutual Newtonian pulls + the indirect
term: the doll's origin falls; docs/law.md "Motion in a doll" and events), DKD split, fixed
step shared by all bodies. Benettin shadow set at total norm d0 = 1e-8, renormalised at 1e-6;
exponential growth (λ_exp/orbit at a = 1) is separated from algebraic Kepler-shear growth by
tail fits of L vs t against L vs ln t. Belt: N equal masses, uniform a ∈ [0.95,1.05], Rayleigh
σ_e = 0.05, uniform angles, 2-D, G = M★ = 1. Floats explore; this is an instrument for rates,
not canonical outcomes.

Reproduce (each ≤ 60 s at N ≤ 400):
```
gcc -O3 -fopenmp -o belt_lyap belt_lyap.c -lm
./belt_lyap 200 0 0.05 64 200 1 curves/x.dat      # negative control
./belt_lyap 200 0.0001 0.05 64 200 1 curves/y.dat # belt cell
./matrix2.sh                                       # full matrix -> matrix2_raw.log
python3 fit.py                                     # fits (points at matrix2_raw.log)
```

## Disclosure: an instrument bug, found and fixed mid-run

The first matrix (`matrix_raw.log`, kept unchanged as the record) ran with a kick that added
acceleration to velocity without ×dt: kicks were 1/dt too strong (spon = 64: 10×; spon = 256:
41×). Its signature — corruption growing with steps-per-orbit, λ_raw up to 23/orbit, fallback
counts ~10⁷ — was diagnosed by first-ejection forensics (a body reaching e = 1.44 at orbit
0.22) and the kick was fixed to `Δv = a·dt`; `matrix2_raw.log` is the corrected decisive
matrix. Predictions were written before the first (buggy) matrix and are judged against the
corrected one. Note the correction did NOT cure μ = 1e-4 corruption — that regime is real
conjunction arithmetic, reported below.

## Results (corrected matrix, matrix2_raw.log)

**Controls.**
- Negative (μ = 0, N = 200, 64/orbit, 200 orbits): λ_raw = 2.3031e-2/orbit, L = 4.606 =
  exactly one renormalisation (d grew ×100 = the shear of the offset over 200 orbits); growth
  algebraic (fits ln t, not t); fallback 0; seed-stable (0.023031/0.023038/0.023034 across
  seeds; μ = 0 cells were immune to the kick bug, so matrix1's controls stand). Everything a
  belt measures above this is real surprise; the floor itself is free (derivable: the
  program knows the orbits — PRINCIPLES 3).
- Positive (N = 50, μ = 1e-2, 64/orbit, 20 orbits, both seeds): **corrupted** — fallback
  45–64k, dH 6–9, λ_raw 9.6–10.2/orbit. With the kick fixed this is physics, not bug: at
  μ = 1e-2 (m = 2e-4) close-encounter timescales drop below any fixed 64/orbit step within
  tens of orbits. P2's "clean in 20 orbits" prediction is FALSE: the strong-scattering regime
  needs the SyMBA changeover (law.md) engaged essentially immediately. A fixed-cadence belt
  instrument without substeps is only valid for cold belts (μ ≲ 1e-4 here).

**Belt cells (the decisive outcome).** Every μ = 1e-4 cell corrupts at every cadence tested
(8, 32, 64, 128/orbit) and every horizon down to 5 orbits: fallback ≥ 2,026 by orbit 5 at
64/orbit (λ_raw 7.05), 9,120 by orbit 10, 35,742 by orbit 25; at 200 orbits fb 7.6e4–2.0e6
across N ∈ {50,100,200} and cadences, dH 0.74–137, λ_raw 1.3–14.4/orbit, seed-dependent.
**No clean operating point exists for a fixed shared kick step on a cold belt.** Mechanism
(first-ejection forensics): conjunctions whose impact parameter falls below the step's
resolution radius d_kill ≈ √(m·dt). Co-planar conjunction b ≈ |Δa| plus epicyclic offsets is a
1-D tail (not 2-D overlap), so the expected count is N²·d_kill/W per horizon — order 10²
killing pairs at this cell per 200 orbits, the first within ~1 orbit; scaling
∝ N²·√(μ·dt)/ē. Real belt λ at μ = 1e-4 is μ-scale per orbit, not 5/orbit: the measured
λ_raw is integrator-manufactured captures **masquerading as chaos**. At 2²⁰ bodies the count
is not a tail but the encounter population itself: the changeover/encounter tier (SyMBA
changeover, Binet cone + exact per-pair handling) is the only representation that can hold a
belt at scale — a representation claim, not a tuning one (PRINCIPLES 19). Energy flags the
corruption (dH ≥ 0.74 ≫ B12's 1e-4) but only after the belt is destroyed; a λ-style surprise
instrument (the H_live measure) must sit behind the changeover or it measures garbage.

## Predictions (predictions.md) — outcome

- P1 negative control: HELD (algebraic growth, λ_raw ≈ 0.0230, fallback 0, seed-stable).
- P2 positive control cleanliness: FAILED — real physics: strong scattering (μ = 1e-2) breaks
  any fixed 64/orbit step within 20 orbits; the changeover must engage immediately there.
- P3 cadence convergence: VOID — no cadence (8–128/orbit) converges; corruption at all of
  them; the cadence ranking is non-monotone and seed-dominated. The predicted energy
  blindness also failed: corrupted cells show dH ≥ 0.74.
- P4 N-scaling exponent: VOID — λ_exp values are corruption-dominated; no clean λ to fit.
- P5 μ = 1e-5 growth law: PARTIALLY HELD, and sharpened the claim. The cell (N = 200,
  64/orbit, 50 orbits, seed 1) is clean by the fallback counter (fb = 0, dH = 1.9e-3) yet its
  growth is exponential: λ_exp = 2.99/orbit (R² = 0.9915 for L ∝ t, vs 0.972 for L ∝ ln t),
  diverging from the first renorm at t = 0.7 orbits. Belt chaos at μ = 1e-5 cannot be
  λ ~ 3/orbit (real conjunction scattering is μ-scale per orbit): this is manufactured
  chaos riding unresolved but still-bound co-orbital pairs — **fallback = 0 is not a
  sufficient cleanliness certificate**. A λ-style surprise instrument needs the conjunction
  criterion (b ≳ √(m·dt), a dimensionless number) as its admission gate, not an ejection
  counter. Reproduce: `./belt_lyap 200 1e-05 0.05 64 50 1 curves/wm5.dat`.

## What would make it wrong

The λ numbers are for a float WH toy of the law's structure, not the integer plane: the
absolute rates are order-of-magnitude; the seed-stability, the algebraic-vs-exponential
classification and the corruption boundaries are the load-bearing findings. A real check must
run the same Benettin shadow on the plane's own belt path (`xtask universe`), where the kick
layer is integer and the changeover exists; the corruption regimes found here should then
shrink to exactly the cases the changeover catches. Single-lens risk: I did not measure the
full exponent spectrum (KS entropy), only λ_max.

## Cost of adopting

A Benettin shadow pair on the belt (2× the kick cost, zero extra drift) added to
`xtask universe --bench` as the surprise-rate instrument the H_live lens (b-h-live.md) needs;
plus the two corruption boundaries as rung criteria for any belt gate.

## Fit with PRINCIPLES

"Compute only surprises" (3): the shear floor is derivable and costs nothing — measured as
algebraic, so the belt program stays valid far longer than an exponential-chaos guess implies.
"The simulation tells us what's next not us" (22): cadence and changeover thresholds come out
of the dynamics, not a chosen step. "A test that cannot fail is a control" (heuristics): the
μ = 0 control is exactly that, and it is what makes the belt numbers readable.

## The lens

Dynamics/attractors: what it may have missed — the 60-minute box cut the corrected matrix to
2 seeds/cell and no spectrum; long-run transients (the lens's own blind spot) are not probed:
200 orbits is short against secular timescales (M/μ ~ 10⁴ orbits). The corrupted-first-matrix
episode is itself a lens artifact worth naming: agreement between cadences was agreement in a
shared bug — the memo-artifact lesson (board, 5 October) reproduced inside one run.
