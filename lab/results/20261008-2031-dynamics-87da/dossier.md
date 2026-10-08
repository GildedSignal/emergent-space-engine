# Dossier — 20261008-2031-dynamics-87da (dynamics lens)

**Claim.** In the decoupled-Kepler encounter model, a candidate pair's
per-synodic-period minimum distance is a fixed function of the circle sampled
by an exact rotation (three-gap verified on integers: ≤ 3 distinct inter-hit
gaps for every single-window pair), so the next encounter is Diophantine
— but the conjunction-sampled skin is the wrong observable: it is certified
"never encounter" for ~99 % of orbit-overlapping pairs at Hill-scale
thresholds and misses 36 % of real close pairs already at e = 0.1 (100 % by
e = 0.2), because the true minima live off-conjunction.

**Bottleneck.** Board focus item 3 ("finding encounters without work per
orbit or per element change"; the 5 October top scaling risk: candidate work
must track real encounters). The rotation certificate replaces per-pair
per-orbit polling with one future event per pair; the leak finding kills the
conjunction skin and names the right observable (the synodic-minimum curve).

## Evidence (all from this run; commands below reproduce each)

1. **The return map is an exact rotation.** Conjunction times are exact
   (t_k = (2πk − Δλ₀)/u), and the phase advance per conjunction is exactly
   δ = 2π n₁/u. Independent paths — conjunction-slice formula vs pure time
   propagation at t_k — agree to **4.0×10⁻¹¹** max relative error (512
   conjunctions × 384 pairs). Grid sampling adds ≤ 1.6×10⁻⁶ (p99).
2. **Three-gap theorem holds operationally (integer decision).** For every
   pair with ≥ 8 window hits at m*=3×10⁻³ (7/7 conjunction-slice; and for the
   synodic-minimum observable, see g̃ table), the set of inter-hit gaps has
   **at most 3 distinct integer values** (max observed: 3). So hit times are
   governed by rotation arithmetic, not chance.
3. **Candidate-set shrinkage (the never-certificates).** With the
   conjunction observable, the fraction of orbit-overlapping pairs with any
   window at m* = 3×10⁻³ is **1.4 %** (7/512), at 10⁻³ it is **0.2 %**, at
   ≤3×10⁻⁴ it is **0 %**. g_min percentiles (σ_e=0.1): median 0.136 a. I.e.
   at asteroid-scale thresholds the conjunction skin certifies *every*
   overlapping pair "never" — while real encounters (time sweep) do occur:
   the skin is wrong, not the pairs quiet.
4. **The leak (why the skin is wrong).** Pairs whose dense time sweep gets
   below 3×10⁻³, split by whether anything below threshold occurs within
   0.2 rad of conjunction: leak = **0 % at e=0.05, 36 % at e=0.1, 100 % at
   e ≥ 0.2** (n = 30/28/13/17/7/7/2 deep pairs per e). r8 v2's 0.5–6 %
   belt leak was measured on encounter lists of an integrated reference;
   per-pair, the conjunction skin is far worse than that.
5. **Waiting-time law where windows exist.** At m*=3×10⁻³ (conjunction
   observable): median first-hit 53 conjunctions, 0 censored of 7; at
   10⁻³ the single windowed pair hits at k=5. The m*^{-1/2} slope prediction
   was **not evaluable** (windows too scarce above the g_min floor) —
   reported as not-evaluable, per the pre-registered rule.
6. **Near-rational structure.** Of 4096 pairs, 15 had windows at 10⁻³; the
   single one with min_{q≤64}||qα|| < 10⁻⁴ was censored (>32768
   conjunctions); β ∈ [10⁻³,10⁻²] gave median k*=92. Sample too small for
   the pre-registered monotonicity claim — **not evaluable** at this
   threshold; the staircase data is in `staircase.csv`.
7. **Drift.** With windows ≥ 0.1 wide (m*=0.28), first-hit k* is 3 (p90 21)
   and η ≤ 10⁻³ per conjunction changes nothing while η·k* ≪ w, as
   predicted. The narrow-window regime could not be populated from random
   pairs (see 3), so the horizon law η·k* ≪ w is confirmed only on the
  trivial side; the narrow-window drift regime remains untested.

## The corrected observable (g̃, this run)

The k-th synodic period's minimum distance is **exactly** g̃(θ₀ + kα)
(windows tile time, so the first window with min < m* is the first real
encounter). Same rotation, right observable. Measured (256 pairs each,
G=360 grid, S=96 samples/window; `gtilde.json`):

| ensemble | m* | window frac | median k* | cens | ≤3 gaps (max) |
|---|---|---|---|---|---|
| tight Δ∈[5e-4,5e-3] | 3e-3 | 13.7 % | 123 | 0 | 97 % (5) |
| tight | 1e-3 | 2.7 % | 641 | 0 | 100 % (3) |
| belt Δ∈[0.005,0.05] | 3e-3 | 5.5 % | 67.5 | 0 | 21 % (8) |
| belt | 1e-3 | 2.0 % | 139 | 0 | 0 % (12) |
| belt | 3e-4 | 0.8 % | 4399 | 0 | 100 % (2) |
| belt | 1e-4 | 0.4 % | 2352 | 0 | 100 % (3) |

