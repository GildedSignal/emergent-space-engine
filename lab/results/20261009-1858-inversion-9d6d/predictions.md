# Predictions — 20261009-1858-inversion-9d6d

Written after the m=100 plumbing pilot only (which showed rank_p99 ≈ 4·k_pred at k_pred = 1).
The decisive grid below has not been run. Code frozen: `crates/encounters/src/bin/rank.rs`.

**Question.** Gold 20261006-0346-taleb-09b5 replaces the pairwise candidate tier inside a fleet
by a phase-neighbour certificate, "every real encounter lies within partner rank 4 along the
orbit", O(n·k). Inversion: rank-4 is not a property of the geometry; the rank a partner occupies
at window start is set by synodic drift across the window divided by local phase spacing.
k must scale as m·E|Δn|·H/TAU ≈ 0.5·m·band·orbits (uniform band, a≈1), or the certificate
misses encounters at large m. The gold's scene (coorbital spec in main.rs: m=300, band 1e-4,
H=50 orbits, σ_e 3e-4, ρ 1e-3) has k_pred = 300·0.5·1e-4·50 = 0.75 — rank 4 is safe there
by a factor ~5, an accident of m=300.

**Grid** (all σ_e = 3e-4, ρ = 1e-3, exact truth per pair, rank in the t=0 mean-longitude sort):

| id | m | band | orbits | k_pred |
|---|---|---|---|---|
| anchor | 300 | 1e-4 | 50 | 0.75 |
| m300  | 300 | 4e-4 | 50 | 3.0 |
| m600  | 600 | 4e-4 | 50 | 6.0 |
| m1200 | 1200 | 4e-4 | 50 | 12.0 |
| collapse | 300 | 1.6e-3 | 50 | 12.0 |
| H25 | 600 | 4e-4 | 25 | 3.0 |

**Pre-registered predictions:**

- P1 (gold reproduces in its own domain): anchor rank_p99 ≤ 4, miss(k=4) = 0.
- P2 (rank ∝ m): rank_p50 and rank_p99 grow roughly linearly in m along m300→m1200;
  at m1200, rank_p50 ≥ 4 and miss(k=4) > 0.5.
- P3 (dimensionless collapse): collapse (m·band equal to m1200) gives rank_p50 within ±40%
  of m1200's and rank_p99 within a factor 2 (discreteness at m=300 is the noise).
- P4 (rank ∝ H): H25 rank stats ≈ half of m600's (p50 within ±40%).
- P5 (the honest floor): enc ∝ m² (m300→m1200 within ×16±50%); tier candidate pairs per real
  encounter roughly constant (the pairwise tier is NOT cost-quadratic at these bands — its
  failure at fixed k is misses, and at tight bands the 135× setup blowup is the separate
  near-identical-orbit degeneracy already killed by the gold).
- P6 (extrapolation, not run): at the board's 10⁶-ship fleet on the gold's own band (1e-4)
  and H=50 orbits, k_pred = 2500: a fixed rank-4 certificate misses essentially every
  encounter; a k-law certificate costs m·k ≈ O(encounters) and stays encounter-linear.

**Kill criterion for my claim:** if anchor shows rank_p99 > 4, or rank stats do not grow with
m beyond noise (ratio m1200/m300 p99 < 2), the drift law is wrong or irrelevant and the gold's
rank-4 stands as scale-free. That would make this run a lead ("rank-4 is robust"), not a finding.

**Added probes after the main grid ran** (predictions written before running them):

- P7 (seed robustness): m600 band 4e-4 H50 with seed 999: rank_p50 3±1, miss(4) ≈ 0.31±0.05.
- P8 (ρ-insensitivity): same scene with ρ = 3e-4: rank stats within ±20% (κ does not contain ρ;
  only encounter counts drop).
- P9 (phase-bunched fleet, the silent phase assumption): m600, band 4e-4, H50, phases uniform in a
  window W = TAU/8 ⇒ local phase spacing 8× tighter ⇒ κ_eff = κ·(TAU/W) = 48: rank_p50 ≈ 20–30,
  rank_p99 ≈ 90–130, miss(k=4) > 0.85. A bunched fleet breaks fixed-k far harder than a spread one.
