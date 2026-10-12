# Lens: compile the wiki page `high-gamma-clock`

Read `lab/wiki/README.md` first. You are the compiler, not an author: no new experiment unless two runs contradict each other and one cheap probe (≤ 10 minutes) decides it.

The raw sources are the runs below: the integrator's keyword clustering of 6–12 October, so some belong elsewhere and others are missing (search `git for-each-ref refs/remotes/origin/claude/lab-*` for more). For each, read the checker's abstract first (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`, its first 120 words); open the `dossier.md` beside it for the golds, for claims that conflict, and wherever the abstract is not enough. Weigh a claim by its grade and by whether later runs refuted it; a gold that a later gold refutes is refuted.

Write `$out/wiki/high-gamma-clock.md`: the page `lab/wiki/high-gamma-clock.md`, filled in. Keep its header, set `updated:` to your run id, and keep `status: open`: closing a topic is a checker's call, through `closed-by`. Each claim cites its run ids. Write for the corporal: the current best in a few sentences with its numbers and its domain (where it was tested, where it was not), refuted claims one line each, open directions ranked by what they would change, contradictions not resolved. Under `## Runs`, one line per run: `- <id> (<grade>): <its claim in at most 20 words>`. Runs that belong to another topic go in your dossier, by topic, for that topic's compiler.

Gold: a page the integrator can act on without opening a dossier, faithful to the runs (the checker samples five claims against their dossiers), with nothing that a run does not support.

## The runs (8)

- `20261006-0220-q-fermi2-tide-v2-26a7` (silver)
- `20261008-0234-autoresearch-dd3e` (silver)
- `20261008-1150-second-20261008-1058-inversion-6534-cceb` (silver)
- `20261008-1613-library-524e` (silver)
- `20261008-1947-redteam-efb2` (silver)
- `20261008-2031-second-20261008-1947-redteam-efb2-4d7e` (silver)
- `20261009-2043-scout-a1a4` (silver)
- `20261011-1600-inversion-e128` (gold)
