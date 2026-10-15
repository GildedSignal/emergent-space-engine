Working...
Check 2 complete. Summary of what I did and found:

**Grade: gold** — written to `lab/results/20261015-1747-second-20261015-1615-spacex-1343-3dc8/check2.md` (first line exact), with a checker note appended to the author's `wiki/nladder.md` (add-only).

**Reproduction**
- Runner's regen: 18/18 flights `ALL IDENTITY`; every dossier number reconstructs (×dem 5.94–5.95, arcs 18,779/25,329 B, rss 445→27 / 542→30 / 979→51 MB, 113-B record, 166–224× record-vs-arc).
- Author's own matrix log (pre-dossier mtime) holds the identical digests — two independent matrix runs.
- P2 anchor verified at e0f9's source branch: digest `5caeb1b6…64c451` and counters 40,187/624,994 exact.
- `patch.diff` applies clean at `base` = HEAD; predictions predate the matrix (tight, ~4 s, but consistent and un-tuned).

**Adversarial, all outside the author's domain, all confirming identity**
1. Seed 3: ctl=seam=variant `c34e03bc…`; retry bit-identical.
2. Cut 4,800 game-s (4× horizon): `e66c350c…`; rss 1,716→32–47 MB — the win **grows** with depth (~54×).
3. N=1,500 (3× stream): `65d6ecd4…`; ×dem 5.94, rss 1,321→69 MB.
4. `ES_LAZY_PASSAGES` alone (no seam): inert, digest = ctl's.

**Findings against the author**: the "46–97×" rss/arcs range doesn't reconstruct (I get 41–46× vs standing arcs, 85–94× vs deleted arcs) — a slip in a secondary sentence; and rtf-paced counters jitter at long cuts while the canonical-cut digest stays bit-stable (worth knowing before freezing a counter as a gate). The crate-suite claim stands on the author's run alone — the release suite outlived my window; the tree was verified restored clean afterward.
