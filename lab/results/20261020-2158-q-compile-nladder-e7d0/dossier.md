# Dossier — 20261020-2158-q-compile-nladder-e7d0 (lens: compile the wiki page `nladder` under its budget)

**Claim.** The `nladder` page is compiled back under every budget — 1,751 lines / 1,423-line
"Current best" (201,305 bytes) becomes **178 lines / 15-line "Current best" (52,141 bytes,
9.8×)** — with all 100 runs kept one line each, 29 superseded claims moved to `## Refuted`
with their refuting runs, 8 open directions ranked by board row, and no supported number
lost: a fixed 30-number sample of the old page's standing results is 30/30 present in the
new page, every dropped number lives behind its cited run line, and the lab's own
instrument (`lab/wiki.py index`, run sandboxed on the compiled page) reports `open, 101
runs` with no over-budget flag.

**Bottleneck.** Not the engine: the lab's memory. The wiki's budget rule (README: ≤ 15
current-best lines, ≤ 300 lines a page) existed but nothing enforced it on `nladder` —
runs prepended `NEW (...)` paragraphs instead of replacing what they superseded, so the
page held ~40 full entry-and-checker blocks of which all but the newest of each thread
were dead. The index flagged it for days (the worst offender: 1,423 vs 15). Gain: one
reading is possible again (a reader can act on the page without re-deriving 40 runs'
supersession order); ~149 KB of superseded prose deleted, everything else moved to the
section the schema gives it (Refuted / Runs / Contradictions), which is exactly the
README's compile rule that had never been run on this page.

**Evidence** (deterministic; `sh lab/results/20261020-2158-q-compile-nladder-e7d0/regen.sh`
regenerates all of it in < 1 s from shipped code + this run's `compile.py`):

```
== base commit: 9bf31c707a315a6cb2627b25ee13b146d548be0d
budget: 178 total lines (cap 300), current best 15 non-blank (cap 15)
runs: 186 old lines over 100 distinct ids -> 100 kept one-per-id (+ this run's own line); 44 grade tokens refreshed from branches
number sample: 30/30 present in the new page
sections: 15 best lines, 29 refuted, 8 open directions, 2 contradictions
== wiki.py index (sandboxed, the lab's own instrument): | nladder | open | 101 | ... |  (no "over budget")
```

- **Mechanics of the compile** (`compile.py`, all audited, exit non-zero on any failure):
  the old `## Runs` held 186 lines over 100 distinct ids (38 ids re-appended by later
  publishes); each id keeps one line — its graded, complete variant — with grade tokens
  refreshed from the run branches by `wiki.py`'s own rule (`git log origin/claude/lab-<id>`):
  44 refreshed (67 silver, 29 gold stand on the page; 21a7's branch has no grade, 03f4's
  branch is unpublished, this run is ungraded — 3 honest "awaiting grade" lines remain).
- **15 run lines ended mid-sentence on the old page** (re-appends kept only the truncated
  first fragment: 404b, cfe5, 1051, 87fd, 4fa8, 1a1c, 917c, 7fcf, 7581, d839, f80a, 1d47,
  a0a1, 23a6, 03f4). Each is completed from that run's own branch dossier (`git show
  origin/claude/lab-<id>:lab/results/<id>/dossier.md`) or its own entry text; four
  `[restored by checker ...]` annotations are preserved verbatim.
- **Number preservation**: the audit checks a fixed 30-number sample spanning every thread
  (27.9k comb period, 4.889e-5 λ, 45.3–45.9 µs/kick, 40.6 ms, 4.2–4.4 µs/BODY, 8eecf1fa,
  0.041 µs/body warm, 0.053–0.399 delta, 12.75 h/era, 830–1,030×, 0.0526 mints/gs,
  (K+38)·224 B, 635 MB, ≤0.15 KB/kick, 1,295/1,760 B, 1,457 MB, 560,764 gs, 42.8 MB/1k,
  2,302.5 s, 9.2 MB/body, 1,643.5 ms, 5.5e-11, 4.85–5.06 kB/body, 2,346 MB, 1.448 s …):
  30/30 in-page. Everything else a run supports is behind that run's line (its branch
  holds the dossier and evidence, immutable).
- **Where two runs disagree, the evidence decides, and the page says so**: 8365 (gold,
  "the stagger kills the freeze") vs 9ed1 (silver, "the answer channel regrows it") —
  both stand, they are different channels, and Refuted carries each one's over-claim;
  1d47's checker's bistability vs 4063's non-reproduction — Refuted as two lines (the
  gate *was* schedule-dependent at ms-anchored cuts; under canonical-tick cuts the
  invariance is empirical, not structural); 20f2's delta band vs its checker ("window
  facts") — the mechanism stands in Current best, the constants are marked window-bound
  in Refuted; 03f4's F1 zero-lag (M1 0.000 vs Linux 1.448 s) — kept as the one open
  Contradiction with the M1 re-measure named.

**Predictions** (`predictions.md`, written before the decisive run): P1 held (178 ≤ 300,
15 ≤ 15 — measured by re-implementing `wiki.py`'s counter, then confirmed by running the
real `wiki.py index` sandboxed); P2 held exactly (186 → 100, one per id; predicted 67
silver / 29 gold / 4 unresolved — measured 67/29/3 + this run's own line); P3 held at the
strong end (predicted ≥ 28/30 in-page: measured 30/30); P4 held (15 completions, none
other reworded beyond grade tokens); P5 held (`lab/wiki/` untouched — `git status` clean
outside `lab/results/`); P6's kill bar never fired (audit exits 0).

**What would make it wrong.** (1) A number a gold or silver run supports that is neither
in the new page nor on a kept run line — the checker's own ten-number sample is the test;
the 30-number audit is my instrument, and agreement is not independence (both share my
choice of "load-bearing"). (2) A grade refreshed from a stale branch (the branches are
local; if a run was re-graded after this checkout, the page's token lags — the run line's
claim itself is untouched either way). (3) A mis-adjudicated supersession: I ranked by
newest measurement, so any error would be an old result retired too eagerly — every
retired claim is one grep away in `## Refuted` with its run cited, and the runs' branches
are immutable.

**Cost of adoption.** One `wiki.py apply` (the standard publish path merges this page
three-way against the base commit 9bf31c70 — main's page is unchanged since, so the merge
is clean), then `wiki.py index` rewrites the row: the "over budget (1,751 lines, current
best 1,423)" flag disappears. No engine code, no gates, no frozen evidence touched.
Risk: any run that lands between my base and the publish re-adds its `NEW` block on main;
the three-way merge keeps my compile where the base agrees with main and takes the newer
run's hunks where it does not — the next run then compiles its own entry in (15 lines of
headroom).

**Fit with PRINCIPLES.** "Text has a cost … One home per kind of text: *truth now* lives
in the page's current best, *history* lives in git and the runs' branches — pointers, not
copies; delete when built." The compile is that rule executed: superseded prose deleted,
standing numbers kept with domain and run ids, history behind cited runs. Also "Write for
the corporal": the page is now one reading, no possible misreading of which number stands.

**The lens.** A compile lens reads for supersession, not for physics: I adjudicated every
disagreement by the newest measurement and could have retired a subtler claim (the
promotion/demotion and record-stack family, runs 13–15 Oct, survives only behind its run
lines — 15 current-best lines cannot hold 100 runs' constants, and I favored the board's
live rows). The five dossier completions are paraphrases, not verbatim quotes. And the
audit's 30 numbers are the numbers I judged load-bearing; the checker sampling ten of its
own is the independent test of the same property.