- g̃ minima are ~100× below conjunction-slice minima (tight ensemble
  median 0.0098 vs 0.136): the deep approaches are off-conjunction, as the
  leak said, and windows now exist at every threshold down to 1e-4.
- Never-certificates at Hill-ish thresholds: **95–98 % of orbit-overlapping
  belt pairs** have no window at m*=10⁻³ (99.6 % at 10⁻⁴): the candidate set
  shrinks ~20–250× below the orbit-overlap set, on fixed elements.
- Three-gap: where the theory applies (**single** window — the ≤3-gaps
  theorem is per interval) it is exact: 100 % of pairs, max 3 distinct
  integer gaps at every narrow threshold. The apparent violations at wide
  thresholds (max 12) are multi-window *unions* (several dips of g̃ below
  threshold), for which the theorem predicts more gap values — consistent,
  not a failure.
- Equidistribution predictor k*≈1/w: 71 % of tight pairs within factor 2 at
  1e-3 (P3's ≥80 % nearly held), only 31 % at 3e-3 — in the wide-window
  regime the three-gap structure (few discrete gaps) dominates the
  mean-field wait, so the predictor is calibration, not certificate.
- Censoring: zero censored pairs among windowed ones at kmax=262144 —
  with the right observable, near-rational α does not produce
  effectively-never pairs in these ensembles (the β<1e-4 censoring case on
  the conjunction slice had n=1; P4 stays unproven).

## Predictions (`predictions.md`)

- Held: P1 (three-gap ≤ 3 wherever the pair has a single window; multi-window
  unions exceed 3 exactly as the per-interval theorem permits).
- Falsified: P5 (leak < 2 % at e ≤ 0.2 — actual 36 % at e=0.1, 100 % by
  e=0.2). This is the run's most load-bearing miss, and it kills the
  conjunction skin as an encounter representation.
- Not evaluable as written: P2, P4 (windows too scarce at conjunction;
  re-measured on g̃ instead, post-hoc — exploratory, flagged).
- Held on the trivial side: P6.
- Process note, disclosed: v1 sampled the wrong configuration slice
  (equal-time instead of conjunction). The shared-harness control did not
  catch it; an independent dense time sweep did (5.9×10⁻⁴ real close
  approach vs 1.69 claimed by the wrong slice). The taste-log lesson
  ("agreement between runs is not independence when they share a harness")
  bit this run too, inside one script.

## What would make it wrong

- The model is decoupled Kepler (r8 v2's own encounter-search model). Real
  secular drift moves α and g̃ between kicks; the certificate must re-derive
  when accumulated drift ~ window width (the horizon law). Not yet measured
  in the narrow-window regime — that is the one experiment this run still
  owes.
- The leak was measured at Δa = 0.02, e₁ = 0.05, coplanar 2D. Other
  geometries change the 36 % number, not the mechanism (deep minima live
  where radial profiles cross at unequal mean longitudes).
- g̃ was validated as a *definition* (windows tile time exactly); its cheap
  evaluation (few samples per window, interpolation) is not built here.

## Cost of adoption, fit with PRINCIPLES

- Per pair: replaces per-conjunction polling with one grid pass over g̃ per
  element change plus one queued event ("no ticks", P14: "you don't advance
  a ship tick by tick you just map where it wants to go"; the pair is
  mapped, not polled). Exactness: "deterministic and reproducible" (P2) —
  the rotation arithmetic is integer-clean (three-gap is an integer check).
- Deletes the conjunction-evaluation tier of the encounters design; the
  pair set itself shrinks by the never-certificates *only if* g̃'s min
  exceeds threshold — for co-orbital/fleet spacings g̃ is small everywhere,
  which is exactly where the 6 Oct phase-neighbour certificate takes over.
- Cost: a g̃ grid (~a few 100 evaluations) per element change per pair. The
  two-tier structure of q-candidate-degree stays; this is its inner tier.

## Reproduce (each ≤ 60 s unless noted)

    python3 enc.py a          # control: slice vs time propagation (4e-11)
    python3 enc.py b          # windows, waiting, three-gap (conj. slice)
    python3 enc.py d          # near-rational buckets, staircase.csv (~90 s)
    python3 enc.py e          # event-level leak (underpowered; superseded)
    python3 enc.py f          # wide-window drift (trivial side)
    # fixups.json: corrected spot-check (agree 1.0), per-pair leak, g̃ drift
    # gtilde.json: synodic-minimum observable, full rotation machinery

Files: `enc.py`, `enc_results.json` (in `st_*/`), `fixups.json`,
`gtilde.json`, `staircase.csv`, `predictions.md`.

## The lens

Dynamics-and-attractors paid off in the return map (a rotation is the
mildest attractor there is) and in the falsification: the interesting
instability was not in the orbits but in the *observable choice* — the
conjunction slice sits at a fixed point of the wrong coordinate. Missed by
this lens: no Lyapunov/KS-entropy measurement (the drift horizon η is the
secular-surprise rate in disguise; a chaos-lens run should own it), and no
3D/inclined check (the game is 2D, so this is in domain).
