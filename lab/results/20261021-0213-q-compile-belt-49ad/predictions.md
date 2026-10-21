# Predictions (written before the audit runs)

The work is a compile, not a new measurement: `lab/wiki/belt.md` (162 lines,
current best 69 non-blank) rewritten under budget. The decisive experiment is the
audit script `check_compile.py`: it re-derives the budget exactly as `lab/wiki.py
index` does, then checks that every digit-bearing token of the old page survives
somewhere in the new page, that the 19 `## Runs` lines are byte-identical, and
that every run-id citation resolves. I wrote the new page by hand before running
it, so the audit is a genuine test of my transcription, not of the script.

1. **Budget.** The new page passes both flags: current best ≤ 15 non-blank lines
   (I count 11 as written) and ≤ 300 lines total (I count ~75).
2. **Token survival.** The old page carries ~230 digit-bearing tokens (excluding
   bare single digits). Prediction: ≥ 230 survive verbatim; at most 3 misses on
   the first run, all punctuation-attached trivia (a stray en-dash range, a
   superscript form), 0 substantive number losses. Any substantive miss I fix and
   disclose in the dossier.
3. **Runs.** The 19 run lines are copied verbatim, so set-equality passes exactly,
   and every `2026MMDD-HHHH` citation prefix in the new prose resolves to one of
   them.
4. **Structure, held to the schema** (lab/wiki/README.md): the five sections in
   order; `## Current best` holds numbers standing now with domain; superseded
   claims moved to `## Refuted` one line each (9 old + 1 new: the frozen program
   as a store-and-forget object, superseded by the phase-locked program);
   `## Contradictions` keeps only the reconciliation note (nothing unresolved);
   open directions re-ranked by board row.
5. **What would falsify the compile:** a supported number that appears nowhere in
   the new page and whose cited run branch cannot regenerate it; or a budget line
   still over 15. The risk spots I cannot rule out by eye are the long
   `second-…` run ids and the Unicode forms (2²⁰, 10⁻¹⁸, e₀, ×, en-dash ranges);
   the audit checks those mechanically.
