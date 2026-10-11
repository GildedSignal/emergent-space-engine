# Predictions (written before the decisive sweep, 2026-10-11)

The decisive experiment: `xtask universe --kick-bench --members {48, 480, 4800, 48000, 240000} --seconds 3`
(cloned kick bench: resolver time and record-clone time separated per kick), plus
`xtask universe --bench --members {48, 48000} --seconds 6 --unpaced --threads 1` for the real frame path.
Machine: i7-4790 (Haswell), L1d 32 KiB/core, L2 256 KiB/core, L3 8 MiB shared, perf blocked (paranoid=4),
so cache attribution is by working-set crossing, not counters.

Cases not tuned on (the sweep sizes and the real-path run), and what I expect there:

- **P1 (resolver is compute-bound, not memory-bound, at warm scale).** The resolver's
  median kick_us stays within 2x from members=48 up to members=240000, because one kick touches
  O(1) state (own record, few parents), all warm from the bench's own index-ordered scan.
- **P2 (clone round-trip share).** clone_us median stays below 0.3 x kick_us median at every N
  (a ~200 B warm memcpy plus one malloc/free of the plan Vec). If it instead crosses 1x at
  members >= 48000 (footprint past L3), the record round-trip, not the resolver, is the
  per-event floor at scale.
- **P3 (real path vs pure resolver).** On the real frame path (`--bench --threads 1`), the
  engine's us-per-ship-item is 3-10x the kick bench's resolver median: the real path adds
  rekey, queue ops, the same clone round-trip, apply/put and the wave's thread coordination
  per event.
- **P4 (the tail is the recompile).** p99/median of kick_us >= 5 at every N (about 99% of
  kicks ask for a shape the exact memo has not seen; the taste log's finding re-measured here
  on a different machine and lens).
- **P5 (footprint).** bytes_per_body reported by the plane is >= 300 B at rest (against the
  16-byte tube the law targets): the plain store's BodyRec + plan Vec + history + compiled
  trajectory share.
- **P6 (leavers vs made).** Leaver kicks (fleet members handed out into the root doll) are
  more expensive than made-ship kicks at the same N by >= 2x median (they rebind across dolls
  and their records are colder), and their share of samples grows with members.

Kill criterion for my own claim: if the resolver median moves by more than 2x across the
sweep, or the real-path per-item cost is within 1.5x of the resolver median, my "compute-bound
resolver, cheap clone" story is wrong and the dossier says so.
