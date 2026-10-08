Working...
Run complete: `lab/results/20261008-1521-quant-97fd/` holds predictions.md (pre-registered), 7 runs with per-frame CSVs, analyze.py (regenerates every quoted number), and dossier.md.

**Claim:** On the flown plane the frame is owned by the view gather — 62–69% of summed frame time (74% at real time) versus 19–26% for all of physics — and a paced frame costs 4.5–6× its hot-loop cost in CPU time, so the repo's hot-loop benches overstate the player's capacity by ~5×; the engine's 5 ms budget holds everywhere except single items that overshoot it 2.2× (10.8 ms fleet/rebind items), a player order is free at p99 (ratio 1.01), and the readout (`b-readout-cost`), not kick cadence, is the frame's owner.
