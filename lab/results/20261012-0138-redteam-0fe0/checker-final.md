Working...
Check complete. `check.md` written to the run folder; nothing else there touched; no git operations.

**Grade: silver.**

**Reproduced exactly** (patch applied, clean tree):
- `redteam_flyby`: all four variants — contacts 216/230/217/233, epochs 33, rebuilds 3/2/2/2, digests `1f8e2ebdefd6`…`14d552ffc197` — bit-identical to `flyby.out`; v0 digest equals the shipped `identity s1` digest.
- `view_newton.py`: 3.00 iterations/frame at every β, 0.05 s.
- `predictions.md` mtime (01:44:16) precedes the decisive output (01:49:15); archived test copy ≡ patch.

**My adversarial cases** (in `work/checker-patch.diff` as `checker_adv_flyby.rs`, `checker_probe.rs`):
1. β at the subluminal boundary (k = 1023/1024), mass 1000, seed 7, 4 threads (digest equals 1-thread), lone pair — **identity holds everywhere**; epoch-shift control fires. The premise is stronger than the dossier claims.
2. **One dossier claim is false**: in the author's exact v3 world (digest reproduced) the two interceptors never contact each other — each is deflected by fleet bodies (6 contacts, β_rel ≈ 0.75–0.8). A lone pair shows the plain lattice *does* hold the head-on contact (t = 480 exactly), but the extent-driven frame's genesis rotation (ω·x ≈ 13 cells/tick at r = 432 000) deflects it by ~10⁴ cells. "Guaranteed near-c pair contact" was never checked against the event log.
3. View gather: cold/stale Newton seeds leave the bracket in 2 iterations at β ≥ 0.9 — the warm start is load-bearing, not merely cheap.

**Why silver, not gold**: no premise fell, nothing deleted, no 10× moved — the actionable findings (stale §1, missing view gate, single-checked re-anchor gold) are integrator text decisions needing no run; and "the attack it had never faced" overstates — H0168's `crates/lattice-event/tests/relativistic.rs` already proved stepper equality at 0.88c heterogeneity (what's new here: that scene class inside the Battle/Frame/epoch-kick machinery). The named experiment to gold: attack the residual exposure the run itself names — a relativistic body handed off out of the frame's size rule, where bit-identity has never been exercised and can actually break.
