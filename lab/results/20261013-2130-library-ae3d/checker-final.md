Working...
Check complete. Verdict: **Grade: silver** — written to `lab/results/20261013-2130-library-ae3d/check.md`, with the author's `wiki/nladder.md` corrected in place.

**What I did:**

1. **Reproduced** — clean tree, empty patch, shipped examples. regen exit 0; my independent reruns match every deterministic field (ck checksums, scars, repacks 2,570) and all timings to the same order. Dossier table matches the author's original probe lines exactly. All 10 quotes re-verified verbatim against the cached corpus (4,580 highlights, 762 sources — exactly as claimed; attributions to Isaacson/Musk, Taleb, Waitzkin, Farnam Street all correct).

2. **Found three substantive problems:**
   - The headline "cost follows events, not bodies" is a **control, not a measurement**: `ladder.rs` times updates only on `shelves[0]`/`progs[0]` — identical work at any population (2²⁰-member sharding makes it so by construction). The ×1.17 is inside the author's own 6–9 ns repeat noise; my rerun flipped its sign. Only bits/member (12.347→12.329) is a real population measurement.
   - The pre-registration is **unevidenced**: the surviving probe stdout captures predate `predictions.md` by ~1 minute.
   - Rule 4 conflates layers: the 6–7 ns hot append is the store's kick path, not the plane's compact→live promotion — which the same-day frame-cost record prices at 486–585 µs, sticky, no demotion (uncited by the author).

3. **Attacked beyond the author's range:** rung 1 (64.1 bits/member, still graceful, 0 mismatches); `battle` — a shipped population never probed, where the worst compaction step is **12.1 ms at zero repacks** (the "repack is the enemy" attribution dies; "spikes are compaction, not the append" strengthens); 10× event rate (append max 36 µs, still 33× below compaction).

4. **Novelty:** new topic, but the storm's memory half sits on known gold curves (a91f, b30e) and rules 1/5 restate PRINCIPLES. Genuinely new: the spike anatomy and rules 2/3's named falsifiers. Silver's one experiment to gold: the instrumented per-body surprise-rate distribution on a shipped scene.
