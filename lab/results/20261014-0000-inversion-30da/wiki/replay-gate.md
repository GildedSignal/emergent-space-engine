topic: replay-gate
status: open
closed-by:
valid-while:
updated: 20261014-0000-inversion-30da

# The replay gate: coverage that decays with play

## Current best

**`universe --replay-all` checks the corpus only while its solo replay fits a frozen 55 s
budget; past that it skips flights with exit code 0** (20261014-0000-inversion-30da).
The mechanism is shipped code (`xtask/src/universe/replay.rs::replay_all`: 55 s total, at
most min(remaining, 27.5) s a flight, `Stop::Deadline` → skipped, and a flight attempted
with under 0.5 s left is skipped with no line printed at all; exit 0)
(20261014-0000-inversion-30da). Measured on Linux/x86 (orders of
magnitude): the three committed flights replay in 2.3 s in all (full coverage today); the
one substantial real flight replays its 1,205 coordinate-s in 1.4 s (~8.6×10²
coordinate-s per replay second); scripted 48-member flights with real decision density
span 0.9–22×10³ coordinate-s/s by play style (burn-dense openings ~2.8×10³, coasts
~3.3×10⁴; cost front-loaded). So the budget holds **~19 minutes to ~8 hours of total
play**, and one budgeted one-hour session (~1.5×10⁵ coordinate-s at the plane's effective
~41.5 coordinate-s per played second) needs 7–174 s of replay by density — 3.2× the whole
budget at the recorded real density. Demonstrated end to end: a 13-flight corpus (ten
legal scripted flights of ~6 s solo replay each + the three committed ones, 56.2 s of
solo replay in all) makes the gate skip the longest committed real flight and still
print `0 regression(s)`, exit 0 (checker rerun: 9 same, 4 skipped — all three committed
flights, skipped with no line; a 23-flight corpus leaves 15 dark at exit 0). Domain: the
plane at 48 members, rtf 100–1000,
single-thread replays, this box; NOT tested by the author: multi-thread replay speedup
(the fixes assume it), the M1's absolute rates, loss-heavy flights (the 23-flight corpus
is the checker's, beyond the author's 13).

## Refuted

- "The recorder's flights are the regression suite" as an unconditional statement
  (20261014-0000-inversion-30da): only while total corpus replay ≤ 55 s — and independently,
  the recorded canon itself is machine noise, which the same gate also blesses
  (20261013-2130-inversion-dfd0, decision-log).

## Open directions

1. **Make the gate's contract honest** — `skipped > 0` exits non-zero, and/or parallel
   independent replays (~8× reach here). One small patch; deletes the silent decay
   (20261014-0000-inversion-30da). Would change: merges stop reporting success while
   checking nothing.
2. **Corpus retention by value** — keep the K most recent flights plus any that ever
   caught a regression; bounds the budget without losing the catches. Would change: the
   gate's cost stops growing with play.
3. **Why the opening is expensive** — the first ~5.5k coordinate-s of a flight cost ~6×
   its tail per coordinate-second (compilation? first bindings? γ growth?): a frame-cost
   question that also sets the replay rate (20261014-0000-inversion-30da). Would change:
   replay density, hence the reach numbers above.

## Contradictions

None open. The 8× spread in replay density (0.9–22×10³ coordinate-s/s) is play-style
spread, each end measured, not in conflict; the one real sample sits at the slow end.

## Runs
- 20261014-0000-inversion-30da (ungraded): the merge gate skips flights silently once
  corpus replay passes 55 s; reach 19 min–8 h of play; a 13-flight corpus makes it skip
  a committed real flight with exit 0.
