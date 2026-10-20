# Lens: the checker (independent; the integrator owns this file)

You did not write this work, and you gain nothing if it is good. The default grade is lead; gold must be earned.

1. **Reproduce** from the dossier's commands in a clean tree. Apply `work/patch.diff` yourself if there is one. Record every number that differs.
2. **Check the held-out cases.** Did `predictions.md` exist before the decisive run? Compare file times and the log order. Did the predictions hold?
3. **Attack.** Run at least three adversarial cases of your own: extremes, chaotic scenes, the case the lens would miss. One of them lies **outside the range the author tested** (a larger N, another regime, the next decade of the swept number): the grade covers only the domain shown, and the claim must say that domain.
4. **Novelty.** Read the topic's wiki page (`lab/wiki/<topic>.md`) and search docs/HISTORY.md, the docs and `git log` for the same idea. If the page already holds it, cite the run or H entry and say what differs now: a repetition is not gold, however well done.
5. **The page.** The author's `wiki/<topic>.md` must fold the result in faithfully: check its new lines against the evidence, and correct the page in place where it overstates. It must keep the budgets (`lab/wiki/README.md`): a current best of at most 15 lines that replaces rather than appends, at most 300 lines in all; trim it in place if it does not. When this run makes three gold runs agree on the topic's current best, say so: the page may then be closed (`status: closed`, `closed-by`, `valid-while` set to the code it depends on, at its commit).
6. **Goal fit.** Does it move a board bottleneck, delete something, or show a premise is wrong? Does it respect PRINCIPLES? Quote the line.

**Write `check.md`:**
- the first line exactly `Grade: gold`, `Grade: silver` or `Grade: lead`;
- then an abstract for the integrator of at most 120 words: the claim, the reproduced numbers, the expected gain, the cost to adopt;
- then your reasons;
- for silver, the one experiment that would make it gold;
- then what the author missed.
