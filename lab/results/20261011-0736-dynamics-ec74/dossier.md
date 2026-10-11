# Dossier — 20261011-0736-dynamics-ec74 (dynamics lens)

## Claim

The impulsive-conjunction encounter representation has a **measured domain rule** —
it is valid only for passages inside the Hill sphere (b ≲ 3·r_H, where toy/RK4
agree within 8–42% at χ ≤ 0.31; outside, shear-shielding makes free-space
Rutherford 2–5× wrong) — and on the swarm-coupling axis Ψ = μ_g/(aσ_e)³ a
mutual-scattering swarm shows three regimes: a **gas** (Poisson events, λ ∝
Ψ^0.95, no stirring runaway), a **birth-burst/capture** regime (event load 18×
above steady state at birth, Fano 177→2186 growing ~ w^1.1 — avalanche scaling),
and a **clump** regime beyond the representation. Real game swarms (ships,
asteroid belts) sit far inside the gas regime at Ψ ≲ 10⁻⁶, where mutual
gravitational encounters are deletable.

## Bottleneck

Board item "candidate work at scale / work must track real encounters" and the
smoothness risk (p99 frames). The Ψ axis decides *whether* the pairwise
encounter tier (crates/encounters, the Binet cone) is needed at all for a given
swarm, and what load statistics it faces where it is needed. Expected gain:
deletion of the candidate tier for entire swarm classes (principle 1, the best
part is no part); a load model (Poisson vs avalanche) for the allocator.

## Evidence

All commands from `lab/results/20261011-0736-dynamics-ec74/work/`, each ≤ 60 s,
deterministic seeds, 8-vCPU Linux runner (orders of magnitude only):

