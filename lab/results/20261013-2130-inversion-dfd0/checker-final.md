Working...
Check complete. Verdict written to `lab/results/20261013-2130-inversion-dfd0/check.md`: **Grade: silver**.

**What I verified:**

- **Reproduction** — regen.sh exit 0 on the patched tree; every invariant holds (tick forks in all arms, digests differ, per-file replay exact, `--replay-all` exit 0). The regen's m400-rich digest (81edb949) is a *third* value for the same arm across three executions — independent confirmation that the recorded "truth" tracks box load.
- **Code reads** — `session.rs:118-120` passes `u.now` (presented tick) to `Universe::input`; no `sched`/quantum anywhere (the a342/a004 port is absent); `input`/`schedule` accept equal ticks (aliasing possible, universe.rs:984/1022); the frozen test flies this same script at 0.5–8 ms and checks only per-file replay (flight_tests.rs:69-73); commit 73c98a46 landed today 16:38 +0200, after the page's warning; HANDOFF line 20 does mandate the gate before every merge.
- **Adversarial (3, one outside range)** — seed 11 + 400 frames: fork 21.8M ticks, gate exit 0; **rtf 1** (regime the author never flew): fork 497K ticks, different digests — the claim survives its steepest test; the committed corpus: 3 flights all "changed" (law moved at 31d124b9), exit 0 — nothing misreports today, as claimed.
- **Novelty** — not a repetition: 40c0 and a004 measured the loop pre-merge; this run's delta is the shipped recorder + gate (the frozen test's blind control, equal-tick aliasing — the regen even shows all six decisions at tick 14 — and exit 0 over six incompatible truths).
- **Page** — faithful fold, every new line matches evidence; no overstatement, left uncorrected.

**Why silver:** the pre-registered held-out prediction #4 failed in direction (fork *grew* at 150 members: 19.7M vs 8.2M — honestly reported, diagnosis consistent with all data), and the player-facing loss-flip remains predicted, never produced. The named gold experiment: a crash-script arm pair at two deterministic budgets where one arm records the loss and the gate reads the quiet re-record as a regression.

Tree restored to the clean state the runner left it in; nothing else in the run folder touched.
