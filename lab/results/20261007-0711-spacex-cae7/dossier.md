# H_live measured: the plane's live stock is ~1.3 KB/body; the compiled trajectory is never shared

## Claim

On the shipped plane (main at 70f27a9), H_live reaches a steady state — creation equals
reabsorption; the light-cone prune works — but the live stock is **1,245–1,277 B per belt body**
(4,665 B/body on the flown plane), because **the catalogue never dedups compiled trajectories**
(`bind.rs::Catalogue::insert` allocates a fresh slot per body; 2,000 ships on *one* orbit hold
2,000 entries), the record is 448 B, and one 192 B history segment is mandatory per body.
Extrapolated, 10⁹ bodies cost ≈ 1.3 TB of live state — **160× over the 8 GB budget** — and even
at the law's own floor widths (12–16 B static + scars) a billion *individual records* is 14–18 GB,
so the billion must be population programs; the scar budget that remains fits only if retention
follows observable distinction, not light distance alone.

## Bottleneck

Board risk "H_live: not measured yet; they, not the body count, decide whether 10⁹ fit in 8 GB"
(HANDOFF 6 October; plane.md "Distinctions created per game-second"). Gain sought: the number
that sizes `crates/shipmem` (programs + scars) and the retention rule. This run deletes nothing
by itself; it names the three deletions and their measured sizes.

Verified: two runs of the belt probe give byte-identical JSON once `wall_seconds` is dropped
(md5 `c7cacca5…`); `cargo test -p emergent-universe` shows 7 passed / 3 failed **identically
with and without this patch** (step.rs passage/handoff tests; pre-existing on main at 70f27a9).
The container reports no battery/thermal state (the JSONs' `machine` field): timings here are
orders of magnitude only, and none of the claims rests on wall time.

## Evidence

Probe: `xtask universe --h-live` (patch to `crates/universe` + `xtask`, saved by `run.sh`):
settle (unpaced, unlimited budget — outcomes are schedule-independent by the digest contract),
`prune`, sample. Runs on this container (8 vCPU, shared; probe caps itself at ~60 s wall):

```
cargo run --release -q -p xtask -- universe --h-live --game-seconds 1.6e6 --stages 10
cargo run --release -q -p xtask -- universe --h-live --belt 2000 --belt-mode formation --game-seconds 1.6e6 --stages 6
cargo run --release -q -p xtask -- universe --h-live --belt 2000 --belt-mode belt --game-seconds 1.6e6 --stages 5
```

JSON outputs in this folder (`hlive-plane.json`, `hlive-formation2000.json`, `hlive-belt2000.json`).
Deterministic given the seed; `wall_seconds` is the only wall-derived field.

- **Widths (bytes):** Segment 192, BodyRec 448, Binding 176, Entry 224, Knot 88, Tube 16.
- **Flown plane, 0.05 yr of game time:** steady state from ~2×10⁵ s: **4,665 B/body** (76 bodies,
  355 KB), 2.45 history segments/body, `catalogue_live == n_bodies` at every sample. The battle
  freezes (3,027 slices, then flat); its 48 members become tubes (28 → 76 bodies) — a battle's
  news is bounded.
- **+2,000 ships at 2 AU, one orbit (formation):** **1,245 B/body**, exactly 1.0 history segment,
  `catalogue_live = 2076`. **+2,000 distinct orbits (belt 1.5–2.5 AU, e ≤ 0.08):** 1,277 B/body —
  identical. Identical shapes sharing nothing is the finding: the Hashlife memo
  (representation.md §3, "identical invariants share one memoized cycle") is designed, not built.
  Sharing would cut a formation body to ~680 B (−47%).
- **Per-body live split (belt ship):** compiled trajectory ~600 B (47%), record 448 B (35%),
  mandatory history segment 192 B (15%), plan ~40 B. The rate-driven part is tiny: kicks arrive
  every 2.8×10⁴ s at 2 AU (3.6×10⁻⁵ /s/body; ≈3,180 per orbit — not the design's 32), retention
  ≈ 2·d/c + 331 s, so rate × retention ≈ 0.05 segments; the measured 1.0 is the `prune` rule's
  "keep at least the last segment". The player (low orbit, 0.097 events/s) holds 16 segments —
  the near-field worst case, at law width 0.8–1.3 KB/body.
- **Extrapolation to 10⁹, one hour in:** as shipped 1.28 TB (160× over). With catalogue sharing
  685 GB. At law-native widths: static 12–16 B + 0.05–0.4 scars/body (2–10 AU) × 24–40 B =
  **14–18 GB — still over 8 GB**. With population programs (components-98bc: 0.126 bits/body =
  16 MB static) the scar stock is 1.2–1.9 GB at 2 AU (fits, ~4× margin) but 9–15 GB at 10 AU,
  where light distance inflates retention: **retention must follow what the player's view can
  distinguish** (one sample per pixel; aggregates for the rest), not light distance alone.

## Predictions (`predictions.md`)

Held: creation rate is not the binding term at belt scale (3 ✓, 5's direction ✓); catalogue grows
linearly with distinct radii (4 ✓). Failed, all in one direction — I guessed the engine leaner
than it is: Segment 192 vs predicted ≤144, BodyRec 448 vs ≤330, flown plane 4,665 vs ≤450 B/body,
per-body total 1.28 TB vs 280 GB; and I predicted identical shapes share an entry — they share
nothing (the formation's 2,076 entries). The failures strengthen the claim.

## What would make it wrong

`bytes_of` is the engine's own accounting (records, plans, trajectory shape, history), not RSS;
it excludes the fleet's lattice store, the queue and the view cache — all small next to 10⁹
tubes, but a checker should confirm the split with an allocator trace at one belt size. The
scar-width floor (24–40 B) is the law doc's, not measured. If `prune`'s "keep ≥ 1 segment" is
dropped and derivation replaces it, the 192 B/body term vanishes and the law-native margin
widens ~10×; that is a design change to cost, not a measurement error. The 10⁹ extrapolation
assumes belt-like populations; tight-orbit billions (Home-doll rates) are 0.8–1.3 KB/body in
scars alone and do not fit at any width — the game must not put a billion bodies there.

## Cost of adoption

The probe (`--h-live`) is one xtask mode + two accessor methods; it stays useful as the H_live
gate's instrument (b-h-live in the queue). Acting on the findings is the queue's own work:
catalogue dedup by shape (one function, `Catalogue::insert`), the mandatory segment's width, and
observability-based retention — each belongs to b-belt-wire / b-readout-cost / news gravity, not
to this run.

## PRINCIPLES

"Compute only surprises" (3): the light-cone prune already reabsorbs; the waste is width, not
rate. "The memory floor is information" (24): 1,277 B/body against a ~2 B/body information
content — the idiot index is ~600×, worst on the unshared trajectory. "Store the generator, not
the generated" (6): the compiled cycle is the generator, and it is stored once per body instead
of once per shape.

## The lens

SpaceX's delete-first fixed the frame (idiot index, one worst part named). It may undervalue
that `prune` is a one-way door: history dropped is unrecoverable, and the observability-based
retention I propose must be justified by what the gather *actually reads* (b-readout-cost),
which this run did not measure. The kick cadence datapoint (3,180/orbit at 2 AU vs the design's
32) arrived as a by-product and belongs to the cadence question, not this claim.
