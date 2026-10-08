# dossier.md — 20261008-0458-second-20261008-0338-library-f045-0102 (second author)

## Claim

The original run's one measurement — A(τ) crossing 1 at 0.17 < τ* < 0.25, "on top of
r9's τ₀" — is dead twice over: its harness carries three defects (one teleports the
particle ~180° at step 1 of every run; another fires a sign error at 70–75% of kick
steps; the third mislabels every cadence by 2π), and on a corrected harness the
checker-named experiment (median A16 over 12 secondary phases, fixed μ = 1e-3, true
cadences) shows **no phase-robust τ-crossing**: the median is non-monotone (0.85,
1.24, 2.08, 0.57, 0.74, 1.07, 1.14 across τ = 0.05–0.30), *below* 1 exactly inside
the claimed crossing window, with quartiles straddling 1 nearly everywhere. The
shock-asymmetry regime trigger must not be frozen into q-cadence; that kill is this
run's deliverable, and the checker's conditional engine test (r9 ladder, B14) is
mooted because its premise (a surviving crossing) is gone.

## Bottleneck

Same as the original run: board item 1, kick cadence (q-cadence queued, no rung
file). The decision served: q-cadence must not adopt A(τ) as a regime trigger, and no
future rung may rebuild this toy as written. Gain: a wrong criterion never gets
frozen — gates are frozen before runs, so deleting it before q-cadence writes
criteria is the cheap kind of 10×.

## Evidence

**The three defects** (each reproducible in seconds from this folder):

1. **vr-branch flip** (`shock_probe.py`: `if f1 > math.pi: vr = -vr`): mean anomaly
   wraps to (−π, π], so on the descending branch f1 lands negative and vr keeps the
   wrong sign. Fires at **70–75% of the toy's kick steps** (`flip_rate.py`);
   single-step state error = 2·|vr|, purely radial, with a, e, |h| preserved
   (`single_case.py`: vel_err 1.52e-2 = 2·vr at e = 1e-3, M0 = 4.651; position exact
   to 1e-9). Control (`control_p1.py`): pure two-body drift, e = 1e-3, 4800 steps —
   the original drifts ω by **π rad**; branch-corrected it stays ≤ 9.6e-7 rad.
2. **Circular-start ω-noise teleport**: at the exact circular start the e-vector is
   1.2e-16 of cancellation noise; `om = atan2(ey, ex)` returns its direction —
   deterministically π here — and step 1 rotates the state by it: the particle leaves
   at 183.4° instead of 3.6° (diagnostic in `single_case.py` trace; with `om := 0`
   the full-orbit roundtrip from the same start is 2.0e-16, `v2_controls.py`). Every
   published number — the author's row, the checker's attack rows, my reproduction —
   shares this same rotation, which is why bit-faithful reproduction proved nothing.
3. **2π cadence/orbit mislabel**: `P = a**1.5` but GM = 1 makes the period 2π·a^1.5:
   "1 kick/orbit" was 6.28 kicks/orbit, "16/orbit" was 100.5/orbit, "300 orbits" was
   47.7. The published A(1/16) never compared the cadences its labels claim.

**Reproduction of the published record**: `python3 shock_probe.py` (25 s) regenerates
the author's φ = 0 row digit for digit (A16 = 0.45, 0.80, 0.75, 1.68 at τ =
0.05–0.25; `repro-phi0.log`) — faithful to a broken instrument.

**The named experiment on the corrected harness** (`v2.py`: all three defects fixed;
controls: ω conserved to 7.5e-8 rad over 4800 drift steps, circular roundtrip
2.0e-16, truth converged 4000 vs 8000 steps/orbit to ≤ 7.4e-6). 12 phases kπ/6,
μ = 1e-3, true cadences K = 1/4/16 per orbit, 300 orbits (`sweep_fixed_300.log`,
`finish_300.log`):

| τ_Hill | med A16 | q25 | q75 | min | max | frac>1 |
|---|---|---|---|---|---|---|
| 0.05 | 0.849 | 0.42 | 2.12 | 0.10 | 9.6 | 0.42 |
| 0.10 | 1.236 | 0.74 | 2.73 | 0.02 | 10.2 | 0.58 |
| 0.13 | 2.078 | 0.20 | 3.44 | 0.15 | 8.6 | 0.58 |
| **0.17** | **0.567** | 0.17 | 1.06 | 0.05 | 2.3 | 0.25 |
| **0.20** | **0.742** | 0.37 | 1.11 | 0.08 | 2.8 | 0.25 |
| 0.25 | 1.069 | 0.73 | 3.41 | 0.25 | 52.7 | 0.58 |
| 0.30 | 1.141 | 0.91 | 6.48 | 0.36 | 105.7 | 0.67 |

