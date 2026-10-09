Grade: silver

**Abstract.** The diagnosis reproduces: every frame pays three O(N) schedule passes (calendar drain, deadline rekey, deferred requeue) whether or not anything is due. My clean-tree runs at 10⁵: empty frame 77.9 ms (drain) → 13.5 ms (break), 5.8× (author: 60.6 → 11.2, 5.4×); per-event flat ≈ 21 µs; bytes_per_body 1039; plane tests 6/6 pass under the patch. But the one-line break is not adoptable as shipped: at the same canonical cut, drain and break digests differ (09f67947… vs 79d01861…, restricted, 10⁴ ships), and after settle(limit) the break leaves 14 entities with next tick ≤ limit — settle's contract is broken. The guards compare the break only against itself. Fixed cost gain moves the 60 Hz wall from ≈5×10⁴ to ≈1.5×10⁵ bodies.

**Reasons.**

1. **Reproduced** (patch applied to a clean tree; binaries built with `CARGO_TARGET_DIR=/home/glmlab/lab-target-3`):
   - `$B 100000 16 20000`: empty frames 20×, drain ≈ 77.9 ms, break ≈ 13.5 ms (5.8×; author 5.4×; machine now more loaded than the author's run, hence higher absolutes — shape and ratio hold). ns/event flat 21.4–21.7 µs across 10³–10⁵ in the author's three data files, consistent with my runs.
   - `cargo test --release -p emergent-universe --test plane`: 6/6 pass under the full patch — the author's guard claim is accurate as stated.
   - The 10⁶ point (author data: empty 815–891 ms, HWM 1.96 GB, 34 s wall) is consistent with the per-entity growth 263 → 606 → ~830 ns; I did not rerun it (memory ceiling).

2. **The break changes canonical outcomes — measured, not argued.** The drain does not stop at a too-late head: it sets the head aside and keeps resolving deeper items whose *tick* is within the frame (idle-time work, `universe.rs` module doc). Deadline order ≠ tick order (deadline = t + light distance), so the first too-late head can hide due items. The break skips them; `settle` exits on `a.events == 0` at that head, leaving tick-≤-cut items unresolved. My race (`qc` harness, same scenario/seed/windows as `quant_events`, digest printed after `settle(limit)`):
   - drain, 16 rounds: digest `09f67947110ae5809f3dae2f2aea5cc6`, lag (entities with next tick ≤ limit after settle) **0**;
   - break, 16 rounds: digest `79d01861de1770861407b4f47a9826ed`, lag **14** (earliest 2.6×10⁸ ticks below the cut);
   - both variants are internally deterministic and history-stable at the cut (8-round and 16-round runs converge to their own digest), but they disagree with each other — the digest is documented "independent of schedule, budget, threads and observation", and `universe.rs` line 16 says the queue's order "is only a schedule: nothing it breaks a tie by reaches an outcome". This change reaches an outcome. Adopting it silently shifts every digest relative to mainline — a law change, exactly the shape the taste log rejected on 5 October (the quantized memo cell: "changes orbits, so it is a law change"). The author's own saved data held the signal: runi vs break resolve different event streams every round (round 0: 6881 vs 6862 events; totals 1323331 vs 1323162), unremarked in the dossier.
   - The author's "What would make it wrong" names this exact case but discharges it with an argument ("the horizon rule should then present earlier, not lose work… that is an argument, not a measurement"). I measured it: the work is lost *at the cut*.

3. **Predictions.** Genuine held-out discipline: `predictions.md` (19 m before the data files' 18 m → 1 m) precedes every n ≥ 10⁴ run; P1 honestly killed (events flat), P2 confirmed and stronger (per-entity cost grows 263 → 606 → ~830 ns), P3 confirmed (1039 B/body; HWM 1.9 KB/body at 10⁶), P4 answered by stage buckets after perf was refused (`perf_event_paranoid=4`, disclosed in the CSV). The "honest miss" (first variant failed motion, blamed the break, exonerated by stash-and-rerun) is credible.

4. **Novelty.** No HISTORY entry measures the universe crate's per-frame fixed cost against N; the nearest are engine-crate scale ladders (p99 frames) and allocator work — different crate, different question. Board item 4 (smoothness and the allocator) gets its first plane-side measurement here, and it relocates the wall from the event path (flat, cache-friendly) to the schedule's O(N) passes. New, and it survives.

5. **Fit.** PRINCIPLES #12 ("i care about the p95/99 results i want the game to be smooth") and #1 ("the cheapest compute is compute not done") — the diagnosis is on-goal. The fix as shipped conflicts with the certificate discipline the same file states (schedule must not reach outcomes); that is why silver, not gold. Not lead: the bottleneck measurement is reproduced, new, and prices the next lever (rekey ≈ 112 ns/entity, readback ≈ 2.6 µs/event).

**The one experiment to gold.** Make the break cut-preserving and race it against the drain: a second, tick-ordered index over entities (or a count of due items) so `advance` breaks only when no t ≤ target item remains behind the head — then the horizon, the cut and every digest match mainline by construction. Acceptance gate: my `qc` race (same cut, 8- and 16-round histories, several n) shows identical digests and lag 0, while the empty-frame gain stays ≥ 5×. My harness is 40 lines on top of the author's; commands in the author's dossier reproduce everything else.

**What the author missed.**
- The cross-variant digest race — the one adversarial test that matters for a schedule change; "every behavioural guard green" tests the break against itself, not against mainline (the 5 October lesson: agreement between runs sharing a harness is not independence).
- The signal in their own data (diverging per-round event streams between runi and break).
- Their own lens note ("a representation change would delete it") applied one lever too few: the drain exists because one heap serves two orders — deadline for priority, tick for causality. The fix is a second order, not a faster drain; they saw that shape for the rekey only.
- The digest risk is scenario-dependent (my test has no player; the plane tests' cuts happen to leave an empty band), so passing tests there is luck, not guarantee.
- Bookkeeping slips: the quoted 10⁶ empty range (695–835 ms) does not match the saved artifact (815–891 ms); the readback figure (3.1 µs, 14% of an event) is ≈ 2.6 µs / 12% from their own prof deltas. Minor, disclosed here for the record.

Checker's tree restored to clean (`git checkout` + example files removed); nothing else in this folder touched.
