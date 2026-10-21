Working...
Check complete. `check.md` written: **Grade: silver**.

**What I did:**

1. **Reproduced** — ran `regen.sh` twice (runner's log and my own): identical PASS. Then re-derived everything independently, bypassing the author's `verify.py` where it mattered: line counts (424/104, current best 244/8 via wiki.py's own rule), run retention (91 date-anchored old run lines → 56 distinct, 0 lost/extra/duplicated), and `lab/wiki.py index` run directly on a scratch copy (`open | 56`, no over-budget flag).

2. **Adversarial cases (4, one outside the author's domain):**
   - Independent token sweep with a different tokenizer (294/80 vs the author's 345/123): **every** missing token is a checker-arm, seed-level, battery or kill-table variant behind a kept run line — corroborates "zero lost supported numbers."
   - Qualitative sentence hunt (outside their numeric scope): all standing sentences traced to homes **except one** — 7fd3's named untried lever (basin-reuse exact fit) has no new home anywhere in the page.
   - Duplicate-collapse integrity + the 469c/461c twins; 22/55 run lines exceed the README's 20 words (inherited, not introduced).
   - Faithfulness of the long Current best lines: both sides kept in the compile-share adjudication, b6ef stated at its checker's −12…−22%, inference markers preserved.

3. **Found the grade-capping defect:** dossier and predictions claim "101 run lines / 45 duplicates" — the run's own audit regenerates **91 / 35** (101 counts every bullet on the page), and the wrong number was baked into the page's intro line. I corrected the page in place (permitted) and re-ran the audit: still passes. Also recorded: "second-worst offender" is false (8th by lines), and a cosmetic verify.py print bug.

4. **Novelty:** compile runs are an established pattern (three sibling q-compiles in the prior window, 2eb3 folded at silver); this is the first compile of frame-cost, which the wiki's own rule required before the page takes new runs — maintenance, not a mechanism, hence silver on the ledger despite clean execution. The named gold step: reconcile the frozen record's counts and give the basin-reuse lever a home or a refutation.
