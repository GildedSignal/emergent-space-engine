# Predictions — 20261021-0142-q-compile-cell-rebind-4c5b

Held out before the decisive check (`compile_check.py`): the cases I did not tune on, and
what I expect there. The decisive check is stronger than the gold bar's ten-number sample:
it extracts **every** numeric token from the old `lab/wiki/cell-rebind.md` (fetched from
`HEAD`, since the patch replaces the worktree copy) and requires each to appear in the new
page **or** in one of the four cited runs' branch artifacts (dossier, regen, checks,
predictions, finals).

Facts already verified before this file (not predictions): the four runs' grades read from
branch heads — 9eeb silver, ef8c silver, f7c3 silver, 6e91 gold; `lab/wiki.py`'s budget rule
(`best_lines > 15` or total `> 300` flags; the old page reads 117/47 via that rule).

## P1 — Budget

`wiki.py index` on the compiled page shows no `over budget` flag on `cell-rebind`. I expect
current best at 13 non-blank lines (budget 15), total page ≈ 55 lines (budget 300), and the
index Runs count for the topic to drop 7 → 4 (the three `(awaiting grade)` lines are exact
duplicates of graded lines for the same run ids and fold into them; the README schema is one
line per run).

## P2 — Number conservation (the checker's bar, applied to all tokens)

- 100% of old-page numeric tokens are found in (new page ∪ cited-run artifacts).
- ≥ 90% of the load-bearing constants stay **in-page**: census counts (1,095/1,831/2,141,
  1,731/1,960, 4,096), B13 counts (46/64, 60/64, 47/64, 53/64), the CPU constants (4.95,
  0.641, 7.8×, 3.04–3.36e-5), the 10⁹ cores row (0.15–0.17 → 0.019–0.022), the knot hazard
  (0.80–0.82%), 96.7%.
- The tokens I deliberately leave only behind a cited run are secondary details whose runs
  hold them: 4.84 µs and 0.728 µs (6e91's check2), 382/844 kicks and 4.5e-1/1.8e-2 (6e91's
  checker 2), 167,262 vs 166,985/167,352 kick counts (6e91), β = 0.083, 2.03 MB, 0.20 B/body
  (f7c3's checker), seed-2/3 recurrence pairs (6e91). If any of these is **absent** from its
  run's artifacts too, that is a miss: I then put the number back in the page rather than
  weaken the check.

## P3 — Disagreements adjudicated by evidence

The page must say which run stands where two disagree: 6e91 (gold, measured on the belt's
own 99,699 genesis keys at two scales) supersedes f7c3's 3.7–4.5-compiled-cores composition;
f7c3's served estimate (0.02–0.04 cores) agrees with 6e91's 0.019–0.022. 9eeb's hit-rate
half stands; its adoption half is refuted by 6e91's B13.

## P4 — Formats that could break token matching

Superscripts (2⁻¹¹, 10⁵), commas in 1,095, "96.7 %", "N^0.11", en-dash ranges. The script
normalizes superscripts to `^` and strips digit-grouping commas on both sides; if any format
still resists, I count that token manually instead of relaxing the check.

## P5 — Run lines

The old `## Runs` lines are truncated mid-claim at ≈74 characters in the runs' own proposals
(verified on their branches) — the full claims exist only in the dossiers. The compiled page
completes each claim from its run's dossier, ≤ 20 words, one line per run id, final grade.
Prediction: a reader checking any completed claim against its dossier finds it faithful.
