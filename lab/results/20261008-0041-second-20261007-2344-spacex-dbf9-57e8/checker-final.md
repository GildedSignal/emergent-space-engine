Working...
Check complete: **Grade: gold**, written to `lab/results/20261008-0041-second-20261007-2344-spacex-dbf9-57e8/check.md`.

What I verified, independently:

- **Provenance.** The published `code/live-ledger.patch` is byte-identical to the two dangling stash objects (`a2246852` tracked, `8e5e31a2` untracked), both stamped 23:56:40 at `a838a28` — the exact state that produced the original table. The first checker's `/tmp/spacex-dbf9-recovered.patch` indeed lacks the two new files.
- **Reproduction.** Clean worktree, patch applied, build 47.5 s, `cargo test` 58/0. All six rows reproduce exactly — every counter and every digest — plus a digest-identical rerun (third invocation, third tree).
- **The corrected bullet.** My runs print exactly 1/127/283/272 swallowed; the original "0 in every run" claim is dead as the dossier says, and the ≥98.8 %-move-the-tube substance survives.
- **Adversarial.** Seed 9 at 30k (rate 0.182, balanced, swallowed 1.54 %), 400k game-s (rate 0.0207, stock 5,313 — the fall continues), and 550k where the scene itself ends (player lost near 430k: a window limit, not a defect).
- **run.sh fix.** `work/patch.diff` applies; the `mkdir -p "$out/work"` one-liner is the correct cause-level fix.

Nits recorded for the integrator: the "1.17 % of resolved kicks" denominator is really rebinds (1.18 %) and is seed-dependent (1.54 % on my seed 9 → "≥ ~98.5 %" is the honest phrasing); the dossier was saved ~40 s before the regen log closed; the ~430k-game-s scene horizon bounds the measured asymptote. None touches the decision: ~0.2 GB of scars per hour for 10⁹ bodies at plane density, interactions not N.

My worktree, target dir, and scratch files are removed; nothing else in the run folder or the tree was changed.
