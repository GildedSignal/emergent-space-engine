Working...
Check complete — `Grade: gold`, written to `lab/results/20261020-1210-spacex-624a/check.md`.

**What I did:**

- **Reproduced:** applied `work/patch.diff` at base `caa2a43b`, re-derived every dossier number from the raw regen JSONs — fleet 1,104,124 knots / 105,241 panels touched exactly, never-landed 90.0%/93.5%, medians 14.3%/0.68%, tail 39.8% of cycle knots at 5.1% median — and ran the full-walk control test myself (1 passed). Digest neutrality holds on all three arms. The author's saved decisive rows are bit-identical to the runner's regeneration (18,967/18,967): no post-hoc instrument change, and predictions.md predates the decisive data.
- **Instrument audit:** code review of every readout path — all panel landings touch the census (`outbound_at`, `at_radius` refine, `crossing_state`, passage inner arcs); tails are a separate vector correctly counted as tail hits; sum-word reads honestly excluded. Complete.
- **Adversarial (4 arms, ~113k more mints):** rtf 1000 (outside the swept range), seed 7, members 4/rtf 1, 55 s. Never-landed stays 81–98%, medians 12.5–20%/0.7% — the claim holds everywhere. Found the one overstatement: the absolute "0 mints ≥ 0.9" is domain-bound (a 0.007–0.07% cycle tail outside the tested range); pricing untouched. Also caught a count slip: 21,520 mints, not 21,449.
- **Novelty:** the topic page itself marks the traversed fraction "NOT yet measured" (od 1); 4ea0 scoped exactly this as unmeasured. This is the named decider, and it kills the class-split fork while pricing the lazy lever 4–7× (ceiling ~10×) on both scoreboard rows.
- **Page corrected in place** (two bracketed checker notes), tree restored pristine, nothing else touched, no git operations.
