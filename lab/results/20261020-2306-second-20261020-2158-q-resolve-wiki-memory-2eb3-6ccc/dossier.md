# Dossier — 20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc

## Claim

The checker's named gold experiment is done: 87d0's flight-proven +92/−9 patch is hand-merged at HEAD (its one index hunk; the other four apply clean) with the Runs union keyed on run id, and the real publisher then lands the wiki-memory fold by itself — one line per run, zero markers, both flags clear, idempotent on re-publish — so adoption is exactly `git apply work/patch.diff`, no integrator hand-fold.

## Bottleneck

The lab's memory, as the prior run. The exact-text Runs union is the last measured compounding source on this page: it grew the silver publish to 6 Runs lines (de18×3, 87d0×2), and it stands on 29 of 40 pages today (391 duplicate lines; nladder 143, encounters 65). Keying it on run id deletes every duplicate at each topic's next publish (corpus ceiling 1194→803 Runs lines), and the line-anchored flag kills the false-positive mode that stuck this topic for four days.

## Evidence

All numbers regenerate by `bash lab/results/20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc/regen.sh` (< 1 s; 17/17 checks pass):

- **S1, the merge:** 87d0's raw +92/−9 fails `git apply --check` at pristine HEAD exactly at `lab/wiki.py:83` (one hunk rejected, the other four apply — the checker's measurement); the hand-merged patch (`work/patch.diff`, +102/−10: 87d0's defuse/heal/skip verbatim, the flag anchored by `has_markers` around the 20 Oct budgets lines, plus `fold_runs`) applies cleanly to pristine HEAD.
- **S2, the named flight:** 2eb3's actual silver publish replayed through the patched `apply()` (ours = the page at its base 9bf31c70, theirs = its graded proposal, base = the same commit) lands **exactly 3 Runs lines, one per id**, the graded wordings standing (de18 silver, 87d0 gold; both stale variants gone), the body above `## Runs` **byte-identical** to what the shipped publish landed, 0 marker lines of all three kinds, no unmerged banner, index row `| open | 3 |` with **neither flag**.
- **S3, idempotent:** applying the same run again is a byte-identical no-op (the skip); index row unchanged.
- **S4, the next publish carries a correction:** a following run's page for the topic (this run's) lands as **4 Runs lines, one per id**, and its corrected 2eb3 line ("silver" for "awaiting grade") **replaces** the stale variant instead of being re-added beside it — the exact case that grew the page to 6 lines under the shipped union. The sim's DONE grade is a stand-in "silver" (the gate checks membership in {gold, silver} only); the true grade arrives at real publish time.
- **S5, negative control:** the same replay through pristine `HEAD:lab/wiki.py` reproduces the shipped landing **bit for bit** (6 lines: de18×3, 87d0×2, 2eb3×1) — the replay is the real publish.
- **S0, no-regression control:** the patched `index()` on the current corpus is byte-identical to the shipped index.
- **S6, corpus ceiling:** 29 of 40 pages carry duplicate run ids (391 duplicate lines); folding each page's own Runs list on id clears every page with no id lost.

## Predictions

`predictions.md` was written before the decisive instrument `second_check.py` ran. All six held: P1→S1, P2→S2a–e, P3→S3, P4→S4a–c, P5→S5, P6→S6 (P6's count matched: 29 pages ≥ 25 predicted).

## What would make it wrong

The union would be wrong if a page legitimately needed two lines for one run id — the README's schema says one line per run, and S6 shows the fold loses no id anywhere. The landing would be wrong if the three-way body diverged from what shipped `apply()` produces — S2c and S5b assert byte-identity in both directions. Adoption would need re-merging if main moves `wiki.py` again (one hunk, as here). The checker's one caveat stands: the patch is proven at HEAD, not adopted on main.

## Cost of adoption, fit

One `git apply` of this run's `work/patch.diff` (+102/−10 on `lab/wiki.py`), then publish as usual (`heal` included; a no-op on today's corpus). Nothing else changes: S0 proves `index()` output is byte-identical until a publish touches a page. Fits PRINCIPLES #1 (*the cheapest compute is compute not done… delete before optimizing*: 391 duplicate Runs lines die) and #13 (*errors never compound*: the exact-text union and the substring flag were the two one-line compounding sources the topic had left, both closed at the source).

## The lens

A second-author lens executes the named experiment faithfully; what it may miss is what the experiment did not name — the two residuals 87d0 left open (a line of exactly seven `=`; a conflict block containing the `## Runs` header), kept as open directions on the page, and any preference the integrator may hold for de18's superseded variant of closing the amplifier.
