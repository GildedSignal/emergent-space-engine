# Dossier — H_live measured: what a belt's history costs the store

Run 20261009-1649-components-6b55 (lens: first principles, one component: the
population store's dynamic layer). Component: `crates/shipmem` Form P (program +
scars), whose missing number is the board's top-listed unmeasured risk
("Distinctions created per game-second … decide whether 10⁹ fit in 8 GB; not
measured yet"; HANDOFF "Risks to attack first"; queued as `b-h-live`).

## Claim

A billion-body belt's mutual encounters never force the store live at any
behaviour-plausible element quantum, **provided the encounter threshold ρ stays
at a physical scale**: the walk crosses Q_e = 10⁻⁷ (relative) only after ~4×10³
orbits at Kuiper mass and never crosses Q_e = 10⁻⁵ (margin 4×10³ in time) — but
the ρ ∝ 1/N regime that keeps per-body encounter compute constant destroys the
program store at any mass (every near-collision impulse, ∝ M_belt and N-invariant,
scars immediately). The element quantum carries a new, measured constraint:
Q_e ≳ 2×10⁻⁹·(M_belt/10⁻⁷ M⋆)·(10⁹/N)^½ at fixed ρ for a 10⁴-orbit session.

## Bottleneck

Bottleneck 5 on the board (10⁹ bodies in 8 GB) and the H_live risk. Expected
gain: deletes the fear that history, not the static program, decides the billion-
body budget (the static floor is 0.126 bits/body, gold components-98bc); it also
gives the encounters design a measured constraint it did not have (choice of ρ
regime vs the store) and gives B18b/the plane the H_live instrument's first
numbers.

## Evidence (commands, each < 60 s)

- `cargo run --release -p emergent-encounters -- scale n` (the repo's own
  experiment, unmodified): `enc_per_body_orbit` = 0.0412, 0.0394, 0.0396,
  0.0388, 0.0404 at N = 10³…10⁵ in the ρ∝1/N regime (σ_e = 10⁻², ρN = 10⁻⁴) —
  **measured: the per-body encounter rate is N-independent in that regime**, and
  my analytic rate formula over-counts 22× (0.86), which I use as the
  calibration factor for all model rates.
- `python3 hlive.py metrics.json` (23 s, `work/hlive.py`, numpy): per-body
  Monte-Carlo of conjunction impulses (exact 2D impulse dv = 2m/(b·v_rel),
  Gauss's equations to δa, δe; offsets accumulate exactly as integers on the Q_e
  grid, r2's lesson), belt geometry from r8 v2 (a ∈ [1,1.5], σ_e = 10⁻²,
  ρ = 10⁻⁴), N ∈ {10⁴, 10⁶, 10⁹}, M_belt ∈ {10⁻⁹…10⁻³ M⋆}, Q_e ∈ {10⁻⁹, 10⁻⁷, 10⁻⁵},
  session 10⁴ orbits. Key rows (rates 22×-corrected; τ = crossing time):

  | regime | M_belt | Q_e | σ_walk(10⁴ orbr) | τ (orbits) | live bits/body |
  |---|---|---|---|---|---|
  | fixed-ρ | 10⁻⁷ | 10⁻⁹ | 1.6×10⁻¹¹ | 4 | ~50 (degenerate) |
  | fixed-ρ | 10⁻⁷ | 10⁻⁷ | 1.6×10⁻⁹ | 4×10³ | ~10 (crosses late) |
  | fixed-ρ | 10⁻⁷ | 10⁻⁵ | 1.6×10⁻¹¹·10² | 4×10⁷ | 0 (free) |
  | ρ∝1/N | any | ≤10⁻⁵ | ≥2×10⁻⁵ | <1 | 24–64 (degenerate) |

  Mechanism (fixed ρ, per-body rate Γ ∝ N but m ∝ 1/N): σ_walk ∝ M_belt/√N —
  memory *heals* with N while per-body encounter compute grows; in ρ∝1/N both
  Γ and the per-event impulse are N-invariant, so every counted event is a
  near-collision (∼150 m at N = 10⁹) whose impulse dwarfs any quantum.
- Controls, both live: MC walk σ / analytic diffusive σ = 0.886 (window
  [0.7, 1.4]; a first run failed at 1.77 and exposed a factor-4 bug in my
  analytic σ, fixed); a heavy belt (M_belt = 10⁻³, Q = 10⁻⁹) scars 100% — the
  instrument can see the failure mode.
- Player light-cone bound (analytic, real units): a light-second cone at belt
  density holds 3.2×10³ bodies → ≤1.0×10⁵ bits/game-second at 32 bits each
  against a 4 GiB/h budget of 1.2×10⁶ bits/s (8.6%): bounded, non-zero.
- Physics sanity: extrapolated to 4×10⁹ orbits the self-encounter walk is
  ~3×10⁻² m/s, far below the real Kuiper belt's excitation (which Neptune, not
  self-encounters, owns) — consistent with known Gyr self-excitation timescales.

