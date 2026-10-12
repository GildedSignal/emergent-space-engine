# Dossier — run 20261007-1646-second-20261007-1550-dynamics-71a5-f282 (lens: second author)

**Claim (one sentence).** The second checker's named experiment, run, splits the original
claim in two: the aging law itself now holds fitted on the shipped record — first-miss time
scales as Δϖ̇⁻¹·(travel to tangency) (G6 ensemble: exponent −1.08, D = Δϖ̇·H = 1.45–1.51 ≈
the exact travel 1.4568; 20 more G4n events, all post-tangency, 34/34 cumulative; results3
regenerates bit-for-bit with the corrected far-tangency column) — but the proposed fix in its
rebuild-cadence form is **refuted**: re-cutting sections at any staleness θ from 0.05 rad
down to per-synodic-passage refresh leaves every missed encounter in place (G6: the same 5
events at every θ; G2: 1; G4n: 1), because they are **fold events** — conjunctions whose
depth turns on within ~3×10⁻³ rad of differential rotation (measured: at the exact passage
geometry every event's distance is reproduced; at ±0.01 rad all are back above the 1.2ρ
safety band) — so only evaluating the section at the exact current Δϖ per passage (the O(1)
integer-add ride, now load-bearing rather than polish) certifies them, and no kick cadence
shadows them (the miss set is invariant in re-cut cadence).

- **Bottleneck.** Board focus "finding encounters without work per orbit or per element
  change"; top scaling risk. The horizon bounds the standing certificate; this run measures
  what re-setup rate actually buys (waste only, not safety) and what the fix must be.
- **Novelty.** Second-author run on 20261007-1550-dynamics-71a5 (gold/silver split). The
  fold mechanism and the invariance of the miss set under re-cut cadence are new; r8 v3's
  cone theorem governs orbit-pair tangencies, not conjunction-family folds under drift.

## Evidence

Instrument: the run's own (`cert.py` unchanged; brute-force truth = `pair_minima`,
certificate = frozen proposals, MISS = true minimum < ρ with no valid proposal within
0.4 synodic spacings). My evaluator reproduces the author's stored A2 row at Δϖ̇ = 10⁻³
**bit-for-bit** (C0: misses 1, waste 27, props 27, earliest = 1458.6059965793488). New
machinery: piecewise-frozen windows — a window cut at t_w is the pair frozen at its t_w
elements, an exact rigid time-translation of the frozen list, so one brute-force truth
serves every policy; staleness θ = |Δϖ̇|·(t − t_w). All numbers in `work/results4.json`;
machine state inside. ρ = 4×10⁻³, safety 1.2ρ, T = 1500 (3000 for G4n), grid 2²¹ (2²²).

1. **Controls (all exact).** Kepler (zero drift): 0 misses, 0 waste on G6 (27 proposals)
   and G2 (4). Rigid equal-precession on deep-crossing G2 (both Ω = 0.05): 0 misses,
   0 waste, m0_true = 0.003627814391298531 vs frozen 0.003627814391297579 — the rigid
   rotation is an exact symmetry at e = 0.4 too (prediction 5 held).
2. **E1 — first-miss scaling, now fitted (silver gap i).** G6, 12 conjunction phases,
   Δϖ̇ ∈ {1,2,3,5,10}×10⁻³: misses 1/9/5/6/10 (at all five rates; fit on the four with ≥3
   missing phases). Earliest first-miss vs rate: exponent **−1.078**; D = Δϖ̇·H_earliest =
   1.4586, 1.4852, 2.0022, 1.5137, 1.4534 ≈ the exact travel to the next tangency
   (Δϖ₀ + Δϖ* = 0.73 + 0.72682 = 1.4568). Median first-miss exponent −0.571 (waiting-
   dominated), the safety-vs-realization split the pre-registration asked for. The G6 pair
   under body-i precession sweeps out of and back into the Binet crossing zone; the first
   miss rides the re-entry tangency exactly as G4n's rides its far tangency.
