# Dossier — run 20261008-0041-redteam-ecfd (premise red-team)

## Claim

The two-body doll's premise — exact Schwarzschild geodesic + 1PN energy map,
"ν only through the energy map" — **survives its first 2PN measurement** (worst
case +0.36% periastron error at the gate's hardest seed ν=0.25, p̄=20M, e=0.6,
c₂ gap 0.06 vs 4.5); the attack lands one level up: **B11's precession
criterion carries no GR information at any p̄ in its range** — its 1PN-oracle
reference is 5–170× farther from the shipped law than GR is, and its tolerance
(1% + 16/p̄) is ≥3.6× the 2PN effect everywhere, so it passes a law whose 2PN
periastron correction has the **wrong sign**. Fourth member of the
oracle-domain defect family (B12, B13, B17 — HANDOFF's trap list).

## Bottleneck

Not a compute bottleneck: a **gate-validity** hole on the frozen B11, which is
about to judge the motion law v2's binaries. Closes H0183's flagged gap ("No
2PN comparison ... either 2PN on both sides, or a convergence-order gate" —
never run). Gain: B11's precession leg goes from certifying nothing GR-shaped
to certifying the law against 2PN GR with a 1.5 s reference; deletes nothing
in the law (the law needs no change — that is the result).

## Evidence

Everything from `python3 falsifier.py` (1.5 s, float64, scipy; writes
`falsifier-out.json`). Method: all orbits built from **identical geometric
turning points** (u_p, u_a), so no coordinate or (p,e)-label ambiguity;
`shipped` = exact Schwarzschild advance (the eob-doll's shape; the energy map
moves the orbit only at 2PN order), `GR2PN` = 2PN EOB Hamiltonian with
A = 1−2u+2νu³, D = 1−6νu² (Damour, arXiv:1212.3169 eq. 18–19, fetched and
read this run), F = A²D. Controls: EOB(ν→0) reproduces the exact advance to
≤1.8e−6, H_eff drift ≤4e−15, integration matches the closed form
2π(1/√(1−6/p̄)−1) to ≤0.85% (the closed form's own e-dependence).

| p̄ (M) | shipped − GR2PN (ν=.25) | (ν=.1) | 1PN oracle − shipped | B11 tol |
|---|---|---|---|---|
| 20  | +0.36% | +0.14% | −23.8% | 81% |
| 30  | +0.08% | +0.03% | −15.7% | 54% |
| 50  | −0.01% | −0.005% | −9.3% | 33% |
| 100 | −0.03% | −0.01% | −4.6% | 17% |
| 1000 | −0.01% | −0.01% | −0.45% | 2.6% |

c₂ (advance = 6πu(1+c₂u), fit p̄∈{30,40,60,80}): shipped 4.490, GR2PN
ν=0.01/0.1/0.25 → 4.493/4.514/4.548; gap(ν=0.25) = −0.058 (e=0.6), −0.023
(e=0.3). Apsidal drift at the hardest seed: 0.0044 rad/orbit → 1 rad in ~230
orbits. The oracle family follows −4.5/p̄ exactly (measured 0.238/0.226 at
p̄=20 vs predicted 0.225). Sign-flip check: a law with the 2PN correction's
sign reversed deviates from the 1PN oracle by exactly |4.5/p̄| ≤ tol/3.6 at
every p̄ ∈ [20,1000] → **B11 precession passes it at every seed**.

## Predictions

`predictions.md` was written before the decisive run (calibration: ν→0 control
at one p̄ only). Held: scale and monotonicity in ν (1, 2), oracle family
−4.5/p̄ from my own integrator (4), c₂ fit 4.5±0.1 for shipped and GR2PN(0.25)
inside the predicted [1,8] (5), B11 reach arithmetic (6). **Failed: 3** — the
D̄ sign matters at strong field (2.8% at p̄=20, not <1e−3): p_u ~ e/u is not
small, so D̄'s "3PN-scale" term moves c₂ by 0.58. Resolved by grounding on
Damour eq. (19): D = 1−6νu². Checkers beware: D̄ = 1+6νu² (my first memory)
gives c₂=3.96 and a false "+3.2% GR error at p̄=20" — that number is the
wrong-oracle artifact, not physics.

## What would make it wrong

The shipped law's orbit at fixed real invariants is not exactly the geodesic
through those turning points (the energy map shifts them at 2PN, same order as
the effect measured); an EOB-coordinate comparison at fixed turning points
carries e-dependent labeling systematics (~0.02 in c₂, from the e=0.6/0.3
spread). Both are ≤ the quoted bound's own margin — the survival verdict is
robust; the third decimal of c₂ is not. Adoption cost: none for the law; for
B11, re-point its precession oracle (ν→0/small-ν seeds: the exact Darwin
oracle the project already owns; ν>0: this script, 1.5 s) or restrict its
precession judgement to p̄ where the 1PN oracle can vouch (≥450M for 1%).

Fit with PRINCIPLES: "Measure before claiming, and never strawman" — the 1PN
claim had never been measured against GR; "A laboratory result never counts as
integrated qualification ... gates judge a representation" — B11 currently
judges nothing; "errors never compound" (13) — the residual 0.36%/orbit apsidal
drift accumulates unboundedly but at 230 orbits/rad sits far below any player
floor at every scale the plane has today (planetary p̄ ~ 10⁹M: zero).

## Ranked attacks (the lens's deliverable), by player visibility

1. **Two-body doll at 2PN (this run's falsifier).** Premise survives with a
   first measured bound; the defect is B11's precession criterion (above).
   Criterion that should have caught it: **B11's** — none does today; r3 v1
   saw the symptom ("oracle's own truncation about 72% at p=20, contaminated")
   and v3 widened the tolerance instead of measuring GR.
2. **Binet cells as "the primary in-cell solution" (representation.md §1).**
   Already killed by `space-darwin16-v1` (law.md: band-centre tangent slope
   error at turning points), yet the design doc still presents the Minsky map
   as primary — a builder reading it rebuilds a killed mechanism. No rung
   needed; the doc line must die. Not edited here (docs are not mine).
3. **Kicks and cycle derivatives absorbing perturbations.** Scoped survivors
   with named kills already on record (r4 v2/v3 resonance, r9 precession above
   τ₀=0.0036, df81 jet re-anchor, redteam-4643 re-pay ceiling). Open hole:
   deep flybys (m-meso-motion's conditional). No new rung gap.
4. **Dense order bit-identical to sparse (r5 open).** The tie rule (6254)
   covers same-epoch same-body batches; the residual is same-root-time
   **lightlike**-separated events across dolls with different tick grids
   (15–1,400 ticks at a sphere's edge, HANDOFF) — ordering is undefined until
   root-clock event keys (law step 4) land. r5 as scoped (single-doll scene)
   cannot catch it; its criterion should add a two-doll lightlike-tie case.
5. **View gathered at the past light cone (r6 open).** Newton seeded from the
   previous frame's crossing has no stated fallback: at γ ≳ 100 with a hard
   course reversal (the plane's L15 burn reaches β=0.999) the seed can leave
   the basin mid-swing, and `deflection(b)` has a log divergence approaching
   the photon ring. Prediction for r6: iteration/divergence count at a
   high-γ U-turn, branch continuity across it. Not run this window (time);
   registered here so the rung can freeze it.
6. **"≈0 cost for undisturbed bodies" (§6 table).** Fine at representation
   level (a cycle is additions); the real cost is kick cadence × candidate
   resets, already the board's live lever (slack skin 12.6×). No gap.

A premise that survived is worth reporting (lens brief): the EOB resummation
choice is 66× better than its own gate believes at p̄=20 — the design
under-sells its accuracy, and now that is measured, not assumed.

## The lens

Red-teams overweight exotic cases; I ranked by player visibility and the
two-body attack is invisible at today's planetary scales — its value is the
gate fix before B11 judges the motion law v2. What this lens may have missed:
everything requiring the integer law or the real crates (I measured the
design's float truth, not the shipped Rust); and the merger regime p̄ ≲ 15M,
where PN itself dies and the design currently has no representation and no
oracle (plunge tubes are queued) — flagged, not probed.
