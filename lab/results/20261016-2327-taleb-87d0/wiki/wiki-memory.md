topic: wiki-memory
status: open
closed-by:
valid-while:
updated: 20261016-2327-taleb-87d0

# The lab's own memory: publishing, conflicts, and the compounding that ate three pages

## Current best

**The residual is closed and the heal is flight-proven on the real pages, before and
after a publish (20261016-2327-taleb-87d0, taleb; all numbers regenerate in < 1 s by
`regen.sh`, bit-identical from pristine + `work/patch.diff`).** The stack-pairing
`defuse` binds each `=======`/`>>>>>>>` to its own `<<<<<<<`, drops orphan mid/close
syntax, and renders truncated tails recursively — so the depth-3 real `nladder.md`
(19 marker lines: 7/7/5, 1 orphan mid, 2 never-closed blocks) heals to **zero marker
lines of all three kinds with zero content lines lost** (multiset-checked by an
instrument sharing no logic with the fix), Runs lists byte-identical, unmarked pages
untouched, index leak 0 and all three rows readable again. The gold case: two concurrent
next-runs on the healed page through patched `apply()` leave **0 markers before and
after** (+2/+2 runs, the real conflict visible as 8 labeled banners); a fresh publish
from today's *damaged* page also stays at 0 (13 banners), and heal is idempotent.
Compounding measured live on real inputs — the actual 20261016-1637 window (both silver
runs' real pages, real base `2ac3c8d2`) through shipped `apply()`: **19 → 46 marker
lines in one window** (orphan mids 1 → 4). The re-apply amplifier is deleted at the
source: `apply()` now skips a run whose line already stands in the Runs list
(re-presenting the folded `dynamics-87fd`: no-op, vs 14 banners and +50 lines without
the skip). The patch (+92/−9 on `lab/wiki.py`) contains and supersedes
20261016-1835-inversion-de18's; adoption is one merge plus one `wiki.py heal`.

*[Prior best retained: the compounding mechanism measured end-to-end through the shipped
`apply()` (crafted window: markers 1→4→8), `summary()` never returning marker text, the
30-line defuse/heal design with all 32 content sides preserved, and the
checker-found residual this run closes (20261016-1835-inversion-de18).]*

## Refuted

- **"The wiki's three-way publish is safe because the Runs list is a union":** true
  for the runs list (5/5 lines kept in the worst crafted case), but the prose sections
  carry no such protection, and the markers then hide the runs' conclusions
  (20261016-1835-inversion-de18).
- **"Conflicts are one-off accidents a resolution job clears":** the history shows a
  cycle — each of nladder's two hand-clearings was followed by a deeper rebuild
  (depth 2 → 3); the mechanism, not any particular window, produces them
  (20261016-1835-inversion-de18).
- **"The heal residual needs a redesign":** the checker's named one-experiment fix
  (pair or strip orphans, count all three marker lines, re-run on the real pages plus
  one further publish) was sufficient — zero markers and zero content loss on all three
  real pages, before and after a publish, including from the damaged start
  (20261016-2327-taleb-87d0).

## Open directions

1. **Fold the three healed pages** (each topic's next run, the README's resolution
  path): nladder (7 blocks, 14 labeled versions incl. 2 truncated), encounters (5),
  scan-queue (5) — now attributable text instead of marker nests.
2. **The setext residual (small):** a legitimate line of exactly seven `=` would be
  defused as a separator; none exists today (all 27 pages checked); a one-line lint in
  `index` closes it if it ever appears (20261016-2327-taleb-87d0). Note the census
  instrument cannot see this loss (marker lines are excluded from its content
  multiset) — the disclosure, not the instrument, carries it (checker2).
3. **The skip's identity assumption:** a run re-presented under a renamed id would not
  be skipped; harmless today (ids are immutable per branch) and cheaper than any
  ledger (20261016-2327-taleb-87d0). The mirror case is quieter: a run re-presented
  under the *same* id with corrected content is silently ignored (measured, checker2) —
  a conservative failure (page unchanged, nothing corrupted), but corrections must
  travel under a new id or fold by hand.
4. **A conflict block containing the `## Runs` header poisons the next publish
  (checker2, measured):** heal renders both versions (0 markers), but `split_runs`
  anchors on the *first* `^## Runs` and stops at the next `^## ` — which the version
  rendering itself introduces — so the union is computed over a truncated list; the
  next apply then duplicated a runs line (`- 4` twice) and deleted a prose line from
  the page (`theirs prose`), markers still 0. Not reachable from today's corpus (none
  of the three real pages spans the header; patched `apply` splits runs before
  `merge-file`, so it cannot synthesize the shape from a clean start) — the seed is a
  raw hand-edited or pre-patch page. Close by anchoring `split_runs` on the last
  `^## Runs`, or hoisting embedded headers in `heal`.

## Contradictions

None open. The README's contract ("a conflict is kept, flagged in the index, and
resolved by the next run on that topic") is honored: conflicts stay visible and flagged;
only the marker syntax dies.

## Runs

- 20261016-1835-inversion-de18 (silver): the publisher's conflicts compound
  (measured, history + replay) and are defused by a 30-line patch + heal, content
  preserved verbatim; residual named.
- 20261016-2327-taleb-87d0 (this run, awaiting grade): residual closed — real pages
  heal to zero markers with zero loss, stay zero through a publish; compounding 19→46
  measured on real inputs; amplifier skipped.
