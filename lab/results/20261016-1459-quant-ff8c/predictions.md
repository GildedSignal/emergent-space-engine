# Predictions (written before the decisive runs)

The lever: `apply`'s `root_state_raw` position walk (stage ROOT) is deleted under `ES_POS_CARRY`
by (a) carrying `scalars(exact)` out of `rebind` — the binding holds it bit for bit at its event
tick (bind.rs) — and (b) skipping the walk when nothing rebound, because the cache already holds
the same binding's state at the same event tick (`pos_tick`).

Cases I have NOT tuned on, and what I expect:

1. **Bit identity of the carried own half (ES_POS_VERIFY, belt N=10⁵ through the first wave and
   past it, plus the plane's 28 bodies):** `POS_MISMATCH = 0`. The bind.rs doc promises the readout
   at the binding event is the bound state bit for bit; if the promise is false anywhere the
   counter goes non-zero and the run reports a kill, not a win. Risk accepted: if a mismatch
   appears, it names a law property worth knowing, not a silent drift.
2. **Digest identity:** `ladder_digest` (all cases × 4 schedules) and `frame_digest` (8 flights ×
   4 schedules) print identical lines OFF vs ON. The carry changes no value the core reads (the
   position cache feeds only deadline heuristics, and even those are bit-identical); any digest
   move kills the lever. The `POS_WALK_ERR` counter (walk errors where the carry succeeds) may be
   non-zero without breaking digests — the walk's error path leaves the cache stale, the carry
   refreshes it; deadlines differ then, and if digests still hold that is itself evidence of
   schedule independence at the canonical cut.
3. **Hit structure at N=10⁵ belt (root doll, clock law):** hits ≈ fired kicks (every rebind),
   skips ≈ boundaries + unfired kicks (no rebind, cache exact), walks ≈ first applies only
   (thousands, not hundreds of thousands). If skips are small and walks large, my "no-rebind ⇒
   cache exact" reasoning is wrong somewhere and the run says so.
4. **Wall:** ROOT stage ns falls by the own-half share. On the belt (root doll, no ancestors)
   I expect the walk to be deleted almost whole: ROOT calls → ~walks (near zero), ROOT ns down
   5–15× at the event cycle level; the fired kick item falls by ~1 walk ≈ the readout cost it
   re-paid (~2–5 µs of the ~41–50 µs item, i.e. −5–12%), less than 5ade's −13% cycle figure
   because that priced both the skip and the carry across 2.06 applies/kick. For planet-doll
   ships (locals) the ancestor half remains — I expect ROOT to survive there and name it.
5. **The OFF arm is shipped verbatim:** no env var set ⇒ byte-for-byte the old code path (the
   gate reads env once, the else branch is the old walk). Digests of the OFF arm must equal the
   frozen record's (ladder_digest's own lines on this box).
