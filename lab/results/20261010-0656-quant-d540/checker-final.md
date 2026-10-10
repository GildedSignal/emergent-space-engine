Working...
Check complete — `Grade: gold` written to `lab/results/20261010-0656-quant-d540/check.md`, tree restored to clean, nothing committed.

**What I did:**
- **Reproduced** from `work/patch.diff` in a clean tree (build 10 s): digest control bit-identical (1674 events, EQUAL); main sweep Ω(N) at zero events (199 → 5 264 → 64 453 µs at 10³/10⁴/10⁵, events 0); fresh layout matches the author to 1.03×; far end 194 246 µs at 3×10⁵ (+0.4%), 839 041 µs at 10⁶ (+16% at load 2.7); peak RSS 1 930 140 vs the author's 1 930 272 KB — the 1.9 KB/tube number is exact.
- **Verified the attribution in source**: `advance`→`rekey` unconditional (universe.rs:792), one `Calendar::set` per entity in rekey (499–505), remove-then-requeue of every far entity (805–832), and `Calendar::set_unchecked` (calendar.rs:75–97) has no same-key fast path — three real heap ops per body per frame, always. `find` is the shipped default finder (207), linear per body.
- **Predictions**: all five held; predictions.md written 8 minutes before results.md.
- **Adversarial**: rtf 1000 (wall unchanged); stride-0 co-orbital pile-up (wall unchanged, but it exposed that `law::hit` requires approach — two bodies in exact formation within reach are *never* encounters: 0 hits measured with 512 ships two-per-identical-orbit; recorded as a correctness lead the author missed); no-player scene means the frame numbers are optimistic vs a real plane.
- **Novelty/goal fit**: no prior measurement of the plane's presented-frame cost vs N (the H0157–H0173 scheduler work is the pre-pivot engine); plane.md foundation 7's "bounded work per presented frame" is measured false; both `b-belt-wire` and `b-readout-cost` are queued bets this redirects.

**Dings recorded**: the author's own 10⁶ row violates their "sched-only within ±5%" line (+10.3%); the ≥700× gain is projected, not measured; small-N constants wobble ±2× on the shared box.
