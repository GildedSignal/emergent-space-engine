# Predictions (written before the decisive A/B, after the baseline only)

Baseline measured on this box (shipped, `--kick-bench --seed 3 --rtf 100 --seconds 8`, m400):
made 36.6 µs median (108), leavers 203.7 µs (425), all p99 382.4, refused 0,
digest `36637e67…`, replay digest `f282c907…`.

The change: the crash/exit searches (plain midpoint bisection on an exact per-probe
readout, ~4.6 µs each) keep their exact integer predicate but choose each probe by
Illinois false position on the radius value the predicate already computes
(`to_f64`, observation only). Env-gated `ES_FP=1`; off is shipped verbatim.

- **P1 (mechanism).** Mean exact probes per `next_impact` search falls from ~23–26
  (shipped midpoint count, to be read off the counter in the OFF arm) to **< 10** at
  every arm; worst per search ≤ 14; the 30-probe bisection fallback never fires.
- **P2 (leaver kick).** Leaver-kick median at the flying arm falls **≥ 25 %**
  (203.7 → ≤ 155 µs); all-kick p99 falls ≥ 15 %.
- **P3 (identity).** `digest` and `replay_digest` bit-identical off/on at every arm
  and seed I run, and the universe suite green with `ES_FP=1` in the environment.
- **P4 (made kicks).** Made-kick median moves < 10 % (most made kicks carry no
  surface search — if it moves more, something else moved).
- **P5 (exit searches).** `next_exit` probes per search fall the same way where
  hand-outs occur (needs m1500/m4000 at rtf 1 with the members clamp lifted); at the
  flying m400 arm I expect ~0 hand-outs (record), so EXIT counters near zero there.

**Kill rule (frozen now):** the lever is dead if any digest or replay digest moves,
if all-kick p99 regresses > 5 % on any arm, if the worst probe count exceeds 30 (the
fallback fired), or if the leaver median fails to fall ≥ 25 % at the flying arm.