3. **E2 — safety vs realization on the "never" pair (silver gap i, second arm).** G4n,
   6 phases × 4 rates (T = 3000): 20 realized sub-ρ encounters, **0 before t_tang** (with
   the author's and checker's events: 34/34). Tangency arithmetic re-derived in closed form:
   Δϖ* = arccos((V_i²+V_j²−ΔU²)/(2V_iV_j)) = 0.726924, far travel 1.426924 — matching the
   first checker's independent bisection. Earliest-per-rate delays 31.5/210.3/121.5/66.7
   show no rate trend (realization waiting is rate-independent); the linear fit of
   earliest t_first on 1/Δϖ̇ gives slope 1.350 (5% under travel; waiting bias, disclosed),
   the all-events fit 0.540 (waiting-dominated — my prediction 2's slope = 1.4268 ± 0.03
   failed as written; the invariant form held).
4. **E3 — the fix, rung where non-vacuous (silver gap ii): refuted in rebuild form.**
   Staleness sweep on G6 (12 phases, Δϖ̇ = 3×10⁻³ ≈ a belt pair at Δp/p ≈ 5%) and G2 (deep
   crossing, cone gap −0.138, e = 0.4): misses are **invariant in θ** — G6: 5 at every
   θ ∈ {0.05, 0.1, 0.2, 0.45, 0.9, ∞}; G2: 1 at every θ; θ = 0.05 is one refresh per
   synodic passage. What re-cutting does fix is decorrelation: G6 waste 27 → 11–13
   (frozen → any θ). On G4n at θ = 0.2 the certificate's only realized event (t = 1980.6)
   is still missed. The checker's "0 misses at θ = 0.05/0.2" probe does not survive the
   full ensemble: it held on the phase it was run on.
5. **E6 — the miss mechanism is a fold, measured.** For all six persisting events (G6
   667.4, 917.1, 1394.1, 1086.5, 975.0; G2 747.8): scanning the passage distance against a
   differential-rotation offset around the exact event geometry (Q(δ) reproduces the true
   pair exactly at δ = Δϖ̇·t — validated: offset-0 minimum = the measured event depth, e.g.
   0.001875 vs event 0.00188) shows the depth collapses outside a band of **~3×10⁻³ rad**
   (G6; G2 up to 10⁻²): at |offset| = 0.01 every event is back above the 1.2ρ proposal
   band. So the encounter appears through a conjunction-family tangency where ∂d/∂Δϖ ≈
   1–2 per rad: no fixed re-cut cadence — and no per-orbit re-evaluation (staleness
   Δϖ̇·P = 0.019 rad at this rate) — can certify it. Evaluating the section at the exact
   current Δϖ does (offset-0 depth < 1.2ρ in all six cases).
6. **E5 — the record regenerates (silver gap iii, record).** The author's results3 grid,
   recomputed from shipped code: all 12 `first_sub_rho` values **bit-identical**; 7
   realized events, all after the corrected far tangency t_tang = 1.426924/Δϖ̇
   (2853.8/1426.9/713.5). `work/results3.regen.json` carries the corrected 4-column record
   (the stored third column encoded the near-side travel of the direction not run).
