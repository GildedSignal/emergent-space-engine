topic: wiki-memory
status: open
closed-by:
valid-while:
updated: 20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc

# The lab's own memory: publishing, conflicts, and the compounding that ate three pages

## Current best

**Landed end-to-end (this run): 87d0's flight-proven +92/−9 patch hand-merged at HEAD (its one index hunk meets the 20 Oct budgets commit; the other four apply clean) plus the id-keyed Runs union (`fold_runs`: one line per run, a re-graded or reworded line replaces its stale variant) — and the real publisher then lands the resolved page itself, so no integrator hand-fold is waiting (20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc).**
Replaying 2eb3's actual silver publish (ours = the page at its base 9bf31c70, theirs = its graded proposal) through the patched `apply()` lands exactly 3 Runs lines — one per id, de18 (silver) and 87d0 (gold) wordings standing — with the body above `## Runs` byte-identical to what the shipped publish landed, 0 marker lines of all three kinds, no unmerged banner, index row `| open | 3 |`, neither flag (this run).
Idempotent: re-publishing the same run is a byte-identical no-op (the skip); the next publish (a new run's page for the topic) appends its own line (4, one per id) and its corrected 2eb3 line ("silver" for "awaiting grade") replaces the stale variant instead of being re-added beside it — the exact artifact that grew this page to 6 lines under the shipped exact-text union (this run).
Controls: the same replay through pristine HEAD `wiki.py` reproduces the shipped landing bit for bit (6 lines: de18×3, 87d0×2, 2eb3×1), and the patched `index()` on the current corpus is byte-identical to the shipped index — no regression, the false-positive mode included (the flag now anchors at line start and keys on the unmerged banner) (this run).
Corpus ceiling: 29 of 40 pages carry duplicate run ids today (391 duplicate lines; worst nladder 143, encounters 65); folding each page's own Runs list on id clears every page with no id lost — every topic self-heals at its next publish (this run).
Adoption: `git apply` this run's `work/patch.diff` (+102/−10 on `lab/wiki.py`; 87d0's defuse/heal/skip verbatim, one hand-merged hunk, plus `fold_runs`); `heal` included, a no-op on today's corpus. Until it lands, main still compounds — the 19→46 ladder is one same-window collision away (20261016-2327-taleb-87d0).

## Refuted

- **"The wiki's three-way publish is safe because the Runs list is a union":** true for keeping lines, but the exact-text union re-adds stale variants (de18×3, 87d0×2 stood on this page) and the prose sections carry no protection at all; the markers then hide the runs' conclusions (20261016-1835-inversion-de18; measured 20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc).
- **"Conflicts are one-off accidents a resolution job clears":** the history shows a cycle — each of nladder's two hand-clearings was followed by a deeper rebuild (depth 2 → 3); the mechanism, not any particular window, produces them (20261016-1835-inversion-de18).
- **"The heal residual needs a redesign":** the checker's named one-experiment fix was sufficient — zero markers and zero content loss on all three real pages, before and after a publish, including from the damaged start (20261016-2327-taleb-87d0).
- **"The three healed pages await folding":** done by their own next runs — nladder (20261020-1210-library-a31c), encounters (20261019-1906-scout-f2f1), scan-queue (20261018-0543-second-20261018-0431-system-0e9c-d7d1); all three stand marker-free at HEAD (checked 20261020-2158-q-resolve-wiki-memory-2eb3).
- **"Landing the fold needs an integrator hand-merge or a corrected publisher first":** refuted — with the patch at HEAD the shipped publisher itself lands one-line-per-run through its own `apply()`, measured on the real publish (20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc).

## Open directions

1. **Adopt the landed patch** (`git apply` this run's `work/patch.diff`, +102/−10, then `wiki.py apply`/`index` as usual): the defuse/heal/skip flight (87d0), the line-start flag anchor and the id-keyed union (this run) all live in it; until then HEAD still compounds and the flag can still false-positive on quoted syntax.
2. **The setext residual (small):** a legitimate line of exactly seven `=` would be defused as a separator; none exists today (all pages checked); a one-line lint in `index` closes it (20261016-2327-taleb-87d0).
3. **A conflict block containing the `## Runs` header poisons the next publish:** `split_runs` anchors on the *first* header; not reachable from today's corpus (patched `apply` splits runs before `merge-file`); close by anchoring on the last header or hoisting embedded headers in `heal` (20261016-2327-taleb-87d0).

## Contradictions
None open. The two the sides carried are decided by evidence: (a) the heal residual needed the checker's one-experiment fix, not a redesign — 87d0 (gold) measured zero markers and zero content loss on all three real pages, before and after a publish, from the damaged start; (b) the re-apply amplifier closes by the skip inside `apply()`, not by passing only the newly finished run — 87d0 measured dynamics-87fd re-presented as a no-op.

## Runs
- 20261016-1835-inversion-de18 (silver): shipped apply() compounds conflicts (1→4→8 crafted; mechanism cyclic); defuse/heal designed; residual named.
- 20261016-2327-taleb-87d0 (gold): residual closed: real pages heal to zero markers, zero loss, stay zero through publishes; 19→46 live; skip deletes the amplifier.
- 20261020-2158-q-resolve-wiki-memory-2eb3 (silver): the conflict flag was a substring false positive; page folded to budget by hand; the publish-path hazard measured.
- 20261020-2306-second-20261020-2158-q-resolve-wiki-memory-2eb3-6ccc (awaiting grade): patch hand-merged at HEAD, Runs union keyed on run id; the real publisher lands the fold; idempotent.
