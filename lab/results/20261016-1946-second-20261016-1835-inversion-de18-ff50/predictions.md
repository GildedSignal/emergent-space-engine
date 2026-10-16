# Predictions — second-author run on 20261016-1835-inversion-de18

Written before any v2 experiment ran (only the original run's record, the shipped
files, and `grep` of the three damaged pages have been read). The checker's named
experiment: fix `defuse`'s pairing (openers tracked so each `=======`/`>>>>>>>`
binds to its own `<<<<<<<`), count all three marker lines in heal and its check,
then show truly-zero markers on the real pages before and after one publish.

## The real pages' pairing, read off the marker lines (stack discipline)

- **nladder.md** (7 openers at 5,8,18,96,195,197,209; 5 closers at 13,98,202,250
  … wait, 4 closers visible: 12,13,98,202,250 = 5): closers bind to 8,5,96,197,209
  in stack order; **C18 (line 18, in `## Current best`) and C195 (line 195, in
  `## Refuted`) never close** — that is why v1's heal left the orphan
  `>>>>>>> 20261016-1637-second-…-fermi-1051-1a46` and a bare `=======`: it closed
  C5 at the inner closer (line 12) and C195/C209 early, dumping their closers and
  C209's second separator (line 248) into the output as orphans.
- A section heading (`## …`) resyncs the stack (conflicts in these pages are
  section-local), so C18 truncates at `## Refuted` (line 194) and C195 at the
  duplicate `## Open directions` (line 283); the `## Runs` section (line 332)
  stays at column 0 and every run line stays countable by `index()`.
- **scan-queue.md** and **encounters.md**: openers == closers == separators
  (7 and 5), all depth-1, no nesting, no truncation — they heal to plain labeled
  blocks exactly as v1 did (v1 was already clean there).

## Held-out expectations (v2 heal + instruments that count all three marker lines)

1. **H1 (real heal):** after v2 `heal` on a copy of the real wiki, every page and
   the index have **0 lines matching `^<<<<<<<`, `^=======$` (exact seven), and
   `^>>>>>>>`** — v1's count was 0 `<<<<<<<` but nladder still carried 1 orphan
   `>>>>>>> <run>` and 1 bare `=======`.
2. **H2 (content):** every non-marker line of each original page appears in its
   healed version in the same order (subsequence), for all three pages; the only
   added lines are label/notice syntax.
3. **H3 (apply after heal):** two publishes later (a first run editing
   `## Current best`, then a second concurrent one from the same base, so
   merge-file conflicts against a page whose sides are labeled blocks): 0 marker
   lines of all three kinds **before and after** each publish, both sides' text
   present, runs union intact, `summary()` returns prose (not marker/label
   syntax), the index row keeps `**conflict to resolve**` on conflict and prints
   the standing best.
4. **H4 (the checker's E-cases):** patched apply on a pristine-damaged page
   (three concurrent runs first run through the pristine `apply`), with or
   without a heal in between, writes **0** marker lines (v1 wrote 2 back); the
   damaged real nladder defused directly also emits 0.
5. **H5 (regression):** pristine replay still gives markers 0→1→4→8 with
   `summary()` = `<<<<<<< main`; patched replay still 0 at every publish through
   six concurrent publishes; content cross-check pristine-final vs patched-final:
   no content line lost.
6. **H6 (adversarial shapes I crafted but did not tune on):** opener inside the
   ours-side of another conflict; orphan `=======` with an empty stack; orphan
   `>>>>>>> label` with an empty stack; a conflict truncated at end of page; a
   conflict cut by a `## ` heading. All defuse to 0 marker lines with content
   preserved as a subsequence; orphan bare markers (no content) are dropped.

## What would falsify the v2 claim

Any of: a marker line of any of the three kinds surviving heal or a later apply;
a content line of a real page lost or reordered; the `## Runs` union broken by a
publish over a healed page; or the E-cases still writing markers.
