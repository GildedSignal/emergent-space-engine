Working...
`check2.md` written. Verdict: **gold**.

**What I did (45-min budget):**
- **Reproduced** in a clean tree (patch empty, shipped binary): E0 digest `f8b75cec…` full 64-hex match; paced M384 s1 → `dd178af9…` with cpu_worst 17.62 vs stored 17.63 and cpuH [1,0,0] both; unpaced 30 s → same digest, same 1,800 frames, wall 7.9 s.
- **Recomputed** all 40 stored ladder runs independently of the author's `analyze.py`: every median, range, guard count (6/40 wall−CPU gaps; 0/40 gather-stalled) matches.
- **Held-out cases (mine):** fresh seeds 9/10 at M400 (no cliff: cpu_worst 16.5/17.2, 0–1 hitches, share 0.61–0.63); cadence tax at a second point (×2.59, same digest); spinner at M384 s1 (digest equal, cpu_worst −48%, engine cpu p50 0.44→0.15); members-4 extreme (share 0.77 — gather dominance even stronger below the ladder). All held.
- **Provenance:** predictions.md predates all data files; the author's mem768 JSON indeed carries 0 CPU hitches under its 23.25 ms gather max, grounding the cliff refutation.
- **Found one letter error:** claim says cpu_worst medians "15.2–17.4 at every point 212–424" but its own M400 median is 14.57 — favorable direction, noted.

Gold path: premise-wrong — the original silver's compute cliff is a contention artifact, the gather is the dominant CPU term (0.55–0.68) with the 60 Hz cadence tax ×2.5 measured, and the queued `b-readout-cost` build gets a correctly-sized work order (budgeted, deferrable, idle-time-fed). Nothing else in the run folder was touched; no git commands run.
