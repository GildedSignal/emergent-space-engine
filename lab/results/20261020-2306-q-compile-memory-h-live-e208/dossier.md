# Dossier — 20261020-2306-q-compile-memory-h-live-e208

## Claim
`lab/wiki/memory-h-live.md`, the lab's most over-budget page (587 lines, 333-line Current best), is compiled to 178 lines with a 15-line Current best, zero lost numbers (all 559 canonical digit-tokens outside the old `## Runs` present in the new page), all 110 dated run ids kept one line each, all 25 refuted entries kept plus 1 added, 7 ranked open directions — verified by `lab/wiki.py`'s own budget rule.

## Bottleneck
The wiki's own budget rule (`lab/wiki/README.md`, 20 October): an over-budget page "is compiled back under it before it takes new runs". This page was flagged the worst on the index (587/333) and therefore blocked every future memory-h-live run. No physics was re-measured; the deletion is of duplicated history, compile-log artifacts and superseded narrative, exactly the "runs prepend instead of replace" disease the budget names.

## Evidence
All numbers regenerate via `./regen.sh` (runs `work/compile_check.py`, < 1 s; it rebuilds `wiki/memory-h-live.md` from `work/head.md` plus the run lines of the original page and re-checks):

- Old page: 587 lines, Current best 333 non-blank lines, 115 run lines (113 dated, 3 duplicate ids), 25 refuted entries. New page: **178 lines** (≤ 300), **Current best 15** (≤ 15), **112 run lines** (110 dated + 2 checker lines), **26 refuted entries**, **7 open directions** (≤ 8).
- **Numbers: 0 of 559 lost.** Every digit-bearing canonical token outside the old `## Runs` section appears in the new page — stronger than the lens's criterion (a checker samples ten; this is the full set).
- **Run lines:** every dated id preserved; the three merges are (a) two dangling half-lines of 4b55 and 09a1 whose complete lines already exist later in the section, (b) a near-exact duplicate of the fc22-a7d0 gold line; the dangling second-checker line was completed from the page's own 470f entry (text shown in `work/compile_check.py`).
- **Refuted:** all 25 old entries kept (verified structurally, first-60-chars match, 0 absent) + 1 new entry (4b8c's "m400 = m800" saturation reading → the `--members` CLI clamp), and the old dangling bimodality entry restored to its full quoted claim.
- **`lab/wiki.py index` dry-run on the compiled page** (sandbox copy, real `lab/wiki/` untouched): no over-budget flag, 110 runs, `updated:` = this run.
- Supersession decisions, each kept as a one-line Refuted entry with its refuting run: b77d's 475 B/candidate and superlinear pin → flat 226 B × C (1fcf); 470f's "machine-load-dependent" → utilization (b8e2); both 13:30 pins as absolute numbers → quiet-subtracted pin(m) (b8e2); count-cap-as-fence → byte fence (b8e2/1fcf); prune-starvation → wall-owned cleanup (4b8c/7bd9 checker).

## Predictions
Written before the decisive check (`predictions.md`). Held: first-run token loss non-empty and in the 10–60 band (actual: 26, mostly hyphen/en-dash variants and short-form run citations); zero dated ids lost; Current best counted exactly 15; the two dropped italic meta-notes cost zero tokens. Missed: total line count landed at 178, below my 195–215 band (Refuted joined more compactly than estimated) — a harmless miss on the right side of the budget. The kill criterion (a gold/silver number that cannot be placed within 15 lines) never triggered: every one of the 559 tokens placed.

## What would make it wrong
- Token presence ≠ claim context: the check proves each number string survives, not that it still qualifies the right claim. Mitigated, not eliminated, by the structural checks (all refuted entries and run ids kept verbatim); a checker reading a specific number's surrounding prose is the real test.
- The two merged dangling run lines could in principle have carried a distinct claim the complete lines do not; I read them as truncations (they end mid-clause and duplicate later complete lines verbatim in their opening words).
- Publishing cost: `lab/wiki.py apply` merges this page three-way against the page the run started from; since this run rewrites the same file's whole body, the integrator should expect a large diff or conflict there. Zero code changes elsewhere.

## Fit with PRINCIPLES
"Text has a cost … One home for kind of text: truth now lives in … rewritten in place and hold no change logs" — this is that rewrite. "Delete when built": the compile-log artifacts (italic meta-notes, `NEW` preambles, superseded pins) are deleted with their content moved to Refuted or left behind the cited run. "Survive compaction": the page is the lab's durable memory; a 333-line Current best is what does not survive a context window.

## The lens
What a compile lens may have missed: readability. Fifteen dense lines (some ~2,600 chars) satisfy the letter of the budget and the wiki's existing style, but "a reader can act on in one reading" is a stronger demand than line count measures — the checker should read line 2 (the fence) and line 6 (the mechanism) cold and confirm an author could pick up direction 1 from them alone. I also did not re-verify any cited number against its run's branch (out of scope for a compile, but a number transcribed wrong decades ago now persists in tighter prose).
