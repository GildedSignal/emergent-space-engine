Working...
**Grade: gold** — written to `lab/results/20261010-1029-taleb-5c01/check.md`. Tree restored (patch reverse-applied, `git status` clean), scratch files removed, nothing committed.

**What I did (30 min budget):**
- **Reproduced bit-for-bit** from `work/patch.diff` on a clean tree: adj control 5/234 (2.1%), dilute fleet 284/1407 (20.2%), 2-orbit 281/2250, 20-orbit 162/8279 — the miss count stays pinned while truth grows 6×, exactly the dossier's edge signature. Also reproduced k=256 (own edit of `pairs.rs` k=32→256, then reverted): 5 and 284 again.
- **Adversarial fresh seed 77** (author never ran it): 288/1365 (21.1%) — holds.
- **Independent-language attack:** my own python Kepler recomputed all 125 dumped missed pairs across three scenes — every one has its true minimum *exactly* at t=0 or t=H (worst edge-distance fraction 0.0), sub-ρ at that edge, zero interior. That verifies both the isolation and the proposed fix (edge checks catch 125/125).
- **Mechanism read in main:** `run_section` (method.rs:67) evaluates only steady-state conjunction offsets from `base`; nothing checks the boundary instants — consistent with the drops.
- **Novelty:** HISTORY clean; located run 0306-taleb-8af8's "missed 0 encounters on every scene" (dossier line 56) — its Halley-truth reconciliation is the one argued-not-run piece, disclosed by the author.
- **Predictions:** mtime order confirms written before all outputs; P2/P3 failures are the anti-guard finding itself, honestly scored.

Gold despite failed P2/P3: the positive control held, nothing was post-hoc, the finding overturns a premise (0306's zero-miss; the gold 09b5 "concentration corner" framing), and it's adoptable in one step. Caveats named in check.md: the 0306 reconciliation is one command away, and the "~0 cost" fix is actually +~33% evals in the dilute regime where setup is cheapest.
