Working...
Check complete. `check2.md` written; tree restored to its prior state (only untracked `lab/results/`).

**Verdict: silver.**

What I did in the 30 minutes:

- **Reproduction (exact).** Applied `work/patch.diff`, rebuilt, ran the dossier's commands: the 54-run matrix and 12 play runs are byte-identical to the author's stored output modulo `wall_ms`. The `fixed-input` control equals `direct` at 80 M on all seeds (`49a1b20b…/264b1bee…/9fbcaa5f…`) — I ran the missing `direct`-at-80 M side myself. Code claims verified at cited lines: `session.rs:79–80`, `kick_bench.rs:68`, `server.rs` replay validation.
- **Adversarial cases.** (1) A seeded random interleave of every schedule mechanism (event/wall budgets, frames at 30/60/144 fps × rtf 1/10/100, settles, full-body readouts) at 1 and 8 threads — digests still equal `direct`; the core survives churn beyond the author's paths. (2) 18 extra `thr8` runs — bit-identical, no race. (3) `rtf 1` play, the author's admitted gap: the leak persists (digests split by fps on 3/3 seeds; seed 22's starve case reproduces the ruin form at fixed fps, logged tick 101 490 → 98 128), but the encounter/contact count flips did not appear at rtf 1 in 9 runs — position-level, not history-level, at real-time pace.
- **Novelty split.** Core schedule-independence is H0213's committed result and designed-in by law.md's tie key; the new substance is the measured proof that the shipped, served path (`http.rs:97` → `Session::step`) violates law.md's adopted "never at a wall-derived one" rule.
- **Record error found.** The dossier's claim that HANDOFF "Risks to attack first" names silent nondeterminism as a ruin state is false — no such line exists.

Gold is one experiment away: build the two-line scheduled-game-time decision tick, show the four play paths collapse to one digest per seed at rtf 100 and rtf 1, matrix unchanged.
