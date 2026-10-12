# Lens: compile the wiki page `b12-statistic`

Read `lab/wiki/README.md` first. You are the compiler, not an author: no new experiment unless two runs contradict each other and one cheap probe (≤ 10 minutes) decides it.

The raw sources are the runs below: the integrator's keyword clustering of 6–12 October, so some belong elsewhere and others are missing (search `git for-each-ref refs/remotes/origin/claude/lab-*` for more). For each, read the checker's abstract first (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`, its first 120 words); open the `dossier.md` beside it for the golds, for claims that conflict, and wherever the abstract is not enough. Weigh a claim by its grade and by whether later runs refuted it; a gold that a later gold refutes is refuted.

Write `$out/wiki/b12-statistic.md`: the page `lab/wiki/b12-statistic.md`, filled in. Keep its header, set `updated:` to your run id, and keep `status: open`: closing a topic is a checker's call, through `closed-by`. Each claim cites its run ids. Write for the corporal: the current best in a few sentences with its numbers and its domain (where it was tested, where it was not), refuted claims one line each, open directions ranked by what they would change, contradictions not resolved. Under `## Runs`, one line per run: `- <id> (<grade>): <its claim in at most 20 words>`. Runs that belong to another topic go in your dossier, by topic, for that topic's compiler.

Gold: a page the integrator can act on without opening a dossier, faithful to the runs (the checker samples five claims against their dossiers), with nothing that a run does not support.

## The runs (15)

- `20261006-0737-redteam-b12-stat-e5fe` (silver)
- `20261006-1545-q-b12-design-9242` (missing)
- `20261007-0528-dynamics-f819` (gold)
- `20261007-1420-library-240c` (silver)
- `20261007-1550-second-20261007-1420-library-240c-32f9` (gold)
- `20261008-1150-scout-2c45` (silver)
- `20261008-2206-library-73ca` (silver)
- `20261009-0208-second-20261008-2206-library-73ca-618f` (silver)
- `20261009-2257-dynamics-a47e` (silver)
- `20261009-2348-second-20261009-2257-dynamics-a47e-09fb` (gold)
- `20261010-0920-second-20261010-0814-system-fbc6-b903` (silver)
- `20261011-0134-scout-7567` (silver)
- `20261011-0224-second-20261011-0134-scout-7567-cc25` (silver)
- `20261012-0138-library-060f` (silver)
- `20261012-1227-dynamics-bd4e` (silver)
