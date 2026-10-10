# Dossier — 20261010-1947-spacex-19bc

**Claim.** On the plane's own scene, a live ship creates distinction at 0.0013–0.0015 bits/s at
the 24-bit memo-key level but 0.08–0.14 bits/s at the exact Q48 level, so at 10⁹ ships the exact
stream alone is ~45 GB per game-hour (5.6× the whole 8 GB machine) while the quantized stream is
0.65 GB/h — the 8 GB premise survives **only** on the coarse side of that line, and reabsorption
to hold it costs ~2 % of one core.

**Bottleneck.** HANDOFF's risk "distinctions created per game-second (H_live) … decide whether
10⁹ fit in 8 GB; not measured yet" (board item 5). This run supplies the first measured rates and
splits them by representation level, which is the decision b-h-live and b-belt-wire need: it says
**what the belt's store must keep out of the live set** (per-body exact remainders: 70× the
budget per hour) and what it may keep (memo-key-level scars). Expected gain: it redirects a build,
deleting the option of storing exact per-rebind state at scale — the idiot index here is
~600× (plane store 4.4–4.8 KB/body today vs an 8 B/body budget at 10⁹).

**Evidence** (Linux x86 shared runner, 8 vCPU; orders of magnitude only; machine state recorded
in the JSONs — thermals/batt unavailable on this host).

New mode `xtask universe --hlive` (patch; the resolver is untouched — the mode replays each
distinct pending ship item against deterministic snapshots exactly as `--kick-bench` does, and
the plane applies the real update; replay digest, cut digest and store samples replicate
bit-for-bit, `data/hlive-rtf100-s1-rep.json`).

```
cargo build --release -p xtask                                   # 38 s
xtask universe --hlive --rtf 100 --seconds 30 --seed 1           # 12 s -> data/hlive-rtf100-s1.json
xtask universe --hlive --rtf 100 --seconds 30 --seed 7           # 12 s
xtask universe --hlive --rtf 1000 --seconds 3  --seed 1          # 12 s (same 3000 game-s)
xtask universe --kick-bench --rtf 100 --seconds 30 --seed 1      # 74 s (over the 60 s preference; median pre-print at 55 s guard not hit)
```

| Measured (3000 game-s, ~66–71 ships) | seed 1 | seed 7 | rtf 1000 |
|---|---|---|---|
| rebinds / ship / game-s (all causes) | 0.0058 | 0.0078 | 0.0042 |
| plane-made ships only | 0.00183 | 0.00189 | 0.00183 |
| fire rate (kick ⇒ rebind) | 1.000 | 0.999 | 1.000 |
| conditional entropy, 24-bit memo key, bits/rebind | 0.26 | 0.17 | 0.34 |
| exact-key first difference (Q48), p50 / p99 bits | 15.5 / 25.0 | 17.5 / 25.4 | 18.2 / 25.1 |
| **bits / ship / game-s: coarse / exact bracket** | 0.0015 / 0.090 | 0.0013 / 0.136 | 0.0014 / 0.076 |
| kick resolver µs (median / p99) | 72.3 / 392 | | |
| memo: exact hit / quantized hit | 0 % / 95.5 % (1125 exact shapes → 51 quantized cells) | | |

Store trajectory: bytes/body **settles** at 4.4–4.8 KB (no growth; history is pruned at
2·light-distance), dominated by each body's private compiled cycle (knots), `bytes_of` in
`crates/universe/src/body.rs`.

Scale arithmetic at 10⁹ ships, 3600 game-s, pop = 128 packed blocks, stock 48 bits/body,
recompile = one rebind (72 µs median):

| Level | created | fills 8 GB in | reabsorption duty |
|---|---|---|---|
| 24-bit memo key (coarse) | 0.65 GB/h | 12.3 h | **0.017 cores (1.7 %)** |
| exact Q48 remainder (p50 differencing) | 45 GB/h | 0.2 h | 1.18 cores |

**Predictions** (`predictions.md`, written before these runs): P2 fire rate ≥ 95 % — held (≥ 99.9 %).
P1 rtf invariance within 10 % — held for plane-made ships (0.00183 at rtf 100 and 1000, identical);
**missed for fleet members** (0.0023–0.0059 across rtf and seeds: a small, chaotic-loss population,
and the replay harness takes decisions at `u.now` per frame rather than canonical ticks, so timing
differs across rtf — a harness caveat, not a law claim). P3 brackets — held for the exact side
(15.5–18.2 in 8–20), **missed low** for the coarse side (0.17–0.34 vs predicted 0.3–3). P5 store
growth — **falsified**: the store is bounded; the idiot index is a stock ratio (~600×), not a
growth rate. P4 — held, with the refinement that the verdict splits by representation level.

**What would make it wrong.** The rates are measured on one star system's ~70 ships where kicks
come from the parent's tide and the secondaries' moments; if a denser scene (belt, fleets in
formation) raises per-body kick rates — the field is aggregated, so I expect rate ≈ scale-free
[INFERENCE], but this is unmeasured — both columns scale together and the exact side dies harder.
The exact bracket assumes a per-body first-difference coder; a population program that predicts
the drift drives the exact column toward the coarse one, which is precisely the untested content
of b-belt-wire. The entropy estimators are plug-in on ~10³ samples (biased down for the coarse
conditional entropy; the magnitude histograms cross-check it).

**Cost of adoption.** One xtask mode (~200 lines, `work/` patch; no engine change, no digest
change). The numbers feed b-h-live's definition: report both levels, not one number.

**Fit with PRINCIPLES.** "The memory floor is information-theoretic" (§Standing decisions) and
"why do you need so many bytes per body?" (OC#34): the measured answer is that the bytes are
decided by *which distinctions the store keeps*, and only the quantized ones are cheap enough to
keep. "Compute only surprises" (P3): the 95.5 % quantized memo hit says the surprise at key level
is rare; the 0 % exact hit says exactness is all surprise — 22× more shapes than cells.

**The lens (SpaceX).** The idiot index came out as a stock ratio, not a flow ratio, and I did not
question the 48-bit stock target or the pop = 128 size — both are recommendations, not physics.
A different lens would attack the *information* claim itself: first-difference entropy is a weak
model of what a program can predict; the belt build will measure the real thing.
