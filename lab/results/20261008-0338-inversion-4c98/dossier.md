# Dossier — inverting the co-orbital phase-neighbour certificate

**Claim.** The co-orbital gold's "every real encounter lies within partner rank 4 along the orbit" is a
certificate of near-identical mean motion, not of concentration: it survives inside any lone formation
(reproduced: 0 misses, 800 ships, and still 0 at 10× radial spread) but in the game's normal mixed
scenes a phase ordering structurally cannot see different-n partners — fleet-scope misses 100% of
cross-population encounters, global-scope misses 7.8–21.7% at k = 4 — and the required rank is not a
constant: it is Δn·Δt_refresh·N/(2π), measured to trade linearly against refresh cadence (p99 rank
33.6 → 11.0 → 6.1 → 3.0 as cadence goes 8 → 16 → 32 → 64 per orbit).

**Bottleneck.** The board's #1 risk ("candidate work at scale … work must track real encounters") and
the in-flight `co-orbital certificate` build (two lanes, HANDOFF table). Gain: this red-team confines
the certificate before it freezes, and hands the build the correct trigger — a dimensionless number in
Δn·Δt·N, not spatial concentration — plus the measured necessity of an orbit-geometric cross tier
(Binet arcs, O(n_other) orbit-pairs, not O(n_fleet·n_other) body pairs, which measured 320,000
candidate pairs for 522 real cross encounters = 625 pairs per encounter, the gold's quadratic setup
returning at 800×400 scale).

**Evidence** (2D plane, one star; truth = every pair-local minimum of distance below ρ = 1.5×10⁻³ AU
over 2 orbits, Keplerian, aligned with `crates/encounters/src/truth.rs`; validated against dense
Brent to ≤ 2.2×10⁻⁹ AU; certificate checked at the last refresh before each encounter's minimum;
2 seeds each, medians; cadence 16/orbit unless noted; each run 6–20 s, load 0.3→4 on 8 vCPU):

| scene (N) | pair type | E | miss@k=4 | rank p99 | note |
|---|---|---|---|---|---|
| fleet (800) | fleet-fleet | 263 | **0.000** | 1.0 | control: gold reproduced |
| loose fleet, σ_a/a=1e-2 (800) | fleet-fleet | 73 | **0.000** | 1.2 | spread alone doesn't break k=4 |
| fleet + 80 crossers (880) | fleet-fleet | 270 | 0.006 | 2.1 | crossers contaminate the ordering |
| fleet + 80 crossers | fleet×crosser | 136 | 0.217 (global) / **1.000 (fleet-scope)** | 11.0 | crossers unrankable in fleet-scope |
| fleet + 400-body belt (1200) | fleet-fleet | 255 | **0.000** | 2.0 | the formation itself stays exact |
| fleet + belt | fleet×belt | 512 | 0.078 (global) / 1.000 (fleet-scope) | 8.0 | |
| fleet + belt | belt×belt | 134 | **0.127** | 9.3 | a population is not a formation |

Cadence coupling (global-scope, cross pairs, p99 rank): crossers 33.6 @8 → 11.0 @16 → 6.1 @32 →
3.0 @64 per orbit; belt 20.7 → 8.0 → 4.0 → 2.0. k ≈ Δn·Δt_refresh·N/(2π) confirmed to first order;
holding k = 4 for crossers needs ~64 refreshes/orbit, multiplying the O(n·k) tier's sort cost by 64
at exactly the 10⁶ scale where the sort is the cost being replaced.

Reproduce: `cd lab/results/20261008-0338-inversion-4c98/work && python3 probe.py <case> <seed>`
(cases: fleet, loose-fleet, fleet+crossers, fleet+belt; seeds 1, 2), then `python3 analyze.py`;
per-population split: the snippet in the run log (`tt = pop[I]*2+pop[J]`). Data: `*-1.json`, `*-2.json`.

**Predictions** (`predictions.md`, written before the decisive run): P1 control pass ✓; P2 fleet-scope
misses ≥ 95% of cross ✓ (100%); P4 belt cross miss > 5% ✓ (7.8%); P5 loose-fleet intra rank ≤ 4 ✓
(1.2 — the failure is differential n across populations, not spread within one); **P3 failed in
magnitude** (predicted p99 > 20, measured 11.0 — direction right, k = 4 still killed); **P6 half
failed**: the linear coupling held (ratios 0.33/0.56/0.49 vs predicted 0.5 ± 0.3) but at cadence
1/64 the crosser p99 is 3.0, not > 8 — at that cadence k = 4 closes the crossers' tail by paying 64
sorts per orbit. Both misses are reported, not absorbed.

**What would make it wrong.** (1) The truth is unperturbed Kepler — mutual gravity is absent; but the
gold's claim is about candidate geometry, and the crate's own truth is the same class. (2) My
certificate semantics (refresh cadence, circular rank, last-refresh-before-minimum) is disclosed, not
the build's; if the build refreshes adaptively per pair the numbers move but the structural result
(fleet-scope cannot rank outsiders; Δn sets the rank) does not — it is representation-independent
arithmetic. (3) If the in-flight build already scopes the certificate per formation and keeps a Binet
cross tier, this kills only the board's universal sentence, and confirms the design instead.

**Cost of adoption.** No code; one constraint on a spec that is being written now: the concentration
trigger must become Δn·Δt_refresh·N/(2π) ≲ k (with k's budget stated against the sort cost), the
phase tier must be scoped to Δn-bounded formations, and cross-population encounters must go through
orbit-geometry (each foreign orbit vs the formation's one orbit: two arcs, a phase window on the
ring), never through body-pair setup.

**Fit with PRINCIPLES.** "A fix signals the wrong representation" (19): raising k or the refresh rate
to catch crossers is the bandaid; the orbit-pair tier is the right water. "Symmetry is found, not
given" (32): phase rank is the symmetry of co-rotation — Δn = 0 — and it dissolves outside it.
"Spartans" (10): the cheapest falsifying scene (one fleet, one belt, 20 s) before the 10⁶ build freezes.

**The lens may have made me miss:** the actual certificate implementation on the branch (not in this
checkout — it may already be right); whether the game even keeps mixed scenes at one scale long
enough for the cross tier to matter (an arriving fleet spends most of a synodic period far away);
and the checker should re-run with an eccentric fleet (e > 0 formations), which I did not test —
rank in true anomaly, not longitude, may be required there.
