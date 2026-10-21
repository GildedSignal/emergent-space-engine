# Predictions (written before running work/compile_check.py)

The decisive instrument is `work/compile_check.py`: it assembles the compiled page and
compares it with `lab/wiki/memory-h-live.md` on budgets, run-line preservation, and
digit-token preservation. Cases I did not tune on, and what I expect there:

1. **First-run token loss is non-empty (10–60 tokens).** I drafted the 15-line Current
   best from the old page's claims, not from the token list, so I expect the first run
   to name losses that are pure punctuation variants of the same number (hyphen vs
   en-dash ranges like `0.4-0.55` vs `0.4–0.55`, `2.2-2.5` vs `2.2–2.5`, `84-112` vs
   `84–100`) and methodology numbers (frame counts, load ranges) I compressed away.
2. **No dated run id is lost** — the assembly copies the old `## Runs` lines verbatim
   (only the two dangling duplicates of 4b55/09a1 and the near-exact fc22-a7d0
   duplicate are merged, and the dangling second-checker line is completed from the
   page's own 470f entry). If any id shows as missing, it is an assembly bug, not a
   judgment call.
3. **Line counts:** new page lands at 195–215 lines (115 run lines + ~90 head), so the
   300-line budget passes with large margin; Current best lands at exactly 15 non-blank
   lines by construction — I predict the check counts 15, and if it counts more, the
   cause will be a stray blank-line split inside a line I wrote.
4. **The checker's own sample:** if the checker samples ten numbers from the old page's
   Current best, I predict all ten are findable — either literally (my lines keep the
   literals) or in a kept `## Runs` line. The riskiest samples are the b77d narrative's
   load figures (`9.25-13.79`, `0.4-1.2`) and 1fcf's `359–405`, which sit in one line
   each; I kept all three deliberately.
5. **A judgment call to verify:** the two old italic meta-notes ("[The two 13:30
   entries stand as prior bests...]" and "[The standing record ... retained on main's
   page below this entry...]") carry no supported numbers and are compile-log artifacts;
   I predict dropping them loses zero tokens (their only number, `13:30`, also lives in
   `## Contradictions`, which I kept).

Kill criterion for the run: any LOST token that is a gold- or silver-supported number
which I cannot place in the new page without pushing Current best over 15 lines — then
the page is over-constrained and the compile must be re-derived, not padded.

## Outcome (after the run)
1. Held: first-run loss = 26 tokens, inside the predicted 10–60 band, and the losses were
   exactly the predicted classes (hyphen/en-dash range variants, short-form run citations,
   methodology numbers). 2. Held: zero dated ids lost. 3. Held: Current best counted
   exactly 15; missed on total lines (178 against the predicted 195–215 — Refuted joined
   tighter than estimated, the safe side of the budget). 4. Held, and strengthened: the
   full 559-token set is preserved, not just any ten sampled. 5. Held: the two italic
   meta-notes dropped at zero token cost. The kill criterion never fired.
