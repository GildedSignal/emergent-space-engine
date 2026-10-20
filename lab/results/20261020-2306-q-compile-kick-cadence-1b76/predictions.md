# Predictions (written before the compile is verified)

The work: compile `lab/wiki/kick-cadence.md` (664 lines, current best 423) under the
wiki budgets (`## Current best` ≤ 15 non-blank lines, page ≤ 300 lines, `## Open
directions` ≤ 8, `## Runs` one line per run) into
`wiki/kick-cadence.md` in this run folder, losing no supported number: every number
either stays inline or sits behind a run id cited in the page for that claim.

These predictions are about the compiled page and the verification instrument
(`check_compile.py`), which I have not run yet. The instrument is written by me, so
the structural checks (P1, P2, P4) verify my own transcription as much as anything;
the held-out part is P3's inline rate — how many of the curated sample numbers I
actually carried inline versus legitimately left behind a cited run — and P5.

- **P1 (budgets).** The compiled page holds ≤ 160 total lines (my draft targets ~140)
  and `## Current best` = 12 non-blank lines (headline + 11 items). A scratch
  `lab/wiki.py index` run over a wiki copy with the page swapped in reports
  kick-cadence with no "over budget" flag and no conflict flag.

- **P2 (runs).** The old page's `## Runs` holds 64 lines but only 62 distinct run ids
  (20261016-1835-fermi-4093 and 20261019-1906-spacex-9edc each appear twice: a
  truncated "this run" placeholder plus the graded line). The compiled page keeps all
  62, one line each, in the original append-only order, with the five lines the old
  page left truncated mid-sentence (8ffc, 16ec, 9edc's placeholder, 225d, 4093's
  placeholder) completed from the runs' own records on the page above.

- **P3 (numbers, the held-out rate).** Of a fixed sample of 60 distinctive numbers
  drawn from every section of the old page (curated in `check_compile.py` before the
  first run), at least 45 appear verbatim in the compiled page, and all 60 are
  accounted for: inline, or explicitly mapped in the instrument to a run id that the
  page cites (the gold criterion's "behind a cited run"). I expect the inline rate to
  land 50–58/60; the deliberate "behind" set is small (checker-provenance arithmetic,
  digest hex strings, one-off derived constants), each mapped to the run that measured
  it.

- **P4 (faithfulness invariants).** Every `## Current best` line cites at least one
  run id; every `## Refuted` line names the run that killed or superseded the claim;
  no line in the compiled page states a number or claim that the old page does not
  carry (compilation adds ordering and compression, not physics). Predict 0 violations.

- **P5 (what would make it wrong).** Any sampled number neither inline nor behind a
  cited run, any budget exceeded, any run line lost, or any grade label changed beyond
  completing truncated placeholders (the one sanctioned edit: cca6's line gains its
  checker2 gold verdict, which the old page's own record states). If P1–P4 fail I fix
  the page before submitting; if the inline rate lands below 45/60 I re-balance
  Current best rather than shrink the sample.

Kill criterion for the run: the instrument must be able to fail — if I find myself
editing the sample list to make P3 pass, the run is void and I say so in the dossier.
