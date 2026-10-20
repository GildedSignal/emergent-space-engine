# od 6(a) closed: the two arrays are named — one is not an engine array's twin but the radial id list, and only it has a safe `with_capacity`

## Claim

The player item's two census ladders (5f76) are **`encounter.rs:188`'s `candidates: Vec<(usize, Binding, Scalar)>`** (the capped ladder, terminus exactly 57,344 B = 128 × 448-B tuples, ~1.1 builds/item) and **`radial.rs:257`'s `ids: Vec<u32>` = `unbounded.clone()` + bin `extend_from_slice`s** (the "short ladder", sizes 2,560 → 5,632 → 11,776 B = caps 640 → 1,408 → 2,944 u32s, ~1.1 builds/item, exact-reserve growth, not doubling; `sort_unstable` allocates nothing — micro-test). The one-line fix exists for only one of them: `Vec::with_capacity(hit + idx.unbounded.len())` (the bound is already computed for the early-return check at radial.rs:254) is exact, deletes the whole second ladder, and measures **193.4 → 179.7 KB/item (−7.1%) and −11.5% player-scope reallocs** on the shipped coast arm. For the capped ladder the census's own fix idea is refuted as stated: `with_capacity(near.len())` would allocate ~1.3 MB per player item — 23× the terminus — because **~96% of the radial ids die inside capture's filters** (2,944 ids in, ~128 candidates out), so the fix belongs to the read set (cc9d's row), not the allocator call.

## Bottleneck

budget-1e9's od 6(a)+(b): the census that counts the player term's structure (194 KB/item, law-grade across three seeds and three decades of K) but "cannot name" its two array-builds, and the one-line `with_capacity` whose saving ("halves the player term") was a claim. Gain is not at 10⁹ (the player term is a bounded ~19 KB/game-s there — unchanged); the gain is decision-level: od 6(b) is decided for one array and refuted for the other, with the mechanism (the 96% filter die-off) that redirects the real fix to the read set.

## Evidence

All on this box (8 vCPU, load ~0.5-1.0), shipped `nladder` scene via `plane_extra`, seed 1, rtf 2000, 12 ms, x86 orders only. Commands: `bash lab/results/20261020-2102-fermi-6e76/regen.sh` (~2 min; the four blocks below, in order).

