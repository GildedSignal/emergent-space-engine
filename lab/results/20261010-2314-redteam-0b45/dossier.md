# Dossier — redteam 20261010-2314: the view's gather has no clock

## Claim

The design's view gather (one Newton solve of the emission time plus a
deflection(b) memo for the direction) reads every moving emitter near a compact
mass at the wrong retarded time: measured on exact Schwarzschild null geodesics,
a body orbiting at 6–20 M is drawn 7°–86° of orbit out of phase (median 1°–66°),
i.e. 3.7–150 % of its orbit radius, 2–7 px at 1080p framing the whole system and
30–741 px zoomed to the orbit — and **no rung or gate anywhere judges the view's
timing** (r6 is unwritten, and as specced in representation.md §7 it measures
only "Newton iterations and samples per frame").

## Bottleneck

Not a cost bottleneck: a correctness hole in "knowledge", which Julien ranks
with navigation and dynamics as what "need to be perfect" (OC#16, principle 30).
It hits the marquee content (anything orbiting a black hole), the AI (perception
is the same gather, adopted merge candidate 1), and it oscillates over each
orbit, so the sky visibly breathes near compact masses. Expected gain of fixing
before build rather than after: deletes a wrong-implementation class from r6
before it is written.

## Evidence (all commands ≤ 60 s, float64, Linux x86)

Setup: Schwarzschild G = c = M = 1, equatorial plane (the game's plane).
Observer static at r_o = 1000; emitter on an exact circular orbit (dφ/dt =
r^(-3/2), exact in Schwarzschild coordinate time) at r_e ∈ {6, 8, 10, 20, 50}
(local β = 0.50, 0.41, 0.35, 0.24, 0.14); 60 orbital phases, primary image.
Oracle: null geodesics from first integrals, (du/dφ)² = 1/b² − u² + 2u³,
dt/dφ = 1/(b u² (1 − 2u)), composite Simpson with a turning-point substitution.
Attacked gather: the emission event from t_obs − t_e = Euclidean distance (the
only light-time the spec's mechanism implies), solved exactly (bisection; the
attack is the residual model, not Newton's convergence).

| r_e | β | emission-time error (M), median / max | orbit-phase error, median / max | displacement max | px, full frame / orbit zoom |
|---|---|---|---|---|---|
| 6 | 0.50 | 17.1 / 22.1 | 66.5° / 86.0° | 9.0 M (150 % of r_e) | 6.2 / 741 |
| 8 | 0.41 | 15.9 / 18.5 | 40.1° / 46.7° | 6.5 M (82 %) | 6.6 / 585 |
| 10 | 0.35 | 14.5 / 16.8 | 26.3° / 30.5° | 5.3 M (53 %) | 5.8 / 417 |
| 20 | 0.24 | 10.9 / 14.6 | 7.0° / 9.3° | 3.3 M (16 %) | 3.8 / 136 |
| 50 | 0.14 | 7.7 / 13.1 | 1.2° / 2.1° | 1.9 M (3.7 %) | 2.1 / 30 |

Mechanism, two parts: (i) the flat light-time misses the curved optical path
time (the climb-out floor alone is 2M·ln((r_o−2M)/(r_e−2M)) ≈ 10.8 M at r_e = 6);
(ii) the moving emitter amplifies it by the apparent-motion factor
1/(1 − β∥): measured 15.7 → 22.1 M (×1.41) at r_e = 6. At β = 0.9 this factor
reaches 10, so a relativistic fleet stream near a compact mass is smeared by
tens of M along its motion.

Controls (instrument checks, `check_oracle.py`):
- flat limit reproduces branch-aware closed forms: Δφ to 1e-13, T to 9e-5;
- exact radial anchor T = (r_o−r_e) + 2M·ln((r_o−2M)/(r_e−2M)): rel 6e-10;
- independent RK4 integration of the Binet ODE u″ = 3u² − u at the solver's own
  b (16 spot-checks, both branches): Δφ to 1e-7 (its grid limit), T to 1e-4;
  the measured effects are 4–5 orders above the instrument floor.

Commands, in `lab/results/20261010-2314-redteam-0b45/work/`:
`python3 check_oracle.py` (~2 s), `python3 shapiro_gather.py` (~25 s, writes
`shapiro_results.json` with all rows), log frozen in `evidence.txt`.

Which gate should have caught it: **none exists.** B3 judges deflection (angle),
B7 clock *rates* (local formulas), B16 moving-lens deflection (angle); r6 is
named in representation.md §7 but unwritten, and its stated criteria are cost
only. Rung r6 as it should be written: retarded emission events of moving
emitters vs an exact-geodesy oracle, timing error below one pixel at the
player's floor, at conjunction and quadrature, with a flat-light-time gather as
the planted negative control (it must fail).

## Predictions

`predictions.md` was written before the decisive run. What happened:
- Flat control: PASS after I fixed my own comparison (the machinery was right;
  my first control used the wrong branch formula — caught, corrected).
- Oracle vs textbook 2M·ln(4r_e·r_o/b²): **my formula was misapplied** (it needs
  periapsis b ≪ endpoints; this geometry has periapsis = r_e). Replaced by the
  radial anchor + RK4 cross-check. Held-out miss, reported.
- δt = Δt_Shapiro to 1e-6: **MISS** — the moving-emitter coupling
  1/(1+Ω·d′) rescales it first order; measured ×1.41 amplification. The miss
  strengthens the attack (apparent-motion amplification).
- Magnitudes: all four quantitative bands were exceeded in the same direction
  (measured larger): max 18.5 vs predicted 5–15 M; median 15.9 vs 2–6 M;
  displacement 6.5 vs 1–4 M; zoom px 585 vs 50–200. My Fermi estimate missed
  the climb-out baseline delay.
- β scaling and the cost-table Fermi (premise 6): held.

## What would make it wrong

If the intended gather already evaluates the photon tube's own t(φ) as the
light-time — the design text nowhere says so (representation.md §2 and law.md's
observation section name only the Newton crossing and the deflection memo, and
the view's cost table has no delay term). A strawman reading would be unfair
only if "gathered at the past light cone" were defined operationally somewhere;
it is not.

Cost of adopting the fix: small and in-hand. The compiled photon cycle already
integrates dt/dψ (law.md §Motion, light: "the same map parameterized by b");
storing T(b) next to deflection(b) in the doll memo makes the curved light-time
one lookup, and the crossing solve uses it per doll segment, summed along the
light path (a log-add per sample, same order as the deflection lookup; still
"one sample per pixel"). The fix must also enter AI perception, which is the
same gather.

Fit with PRINCIPLES: "what really matters is navigation, knowledge and dynamics
those need to be perfect" (principle 30); "The view is an instrument … real vs
displayed is not the same thing" (principle 28) — the view's *timing* is the
instrument's reading, and it is systematically wrong. Also principle 3, "compute
only surprises … clocks, redshift, views are derived not evolved": deriving the
crossing with flat time is deriving the wrong event.

## Ranked attacks (all six lens premises; rank = likelihood the player sees it)

1. **View gather timing (premise 5)** — measured above. No rung. Top attack.
2. **Dense/sparse bit-identity (premise 4)** — unrung (r5 unwritten). Named
   crack: law.md applies dense-region tide kicks "at epochs" and sparse kicks
   "at a fixed step in the drift's own phase"; for a body fed by both (region
   boundary, or a region going sparse↔dense mid-run), the same physical kick
   lands at different phases per order → different integer rounding → different
   bits, violating B8's promise. r5 as it should be written must contain a
   *transition* case, not just a static dense region. Not falsified here:
   it is an integer claim needing both orders (out of this run's 60-minute
   budget); argued from the two spec sentences.
3. **representation.md integrity** — three load-bearing mechanisms in the
   design doc are already falsified or retired by law.md, and the doc still
   teaches them: §1 "Binet cells (the primary in-cell solution)" with Minsky's
   map (replaced by `space-darwin16-v1` after a first-order slope error at
   turning points, law.md §Motion); §1's Clohessy–Wiltshire closed form (now
   the Fermi normal frame, law.md §Causality); §3's "a kick updates the cycle
   by a multiply-add" (killed by red-team 20261006-0346-redteam-df81; law.md
   adopts re-anchoring and calls the derivative jet "Not adopted"). A builder
   reading the design doc builds dead mechanisms. No rung covers docs; the
   doc's own freeze condition ("until the falsifiers in §7 have run") has been
   overtaken by law.md without the design doc being rewritten.
4. **Missing behaviour: resonance shaping populations.** A player looking at a
   belt sees Kirkwood gaps; B18b judges a *smooth* belt's statistics and B17
   one resonant pair; no gate that resonances *shape* a population. Ungated,
   and cheap to add to B18b's ladder.
5. **Two-body doll (premise 1)** — survives at its stated scope: ν-only-in-the-
   energy-map is exact at 1PN (standard EOB), confirmed r3 v3 and B11. Scope
   note: at B11's own inner seeds (p ≈ 20 M, ν ≤ 0.25) the 2PN terms are of
   the same size as the gate's tolerance (1% + 2·8/p = 1.8 %), so the gate
   cannot distinguish 1PN from 2PN there — the oracle-domain lesson again,
   not a falsity.
6. **Costs ≈ 0 for undisturbed bodies (premise 6)** — survives the Fermi check:
   10⁹ bodies × 0.3 kicks/orbit ÷ 10⁴ s ≈ 3×10⁴ kicks/game-second, consistent
   with §6's 6×10⁴ at 50 ns each; the resonance-adjacent ~10 % of a belt
   (within W = 2.5·μ^(2/3) of strong low-order resonances at μ ≈ 10⁻³) triples
   their kick rate and stays far below a core. H_live (memory) stays the real
   unknown, as HANDOFF already says. A surviving premise, as the lens allows.

Principles scan beyond the above: the dense order's lockstep is defensible
against principle 14 ("a tick wastes nothing when everything changes every
tick") *inside* a dense region; the crack is only the boundary (attack 2).
"Fleets, battles" as doll triggers are dimensionless in the text (events per
cell per light-crossing), so no principle-4 violation. The error model's
"never compounds" (principle 13) currently rests on B12, which is
miscalibrated and being rebuilt — known, not re-derived here.

## The lens

A premise red-team overweighted exotic geometry before rank: my first run's
most spectacular row (r_e = 50 behind the mass, −33.6 M) turned out to be my
own quadrature error at a near-tangential endpoint, not physics — a red-team
that had stopped there would have reported a wrong number loudly. The lens also
biases toward the measurable: attack 2 (bit-identity) is likely the more
load-bearing *engineering* risk but got analysis only, because a 60-minute
budget cannot build two evaluation orders. And this lens reads design docs
closely and runs little code, so cost-side premises (6) got arithmetic where a
probe would be better.
