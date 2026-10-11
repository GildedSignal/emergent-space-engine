Grade: silver

**Abstract.** Claim: the event calendar needs no container — a per-frame counting scan over per-body next-event keys reproduces the shipped 4-ary heap's pop stream exactly (rolling FNV, all 18 configs) at 2.7–3.1× lower ns/event at 1–4M bodies, zero container memory; the bucket-wheel steal reaches only ~1.9×. Reproduced: pop counts bit-exact (4M belt 13,946,500/13,948,404; 1M uniform 6,000,120/6,000,219), timings within load noise, identity true under my churn-storm, burst and sparse attacks. But the flat scan loses 2.2× at ~250 keys/event and 50–100× when bodies are megatick-silent — the dormant-majority shape of the 10⁹ goal — and silently drops events on any key written below the frame base (past-write attack: −3,487 pops); one guard fixes it. Gold experiment: hierarchical/per-doll scan at mixed dense+dormant loads.

**Reasons.**

1. **Reproduction (clean tree, no patch to apply — `work/patch.diff` is empty; all work lives in `calbench.rs`).** `rustc -O calbench.rs` then `--n 4000000 --load belt` (31 s) and `--n 1000000 --load uniform` (3 s): heap 375–387 ns vs stored 384–415, scan 129–133 vs stored 132–134, wheel 206–212 vs stored 207–211. Pop counts match **bit for bit** (deterministic regeneration; every ≤ 60 s as claimed). The author's box ran under load 1.4–3.0 (state-decisive.txt), mine at 1.0–1.9 — stored numbers are conservative, not inflated.

2. **Predictions.** `predictions.md` (20:49) precedes the decisive JSONs (20:56/20:57); smoke-tuned numbers in it match what a 100k run gives. 3 of 6 predictions held (exactness; heap growth 2.37× ≥ 1.5; wheel ≥ 20× above the FIFO floor); the three failures (≥4×/5× speedup, wheel flatness, uniform-weakest) are reported as failures with diagnoses. Honest reporting discipline.

3. **Faithfulness.** The bench's `Heap` is a faithful port of `crates/space/src/events/calendar.rs` (4-ary, `pos[]` side table, `(time, slot)` tuple ties, `set/clear/peek` idiom), and the drive loops match the engine's real pattern (`EventQueue::pop_through`: peek→pop≤deadline; `Universe::requeue`: `set(e, deadline)`), cadences and 256-tick frames a fair abstraction of a 32-kicks/orbit belt.

4. **My attacks (all with a modified copy in /tmp; the run folder untouched).**
   - *Churn storm* (50%/frame, belt 1M): scan 135–155 vs heap 399–498 ns — still 2.9–3.2×, exact. The win is churn-robust (plain key writes vs unlink+sift).
   - *Sparse* (cadences 10⁶–10⁸ ticks, 1M): scan stays **exact** but 23.5–24.7 µs/event vs heap 404–473 — a 50–100× loss. The disclosed amortization boundary is real, close, and now measured: the scan wins at ≲60–80 keys/event, loses at ≳200.
   - *Burst + 50% churn* (100k, shared cadence): scan loses 2.2× (395 vs 175 ns), exact — same boundary, not a tie-rule failure.
   - *Past-tick writes* (1-in-50 of churn lands at target−300): **the scan silently drops events** (pops 234,197 vs 230,710; hash differs) — a key written below `base−1` is never collected. The wheel stays identical (late path). `universe.rs`'s `requeue` (deadline = event time + light distance ≥ now) satisfies the precondition today, but it is unstated in the dossier and unguarded in `ScanCal`; adoption needs a clamp or a min-written-key guard. Note the bench's identity control *cannot* catch this class: its own op stream never writes the past.
   - *Wheel horizon* (sparse run): beyond ~4.19M ticks (1024 windows × 4096) the wheel's level-1 index aliases and pop counts diverge (300,041 vs 300,007) — the control caught it. The author's stored runs all advance <60k ticks (pops × cadence / n), so no stored number is affected; the aliasing further justifies rejecting the wheel.

5. **Novelty.** No HISTORY entry proposes replacing the calendar; this settles the open prior-art lead (`docs/reference/original-research-report.md:643`, "radix heaps or hierarchical bucket queues deserve benchmarking") with a measurement: the bucket wheel is the wrong half, the radix/counting scan the right one.

6. **Goal fit.** PRINCIPLES #6 ("store the generator, not the generated") — the engine already holds per-body next-event times; the heap is a second ordered copy, and this deletes it (16 B/body container + pos table → 8 B/body riding existing state) with exact semantics at belt density. #16 (cheapest arithmetic: a counting pass, no comparisons). Against the gold bar it is short on magnitude: 3× is component-level; by the author's own Amdahl (queue ≈ ⅓ of an event's cost, 6 Oct gold) that is ~1.2× on a frame today, and the flat scan's regime excludes the dormant-majority case of the 10⁹ goal — exactly where the author claims the gap "widens". The premise "flat in n at fixed density" held (scan 117→133 for 4× n), but density, not n, is the surviving risk, and my measurements bound it.

**The one experiment for gold:** the hierarchical variant (or a per-doll scan over each doll's *active* set) at mixed dense+dormant loads at ≥4M — the 10⁹ preview — with the past-write guard, judged on the same pop-stream identity. If it holds the heap's advantage off there too, that is the 10× (the heap's 24 GB working set at 10⁹ vs a scan over active sets), and it deletes the container everywhere, not just at belt density.

**What the author missed.**
- The `key ≥ base−1` precondition: silent event loss on violation, unstated; and the identity control's op stream cannot test it (control hole — the two bugs it caught were of a class it could see).
- The sparse-loss magnitude (50–100×) and the burst loss (2.2× at 250 keys/event) were unmeasured; "pathological sparsity" undersells how near the boundary sits.
- Empty frames are dropped from per-event stats in all three drivers, so the scan's per-frame key-pass cost is invisible in exactly the regimes where it dominates (my sparse run loses regardless, so the conclusion's direction stands).
- `counts[]` is hardcoded to 260 with frame=256 (span 257): the frame length is not a parameter; a different frame panics.
- The wheel's 4.19M-tick aliasing horizon is unmentioned; "wheel degrades like the heap" conflates DRAM pointer-chasing with the aliasing it would hit on longer horizons.
- The "memory-physical floor ≈ 60–100 ns" is an argument, not a measurement (the FIFO instrument is a control that cannot be reached, as designed); fine as stated with "~".

Machine state during checks: load 1.0–1.9 on 8 vCPU, 11 GB free, no swap pressure, ~21:0x local; all processes ≤ ~1.5 GB.
