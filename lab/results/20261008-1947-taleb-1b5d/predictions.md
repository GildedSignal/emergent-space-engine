# Predictions — written before the decisive sweep (2026-10-08)

Claim under test (board, gold 20261006-0346-taleb-09b5): under a formation,
every real encounter lies within partner rank 4 along the orbit, so a
phase-neighbour certificate at O(n·k) replaces the quadratic tier, triggered by
a dimensionless number (a-concentration).

The sweep varies lawful formation knobs the gold did not: certificate lifetime
T, semimajor spread sig_a, eccentricity e with apsidal spread (varpi uniform),
and phase-space multimodality (two varpi clusters). Not tuned on any of these
numbers; predictions from two-arguments-on-paper only.

- P1 (drift vs lifetime, aligned circular): conjunction partners are bodies the
  synodic drift carries across ~1.5·S·(T/P)·N spacings of phase. Expect
  miss@4 ≈ 0 at T=1P, S=1e-3; rising to 5–40% at T=4P; ≈ 0 at S=1e-4; and
  ≥ 50% at S=1e-2 (drift ~60 spacings at N=1024). A quarterly rebuild (re-rank
  every P/4) should zero the first two but leave residue at S=1e-2.
- P2 (eccentricity is geometric, not drift): with varpi spread, conjunctions
  happen at orbit crossings where mean longitudes differ by the Kepler M−f
  offset (up to ~1.4 rad per body at e=0.8). Expect partner ranks of order
  N·|Δλ*|/2π, i.e. miss@4 majority at e ≥ 0.3, max rank scaling ~linearly in N
  (256 vs 128 at e=0.6 roughly doubles), and NO fix from rebuilds.
- P3 (multimodal phase): two varpi clusters (battle-like) put every
  inter-cluster encounter at rank ~N/4; expect inter-cluster miss@4 ≈ 100%
  while intra-cluster rank-4 still holds.
- P4 (silence): sig_a identical (1e-4) between the gold-repro case and the
  eccentric cases, so any trigger reading only a-concentration fires in both;
  the eccentric misses are invisible to it.

Kill criteria for my own probe: if the eccentric cases show miss@4 ≈ 0 at
e=0.8, or inter-cluster encounters at rank ≤ 16, the fragility claim is wrong
and the certificate's domain is wider than argued.