## Predictions (predictions.md, written before the sweep)

P2 (diffusion ratio) and P3 (heavy control) held; P4 held partially (rate
N-invariance *confirmed by the crate's own numbers*; walk σ drifted 2× across N,
from the b_min log-term cap). **P5 failed, honestly**: I predicted no crossing
at Kuiper mass, Q_e = 10⁻⁷, N = 10⁹ with margin >100; measured τ ≈ 4×10³ orbits
(fixed ρ) and ~0.2 orbits (ρ∝1/N). My hand estimate missed the log-divergent
close-encounter tail (√ln(ρ/b_min) ≈ 3) and the 1/b weighting. P6 held (the
boundary mass at Q_e = 10⁻⁷ lies at the edge of my bracket [10⁻⁵, 10⁻³]). P7 held
(0.086 of budget, predicted 5–15%). P1 partially failed: the model reproduces
belt-0's 427 encounters only within 12–122× (draw unknown); superseded by the
crate's direct measurement.

## What would make it wrong

The 22× rate calibration is measured only at N ≤ 10⁵, σ_e = 10⁻², ρN = 10⁻⁴; if
the rate's N-scaling bends beyond that, the fixed-ρ τ values move as Γ⁻¹. The
walk treats consecutive conjunctions as independent; real conjunctions are
quasi-periodic (r8's own finding), which makes successive impulses correlated —
coherent repetition can cross a quantum *faster* than diffusion (this is the
biggest unmodelled risk; it needs the plane's belt, not this Monte-Carlo). The
Gaussian session estimate assumes reabsorption keeps every sub-quantum body
folded into the program; shipmem's `seal` implements exactly that, but its
equilibrium was not measured here. Planet-driven chaos (resonant bands, Lyapunov
growth ~10⁴–10⁵ orbits) is generator-side at session scale and was only bounded
by argument, not measured.

## Cost of adoption, fit with PRINCIPLES

No code change proposed; the outputs are a measured constraint (Q_e vs M_belt
and N; the ρ-regime tension) for the encounters design, B18b and the plane's
H_live instrument. Fits "Store the generator, not the generated" (P6) — the
generator holds unless the quantum is finer than the belt's own diffusion;
"the biggest quantization we can get away with" (P16) now has a memory-side
answer; "a raindrop is an event for an ant and nothing for a lion" (P33) — at
10⁹ bodies the store must let sub-quantum flybys enter the aggregate, and the
aggregation scale must stay physical (fixed ρ), not shrink with N.

## The lens

The component lens made me measure the belt in isolation; the neighbours that
matter for the store's equilibrium are the reabsorption mechanics in
`shipmem::program` (seal/infer cadence) and the encounters skin, whose costs I
estimated but did not run. A different lens (dynamics) would have simulated
consecutive conjunctions of the same pair rather than assuming independence.
