# Lens: compile the wiki page `cell-rebind` back under its budget

Read `lab/wiki/README.md` first, its budgets above all. The page `lab/wiki/cell-rebind.md` has grown into a log (`lab/wiki/index.md` flags it over budget): runs prepended their results to `## Current best` instead of replacing what they superseded.

Write `$out/wiki/cell-rebind.md`, the same page compiled:
- `## Current best`: at most 15 lines, the numbers standing now with their domain and their run ids; nothing superseded.
- `## Refuted`: one line per superseded or killed claim, with the run that superseded or killed it.
- `## Open directions`: at most 8, ranked by the scoreboard row each would move and by how much (`lab/board.md`).
- `## Contradictions`: only the unresolved ones.
- `## Runs`: every existing run line kept, one line each.
At most 300 lines in all. Drop nothing a gold or silver run supports: move it to the right section, or point to the run. Where two runs disagree and the evidence decides, say which one stands and why.

Gold: a page under budget that a reader can act on in one reading, with no supported number lost (the checker samples ten numbers from the old page and finds each in the new page or behind a cited run).
