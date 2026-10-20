# Predictions — 20261020-2158-q-compile-nladder-e7d0 (compile `nladder` under budget)

Written before the decisive run of `compile.py` (the page build + audits). The
old page is `lab/wiki/nladder.md` at HEAD 9bf31c70 (201,305 bytes, 1,751 lines,
`## Current best` holding 1,423 non-blank lines by `lab/wiki.py`'s own counter —
the index's flag).

- **P1 (budget).** The compiled page lands ≤ 300 total lines with `## Current best`
  ≤ 15 non-blank lines, measured by re-implementing `lab/wiki.py index`'s counting
  on the output (not by eye). Prediction: ~170 total, 15 current-best.
- **P2 (runs).** The old `## Runs` holds 186 lines over 100 distinct run ids
  (38 ids duplicated by re-appends). The compiled page keeps exactly 100 lines —
  one per id, none dropped — preferring each id's graded, complete line.
  Grade annotations refreshed from the run branches via the wiki's own rule
  (`git log origin/claude/lab-<id>`): prediction 67 silver, 29 gold, 4 unresolved
  (03f4's branch is not published at writing time).
- **P3 (no supported number lost).** A fixed sample of 30 load-bearing numbers from
  the old page's standing results: each appears in the new page, or its carrying
  run line is kept verbatim (the run's branch holds the rest). Prediction: ≥ 28/30
  appear in the new page itself; zero lost.
- **P4 (truncated run lines).** Five run lines end mid-sentence on the old page
  (4fa8, 1a1c, 917c, 7fcf, 7581). Each is completed from its own branch dossier
  or its own entry text; no other run line is reworded beyond its grade token.
- **P5 (the live wiki untouched).** `compile.py` writes only inside
  `lab/results/20261020-2158-q-compile-nladder-e7d0/`; `lab/wiki/` is read-only
  to this run (publishing merges `wiki/<topic>.md` three-way; it is not mine to edit).
- **P6 (kill criterion).** If any audited number in P3's sample is absent from the
  new page AND from every kept run line, the compile has dropped a supported number
  and the run is void until fixed — the audit must exit non-zero.
