Working...
Check complete. `check2.md` written: **Grade: gold**.

**What I verified (all from a clean tree, blind to `check.md`):**

- **Provenance, byte-level** — the published 368-line patch applies cleanly to pristine `a838a28`, and all 6 files are byte-identical to the dangling stash objects `a2246852` + `8e5e31a2` (still present in this runner's object store). The first checker's `/tmp` patch was indeed incomplete: 93 lines, zero references to `live.rs`/`h_live.rs`.
- **Reproduction exact** — my own worktree + `regen.sh`: all six rows match the published JSONs on digest, `cut_tick`, and every `h_live` counter; balance identity `created − reabsorbed = live_now` in all six; 58/0 tests with the dossier's exact per-binary breakdown (confirmed twice by two independent runs).
- **Predictions** — `predictions.md` mtime precedes the row JSONs and regen log; all five held, including the swallowed-bullet correction (1/127/283/272 = 0.03–1.17% of resolved kicks).
- **Adversarial (mine)** — unseen seed 7 @ 200 k (rate 0.0322, 0.198 GB extrapolation), seed 42 @ 3 k, extreme 1,000,000 game-s (stock grew only 1.7% for a 5× window, confirming ~t^0.10), double-invocation determinism (bit-identical), and digest invariance re-proven: the unpatched base yields the identical digest `41343a14…` — the ledger is a pure read.
- **Arithmetic** — exponents 0.81/0.84/0.103 and the 0.196–0.213 GB extrapolations all recompute.

**Noted as missed:** the swallowed counter saturates at 283 beyond 200 k game-s (a transient, not an asymptote), the digest-invariance proof was left on the first checker's authority, and the 0.2 GB figure is an upper bound, not the information-theoretic floor.

Worktrees cleaned up; live tree and run folder untouched except `check2.md`; no commits or pushes made.
