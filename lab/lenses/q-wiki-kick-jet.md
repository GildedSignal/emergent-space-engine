# Lens: compile the wiki page `kick-jet`

Read `lab/wiki/README.md` first. You are the compiler, not an author: no new experiment unless two runs contradict each other and one cheap probe (≤ 10 minutes) decides it.

The raw sources are the runs below: the integrator's keyword clustering of 6–12 October, so some belong elsewhere and others are missing (search `git for-each-ref refs/remotes/origin/claude/lab-*` for more). For each, read the checker's abstract first (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`, its first 120 words); open the `dossier.md` beside it for the golds, for claims that conflict, and wherever the abstract is not enough. Weigh a claim by its grade and by whether later runs refuted it; a gold that a later gold refutes is refuted.

Write `$out/wiki/kick-jet.md`: the page `lab/wiki/kick-jet.md`, filled in. Keep its header, set `updated:` to your run id, and keep `status: open`: closing a topic is a checker's call, through `closed-by`. Each claim cites its run ids. Write for the corporal: the current best in a few sentences with its numbers and its domain (where it was tested, where it was not), refuted claims one line each, open directions ranked by what they would change, contradictions not resolved. Under `## Runs`, one line per run: `- <id> (<grade>): <its claim in at most 20 words>`. Runs that belong to another topic go in your dossier, by topic, for that topic's compiler.

Gold: a page the integrator can act on without opening a dossier, faithful to the runs (the checker samples five claims against their dossiers), with nothing that a run does not support.

## The runs (36)

- `origin/claude/lab-20261006-0346-redteam-df81` (2026-10-06)
- `20261006-1249-redteam-4978` (gold)
- `20261007-0621-components-8306` (silver)
- `20261007-2057-second-20261007-2002-spacex-3b99-be63` (gold)
- `20261008-0338-second-20261008-0234-spacex-0083-492f` (silver)
- `20261008-1337-redteam-2040` (silver)
- `20261008-1419-second-20261008-1337-redteam-2040-9a04` (gold)
- `20261008-1521-spacex-8016` (silver)
- `20261008-1613-redteam-7922` (silver)
- `20261008-1613-second-20261008-1521-spacex-8016-6c47` (gold)
- `20261008-1719-second-20261008-1613-redteam-7922-e86c` (silver)
- `20261008-1719-system-0ccd` (silver)
- `20261008-1757-second-20261008-1719-system-0ccd-b33f` (gold)
- `20261009-0401-quant-ea6b` (silver)
- `20261009-0521-second-20261009-0401-quant-ea6b-96b4` (silver)
- `20261009-1858-redteam-075b` (silver)
- `20261009-1936-second-20261009-1858-redteam-075b-a059` (gold)
- `20261010-0541-components-8c81` (silver)
- `20261010-0656-second-20261010-0541-system-d51f-3e48` (gold)
- `20261010-0814-second-20261010-0656-autoresearch-cc88-8ce2` (silver)
- `20261010-0920-quant-30e1` (silver)
- `20261010-1706-second-20261010-1544-system-97ce-b18f` (gold)
- `20261010-1816-system-67f2` (silver)
- `20261010-2141-system-eea5` (silver)
- `20261011-1102-scout-4c5b` (silver)
- `20261011-1332-fermi-e3bc` (silver)
- `20261011-1456-components-f797` (silver)
- `20261011-1456-second-20261011-1332-fermi-e3bc-c4ce` (silver)
- `20261011-1729-system-2c68` (silver)
- `20261011-1814-second-20261011-1729-system-2c68-b242` (missing)
- `20261011-2235-redteam-6164` (silver)
- `20261011-2306-second-20261011-2235-redteam-6164-ee08` (gold)
- `20261012-0036-second-20261011-2306-system-3367-1e74` (gold)
- `20261012-0358-components-fa08` (silver)
- `20261012-1117-redteam-4808` (silver)
- `20261012-1227-second-20261012-1117-redteam-4808-d617` (gold)
