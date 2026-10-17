topic: wiki-memory
status: open
closed-by:
valid-while:
updated: 20261016-1835-inversion-de18

# The lab's own memory: publishing, conflicts, and the compounding that ate three pages

## Current best

**The publisher's conflict handling compounds and has eaten the lab's two most-run
pages: `wiki.py apply` writes `git merge-file` markers into the page (nesting deeper
on every unresolved publish; nladder's history shows two full conflict→hand-resolution→
rebuild cycles ending at nesting depth 3, and scan-queue went 0→7 markers in one
publish), the markers leak into `index.md` as the topic's "Current best", and authors
stop compiling the page ("prior best retained below") — measured end-to-end through
the shipped `apply()` (crafted concurrent window: markers 1→4→8, depth = count) and
killed by a 30-line patch: `defuse()` rewrites conflict blocks as labeled attributable
versions, `apply()` defuses inputs and output,
`summary()` never returns marker text, `heal` cleans the damaged pages with all 32
content sides preserved verbatim and the index flags kept — with a checker-found
residual: on interleaved depth ≥ 2 damage (the real `nladder.md`) `defuse` mis-pairs
the nesting and heal leaves 2 orphan `=======`/`>>>>>>>` lines, its `<<<<<<<`-only
success check blind to them
(20261016-1835-inversion-de18, inversion; history census + crafted replay + patched
replay + heal, all regenerable in < 1 min).**

## Refuted

- **"The wiki's three-way publish is safe because the Runs list is a union":** true
  for the runs list (5/5 lines kept in the worst crafted case), but the prose sections
  carry no such protection, and the markers then hide the runs' conclusions
  (20261016-1835-inversion-de18).
- **"Conflicts are one-off accidents a resolution job clears":** the history shows a
  cycle — each of nladder's two hand-clearings was followed by a deeper rebuild
  (depth 2 → 3); the mechanism, not any particular window, produces them
  (20261016-1835-inversion-de18).

## Open directions

1. **Adopt and heal (the integrator's one-step):** merge the patched `wiki.py`, run
   `heal` once, and the three conflicted pages become readable with both sides
   labeled; the next run on each topic folds the labeled versions into one best (the
   README's own resolution path, now with attributable text instead of marker nests).
2. The `defuse` label "standing" vs "this publish" assumes publishes are ordered; a
   `wiki.py apply` invoked with a whole results directory re-applies past runs each
   time (the amplifier in the crafted replay) — the publisher could pass only the
   newly finished run, deleting that amplifier too.
3. **Close the heal residual (checker, this run):** `defuse` pairs each conflict's
   `=======`/`>>>>>>>` with the first available opener, so interleaved nested damage
   (depth ≥ 2, the real `nladder.md`) leaves orphan marker lines heal cannot remove
   and a later apply on such a page can turn back into `<<<<<<<` markers; pair or
   strip the orphans, and let heal/verify count all three marker lines, not just
   `<<<<<<<`.

## Contradictions

None open. The README's contract ("a conflict is kept, flagged in the index, and
resolved by the next run on that topic") is honored by the patch: conflicts stay
visible and flagged; only the marker syntax dies.

## Runs

- 20261016-1835-inversion-de18 (awaiting grade): the publisher's conflicts compound
  (measured, history + replay) and are defused by a 30-line patch + heal, content
  preserved verbatim.
