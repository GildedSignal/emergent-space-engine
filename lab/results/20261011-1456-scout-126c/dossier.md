# Dossier: plunge and radial tubes — extended Darwin variables, falsified in float

**Run:** 20261011-1456-scout-126c (scout lens). **Machine:** Linux CI, 8 vCPU, load recorded in `metrics.json`. Wall: ~30 s per full run.

## Claim

Extended Darwin variables (Blanco 2026, arXiv:2604.28140, "Beyond the Separatrix") are the
representation the compiler lacks for plunge and near-radial orbits: the same
`(f, A, phase)` form with `φ(η) = cosh(η−η₀)` in place of `cos η`, classified exactly by the
root structure of the radial cubic, ending in an exact terminal event — measured in float to
oracle accuracy at bound-orbit panel cost in every massive sector, including the kick across
the separatrix that the plane today refuses as `NoBoundOrbit`.

## Bottleneck

Board focus item "the motion law v2, finished: plunge and radial tubes" (HANDOFF, Headed next
3); risks list "orbits with no tube". `crates/space/ENVELOPE.md:93` states the gap: "Plunges,
radial L=0 paths and horizon arrival times remain outside this compiler"; bound generators
stop at the separatrix (p > 6+2e). The directed build `lab/lenses/b-plunge-tubes.md` is
queued on it. Gain: deletes a refusal class (B13 draws at steps 7–10, Julien stopped dead
relative to a planet), one representation instead of a new orbit category.

## Requirements (numbers, tied to PRINCIPLES)

- Cover every massive sector of Schwarzschild geodesics: outer (V_max < E² < 1), direct
  (E² > 1 past the barrier or no barrier), inner (both the bound/plunge inner branch and
  E² < V_min), near-radial L→0, plus the kick that crosses the separatrix mid-orbit.
- Terminal events exact: star surface (all clocks finite) and horizon in proper time
  (law.md line 27: E and L go to the doll's ledger at that event; coordinate t has no
  finite value there — the photon `light::Capture` precedent).
- Error type over error size (principle 2): fixed panels at fixed cuts ⇒ identical error on
  every evaluation; nothing is stepped (principle 14).
- Cost at the bound cycle's own budget (B9-analog): panels per branch, not steps per orbit.
- Classification is an integer decision (floats explore; canonical outcomes exact).

## The candidate, and how it maps onto the law

`r̃ = 1/(f + A·φ(η))`, `f = ½(1/r₊ + 1/r₋)`, `A = ½(1/r₊ − 1/r₋)`, `φ = cos η` (bound/scatter),
`cosh(η−η₀)` (inner plunge), `cosh(η−η₀) − 2` (outer/direct plunge). The three roots of
`R(r̃) = Ẽ² − (1−2/r̃)(1+L̃²/r̃²)` pick the sector (their count and order), the same cubic the
law already factors in integers (law.md "Motion in a doll" 2). Phase flow
`dτ/dη = |dr̃/dη|/√R` with `dφ/dη = L·u²·dτ/dη`, `dt/dη = Ẽ/(1−2u)·dτ/dη` — the same
integrand family as the cycle compiler, so the same integer panel machinery applies.
Bound and plunge differ **only** in `φ(η)` and the root pair: one law at every scale
(principle 19), no new category (principle 4). The paper's C² continuation rule (cos to last
apoapsis, then cosh−2) exists for smooth waveforms; for the law a kick simply recompiles from
the new (E, L) anchored at the event state — which is what the law already does on every kick.

## Evidence (all in `metrics.json`; reproduce: `python3 falsifier.py`, ~30 s)

- **Classification (P1 held):** 730 seeds stratified at every boundary (separatrix V_max,
  E²=1, V_min, barrier existence L̃²=12), root-structure rule vs brute-force DOP853
  trajectories: **0 mismatches** (40 near-turning starts undecided, excluded; ties
  pre-excluded at 1e-9). Plunge-vs-not is exact algebra.
