Working...
Check complete. **Verdict: silver** — written to `lab/results/20261021-0213-q-compile-belt-49ad/check.md` (abstract 116 words, first line `Grade: silver`). Nothing else changed; the author's page needed no correction.

**What I did as checker:**

1. **Reproduced**: `regen.sh` exit 0, output byte-identical to the dossier — 162/69 → 71/7 lines, 242 tokens 0 missing, 19/19 run lines identical, 24/24 citations. Base commit 046d8d9c's page == tree == snapshot, so the compile targets the right page.
2. **Stronger instruments (outside the author's range)**: multiset occurrence sweep — zero substantive losses (25 lost occurrences are all `second-…-`→full-id citation expansion and Current-best/Refuted dedup); reverse sweep for *added* numbers — only metadata, board-row names, and short attributions, all verified correct (2.4 bits/body is 6273's own measured μ_b=10⁻¹⁸ row, not compiler arithmetic).
3. **Adversarial**: 4/4 mutation probes (dropped number, fake citation, padded budget, tampered run line) each fail the audit for the right reason — the instrument has teeth.
4. **The series' gold-blocker, untested by the author**: I replicated `wiki.py apply()` verbatim — clean landing, 0 conflicts, 19 run lines, 0 duplicate ids, budget green, merged page byte-identical to the audited page. The Runs union no-ops because the lines are verbatim; the encounters-9e80 failure mode is absent.
5. **Novelty**: belt's page has only two prior commits (creation; the 12-October initial compile `dbfb` — a different job); this budget compile is new and integrator-queued (`start q-compile-belt 90`).
6. **Why not gold**: no board row moves 10× (maintenance-class, consistent with all nine prior compile grades), and one held-out sub-clause failed on count (7 first-run token misses vs ≤3 predicted — kind held, honestly disclosed). Named gold experiment: fold the run's own `## Runs` line in (memory-h-live convention) and re-verify; beyond that, gold for a compile is a policy call for the integrator, not an experiment.
