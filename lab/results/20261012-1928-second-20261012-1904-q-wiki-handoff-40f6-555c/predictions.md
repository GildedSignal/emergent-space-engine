# Predictions — second-author run 20261012-1928-…-555c

Written before the decisive pass (the page fold, the routing table and the
needle verification). Already measured, so not predicted: 84 in-window hits at
this snapshot (83 at the author's), 593 branches carrying a check.md (589 at
the author's), 25 of the 84 unhomed on every standing page, the six grades
(a7f7/13ae/21db/3d2c/3565 silver, 7a46 gold), `handoff_params_derived` absent
from `origin/main` crates, and the published `lab/wiki/handoff.md` equal to
the run branch's page modulo one blank line.

1. **Accounting closes.** Every one of the 84 snapshot hits takes exactly one
   of: on the original page (11), the original routing (5), a new fold by this
   run (6: a7f7, 13ae, 21db, 3d2c, 3565 r3-v3, 7a46), a superseded-iteration
   line (2: r3 v1/v2, accounted by v3), or a recorded routing/scoping decision
   (the rest). No residual "unknown".
2. **The r3 series splits 3/0.** v1 (453e) and v2 (aac0) are abstract-bearing
   checkers whose content is superseded by v3 (3565); all three matched the
   sweep regex (verified), none is homed anywhere (verified).
3. **New needles hold verbatim.** All ~30 new needles I extract from the six
   folded runs' check.md/dossier.md pass on the first verify run, in the
   checker-corrected forms where a checker corrected the author (a7f7: carry
   drift 97 not 58, 0.095/loop, 80 vs 4172; 13ae: retro boundary stated
   separately, kick-8 3.8% vs avg1Q 46.7% at 0.30 R_H retro).
4. **Nothing retrofits.** The original 96 checks still pass unchanged (they
   read source branches, not the page), and the two count fixes (cluster 16;
   denominator = branches with a check.md, not ~200 abstracts) are the only
   dossier-sentence changes outside the new sections.
5. **Live regen drift is small.** The live sweep at regen time finds ≥ 84
   in-window hits and every hit at or before this snapshot stays accounted;
   branches landing later are listed, not failures.
6. **The published neighbours already homed the original five.** 1381/8d6e/11de
   appear on the published kick-jet page and 24cd/97bf on frame-cost (the same
   publish batch executed the original routing), so this run records rather
   than re-routes them.
