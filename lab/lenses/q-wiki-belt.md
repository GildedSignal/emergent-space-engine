# Lens: compile the wiki page `belt`

Read `lab/wiki/README.md` first. You are the compiler, not an author: no new experiment unless two runs contradict each other and one cheap probe (≤ 10 minutes) decides it.

The raw sources are the runs below: the integrator's keyword clustering of 6–12 October, so some belong elsewhere and others are missing (search `git for-each-ref refs/remotes/origin/claude/lab-*` for more). For each, read the checker's abstract first (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`, its first 120 words); open the `dossier.md` beside it for the golds, for claims that conflict, and wherever the abstract is not enough. Weigh a claim by its grade and by whether later runs refuted it; a gold that a later gold refutes is refuted.

Write `$out/wiki/belt.md`: the page `lab/wiki/belt.md`, filled in. Keep its header, set `updated:` to your run id, and keep `status: open`: closing a topic is a checker's call, through `closed-by`. Each claim cites its run ids. Write for the corporal: the current best in a few sentences with its numbers and its domain (where it was tested, where it was not), refuted claims one line each, open directions ranked by what they would change, contradictions not resolved. Under `## Runs`, one line per run: `- <id> (<grade>): <its claim in at most 20 words>`. Runs that belong to another topic go in your dossier, by topic, for that topic's compiler.

Gold: a page the integrator can act on without opening a dossier, faithful to the runs (the checker samples five claims against their dossiers), with nothing that a run does not support.

## The runs (14)

- `20261005-2231-q-secular-008e` (lead)
- `20261006-0737-q-secular-v2-5f69` (silver)
- `20261006-0916-redteam-e84d` (silver)
- `20261007-0711-second-20261007-0621-scout-6e10-ab9d` (gold)
- `20261007-0933-second-20261007-0842-fermi-fc22-a7d0` (gold)
- `20261007-1032-second-20261007-0933-system-0510-53f6` (silver)
- `20261007-1106-second-20261007-1032-taleb-ab03-0263` (gold)
- `20261008-1947-library-d583` (silver)
- `20261009-0208-redteam-e369` (lead)
- `20261009-1649-dynamics-ec3a` (silver)
- `20261009-1858-second-20261009-1754-spacex-c6d8-71bd` (silver)
- `20261010-0352-second-20261010-0306-spacex-acb2-7b82` (silver)
- `20261011-0006-second-20261010-2314-taleb-6baf-2b8e` (gold)
- `20261011-2306-dynamics-0b04` (silver)
