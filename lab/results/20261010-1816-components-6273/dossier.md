# Dossier — H_live measured: the stirred belt's scar store, its floor and its idiot index

## Claim

The belt body store's live cost is not 157 bits/body but **rate × kernel**: at the law's
own 1-tick grid, mutual encounters below a measured crossover mass (μ_b ≈ 1.7×10⁻¹⁸ of the
star, a ~1 km rock) create **zero** distinctions — a ship belt stays a 0.126-bit program
forever — and above it each encounter costs 1.4–38 bits, so a 10⁹-body stirred belt costs
0.3–3.2 GB after 100 orbits with a measured dual rule (append scars while young, rebind
into genesis-anchored offsets when hit again), against 19.6 GB naive.

## Bottleneck

Board risk "distinctions created per game-second (H_live): not measured yet" (HANDOFF,
Risks; the outside review: this, not the body count, decides whether 10⁹ fit in 8 GB).
This run measures it and gives the store design that sits on the measured entropy. It
deletes the per-body element array from the belt design (the naive 157-bit store), the
same way the genesis program already deleted it for unstirred belts.

## Component (lens steps)

1. **Requirement.** P6 "Store the generator, not the generated"; P24 "The memory floor is
   information" / "why do you need so many bytes per entity?"; standing decision "every
   body real, never averaged". The store must regenerate every body exactly from program +
   distinctions.
2. **Floor.** Genesis: 0.126 bits/body (gold components-98bc, cited). Distinctions: the
   entropy of the quantized kick increments on the law's integer grid (period/periapsis in
   ticks of 2⁻³² time units; e, angle at 2²⁴ fractional bits). Measured order-0 kernel
   1.4–38 bits per marking encounter; the conditional floor (given encounter distance d)
   is 0.6–2.0 bits lower per event.
3. **Idiot index.** Naive quantized store 157 bits/body (19.6 GB per 10⁹) vs measured
   2.4 bits/body at μ_b=10⁻¹⁸: **65×**; vs a ship-mass belt: **∞** (0 bits needed). The
   naive store does not fit the machine at any stir level; the measured one fits until the
   horizon × kernel exceeds 64 bits/body.
4. **Design within 10× of the floor (built, `hlive.rs`).** Program + dual scar store:
   append quantized increments coded at their empirical entropy while a body is sparsely
   hit; when cumulative scar bits exceed the entropy of its final genesis-anchored offset,
   rebind it (recode the offset once). The code implements exactly this min() and both
   sides are measured, so the store runs at the measured order-0 entropy, within the
   0.6–2.0 bits/event of the conditional floor.


## Evidence

All commands run from the repo root, each well under 60 s (machine: GitHub Actions
Linux, 8 vCPU, load 4.0, 15 GB, 13 GB available; Linux/x86 — orders of magnitude only):

```
cargo build --release -p emergent-encounters --example hlive --offline
cargo run --release -p emergent-encounters --example hlive -- scan 2000 1e-2 1e-3 1.0 1.5 100.0 20261010   # main-sweep.jsonl
cargo run --release -p emergent-encounters --example hlive -- scan 2000 1e-2 1e-3 1.0 1.5 100.0 31        # heldout-seed31.jsonl
cargo run --release -p emergent-encounters --example hlive -- scan 300 3e-4 1e-3 1.0 1.0001 50.0 31       # heldout-coorbital.jsonl
cargo run --release -p emergent-encounters --example hlive -- scan 400 0.025 3e-3 1.0 1.0025 20.0 31      # heldout-narrow.jsonl
cargo run --release -p emergent-encounters --example hlive -- feedback 2000 1e-2 1e-3 1.0 1.5 100.0 20261010  # feedback.jsonl
```

Method: every encounter of the belt through the crate's verified cone candidates + exact
per-pair checks (r8 v3 machinery, untouched); mutual impulse kicks applied in time order
(perturbative everywhere here: the largest total period change over 100 orbits is
ΔP/P = 1.2×10⁻³ at the strongest mass 10⁻¹², 1.2×10⁻⁹ at 10⁻¹⁸ — so Δv/v ≲ 6×10⁻⁴ and
the impulse approximation's error is second order);
elements refit on the law's integer grid (the crate's own `Body::new`, period and
periapsis rounded to ticks). Scars are the quantized increments; bits are the increments'
measured order-0 entropy, first-distinction address included. The frozen-geometry
protocol (encounters detected once, kicks applied offline) was validated by the feedback
run: 1222 events frozen vs 1222 fed back at μ_b=10⁻¹⁸, 1222 vs 1215 (−0.6%) at 10⁻¹².

Main belt (n=2000, σ_e=10⁻², ρ=10⁻³, a∈[1,1.5], 100 orbits; 1222 events; rate
6.1×10⁻³ events/body/orbit), store bits per belt body after 100 orbits, per 10⁹ bodies:

