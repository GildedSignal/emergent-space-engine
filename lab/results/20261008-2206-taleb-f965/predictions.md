# Predictions (written before any scene ran)

Question: the co-orbital certificate adopted on 6 October (phase-neighbour rank ≤ 4 at O(n·k) for
concentrated workloads, replacing the quadratic window tier) — where does it break, and does a
family-level crossing gate keep candidate work tracking real encounters?

Scenes (all coplanar Kepler, µ = 1, a ≈ 1, ρ = 1e-4, independent truth = `truth_pair` on all
radially overlapping pairs):
- S1 `formation` (control, the gold's own regime): n = 300, a ∈ [1,1.0001], Rayleigh e σ = 3e-4,
  uniform angles, 50 orbits.
- S2 `fleet-belt`: fleet n = 150 (a ≈ 1 ± 5e-5, e = 0.2, ϖ ≈ 0, λ uniform) crossing a belt
  n = 400 (a ∈ [0.93,1.07], Rayleigh e σ = 0.01), 15 orbits.
- S3 `fleet-fleet`: two fleets n = 150 + 150, same (a, e) = (1, 0.2), ϖ = 0 vs π/2 (crossing
  ellipses), λ uniform, 20 orbits.
- S4 `wedge`: fleet-fleet where the second fleet's λ lies in a 0.3 rad wedge aimed at the crossing
  (all near-simultaneous at the crossing: the contact storm), 20 orbits.

Methods: `cone` (the adopted two-tier: Binet cone + section windows, all candidates);
`rankk-global` (the dangerous reading of the trigger: phase-rank k = 4 over *all* bodies by
longitude at t = 0); `gate` (this run's repair: greedy families in Binet space ε = 2e-3, rank-4
inside a family, and for each crossing family-pair a time gate at the crossing longitudes with
safety S = 4 on the window ρ+ε over relative speed, then the same exact per-pair check).

Predictions, each falsifiable:
- P1 (control): S1 `gate` (rank-4 intra) misses 0 of the truth's encounters. If it misses, the
  gold does not reproduce in this harness and everything below is void.
- P2 (blind spot): S2 `rankk-global` misses > 50% of the truth's encounters (cross-population
  encounters are not phase neighbours at t = 0).
- P3 (cliff): S2 and S3 `cone` candidate pairs ≈ n_fleet · n_other (orbit overlap, not timing):
  ≳ 6×10⁴ on S2, ≳ 2×10⁴ on S3, regardless of how few encounters happen.
- P4 (gate soundness): `gate` misses 0 on S2, S3, S4 at S = 4.
- P5 (gate cost): `gate`'s pair checks ≤ ~10² × real encounters per scene, and its hits per
  encounter does not grow when both fleets double (S3 scaling 37/75/150), while `cone`'s
  candidates grow ~4×.
- P6 (honest risks): near-tangential family crossings widen the window (cost, not misses); member
  spread ε vs ρ sets the slack: hits/enc ≈ S·(ρ+ε)/ρ ≈ 84 here. If misses persist at S = 16 the
  time-gate representation is unsound and I kill it in the dossier.

Kill criterion for the rung this feeds (`b-coorbital-cert`): any method that misses encounters it
claimed to certify, at any N, is dead; a method whose work per real encounter grows with N is
dead at scale even with zero misses.
