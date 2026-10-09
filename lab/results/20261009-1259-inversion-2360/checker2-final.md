Working...
**Grade: gold** — written to `lab/results/20261009-1259-inversion-2360/check2.md`.

**Reproduction** (exact, ~15 s total, <200 MB): applied `work/patch.diff` alone (it is self-contained — the dossier's two-step apply would conflict) and regenerated every decision number: the detector cliff (24/17/10 clumps, 149/36/22 bodies, 1,571/21/14 of 19,900 pairs at σ_e = 5e-3/0.02/0.05), forced-clump soundness (0 misses/0 false on 123 encounters), watch fractions (130/501/1,337), the 68× pairwise crossover, and the degenerate corner (ζ = 0.11–0.12 firing, 63–91% watch, 150–225× worse). Controls 0/0 on 478 raw truth encounters (the dossier's 474 is the edge-trimmed count).

**Predictions**: existed before the decisive run (mtimes 13:08 vs 13:14). Controls, family soundness and σ_e-linear watch held; the bunched-decline mechanism and pairwise-miss predictions failed — both honestly reported, and the pre-registered kill criterion (b) is met in substance.

**My seven attacks** all land on the dossier's side or strengthen it: the cliff is sharp (2/3/4e-3 → 3/10/22 clumps); at σ_e = 0.1 ζ itself declines (1.11) even when clumped — the working band is bounded above too; bunched σ_e = 0.1 reaches a 99% watch at ~3,000× worse; n = 600 confirms blindness at σ_e ≥ 0.02 (0.12% pairs) while chaining softens it near the cliff edge; the dead build's never-run scenes (`equalp`, `ring600`) pass.

**Novelty/goal**: first execution of the adopted gold's never-run module; the finding (engagement hole in the certificate both GLM and Codex are queued to build this week) redirects that build at zero code cost. Errata recorded: the 277-family-encounter count doesn't regenerate (actual 126), and the inherited `with_delta` placeholder bug in `zeta()` (no decision flips here).

Tree restored clean; nothing else in the run folder touched.