| μ_b (star=1) | marks/encounter | kernel bits | scar store | rebind (genesis-anchored) | GB per 10⁹ |
|---|---|---|---|---|---|
| ≤10⁻²² | 0.000 | — | **0 bits** | — | 0.016 (program only) |
| 10⁻¹⁹ | 0.041 | 0.51 | 0.42 b | 0.43 b | 0.05 |
| 10⁻¹⁸ | 0.291 | 1.52 | 2.4 b | 2.2 b | **0.30** |
| 10⁻¹⁶ | 1.000 | 12.8 | 16.8 b | 12.0 b | **1.5** |
| 10⁻¹⁴ | 1.000 | 25.3 | 31.0 b | 19.5 b | 2.4 |
| 10⁻¹² | 1.000 | 37.5 | 45.8 b | 25.9 b | **3.2** |

- Crossover (50% of encounters mark): μ_b ≈ 1.7×10⁻¹⁸ M_star ≈ 3×10¹² kg ≈ a 1 km rock.
  Ships (≤10⁹ kg) are 300× below it: their mutual encounters never leave the program —
  only burns (the player, P5) distinguish them.
- Field structure: at μ_b ≤ 10⁻¹⁶ over 96% of kernel bits are period+periapsis ticks; e
  and angle quanta idle (P4). Halving their grid 2²⁴→2¹⁶ changes total bits <1% at 10⁻¹⁸,
  33% at 10⁻¹².
- Conditional floor: H(ΔP | distance bin) is 0.6–2.0 bits below H(ΔP) for μ_b ≥ 10⁻¹⁴.
- Rebind wins where the same bodies are re-hit: coorbital belt 4.7× cheaper than the
  append-only log (5.3 vs 25.0 bits/body); wide belt 1.8× at 10⁻¹²; below 10⁻¹⁸ they tie.
- Rates are belt-shaped, not universal: wide 6.1×10⁻³, coorbital (n=300) 1.9×10⁻², narrow
  hot belt (n=400, ρ=3×10⁻³) 5.7×10⁻² events/body/orbit. **Rate scales as density × ρ**:
  H_live(scene) = rate × kernel, both now measurable per scene; the b-h-live dashboard
  build can consume this kernel directly.

## Predictions (predictions.md, written before the run)

- P1 crossover ∈ [10⁻²¹, 10⁻¹⁹]: **missed** — actual ≈ 1.7×10⁻¹⁸. My Fermi anchor took
  shear-dominated encounter speeds (U~10⁻³); the belts are eccentricity-dominated
  (U~σ_e~10⁻²), weakening kicks ~10×. Confirmed by the held-out belts: crossover moves up
  with σ_e (narrow belt: 0.015 marks at 10⁻¹⁸) and down with it (coorbital: 0.385 at
  3×10⁻²¹).
- P2 bits/body at 10⁻¹⁸ ∈ [8, 80]: **missed low** — 2.4 (rate and mark-fraction both below
  my guess). Good for the machine, wrong for the prediction.
- P3 coorbital rate 5–50× the wide belt: **missed** — 3.1× (the named pair); the narrow
  hot belt, 9.3×, does fall in the window.
- P4 period+periapsis carry >70% below 10⁻¹⁶: **held** (>96%).
- P5 controls: **held** — μ_b=0 (and all ship-class masses) mark exactly 0 bodies; the
  unquantized accounting would mark every encounter (the mark-fraction column is that
  lever measured: 0.29 vs 1.0 at 10⁻¹⁸, ~100× in bits).
- P6 conditioning on d saves ≥1 bit: **held at μ_b ≥ 10⁻¹⁴** (1.4–2.0 bits), marginal at
  10⁻¹⁶ (0.6).

## What would make it wrong

- Contact-dominated encounters (ρ = physical radius, docking, collisions) replace the
  gravitational kernel with a different delta distribution; the crossover mass and kernel
  bits must be re-measured for that channel.
- A planetary perturber stirring the belt (secular tides, the J2/planet term) creates
  distinctions through a channel this run did not measure — for real asteroid-belt scenes
  it plausibly dominates mutual encounters. The lens's own blind-spot warning: I measured
  the encounter channel; the field channel is the neighbour to measure next.
- Belts with a mass function integrate this kernel over N(m) dm; a few km-scale stirrers
  mark everything they pass, so the *stirrer mass function*, not the body count, sets
  H_live.
- Order-0 coding is an upper bound on cost; true sequence correlations (re-encounters on
  quasi-periodic Diophantine returns) can push the floor lower. My numbers are therefore
  a floor-adjacent ceiling, not the floor itself.

## Cost of adoption, fit with PRINCIPLES

The design lands in `shipmem` (currently a deletion candidate because unused): the belt
store becomes program + dual-mode scars, ~200 lines, no engine change; the kernel table
above parameterizes the 8 GB decision per scene. P16 ("what's the biggest quantization we
can get away with?") is the lever the crossover measures; P5 ("the player is the only
wildcard") is confirmed for ship-mass belts; P6 and P24 own the whole framing; P2
("'exact' means deterministic and reproducible") is why only integer increments are
stored. Cloud timings: Linux/x86, orders of magnitude only.

## The lens (what it may have missed)

One component, one channel: the same encounters also drive candidate re-certification
(compute, the b-encounter-skin build's budget); a store that kept Diophantine certificates
to cut compute would add memory — the memory/compute trade across this boundary is
unmeasured here. Also single-star, coplanar, one doll; no player burns were injected
(the player channel is trivially unbounded and belongs to the plane).
