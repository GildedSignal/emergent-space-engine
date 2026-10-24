# The lab wiki

This is the lab's memory, so runs stop rediscovering what earlier runs found (Julien, 12 October: "maybe we need a karphaty style wiki where the current best and directions are clear and not missed to update"). It follows Karpathy's pattern for LLM knowledge bases:
- **the raw sources** are the runs, immutable on their `claude/lab-<id>` branches;
- **the wiki** is these pages, compiled from the runs and owned by the lab;
- **the schema** is this file.

[index.md](index.md) is the entry point: one row per topic, with its state, its run count and its current best.

## A page

- **Header.** The first lines are the header, `key: value`, up to the first blank line:
  - `topic`;
  - `status` (`open` or `closed`);
  - `closed-by` (gold run ids);
  - `valid-while` (paths `@` a commit);
  - `updated` (a run id).
- **Body.** Then the title and five sections, in this order:
  - `## Current best`: the result now standing, its numbers and its domain (where it was tested, and where it was not);
  - `## Refuted`: one line each, with the refuting run;
  - `## Open directions`: ranked by what each would change;
  - `## Contradictions`: unresolved;
  - `## Runs`: one line per run, `- <id> (<grade>): <claim in at most 20 words>`, append-only.
- **Citations.** Every claim cites its run ids.
- **Budgets (20 October: the pages had grown to 1.1 MB, one "current best" to 149 KB, none closed).** `## Current best` holds at most 15 lines: the numbers standing now, never their history. A run that supersedes a line *replaces* it, and the old line goes to `## Refuted` as one line with its refuting run. A page holds at most 300 lines in all; `## Runs` keeps one line per run, and the runs' branches keep everything else. `lab/wiki.py index` flags a page over budget, and an over-budget page is compiled back under it before it takes new runs.

## How it stays true

1. **Every author reads first.** Before choosing an experiment, an author reads the index and the page of its topic. Its result must add what the page lacks: a new current best, a refutation, or a closed direction.
2. **Every graded run proposes its page.** It writes `lab/results/<id>/wiki/<topic>.md`, the page with its result folded in. The checker checks that the page update is faithful. Publishing then merges gold and silver pages into `lab/wiki/` three-way against the page the run started from (`lab/wiki.py apply`). A conflict is kept, flagged in the index, and resolved by the next run on that topic.
3. **A page is a certificate.** A checker closes a topic when three gold runs agree, by setting `status: closed`, `closed-by` and `valid-while` to the code the result depends on, at a commit.
   - The index shows a closed page as reopened as soon as that code changes on main, or if fewer than three of its `closed-by` runs are gold.
   - Closed topics take no new runs. Reopened ones go first.
4. **The index is never edited by hand.** `lab/wiki.py index` rewrites it after every publish.

Lower tiers own this wiki. The integrator reads it and steers through `lab/queue.txt` and the board. Runs are never rewritten here, only compiled.
