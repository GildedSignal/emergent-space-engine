Working...
Check complete. `check2.md` written to the run folder; tree restored (patch reverted, my adversarial bench removed; only `check2.md` added to the run folder; no commits).

**Grade: gold** — second checker, blind to the first.

**Reproduction** (clean tree, `git apply work/patch.diff`, load 1.8→4):
- Digest control: EQUAL, 1674 events — byte-identical digests to the author's.
- 10⁵: frame 63.6 ms, sched-only 67.3 ms, events 0, hits 90 (author 55–68 ms); 10⁶: frame 908 ms p50, find 3.36 s, peak RSS 1.930 GB vs author's 1.930 GB — exact.
- Break points re-derived from my own numbers: frame crosses 16.67 ms at ≈3×10⁴; one `find` at ≈10⁴. Both as claimed.
- All five frozen predictions held (P3 at the disclosed low edge; P2's "±5%" is load-flattering, −22% at 10⁶ under load 4 — noted, not disqualifying).

**Attack** (4 cases): eccentric ships (e ≤ 0.125) — events still 0, wall unmoved; rtf=1000 — cost is per frame, not per game-second; threads=8 at 10⁵ — no rescue (the wall is the single-threaded rekey + defer sweep, verified in code at universe.rs:792/807/827–832); code audit found `prune` is another O(N) sweep every 64 frames in the shipped `frame()` — the bench *understates* the wall.

**Novelty**: `tail.rs`/`view_cost.rs` and HISTORY's plane entry are all small-N; no prior N-sweep of the frame loop exists. Lands before the `b-belt-wire` bet it flags.

**What the author missed** (recorded in check2.md): per-event cost at N unmeasured; the zero-event premise rests on scene structure, not a real belt birth — b-belt-wire must re-measure the event rate, not just fix the queue.
