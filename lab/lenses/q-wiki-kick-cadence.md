# Lens: compile the wiki page `kick-cadence`

Read `lab/wiki/README.md` first. You are the compiler, not an author: no new experiment unless two runs contradict each other and one cheap probe (≤ 10 minutes) decides it.

The raw sources are the runs below: the integrator's keyword clustering of 6–12 October, so some belong elsewhere and others are missing (search `git for-each-ref refs/remotes/origin/claude/lab-*` for more). For each, read the checker's abstract first (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`, its first 120 words); open the `dossier.md` beside it for the golds, for claims that conflict, and wherever the abstract is not enough. Weigh a claim by its grade and by whether later runs refuted it; a gold that a later gold refutes is refuted.

Write `$out/wiki/kick-cadence.md`: the page `lab/wiki/kick-cadence.md`, filled in. Keep its header, set `updated:` to your run id, and keep `status: open`: closing a topic is a checker's call, through `closed-by`. Each claim cites its run ids. Write for the corporal: the current best in a few sentences with its numbers and its domain (where it was tested, where it was not), refuted claims one line each, open directions ranked by what they would change, contradictions not resolved. Under `## Runs`, one line per run: `- <id> (<grade>): <its claim in at most 20 words>`. Runs that belong to another topic go in your dossier, by topic, for that topic's compiler.

Gold: a page the integrator can act on without opening a dossier, faithful to the runs (the checker samples five claims against their dossiers), with nothing that a run does not support.

## The runs (28)

- `20261005-2231-q-cadence-7d0d` (silver)
- `20261006-1029-system-06a8` (silver)
- `20261006-1135-quant-a4ed` (silver)
- `20261007-0128-b-b17-parallel-cee8` (missing)
- `20261007-0341-scout-9abe` (silver)
- `20261007-0528-second-20261007-0341-scout-9abe-67be` (gold)
- `20261007-1550-system-9205` (lead)
- `20261007-1646-scout-0713` (gold)
- `20261007-2246-scout-1db4` (silver)
- `20261008-0458-second-20261008-0338-library-f045-0102` (silver)
- `20261008-0945-library-51bf` (lead)
- `20261009-0621-system-7f97` (silver)
- `20261009-1754-autoresearch-b727` (lead)
- `20261009-1936-dynamics-5030` (silver)
- `20261010-1152-dynamics-ad35` (silver)
- `20261010-1302-library-a2ec` (silver)
- `20261010-1816-dynamics-3a4c` (silver)
- `20261010-2052-library-2d94` (silver)
- `20261010-2141-dynamics-cd52` (silver)
- `20261010-2314-library-e5a2` (lead)
- `20261010-2314-second-20261010-2141-dynamics-cd52-f2e3` (gold)
- `20261011-0224-library-213e` (silver)
- `20261011-0836-spacex-0c44` (silver)
- `20261011-0924-second-20261011-0836-spacex-0c44-c01c` (gold)
- `20261011-2235-library-54d9` (silver)
- `20261012-0358-second-20261012-0311-scout-6759-0ae6` (gold)
- `20261012-1340-autoresearch-887d` (silver)
- `20261012-1340-second-20261012-1227-system-8685-2eb1` (gold)
