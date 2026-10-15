Grade: silver

**Abstract.** The retention rule for the lazy-Entry seam is built and priced, and the record's sentence is confirmed half right: with the cache shared across slot clones, promotions = demotions exactly on all eight scenes flown (85–95% of reads hit; compile 12.4 → 1.37 s at 10⁵/48k, 15.5× on burn; digests bit-identical everywhere, including burn, 3×10⁴, 2×10⁵ and a 100k-game-s deep cut the author never flew). Global retention erases the memory win (rss ≥ shipped; retained set ≈ 2×N, plateauing), while the redundancy it deletes is N-independent (hits exactly 763,888 at four rungs). The adoptable bounded hot cache is named, not built (~30 lines, default-off). Gold: build and fly it.

## Reproduction

Re-applied `work/patch.diff` myself (tree had been restored post-regen), rebuilt (no source drift: 11.6 s no-op), and re-flew. Every deterministic number in the dossier matches the runner's regen and my own flights bit for bit: demotions/promotions 41,053/804,941 → 41,053; 131,053/894,941 → 131,053; 273,200/2,709,722 → 273,200; 39,459/754,881 → 39,459; hits 763,888 / 715,422 / 2,436,522; digests `5e8c9e24…`, `bc8b489a…`, `a287f479…`, `2109a2e0…`. The only differing numbers are load-dependent walls/compile-seconds (12.41 → 13.34 s seam compile on the shared box), which the dossier itself scopes as order-of-magnitude. Crate suite on the patched tree: lib+tests 77 passed, 0 failed. (The `nladder` *example* fails to link on Linux — `proc_pid_rusage` is macOS-only in an untouched shipped file; pre-existing, not the patch.)

## Predictions

`predictions.md` predates the flights (file times 13 m vs 6–7 m; log order consistent). P1 (identity) held on every arm including the held-out seed. P2 held (85.4% ≥ 85% at 10⁵/20k — barely; 89.9% at 48k). P3 held exactly (1.0× demotions, inside [0.3, 1.5]). P4 held (+6%/+12.5% ≤ +15%). P6 held (≈15.6 cores). The first build's cold-clone miss (39% deletion) is disclosed, with the sharing fix and the finding (reads cross the store's record clones). One defect: P5 was written as a two-branch either/or where each branch "decides adoption" — it could not fail as written; the author reported the dense branch honestly, but the instrument had no surprise channel there. The frozen kill rule (>50% deletion) did not trigger (85% deleted).

## Attack (five cases, all outside the author's flown domain)

1. **Burn, 10⁴/20k/s1** (author flew coast only): digest identical across ctl/seam/retain (`5caeb1b6…`); demotions 40,187, seam promotions 624,994, retain promotions 40,187 = demotions exactly; hits 584,807 (93.6%); compile 3.73 s → 0.24 s (15.5×).
2. **Mid-N 3×10⁴/20k/s1**: digest identical (`a2fab8c8…`); hits **exactly 763,888**; demotions 61,053.
3. **N = 2×10⁵** (2× the author's top rung): digest identical (`af43df43…`); hits **exactly 763,888** again; promotions = demotions 231,053; rss 1,088 vs 1,069 MB ctl (memory regression persists); wall +9.9%. Demotions = belt_N + 31,053 at every rung (10k/30k/100k/200k → 41,053/61,053/131,053/231,053) and seam promotions = demotions + 763,888: the author's inference "the entire redundant read stream lives in the N-independent locals" is now arithmetic, not inference.
4. **Deep cut 10⁵/100k** (2× the author's deepest): digest identical (`ded7fe63…`); promotions = demotions 535,582; hits 5,710,947 (91.4%); **retained_now plateaus at 200,528 ≈ 2.0×N** (200,500 at 48k → 200,528 at 100k): the retained set is bounded by the history depth, not growing with play — the memory regression is a flat +3%, not an unbounded climb.
5. **`ES_RETAIN=1` without `ES_LAZY_ENTRY`**: inert — digest equals shipped control, all counters 0.

The claim's domain now covers coast and burn, seeds 1 and 7, 10⁴–2×10⁵ bodies, cuts 20k–100k. Contacts stayed 0 on every arm (mine included), so the `same()`-on-demoted path remains unexercised — the author flags it open; still open.

## Novelty

No retention build exists anywhere: `ES_RETAIN`/`RetainCache` appear in no doc, no wiki page, no run (newest history entry H0218 predates the seam). e0f9 named the rule ("promote once per demotion, keep until the next kick" — the integrator's open call #1); this run builds it, prices it, and shows its memory half is wrong: a measured premise correction of the integrator's own call, plus the correction of direction (bounded, not global). Not a repetition.

## Goal fit

Board bottleneck #1 (bodies in the flyable engine). The seam deletes 41% standing memory; its CPU objection (~130 cores of re-mints at 10⁹) is deleted by retention to the kick floor (= the shipped engine's own compile-per-kick, ~15.6 cores). PRINCIPLES: "Store the generator, not the generated" (the cache returns the generated — which is exactly why the run concludes the cache must be bounded to the hot set); "Compute only surprises" (one mint per kick, hits free). The run respects via negativa: it measures its own proposed rule to be unadoptable as named.

## Why silver, not gold

The run's own conclusion is that the configuration it built and flew (global retention) "should NOT be adopted as-is", and the rule it recommends (a bounded hot cache, O(10²–10³) entries) is explicitly "the named next experiment, not flown here". Gold requires adoptable-within-one-step; nothing adoptable is flown. Same shape as 760f→e0f9 on this page: the named variant must be flown.

**The one experiment:** build the bounded cache (~30 lines: cap the retained count, evict oldest) and fly two arms (coast 10⁵/20k, burn 10⁴/20k): assert digest identity, retained_now ≤ cap, rss at the seam's ~390 MB, promotions ≤ demotions + belt reads, hits still ≥ ~80%. If the locals' 2.2k-hit streams survive the eviction policy, the seam + bounded retention is adoptable and this becomes gold.

## What the author missed

- The retained set is **bounded** (plateaus at 2.0×N by 100k): the dossier's "history segments hold their filled caches too" reads as unbounded; it is one retired generation deep. The global-retention memory regression is a flat +3%, which weakens (does not overturn) the case against it.
- The retain arm's wall residue over shipped grows ~linearly with wave count (+0.7 s at 20k, +2.8 s at 48k, +8.8 s at 100k at 10⁵): the per-read machinery (locks, Arc traffic on 6.2 M reads) scales with kicks. The hit stream itself is N-independent so this does not grow with N, but it should be priced at the 10⁹ cadence before adoption.
- The mid-N rung the author skipped (3×10⁴) would have turned the hot-set inference into arithmetic for the cost of one 8-second flight; two rungs left it an inference.
- "e0f9's suite passes" is true of lib+tests only; the `nladder` example does not link on Linux (pre-existing, macOS-only `proc_pid_rusage`).
- The page's "85–90% of reads hit" understates its own 10⁴ numbers (94.9%) — say 85–95%.
