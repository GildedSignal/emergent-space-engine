# Predictions (written before the decisive verifier and apply demonstration)

The three named gaps in the checker's verdict, and what I expect before running.

## P1. The honest sweep (fix the unit of sweep: paragraphs, not only `- ` bullets)

The old page's `## Current best` is eight `**…` prose paragraphs (0 bullets), so the
original verifier's 109-token tally covered `## Refuted` alone. With every non-blank
line of both sections as the unit:

- total multi-digit tokens: ~500–560 (checker's own re-sweep: 535);
- in-page verbatim: ~70–80% (checker: 419 of 535);
- behind a cited run: the rest (checker: 116);
- **LOST: 0** — the compile's substance claim survives the honest instrument;
- grade-token edits change no number token, so the tally on my corrected page
  equals the tally on the original compiled page.

## P2. Grade refresh (7 stale tokens, from the run branches' `Grade:` commits)

Pre-audit already read (this is the one lookup done before writing this file):
061f/7d2b/de99/c4d3 say "silver" on the page, branch says gold; a765 "awaiting
grade" → gold; ceb2 "awaiting grade" → silver; d65c "second author, awaiting
grade" → gold. Prediction:

- exactly these 7 lines are stale; every other of the 57 tokens already carries
  its branch grade (or the branch is absent locally, e.g. df81, and the token
  already says gold — no understatement possible);
- after refresh: 0 tokens understating a locally-known branch grade;
- no grade *regresses* (no silver→awaiting, no gold→silver).

## P3. Adoption through the real tool (id-aware Runs fold in `lab/wiki.py apply`)

`apply()` line 129's union is literal: `ours + [theirs not in ours]`. With a
`fold_runs(theirs, ours)` (one line per run id, the run's variant winning a
collision), driving the **real** `lab/wiki.py` in a sandbox:

- **Historical control (unpatched HEAD code):** ours = the 444-line page at
  624c4a51, base = 624c4a51, theirs = the original compiled 107-line page →
  reproduces **byte-for-byte** the page now on main (135 lines, 85 raw run
  lines, 57 distinct, 28 duplicate excess). If not byte-identical, the control
  fails and I report the diff.
- **Historical, patched:** same inputs → 107 lines, 57 run lines, 0 duplicate
  ids, and the landed page equals the compiled page the run actually wrote.
- **Forward, patched:** ours = main's current 135-line page, base = 5c06c9cc
  (this run's start), theirs = my corrected page → lands my page exactly:
  107 lines, 57 distinct, 0 dupes; `wiki.py index` on the sandbox reports the
  kick-jet row open, no conflict, no over-budget flag (135 was already under
  both budgets — the inflation was Runs hygiene, not a flag).
- The patch touches only the Runs union; body three-way merge paths are
  unchanged, so no other page's merge semantics change beyond deduplication.

## What would falsify the whole thing

Any LOST token under the honest sweep, a byte-diff in the unpatched control
against main's page, a stale grade remaining after refresh, or the patched
apply losing/inventing a run id.
