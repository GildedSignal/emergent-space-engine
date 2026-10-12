# Lens: compile the wiki page `handoff`

Read `lab/wiki/README.md` first. You are the compiler, not an author: no new experiment unless two runs contradict each other and one cheap probe (≤ 10 minutes) decides it.

The raw sources are the runs below: the integrator's keyword clustering of 6–12 October, so some belong elsewhere and others are missing (search `git for-each-ref refs/remotes/origin/claude/lab-*` for more). For each, read the checker's abstract first (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`, its first 120 words); open the `dossier.md` beside it for the golds, for claims that conflict, and wherever the abstract is not enough. Weigh a claim by its grade and by whether later runs refuted it; a gold that a later gold refutes is refuted.

Write `$out/wiki/handoff.md`: the page `lab/wiki/handoff.md`, filled in. Keep its header, set `updated:` to your run id, and keep `status: open`: closing a topic is a checker's call, through `closed-by`. Each claim cites its run ids. Write for the corporal: the current best in a few sentences with its numbers and its domain (where it was tested, where it was not), refuted claims one line each, open directions ranked by what they would change, contradictions not resolved. Under `## Runs`, one line per run: `- <id> (<grade>): <its claim in at most 20 words>`. Runs that belong to another topic go in your dossier, by topic, for that topic's compiler.

Gold: a page the integrator can act on without opening a dossier, faithful to the runs (the checker samples five claims against their dossiers), with nothing that a run does not support.

## The runs (13)

- `20261006-0346-spacex-1381` (silver)
- `20261006-0737-autoresearch-8d6e` (silver)
- `20261006-1738-b-handoff-surface-18d2` (lead)
- `20261006-1738-b-kerr-compiler-fa4b` (silver)
- `20261006-2240-b-root-keys-ae29` (silver)
- `20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c` (silver)
- `20261007-0341-quant-24cd` (silver)
- `20261007-1234-components-97bf` (silver)
- `20261008-0041-redteam-ecfd` (silver)
- `20261009-2348-scout-3851` (silver)
- `20261011-1102-autoresearch-11de` (missing)
- `20261011-1729-scout-6765` (silver)
- `20261012-0036-scout-aac1` (silver)
