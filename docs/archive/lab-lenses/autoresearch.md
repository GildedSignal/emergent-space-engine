# Lens: autoresearch on something that works

Pick one artifact that works (a probe script, the gravity-gate harness, `crates/lattice`, the oracle) and one scalar metric tied to a bottleneck on the board: events per orbit, ns per event, bytes per body, or the energy growth exponent. Hold its behaviours fixed as constraints.

**Before the loop,** write `predictions.md` with a held-out set of cases you will not tune on.

**The loop:**
1. State a hypothesis.
2. Make one change.
3. Measure it.
4. Keep the change or revert it.
5. Log a line in `log.md`: hypothesis, change, metric, kept or reverted.

Stop when three rounds in a row gain less than 10%.

**At the end,** run the held-out set once.

**Deliver** the best configuration as a patch, the log, the held-out result, and the one idea that carried most of the gain.

**Blind spot:** a local search finds local optima. Say what structural change would beat your best.
