# Predictions — 20261006-1354-system-d9fb (written before any run)

Question: are the encounters subsystem's three adopted components — the Binet-cone two-tier
certificates with per-pair numeric-window setup, the co-orbital phase train, and the slack
skin that defers setup — projections of ONE storeless mechanism: per-body exact band
constants + relative-phase epoch events (true-longitude alignments), with nothing
materialized per pair?

The watch (method under test), per pair, all O(1) arithmetic unless an epoch exists:
1. theorem filter: r-ranges must overlap (d < ρ ⇒ |r_i − r_j| ≤ ρ);
2. band epochs: true-longitude alignment Λ_i = Λ_j requires |Δλ(t)| ≤ C_i + C_j where
   C = each body's EXACT max equation-of-center (a per-body constant, in fact a function
   of e alone ⇒ one table). Epochs are solved from the linear drift Δλ in closed form;
3. inside an epoch only: Newton roots of Λ_i(t) − Λ_j(t) = 0, one distance eval each.

No per-pair store, no numeric windows, no sections, no setup, no skin. The train regime is
the Δn→0 limit (band always on, few partners), not a separate mechanism.

Scenes: uniform belt N ∈ {250, 500, 1000, 2000}, σ_e = 0.01 (components-4643's main
workload), a ∈ [0.9, 1.1], ρ = 1e-4, T = 20 orbits; adversarial at σ_e = 0.05: high-e
(0.7–0.9), a-clumped, phalanx (co-orbital, the gold's kill case), resonant rings.
Truth: theorem-filtered dense sampling (64/orbit) + refinement, plus an unfiltered 2%
audit sampled by true anomaly (different bias than time-uniform), plus ultra-dense
adjudication of every dispute.

Pre-registered predictions on cases I have NOT tuned on:

- P1 soundness: zero adjudicated misses on every scene, including the phalanx and the
  conjunction-less population (r8 v2's leak: 0.5–6% of encounters, 78% adversarial).
  Any adjudicated miss KILLS the claim.
- P2 conjunction-less: in the uniform belt, encounters whose pair has NO mean-longitude
  conjunction within T are ≥ 0.5% of encounters (they exist), and all of them lie in
  pairs whose band |Δλ| ≤ W while Δλ never crosses 0 — the epoch rule catches them.
- P3 scaling: watch evaluations per real encounter flat in N at fixed belt geometry
  (log-log slope ≤ 0.1), vs element-sort's measured ~2 (r8 v2).
- P4 tails: per-pair evals bounded — max per-pair evals over a scene ≤ 60× its epoch
  count + 60 (the tier's single pairs spiked to 5,926 evals; fat tails are the claim's
  death).
- P5 phalanx replication: true encounters within phase-rank ≤ 4 of their partner
  (independent replication of taleb-09b5's train finding), at O(1) events per encounter
  (the regime dissolves into the same watch).
- P6 memory: the watch holds ~2N certificates; the tier materializes cone-passing pairs,
  which I predict is 0.1–0.6·N² (the 40-TB ruin arithmetic of the gold).
- P7 held-out risk I name myself: near-resonant rings (2:1, 3:2) make many pairs with
  fast synodic rates; I predict evals per encounter stays within 3× the uniform belt's
  (if it explodes, the watch is missing a resonance-specific structure).

Kill criteria: P1 any miss = kill; P3 slope > 0.3 = kill; P4 violation = kill of the
no-fat-tail claim (claim survives weakened if only in the resonant scene).
