Working...
Check complete. Verdict: **silver** — written to `check.md`, with one in-place correction to the author's page.

**What reproduced** (regen.sh exit 0 twice, all numbers exact):
- 196 → 75 lines, Current best 11 ≤ 15, 8 open directions, 17 run lines for 17 distinct runs (was 46 bullets), scratch `wiki.py index` reads `open | 17` with no over-budget flag.
- 179/179 old numeric tokens survive (verified with my own tokenizer, not just the author's script); the 33 extras are 30 completions I traced to the page's own git history plus 3 self-referential run ids — none fabricated. Spot-verified against the authoritative branches: 13c6's and 12db's dossiers match the recovered numbers line-for-line.
- Grades: all 17 re-derived from branch subjects. Notably the page correctly carries **silver** for c78d and 4ff1, whose own `check.md` says gold but whose branch subject records "second checker disagreed" — the author used the adjudicated source.
- The one deliberate content change (killing the "~1800× floor" framing) matches kick-jet's gold a765 exactly.
- Predictions pre-registered; P1's first-draft failure (98.9% < 99%) honestly disclosed; negative control fails as designed.

**The finding that blocks gold** (outside the author's tested range — they ran `index`, never `apply`): I replayed the real publish path. `wiki.py apply`'s Runs union is string-keyed, and all 17 rewritten run lines differ from the old 46, so the union **appends** them: the page would publish as **121 lines / 63 bullets / 17 ids**, undoing the compile's core fix. HEAD's own publish of four sibling compile runs tonight demonstrates it live (bullet counts landed 16→26, 7→11, 85→92, 18→32). The dossier's "one `wiki.py apply` merge; conflicts are impossible" is true but irrelevant — shipped apply cannot delete, only append. The cure is already known and pending in the lab's memory (6ccc's `fold_runs` patch, checker-verified by 691b); landing it, then publishing, is the one step to gold.

**Page correction made**: old OD6's named arms "cold-sky floor plus real dispersion (additive in quadrature with 1885/7bcf); clustered skies" were dropped — exactly the non-numeric loss class the author self-flagged as invisible to the token check. Restored into OD3, marked `[checker 16c3]`; all budgets re-verified (PASS, exit 0).