- **Terminal accuracy vs an independent second-order geodesic oracle (DOP853, rtol 1e-12):**
  - outer, no barrier: max rel err 4.3e-7 at 64 uniform-η GL4 panels; 1e-9 at 8–16 panels.
  - direct from r=10⁴: 1.6e-11 at 64 **geometric-u** panels (uniform-η gives 0.35: the
    u→0 tail needs the passage machinery's shrinking panels — ENVELOPE already does this).
  - inner: Δφ, Δτ at 1e-7 (1e-12 below V_min with anchored pairing); Δt at a terminal
    r=2.001 only 1.7e-2 because coordinate t **log-diverges** at the horizon: measured
    slope 2.001–2.13 against the predicted 2 (P6 held). τ- and φ-terminals stay exact;
    absorption is a proper-time event (the ledger rule).
  - near-radial: the paper's literal pairing `1/Re(r̃₊)` cancels catastrophically as L→0
    (error 3e-9 at L=10⁻², leaves the allowed band at L=10⁻⁶); with a **fixed anchor
    partner (2M)** every L down to 10⁻⁶ gives 8 panels, 4e-12. L=0 breaks the form
    (double root at r̃=0) — the separate radial path the lens names is confirmed necessary
    (P5 held). The anchored partner is dyadic and needs **no complex arithmetic at all**:
    the compiler factors one real root, pairs it with the horizon anchor.
  - **kick across the separatrix (P7 held — the plane's actual refusal):** 24/24 seeds, a
    bound orbit kicked at random phase into the plunge sector, recompiled and continued:
    terminal (Δφ, Δt, Δτ) errors ≤ 8e-12 at 64 panels.
- **Near-separatrix valley (P2's bulk claim failed, its log-cost sub-claim held):** just
  above the separatrix the trajectory lingers at the barrier top where √R dips to √δ;
  the complex pair is a second branch point the cosh form does not absorb, so uniform-η
  GL4 degrades to fractional order (rel err 0.16 at 128 panels for δ=10⁻⁸). With
  valley-aware cut placement the panel count grows logarithmically:
  **43 (δ=10⁻²) → 83 (10⁻⁴) → 133 (10⁻⁶) → 205 (10⁻⁸)** for 10⁻¹¹ panel agreement, and
  hits a float floor below δ≈10⁻⁹ (no such floor in integer arithmetic). For scale, the
  bound cycle's B9 budget at m=16 is 2m·log₂(r_apo/r_peri)+8 ≈ 78 for the same span.
  δ→0 is the unstable circular orbit, where the compiler's existing exact circular
  generators take over (ENVELOPE v4 boundary).
- **Negative control (P4 held):** GL panels in r with no phase absorption across the
  apoapsis: relative error ≈ 2.0 (100%) at 16→4096 panels. The absorption is load-bearing.
- **Positive control:** the same machinery on a bound half-cycle (apo→peri):
  3e-12 at 8 panels (mid-field), 5e-8→1.6e-12 at 16 (near-separatrix), 4.5e-11 (near-circular).

## Predictions (`predictions.md`, written before the decisive run)

P1 held (0 mismatches); P3 held (8–16 panels vs bound's 8–16, outside the valley);
P4, P5, P6, P7 held. P2 held in the bulk but failed in its near-separatrix clause: 1e-6
at ≤96 **uniform** panels is false below δ≈10⁻⁴; it holds only with valley-aware cuts,
which cost log(1/δ) panels — reported as held-out-failed for that clause.

## What would make it wrong

- The oracle and the candidate share R's algebra; the oracle's independence is its
  formulation (second-order geodesic equation, adaptive step, event location), not its
  physics. A sign or branch error common to both would pass. Mitigated by the negative
  control and the closed-form t-slope check, not eliminated.
- Float-only: the integer law's carries, cut quantization (B9-style bands r_k = 2^(k/m))
  and exact roots are not exercised. The measured panel counts are a lower bound on the
  integer compiler's, not a prediction of its error.
- Kerr is untested (equatorial Kerr is B19's oracle; Blanco's construction is
  Schwarzschild-only; Dyson 2023 covers Kerr plunge in elliptic functions — the same
  root-structure recipe should extend, UNVERIFIED here).
- γ ≫ 1 direct plunges: the literal direct pairing degrades as the negative root → 0
  (E² ≫ 1); that is b-high-gamma's register problem, not tested here.

## Cost of adopting, and fit

One sector extension of `crates/space`: factor the turning root (already integer), pair it
with a fixed dyadic anchor (2M outer / >r₁ inner), choose φ = cosh, cut panels geometric in
u with the cosh phase only for the turning-point stretch, valley-aware cuts within
|E²−V_max|/E² < 10⁻⁴, terminal by root-find in the last panel, ledger absorption at the
horizon in τ. The classification test (root count + position band) is an integer predicate.
No new math library; no closed-form transcendentals. Fit: "if you find yourself fixing
things that's oftentimes a signal that it is the wrong representation" (principle 19) — this
is the opposite case: the bound machinery continues unmodified.

## The lens (what scout may have missed)

Scout optimizes for prior-art fit; the build's real costs (integer cut tables, memo keys for
one-way plunge tubes, the handoff into a plunging doll) are engineering questions this run
does not touch. The paper is 6 months old and uncited in our docs; I did not check whether
Sonnet/Astra already know it — novelty here is against `docs/HISTORY.md` and the docs, which
have no plunge-tube representation (checked: law.md, ENVELOPE.md, board, taste log).

## Grade suggested

Silver-to-gold: every number above is regenerated by one command, held-out predictions were
written first, and it unblocks a queued build within one step. It is not gold by the letter
because the decisive near-separatrix clause of P2 failed as written (uniform panels), and
the fix (valley cuts) is measured only in float adaptive form, not as the law's fixed
integer cuts.
