# Predictions — second author on 20261012-1621-q-wiki-kick-jet-9392

Written after the branch search ran (646 branches swept, keyword pass done, the five
checker-named abstracts read) and BEFORE the decisive work: the check2 verification, the
2c68 checker-number check, the page fold and the regen.sh assertions. Cases not tuned on:
every check2 file, 2c68's check.md medians, and the fold's effect on the page.

- **P1 (check2 = the standing grades' basis).** Every standing gold on the page has a
  second check grading gold (the six refutations 4978, 9a04, a059, b33f, ee08, d617, plus
  6c47, b18f, 1e74); every standing silver has a second check grading silver (8306, 7922,
  e86c, 96b4, 6164, 67f2 and the rest); df81 alone is single-checked (gold, flagged).
  The first checker verified the golds; I predict the silvers' check2 lines also exist
  and say silver, so regen.sh can assert all of them.
- **P2 (the two page additions).** 0083 (silver): compile 62.1 µs of a 97.3 µs median
  kick (64.5%), rebind 78.7%, forces 8.8%, trivial reuse 0.8–1.5%, lever 3.3–4.4× —
  it corroborates the page's "the compile owns the kick" and predates its second author
  492f. 620e (gold): fired kick ~25× above floor, gap = rebind 68% + secondaries 27%,
  forces 6%; consistent with the page's pricing paragraph, no contradiction with
  1e74/fa08 (different floors: 620e's is the integer force path, fa08's is two-integer
  rebind). Both fold into Runs + Current best without touching any refuted line.
- **P3 (2c68's checker medians).** 2c68's check.md carries corrected-body medians
  72/314/705 verbatim; citing them beside the dossier's 34–790 range keeps the
  contradiction entry faithful to both records.
- **P4 (the adjacent triage holds).** ec9d (silver): the leaver-kick tail is
  Passage::compile (89–97% of the leaver rebind, median 365–381 µs vs made 42.8 µs) —
  a kick-cost claim, in window, page-worthy as the leaver-tail anchor. 3367 (silver):
  its unique yield (motion-law-v2 per-event cost, view 64–83% of frame) is frame-cost/
  view; its kick part (1125/1125 re-fits) is already on the page via b063/1e74 — so it
  goes to the cross-topic handoff. b063 (components, gold): the board files its
  ~1,800× under frame-cost, so it goes to the frame-cost handoff with a cross-reference
  to fa08's ~270× (different floors).
- **P5 (the wider sweep is secondary, not missing).** The keyword pass's other in-window
  hits (6–12 Oct) have kick mentions secondary to another topic: memory (21c3, df14,
  a11b, ba64, 5465, c304), cadence (c01c, 9abe, 67be), frame/scheduler (5457, f045,
  ec3a), co-orbital (inversion-b063), belt/encounters (e2a9, 2a9d, 6e10, ab9d, 8bfa,
  57c1), compiler representation (fa4b, 6586, 126c, 640f, c3a5, 0528, 2eb1). None of
  them, read at abstract level, changes the page's current best, its refuted list, or
  its open directions; they go to the dossier's cross-topic handoff, one line each, so
  the next compilers inherit the triage instead of redoing the sweep.
- **P6 (the count moves as measured).** After the fold the page carries 32 run lines
  (30 + 0083 + 620e + ec9d = 33 if ec9d takes a page line — P4 says it does), every id
  with a branch, `updated:` set to this run, `status: open`.

Misses will be reported and folded the same way the first author's P4 miss was.
