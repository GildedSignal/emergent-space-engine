# Predictions — 20261012-1827-q-wiki-encounters-e8e3 (compiler run)

Written before the page is finalized. This is a compile, not an experiment; the
held-out cases are what an independent checker will find when auditing the page
against the raw runs. No new probe was needed: no two encounters runs contradict
each other unresolved (the three silver/gold pairs that conflict — 969a/5d90,
136a/ca96, 9834/5c16 — are each resolved by their own second checker).

- **P1 (partition).** Of the 65 clustered runs, 51 are encounters-tier runs and
  will appear on the page: 18 gold, 29 silver, 4 lead. 9 route to other topics
  with graded records (5 kick-cadence, 1 gravity-news, 1 b12-statistic,
  1 memory-h-live, 1 frame-cost); 5 have no graded record (2 VOID r8-v4 rungs
  that belong to coorbital-cert, 3 dead branches).
- **P2 (existence and grade).** Every run id on the page exists as
  `origin/claude/lab-<id>` with a `check.md` whose `Grade:` line matches the
  page's grade exactly.
- **P3 (faithfulness under sampling).** If the checker samples any five in-text
  claims, every number in them appears verbatim (or as the checker's own
  corrected value, where the second checker corrected the author) in the cited
  run's `check.md` or `dossier.md`.
- **P4 (no cross-page collision).** No run on this page appears on the
  `coorbital-cert` page's run list (compiled 20261012-1715), and no claim here
  contradicts its standing results; the seam is explicit (χ_t routing and the
  crossing-fleet ruin live here, the phase-neighbour certificate there).
- **P5 (regeneration).** `regen.sh` re-derives the partition, the grade tallies
  and the five sampled claim strings from the refs in under 15 minutes on this
  machine without network access.

What I expect could fail: P3 on numbers I rounded (I kept the cited runs' own
digits), and P1's boundary if the checker reads `20261009-1649-system-aa29`
(kick resonance gate ≡ CF pass) or `20261007-0933-system-0510` (synodic
calendar carries the kick) as encounters rather than cadence; both are
defensible either way, and the dossier names them.
