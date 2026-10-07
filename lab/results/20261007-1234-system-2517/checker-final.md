Working...
Check complete — `check.md` written, nothing else in the run folder touched, no git operations.

**Grade: gold.**

What I did:

**Reproduced (clean tree, no patch needed):**
- Digests bit-for-bit: `a0096d59e1` (members 48, rtf 100) across engine-ms/threads/pace — including a knob combo (e1/t1/unpaced) the author never ran; `bfacdfc5bb` (members 400, rtf 1000) at e5 and e2.
- The cliff: rtf median 309.6 → 0.098 with events/s budget-proportional (3071 → 1315), h16 = 0 everywhere.
- Held-out seed 3 (author used only seed 1): digest invariance and the cliff both hold (1000 → 0.020).
- Wave claim in direction: engine p99 3.75 ms (4 threads) vs 1.90 ms (1 thread).

**Mechanism — proven beyond the author's code reading:** my differential at fixed budget/load (rtf 1000, engine-ms 2): members 4 → rtf 1000.0, members 100 → 0.31, members 400 → 0.098. The presentation collapse is caused by *the fleet's* deadlines clamping the global horizon (`advance` 822–833), exactly the rule-8-rung-2 defect the dossier names.

**Caveats recorded in check.md:** the headline "523 305 → 845 (~600×)" statistic is computed on the trace's `target` column, not presented time (horizon median 524 206 → 59; the true collapse is ~10⁴× — understatement, not fabrication); the allocator-unreachable finding was already in HANDOFF's 7-October deletion note; report JSONs don't record `threads`; the horizon's bimodal 2^19 stroboscope jumps (missed by the author) strengthen the case for the rung.
