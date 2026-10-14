# Dossier — 20261014-1631-taleb-6138 (Taleb)

**Claim.** The plane's F1 pass at 10⁶ is measured in a window that ends 11,000 game-s before
the shock every belt delivers: the belt's first-kick wave (13,037–14,542 game-s, one smooth
birth-synchronized wave) meets the burning player in the root doll, where the player's item
resolves the whole backlog inside one unbudgeted item — worst frame **315 ms at 10⁵ and
1,213 ms at 2×10⁵ (seed 1) / 1,244 ms (seed 2)** against a 12 ms budget, while the same
wave with the player out of the root doll coasts at **12.0 ms, zero frames over** — a
structural freeze, not schedule luck, and it recovers fully once the wave passes.

**Bottleneck.** Ladder break #3's pull half (the seam a2c1 did not measure; its checker
flagged the "one item 14.6 ms" as inferred). This is the furthest-gap line (bodies: 10⁶
certified, 10⁹ wanted): the wave turns the certification into schedule-domain luck, and the
freeze scales with N (batch ≈ wave density × the player's item horizon). Gain from fixing:
the plane's smooth-flight claim extends from "20 s coasting" to "past the first wave under
burn"; what it deletes: the unbudgeted item itself (the engine's own hold-the-scan path
already exists at `universe.rs:1164`).

**Evidence** (shipped main `db0f3e74`, Linux 8 vCPU shared, load 0.5–2.2, 14 GB free;
`target/release` via `CARGO_TARGET_DIR`; runs in `raw/`, one file an arm; every command
≤ 40 s wall — the probe is unpaced, so "200 s flights" are 20–40 s wall here):

- `belt_first 200000`: the belt's 199,700 first items land in one window, game s:
  **min 13,037, p01 13,377, p50 14,072, p99 14,473, max 14,542** — smooth, mean ≈ 221
  bodies a frame at rtf 100; no intrinsic spike can make a 24,467-event frame (110× the
  mean): the monsters are accumulation.
- Flights (200 s page time, rtf 100, budget 12 ms, L8 burn from 1 s; `ladder:` line in each
  raw file; player's doll: `(0, doll 2) → (948, doll 0 = root)`):

| arm | p50 ms | p99 ms | max ms | >12 ms | ev/frame max | worst lag s | end RSS |
|---|---|---|---|---|---|---|---|
| 10⁵ burn s1 | 0.008 | 11.9 | **315.2** | 23 | 6,443 | 1.45 | 729 MB |
| 2×10⁵ burn s1 | 0.009 | 11.9 | **1,213.1** | 27 | **24,467** | 1.45 | 1,457 MB |
| 2×10⁵ burn s2 | — | 11.9 | **1,244.5** | 26 | 24,997 | 1.18 | 1,456 MB |
| 2×10⁵ coast s1 | — | 11.9 | **12.0** | **0** | 238 | 1.45 | 950 MB |

- The monster frames sit at 8,367–8,678 (the wave) spaced **49–50 frames apart** — exactly
  the player's item cadence under burn — each carrying ~49 µs × events of work inside one
  item: (8516, 1,213.08 ms, 24,467 ev), (8416, 1,197.38, 24,419), (8466, 936.36, 19,081).
  Between them the budgeted drain saturates at 11.92–11.94 ms carrying 232–243 events and
  cannot catch up: it only reaches the frame's 1.67 game-s target tick, while
  `pull_ships(key, !in_root)` (`universe.rs:769`) resolves every ship whose key is below
  the *player's next item* (~83 game-s of horizon at this burn level). **Batch = wave
  density × the player's item horizon → linear in N**: 6,443 → 24,467 → (M1 record) 37,938
  at 3×10⁵, i.e. ~5 s of freeze per player item at 10⁶.
- Coast, same seed, same wave: max 12.0 ms, zero over — but the presented time falls
  **1.45 s behind** (budget-saturated drain, 238 ev at 11.95 ms) and recovers after the
  wave. The overload is real in both flights; the seam decides its *shape* (lag vs freeze).
- Recovery (P6): past the wave, sampled frames ≤ 1.17 ms, zero over; the freeze does not
  ratchet. A second, milder seam exists at frames 11,094+ (13–55 ms, event-thin, every ~50
  frames, burn only) — unnamed here, listed as an open direction.
- Machine guard: all runs stayed ≤ 1.46 GB RSS (the cap that kept the M1's 3×10⁵ run at
  3 GB footprint out of reach here; its 1,280 ms record is quoted, not re-run).

**Predictions** (`predictions.md`, written before any flight): P1 held in direction
(worst(2×10⁵)/worst(10⁵) = 3.85×, kill was ≤ 2.2×; exponent 1.94) but the point estimate
(150–450 ms) was low — the 10⁵ arm's batch was 4.8× the M1's (315 vs 45 ms): the exact
monster size is schedule-conditional (where the item lands in the wave), the phenomenon and
scaling are not. P2 held (24,467 > 5,000). P3 held (12.0 ms, 0 over — with the lag caveat
above, which the prediction's wording missed). P4 held (seed 2 at 1.03× of seed 1).
P5 held at percentile resolution (smooth window; finer-than-percentile spikes unexcluded —
caveat). P6 held.

**What would make it wrong.** The batch-size model (density × horizon) is inferred from
three points and the 50-frame spacing, not instrumented per-item; a direct counter on
`pull_ships` (events per call) would nail it. The 10⁵ arm disagrees with the M1 record's
45 ms by 7× — if the M1 number is the truthful one, the cliff sits between 10⁵ and 2×10⁵
rather than below 10⁵, which changes the "10⁵ already freezes" reading to "10⁵ is
schedule-lucky". Cost of adopting the fix: small (hold the scan when the backlog it would
read is over a threshold; the engine already holds scans off the critical path), but its
certificate is bit-exactness — `frame_digest` unchanged on every flight, including held-scan
answer order — and the pull exists for a bit-exactness reason the scan read must keep.
Fit with PRINCIPLES: #12 ("the algorithm that allocates the work to prevent those heavy
tails, it's the most important one" — this is a heavy tail the allocator cannot see), #5
(priority is slack, not proximity), and the lab rule that a certificate judges what the
player meets: the 20 s rung ends before every belt body's first event.

**The lens (Taleb).** It found the cliff and the saturation; what it may have missed: the
freeze is bounded and self-healing (no ruin of the history — bits held, refusals 0, dead 0),
so against ruin-theory's ranking this is a smoothness bug, not a correctness one; and the
lens under-weighted that the honest gate fix (fly past the wave) costs nothing but run time.

## Commands (each ≤ 40 s here; full regen ≤ 15 min: `regen.sh`)

    belt_first 200000
    NLADDER_MAX_S=260 NLADDER_TRACE=1 nladder 200000 burn 200 100   # and 100000 burn,
    NLADDER_SEED=2 ... 200000 burn ...; 200000 coast ...            # raw/*.txt, table.py
