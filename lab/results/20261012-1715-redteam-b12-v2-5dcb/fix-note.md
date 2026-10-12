# Fix record (regen.sh repair, 12 October)

The original `work/patch.diff` was empty (0 bytes): the author's edits lived in a
removed /tmp worktree, so run.sh's patch capture recorded nothing and `git apply`
exited 128 ("No valid patches in input"). `regen.sh` itself was correct.

The fix rebuilt `xtask/src/behave/rt_b12.rs` and its `#[cfg(test)] mod rt_b12;`
wiring from the run's own record: the 7 test names and their full printed output
(`work/rt-all.log`, the author's captured run), the dossier's stated error shapes,
and the candidate branch's shipped code (`b12_stat::arrow`/`pooled_score`/
`inject_leak`, `handoff::b12`/`kept`/`coarse_times`, `laws::lay`/`Events`).
Anchors that are exact by construction: echo, planted-bounded and planted-compound
are shipped laws (deterministic); the creep/half/minority leak components use the
candidate's own shift formula (`c0 * total * t / (PERIODS * period)`, handoff.rs).
The blip profile (sin² window) was inferred: its per-ship z decimals may differ
from the author's log; verdicts and mechanisms are asserted, not the decimals.
The author's original captured output is preserved as `work/rt-all.author.log`;
regen.sh writes its own output to `work/rt-all.log` as before.
