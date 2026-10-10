# Predictions — 20261010-1152 (second author on 20261010-1029-library-6cfc)

Written before running `cost`, `truth`, or `slack` (only `smoke` has run: machinery works,
mini-fleet metric set 119 vs phase set 5, 2 hits found). The checker's named experiment:
the metric-vs-phase-rank skin comparison on the engine's real encounter path
(`crates/encounters`' own machinery), on the taleb-09b5 formation workload,
station-kept, with kick churn and eccentricity dispersion, counting setups AND
pair-evals end-to-end, and the 12.6x slack lever's survival.

Setup (fixed before runs): belt = n 4000, a∈[1.0,1.5], e~Rayleigh(0.01); fleet =
taleb-09b5's (400 ships, a=1±1e-5, e~Rayleigh(0.001), ϖ within ±0.1, λ uniform, + 3600 sea
a∈[0.9,1.1] e~Rayleigh(0.05)), ρ=1e-4, cert horizon 20 orbits, 100 kicks on fleet bodies,
station-keep (λ re-pack) every orbit, kick eps ∈ {1e-9, 1e-7, 1e-5, 1e-3}.
Phase skin: k=5 partners nearest in mean longitude, rebuild interval =
boundary gap / (2 × max |Δn| over the whole clump) — sound against non-members.

## P1 — metric-skin saturation on the real path is permanent (element-based)
The metric (Binet-cone) set of a kicked fleet body has p50 ≥ 350 fleet partners at every
eps ≤ 1e-5 (the cone is element-based: λ-packing is irrelevant, the a-clump alone
saturates it — stronger than the synthetic probe, which needed phase packing).
Fleet per-kick evals ≥ 50× belt per-kick evals. At eps=1e-3 the kicked body leaves the
clump (Δa = 100× clump width) and its fleet set collapses.

## P2 — phase skin holds O(k) cost under the same workload
pairs_per_kick = 5 exactly; µs/kick within 3× of the belt's metric µs/kick;
rebuilds/body/orbit ≤ 50 at eps ≤ 1e-5 (≈ 1 station-keep + churn), rising at eps=1e-3.

## P3 — partner rank under churn and station-keeping (assumed by the dossier, unmeasured)
In the phalanx truth runs (200 ships, σ_λ=0.01, churn 1e-5 and 1e-3, 3 orbits):
distance-rank max ≤ 8, λ-rank max ≤ 8, p99 ≤ 3. Misses: k=8 → 0; k=5 → ≤ 2% of
encounters (0 if taleb's static rank≤4 transfers); k=4 → possibly a few (the gold's
own claim is rank ≤ 4, which needs k=5 partners — the off-by-one the checker flagged).

## P4 — the synthetic probe's belt row does NOT transfer to the real belt
On the real multi-a belt the sound phase skin's rebuild rate (analytic: gap/(2·Δn_max))
is ≥ 10³ per body per orbit (Δn_max ~ 0.2 there vs ~3e-5 in the clump) — a rebuild
storm. The synthetic probe's "phase skin is fine in belts too" was an artifact of its
one-ring model. Prediction: the adoptable claim is regime-conditional (train inside the
co-orbital clump, cone elsewhere), matching taleb-09b5's trigger one layer down.

## P5 — the 12.6× slack lever dies on the metric skin under concentration, survives in the train
Belt metric pairs (control): skippable fraction at eps=1e-7 ≥ 0.5 (the shipped kick()
regime; anchor: regenerate the crate's own `kick` numbers).
Fleet fleet-fleet metric pairs: mostly silent (dormant) but with tiny slack budgets —
skippable at eps=1e-7 < 0.3 (uncertain: if Full/Wide windows absorb drift, could be
higher; I commit to < 0.3 as the kill line for "slack alone saves the metric skin").
Phase-partner pairs: skippable ≥ 0.5 at eps=1e-7 (the lever survives inside the train).

## P6 — belt phase-rank coverage is not the failure mode there
λ-rank of belt-encounter partners: max ≤ 4 (sparse coincidence; the belt kills the phase
skin on rebuild cost, P4, not on coverage).

Kill criteria for the run's claim: P1 or P2 failing refutes the library run's cost
story on the real path; P3 failing (rank > 8 or k=8 misses) refutes the train
certificate under churn; P4/P5/P6 calibrate the regime boundary and the lever.
