# Predictions — 20261021-0213-second-20261021-0142-q-compile-promotion-e094-b327

Written before the decisive replays. The e094 checker's named gold experiment:
patch `wiki.py apply`'s Runs union to be id-aware (preferring the compiled
variant), push the promotion page through the real `apply` + `index`, record
the landed state (no flag, no duplicated ids). Setup already measured (not a
prediction): the shipped record at HEAD 046d8d9c carries 29/40 diseased pages,
468 duplicate Runs lines; promotion 32 lines / 14 ids / 13 duplicated ids.

Patches involved: `6ccc` = wiki-memory's +102/−10 (fold_runs, defuse/heal/skip,
LAB_WIKI sandbox hook; applies clean at HEAD, checked); `b327` = 6ccc + a
heal-on-skip extension (the skip rewrites ours' Runs with
`fold_runs(ours, [])` when it fires, instead of no-op'ing).

- **P1 (harness fidelity control).** Replaying e094's 02:12 first publish
  (ours = the page at its base 5c06c9cc, theirs = its graded proposal) through
  a *pristine* wiki.py in a sandbox lands `promotion.md` byte-identical to what
  commit 046d8d9c actually shipped. If not, my harness is wrong and everything
  below is VOID.
- **P2 (the literal named experiment, unpatched-publisher arm).** Re-presenting
  e094 to the *shipped* wiki.py on the diseased HEAD page is a no-op (its line
  is textually present, so the literal union appends nothing): 32 lines, 13
  duplicated ids stand. The disease does not heal and does not grow.
- **P3 (6ccc's patch alone does not heal it).** With 6ccc's skip
  (`continue` when the run's line is already present), re-presenting e094 is a
  no-op too — the named experiment's literal form heals nothing. This is the
  gap I close with the heal-on-skip extension.
- **P4 (the named experiment with the extension).** Re-presenting e094 through
  patched+extension `apply` + `index` heals promotion: Runs 32 → 14 lines, one
  per id, 0 duplicated; the healed Runs section is byte-identical to e094's
  compiled proposal's Runs section (the compiled variants are the later
  occurrences, so later-wins picks exactly them); body untouched; index row
  `open | 32` → `open | 14`; no over-budget flag before or after.
- **P5 (idempotence).** A second identical sweep is byte-identical (no further
  writes; fold of an already-folded list is a fixed point).
- **P6 (the whole 02:12 sweep heals, not just this page).** Staging all four
  graded runs of the 02:12 window (8179, 4c5b, e094, 9141) and running one
  patched `apply` + `index` — the publisher's exact invocation — heals every
  page that sweep compounded: promotion 32→14, budget-1e9 26→10 ids/lines,
  cell-rebind 11→4, kick-jet 92→~57, each byte-identical in Runs to its own
  compiled proposal, 0 duplicated ids anywhere in the wiki afterwards.
- **P7 (corpus bound, no loss).** Folding every page's own Runs list at HEAD
  (`fold_runs(page, [])`) clears all 468 duplicate lines across the 29
  diseased pages and loses **zero** run-id tokens (the set of ids appearing
  anywhere in each Runs section is unchanged, range lines included).
- **P8 (no index regression).** Patched `index()` on the untouched HEAD corpus
  is byte-identical to the shipped `index()` output (6ccc's claim, re-verified
  at HEAD); after the heal sweep only the four healed rows' run counts change.
- **P9 (the next real publish, mechanism replay).** Staging this run's own two
  proposed pages (b327, with a hypothetical `Grade: silver` DONE — the
  publisher only folds gold/silver; my real grade is not yet written) on top of
  the healed state lands promotion at 15 Runs lines (one per id, b327 added)
  and wiki-memory at one line per id, both under budget.

Kill criterion: any of P1, P4, P6, P7 failing kills the adoption claim for the
extension (P3 alone would kill only the "re-present heals" form, leaving
6ccc's next-publish heal standing — I would report it that way).
