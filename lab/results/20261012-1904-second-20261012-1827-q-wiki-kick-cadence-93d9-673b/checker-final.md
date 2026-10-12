Working...
Check complete. **Grade: silver** — written to `check.md`, with the page corrected in place.

**What reproduced exactly:**
- `regen.sh` green twice over (43 runs listed, 157 needles, 0 failures, tally 9 gold / 29 silver / 4 lead / 1 missing — all script-derived from the page); `sweep.py` regenerates `sweep.jsonl` byte-identically over all 654 branches; tree clean at the recorded base, patch empty.
- All 43 page grades equal their branch grades; the 25 original 93d9 run lines are byte-identical (append-only holds); routing verified (`kick-jet.md:31` points 67f2 back).
- `predictions.md` (19:05:32) predates the sweep (19:05:44). P2 held exactly; P1 failed honestly (18 found vs the checker's 6); P3 failed interestingly — the 524e-vs-54d9 contradiction is entered live with a named deciding experiment.
- Deep-sampled folds (524e, b7a4, 67f2, 8685, 0510, 83f9): every number in the right direction, checker caveats folded. 67f2's kill is upheld by its own gold second check.

**Why not gold — the attack that landed:** the sweep extracts abstracts via `\*\*Abstract\.\*\*`, so **99 of 572 graded branches have empty abstracts** — invisible to the author's two keyword passes and to any abstract-based pass; the signal sat in the author's own `sweep.jsonl`. Screening those 99 branches' claim lines directly, I found three graded, cadence-primary, unhomed runs off the page: **aa78** (kernel floor 8/orbit, "the 16× sits in `step_log2`" — number duplicated via 27ce, run and its resonance extension absent), **ef10** (output-only correctors buy a solid 2× fewer kicks in the strong-tide regime — on no page in any form, and it regime-qualifies the "correctors buy nothing" shorthand), **76d6** (leapfrog needs fewest kicks/orbit; nothing passes at e = 0.9 ≤ 192/orbit). The dossier's own "what would make it wrong" names this failure mode, but the claimed mitigation cannot see it — so "nothing cadence-primary is left off the page" was overstated. I scoped that sentence on the page (three ids named); regen stays green. Borderline exclusions (a7f7, bb60, 5b6a, 1eca, 3ea5, e04a, 2ef5) I judged defensible and recorded for the integrator.

**The one experiment for gold:** one git-read-only pass — extract claim lines for the 99 empty-abstract branches, fold aa78/ef10/76d6 with needles and caveats, judge the borderline homes explicitly. Seconds of compute, no simulation.
