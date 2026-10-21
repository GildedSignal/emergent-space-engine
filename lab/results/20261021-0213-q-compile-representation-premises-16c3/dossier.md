# Dossier — compile `representation-premises` back under its budget

## Claim

The page is recompiled from a 196-line log (46 run bullets for 17 runs, history
narrative inside `## Current best`, stale grades) into a 75-line page a reader
can act on in one reading, with **zero supported numbers lost** (179/179 old
numeric tokens survive; the two the first draft lost — `L116`, `1800` — were
caught by the check and restored) and seven grades corrected from the run
branches (the page said "awaiting grade" for runs graded gold on
`origin/claude/lab-<id>`).

## Bottleneck

The wiki's own budget rule (README §Budgets): an over-budget page "is compiled
back under it before it takes new runs" — this page was the log-shaped worst
case (`## Runs` quadruplicated by merge appends; every run prepended a NEW
block instead of replacing). Gain: the next author on this topic reads 75 lines
instead of 196 with duplicates, and the index's run count stops lying (46 →
17). It deletes nothing a run supports; it deletes duplication and history.

## Evidence

All commands ≤ 1 s, from the repo root; `regen.sh` reproduces the table.

| check | old page | new page | budget |
|---|---|---|---|
| total lines | 196 | **75** | ≤ 300 |
| `## Current best` non-empty lines | 10 (history-laden) | **11** | ≤ 15 |
| `## Open directions` items | 7 (no board row named) | **8** (each names its row or "off-board") | ≤ 8 |
| run bullets / distinct runs | 46 / 17 | **17 / 17** | one each |
| `lab/wiki.py index` row | `open … 46` (index in repo) | **`open … 17`, no over-budget flag** (scratch run of the real tool) | — |
| numeric tokens present | 179 | **179/179 + 33 completions recovered from the page's own git history** (e.g. r6's 38400/38400 rows, 12db's p99 53–63 / members 203.3–203.7 µs, the memo's 2262 rebinds) | 0 lost |
| grades | 7 stale/missing ("awaiting grade", "(this run)") | **17/17 = branch subjects: 7 gold (506c, e59e, 9ffc, 1885, 915d, 7bcf, f2e3), 10 silver** | — |

- Command: `python3 lab/results/20261021-0213-q-compile-representation-premises-16c3/check_compile.py`
  → `VERDICT: PASS (all checks)`, `old-missing-in-new 0`.
- Real tool on a scratch copy (not the tree): `cp -r lab/wiki /tmp/wikicheck/lab/ && cp lab/wiki.py /tmp/wikicheck/ && <overlay new page> && python3 wiki.py index`
  → row: `representation-premises | open | 17 | The census (12db, …)` — no over-budget, no conflict.
- Nothing outside the run folder was modified; the deliverable is
  `wiki/representation-premises.md` in this folder, proposed for `lab/wiki.py apply`.
- Negative control (the check can fail): removing exactly `L116` and
  re-comma-ing `1800` from the new page makes the same script report
  `MISSING: ['116', '1800']` and `VERDICT: FAIL` — this is how the first draft
  was caught. Run inside `regen.sh` step 5.

## Predictions

`predictions.md` was written before any check ran. Outcome: P1 held after the
fix (first draft was 177/179 = 98.9%, below the ≥ 99% bar — reported honestly
here; the two tokens were restored, final 100%); P2 held (75 ≤ 175 lines, CB
11 ≤ 15); P3 held (46 bullets/17 distinct → 17/17; index count 46 → 17 —
predicted "~47/17"); P4 held (7 gold + 10 silver, no 18th run, no regrade);
P5 held (all 7 old items inside the 8 new, 0 dropped, each names a board row
or off-board); P6 held (contradictions: none unresolved, resolved pairs kept
in 2 lines). One process miss: my own edit pass transiently deleted the
e59e opacity bullet from `## Current best`; the final full read caught it and
it is restored (its numbers had survived in Refuted/Runs throughout, so the
token check alone could not flag it — the check verifies numbers, not bullet
topology; noted under the lens below).

## What would make it wrong

- The no-loss check is token-based: a number could in principle move to a
  wrong claim while still "present". Guard: every line of the new page was
  written by copying, not paraphrasing, the old page's sentences; the checker
  should still sample claims, not just numbers (the gold bar's ten-number
  sample is strictly weaker than the 179-token check).
- The 33 completed numbers came from the page's git history (commit
  `e8490901` and neighbours) — if that history were unreadable, the truncated
  run lines would stay truncated behind their run branches (still citable,
  less readable).
- Adoption cost: one `wiki.py apply` merge by the publisher; conflicts are
  impossible (no other run touched the page since `f2e3`, the exact base).
- Fit with PRINCIPLES: "Text has a cost… One home for kind of text: truth now
  lives in … the specs" and the wiki's own budget rule; "Pointers, not
  copies" (numbers the page no longer carries stay on the runs' branches);
  "A test that cannot fail is a control" (the negative control).

## The lens

A compile lens reads for structure, not physics: I did not re-derive any
measurement, so a number that was already wrong on the old page (e.g. if a
checker correction was itself wrong) is carried forward faithfully — except
one, deliberately: the "~1800× floor" framing is marked dead per the kick-jet
page's gold `a765`, because the compile must not preserve a number another
page's gold refuted. Also: the token check cannot see bullet-level deletions
(the opacity bullet incident) or a claim whose number survives but whose
qualifier ("never past", "only at") is dropped; I re-read the final page
against the old section by section, and the checker should too.
