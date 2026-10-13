# Dossier — 20261013-2130-inversion-dfd0 (lens: inversion)

**Claim.** The flight recorder merged ahead of the decision-tick fix it was told to wait for, so
the project's new regression gate certifies load noise as player intent: one player session,
flown twice on one machine, records two (six, across arms) different canonical flights — every
one of which `--replay-all` blesses as exact.

**Bottleneck.** Truth, not cost: the recorder + `--replay-all` gate merged 13 October (73c98a46,
"decisions are logged at the tick they take effect") is the integrator's pre-merge check
(HANDOFF: "universe --replay-all before every merge"). AGENTS.md's first Truth line — "Canonical
outcomes are exact and independent of cache, partition, observation, schedule and hardware" — is
violated at the recording step: `session.rs::step` (xtask/src/universe/session.rs:118-122) still
derives the decision tick from `u.now`, the frame's presented tick, i.e. "what the budget left
behind" — the exact hole 20261008-0615-taleb-40c0 (gold) measured and 20261013-1249-taleb-a004
re-measured on the current tree; the a342/a004 port (`sched` timeline + decision quantum) is
absent from the tree (verified by read: no `sched`, no quantum, `input(now, keys)` at the
presented tick). The decision-log page's open direction 1 said: "The flight recorder must not
merge before this does." It did. Gain: not a speedup — it deletes a wrong instrument before it
freezes Julien's flights ("his flights are the regression suite once the recorder lands") as
machine-noise-frozen canon, and before a re-recorded suite starts reporting load coin-flips as
regressions (a004: "a coin flip on machine load").

**Evidence** (all from shipped code + this run's patch, which adds one test to the recorder's own
frozen module `xtask/src/universe/flight_tests.rs`, modeled on its `fly()` helper; same seed 3,
same six-decision script at the same frames, same jittered dt cycle, only the engine's wall
budget differs; command: `cargo test -p xtask one_session_two_loads_two_flights -- --nocapture`,
35 s incl. replays; full log: `probe-output.txt`):

- **The fork, in the files.** 260 frames ≈ 4.61 s wall at rtf 100 (≈ 461 game-s; the keeping-up
  arm's 56,322,175 presented ticks ⇒ ≈ 1.22×10⁵ ticks per game-second, derived). Max tick fork
  over the six decisions: members 400, 8.0 vs 0.05 ms budget: **8,207,771 ticks ≈ 67 game-s**;
  members 150: **19,685,304 ≈ 161 game-s**; members **8** (the frozen test's own configuration,
  its own budget extremes 8.0 vs 0.5): **13,391,227 ≈ 110 game-s**. Digests fork in every arm
  (m8: `fac8be060cb0…` vs `0596f2891d25…`; m400: `4ed7ae25752f…` vs `04bc51e33b34…`). So the
  recorder's own frozen test — which flies this very script at 0.5–8 ms and checks only that
  *each* file replays to *itself* ("every flight, whatever its frames, replays to its own
  digest") — has been generating contradictory flights and certifying each since it was frozen;
  its control is one line short of the Truth criterion (compare across configurations, not just
  replay within one).
- **No starvation knob needed: the same arm re-recorded gives a different flight.** The m400
  rich arm flown twice in this run's two executions (nothing changed but the box's load):
  digest `dd39afb78b9f…` then `4ed7ae25752f…`; m150 rich: `cf87cb973348…` then `a28821f6d2f7…`.
  The recorded "truth" is a function of machine load at record time, on any budget, on any
  scene — including the three committed flights in `artifacts/flights/` (their digests were
  taken under whatever the box was doing; they still replay exactly, which is the point: the
  gate cannot see it).
- **Decision aliasing under load.** In the first execution the starved m150 arm logged two
  presses 40 frames apart (frames 50 and 90, words 241 then 245) at the *same* tick 2,121,741:
  under a biting budget sub-frame player intent is silently merged into one canonical tick
  (schedule accepts equal ticks; `Universe::schedule` refuses only `t < last_decision`).
- **The gate blesses every branch.** All six files: `replay()` → `same=true, notes=[]`
  (0.1–2.9 s each); the m400 file replayed at 4 threads: `same=true` (the instrument is exact —
  the difference lives in the recording, not the replay); and `--replay-all` over the six
  contradictory files: **"6 same, 0 changed, 0 regression(s)", exit code 0** — the pre-merge
  gate passes a corpus that contains six incompatible answers to "what happened".

**Predictions** (`predictions.md`, written before the run). Held: the fork appears in the files
(#1, every arm incl. the frozen test's own), the digests differ (#2), the gate blesses both/alls
(#3, exit 0 over the pair), the thread-count control stays exact (#5). Missed, reported: #4 said
the fork would *shrink* at 150 members; it *grew* (161 vs 67 game-s) — the fork tracks the
*differential* delivered engine time between arms, which is maximal when the machine is fast
enough for one arm to keep up (at 400 members the rich arm also lags on this shared box:
presented 22.0M vs the m8 arm's 56.3M of full pace), so lighter scenes widen the fork under the
same starvation; the lag is also burst-shaped (the burn's waterfall), not monotone in wall time
as #1 implied. No loss flip materialised on this script (all six flights end `loss: None`) — the
digest fork is the demonstrated half; the loss channel stays a004's measured prediction.

**What would make it wrong.** The a342/a004 port landing would close future recordings (verify:
`session.rs::step` no longer passes `u.now`; the page's residues — the 0.26 s straddle, the
rtf-dependent quantum, "a decision snapping past the cut never lands" — then govern). If the
player's Mac were always quiet enough that budgets never bite, the fork would be latent rather
than active — but the m8 arm forks at a 0.5 ms budget on an 8-member scene, HANDOFF records the
M1 "swap near its 10 GB limit in daily use; timing swings about 30% with heat", and the
burst-shaped lag means a single burn waterfall under load is enough. **Cost of adopting:** land
the port (the page: 30 lines in `universe.rs` + 4 in the loop + one test; universe suite green
on the patched tree), then re-record or transform `artifacts/flights/` after it; the already
committed three flights keep replaying exactly either way, so nothing breaks at adoption. Add
one regression criterion to `flight_tests.rs`: the same session at two budgets yields one
flight (this run's probe is that line). **Fit with PRINCIPLES:** "Laws are versioned. Canonical
outcomes are exact and independent of cache, partition, observation, schedule and hardware"
(AGENTS, Truth) — the recorder currently freezes schedule *into* the outcome; and #5 "The player
is the only wildcard" — the machine must not be a second one. Julien (DC, #28): the logs are the
record of what the player did; a log that encodes the machine's afternoon is not that.

**The lens.** Inversion found the seam by asking what the freshest merge silently assumes; what
it may have missed: (i) I did not re-run `--replay-all` against the committed
`artifacts/flights/` (the integrator's "0 regressions" stands unchallenged — my point is about
what the gate *cannot* see, not what it misreports today); (ii) the port's own soundness is
taken from a004's record, not re-measured here; (iii) the loss-flip channel (a recorded loss
that a quiet re-record would not contain — the strongest player-facing form of the hole) was
predicted but not produced on this script; (iv) rtf changes mid-flight (`[` `]` keys) were read
in code (`Recorder::current` stores the *current* rtf; replay uses the file's last value) but
not flown.
