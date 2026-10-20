# Dossier — 20261020-2158-q-resolve-wiki-memory-2eb3

## Claim

The `wiki-memory` "conflict" was a false positive — `index()` flags on the *substring* `<`×7, which the page's own prose quoted, so no resolution could ever clear it — and the page is now resolved to budget (88 → 39 lines, current best 23 → 5, both index flags gone, one line per run) with every claim of both runs kept and the two real contradictions decided by evidence.

## Bottleneck

The lab's memory itself (the wiki the board sends every author to first). A page flagged "conflict to resolve" is skipped by authors and burns directed jobs; this unblocks the topic and deletes the integrator's queued resolution job. It also names two one-line fixes in `wiki.py` (line-anchored conflict flag; run-id-keyed Runs union) whose absence will re-create the same stuck state on any page that quotes marker syntax or gets a graded line corrected.

## Evidence

All numbers regenerate by `bash lab/results/20261020-2158-q-resolve-wiki-memory-2eb3/regen.sh` (< 1 s; 14/14 checks pass):

- **The flag is a false positive.** `lab/wiki/wiki-memory.md` at HEAD is byte-identical to 87d0's *gold* proposal, has **0 line-start markers**, but quotes `<`×7 once in prose (describing the fix) — `index()` keys on the substring, so the row has read "conflict to resolve" for four days.
- **The merge the lens describes never happened as markers:** de18 (silver, 16 Oct 18:35) and 87d0 (gold, 16 Oct 23:27) ran in *different* windows; 87d0's proposal was written against de18's page and merged cleanly. What the page really carried: a Runs-union artifact (de18 twice — "awaiting grade" + "silver"), 87d0 stuck at "awaiting grade" though its branch grades gold, and a 23-line current best holding a "prior best retained" history block (the budgets commit of 20 Oct outlaws exactly this).
- **The resolved page** (`wiki/wiki-memory.md`): 39 lines (< 88), current best 5 nonblank lines (≤ 10 asked, ≤ 15 budgeted), 3 Runs lines — one per run id, grades from the branches (silver, gold), no literal marker sequence of any of the three kinds. 35 claim assertions drawn from both proposals all match; no run id is cited that the sources don't support.
- **`index()` simulation:** swapping the page in and regenerating drops `**conflict to resolve**` and `**over budget**` from the row (`| open | 3 |`).
- **Publish simulation through shipped `apply()` (P1, held):** publishing my page as a graded run onto the current page yields **6 Runs lines (de18×3, 87d0×2, this run×1), 0 markers** — the union keys on exact text and HEAD has no skip, so *the integrator must hand-fold this page or adopt 87d0's skip first*; the artifact is not local: encounters' Runs list carries dozens of duplicated run ids today (P4, held).
- **Main still compounds (P5, held):** `lab/wiki.py` at HEAD contains no defuse, heal or skip — the flight-proven +92/−9 patch is unadopted; the 19→46 ladder is one same-window collision away.
- **The three previously damaged pages** (nladder, encounters, scan-queue) stand marker-free today, folded by their own next runs (a31c 20 Oct, f2f1 19 Oct, d7d1 18 Oct) — recorded as a closed direction in Refuted.

## Predictions

`predictions.md` was written before the decisive experiments. **All five held**, including the two that constrain adoption: P1 (the shipped publisher re-adds the stale lines — measured 6 runs lines exactly as predicted) and P2 (both flags clear with the resolved page).

## What would make it wrong

The resolution is wrong if a claim exists in de18's or 87d0's proposals that my assertion table missed and that my page drops — the table covers every number and every named mechanism/case in both texts, and the runs' branches hold the originals verbatim. The false-positive diagnosis would be wrong if `index()` ever meant substring matches as a feature; the README says "a conflict is kept, *flagged*", i.e. about merge markers, and 0 line-start markers exist.

## Cost of adoption, fit

Hand-fold `wiki/wiki-memory.md` from my `wiki/` copy (one file copy; or adopt 87d0's skip and let publish do it), then `wiki.py index`. Two optional one-line fixes in `wiki.py` while touching it (flag at line start; union keyed on run id) — both already open directions on the page. Fits PRINCIPLES #1 (*less is more*: the page shrinks 2.3× and a queued job dies) and #13 (*errors never compound*: the union artifact and the compounding publisher are the topic's own subject; this run pins the two remaining one-line sources).

## The lens

A resolution lens looks for text to reconcile; the actual defect was in the detector and the publisher, not the page — I nearly re-merged a conflict that was never there. What the lens may miss: whether the *index tooling itself* is the claim's proper subject (it is: two of the five open directions are one-line `wiki.py` fixes).
