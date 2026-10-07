# Dossier — 20261007-0528-fermi-aab3 (Fermi lens)

## Claim

At 10⁹ bodies the 8 GB promise is decided by the *individualized fraction* f_ind (bodies
forced out of programs into 16-byte tubes — resonance capture and identity policy), not by
the encounter stream: every measured H_live term is 3–8 orders below the floor, and the
gate is f_ind ≤ 0.375 of the population at 6 GB usable (≲ 0.2 with engine tenants); today's
unmeasured quantity to gate is therefore f_ind, and the design answer if it threatens the
budget is a libration/resonance *program*, not per-body tubes.

## Bottleneck

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" and the
handoff risk "H_live: not measured yet". This run supplies the missing orders of magnitude
so the B18b/shipmem builds gate a number instead of a fear. It also independently
re-derives r8 v2's belt-0 encounter count (claim check) and the kick-cadence arithmetic
behind "190 cores".

## Evidence

All numbers regenerate in < 1 s: `cd lab/results/20261007-0528-fermi-aab3 && python3 hlive.py`
(numpy 1.26, exact 2-body conjunction geometry — belt-0's own generator shape from
`crates/encounters/src/belt.rs`: a ∈ [1,1.5], Rayleigh σ_e = 0.01, coplanar; closest
approach from exact Kepler velocities at a random-conjunction angle; 2×10⁶ pairs).

1. **r8 v2 claim check (427 encounters / 20 orbits, 1.7M candidate pairs).** My independent
   rate curve enc(ρ) at σ_e = 0.01 jointly fits both numbers at N ≈ 4250, ρ ≈ 1e-5
   (candidates 1.1M, −34%; encounters 444, +4%). At the N = 10⁴ I first assumed, the match
   needs ρ ≈ 2×10⁻⁶. Reproduced within a factor 2 — no 10× disagreement anywhere.
2. **Mutual encounters of ship/rock-mass bodies create ~0 bits.** Measured impulse
   δv/v = 2μm/(b·v²): ship 10⁶ kg → ≤ 10⁻¹⁷; rock 10¹² kg → ≤ 10⁻¹¹; even 10¹⁵ kg at a
   15 km miss → 10⁻⁸. Below any program quantum (10⁻⁶): bits/encounter = 0. Encounter
   *memory* is a non-problem; encounter *candidate work* stays the board's top compute risk.
3. **What does create bits: embryos/planets.** 10²² kg at b = 10⁻⁴ AU: δv/v ≈ 10⁻⁴ →
   ~6.7 bits (q = 10⁻⁶); at 1.5×10⁵ km (b_bits = 2μ/q): ≥1-bit kicks. With 10³ embryos
   among 10⁹ (spread at belt-0 density): 4 bit-kicks/rock/orbit → **creation ≈ 3.8×10²
   bits/s game-time**; strong scatter (δv/v > 10⁻³) materializes tubes at 0.39/s →
   0.6 MB per 10⁵ game-s; full materialization of the whole belt would take ~80 game-years.
   Battles: bounded by participants — a 10⁶-ship fleet fully individualized = 16 MB.
   Player: ~10³ bits/s. Program floor: 0.126 bits/body (gold components-98bc) = 16 MB at 10⁹.
4. **Optical depth: 10⁹ cannot sit in ONE belt-0 annulus.** Same volume, N × 10⁵ density:
   10²–10³ encounters per body per orbit (measured curve × N²). That kills it on candidate
   work, not memory. The 10⁹ must spread over dolls/bands at fixed local density (then
   belt-wide rates scale ∝ N, and items 1–3 apply per doll).
5. **Kick cadence arithmetic (claim check on "190 cores").** At 10⁹ bodies, a = 1 AU
   (orbit = 3.16×10⁷ game-s), rtf 100: today's ~500 steps/orbit costs 1.6×10⁶ step-events
   per real second — fits the M1 only at ≤ 10³ ops/step; the averaged law (0.3 kicks/orbit,
   H0190) costs 950 events/s real — 1700× less, i.e. averaging is existential at 10⁹, not
   an optimization. The 190-core figure corresponds to ~10⁵–10⁶ ops/event at fixed-step
   cadence: consistent, and the swing variable is ops/event, not cadence.

## Predictions (predictions.md, written before the run)

- P1 (belt-0 count within ×3 for ρ ∈ [1e-5, 3e-5]): **held** with N free (joint fit
  N ≈ 4250, ρ = 1e-5, +4% on encounters); at fixed N = 10⁴ the matching ρ is 2×10⁻⁶,
  5× below my predicted band — the prediction was right only because N was free.
- P2 (ship/rock impulse ≤ 10⁻⁶ v): **held, strongly** (≤ 10⁻¹⁰ v).
- P3 (embryo 5–40 bits/encounter): **held** (6.7–12 bits; 1-rad drift clock 200–6600 orbits).
- P4 (10⁹ in one annulus ≥ 0.1 encounters/body/orbit): **held** — 10²–10³, i.e. off by
  orders in the direction predicted (doll layering forced).
- P5: peacetime creation 10⁰–10² bits/s: **just missed high** — 3.8×10² bits/s with the
  10³-embryo assumption (0 without embryos). The f_ind threshold I wrote ("5% → 8 GB")
  was a bit/byte slip: 5% × 10⁹ × 16 B = 0.8 GB, fine; the true gate is f_ind ≤ 0.375.

## What would make it wrong

- A population whose distinguishing kicks are much larger than embryo-scale at much higher
  rates (e.g. game-engineered dense rubble swarms around planets: higher n, real σ).
- f_ind measurements: if B18b-class belt runs show resonance capture or identity policy
  individualizing ≳ 20% of a 10⁹ population, the 8 GB budget closes only with resonant
  programs or a doll restructure.
- My straight-line-pass and coplanar-2D geometry miss inclined 3D belts' encounter rates by
  ~×2–3 (stated systematic; not near any decision threshold).
- Adoption cost: ~zero (no engine change) — this is a gate design and a priority call:
  instrument f_ind and bits/scar in shipmem/belt runs; do not spend on encounter-memory.

## Fit with PRINCIPLES

- "The memory floor is information-theoretic" — the run puts numbers on the floor:
  program 0.126 bits/body + ~0 from smooth-belt dynamics; only identity/resonance pays.
- "Compute only surprises" — measured: smooth-belt encounters carry no surprise bits at
  ship/rock mass; the surprise is concentrated where averaging fails (resonance), exactly
  where the board already knows the law needs phase feedback.
- "Baby Spartans start small": one 0.4 s script + held-out predictions, aimed at a named
  unmeasured risk before the B18b builds pay for measurement.

## The lens (what Fermi may have missed)

Estimates favor point masses and game-free physics: no inclinations, no dissipative
contacts, no migration epochs (which can capture large fractions into resonance
temporarily), a=1↔1 AU scale assumption, bits-per-crossing set to 3 by hand, and creation
measured rather than steady state (materialized tubes are bounded only by the 80-game-year
horizon if nothing reabsorbs). The checker should attack with an inclined, embryo-rich, or
post-migration belt.
