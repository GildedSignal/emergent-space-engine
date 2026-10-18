# Dossier — 20261018-1126-redteam-1885: "Aggregates are one sample each" dies at high γ

## Claim

The design's aggregate-view premise — "Aggregates are one sample each, and the screen
caps the work at about one sample per pixel" (representation.md L59, L116) with "beaming
k⁴, which in log form are additions… a type × log k table gives the sprite" (L58) — is
refuted in the goal's flagship regime and safe only where nothing relativistic flies:
at β 0.9 with a 3% c line-of-sight dispersion the one-sample sprite is wrong by a median
40% (p90 86%), its brightness jumps 58% per frame (a strobe), and holding a 5% flux bar
by sampling needs 196–799 samples per aggregate, not 1; at β 0.99 with 1% c dispersion
the top 1% of members carry 37% of the fleet's seen flux — exactly the tail Julien
forbids crushing — and the sample-count need is 1.7×10⁴. The failure variable is the
**rapidity dispersion** s = σ_φ = γ²·σ_β (exact: ln k = φ for approach), every error is a
closed form in s, and the player's own motion alone (β_O 0.5, a formation spanning 0.1 rad,
zero internal dispersion) already produces 7% errors and a 9%/frame strobe.

## Bottleneck

Not a current board bottleneck line-item; it is a **premise** hole in the view's cost
and correctness law (§2 observables + §6 "The view ≤ 1 sample per pixel, GPU"). What it
lets us delete if fixed in the design's own spirit: nothing — what it **prevents** is
freezing a view readout (the sprite table, the sample cap) that is guaranteed-wrong at
the relativistic speeds the goal exists to make feelable ("it lets the player feel what
living at high c would feel like"). Expected gain of adopting the corrected readout law:
the cap survives at belts (s ≲ 10⁻⁴) and is replaced by s-dependent sampling/moment rules
at fleets — a law change before any M1 wiring, so ~free now.

## Evidence

Instrument: standalone float NumPy (the shipped plane cannot express mutual β at fleet
scale — gravity-news open direction 3 records the same expressibility wall; standalone
float is the lab's established pattern for it). Exact SR: k = 1/(γ(1−β·n̂)) per member;
bolometric seen flux k⁴ (I_ν/ν³ invariant); colour temperature k·T. **Fleet model exact,
no approximation:** for approach, k = e^φ (rapidity φ; γ(1−β) = e^−φ), so a LOS velocity
dispersion σ_β is a rapidity dispersion σ_φ = γ²σ_β and ln k is exactly normal — every
arm is lognormal by construction and carries a per-arm analytic assertion.

Controls, both sides, all pass: the shared-log-word readout equals exp(−8s²)−1 in every
arm (MC −0.0772/−0.5123 vs closed form −0.0769/−0.5132, and 12/12 fleet arms within
0.02 — printed per run); the Newtonian k=1 readout under-reports the β 0.9 fleet by
628× (the instrument sees beaming); the belt control (β 10⁻⁵, σ_β 10⁻⁵) reads all zeros
(the premise is safe exactly where B18 tests it).

| arm (approach; s = γ²σ_β) | s | 1-sample med (p90) | log-word bias | strobe med/frame | frames >2% | top-1% flux share | samples for 5% / 2% |
|---|---|---|---|---|---|---|---|
| β 0.9, σ_β 0.01 | 0.053 | 14% (34%) | −2.2% | 19% | 94% | 1.7% | 19 / 114 |
| β 0.9, σ_β 0.03 | 0.158 | 40% (86%) | −18% | 58% | 98% | 4.5% | 196 / 1,221 |
| β 0.9, σ_β 0.05 | 0.263 | 63% (121%) | −43% | 94% (2.6×) | 99% | 10.1% | 799 / 4,989 |
| β 0.99, σ_β 0.001 | 0.050 | 14% (33%) | −2.0% | 19% | 93% | 1.7% | 17 / 104 |
| β 0.99, σ_β 0.005 | 0.251 | 60% (117%) | −40% | 92% | 98% | 9.4% | 709 / 4,429 |
| β 0.99, σ_β 0.01 | 0.503 | 92% (100%) | −87% | 173% (5.7×) | 100% | **37.2%** (top 0.1%: 13.6%) | 16,788 / 104,922 |
| belt β 10⁻⁵, σ_β 10⁻⁵ | 0 | 0.0% | 0 | 0.0% | 0% | 1.0% | 1 / 1 |

Observer arm (static crowd, all members same velocity, dispersion **zero**; the player
moves): β_O 0.5, crowd ±0.05 rad at 90° from the velocity vector: one-sample 6.8% (p90
17%), strobe 9.4%/frame, 88% of frames >2%; β_O 0.9 same crowd: 12% (p90 30%) / 16%,
94%; β_O 0.9, ±0.2 rad: 49% (94%), log-word −27%, strobe 65%, top-1% share 8.7%;
centred dead ahead (θ=0) the aberration gradient vanishes: s 0.015, 3.5% (p90 7%),
strobe 2.8% — the failure is lateral, worst at 90°, gone ahead, exactly
d ln k/dθ = β sinθ/(1−β cosθ).

Colour: the sampled sprite's colour temperature is off by a median 28% (p90 48%) at
s 0.263 and 68% (p90 83%) at s 0.503 against the flux-weighted true colour
k_F = Σk⁵/Σk⁴ — the "type × log k table" draws the wrong blackbody band most frames.
Integrated totals strobe too (P independent pixel samples): median |Δ ln F| = 14%/frame
at P=100 and 4.3% at P=1000 in the s 0.263 fleet (37.9%/15.8% at s 0.503) — even the
whole-fleet brightness flickers above the 2% bar at realistic sub-resolution pixel counts.

Closed forms (CV and log-word verified ≤1%, strobe median ≈ 4s within 4% at s ≤ 0.27,
10% at s 0.50): CV(k⁴) = √(e^{16s²}−1); log-word miss factor = e^{8s²}; strobe median
≈ 4s; visibility boundary (strobe > 2%) at
s* ≈ 0.005 ⇔ **σ_β* = 0.005/γ²**: 0.7% of c at β 0.5, 0.095% at β 0.9, 0.01% at β 0.99.
Battle manoeuvre dispersions (0.01–0.05 c; the shipped fleet lattice runs closing β to
0.9) sit 10–500× above the boundary; belt conjunction speeds (10⁻⁵ c) sit far below.

Reproduce: `cd lab/results/20261018-1126-redteam-1885 && python3 falsifier.py` (3 s;
`sh regen.sh` prints the same table; full rows in results.json; fixed seeds, PCG64).

## Predictions

`predictions.md` was written before the decisive run (priors from the analytic lognormal
only). Scorecard: 9/10 held — instrument control exact (reciprocal-sign nuance noted in
the file), Newtonian ≥30× → 628×, belt-safe zeros, log-word factor 1.73 predicted vs
1.74 measured, strobe boundary s* 0.005 predicted vs measured 2.1% median at s 0.005
(51% of frames >2%), tail 10% at s 0.26 → 10.1% (35% at s 0.5 → 37.2%), observer arm
12% predicted vs 12.3% measured, cost ~700 → 799, colour ×1.3 → ×1.28. The one miss is
conservative: I predicted a 90% one-sample median at s 0.263, measured 63% (skew of the
lognormal ratio; I over-predicted the failure, under-claimed nothing).

## What would make it wrong

1. The letter means presence-only samples and the flux is *derived* from the crowd's
   program (not the sampled member). That reading is not what L58 says ("a type × log k
   table gives the sprite"), it heals only smooth programs (belts — where it is the
   design's own "derive, don't sample" and should be written as the pixel's k-moments in
   closed form), and it cannot heal real fleets: member velocities are individual states
   (principle: every body is real), the seen flux is a heavy-tailed integral over them,
   and its observer-dependence (k is a function of the observer's velocity and viewing
   angle) means no per-aggregate constant can carry it.
2. My visibility bar (2% contrast steps) is a cited assumption, not a measurement —
   human contrast sensitivity at these frequencies is ~1–3%, so the boundary s* moves at
   most ×2, and the flagship arms sit 10–500× above it either way.
3. Transverse dispersion only (no LOS component) is second order (enters via γ) — if
   fleets held zero LOS dispersion at all times the fleet arms would soften; real
   manoeuvres and the observer arm (which needs no dispersion at all) do not.

Cost of adopting the correction: a design-doc edit (strike L59/L116 as written; the
readout law becomes s-aware: closed-form k-moments for smooth programs, sampling count
∝ CV(k⁴)² or tracked moments for crowds) plus one float rung. No engine code changes
(the shipped view draws members individually at ≤ β-limited scale today; the aggregate
path is the belt/promotion tier, wired at β ≈ 0).

Fit with PRINCIPLES: principle 20 — "averages crush data especially tail events": at
γ 7 (β 0.99, σ_β 0.01), 1% of ships carry 37% of what the player sees; a one-sample
sprite draws them 1% of the time. Principle 12 (smoothness): per-frame brightness jumps
to 6× are the anti-smooth. Principle 13 (errors never compound): the strobe is a new
instrument error every frame, never averaged down inside the cap. Principle 2 (error
type over size): this is a *type* error — the representation (point k) cannot express
the quantity (a k⁴-moment of a crowd). Principle 18/19 (right representation): the
water for this fish is the moment/rapidity integral, not the point sample.

Rung that should have caught it: none exists. r6 gates per-emitter readout cost and row
presence; B18 gates the belt's storage and births at β ≈ 0 (my belt control shows why
it passes there); r7 is AI. 2fa4 (14 Oct) already noted "no gate judges a seen value"
for individual members — this run extends that to the aggregate readout with magnitudes.
Proposed cheap criterion (freeze-ready): at β_bulk 0.9, σ_β 0.03, an aggregate drawn
from N = 10⁶ members must match Σk_i⁴ within 5% at p99 over 60 frames, and its frame-to-
(must strobe ~58%/frame) and the shared-log-word readout (must sit at −18%). Add the
observer-motion arm (β_O 0.9, ±0.05 rad static crowd: must hold 2%; one-sample fails at
16%/frame).

## The lens

Premise red-team ranks by player visibility: this failure is visible in the game's two
flagship scenes (a relativistic fleet battle; the player at high γ looking at any
extended crowd) and invisible in every tested regime — the exact inversion of the
current test coverage. What the lens may have missed: the exotic-heavy attacks in my
ordered list (two-body doll below p̄ 65M, near-separatrix Binet rows) are already owned
by stronger instruments (r3, r1v2) and were left to them; and I did not price the
moment-tracking fix (an incremental Σk^p per aggregate as a function of observer state)
beyond naming it — it may be cheaper than sampling and deserves its own run.
