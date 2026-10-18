# Dossier — 20261018-1617-taleb-2403

## Claim

The held-scan mint rate is not a law constant but the player's pacing: a burning player mints
13.5× (continuous level 8) to ~116× (level-8 burst phase rate) the coast rate every fence
number was sized on, and the burn simultaneously eats the drain's margin — held max 1 → 258
on the same quiet box, scene and K, with the arrivals unchanged when the margin is restored.

## Bottleneck

Memory at 10⁹ / the nladder pin (board #1 and #4 interlocked). acf2 sized the wall with
λ = 0.0526 mints/game-s (K-flat, "one flat law") and set the fix's requirement
(answer-or-expire). That λ is a **coasting** wildcard. Rescaled by the burn's distinct-rate
ratio (13.5×), the 8 GB-at-687-game-s wall at 10⁶ moves to ≈ 51 game-s ≈ 0.5 wall-s at
rtf 100 — not a slow leak the fix can chase, a step the fence must absorb at birth
[INFERENCE: arithmetic on acf2's measured byte law × this run's measured rate ratio; the
10⁶ point itself is unflown]. What it deletes: any fence, cadence or expiry sized from the
coast record.

## Evidence

Instrument: `ES_MINT` print-only probe (counters + per-entry `MINT t= cls= held=` lines),
gated and digest-neutral — the 5 s smoke arm gives digest `20a45aa4…` with the probe off and
on. Trigger census classes each entry: `t` (player event clock moved), `L` (head count
flipped), `0` (identical re-push; the deque's ~2× entries/distinct, acf2's 1.95, reproduced).

Bench (paced 60 Hz, the player's real loop, engine budget 5 ms, 800 game-s, script burns
33 game-s every 400; `out/b-*.json`, `out/mint-b-*.err`):

| arm | entries (distinct) | λ burn-phase | λ coast-phase | held max |
|---|---|---|---|---|
| L0 | 43 (26) | 0.090 | 0.0505 | 1 |
| L8 | 393 (197) | **5.87** | 0.0027 | 114 |
| L12 | 1215 (642) | **13.5** | 0.431 | **640** |
| L8 seed 2 | 393 (197) — identical to the digit | 5.87 | 0.0027 | 115 |
| 400 members L0 | 43 (33), census L=10 | 0.090 | 0.0505 | 14 |
| 400 members L8 | 393 (198) | 5.87 | 0.0027 | 157 |

391 of L8's 393 entries land inside windows covering 8.3% of game time: the mint **is** the
burn. Seed 2 identical (arrivals follow the canonical decision log — stronger than
seed-independence: structural). Members 400 opens the death channel (census L: 10 vs 3) but
the volume is the player's (43/43, 393/393).

Ladder scale (`nladder 10000`, 12 ms budget, ~1,830–1,900 game-s; `out/n10k-*.txt/.err`):

| arm | entries (distinct) | λ entries | held max | footprint |
|---|---|---|---|---|
| coast | 193 (99) | 0.097 (0.054 distinct — acf2's 0.0526) | 1 | 27→34 MB |
| burn L8 | 2136 (1334) | 0.977 (0.728 distinct, **13.5×**) | **249–258** | 27→55 MB |
| burn L8, 24 ms budget | 2136 — identical | 0.977 | **0** (drained every frame) | 27→53 MB |
| coast, 5 ms budget | 187 | 0.097 | 1 | 27→34 MB |

The budget pair isolates the mechanism: same arrival stream (2136 both), pin 258 at 12 ms and
0 at 24 ms; squeezed margin alone (coast at 5 ms) pins nothing when λ is small. The burn also
raises engine p99 5.8 → 10.8 ms — the wildcard both raises arrivals and cuts service.

Commands (each ≤ 60 s; from the repo root, patch applied):
```
ES_MINT=1 cargo run --release -q -p xtask -- universe --bench --seed 1 --rtf 100 --seconds 8 --level L [--members M|--seed 2] --no-record
ES_MINT=1 cargo run --release -q -p emergent-universe --example nladder -- 10000 coast|burn 20 [100 [12|24|5]]
python3 lab/results/20261018-1617-taleb-2403/analyze.py   # writes out/analysis.json
```
Machine: quiet shared runner (load ~0.5–1.5 during the flights, recorded in each bench JSON's
`machine_before/after`); Linux/x86, orders of magnitude only.

## Predictions

All six pre-registered predictions held (`predictions.md`): coast λ 0.05–0.10 ✓; burn ≥ 3× ✓
(116× phase rate, 13.5× continuous); λ rises with level (0.09 → 5.9 → 13.5) ✓; seed 2 within
30% ✓ (identical — the canonical log decides arrivals); members 400 opens the L channel
without moving the count ✓; ladder burn held > 20 (258) and footprint +21 MB over coast ✓.
Nothing was tuned after the fact; the kill criterion (ratio < 2) did not fire.

## What would make it wrong

A 10⁶-scale flight whose burn λ does not scale as measured here (I flew K = 10⁴; acf2's
K-flatness plus the census mechanism — the player's event clock — argue it carries, but the
10⁶ burn point is unflown). A load axis other than the budget: my margin variation is the
engine budget, not machine load; b8e2's load law says they are one utilization knob. If the
answer-or-expire fix lands with a cadence above ~14 answers/game-s at the player's doll, this
exposure closes and the record becomes moot. Adoption cost: none in code — it re-sizes a
constant in a fix not yet written; it adds one requirement line: **the fence is sized for the
burning wildcard, and the expiry cadence must exceed λ_burn, not λ_coast.**

Fit with PRINCIPLES: "The player is the only wildcard" (5) — the mint rate is literally his
throttle hand; "Size the allocator … for the worst cell, not the average one" (Taleb lens) —
0.0526 is the average cell; "no work for no reason" (14) — a scan per re-timed kick during a
burn is work the held-scan design meant to defer, now arriving 14× faster than designed.

## The lens

Taleb: the average lied (coast λ), the tail was the wildcard's own hand (burn), and the harm
is convex (arrivals up AND service down in the same frames). What the lens may have missed:
it prizes the ruin framing and under-weighs that the drain, given margin, is genuinely
competent (0 held at 24 ms) — the fix is a sizing change, not a redesign; and I did not fly
the 10⁶ rung or a loaded box, so the wall's absolute time at 10⁶ under burn is inference, not
measurement.
