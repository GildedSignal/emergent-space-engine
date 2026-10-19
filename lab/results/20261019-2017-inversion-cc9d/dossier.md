# 20261019-2017-inversion-cc9d (inversion)

## Claim

The ladder's next wall at the memory-fence-unlocked rungs is not memory, per-frame walks, rekey or the queue: it is the player's own item in the root doll, which must resolve **every due ship of its doll before its neighbourhood check can read it** — one top-level item that legally carries the whole wave (32,959 nested kicks, **1.64 s**, at 2×10⁵) past a budget that never sees it; the worst frame is `max_ms ≈ 8.1 µs × K`, so the fence's adoption trades the OOM crash for a repeating multi-second freeze the player feels at every belt wave.

## Bottleneck

Board item 1 ("which term breaks first as the plane grows … per-frame walks, rekey, the queue, memory per live body"): none of those four — the fifth term, the player item's O(doll) read set, breaks first at every rung ≥ 5×10⁴. Also answers, by inversion, what the pending TTL-fence adoption (e181/7b6f) buys: memory yes, smoothness no. Julien: "i care about the p95/99 results i want the game to be smooth" (CL 09-25 14:06) — at 2×10⁵ the wave's gulps take p99 to 82 ms and max to 1.64 s.

## Evidence

Instrument: print-only `ES_WAVE_PROBE` (per-frame deltas of `stats` by class + the 24 prof stages; off = shipped output) + a Linux `/proc` footprint stub + an `ES_RSS_CAP_MB` flight guard (this run's patch, `work/patch.diff`; `--features prof`). Shipped `nladder` scene, L8 burn, seed 1, rtf 1000, 12 ms budget, one box, one build. Commands in `regen.sh` (each flight ≤ 40 s wall); logs in `out/*.log`.

The worst frame of every rung, decomposed (`f`, ms, top-level items, nested kicks, wall by entity class [planet moon ship player fleet], owning prof stages):

| rung | max_ms | top-level items | nested kicks in that item | class wall | stages |
|---|---|---|---|---|---|
| 10⁴ | 47.7 | 905 (items_by_class [0,0,0,**1**,0]) | 904 | 99.7% player | process 42.3; kick(clock) 41.4; fit 17.5 |
| 5×10⁴ | 375.4 | 7,530 ([0,0,0,**1**,0]) | 7,529 | 99.7% player | process 329; kick(clock) 328; fit 139 |
| 10⁵ | 819.3 | 16,074 ([0,0,0,**1**,0]) | 16,073 | 99.7% player | process 717; kick(clock) 717; fit 300 |
| 2×10⁵ | 1,643.5 | 32,959 ([0,0,0,**1**,0]) | 32,958 | 99.7% player | process 1,438; kick(clock) 1,438; fit 604 |

- **P1 mechanism, held at all four rungs:** the worst frame is ONE top-level item — the player's (`items_by_class` = one player entity, zero ship entities) — and ≥ 99.5% of its wall is nested ship kicks (`item: kick (clock)`; the fit is inside them). Around the worst frames, every neighbour frame clamps at exactly 11.9 ms delivering ~150–230 budgeted events: the budget is working; the gulp is invisible to it.
- **The K-law, saturated:** per-kick nested cost flat at every rung (49.8–52.7 µs — the record's usual kick cost; no cache cliff to 2×10⁵), and kicks-per-gulp-per-body saturates at ~0.16, giving **max_ms ≈ 8.1 µs × K** (10⁵: predicted 0.81 s, measured 0.819; 2×10⁵: 1.62 vs 1.643). It reconciles the whole scattered record: 9e75-checker2's 5×10⁴ burn worst 414 ms; 4093-era 3×10⁵ burn "2.5–2.6 s carrying ~50k events" (law: 2.43 s, ~48k); 7b6f-checker's 2×10⁵ 1,286–1,312 ms (same mechanism and magnitude; their arms differed in load/fence).
- **rtf control (P3, held):** 10⁵ at rtf 600 → max 862.7 ms vs 819.3 at rtf 1000 (+5.3%), gulp 16,944 vs 16,074 kicks — the gulp is cadenced in game time (the player's item), so it hits at the player's pace too; the record's own rtf-100 3×10⁵ arm is the same number.
- **Code path:** `resolve_body(player)` ends with `pull_ships(key, !in_root)`; in the root doll `!in_root = false` ⇒ `children_only = false` ⇒ `ship_ticks` = **every due ship of the root doll** — nested `resolve_body` calls with no `Budget` check between them (the check exists only between top-level items), and the player's light distance is zero so its item is first in deadline order where "the first item of a frame always runs" (universe.rs:1008). The 766–770 fix narrowed the old burst from every doll to the player's own doll; in root, the player's doll is everything.
- Memory never bound first in these arms: the RSS cap (1,750 MB) tripped only at 2×10⁵ after 24k game-s, past the whole first wave (gs ~14.7k); the wave gulps arrive before the scan channel's guard would.
- Wall digits are schedule-elastic on this shared box (the regen self-test read 59.6/434 ms at 10⁴/5×10⁴ against 47.7/375 in the recorded flights, and 9e75-c2's 414 sits in the same band): the claim is the mechanism, the class decomposition and the 8.1 µs × K constant, not any single max_ms.

## Predictions

`predictions.md` written after the 10⁴ validation arm, before the decisive arms. **P1 held at every rung. P2's letters failed low** (5×10⁴ measured 0.375 vs [0.19,0.32]; 10⁵ 0.819 vs [0.38,0.65] — growth is super-linear below saturation because the budget's between-gulp delivery becomes negligible; the ratio band [3.3,6.0] held at 4.38). **P3 held** (+5.3%). **P4's extrapolation constant was under** (measured 8.1 µs/body vs the 4.7–6.5 predicted from the sub-saturated 10⁴ anchor): 10⁶ → **~8 s in one frame** (unflown: build 2.34 GB > this box's cap), 10⁹ → ~2 hours — the frame, not the average, at a root-doll player.

## What would make it wrong

A rung where the worst wave frame is instead spread over many top-level items (budget overrun) or owned by rekey/prune/scan stages — none seen 10⁴–2×10⁵, but the arms are one scene (L8 burn, seed 1, plane_extra's phase-locked belt) and this box; the gulp's ~0.16 kicks/body saturation could differ on a stirred or de-phased belt (a de-phased belt should shrink the *wave* into many small gulps — same per-due-ship cost, smaller max; unflown here). The decomposition relies on `stats.cost_ns`/prof being inside the same `Instant` windows as the frame timer (they are: `resolve_entity` wraps `resolve_body`, and `frame_to` wraps `advance`).

## Cost of adopting / fit with PRINCIPLES

Nothing to adopt from this run (a measurement), and it sizes the next step: the fix is **the player item's read set**, not the kick (50 µs is already known-cheap per event) and not the allocator (the budget is healthy around every gulp). Two directions, both already owned elsewhere: wire the encounter tiers (`crates/encounters`, built, unwired) so a root-doll player's neighbourhood check no longer reads every body exactly; or make the pre-scan pull a budgeted stream of items (the 766–770 pattern extended to root — a law change, digest re-freeze owed). PRINCIPLES: "minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly" (OC#36) — this is the spike, measured; "the algorithm that allocates the work to prevent those heavy tails, it's the most important one" (CL 09-25 14:28) — the allocator cannot prevent a tail it is structurally blind to.

## The lens

Inversion asked what the pending fixes make worse, and the answer inverted the board's own list: the TTL fence (a memory fix) extends flights into a compute freeze at every wave, and the four named candidate terms are all innocent. What the lens may have missed: the coast scene (player never in root) does not have this gulp — the coast crest is the budget-delivered comb (4093/9e75's law) — so a reader could mistake this for a burn-only artifact; the burn is merely what puts the player in the root doll, and any far flight does the same (the `range` red's domain). Also unflown here: whether a de-phased/staggered belt (98cb's composed levers) shrinks the gulp max proportionally.
