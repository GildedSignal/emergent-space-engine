# Predictions (written before any run of the crossing experiment)

Scene: two concentrated coplanar lanes crossing. Lane A: circle, a∈[1.0000,1.0002], Rayleigh e (σ=1e-4), uniform ϖ, λ. Lane B: eccentric stream, a∈[1.1000,1.1002], e=0.12±5e-6, ϖ∈±0.02 rad, uniform λ; its annulus [0.968,1.232] crosses lane A at θ*≈±0.79 rad. ρ=1e-3, horizon 20 orbits of a=1 (t_end=40π), same conventions as the crate's verify sets. Lanes have fixed extent, so growing m grows lane density — the complement of the dilution direction; game scenes are concentrated (rings, debris streams, traffic lanes).

The adopted certificate stack, as recorded on the board: tier-1 group envelopes (pay once while disjoint — refuses here, the lanes cross), tier-2 per-pair Binet cone + Diophantine sections, and the 6-Oct gold's phase-neighbour route for same-orbit concentration (rank ≤ 4 along one orbit — does not apply across two different orbits). So the A×B block must go through tier 2.

Predictions, held out (not tuned):

1. **Candidates are the full product.** cone_pairs and radial_pairs both return exactly m² A×B pairs at every m (no pruning is possible: the orbits cross by construction), and ~m²/2 within each lane.
2. **Hits scale as the product** (encounter rate = flux × flux × cross-section): exponent of hits vs m = 2.0 ± 0.2 on m ∈ {125,…,2000}.
3. **Setup dominates and is the product.** Total evals ∝ m²; setup (sections) share > 60%; constant C = evals per A×B pair in [20, 300]; per-hit check cost stays flat in m.
4. **The adopted metric stays formally fine while the absolute work dies**: work per real encounter (evals/hits, checks/hits) varies by less than ~2× across m, but total A×B evals at m=2000 reach ~10⁸ on 4 threads. Extrapolated to 10⁶×10⁶ ships: C·10¹² evals per epoch (and setup re-pays per element change), i.e. ≥ 10⁴ s on this machine even at C=20 — tier 2 cannot be paid even once at game scale.
5. **Zero-miss holds at m=100** (method vs truth on the A×B block; no misses, no false, all truth events inside the cone set): the failure is cost, not correctness.
6. **Within-lane blocks (A×A, B×B) reproduce the gold's pathology**: near-identical orbits → wide/full sections, evals-per-hit ≫ the crossing block's, hits sparse (synodic lap ≫ horizon).
7. **The constructive invariant**: every A×B encounter has both bodies' longitudes within ~0.15 rad of a crossing longitude θ*, with a width that does not grow with m — which is exactly what a mean-lane section + sorted-phase range query needs to collapse the m² block to O((n_A+n_B) log n).

Kill criteria for my own claim (if any hits, the finding dies or inverts):
- A×B cone candidates ≪ m² at large m (the tier already prunes concentrated crossings), or
- hits grow ≪ m² while evals grow as m² (per-encounter work diverges — different, weaker finding), or
- truth at m=100 finds encounters the cone misses (unsoundness, a different and more severe finding, to be reported as such).
