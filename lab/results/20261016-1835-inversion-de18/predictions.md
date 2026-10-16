# Predictions — 20261016-1835-inversion-de18 (written before the decisive experiment)

Topic: the lab's own memory (lab/wiki) as failure mode 5 of the inversion lens
("a process that eats the builders' time"). Premise: `lab/wiki.py apply` keeps
`git merge-file` conflict markers in the page, they compound across publishes, and
they leak into the index — the wiki's contract ("current best is clear", Karpathy,
Julien 12 October) is already broken on its most important pages.

Cases I have NOT tuned on (the history census and the crafted replay are the
decisive instruments; the patch is written after these are checked):

- **P1 (history, real):** the committed history of `lab/wiki/nladder.md` shows the
  conflict-marker count growing across the 16-October publish windows (≥ 2 windows),
  with nesting depth ≥ 2 at the 16-1637 window — i.e. publishes compound on top of
  unresolved markers rather than starting from a clean base. If markers appeared only
  once and never nested, the premise of compounding dies.
- **P2 (mechanism, crafted):** driving the shipped `apply()` end-to-end on a scratch
  repo (two gold runs, same start commit, both rewriting `## Current best`) writes
  raw `<<<<<<<`/`=======`/`>>>>>>>` markers into the published page. If apply skips
  or refuses conflicted output, the premise dies and the dossier says so.
- **P3 (compounding):** a third publish on the same start commit over the already
  marked page nests markers (a `<<<<<<<` line inside a conflict side; depth 2).
- **P4 (index leak):** `summary()` on a marked page returns text beginning with a
  marker (or empty), so the index row for that topic is unreadable — the mandated
  entry point ("read lab/wiki/index.md instead of dossiers") shows marker text.
- **P5 (patch):** replaying the same sequence (A, B, C) through the patched
  `apply()` writes zero markers anywhere: each concurrent update lands as a labeled,
  run-attributed block in run order; a fourth publish stays at depth 1; the index
  still flags the conflict (visible, not hidden — the README contract keeps
  conflicts for the next run on the topic to resolve) but prints readable text.
- **P6 (heal):** `heal` on today's real `lab/wiki/nladder.md` (7 blocks, nested)
  leaves zero markers and changes only the marker blocks: every line outside them
  byte-identical, both sides of every block preserved verbatim inside labeled
  blocks.

Held-out (checked only after the patch runs): P5's fourth-publish depth, and the
exact marker/nesting counts of P1 (recorded by the census script before I look at
them page by page).
