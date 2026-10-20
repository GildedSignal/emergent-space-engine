Working...
Check complete. **Grade: silver** — `check.md` written, the author's page corrected in place (still 178/15, under budget), nothing else touched.

**What reproduced exactly** (`regen.sh`, exit 0, < 1 s): 1,751 lines/201,305 B → 178/52,141 B, 15-line Current best, 186 duplicate run lines → 100 one-per-id, 4/4 restored-checker annotations, `wiki.py index` sandboxed reads `open | 101` with no flag. Predictions preceded the decisive run (22:04 vs 22:12). Completions grounded (7581 vs its branch dossier; 03f4 vs the old page's own NEW block). Spot-checks of every new-page number absent from the old page in exact format all trace to old-page facts — no inventions. My own 10-number sample: zero lost (4 live behind kept run-line pointers).

**Why silver, not gold — two defects found by attack:**

1. **The stated adoption path re-breaks the budget.** I replicated `wiki.py apply`'s exact merge under the author's own scenario (base == main). The body merges clean, but the Runs section is a *literal-line* union: main's 186 lines stay and every refreshed (44) or completed (15) line is appended beside its old variant → **246 run lines, 145 duplicates reintroduced, 322 total lines — `wiki.py index` flags `over budget` again**. The dossier's "the flag disappears" is false on the shipped tool; the page is adoptable by hand, not by the named path.
2. **Grade tokens: 9 of 100 wrong or missing.** 4 lines carry no token though their branches grade them (7497/79ca/dd75 gold, 1a46 silver — `refresh_grade`'s regex misses the `(second author):` form); 4 say silver where the branch says gold (re-graded before this checkout, never refreshed); 7f99 says gold, branch says silver. The "grades refreshed from the branches" headline overstates; branch truth is 30 gold/68 silver/2 unresolved, not the claimed 67/29.

Minor: P4 predicted five truncated lines, 15 were found, and the dossier reports the prediction as "held".

**The gold experiment:** make the Runs merge id-aware (or adopt by direct replacement), refresh all tokens from branches, then run the real `wiki.py apply` + `index` and show the row with no flag. Novel (first of the eleven queued compile jobs to land), directed, PRINCIPLES-fitting ("Text has a cost … delete when built").
