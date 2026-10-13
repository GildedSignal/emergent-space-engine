# Predictions (written before the ladder probe, 2026-10-13)

The probe: `shipmem`'s degradation benchmark (`crates/shipmem/examples/ladder.rs`), the
shipped hot/cold body store. Rung = fraction of members kicked. I predict, on cases I have
not run and numbers I have not seen:

1. **Cost per update is flat in population.** Hot update cost per kicked member
   (`b_update_ns`) and compact cost per update (`b_compact_ns_per_update`) change by less
   than 2x when npop goes 2e4 -> 2e5 at fixed rung 1e-3 and fixed update count. The store's
   cost follows events, not bodies.
2. **Bits per body after compact are flat in population** (within ~20%): memory per live
   body does not grow with the shelf count.
3. **The spike term is compaction, not the hot append.** Hot-update p99 stays within ~3x of
   its median; `compact_max_step_ns` (a repack) exceeds the per-update compact mean by more
   than 10x. If true, the allocator's enemy is the repack step, and it is the term to
   schedule in slack.
4. **Promotion-storm cost is bounded, not quadratic.** At rung 0.3 vs 1e-3 (300x more churn)
   the per-update hot cost rises by less than 2x per update actually applied; i.e. the O(1)
   hot append stays O(1) when it is hammered. (The rung sweep is the promotion storm.)

If (1) or (4) fails, the "hot append is the promotion, buy the option" lesson loses its
measured leg and I report it as failed, not held.
