# Predictions (written before any flight of the new arms)

The checker's named gold experiment: standalone mint+demote on the flown store at ≥2 dwell
classes, coast AND burn, reconciled against the anchors 9.2 / 34–38 / 486 µs, then the
two-part verdict: does the measured cost land ≤ 23.1 µs (the 4-core mint budget at 10⁹
rtf 100, composed ÷8 + 61% delete), and does the burn knee respect the dwell dial.

Instrument: 0619's patch (seam + retention + hot ring, bit-identical behaviour) plus this
run's print-only additions: (a) the demotion block timed at the settle site (assignment +
old-entry Arc drop; the discarded fresh compile's Arc-free stays outside, one allocator op);
(b) `ES_RETAIN_DWELL=<game-s>`: the retain cache gains a last-use tick, every mint registers
in the ring, and a sweep every 6 frames evicts entries idle > dwell (frame granularity at
rtf 100 is 1.67 game-s, so the smallest honest dwell class is 10 game-s; eviction lag ≤ 6
frames). Cache policy only — no law path changes: every arm must print the ctl digest.

Anchors already on the record (not predictions): coast 10⁵ retain promote p50 4.44 µs,
promotions = demotions = 131,053, retained_now 100,788, digest a287f479…; burn 10⁵ ctl
digest d3542eea…; burn 10⁵ sat WS = 130,187 = demotions.

## Held-out predictions

1. **Standalone mint (promote_us p50), coast:** ∈ [4.0, 5.5] µs (the compile at true belt
   keys; 1d52 measured 4.44 once). **Burn:** ∈ [4.0, 6.5] µs (held-out: same key mix,
   unknown allocator pressure under the burn's allocation storm).
2. **Standalone demote p50:** ∈ [0.05, 2] µs at both regimes (an Arc drop + a slot
   write; the catalogue insert it avoids is the shipped cost it deletes).
3. **CPU half of the ledger:** measured mint+demote ≤ 23.1 µs ⇒ at composed+delete
   (λ_del = 1.73×10⁵ promotions/s at 10⁹ rtf 100) the promotion stream lands ≤ 4 cores —
   predicted **0.8–1.2 cores**, and at the shipped rate (3.55×10⁶/s) **15–18 cores**:
   the "23 µs transfers" sentence holds, and the cadence+delete levers remain necessary.
   Falsifier: mint+demote > 23.1 µs measured → the sentence dies at the measured store.
4. **Coast dwell dial works:** at dwell = 10 game-s on 10⁵ coast, retained_now ≤ 3,000
   (vs retain's ~101k) while promotions ≤ 1.5× retain's 131k (the belt mints once per
   kick interval regardless; its re-reads are the kick planning itself).
5. **Burn knee does NOT respect the dwell dial (held-out, the decisive cell):** on 10⁵
   burn, dwell = 10 game-s gives retained_now ≤ ~3,000 but promotions ≥ 3× retain's
   (the resolver's re-read stream, ~15 reads/body per 20k game-s at ~1,300 game-s gaps,
   re-mints at any dwell below the gap scale); dwell = 1,000 game-s still ≥ 2× retain's.
   Extrapolated, no dwell meets both 6 GB and 4 cores at 10⁹ burn — the reads are the bill.
   Falsifier: promotions(dwell10) ≤ 1.5× retain's on burn ⇒ the dial DOES hold the burn
   floor and the ledger's resident = λ×dwell identity is universal, not coast-scoped.
6. **Identity controls:** every arm prints the ctl digest per scene (a287f479… coast 10⁵
   s1, d3542eea… burn 10⁵ s1, and the 10⁴ digests as flown); ES_RETAIN_DWELL without
   ES_LAZY_ENTRY is inert (bit-identical to ctl).
