# Lens: compile the wiki page `view`

Read `lab/wiki/README.md` first. You are the compiler, not an author: no new experiment unless two runs contradict each other and one cheap probe (≤ 10 minutes) decides it.

The raw sources are the runs below: the integrator's keyword clustering of 6–12 October, so some belong elsewhere and others are missing (search `git for-each-ref refs/remotes/origin/claude/lab-*` for more). For each, read the checker's abstract first (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`, its first 120 words); open the `dossier.md` beside it for the golds, for claims that conflict, and wherever the abstract is not enough. Weigh a claim by its grade and by whether later runs refuted it; a gold that a later gold refutes is refuted.

Write `$out/wiki/view.md`: the page `lab/wiki/view.md`, filled in. Keep its header, set `updated:` to your run id, and keep `status: open`: closing a topic is a checker's call, through `closed-by`. Each claim cites its run ids. Write for the corporal: the current best in a few sentences with its numbers and its domain (where it was tested, where it was not), refuted claims one line each, open directions ranked by what they would change, contradictions not resolved. Under `## Runs`, one line per run: `- <id> (<grade>): <its claim in at most 20 words>`. Runs that belong to another topic go in your dossier, by topic, for that topic's compiler.

Gold: a page the integrator can act on without opening a dossier, faithful to the runs (the checker samples five claims against their dossiers), with nothing that a run does not support.

## The runs (28)

- `20261006-0030-m-obscure-8202` (silver)
- `20261006-1029-constraint-f22e` (silver)
- `20261006-1436-quant-18e5` (silver)
- `20261008-0458-constraint-3102` (silver)
- `20261008-0945-second-20261008-0743-constraint-4588-0e54` (silver)
- `20261008-1521-quant-97fd` (silver)
- `20261008-1859-scout-141c` (silver)
- `20261008-2113-second-20261008-2031-constraint-4b27-08f7` (silver)
- `20261008-2349-constraint-70b0` (missing)
- `20261009-0521-redteam-93a4` (silver)
- `20261009-0621-constraint-51bf` (silver)
- `20261009-1649-second-20261009-1556-redteam-18fc-94dc` (gold)
- `20261009-2120-redteam-ace6` (silver)
- `20261010-0541-system-d51f` (silver)
- `20261010-1544-scout-c4cb` (silver)
- `20261010-2052-redteam-8be2` (silver)
- `20261010-2141-second-20261010-2052-redteam-8be2-9f4a` (gold)
- `20261010-2220-scout-9096` (missing)
- `20261010-2314-redteam-0b45` (silver)
- `20261011-0006-constraint-48cf` (silver)
- `20261011-0614-redteam-a616` (missing)
- `20261011-0924-redteam-5977` (gold)
- `20261011-1234-redteam-6eae` (silver)
- `20261011-1332-constraint-acff` (silver)
- `20261011-1332-second-20261011-1234-redteam-6eae-8f00` (silver)
- `20261011-1917-redteam-fb64` (silver)
- `20261012-0138-redteam-0fe0` (silver)
- `20261012-0311-components-5465` (silver)
