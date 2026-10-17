# Dossier — 20261016-2327-taleb-87d0 (taleb lens): the lab's memory, ruin closed end to end

## Claim

The wiki publisher's residual is closed: with a stack-pairing `defuse` that binds every
`=======`/`>>>>>>>` to its own block and drops orphan syntax, the three really-damaged
pages (nladder 145 runs, encounters 95, scan-queue 8) heal to **zero marker lines of all
three kinds with zero content lost**, and stay at zero markers through a further publish —
the exact experiment silver 20261016-1835-inversion-de18 was named for.

## Bottleneck

Not an engine bottleneck; the ruin layer under all of them. The wiki is the mandated entry
point ("Every author reads first"), and 3 of 27 index rows — including the two most-run
topics, the board's #1 (`nladder`) and #3 (`encounters`) — print `<<<<<<< main` as their
current best. Compounding measured **live on real inputs**: replaying the actual
20261016-1637 window (two silver runs' real pages, real base `2ac3c8d2`) through shipped
`apply()` takes nladder from 19 marker lines (7 open / 7 mid / 5 close; 1 orphan mid, 2
never-closed blocks) to **46** (16/16/14; 4 orphan mids) — ×2.4 in one window. Expected
gain: the lab's memory stops decaying per publish; what it deletes is the marker syntax
itself plus the re-apply amplifier (already-folded runs are skipped, killing the measured
quadratic labeled-block growth at its source).

## Evidence (all from `bash lab/results/20261016-2327-taleb-87d0/regen.sh`, deterministic, < 1 s of compute, bit-identical from a pristine tree + `work/patch.diff`)

- **C1 census (independent instrument, no logic shared with the fix):** nladder
  7/7/5 markers, 1 orphan mid, 2 unclosed; encounters 5/5/5; scan-queue 5/4/4, 1
  unclosed; 3 of 27 index rows leak marker text. No legitimate `^=======$` line exists
  anywhere else in the wiki (instrument control: the marker grammar is unambiguous).
- **S2 arming control (shipped code, real inputs):** 19 → 46 marker lines; tree restored
  byte-identical afterwards.
- **S3 heal (patched, on copies of the real pages):** markers 0 on all three pages (0/0/0
  each kind); content multiset: **0 lines lost** (only the `⚠ unmerged` banners and
  `*Version*` labels added); each `## Runs` list byte-identical; unmarked pages
  byte-identical (heal touches only marked pages); regenerated index: 0 marker leaks, and
  all three rows readable (nladder's current best is again a sentence, not `<<<<<<<`).
  Nested damage renders as attributable versions; the two never-closed blocks render as
  labeled `(truncated)` versions — the checker's E-case, on the real page.
- **S4 the gold case (post-heal publish):** two concurrent next-runs editing the same
  Current-best region through patched `apply()` on the healed page: **0 markers before
  and after**, runs union +2/+2, healed content fully present, the real conflict visible
  as 8 labeled banners (readable, attributable to run ids).
- **S5 from today's damaged page (worst start):** a fresh publish through patched
  `apply()`: 0 markers (13 labeled banners); a following `heal`: 0 markers, 0 content
  lost, idempotent.
- **S6 amplifier:** re-presenting the already-folded `20261016-1637-dynamics-87fd`
  alongside a new run — patched: the old run is skipped (page unchanged at 7 banners,
  runs +1); no-skip control: the old run re-merges with conflicts (14 banners, 50 lines
  fatter). The skip is two lines in `apply()`.
- **Patch:** `work/patch.diff`, +92/−9 on `lab/wiki.py` only. It **contains and supersedes**
  the silver's patch (defuse/labels/heal/LAB_WIKI) plus: stack pairing, orphan-mid/close
  drop, recursive rendering of truncated tails (the fallback that let markers back in),
  `has_markers` counting all three kinds (heal guard, index flag), `GIT_WIKI` so sandbox
  replays read base pages from the real repo, and the already-folded skip.

## Predictions

`predictions.md` was written before every instrument ran. **P1–P6 all held.** Held-out
items: the exact banner count after S5's publish (13) and S4 (8) were not tuned; the
one miss is a denominator: the index has 27 topic rows, not the 30 I predicted (leak
count 3 was right). The held-out orphan census matched exactly (nladder 1 orphan mid +
2 unclosed; scan-queue 1 unclosed).

## What would make it wrong

- A page legitimately containing a line of exactly seven `=` (setext underline) would be
  defused as a version separator; none exists today (checked, all 27 pages), but nothing
  forbids one — a one-line lint in `wiki.py index` would close it if it ever bit.
- Readability is not resolution: the labeled versions on nladder/encounters/scan-queue
  still need each topic's next run to fold them into one best (the README's own contract;
  now with attributable text instead of marker nests).
- The skip relies on the Runs list being the union (it is, by construction of `apply`);
  a run folded under a *renamed* id would not be skipped.

## Cost of adoption, fit

One merge (`work/patch.diff`), one `python3 lab/wiki.py heal`, then publish as usual —
no crate, no gate, no doc outside `lab/` touched. PRINCIPLES 13: "basically we don't want
errors that can compound that's the goal" — measured compounding on the lab's own
canonical history, closed. AGENTS: "Survive compaction … anything that isn't written
durably is lost" — the wiki is that durable memory; it was the thing decaying.

## The lens

Taleb: ruin before optimization — this is the lab's corrupted-canonical-history state,
closed with via negativa (the marker syntax dies; conflicts stay visible). What the lens
may have missed: engine-side fragilities untouched (the allocator's open direction 4 —
real conflict rates of the flown universe — still has no run); and the barbell's
speculative end got nothing here.
