# Dossier — 20261008-1058-inversion-6534 (lens: inversion)

## Claim

The encounter certificate stack adopted on 6 October (Binet-cone tier 2 + group envelopes + phase-neighbour for same-orbit concentration) has a third regime it routes to the full product: **two concentrated crossing lanes pay tier 2 exactly n_A·n_B pair set-ups** (~0.8 µs/pair measured, exponent 2.00), the scene's per-encounter work is the *lowest* of anything measured (39 evals/hit, flat in m) — so every per-encounter metric calls this the healthiest scene while its absolute cost is the one the frame budget cannot pay — and all its encounters lie in a measured, m-independent corridor (±0.03 rad) around the crossing longitudes, which is the invariant a crossing-time-rank certificate needs to collapse the product to O((n_A+n_B)·log n).

## Bottleneck

Board's top scaling risk ("candidate pairs per body grow with N; candidate work must track real encounters", q-candidate-degree) and the 6-Oct gold `20261006-0346-taleb-09b5` (co-orbital concentration → phase-neighbour rank-4). Inversion of that gold: its certificate is rank along *one orbit*; the envelope tier is *Binet-space* and cannot separate orbits that cross. A lane crossing a lane (fleet orbit × ring, debris stream × traffic lane) is concentrated on both sides and between-orbit by construction: both adopted routes refuse it, tier 2 takes it, and tier 2 is per-pair. Gain if fixed: the O(N²) term is removed from the last regime that still has it — two 10⁶-body lanes go from ~2 days of set-up per epoch (measured rate) to a sort plus range queries.

## Evidence

Scene (2D, μ=1, the crate's own conventions): lane A = near-circular, a∈[1.0000,1.0002], Rayleigh e σ=1e-4, uniform ϖ, λ; lane B = eccentric stream, a∈[1.1000,1.1002], e=0.12±5e-6, ϖ∈±0.02 rad, uniform λ; its annulus [0.968,1.232] crosses lane A at θ*≈±0.792 rad. ρ=1e-3, horizon 20 orbits. All commands: `work/crossing/run.sh` (each step < 60 s; raw lines in `work/crossing-outputs.jsonl`). Linux/x86 shared runner (8 vCPU, 4 threads used) — timings are order-of-magnitude only; counts and evals are deterministic.

- **Control (soundness, m=100/lane):** method vs truth over all 10⁴ A×B pairs: 124 encounters, 124 matched, **0 missed, 0 false, 0 dup, 0 truth events outside the cone set.** The tier is *correct* on this scene; the finding is cost, not correctness.
- **No pruning exists:** cone and radial candidate sets both return exactly m² A×B pairs (m=500/1000/2000: cone_ab = 250000/1000000/4000000; scanned = all pairs). Structurally forced: every A orbit crosses every B orbit, and the U-range scan's reach (∝ e_max) cannot exclude a lane it must include.
- **The product, measured (A×B block):** m = 125→2000 per lane: pairs 15 625→4 000 000; hits 189→49 574 (**exponent 2.016**); evals 7 545→1 912 173 (**exponent 2.003**); wall 0.02→3.3 s. Per pair: 0.5 evals, 2 Cross sections, **0 numeric-window evals** (the analytic crossing window suffices), ~0.79 µs/pair, flat in m.
- **The per-encounter metric is inverted:** evals/hit = 39–40 and checks/hit = 1.3 at every m. For contrast, same ρ and horizon: diffuse belt (shipped `steady 2000 1e-3 20`): 14 950 evals/hit; same-orbit eccentric lane (B×B): 32 460 evals/hit. The fatal scene is the *cheapest per encounter* of everything measured.
- **Independent reproduction of the gold's regime (harness positive control):** within-lane B×B (near-identical orbits): 394.0/394.4/395.9 setup evals/pair at m=125/250/500, Wide+Full sections — the setup blow-up the 6-Oct gold reported, reproduced flat in m.
- **The corridor invariant (the exit):** over 15 391 A×B encounters (m=500+1000), every encounter has *both* bodies within d_max = 0.029–0.030 rad of a crossing longitude; d50 = 0.0104 ≈ ρ/sin γ = 0.0127 (γ = 4.5° incidence); **zero encounters beyond 0.15 rad; width does not grow with m.**

**Extrapolation at the measured 0.79 µs/pair (4 threads, cloud):** 10⁴×10⁶ ships (a fleet crossing a ring) = 10¹⁰ pairs ≈ 30 min per epoch; 10⁶×10⁶ = 10¹² pairs ≈ 2 days per epoch — and the 6-Oct gold `components-4643` showed set-up re-pays on every element change. No per-pair engineering closes this: even at 1 ns/pair it is 10³ s per epoch. The product must never be enumerated.

## Predictions

`predictions.md` was written before any run. Held: candidates = exact product (1); hits/evals exponent 2.0 ± 0.2 (2, measured 2.016/2.003); per-encounter flat (4); zero-miss control (5); the gold's pathology reproduced within-lane (6); corridor width ~0.01 rad scale and m-independent, none beyond 0.15 (7). **Failed, informatively:** (3) predicted setup evals/pair in [20,300] and setup-dominated cost; measured 0 numeric setup evals/pair and 0.5 evals/pair total — the crossing block is already near the per-pair floor (one analytic window + one Diophantine jump ≈ 0.8 µs) *and still dies at scale*. The failure strengthens the claim: there is no per-pair fat left to cut.

## What would make it wrong

- The scene is rarer than assumed: if the game never holds two large concentrated populations in mutually crossing annuli, the product block stays small in practice. That is a workload bet, not a certificate — nothing in the design today bounds the block.
- My lanes are coplanar and prograde (the crate is 2D). Retrograde or mutually inclined crossings change the incidence angle (corridor width ρ/sin γ grows as γ→90°) but not the product structure.
- The corridor certificate could fail where the section machinery doesn't: near-tangent crossings (γ→0, corridor → ∞) degrade back to Wide sections — there the product may be genuinely unavoidable, as it is for one self-concentrated orbit.
- The 6-Oct gold's exact trigger lives on its branch (unreadable from this job, no credentials); I attack the routing as the board records it. If its dimensionless trigger already contains a between-lane clause, this run reduces to a measurement confirming why that clause is load-bearing.

**Cost of adopting:** one more route in the trigger (concentrated×concentrated with intersecting cones → crossing-time ranks, not pair enumeration): sort each lane's crossing times per crossing longitude once per epoch, sliding-window merge with half-width ρ/v_rel; exact checks only on window products. O((n_A+n_B)·log n) per window; the rank-window idea is the gold's own, transplanted from orbit phase to crossing time. Fit with PRINCIPLES: "Compute only surprises" (§3), "candidate work must track real encounters" (board), and §10's "We need also to map how things break, think in extremes" — this is the extreme the per-encounter metric cannot see. Via negativa (§1): the fix deletes the enumeration, it adds no mechanism to the law.

## The lens (what inversion may have made me miss)

Inversion optimized for the *guaranteed* failure and found a structural hole between two adopted certificates; it did not attempt the constructive certificate beyond measuring its enabling invariant, and it did not test the third regime's *correctness* claim (a crossing-time-rank certificate would need its own zero-miss rung — near-tangent γ is where I expect it to bleed). It also says nothing about H_live or the allocator, the other two ways the frame dies. One probe, one regime: the war-scene corridor certificate is a design input, not a result.
