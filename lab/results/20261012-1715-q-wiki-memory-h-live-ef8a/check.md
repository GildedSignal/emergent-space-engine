Grade: silver

**Abstract.** Compiler run: the memory-h-live page from 82 primary runs. Reproduced myself: regen.sh exit 0 (111 = 82 on-topic + 24 off-topic + 5 ungraded; 106 abstracts; every Runs grade matches its branch's check.md; all ids and abbreviations resolve; all claims ≤ 20 words). predictions.md (17:23) precedes the page (17:26); all six predictions held. Sampled seven claims against the branches (9d49, 0820, cae7, 4a62, b946, c9fa, 09a1) — every number faithful; the c9fa/b946 regime adjudication is supported by both golds' own records. My attack outside the author's 111-run cluster (535 further October branches swept): ≥ 3 on-topic primaries are missing — fermi-1feb, fermi-2914, components-6273 — none compiled on any wiki page. The current best is unaffected. One sweep-and-fold step from gold.

## Reasons

**Reproduction.** Re-ran `regen.sh` in place: exit 0, identical output (106 abstracts; partition exact; verify OK). `work/patch.diff` is empty as claimed (0 bytes; the run edits nothing shipped). The partition is internally exact: every one of the 111 runs is on-topic, off-topic or no-check.md exactly once; the five named ungraded runs and b-h-live-1599 (branch commit subject "Grade: missing", no check.md on branch — verified directly) are accounted for.

**Predictions.** File times: runs.txt 17:17, gold-dossiers.txt 17:19, predictions.md 17:23, dossier.md 17:26, wiki page 17:26 — written before the page, after the sources, as claimed. All six held: (1) partition 82/24/5 reproduced mechanically; (2) c9fa (gold: compute-bound, 90-min corner, RTF 100) and b946 (gold: memory-bound, compute 0.024 cores at belt scale) both unrebutted and reconciled by regime — b3e7 (gold) measures the ordering; (3) the 3-field/4-field floor split confirmed in 0820's abstract (125.5/126.1 bits/body = 15.7/15.8 GB; phase t_p 64 bits/radial cycle); (4) standing-representation cluster confirmed (cae7 1,245–1,277 B, `Catalogue::insert` never dedups; 4a62 median 1,456 B, 448 B record + 528–968 B shape); (5) scar-family reconciliation carried by b3e7 (S = 61.2 → 172.5, magnitude-dependent); (6) b30e/8072 legal-resolution confirmed (8072: KS 0.031, p = 0.29, gold).

**Claim sampling (7, against the run branches).** 9d49: convoy 17.2–29.6 / first scar ~70–78 / individual 149.7–196.6 / 9.5–12.9% at 4 GiB — matches. 0820: matches verbatim. cae7: matches, including the 2,000-ships-one-orbit observation. 4a62: ~90×/175×, 1,456 B — matches. b946, c9fa, 09a1: match. The m_crit quantum-threshold sentence is a fair reading of the two runs' own definitions (c7eb thresholds at the (E,L) element quantum; 4b55 at the scar quantum); it stays out of Contradictions, with the author's "explained, not measured" flag on record in the dossier.

**Novelty.** The live page (lab/wiki/memory-h-live.md, `updated: 09a1`) held only the 2-run 4b55/09a1 result; HISTORY's wiki entries are the wiki's creation and the 16:21 publish only. This compile is new and the baseline paragraph is preserved rather than rewritten.

**The attack that found the gap (outside the author's range).** The author's universe is the integrator's 111-run cluster plus 4 recoveries; the repo holds 646 `claude/lab-*` branches, 535 of them outside the cluster, 453 in the author's own 6–12 October window. A keyword sweep of those dossiers' heads (memory terms) followed by reading the hits found ≥ 3 memory-h-live **primary** runs absent from the page and from every other wiki page:
- 20261010-1816-components-6273 (silver) — dossier titled "H_live measured": stirred-belt store is rate × kernel, crossover mass ~a 1-km rock below which mutual encounters create zero distinctions, saturated 2.2–2.4 bits/body after 100 orbits (0.3 GB per 10⁹). This is a direct precursor of the page's 07b4 gold (1.7–2.4 B/live-body) and supplies a measured point inside the page's own open m_crit range (10¹²–10¹⁸ kg, open direction 6).
- 20261010-1706-fermi-2914 (silver) — H_live bounded by the current binding (~15–25 bits/body, ~20 bits/kick), anticipating the page's saturation golds (91a0/e4cc).
- 20261007-1843-fermi-1feb (silver) — the first H_live creation-rate estimate; the page lists its checker (ece4) while omitting the primary itself.

None overturns any Current-best line; all are superseded or confirmed by later golds already on the page. But a topic ledger that misses a run titled "H_live measured" is not yet the topic's certificate, and my sweep read only the first 2.5 KB of each dossier — the true miss count is ≥ 3, unknown above. The author's lens note ("runs never keyword-tagged memory are absent by construction") does not cover these: all three self-identify as H_live runs in their claims. The author recovered 4 runs outside the cluster by following citations; a full-branch sweep (6 s of compute here) was in scope and was not done.

**Page.** Left unchanged. The gap is omission, not overstatement, and folding the three lines now would break the run's own verify.py (hard-coded 82 Runs lines) with no way to fix it inside my mandate; the successor folds them and bumps the count.

**Goal fit.** Real: the integrator reads one page instead of ~80 dossiers ("Text has a cost", #11), the board's "~62 bits" line is sharpened to the measured 61.6–62.1 (3-field) vs 125.5–126.1 (4-field, phase irreducible) split ("The memory floor is information", #24), and the admission/census rule is the compiled form of "Compute only surprises" (#3). The Domain paragraph is honest about assumptions (128 bits/rebind, ~10 bits/s player) and untested regimes.

## The one experiment that would make it gold

Sweep all 535 non-cluster branches (full dossier text, not just the integrator's cluster and not just heads) for memory-h-live primary claims; fold every hit into Runs (and Current best where it adds: 6273's crossover mass belongs in open direction 6's m_crit map); update verify.py's expected count accordingly. The three named above are the known minimum.

## What the author missed

1. The three on-topic primaries above (6273 is the material one: a measured m_crit-map point and the precursor of a gold the page already carries).
2. The primary/checker asymmetry (1feb out, ece4 in) — the cluster was followed, not the topic.
3. Cosmetic: regen.sh's echo says "5 runs were never graded" while 6 branches lack check.md (1599 included); the dossier's own accounting is correct.
4. The head-only nature of any sweep (mine included) — full-text sweep is the successor's job.