1. **Anchors reproduce** (A1, coast K=10⁴, 30 s): item-scope **11.35 KB/kick**, base **2.06 KB/game-s**, player term **193.4 KB/item** (5,517 items), ladder top **57,344 B exactly** — 8994/5f76's numbers to 0.1%.
2. **Naming instrument** (new `examples/alloc_bt.rs`, this run's patch; sampled size-tagged `std::backtrace` in scope 4, signatures from file:line records; plus an exact per-size counter):
   - Every ≥2-KiB player-scope event is a **realloc** (0 allocs ≥2 KiB in 1,722 items).
   - Exact census (10 s, 1,722 items): **3,584 / 7,168 / 14,336 / 28,672 / 57,344 × ~1.10-1.13/item** (family A) and **2,560 / 5,632 / 11,776 × ~1.10/item** (family B, + stragglers 3,072/6,656/13,312 = the same build at other bin widths).
   - Backtraces: family A → `encounter.rs:188` (`candidates.push` in `PlayerNeighbourhood::capture` via `encounters_for_player`); family B → `radial.rs:260` area (`Radial::candidates` from capture's closure at encounter.rs:172).
   - **Micro-test** (`rustc -O`, counting allocator): a 600-u32 clone + extends of 768 and 1,536 reallocs at exactly **5,472 → 11,616** (reserve-exact: cap+incoming), and `sort_unstable` adds **zero** allocations ≥1 KB. So family B is the ids build itself (clone 2,560 = 640×4; +768 → 5,632 = 1,408×4; +1,536 → 11,776 = 2,944×4), not a sort scratch.
   - Small third site: `body.rs:141` `PlainBodies::retire` (3,328 B) under `pull_ships → resolve_body → apply` — the pulled ships' own items nested in the player scope (the ~225 sub-2-KiB calls/item, ≈1.4 per pulled body, are this path; ≥2-KiB backtraces only).
3. **The die-off that kills `with_capacity` on the capped ladder:** family B's exact census says the radial build reads **~2,944 ids** per player item, while family A tops at **128 tuples** — **~95.7% of the radial candidates fail capture's filters** (`reach.is_zero()` / doll / alive / born). `with_capacity(near.len())` = 2,944 × 448 B ≈ **1.26 MB per item, 23× the terminus** — 8994's "over-allocate 3.67 MB" warning, now with the measured ratio and the mechanism.
4. **The fix, flown** (radial.rs:257 → `Vec::with_capacity(hit + idx.unbounded.len())`, exact bound already computed at :254; A1fix, same flight): player term **179.7 KB/item** (−7.1%), player reallocs **330,780 → 292,878 (−11.5%)**, family B gone from the census (2-4K bucket 11,512 → 5,846; 4-8K 11,461 → 5,794; 8-16K mean 13,055 → 12,059 = the 11,776 realloc replaced by one 11,776 alloc), family A untouched (16-32K/32-64K counts and means unchanged, top still 57,344). Element sequence and sort/dedup inputs identical (capacity is not semantics); kicks/items within the arm's budget-fed cadence spread (107,843 vs 108,027 over 30 s, the rtf-2000 coupling 5f76 documented).

## Predictions (predictions.md, written before the naming and fix arms)

- **P1 (capped ladder = capture's candidates) HELD**, site and line exact.
- **P2 (short ladder = radial ids build) HELD**, letter-for-letter (clone + bin extends; the collect), with one correction to the census's reading: its growth is reserve-exact, not doubling — "rungs" 2-3 at means 6.5 K/13 K are cap+incoming reserves, not powers of two.
- **P3 (sub-2-KiB calls = the pulled ships' items) HALF-HELD**: the only ≥2-KiB non-scan site is `retire` on the `pull_ships` path; the sub-2-KiB population itself was not backtraced (min size 2,048).
- **P4 (burn chains grow the same site as P1) NOT TESTED**: the backtrace instrument crashes/hangs under the burn arm (allocator-internal capture during the 3.7-MB chain reallocs; killed at 60-120 s twice, alloc_scope's burn arm runs clean in 3.4 s, so the failure is the instrument's). The burn half of the naming stays open.
- **P5 (with_capacity halves the player term) REFUTED in both halves**: the census's two arrays carry 145 KB/item together; only family B (20 KB/item of traffic) has a safe bound, and the measured saving is **13.7 KB/item (−7.1%)**, not half. The "halves" claim applied to the pull's bound, which the die-off measurement now forbids.

## What would make it wrong

The site attribution rests on sampled backtraces (3 per exact size) whose line records point at inlined frames near the true call (family B's records say `radial.rs:260`, the sort, while the micro-test's size fingerprint proves the growth is the clone+extends at :257-259 — the sizes 2,560/5,632/11,776 cannot be a sort scratch, which allocates nothing here). If the engine's coast bins changed width (different K or seed), family B's sizes move with them but the site and the fix do not. The −7.1% is one seed, one K, one box, coast only; the fix's virtue is not the size but its exactness (no over-allocation at any bin width). At 10⁹ nothing changes: the player term stays a bounded per-player rate (0.097 items/game-s), so this is a component decision, not a closure lever.

## Cost of adopting, and fit

The radial one-liner (2 lines with comment, radial.rs:257-260) is exact-bound, semantics-preserving, and deletes ~2 reallocs + 8 KB per player item on every coast arm; it does not touch the read set or the law. The capped ladder must NOT get `with_capacity(near.len())` (23× over-allocation, measured); its fix is filtering before the tuple build — the read-set row (cc9d) — e.g. storing (id, reach) in the radial index so zero-radius bodies never enter the tuple pipeline. PRINCIPLES #1 ("the cheapest compute is compute not done") and #17 ("the best part is no part") cut both ways here: the reserve deletes work, but reserving the unfiltered bound would have *added* 23× memory traffic — the measurement is what tells them apart.

## The lens (Fermi)

The estimate came first and was wrong in a useful way: from the census means I predicted a 448-B element and a 512-B element before flying; the backtrace showed the 512-B family was u32 ids at caps 640/1,408/2,944 (reserve-exact, not a doubling ladder — a family 5f76 could not have distinguished from its rung means alone). What the lens missed: the die-off (2,944 in, 128 out) is the actual reason the capped ladder caps — a selectivity fact, not a size fact — and it, not the allocator, decides which fix is legal. The burn arm's crash also cost P4; the instrument's limitation (capture inside the allocator during giant reallocs) is disclosed above.
