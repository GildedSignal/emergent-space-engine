Working...
Check complete. `check.md` written; tree restored (only `lab/results/` untracked, as found); nothing else in the run folder touched.

**Grade: silver.**

What I verified, clean tree at `a838a28`, patch applied via `git apply`:

- **Digests bit-identical** across the patch, all four cuts (A `7e4c4380…`, B `2138e8c5…`, C `169e1aa3…`, tail/budget-of-one `e8d0d065…`) — reproduced both sides myself.
- **Costs reproduce**: ships 32.0 → 20.4 µs/item (−36%), whole-universe 49.8 → 43.3; kick decomposition (root_state 7.0 µs, rebind 11.3 µs) matches.
- **Tests**: 54 passed, 0 failed, 1 ignored on the patched tree.
- **Predictions**: written 31 m before the first run artifact (22 m); all four held, the overshoot (36% vs 10–15%) reported honestly.
- **My adversarial cases held**: rtf 1000 with the player (digest + horizon identical), threads=4 through `resolve_wave` — the stale-`requeue` site none of the author's threads=1 scenarios touched — identical digest and `now` on both trees.
- **Novelty**: kick cost is a named lever since H0210, but this delete and decomposition are new.

Why not gold: ~1.4× gain, no component deleted, no premise falsified (schedule-independence is *confirmed*). Gold path is the run's own named lever: the `from_state` rebind (≥100× idiot index), which is higher-tier motion-law work.

What the author missed, on the record:

1. `baseline.txt`'s B line ("Dense … 4.25 s") is **unregenerable** — Dense-200@3G takes >90 s on both trees, and the shipped bench says Sparse; the Dense→Sparse switch is undisclosed. The digest claim survives (Sparse regenerates on both trees; Dense==Sparse by contract), but the B wall-time row mixes configurations.
2. All digest scenarios ran threads=1, so `resolve_wave`'s staleness went untested by the author.
3. New lead found while attacking: **threads=4 stalls (>100 s) on a deep 30 G settle on both trees** where threads=1 finishes in ~4 s — off this run's claim, but it bounds H0210's "one digest across budgets and threads" and deserves its own run.
