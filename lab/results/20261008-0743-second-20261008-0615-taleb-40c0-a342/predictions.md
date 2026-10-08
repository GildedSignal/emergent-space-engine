# Predictions — 20261008-0743-second (written before the decisive runs)

Question: check2 (20261008-0615-taleb-40c0) graded the run silver and named the one
experiment for gold: apply the fix — the live loop's decision tick derived from the loop's
*scheduled* game time (frames integrated, immune to a budget that bites), quantized up to a
decision quantum — in `session.rs` and `kick_bench.rs`, then show `play60 = play30 = play144
= play60-starve` give one digest per seed at rtf 100 *and* rtf 1, the 54-run matrix
unchanged, and wire the play pair as a regression.

The fix I will ship in the patch (design frozen before the runs):

- `Universe` gains `sched: Tick`: the scheduled game time of the presented frame, advanced
  by the same `want` as `frame_to`'s target, capped at the same limit. `sched >= now`
  always (a budget that bites delays work, never moves it); the digest never reads it.
- `Universe::input_frame(keys, rtf)`: the tick a key change first shown this frame is
  logged at = `ceil(sched / q) · q` with `q = rtf · 0.25 s / TICK_SECONDS` (the decision
  quantum: a quarter second of wall time, below deliberate human timing, above any frame
  cadence's sampling spread). It calls `schedule` (the calendar path, law.md "Ties"),
  never `input(now, …)`.
- `session.rs` and `kick_bench.rs` call `input_frame`; the probe's play cases call it too,
  and a `-raw` suffix keeps the old presented-tick path so the leak stays reproducible
  from this patch alone.

Pre-registered predictions:

- **P1 (the named experiment, rtf 100):** after the fix, `play60 = play30 = play144 =
  play60-starve` — one digest per seed (11, 22, 33) at the 80 M cut, and the logged input
  ticks, encounters and contacts counters all equal too. HOLD expected (0.85). Risk: the
  30 Hz grid (3.33 game-s frames at rtf 100) straddling a quantum boundary — my integer
  arithmetic on the three key moments (0.5 s, 1.7 s, 3.2 s wall) says all fps variants
  land in the same ceil bucket, but a float-vs-integer slip in `want` accumulation would
  split them.
- **P2 (rtf 1):** the same four paths, one digest per seed at rtf 1 (check2's second pace).
  HOLD expected (0.8). Same risk as P1 at a 50 756-tick quantum.
- **P3 (matrix unchanged):** the 54-run matrix regenerates byte-identical to the original
  run's `work/matrix.txt` modulo `wall_ms` — the fix adds a field and never touches the
  resolved path. HOLD expected (0.9).
- **P4 (control unchanged):** `fixed-input` digests still equal `direct` at 80 M for all
  seeds (the eager path is untouched). HOLD expected (0.9).
- **P5 (threads through the seam):** `play60-starve` at 8 threads now equals 1 thread
  (check1's extra axis closes with the seam). HOLD expected (0.75).
- **P6 (the honest boundary, adversarial):** a key change placed to straddle a quantum
  boundary (0.26 s wall at rtf 100: the 30 Hz loop logs it at quantum 1, the 144 Hz loop at
  quantum 2 — corrected from 0.24 s before any run: with the tick taken at the *previous*
  frame's integrated `want`, the fps spread is `[sched_30, sched_144]` and the straddle
  window is w ∈ (0.25, 0.2667] s) still splits digests across frame rates. SPLIT expected
  (0.9). This is not a bug the fix can remove: two frame rates are two different samplings
  of the player's intent and no function of a sample can recover the continuum between
  them; the quantum is the declared price (a ≤ 250 ms timing ambiguity), and same-cadence
  equality (load, budget, threads — the ruin form) is exact.
- **P7 (raw seam persists):** the `-raw` play paths still produce four distinct digests per
  seed at rtf 100 (the original leak, reproduced from this patch). SPLIT expected (0.95).

Kill criterion (frozen): P1 or P2 failing on any seed kills the fix as shipped (the
quantum or the derivation is wrong); P3 failing means the fix touched the canonical path
and everything is VOID until understood. P6 splitting is a *result*, not a kill: it bounds
the fix and must be reported with the probability argument (spread ≈ 13 ms mean / 250 ms
quantum ≈ 5% of key changes ambiguous across frame rates).

Regression to wire: a test asserting the P1 equality (play60 = play30 = play60-starve at
rtf 100, plus the load-only pair at rtf 1) and pinning the digest, ≤ 60 s.
