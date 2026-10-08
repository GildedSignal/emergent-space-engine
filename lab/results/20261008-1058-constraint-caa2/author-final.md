Working...
Dossier repaired and complete. All artifacts are in `lab/results/20261008-1058-constraint-caa2/` (bench JSONs, scaling ladders across 3 seeds, kick-bench, gate log, predictions written before the ladders, dossier).

**The claim:** the frame's constraint is not the engine the board optimizes (1.3–7.8 % of frame CPU) but the view gather — an unbudgeted, unculled O(N) scan of every body every frame at 24–35 µs per body (64–89 % share, linear, seed-robust), which puts the frozen 2²⁰-body belt at 25–36 s per frame and the goal's 10⁹ at 7–10 hours, and whose fix is culling by distinction on the doll tree the engine already holds, not another constant shaved off the kicks.
