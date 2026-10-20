# Predictions (written before the decisive experiments)

The lens asserts the page carries an unresolved three-way marker conflict. I have
already established (fact-gathering, git + scratch `index()`): HEAD's page is
byte-identical to 87d0's gold proposal, has zero line-start markers, and the index
flag reproduces from the substring `<`×7 quoted in prose. Below are the untested
cases; `resolve_check.py` decides them mechanically.

- **P1 (publish simulation):** pushing my resolved page through the *shipped*
  `apply()` (as a graded run, base = HEAD) re-adds the current page's three stale
  Runs lines — the union keys on exact text and HEAD has no skip — so the merged
  Runs list grows to ≥ 5 lines with de18 and 87d0 each duplicated. Consequence: this
  fold must be hand-applied by the integrator or preceded by adopting 87d0's skip;
  the resolved page stays the faithful target either way.
- **P2 (flag mechanism):** swapping my page in and regenerating the index drops both
  flags ("conflict to resolve" and "over budget") from the wiki-memory row, because
  my page quotes no marker sequence and comes in under budget (current best ≤ 10
  nonblank lines, whole page < 88 lines).
- **P3 (coverage, nothing lost):** every claim assertion extracted from de18's and
  87d0's proposals matches my page (or is listed as superseded with its deciding
  run); my Runs list holds exactly one line per run id {de18, 87d0, this run}.
- **P4 (the artifact is not local):** at least one other page in `lab/wiki/` carries
  the same union artifact today (same run id on two or more Runs lines). I expect it
  on encounters.
- **P5 (main still compounds):** `lab/wiki.py` at HEAD contains no `defuse`, `heal`,
  or skip logic — the flight-proven patch is unadopted, so the next same-window
  collision compounds again (the 19→46 ladder is one publish away).
