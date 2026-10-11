Working...
Check written to `lab/results/20261011-2028-components-6a0e/check.md`; nothing else in the run folder touched.

**Grade: silver.**

- **Reproduced**: pop counts bit-exact (4M belt 13,946,500 / 13,948,404; 1M uniform 6,000,120 / 6,000,219), timings within load noise and conservative (author ran under load 1.4–3.0). `work/patch.diff` empty — everything regenerates from `calbench.rs`, each command ≤ 60 s. Predictions file predates the decisive JSONs; three of six failed and every failure is disclosed.
- **Faithful**: the bench heap matches `crates/space/src/events/calendar.rs` idiom-for-idiom; drive loops match `pop_through`/`requeue` semantics.
- **My attacks**: churn storm (50%/frame) — scan still 2.9–3.2× faster and exact; sparse (megatick-silent bodies) — scan exact but **50–100× slower** than the heap; burst+churn — 2.2× loss at ~250 keys/event; past-tick writes — **scan silently drops events** (−3,487 pops; wheel stays identical), exposing an unstated `key ≥ base−1` precondition and a hole in the identity control itself; wheel aliases beyond its 4.19M-tick horizon (doesn't taint stored numbers — all author runs advance <60k ticks).
- **Why not gold**: 3× is component-level (~1.2× per frame by the author's own Amdahl), and the flat scan's density regime excludes the dormant-majority shape of the 10⁹ goal — the exact regime where the dossier claims the gap widens. The named gold experiment: the hierarchical/per-doll active-set scan at mixed dense+dormant loads, with the past-write guard, on the same pop-stream identity — that is the 10× and the full container deletion.
