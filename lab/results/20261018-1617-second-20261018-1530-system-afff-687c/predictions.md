# Predictions (written before the decisive flights)

Question (the checker's named gold-experiment): does the scan's answer stay
rank-local in the SWEPT metric — rank by miss distance of the relative segment
`d + [0, w]` over the interval, the metric the predicate itself measures — with
`k` chosen by a dimensionless window-density trigger rather than the constant
16, across the three regimes that killed the at-t Euclid read (burn at the
600-member crowd, the 6,000-member dense crowd, seed 2)?

Only a sanity flight of the shipped scene (8 s, 77 scans) was run before this
file; the burn, dense and seed-2 arms are unflown with this build.

- **P1 (the swept metric absorbs the burn entries).** Under burn at 600 members
  (seed 1), ≥ 99% of the hits that sit beyond at-t Euclid rank 15 come inside
  swept rank 16 (`euc_gt15_sweep_le15 / euc_gt15` ≥ 0.99), and ≥ 99.9% of all
  hits lie within swept rank 64. The burn manufactures sweep-entry hits
  (large |w|), and the swept miss of a sweep-entry body is small by
  construction — so the metric should own exactly the class that broke Euclid.
- **P2 (the dense crowd: locality holds only at the answer's own scale, and the
  fixed k=16 rule fails as its own negative control).** At 6,000 members the
  answer itself is thousands (`max_answer` ≈ 4,000), so: `kviol_k16` ≈ 95% of
  hits (the control must fail), while every hit stays within swept rank
  ≈ 2× its scan's own hit count — the interleave (receders with smaller swept
  miss) is ≈ the hit count, not more.
- **P3 (the density trigger covers the transitions).** With k = max(16,
  ceil(α·μ_prev)), μ_prev the previous answered scan's hit count: violations
  ≤ 1% of hits at α = 2 and = 0 at α = 4 across every arm (burn included —
  under burn the scans refresh per kick, so μ_prev tracks the window as fast
  as the record could). If μ jumps between consecutive scans by more than
  ~4× anywhere except the first answered scans, this fails and I report where.
- **P4 (seed 2 reproduces the coast shape).** Coast at 600 members, seed 2:
  all hits within swept rank ≤ 32, `kviol_k16` = 0, census fractions within a
  few points of seed 1.
- **P5 (the gain becomes a law, not a constant).** The k-read's gain is
  cand/k: at the sparse scenes (shipped, ladder, crowd-600) it stays ≥ 20×
  with k ≤ 64; at the dense crowd it collapses to ≈ 1 (the walk is already
  O(answer) there — nothing to delete). The dossier's headline number becomes
  the dimensionless pair (window density μ, walked count K), both maintainable
  without a walk, not a universal K/k.

**Kill criterion for the certificate:** if under burn or the dense crowd,
hits sit at swept ranks beyond ≈ 4× their scan's window density in numbers
> 5%, then no neighbour-metric certificate serves the scan in an ordinary
regime and the k-record claim is refuted for good (the answer genuinely spans
more bodies than the window's density predicts). If only the α ≤ 2 triggers
fail while α = 4 holds, the claim survives with its scope and cost corrected.

**Stated approximation (a limit, not a result):** μ_prev refreshes per
answered scan; a shipped record would refresh per event (birth, kick, death).
At the coast scenes scans are rare, so per-scan refresh is optimistic there;
the dossier carries this as the record's unmeasured churn half.
