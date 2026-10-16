# Dossier — 20261016-1835-inversion-de18 (inversion lens)

**Claim.** The lab's own memory is a measured, compounding failure: `lab/wiki.py apply`
writes raw `git merge-file` conflict markers into the wiki's pages, each unresolved
publish nests them deeper, and the markers leak into `lab/wiki/index.md` — today 3 of
26 topic pages (the two most-run: nladder 145 runs, encounters 95) are unreadable at
the mandated entry point; a 30-line patch (`defuse`, marker-free merges) plus a
one-time `heal` deletes the failure mode with every side's content preserved verbatim.

**Bottleneck.** Not on the board (the board is engine-only), but it gates every board
run: failure mode 5 of this lens ("a process that eats the builders' time"). The wiki
is the lab's compaction survival (Julien, 12 October: "a karpathy style wiki where the
current best and directions are clear and not missed"). Measured tax today: the
integrator's directed queue opens with conflict-resolution jobs (`q-wiki-kick-jet-close`),
authors on conflicted topics write "prior best retained below / sides with neither
standing conflict" instead of compiling the page (visible on `nladder.md`), and every
checker re-adjudicates marker nests by hand. Expected gain: not 10× compute — the
deletion of a recurring whole-job cost (resolution jobs, marker adjudication) and the
restoration of one readable current-best per topic.

**Evidence** (all commands in `regen.sh`, < 1 min, nothing outside this run folder
written):

- **P1, real history** (`git log -- lab/wiki/<page>.md`, marker counts and nesting
  depth per publish): `nladder.md` markers 10 → hand-resolved 0 → rebuilt 7 → 0 → 3 →
  7 with max nesting depth growing 2 → 2 → 3 across resolution cycles; `scan-queue.md`
  went 0 → 7 markers in the single c9657cd1 publish; `encounters.md` 0 → 5 in db0f3e74.
  Checked-out tree: 5+7+7 markers, and `index.md` rows for scan-queue and encounters
  print `<<<<<<< main` as the page's "Current best".
- **P2–P4, the shipped function** (`work/replay-pristine.sh` drives the pristine
  `work/wiki-pristine.py` `apply()` end-to-end in a throwaway repo: four gold runs,
  same start commit, each rewriting `## Current best`, exactly the concurrent-window
  shape): markers 0 → 1 → 4 → 8, nesting depth = marker count (each publish re-applies
  every past run, so the nesting squares); `summary()` returns `'<<<<<<< main'`; the
  index row for the topic is `| ... | <<<<<<< main |`. The runs-union itself is sound
  (5/5 run lines kept) — the damage is confined to the merged prose sections.
- **P5, the patch** (same replay through the patched `lab/wiki.py`): zero markers at
  every publish; conflicts land as labeled, attributable blocks ("*Version `main`
  (standing):*" / "*Version `<run id>` (this publish):*" under a visible ⚠ unmerged
  notice); the index still flags `**conflict to resolve**` (the README's contract:
  conflicts stay for the next run on the topic to resolve) but prints the standing
  current-best text; all four sides' content present (same side counts as pristine).
- **P6, heal on the real pages** (`work/heal-check.py`, on a copy): 16 top-level
  conflict blocks (nladder's 7 markers = 4 top-level + 3 nested; the recursion
  defuses nested blocks with their own recorded labels), 32 sides, **all content
  preserved verbatim** (only marker-syntax lines are rewritten, which is the point);
  healed index: zero marker leaks, all three rows readable with flags kept.

**Mechanism** (three lines of `apply()`): it writes `r.stdout` unconditionally, so
`git merge-file`'s conflict hunks land on main; the next publish three-ways against a
page whose "Current best" now IS markers, nesting them; `summary()` takes the first
line under `## Current best`, which is a marker. The patch: `defuse()` rewrites every
conflict block as labeled versions (recursively, so nesting cannot survive), `apply()`
defuses its inputs and output (depth ≤ 1 by construction), `summary()` skips
marker/label syntax, the index flag also detects the unmerged notice, and `heal`
cleans the pages already damaged. `LAB_WIKI` env override added for exactly this kind
of test.

**Predictions.** `predictions.md` was written before the decisive runs; all six held.
The held-out items (P5's fourth-publish depth, P1's counts) came out at least as bad
as pre-registered: depth grew to 8 in the crafted replay (I predicted ≥ 2), and P1's
history showed TWO full conflict→hand-resolution→rebuild cycles on nladder, not one.

**What would make it wrong.** If the integrator prefers hand-resolution over any
script change: the measurement still stands (the tax recurs; the last two resolution
cycles each ended deeper than the last). The patch would be wrong if a run's proposed
page ever needs literal `<<<<<<<` lines to survive publishing — no page has ever
wanted that, and `heal` preserves all content lines regardless. Adoption cost: one
merge of `lab/wiki.py` + one `wiki.py heal` run; no page content changes (P6).

**Fit with PRINCIPLES.** "Errors never compound" (13) — the publish loop is the one
place in the lab where they measurably do. "It's ok to try but it's not a reason to
wreck havoc either" (11): two concurrent windows is normal operation, not misuse.
"Text has a cost" (AGENTS): unreadable current-bests are the most expensive text the
lab owns. And "A test that cannot fail is a control": the pristine replay fails
exactly as production does, and the patched replay passes it.

**The lens may have made me miss:** engine-side inversion targets — I surveyed the
wiki's topic pages first and every board failure mode (law error, quadratic scaling,
seams, memory growth) already carries a measurement, which is why this run took the
fifth mode; an engine lens might instead fly the still-unflown stationary-player or
undissolved-battle cases (scan-queue direction 2, nladder's 4fa8 note).
