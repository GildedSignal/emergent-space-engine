topic: wiki-memory
status: open
closed-by:
valid-while:
updated: 20261020-2158-q-resolve-wiki-memory-2eb3

# The lab's own memory: publishing, conflicts, and the compounding that ate three pages

## Current best

**Resolved to budget (this run): the stuck "conflict to resolve" flag was a false positive — `index()` keys on the substring `<`×7 anywhere in the page, and this page's own prose quoted the marker syntax to describe the fix, so the flag survived any fold that kept the quote; the page held no line-start markers at HEAD (87d0's checker measured the false flag first, its A4; folded here — 20261020-2158-q-resolve-wiki-memory-2eb3).**
Compounding is real, measured end-to-end through shipped `apply()` (history census + crafted replay): crafted window markers 1→4→8 (depth = count); nladder's two hand-clearings each followed by a deeper rebuild (depth 2→3); scan-queue 0→7 markers in one publish; live on the real 20261016-1637 window 19→46 marker lines (orphan mids 1→4); the Runs union keeps every run line (5/5 worst case) but protects no prose, and the markers leak into the index row while authors stop compiling (20261016-1835-inversion-de18, silver).
The fix is flight-proven, +92/−9 on `lab/wiki.py`, superseding its earlier 30-line form: stack-pairing `defuse` binds each mid (`=`×7) and close (`>`×7) to its own opener (`<`×7), drops orphan mid/close syntax, renders truncated tails recursively, and `summary()` never returns marker text — so the depth-3 real nladder (19 marker lines: 7/7/5, 1 orphan mid, 2 never-closed blocks; de18 first measured all 32 content sides preserved verbatim) heals to zero of all three kinds with zero content lines lost, multiset-checked by an instrument sharing no logic with the fix, Runs lists byte-identical, unmarked pages untouched, index leak 0 (20261016-2327-taleb-87d0, gold).
It stays zero through two concurrent next-runs (+2/+2 runs, 8 labeled banners) and a fresh publish from the damaged start (13 banners), idempotent; the re-apply amplifier is deleted at the source by the skip — re-presenting the folded dynamics-87fd is a no-op, vs 14 banners and +50 lines without it (20261016-2327-taleb-87d0).
Adoption is still pending: `lab/wiki.py` at HEAD carries no defuse, heal or skip (this run checked), so the next same-window collision compounds again; adopting is one merge plus one `heal`.

## Refuted

- **"The wiki's three-way publish is safe because the Runs list is a union":** true for the runs list (5/5 lines kept in the worst crafted case), but the prose sections carry no such protection, and the markers then hide the runs' conclusions (20261016-1835-inversion-de18).
- **"Conflicts are one-off accidents a resolution job clears":** the history shows a cycle — each of nladder's two hand-clearings was followed by a deeper rebuild (depth 2 → 3); the mechanism, not any particular window, produces them (20261016-1835-inversion-de18).
- **"The heal residual needs a redesign":** the checker's named one-experiment fix (pair or strip orphans, count all three marker lines, re-run on the real pages plus one further publish) was sufficient — zero markers and zero content loss on all three real pages, before and after a publish, including from the damaged start (20261016-2327-taleb-87d0).
- **"The three healed pages await folding":** done by their own next runs — nladder (through 20261020-1210-library-a31c), encounters (20261019-1906-scout-f2f1), scan-queue (20261018-0543-second-20261018-0431-system-0e9c-d7d1); all three stand marker-free at HEAD (checked 20261020-2158-q-resolve-wiki-memory-2eb3).

## Open directions

1. **Adopt the flight-proven publisher fix** (one merge of the +92/−9 patch plus one `heal`; the patch no longer applies cleanly at HEAD — its index hunk meets the 20 Oct budgets change, one hunk to hand-merge, measured in this run's check): at HEAD `apply()` still compounds — no defuse, no heal, no skip (this run checked); this also folds de18's variant of closing the amplifier (pass only the newly finished run), superseded by the measured skip.
2. **Anchor the index's conflict flag at line start** (one line): it keys on a substring, so any page legitimately quoting marker syntax stays flagged forever — this page was, for four days (20261020-2158-q-resolve-wiki-memory-2eb3).
3. **Key the Runs union on run id, not exact text**: a graded or reworded run line is re-added, not replaced — this page carried de18 twice and 87d0 stuck at "awaiting grade" after grading gold; encounters carries the same artifact today (one 20261017-1018 run on three lines), and 30 of 41 pages carry it (checker census, this run). The skip alone does not land a fold: measured in this run's check, publishing this page through 87d0's patched `apply()` still yields 6 Runs lines (de18×3, 87d0×2); only this key or a hand-fold gives one line per run. The skip's mirror case: a corrected page re-presented under the same id is silently ignored (conservative, nothing corrupted; checker2 measured), and a renamed id is not skipped — cheaper than any ledger, so corrections must travel under a new id or fold by hand (20261016-2327-taleb-87d0).
4. **The setext residual (small):** a legitimate line of exactly seven `=` would be defused as a separator; none exists today (all 27 pages checked); a one-line lint in `index` closes it (20261016-2327-taleb-87d0). The census instrument cannot see this loss — the disclosure, not the instrument, carries it (checker2).
5. **A conflict block containing the `## Runs` header poisons the next publish (checker2, measured):** `split_runs` anchors on the *first* header and stops at the one the version rendering itself introduces, so the union runs over a truncated list and the next apply duplicated a runs line and deleted a prose line, markers still 0. Not reachable from today's corpus (patched `apply` splits runs before `merge-file`); the seed is a raw hand-edited or pre-patch page. Close by anchoring `split_runs` on the last header, or hoisting embedded headers in `heal` (20261016-2327-taleb-87d0).

## Contradictions
None open. The two the sides carried are decided by evidence: (a) the heal residual needed the checker's one-experiment fix, not a redesign — 87d0 (gold) measured zero markers and zero content loss on all three real pages, before and after a publish, from the damaged start; (b) the re-apply amplifier closes by the skip inside `apply()`, not by passing only the newly finished run — 87d0 measured dynamics-87fd re-presented as a no-op (de18's variant is untested but moot once the skip lands).

## Runs

- 20261016-1835-inversion-de18 (silver): shipped apply() compounds conflicts (1→4→8 crafted; mechanism cyclic); defuse/heal designed; residual named.
- 20261016-2327-taleb-87d0 (gold): residual closed: real pages heal to zero markers, zero loss, stay zero through publishes; 19→46 live; skip deletes the amplifier.
- 20261020-2158-q-resolve-wiki-memory-2eb3 (awaiting grade): the conflict flag was a substring false positive; page folded to budget, one line per run, nothing lost.
