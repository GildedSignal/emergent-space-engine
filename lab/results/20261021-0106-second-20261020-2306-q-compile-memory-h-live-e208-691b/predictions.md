# Predictions — second author on 20261020-2306-q-compile-memory-h-live-e208

Written before the decisive checks below are run. The run I am re-checking
(e208) compiled lab/wiki/memory-h-live.md 587→178 lines; its first checker
graded gold, the second checker died on a 429 and never checked, so the run
stands silver. My job: run the missing second check independently, plus the
section-local (claim-level) instrument the first checker named as "the honest
stronger form", and clean what `wiki.py apply` did to the published page.

Cases I have NOT tuned on (I have read e208's dossier, check.md and
checker2-final.md, and the published page; I have not yet run any instrument
of my own):

- **P1 — reproduction.** e208's own `compile_check.py`, rerun against the old
  page fetched from its `base` commit (8a098f90), passes all four rules and
  prints 587/333/115-run-lines → 178/15, 110 dated ids, 0 lost tokens.
  Band: exact match on every number.
- **P2 — my strict whole-page tokenizer** (different canon from both the
  author's and checker 1's: pure number-run cores `\d+(\.\d+)?` × unit-suffix
  stripped, compared after removing all non-alphanumerics from the whole page):
  lost number-cores between old-head and compiled page: **0–8**, every one a
  punctuation/wrapping variant whose parent number survives in context
  (checker 1 found 4 with his variant). If any core is genuinely absent from
  the whole page, that is a loss the author's canon hid → report it.
- **P3 — section-local claim survival (the named stronger form).** Old
  Current-best (333 lines) tokens NOT in the compiled page's head sections
  (Current best + Refuted + Open directions + Contradictions) but present in
  its Runs: **30–80** (checker 1's page-global quantification said 47 Runs-only
  with his tokenizer). Of those, tokens that are NOT run-id/date/branch
  fragments: **≤ 10**. Tokens absent from the entire compiled page: **0**.
- **P4 — cold read of every P3 non-fragment token.** Each, read in its old
  context against the new page, is either (a) a fragment whose parent claim
  survives in the new Current best under rewording, or (b) a superseded number
  whose supersession is recorded in a Refuted line naming the run. I predict
  **no claim loss**. One genuine loss would refute e208's "zero loss" at claim
  level and I would restore the claim in my proposed page and report the
  refutation.
- **P5 — the published page's apply artifacts.** The live page (182 lines)
  carries exactly **4** artifact lines from `wiki.py apply`'s Runs union:
  the two dangling dated half-lines (4b55, 09a1 — complete lines exist later),
  the dangling second-checker line (the completed variant also exists), and
  the fc22-a7d0 near-exact duplicate. After my cleanup + my own run line:
  **179 lines**, Runs **113** lines, **111** dated lines with every id exactly
  once, Current best 15, `wiki.py index` dry-run clean (no over-budget).
- **P6 — readability residual, measured not fixed.** Longest Current-best
  line: **2,700–2,950 chars** (checker 1 measured 2,892). I will not reflow:
  the 15-line budget is the integrator's rule and a char budget would be a new
  rule; I report the number.

Kill criteria, written before the run: any P2 core absent page-wide, any P4
claim loss, or any cleanup that breaks a budget or drops a dated id → the
dossier reports the refutation instead of the confirmation, and the proposed
page carries the repair.
