# Predictions — 20261015-2041-inversion-398f (inversion)

Question: the seam→ALL direction's memory win (8b89: standing arcs → doll centres, rss
979→20 MB) was measured at cuts ≤ 20k game-s — at most one settle wave. The retained
per-body history (`VecDeque<Segment>`, the record stack; pruned by `key_prune` at
`until + 2·light_distance + 2²⁶` ticks) is the only per-body term that can grow with play.
Does it saturate or grow without bound, per body class, at depth? (Failure path: "memory
that grows with play" — the adoption sentence currently being closed cannot be certified
by any single-cut flight.)

Instrument: 8b89's patch + a 15-line census (`history_census`, `plan_census`) printing, at
the canonical cut, per-body history segments (total/mean/max) and plan items. Base anchors
reproduced first: 10⁴ coast ctl digest `5e8c9e24…5fbab6f`, ALL identity at 20k (done,
pre-ladder).

Arms: belt = `10000 coast <cut> 1 1000` (ctl + all); comets = `100 stargraze <cut> 3 1000`
(ctl + all). Cuts span ≥ 2 settle waves (first settle ≈ 26–28k game-s).

Registered predictions, before any deep flight:

- **P1 (belt, all): history saturates.** At cuts 32k/48k/96k, segments/body ≤ 2 and
  bytes_per_body stays within ±15% of the 20k value (1,004). The prune bounds it because
  belt rekeys are frequent (every settle) and `until` ends promptly. If segments/body grows
  past 3 by 96k, P1 fails.
- **P2 (comets, all): the record stack does NOT saturate — the inversion's kill test.**
  Segments/body at 64k ≥ 1.5× the 32k value (d6ba's checker: 474 B/body ≈ 3.5 segments at
  32k on the seam; the comet's window outer edge at 2×r0 makes `until` outlast any cut, so
  `key_prune` never fires and the stack is unbounded). If segments/body at 64k ≤ the 32k
  value + 1, P2 fails and the record stack is bounded on this class too.
- **P3 (digest): ALL identity holds at depth on both classes** (the re-mint record
  stays sufficient after ≥ 2 settle waves). Any mismatch kills the deletion outright.
- **P4 (ctl control): the ctl record stack also grows on comets** (never-demote keeps
  Live arcs, but history still accumulates segments) — if ctl saturates where all grows,
  the growth is the deletion's doing, not the class's.
- **P5 (bill): passage promotions on stargraze-all grow ~linearly with cut** (each settle
  wave re-mints every demoted passage at ~300–600 µs) — reported, not judged.

Kill criteria: P3 mismatch = the deletion dies. P2 confirmed (unbounded stack) = the
adoption sentence "closed in one flight" is refuted: no single-cut flight can certify
memory that grows with play; the record stack needs a bound before ALL ships. P1+P2 both
saturating = the worry closes with numbers, and the adoption's memory claim extends to
depth.
