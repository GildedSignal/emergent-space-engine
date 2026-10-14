Working...
Check complete. `lab/results/20261014-1719-dynamics-bf21/check.md` written; tree restored.

**Grade: gold.**

**Reproduced** (patch applied myself, beyond the runner's regen):
- Digest `ba1a66b4…` identical across **clean tree / patched-unset / capped** — the patch is default-neutral and the cap changes no canonical bit; encounters 4060 = 4060, kicks 225975 = 225975 in every run.
- Monster frames: baseline 1202–1660 ms across runs (author: 1364.9; ±30% shared-box noise) → 11.96–12.02 ms capped. "114×" is 100–138× on reproduction — same order; "0 frames over" is marginal at the budget edge (one 12.02 ms frame in one run).
- Train anatomy confirmed from the regen log: first items 13,051/14,072/14,542 all `Kick(0)`, recurrence 26,101/28,145/29,084, steps a continuum (predictions 1/3 honestly failed as reported).

**Adversarial (mine):** held-out seed 7 (digest `6ad7a1fa…` equal, 1416→12.1 ms) and N=4×10⁵ outside the author's range (3276→12.0 ms, 61,701-event items, 1.88 GB RSS — at this box's ceiling) both hold. Cap-margin probes: `ES_PULL_CAP=0/1` stay digest-identical — the neutrality is **structural** (the scan's candidates never overlap the wave backlog on these scenes), not a tuned margin — but the frame profile is not cap-monotone: cap 0 leaves 734 ms monsters, cap 1 leaves 94 ms.

**Corrections recorded:** the dossier's "`64` → any small bound" adoption claim is refuted (64 is a measured operating point); the patch's comments describe a capture-deferral that is not in the code (`let _ = backlog;` is dead — the capture is immediate; the digest holds because of what the scan reads); the wrong-variant numbers (4,029 encounters) are the author's killed build, not rebuilt. The author's wiki page got a checker bracket with these bounds; the untested exposure is a player flying inside the belt band during a wave.