- `python3 sweep_final.py` (≈ 60 s) — controls + sweep, N=300, ring width
  0.04, Rayleigh σ_e0 = 0.04, 100 orbits, 128 samples/orbit, K=6 angle
  neighbours, equal masses, one star (GM=1):
  - **Control (b):** impulse counts **converge with sampling in the gas
    regime** — 263 (S=128) vs 267 (S=256) at Ψ=3e-6 — but **do not converge
    in the burst regime**: 1242 vs 10612 at Ψ=3e-4 (8.5×), because slow
    near-capture passages wobble through ρ·v = 0 once per radial oscillation
    and the count grows with the sample rate. All Ψ=3e-4 magnitudes below are
    therefore **existence findings, not measurements**; the Ψ ≤ 3e-5 numbers
    stand.
  - **Ψ=3e-6:** λ_strong (χ≥0.3) = 6.7e-5/body/orbit (2 events in 300 bodies
    × 100 orbits — statistics of two); Fano 0.98/0.92/0.67 at
    windows 1/4/16 (Poisson); σ_e flat (0.05647→0.05660); σ_a 0.0119→0.0127.
  - **Ψ=3e-5:** λ = 6.0e-4; Fano 1.16/1.5/1.33; σ_e flat; λ falls 8.0e-4→3.3e-4.
  - **Ψ=3e-4 (burst regime, existence only):** λ ≈ 0.35/orbit/body, with
    **λ_early ≈ 0.93 → λ_late ≈ 0.051** (an 18× birth burst, then
    self-regulation); Fano 177/655/2186 (≈ w^1.1, avalanche scaling); χ
    median π (95% of events χ>1 — at the toy's validity edge); σ_a
    0.0119→0.0329 (viscous spreading scrambles the birth a-lattice 2.8×);
    σ_e 0.0565→0.0623 (no runaway). Magnitudes detector-inflated (see
    control (b)); the regime's existence, its birth burst, and its
    self-regulation are the findings.
  - λ(Ψ) over the converged gas regime: 6.7e-5 → 6.0e-4 per decade ⇒ **α ≈ 0.95**.
- Single-encounter RK4 control (star + mutual gravity, 3000 sub-steps per
  passage): inside r_H (b/r_H = 0.25–1, χ ≤ 0.31) toy/RK4 element-change
  ratios 1.08–1.42; outside (b/r_H = 5–50) ratios 1.8–5.5 — shear-shielding.
  Kepler round-trip (state→elements→state): exact to 1e-14.

**Voided configuration, kept honest:** the first sweep (`driver.py`,
`summary.json`) was killed by its own controls — non-convergent event counts
(S=256 found 4× S=128) from near-zero-relative-velocity conjunctions. Those
numbers are void; the detector was fixed (each unordered pair once; capture
floor u > 0.2σ_e, captures counted not applied) and re-measured above. A
configuration was killed, not the method (principle 9).

## Predictions (pre-registered in predictions.md; outcome)

- **P1 (T_L·λ ∈ [0.3,3], exponential divergence): MISS.** Twins (all M₀
  perturbed by 1e-9) showed no divergence above 3e-8 in 200 orbits even at
  λ~1/orbit ⇒ T_L·λ ≳ 60. Caveat: measured in the voided-detector sweep; and
  the window may simply be too short for the amplification chain. If it
  stands, it is good news: encounter caches stay valid for tens of encounter
  times.
- **P2 (self-regulation, no σ_e runaway; burst at the invalid corner): HELD.**
  λ(t) fell everywhere (0.56×, 0.42×, 0.055× of initial); σ_e never exceeded
  1.10×σ_e0; the ring spreads secularly (σ_a up to 2.8×) — the drain.
- **P3 (Fano ≤ 5, flat in window): HELD in the gas regime** (0.67–1.5);
  **REFUTED in the capture regime** (177→2186, avalanche scaling) — but that
  regime sits at the toy's validity edge, so it is a flag for a dedicated
  rung, not a measured constant.
- **P4 (validity guard): HELD at Ψ ≤ 3e-5** (χ median 0.36–0.62; frac χ>1 =
  0 and 0.33); **REFUTED at Ψ=3e-4** (95% χ>1) — which is exactly what the
  guard was for: the burst regime marks the boundary, between Ψ=3e-5 and 3e-4
  at filling 0.12.
- **P5 (λ ∝ Ψ^0.8–1.3): HELD** (α = 0.95). Deletability threshold: MISS by
  ~10² — drift at Ψ=3e-6 is 1.4e-6/orbit (from 2 strong events in
  300 bodies × 100 orbits — statistics of two, honestly), not < 1e-8.

## What would make it wrong

The toy is 2D, equal-mass, one star, no planet (no secular/resonant chaos
source), impulse-per-conjunction, and the capture regime (u → 0, χ → π) is
counted, not modelled — the burst statistics there are the weakest number.
The Fermi mapping of real swarms onto Ψ uses my mass/scale assumptions
(ships ~10⁻²⁴ M★ in σ_e~10⁻⁶ formations; belt bodies ~10⁻¹² M★ at σ_e~0.1),
not engine constants. If ship formations are colder than 10⁻⁶ in σ_e, Ψ_ship
rises toward the burst regime (Ψ ∝ σ_e⁻³) — the fleet case must be checked
against the formation's real σ_e before deleting anything.

Cost of adoption: cheap — a rule (b < 3r_H gate on the per-pair exact check;
a Ψ-threshold enrolment rule for the candidate tier) plus one number class
(load model: Poisson in the gas regime). Fit with PRINCIPLES: "Compute only
surprises… Nothing is evolved that can be derived when looked at" (3);
"regimes are chosen by dimensionless numbers" (4); "A fix signals the wrong
representation" (19) — the shear-shielded passages belong to the averaged
kick layer, not the encounter tier; "A failed experiment kills that
configuration, never the method" (9).

## The lens

The dynamics lens looked for attractors and got one clean negative-feedback
loop (λ self-regulates as the ring spreads) and one avalanche flag. It may
have missed: the secular/resonant channel (a planet would pump σ_e without
encounters, moving every swarm rightward on the Ψ axis — my swarms have no
planet, so my gas regime is a lower bound on stirring); and the memory
consequence (σ_a spreading scrambles the birth program — an H_live-style
scar-growth rate I measured as σ_a(t) but did not convert to bits, since the
engine's quanta are not frozen). The named next experiment: a shearing-sheet
rung (local integration through the capture regime) to measure the burst
load's true statistics and the twin-divergence horizon with a converged
detector — one rung from gold.
