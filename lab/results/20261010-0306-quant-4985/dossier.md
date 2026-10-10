# Dossier — H_live measured on the shipped plane: the generator store is the whale

## Claim

On the shipped plane, the live ledger per body saturates (light-cone prune balances creation) at ~2.3 KB per orbiter ship and ~5.0 KB per battle member — not the 16-byte tube — so 8 GB holds ~10⁶ bodies, about 2.5–3 orders below 10⁹; the whales are the per-body compiled generator (~1.2 KB of knots at birth, re-minted by every kick because exact keys never recur), retained history segments, and battle corpses that are never freed.

## Bottleneck

Board risk "distinctions created per game-second (H_live) … not measured yet" (HANDOFF, risks #2; plane.md "Measured on the whole"). This is the first measured baseline on the shipped engine, and it couples the memory question to bottleneck 1 (fewer kicks per orbit): the same lever buys compute and memory. Expected gain from acting on it: the ~10⁵× gap between the shipped per-body cost (2.3 KB) and the population floor (~0.1 bit, shipmem ladder) is the headroom a deduping generator store can spend.

## Evidence

Instrument: `crates/universe/examples/hlive.rs` (counting global allocator + the store's own `bytes_of` ledger, per class: star/planets/ships/player/fleet-members), driven through `Universe::frame_to` at 60 Hz — the player's path, which prunes every 64 frames. One additive engine hook: `BodyStore::history_len` (default 0; real in `PlainBodies`). No gate, no digest-affecting path touched; universe test suite re-run green after the patch.

Commands (each run ≤ 9 s wall, single thread, Linux x86 — orders of magnitude only):

```
cargo build --release -p emergent-universe --example hlive
$CARGO_TARGET_DIR/release/examples/hlive 10000 100 1 48    # seed1-m48.log
$CARGO_TARGET_DIR/release/examples/hlive 10000 100 1 200   # seed1-m200.log
$CARGO_TARGET_DIR/release/examples/hlive 10000 100 1 1000  # seed1-m1000.log
$CARGO_TARGET_DIR/release/examples/hlive 10000 100 5 48    # seed5-m48.log
$CARGO_TARGET_DIR/release/examples/hlive 30000 200 1 48    # long-30000.log (saturation)
```

Raw rows in the logs in this folder. The numbers:

- **Saturation, not growth.** Ships (23 orbiters, seed 1): between t = 10⁴ and 3×10⁴ game-seconds, 4,620 more ship events add 8 retained segments and 1,152 ledger bytes — flat at **2,322 B/ship, 5.9 segments/ship** while events keep flowing at 0.2/s/ship. Creation phase (t < 300 s) mints ~105 B/event of retained segments; the prune window (2·light_distance + 2²⁶ ticks ≈ 400–900 game-s here) reabsorbs them.
- **Battle members: ~5.0 KB/member steady**, constant across fleet size and seed (5,134 / 4,730 / 5,050 B at 48/200/1000 members; 5,265 at seed 5). Member event rate ~3.7 events/s/member during the fight — 20× the orbiters' — and their creation rate ~49 B/s/member (t 31.7→101.7, 1000-fleet).
- **Corpses never freed.** Alive members fall 1000→393 by t = 10⁴ while the store has no removal path (`PlainBodies`: push/put/retire/prune only); allocator-live at the end is 34.2 MB against a 2.04 MB alive-ledger — **16.8×** (retired-segment heap shapes, the fleet's lattice world, dead records, Vec capacity all sit outside `bytes_of`).
- **The tail.** 1000-member fleet: peak live 97.3 MB vs 34.2 MB steady (2.8×); the fleet handout (480 members in ~30 s) spikes live 0.6→11.7 MB; worst body 40.5 KB vs 6.2 KB mean (6.5×).
- **Controls.** Negative: the star — 1,160 B flat, zero events, at every snapshot, all runs. Positive: member bytes scale linearly with members (48/200/1000); ship bytes identical across fleet sizes.
- **Capacity verdict.** 8 GB ÷ 2.3 KB ≈ 3.4×10⁶ orbiters (ledger only, before the 16× allocator structure and the corpse leak). **N_max ≈ 10⁶, about 2.5–3 orders below 10⁹.**

## Predictions

`predictions.md` was written before the decisive run. Scored honestly:

1. Growth linear and kick-minted until prune — **held in kind, wrong in size**: the mint is ~0.1 KB of ledger per event (segment structs); the ~1 KB/kick heap shape is real but reabsorbed, and ships' kick cadence is low (0.2 events/s/ship), so growth is slow, not the leak I expected.
2. Saturation between 500 and 2,000 s — **held** (segments plateau ~5–6/ship by t ≈ 3×10³ s; fully flat by 10⁴).
3. "Tens of KB/ship, N_max 10⁵–10⁶" — **half-held**: 2.3 KB/ship (10× below my guess), N_max ≈ 3×10⁶ sits at the top of my range; "three to four orders below 10⁹" was an overclaim — it is ~2.5 orders by ledger, ~3 with allocator structure.
4. Ledger undercounts allocator truth ≥ 2× — **held**: 16.5–16.8× at saturation.
5. Star flat, tail reported — **held**.

## What would make it wrong, cost of adopting, fit

- `PlainBodies` is explicitly the seam, not the 10⁹ representation (plane.md foundation 6): if shipmem population programs hold bodies at the ladder's ~0.1 bit, the verdict applies to the shipped baseline, not the end state. But the whale it names — a compiled generator per body, re-minted per kick — is a property of the exact-rebind law, not of `PlainBodies`, and survives any store that keeps one exact trajectory per live binding.
- The 16.8× allocator/ledger split is glibc-on-Linux; the M1 may differ (orders of magnitude only, per the lab rules). The steady ledger bytes (2.3 KB / 5.0 KB) are allocator-independent.
- Scene limits: one star system, one fleet battle. A galaxy doll with unvisited regions lowers event rates, but the birth cost (~1.2 KB/body) is distance-independent.
- Cost of adopting: none for the measurement (additive instrumentation, patch in `work/patch.diff`). Acting on it — a deduping generator store (quantized class + lazy exact residual; the quantized memo's measured 94.5% hit rate is the clustering evidence, used as a store rather than a law change) — is one named experiment, judged against this baseline and B18.
- Fit, PRINCIPLES #6 "Store the generator, not the generated": measured, the generator store *is* the whale — every kick mints a generator that never recurs, so the cheapest generator is the one never compiled. #24 "the memory floor is information-theoretic": 2.3 KB measured against ~0.1 bit of ladder floor is the 10⁵× headroom. #14/#1: fewer kicks per orbit deletes compute and memory together.

## The lens

The quant lens counts bytes and tails, not information: the information floor here is quoted from the shipmem ladder, not measured on this scene, and the "one named experiment" (deduping store) is priced by a memo hit rate measured for compute, not for storage. It also trusts `bytes_of` as "the ledger" — I bound its blind side with the allocator, but a third count (heap shapes of retired segments alone) would have separated corpse cost from fleet-world cost, which I left merged in the 16.8×.
