Working...
Check complete. Verdict written to `lab/results/20261014-1137-redteam-56cd/check.md`:

**Grade: gold**

- **Reproduced bit-for-bit** in a clean worktree at base + patch; all four arms identical to the author's log, exit 0.
- **Mechanism code-verified**, not just observed: the refusal is `tube.rs:160`, and `do_anchor`'s refusal path rolls everything back without touching `active` — so a refused anchor hands nobody out and never dissolves; the tide keeps reading the stale tube; `run_to` has no other exit. r5's frozen text has no thrust scene; the `space` crate's unbound passages (merged `range` job) exist, so the proposed fix is real.
- **Predictions pre-registered** (file times confirm) and held, with an honest falsification of P3.
- **Five adversarial arms**, including burn direction — outside the author's tested range. Escape at 3 P: 184 refusals, origin 13,247 dr, unbounded confirmed. But the freeze class is **larger than the claim**: a 0.40 v_c *bound* burn and even a gentle *retro* burn (the mirror of the arm called "tracked cleanly") trip the weak-field refusal at the shipped scene — 9/12 members lost, shape 893%. The fix must escalate on persistent refusal; rebinding to an unbound tube alone doesn't cover this class.
- Corrected the author's wiki page in place (three surgical edits: checker's adversarial block in Current best, the Refuted entry's direction qualifier, and the fix-scope note in open direction 1); nothing else in the run folder touched, worktree cleaned up.
