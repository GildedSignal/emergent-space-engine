# Dossier — 20261008-0945-spacex-5964 (lens: SpaceX)

**Claim.** H_live for populations is decided by which grid the scar lives on, not by body
count: on certificate-grade quanta (ρ/a) a belt of 10⁹ creates 0.09–1.15 scar bits per body
per 100 orbits (0.01–0.16 GB, 40–600× inside the 8 GB budget), while on the doll's 32-bit
(E,L) memo-key grid the same physics creates 12.9–17.2 bits/body (1.6–2.1 GB — 25–33% of the
whole 64-bit/body budget, before tubes, catalogues or events), and ship-mass fleets create
exactly 0 scar bits from their own gravity; therefore the scar's quantum must be the
population's own grid, decoupled from the memo key.

**Bottleneck.** The board's unmeasured risk "distinctions created per game-second (H_live)
decide whether 10⁹ fit in 8 GB — not measured yet" (5 October, outside review). Measured
here at orders of magnitude. Expected gain: keeps the memory question a representation
choice (scar grid) instead of a scaling fight; deletes nothing yet, but pre-empts a 10–100×
memory overpay if scars were stored on the doll grid (the idiot index of that choice:
13–17 bits stored for information the certificates read only to ρ).

**Evidence** (all commands from `lab/results/20261008-0945-spacex-5964/`, each ≤ 160 s,
Python 3 + numpy 1.26):

- `python3 h_live_probe.py validate` → direct time-stepped belt (no conjunction logic,
  N=1500, r8 v2 belt-0 geometry, 8 orbits): **1.25×10⁻³ encounters/body/orbit**, against
  r8 v2's truth anchor ≈2.1×10⁻³ (427 encounters, 10⁴ bodies, 20 orbits; its ρ is drawn in
  [10⁻⁵,3×10⁻⁴]). Geometry model sound within ρ uncertainty.
- `python3 h_live_probe.py main` → conjunction Monte-Carlo, 5 scenes, 100 orbits each;
  `python3 summarize.py` → the table below. My MC overestimates the direct rate by
  4.2× (5.24 vs 1.25×10⁻³; it samples radial alignment without requiring azimuthal
  conjunction) — all MC rates below are reported with that measured ÷4.2 correction;
  the direction is conservative (overestimates H_live).

| scene (N, ρ, σ_e, μ) | enc/body/orbit (corr.) | cert bits/body@100orb (touched) | doll bits/body@100orb | 10⁹: cert / doll |
|---|---|---|---|---|
| belt0_r8 (10⁴, 1e-4, 1e-2, 1e-10) | 1.25e-3 | 1.15 (28%) | 12.9 | 0.14 GB / 1.61 GB |
| belt0_rho3e-4 (10⁴, 3e-4, 1e-2, 1e-10) | 3.6e-3 | 0.089 (2.5%) | 17.2 | 0.011 GB / 2.15 GB |
| belt_hot (10⁴, 1e-4, 1e-1, 1e-10) | 7.9e-3 | 0.22 (6.5%) | 17.2 | 0.028 GB / 2.15 GB |
| belt_shipmass (10⁴, 1e-4, 1e-2, 5e-25) | 1.2e-3 | **0.000** (0%) | **0.000** | 0 / 0 |
| fleet_tight (2×10⁵ on one orbit, ρ=1e-4) | ≤1.2e-3 | kick Δa/a 4.5×10⁻¹³ → **0 quanta** | — | 0 |

- Kicks: asteroid-mass bodies take Δa/a ~10⁻⁴–10⁻³ per encounter (r8 v4's kick scale
  confirmed); ship-mass bodies take ~10⁻¹⁸–10⁻²¹ — sub-quantum on both grids (principle 6
  accumulation needs ~10⁸ encounters to land one cert quantum: never in a session).
- Creation rate at 10⁹, rtf 100 (1 AU orbit = 87.7 game-h): 0.13–1.6 MB/game-hour on the
  cert grid; 18–25 MB/game-hour on the doll grid. Refit every 10 orbits (centre chosen by
  exact stored bits, as the design chooses program-vs-packed form) holds the collective
  walk; the individual walk grows ~linearly until every body is touched, then only as
  Elias(√n) ≈ ½·log.
- Fleet proximity: 99.8% of a tight formation's bodies always have a neighbour within ρ
  (the co-orbital gold's regime — dense order, certificate-driven, not scar-driven).
- Known artifact, reported: the doll-grid "touched" prints 100% where event coverage is
  ~65%; the bit-minimising program-centre shift marks untouched bodies too (a real cost of
  a moving reference, but the no-refit bound is ≤2× the reported bits; the cert-vs-doll
  conclusion, 10–100×, is unaffected either way).

**Predictions** (`predictions.md`, written before the decisive run): P1 held after the
measured 4.2× MC correction (corrected 1.25×10⁻³ in the predicted 0.5–5×10⁻³ band, 1.7× from
r8's anchor). P2 held exactly (ship-mass = 0 bits on both grids; the negative control
returned exactly zero). P3 held on cert (≤8 bits predicted, measured ≤1.15); the doll-grid
magnitude was 2× below my ≥36-bit prediction (refit plus kick-spread effects) but the
conclusion stands (25–33% of the entire budget). P4 held (0 contacts; (R_c/ρ)² ≈ 5×10⁻¹¹).
P5 half-held: refits hold the centre, the spread walks until saturation (½·log). P6 missed
on the anchor scene by 1.6× (1.64 MB/game-h predicted ≤1): belt0_r8 is the harsh end of the
ρ–mass–dispersion cube, not the median scene.

**What would make it wrong.** (1) The engine's kick layer is orbit-averaged (law.md,
"kicks are orbit-averaged on stable orbits"): many small kicks instead of rare
impulse-at-conjunction ones change bits/orbit (fewer quanta-crossings per unit stirring)
but not the grid conclusion, which depends only on kick size ÷ quantum. (2) The v_rel model
is first order in e; the 4.2× MC-vs-direct gap shows the rate is geometry-sensitive — the
absolute creation rates carry that factor. (3) Contacts at ρ → ship size (the tight-fleet
dense order) are a different channel, unmeasured here. (4) If shipmem's packed-blocks form
cannot parameterise its scar exponent per population, the delta is not one step.

**Cost of adopting.** Small and local: shipmem's scar layer takes its fixed-point exponent
from the population (certificate grade), while the memo key stays the doll's 32-bit grid;
per law.md's own rule ("per band, fixed point with one shared exponent") this extends an
existing rule to the scar layer. No gate is touched; B18's information floor must be
measured on the scarred state (program 0.126 bits + scars ≈ scars at 100 orbits), not on
the birth program.

**Fit with PRINCIPLES.** "The memory floor is information-theoretic" (P24) — the doll grid
stores bits no reader resolves; "a fix signals the wrong representation" (P19) — the 10–100×
is removed by changing the scar's grid, not by compressing harder; "compute only surprises"
(P3) — the fleet's zero confirms a program-born formation creates no distinctions until
something interacts with it.

**The lens.** SpaceX's delete-first pushed this toward "which stored bits have no reader"
(the idiot index) and it found the scar-grid overpay; what the lens may have missed is the
via-negativa half: what *removes* distinctions (population re-binning, when a walking body
crosses into the next population) was only bounded, not measured — that is the named next
experiment, and it is where the steady state is actually decided.
