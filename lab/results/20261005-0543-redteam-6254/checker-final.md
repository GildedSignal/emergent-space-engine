Working...
Check written to `lab/results/20261005-0543-redteam-6254/check.md` — **Grade: silver**.

**Reproduced (nothing differed):**
- `order-falsifier` (patch applied, clean tree): both laws, full velocity inversion, worst |dk| = 16384 = 2|k| — exactly as quoted.
- `exp_gas.py`: all five sharing rates (22.5→82.3%), cascade 1.4→19.2→87.7%, median |Δv|/|v| = 1.230, in 5.5 s.
- Every doc citation verified (law.md 7/40/42, representation.md §1/§3/§7, lattice-event:42, gpu.rs:556); `lab/rungs/` really has no r5/r6; no existing test feeds a non-canonical order (`components_resolve_independently` tests locality only).

**Adversarial findings that set the grade:**
1. The 22–82% headline counts all overlapping pairs; the law's own detector (`hit`: approaching-only) and `resolve` (skips separating) act only on firing pairs. My rerun with the approach test: **5.7–36.8%** — ~2–3× lower, though still common at every density.
2. "Two legal orders" is imprecise — `resolve`'s contract requires sorted pairs; the hole is the missing batch-collector key above the law, not the law.
3. plane.md (operative doc) is unaddressed: it reinstates a canonical root clock and asserts "deterministic ties" — the gap survives (no key stated anywhere), but the "abolished the tick" framing targets the older doc.
4. Novelty is partial: H0159/H0161 already chose sequential impulses and implement the canonical batch rule; H0173 already owns the cascade result, uncited.

**Why silver, not gold:** the finding is a missing rule in the text plus a real measured commonness — but no new-design engine exists to falsify, and the author's own "what would make it wrong" concedes the implicit-carryover case is silver. The one experiment for gold: build the slack-ordered one-at-a-time queue as specified and show its digest forks from the tick-batch digest on a dense scene.

Tree restored (patch reversed, my variant example removed); no commits, nothing else in the run folder touched.
