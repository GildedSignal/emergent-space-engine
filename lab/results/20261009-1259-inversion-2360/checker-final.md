Working...
Check complete. **Grade: gold** — written to `lab/results/20261009-1259-inversion-2360/check.md`; tree restored to a838a28 clean.

**Reproduction** (only this run's `work/patch.diff` — the dossier's "apply the dead build's patch first" would double-apply, since the run's patch contains it bit-identical): every verdict-carrying number reproduced exactly.

- Controls: 0 misses / 0 false (my truth count 478 vs the dossier's 474 — tally slip).
- Cliff: 24 clumps/149 bodies/1,571 pairs at σ_e=5e-3; 17/36/21; 10/22/14; bunched 20/41. `binet()` and `eps_max` confirm the ρ-scaled full-Binet-L1 mechanism in code.
- famf soundness: 0/0 on 123 encounters, watch 0.65/2.5/6.7%, pairwise 68× cheaper at σ_e=0.05 (375.7 vs 25,571).
- Degenerate corner: ζ 0.12 fires, watch 62.7/91.4%, 154×/224× worse than pairwise, 0 misses. Unit tests 5/5.

**Adversarials** (my own `famx` set + a full-truth probe):
- σ_e=3e-3 pins the cliff as a ramp (71% of pairs still covered).
- σ_e=0.15 forced: ζ=1.9 **declines** — the degenerate-fire corner is a band, not all high-e.
- n=400: coverage grows 7.9%→34% — the "92% blind" and 72 TB figures are n=200-scale; percolation at 10⁶ likely yields one giant fired clump whose watch is still n²·fraction (ζ is asymptotically n-independent). The structural conclusion survives, stronger.
- σ_λ=0.01 (dropped from the shipped scenes): watch 97.9%, 243× worse.
- Full truth over all 19,900 pairs — the probe the author skipped: only 1/2, 0/3, 2/30 real family encounters lie inside fired clumps. "Never engages there" holds in the strongest sense.

**Gold over silver:** premise break of an adopted design (engagement logic, not the watch's math) with a one-step fix (U-clumping, dormancy-priced ζ, fluid corner), landing one step before both queued co-orbital builds; failed predictions were disclosed and don't underwrite the claims. Flagged for the integrator: the "400/474/277" tally sloppiness, the single-scale 10⁶ arithmetic, and the unreported `equalp`/`ring600` sets.
