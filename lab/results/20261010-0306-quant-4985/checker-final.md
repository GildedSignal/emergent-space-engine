Working...
Check complete. `lab/results/20261010-0306-quant-4985/check.md` written; nothing else touched; tree restored (patch reversed, no tracked changes).

**Grade: silver.**

What I did and found:

**Reproduction** — Applied `work/patch.diff` to a clean tree, rebuilt, reran all five commands: four logs byte-identical to the author's, the fifth differs only in wall time (8.2 vs 8.3 s); all digests and `live=` values match. Universe suite green under the patch (54/54). Structural claims verified in code: no removal path in `PlainBodies`, `bytes_of` omits the `Arc<Entry>` trajectory heaps behind each `Segment` (so the ledger/allocator split is real by construction), prune window `2·light_distance + 2²⁶` ticks every 64 frames.

**Adversarial** — (1) 10⁵ game-seconds: +16,153 ship events added 736 B and 2 segments — saturation is durable, the run's strongest result; (2) 4000 members: 4.7 KB/member steady, 729 MB peak, live/ledger 17.3×; (3) seed 9 consistent; (4) `members=0` panics ("a battle needs two fleets"), so the orbiter-only allocator truth is unreachable — a control the author didn't have.

**Predictions** — mtime 03:13 vs logs 03:23: written before the decisive runs; misses honestly scored.

**Why not gold** — A baseline, not a mover: nothing deleted, no premise killed, and the capacity order (~KB/ship → ~10⁶ ships) was already H0158's on the old engine; new here are the saturation mechanism, whale anatomy and the 16.8× split. Gold experiment named: the deduping generator store judged against this baseline and B18.

**Author's misses** — two unreproducible rate figures ("0.2/s/ship" is fleet-wide, 20× off per-ship; "~3.7 events/s/member" and "20×" match no slice), the star "flat at every snapshot, all runs" contradicted by their own 30k log (star_b=1320), and the 16.8× never decomposed — if partly per-body, allocator-inclusive capacity is nearer 2×10⁵ than 10⁶.