No crossing at 0.17–0.25: the medians there sit *below* 1 while τ = 0.10–0.13 sit
*above* — the opposite ordering, non-monotone, quartiles an order of magnitude wide;
at no τ does even 70% of phases agree on a side of 1. The 150-orbit horizon
(`horizon_150.log`: 0.767, 0.940, 2.02, 1.111, 1.044, 0.833, 1.113) stays within a
factor 2 of the 300-orbit medians but reshuffles the τ-structure (0.17 flips 0.57 →
1.11) — the median's shape is horizon-sensitive, not a regime boundary. The author's
own φ = 0 column on v2 (`phi0_and_detail.log`) reads A16 = 0.102, 0.945, 0.093,
3.402 — the published monotone row does not regenerate, and even at fixed φ = 0 it is
non-monotone; at the claim's own τ₀ = 0.17 fine sampling (K = 16) is 10× *worse*
than batched (K = 1). Per-phase A16 at τ = 0.25 spans 0.25–52.7 (the denominator
collapses at some phases): the ratio is ill-conditioned per phase, so only the median
could have carried the claim — and it does not.

Deeper reading for the cadence rung: median err16 ≈ median err1 at every τ (e.g.
τ = 0.05: 6.4e-3 vs 8.5e-3 per orbit) — 16× the kicks buys almost nothing in dω,
because the error is phase-coherent kick-sampling error, not a quadrature tail. The
toy therefore never supported a batching-vs-sampling convexity measurement at these
cadences, broken or not.

## Predictions (`predictions.md`, written before the decisive runs)

Held: P1 (original drifts ω by π; corrected ≤ 9.6e-7 — exact); P2' (the author's row
does not regenerate on the sound harness); P4' (150 vs 300-orbit medians within a
factor 2 at every τ; worst 1.96 at τ = 0.17); amendment controls (a) and (b) passed
((c), a vec/scalar agreement rerun, was not repeated on v2 — the propagator controls
(a)/(b) subsume it). Failed, and reported: P3's point estimate ("median < 1
everywhere, 0.2–0.9") — the corrected harness puts medians *above* 1 at τ = 0.10–0.13
(1.24, 2.08). The decisive substance — no phase-robust crossing at 0.17–0.25 — held.

## What would make it wrong; cost; fit

Wrong if: the v2 harness is itself defective (its controls pass: ω conservation
7.5e-8 rad over 4800 drift steps; circular roundtrip 2.0e-16; truth converged to
7.4e-6); or if the toy, however corrected, simply cannot represent the engine's
cadence question (likely — its dω error is kick-phase-coherent; the engine's B-gate
judges see different observables — which is exactly why the trigger was never
allowed onto the engine). Cost of adopting the kill: zero — it deletes a criterion
and adds none. Fit: PRINCIPLES 2 ("'Exact' means deterministic and reproducible" —
the published row was reproducible but meaningless), 20 ("behaviours over many
seeds" — the original was one phase of a broken instrument), 9 ("a failed experiment
kills that configuration, never the method" — cadence itself is untouched), 13
(compounding sign errors at 70% of steps).

## What the original checker got right and what it missed

The checker's phase/mass/horizon attack was correct in result and is confirmed — but
it attributed the fragility to physics ("one cell of a surface fragile in phase, mass
and horizon") when the instrument itself was broken three ways. Its own reproduction
inherited defects 2 and 3 silently: both are deterministic, so bit-faithful
reproduction was no evidence of soundness — two independent finders shared one
harness, the 5 October lesson, again. Lesson for the lab: a float toy that reads the
direction of a ~1e-7 e-vector must pass an element-invariance control in pure drift
(a 60-second test, `control_p1.py`) before any number it emits counts, and any
"orbits per run" or "kicks per orbit" label must be checked against the period
formula actually used.

## The lens (second author)

I nearly ran the named sweep on a one-line-fixed harness that still carried defects 2
and 3 — the vectorized/scalar disagreement (6.7e-3 in dω from formulas that should
match) is what forced the audit; a scalar-only second author would have shipped the
half-fix and reported noise as the answer. What I may have missed: the checker's
conditional engine ladder (double kick size across r9's Hill range, B14 judge)
remains the right *positive* experiment if the integrator ever wants a cadence
trigger — but it must start from the engine, not from a toy rebuilt from this one.
