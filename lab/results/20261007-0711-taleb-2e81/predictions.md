# Predictions (written before the decisive runs; smoke at 20×20 H=2 verified the instrument only)

Question (one sentence): the adopted train certificate (taleb-09b5) and its two checkers only ever measured concentration WITHIN one orbit family — what does the engagement of two swarms on crossing orbits (each internally tight, the game's fleet-meets-fleet case) do to the pairwise candidate tier, and is there a bounded-rank guard there?

Setup: swarm A tight near-circular at a=1 (a-hw 1e-5, Rayleigh e≈0.001, ϖ ±0.1, λ uniform), swarm B tight eccentric a=1.2, e=0.3, ϖ=0 (pericentre 0.84, apocentre 1.56 — crosses A's annulus at two longitudes), same spreads. ρ=1e-4, μ=1, safety 1.5. Binaries: `cross econ|guard|rankscale` (crates/encounters/src/bin/cross.rs). Truth = truth.rs conservative advancement (Halley states); method = sections + Diophantine first-hit + exact check (Newton states) — no shared solver path.

P1 (saturation): ≥ 99.5% of the n_A·n_B cross pairs are cone candidates at every n tested; the cross Binet separation (~0.29) sits ~3 orders above eps_u (~4e-4), so the gold's clump trigger (intra-diameter ≤ eps_u) never fires for the cross set — the tier stays pairwise exactly in the engagement regime. Also: swarm B's own intra-diameter is ~5e-2 ≫ eps_u (the e·Δϖ/p term: ±0.1 rad on e=0.3), so an eccentric fleet does not even trigger its own internal train — the trigger's ϖ sensitivity scales as 1/e.

P2 (ruin signature = store, not compute): cross sections are ~2 Cross per pair with ~0 numeric setup evals per pair (analytic crossing windows; unlike the fleet's Wide 606). The ruin is the STORE and the enumeration: Θ(n_A·n_B) pairs × 2 sections × ~72 B ≈ 144 TB for a 10⁶×10⁶ engagement, before any compute. A different signature than taleb-09b5's dormancy-compute ruin: cheap per pair, unpayable in aggregate.

P3 (soundness): on the full 80×80 set over H=8 orbits, method ≈ truth: extra = 0, missed ≤ 2 (boundary-straddling conjunctions per the gold's checker; interior misses 0). Expected true encounter count ~10±5 (per-pair coincidence rate ≈ 2·(2/P_A)·(2/P_B)·ρ/v_rel ~ 1e-3 per 50 time units).

P4 (the guard, decisive): for every true/method encounter, the partner's nearest node-passage (at the encounter's node, the ≤2 crossing longitudes of the mean orbits) ranks ≤ 8 among the other swarm's passages nearest the encounter time; p99 ≤ 4; max rank does NOT grow from n=120 to n=240 (it is set by local λ density ~ n·ρ·window, flat in n at fixed spread). If max rank grows ~linearly in n, the interchange certificate is dead and the engagement needs a different representation.

P5 (my own claim's risk, pre-registered): the node is a property of the PAIR of orbits; intra-swarm e-spread (1e-3) smears each pair's crossing longitude by ~1e-3 rad ≫ ρ. The mean-orbit station still catches everything (the smear stays inside the station's arc), but if I am wrong the ranks will be dominated by encounters far from the mean node — visible as rank outliers attached to passages far from t*.

Kill criteria for my claim: (a) cross-candidate fraction ≪ 1 ⇒ no quadratic store, no hole; (b) node-rank growing with n ⇒ interchange guard dead; (c) missed > 10% ⇒ the window tier is unsound for crossings too, which would be the bigger finding.

Held-out cases I will not tune on: seed offset +7 for guard/rankscale (second λ draw), H halved/doubled for rankscale, n=240.