7. **Shadowing, settled by measurement (silver gap iii, cadence).** Kick cadence K and
   staleness θ are one parameter (a re-cut every K = θ/|Δϖ̇|). Since the miss set is
   invariant in θ, **no cadence shadows the folds**: the dossier's "orbit-averaged kicks
   act once per orbit, the same order as the horizon" is not merely off by 1.5–2.6 decades
   (the checker's arithmetic, confirmed) — cadence cannot buy fold safety at all. What
   cadence buys is waste control (27 → 11). Engine translation: the certifiable staleness
   3×10⁻³ rad ÷ 0.038 rad/orbit (10% belt at p ≈ 50 M) = **0.08 orbit**; at the weak-field
   scene (3.6×10⁻⁹ rad/orbit) it is ~10⁶ orbits — frozen sections remain fine there, as
   the author claimed.

## Predictions (predictions.md, written before the decisive runs)

Held: 1 (scaling: misses at 5/5 rates, exponent −1.078 ∈ [−1.3, −0.4], D ∈ [0.2, 2]),
5 (controls exact). Partial: 2 (0 pre-tangency events ✓, rate-independent delays ✓, but the
slope = travel ± 0.03 fit failed at 5% — waiting bias; the all-events fit is the wrong
instrument and I report it as such). **Failed: 3 and 4, decisively** — piecewise θ = 0.2 and
per-passage refresh both leave 1 miss (G2), and there is no crossover K*: the miss set is
invariant in cadence. My pre-registered kill criterion for 3/4 engaged: this dossier reports
the measured law (the fold mechanism and its width) instead of the staleness-threshold
story. The frozen arm of 3 also under-delivered (1 miss over 4 phases, not ≥3: G2 exits its
crossing zone at t = 148 at this rate, so the ensemble realizes few events).

## What would make it wrong

The truth model is the uniformly precessing conic — the tube's compiled form, by design.
The fold conclusion rests on six events at e ≤ 0.4, prograde, coplanar, one geometry class
each for G6/G2/G4n; the fold-event rate per pair per orbit (what the tier's leak budget
would need) is not estimated — that needs an ensemble over geometries, i.e. a crate rung.
The exact-Δϖ fix is verified geometrically (offset-0 reproduction of event depths), not by
implementing the crate's section arithmetic; "the section evaluated at current Δϖ resolves
folds" is a statement about the geometry the crate's Binet-cone sections encode, argued from
r8 v3's machinery, not measured in Rust. Kicks that change elements mid-drift, the resonance
shelf, retrograde/inclined pairs and e > 0.7 remain untested, as in the original run.

## Cost of adopting, and fit with PRINCIPLES

Adopt: (a) the aging law as fitted — first miss = travel-to-tangency/Δϖ̇ (tangency of the
Binet crossing zone, in either direction), waste decorrelation by Δϖ̇·t ≳ 0.5 rad; (b) the
design correction: sections evaluated at the **exact current Δϖ per synodic passage**
(O(1) integer adds per pair per passage — the cost class the author already proposed per
cycle), with rebuild cadence demoted to a waste/cost knob; (c) no reliance on kick cadence
for safety. Principle 13 ("we don't want errors that can compound"): the fold miss is
exactly the silent, unbounded leak type; principle 32 ("under the right representation
many symmetries can appear"): the representation that restores the symmetry is the
co-precessing evaluation at passage time, not a re-cut; principle 3 (compute only
surprises): per-passage O(1) updates, never per-orbit window setup.

## The lens may have made me miss

A second author inherits the instrument: one brute-force harness, so my "independent"
confirmation shares `cert.py` with the author and both checkers (the 5 October lesson —
agreement is not independence). The 12-phase ensemble is small for tail statements; fold
widths are sampled at 3 points per side, not fitted; and I spent the calibration budget on
G6/G2 folds, leaving G4n's near-tangency soft zone unscanned.

## Reproduce (Linux/x86, 8 vCPU, each step's wall time noted; every process < 300 MB)

    cd lab/results/20261007-1646-second-20261007-1550-dynamics-71a5-f282/work
    for i in 0 1 2 3 4 5; do python3 jobs.py --shard $i/6 & done; wait   # ~12 min, 860 truths
    for i in 0 1 2 3 4 5; do python3 extra_jobs.py $i 6 & done; wait    # ~10 min, +728 grids
    python3 second.py    # < 1 s: controls, E1–E6, writes results4.json
    python3 regen3.py    # < 1 s: corrected results3 record + bit-identity check
