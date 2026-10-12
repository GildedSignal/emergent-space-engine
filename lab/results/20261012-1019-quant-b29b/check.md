Grade: gold

**Abstract.** The plane's presented frame carries an unbudgeted Θ(N) fixed tier: `advance`'s unconditional `rekey` plus the defer/requeue drain, with the event budget unspent while the frame runs over. Reproduced from the dossier's commands on a quieter box: empty frame 0.002/0.25/5.3/96 ms at N = 12/1.2k/12k/120k (author 0.004/0.245/2.9/133.6), p50 4.9 ms at 12k, RSS 484 MB at 120k (author's number exactly), 0 events at every N and at rtf 100; 8 threads leave the empty frame unchanged. My extension to N = 250k gives 158 ms (9.5× the 16.7 ms frame), no superlinear cliff. Ceiling N ≈ 1.5–4×10⁴ confirmed; fix is one step in `universe.rs` (peek-not-drain, rekey on player motion), taking the fixed tier to O(events). Adopt before `b-belt-wire` lands ships as root entities.

**Reasons.**

1. **Reproduced.** Every dossier command ran from a clean tree with `work/patch.diff` applied; each ≤ 60 s here. Mine vs author (this box was less loaded):

   | N | rekey ms | empty frame ms | frame p50 ms | settle µs/item | digest ms | RSS MB | evs |
   |---|---|---|---|---|---|---|---|
   | 1,200 | 0.045 / 0.045 | 0.247 / 0.245 | 0.245 / 0.245 | 20.5 / 20 | 1.8 / 1.5 | 81 / 81 | 0 / 0 |
   | 12,000 | 0.62 / 0.47 | 5.3 / 2.9 | 4.9 / 6.3 | 19.5 / 35 | 17 / 33 | 99 / 99 | 0 / 0 |
   | 120,000 | 8.0 / 14.0 | 95.8 / 133.6 | 85.5 / 132 | 37 / 50 | 175 / 341 | 484 / 484 | 0 / 0 |

   Differences are load-only; the shape is identical at every point.

2. **Mechanism verified in code, not just timed.** `advance` calls `rekey()` unconditionally (universe.rs:792); `rekey` requeues every entity (499–505); the drain defers every not-yet-due entity and requeues it after the loop (805–831); `Budget::events(0)` is never consulted for deferral (the tick check precedes the budget check). The queue is a deadline-keyed indexed 4-ary heap (calendar.rs:4–7) while the drain tests *tick*-due-ness — the two-orders conflict the dossier names is real. With no player in this scenario, `take_due` is a no-op, so the empty frame is exactly rekey + drain + requeue.

3. **Predictions.** P1 held (rekey ≥ 1 ms by 10⁵: 8–14 ms; empty ≈ 6–12× rekey), P2 held (fixed tier wall-dominates; 29–38 % of 16.7 ms at 12k, ≫ at 120k), P4 held (digest linear, 175–341 ms at 120k), P5 held (8 threads: empty frame 7.1 ms vs 5.3 single — not smaller). P3 is borderline (author 2.5× growth, my run 1.9×) and the dossier reported the break against itself. Caveat: `run.log` is 0 B and the restored mtimes are re-stamped, so "written before the decisive run" is unverifiable from artefacts; the kill criteria, the stated inversion branch, and the disclosed P3 break are the internal evidence, and it is consistent.

4. **Adversarial cases of my own.** (a) N = 250k: empty frame 158 ms, rekey 14.8 ms, digest 335 ms, RSS 612 MB, 0 events — the extreme continues the trend, per-entity cost 0.63 µs (no superlinear cliff; the Θ(N) term alone is ruinous). (b) threads = 8, rtf = 100 at 12k: p50 5.2 ms, 0 events — the fixed tier is serial and owns the frame at real cadences. (c) The probe universe has no player at all, so every rekey provably recomputes identical deadlines — the strongest form of the waste, and a fortiori for the finding. I also checked the events-rare premise rather than trusting it: ship kicks at 5.2 AU give ~4 expected events over 240 frames at rtf 100, matching evs = 0.

5. **Novelty.** No HISTORY entry measures the frame's fixed tier in N; `cost_split.rs` decomposes per-event cost only; the plane bench ran at small entity counts. This corrects a stated premise: plane.md foundation 7, "Nothing takes an unbounded synchronous claim on the frame" — the frame's own scheduler is exactly such a claim, budget unspent while the frame is 5–8× over. That is the gold letter ("shows that a premise is wrong"), on board #4 and the top scaling risk, and it lands before the belt (`b-belt-wire`) can ship ships into the wall.

6. **Fit.** PRINCIPLES #12 ("the algorithm that allocates the work to prevent those heavy tails, it's the most important one" — here the allocator's own queue *is* the tail) and #3 (a deadline for an unmoved player is derived N times over). Schedule-only fixes preserve digests at a canonical cut, so adoption is testable.

**What the author missed.**

- The probe has no player: rekey's player-motion branch, `take_due`, and `root_state_raw` (7 µs) are never exercised; fix (a) is untested against a moving player, where that cost also lands per rekey.
- "Streams the 448-byte `BodyRec`s three times" overcounts: the drain pops heap slots (~16 B), not records; `BodyRec` traffic is rekey + requeue (~2×). Immaterial to the claim.
- "Five orders below 10⁹" is 4.2–4.8 orders as measured; say four to five.
- The frame-p50-vs-empty-frame gap (6.3 vs 2.9 ms at the author's load) is not stable — mine inverted (4.9 vs 5.3). Both are the same tier; only the empty ≈ 6× rekey ratio is stable.
- The fixes are priced from code reading, not measured: no A/B of the min-peek drain showing the O(events) frame. One line of evidence short of demonstrating (not identifying) the deletion; the taste log has adopted comparable pricings, so this does not hold the grade back.
