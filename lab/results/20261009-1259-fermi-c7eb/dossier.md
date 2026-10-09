# Dossier — 20261009-1259-fermi-c7eb (Fermi lens)

## Claim

At 10⁹ bodies the binding term on the 8 GB M1 is the flat per-body tube store
(16 B × 10⁹ = 14.9 GiB, 1.9× over), not events (~2% of one core at RTF 100) or
bandwidth (a full sweep is 0.27 s, so only event-driven touches survive); and
belt encounters create **zero** canonical distinctions below a mass threshold
m_crit ≈ 8×10⁻¹⁹ M☉ (≈ a 500-m rock at q = 10⁻⁴ AU, σ_e = 0.1, a = 2.7 AU):
below it the program belt is *exact* — 0 crossed ticks, not a coarse average —
so H_live is bounded in steady play and set by consumers (the player, contacts,
fleets), not by belt self-evolution.

## Bottleneck

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per
game-second"; HANDOFF risk list: "Distinctions created per game-second (H_live)
… **not measured yet**". Gain: deletes one whole failure mode of the 10⁹ target
(belt self-evolution individualizing the population into tubes) and redirects
memory work to a representation choice — *which bodies carry tubes* — where the
already-specced population programs (crates/shipmem, currently a deletion
candidate in method.md) turn a 1.9× break into a ~545× margin.

## Evidence

Machine: shared Linux x86, 8 vCPU, load ~2.5, 15 GB. Counts and arithmetic
only — no timing claims beyond orders of magnitude. All commands ≤ 60 s.

1. **Measured** (repo's own belts, `crates/encounters`, saved in
   `verify-a/b/d.jsonl`): truth-encounter rate per body per orbit, 8 belts:
   1.75×10⁻⁴ (quiet: ρ=10⁻⁴, σ_e=10⁻³) → 7.0×10⁻² (hot: ρ=10⁻³, σ_e=0.1);
   rises with ρ and σ_e as expected. Reproduce:
   `cargo run --release -p emergent-encounters --bin encounters -- verify a` (18 s),
   `verify b`, `verify d` (34 s each).
2. **The law's quantum** (kepler.rs: period in ticks, 2³² per time unit):
   one period tick = Δa = 1.5×10⁻¹¹ AU at a = 2.7. A distinction on the law's
   grid = ≥1 crossed tick in P, tp, e or ϖ.
3. **Per-encounter deflection vs that grid** (`analysis.py`, `analysis-out.txt`,
   <1 s; analytic hyperbolic two-body, G=M☉=1 units): ship (10⁶ t) and 50-m
   rock: Δa ≈ 10⁻¹⁴ AU ≈ 10⁻³ ticks — **no crossing, exactly zero bits**;
   500-m rock: 0.9 ticks (the threshold); 5-km rock: 851 ticks; Ceres:
   1.2×10⁹ ticks (Δa = 0.018 AU, player-visible at once). m_crit follows from
   μ/(qv²) — the same dimensionless number m-meso-motion already uses.
4. **Game-density belt (3D estimate, N=10⁹, width 1.5 AU, σ_e=σ_i=0.1,
   ρ=10⁻⁴ AU):** ~2.8 encounters/body/orbit → ~20 exact pair events/s at 1×,
   ~2×10³/s at RTF 100 ≈ 2% of one core at an assumed 10 µs/event. Secular
   distinct kicks (H0190's 0.3/orbit) → ~2 recompiles/s at 1×. Individualization
   at tick resolution takes <10 orbits **but only for m > m_crit participants**.
5. **Consumer resolution:** 50-m-rock encounter noise needs ~10²¹ orbits to move
   a body one 10⁻³-rad pixel — the program belt is an attractor at what the
   player can differentiate, by ~20 orders.

## Predictions (`predictions.md`, written before any run)

- P1 (rate 10⁻³–10⁻²/body/orbit, rising with ρ, σ_e): **half-held.** Direction
  and order right; spread underestimated (measured 1.75×10⁻⁴ … 7×10⁻²).
- P2 (encounters cross <1% of ticks even at Ceres mass): **split.** Ships and
  <500-m rocks: stronger than predicted (zero ticks, 10³× below grid). ≥5-km
  rocks and Ceres: opposite — *every* encounter crosses (10³–10⁹ ticks). The
  truth is a threshold, not a fraction.
- P3 (storage binding, events far under): **held for storage** (14.9 GiB vs
  8 GiB, 1.9×); events are ~50× under one core, not the 10⁴× I predicted —
  comfortable, and my margin was 200× optimistic.
- P4 (observation-bounded identity, 10⁵–10⁶ bits/s): not measured this run;
  stays an estimate.

## What would make it wrong

- **Co-orbital formations:** m_crit ∝ q·v²; at formation v_rel (~10⁻⁵) instead
  of dispersion (~6×10⁻²), the threshold drops ~10⁷ — *ships in fleets do
  individualize*. This matches gold 20261006-0346 (co-orbital concentration
  breaks the pairwise tier): fleets are deliberate, player-made distinctions,
  and the exception is already a designed tier.
- Zoom: "the zoom level is the minimap" — a player resolved into a fleet sees
  finer than 10⁻³ rad; observed bodies must carry consumer-resolution identity.
- The 3D density rate and the 10 µs/event cost are estimates; the mass
  threshold itself is per-encounter and density-independent (robust).
- The 0.126-bit program price is for a smooth belt (components-98bc); resonant
  structure (Kirkwood gaps) raises the program's cost — unmeasured.

Cost of adopting: none — it is a decision input, not code. The design change it
names (tubes only for m > m_crit / active / observed bodies; programs for the
rest; identity charged to consumer light cones) is the population-program path
already specced (plane.md foundation 6), and it argues *against* deleting
`crates/shipmem` before the plane's belt is wired to it.

Fit with PRINCIPLES: "this is nowhere near the floor on the size and
information theory says so" (24); "the floor is what the player can
differentiate" (register, bottleneck 0); "Compute only surprises" (3);
"redshift and co are not derived but emergent" — the belt's exactness below
m_crit is the same doctrine: nothing is stored that no consumer can distinguish.

## The lens

Fermi arithmetic trusted analytic hyperbolic deflections where the crate could
have given me the real per-encounter distance distribution (truth encounters
carry d; I did not dump it — a 2× tighter m_crit would not change any
conclusion). Both estimate terms (3D density, event cost) are mine, not the
repo's; the repo belts are 2D toys at toy density, and I stretched them to 3D by
hand. No seed variation on the deflection math (it is per-encounter analytic,
not simulated).
