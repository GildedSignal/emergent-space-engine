# Dossier — 20261011-0517-quant-d7bd (Quant lens)

## Claim

In the flying plane, every resolved player item pays `PlayerNeighbourhood::find`, an exact
neighbourhood scan that clones and evaluates every body in the universe: measured 1.5–1.7 µs
per body (linear), so one player event alone crosses a whole 16.67 ms frame at ≈10⁴ bodies in
the store and costs ~1.6 s at belt scale (10⁶) — the exact-encounters seam behind
`Encounters` breaks by four orders of magnitude before the belt, and the Binet cone (or a
skin) is the only asymptotic fix; work must track encounters, not bodies.

## Bottleneck

Board's top scaling risk ("candidate pairs per body grow with N; candidate work must track
real encounters") and the encounters seam (plane.md foundation 6: "an exact per-doll check
now, the Binet cone later"). This run puts a number on *when* "later" must arrive: the
player — the one body the game cannot schedule around — already pays the whole store per
event. Gain of the cone over the scan at N bodies ≈ N/encounters-found ≈ 520× at N = 3×10⁴.

## Evidence

Machine: GitHub Actions Linux x86, i7-4790, 8 vCPU, load 0.5–0.7, 16 GB, no swap in use
(state recorded in `sweep.txt` header run log). Orders of magnitude only; the M1 re-measures.

All commands ≤ 60 s, from the repo root (the driver is `crates/universe/examples/wake.rs`,
saved in this run's patch):

    cargo build --release -p emergent-universe --example wake --offline
    cargo run --release -p emergent-universe --example wake -- sweep        # ~11 s
    cargo run --release -p emergent-universe --example wake -- live 0 10 100  # ~10 s

**Sweep** (`sweep.txt`; the plane plus K orbiters added to the player's doll, scan timed 20×
at the player's committed tick t = 18,874,368, interval 2^22 ticks — the engine's own args
in `encounters_for_player`):

| bodies | find mean µs | µs/body | found/20 calls |
|---|---|---|---|
| 36 | 37.0 | — | 40 |
| 1,028 | 1,541.8 | 1.505 | 100 |
| 10,028 | 16,704.4 | 1.667 | 480 |
| 30,028 | 51,019.0 | 1.699 | 1,160 |

Linear in total body count (it `binding_at`s every body in the universe, `cartesian`s every
same-doll one; the clone is 0.02–0.07 µs, `cartesian` 1.4–1.5 µs of the ~1.6). **16.67 ms is
crossed at N ≈ 10⁴** (10,028 → 16.7 ms mean). Candidate ratio: at 30,028 the scan examines
~30,028 bodies per call to find ~58 encounters (1,160 over 20 calls) — ~520 bodies examined
per encounter found, against ~18 at the plane's own 36 (36 examined, ~2 found per call): the
scan's marginal value per body collapses as the store grows.

**Live, the real plane at K = 0** (`live-k0.txt`; 600 frames at RTF 100, held prograde burn,
one item per `advance`, every item timed and attributed by kind):

- player item: mean 207.8 µs, p99 446.5 µs — of which the scan at N=36 is ~37 µs (18%);
  the kick itself (recompile, readouts, rebinding) is ~170 µs, matching `cost_split`.
- ship item: mean 95.6 µs; fleet item: 32.5 µs. No frame over 16.7 ms (max 4.8 ms).
- Cadence: 68 player items over 1,000 game-seconds ≈ 0.07/game-s (one per ~14 s); the scan
  interval is 2^22 ticks ≈ 21 game-s.
- The scan does real work at this scale: 74 encounters, 6 contacts per 1,000 game-s
  (the handed-out fleet lies on the player's own orbit).

**Controls.** Budget contract: resolving one item per `advance` gives the same digest as
unlimited budget at the same cut — MATCH, twice (K=0). Both failures below are disclosed in
`live-k2000.txt` and were pre-registered as voiding conditions: a second `Universe::start()`
is not digest-neutral (MISMATCH), and `add_body` after `start()` panics at
`universe.rs:532` (`pos` is sized at start; the first fleet hand-out indexes past it) — so
in-situ flight at K>0 is not reachable through the public API, and the N-dependence rests on
the sweep. Its K>0 scene is static tubes — observably, zero fleet leavers appear at K>0
(n stays 28+K) where K=0 hands out all 8, and the live K>0 run panics at the first hand-out;
the added bodies' ids sit in the fleet/hand-out entity range, and [INFERENCE] that
displacement starves the hand-out path. The scan never reads the battle.

## Predictions (predictions.md, written before the run)

- P1 ✓ linear, slope 1.48–1.70 µs/body, inside [0.5, 8].
- P3 ✓ 16.7 ms crossed at N ≈ 10⁴, inside [5×10³, 5×10⁴].
- P4 ✗ **wrong, and the miss is informative**: the scan is not ~100% waste — it finds ~2
  encounters per call at the plane's N (real: the fleet leavers share the player's orbit)
  and ~58 per call at 3×10⁴. The honest metric is the candidate ratio (~520 bodies examined
  per encounter found at 3×10⁴), not emptiness.
- P6 ✗ cadence is 0.07 items/game-s, not 10²–10⁴: the player kicks ~128×/orbit.
- P2 unmeasurable in situ (API hazard above); scan share at K=2,000 extrapolates to ~95%
  (3.1 ms scan vs 0.17 ms kick) — inference, not a measurement.
- P5 ✓ exactly as pre-registered: both controls failed → live claim shrinks to K=0 and the
  sweep stands.

## What would make it wrong

The sweep times the scan on static tubes at one committed tick; if `find`'s per-body cost
depends on bodies being mid-flight (retired bindings, cache state under load), the slope
could shift — but the live K=0 point brackets it (engine-in-situ encounters and scan cost
agree at N=36), and the slope is dominated by `cartesian`, which mid-flight bodies also pay.
x86 vs M1 moves the slope, not the linearity: the M1 could be ~2× faster per body, moving
N* to ~2×10⁴, not past the belt. If the Binet cone lands with work ∝ encounters, this
bottleneck is deleted rather than tuned; a constant-factor fix (no `Binding` clone, cached
positions) buys only ~5–10× (N* ~10⁵) and leaves the asymptote.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt in main: the seam (`set_encounters`) already exists and the Binet cone is
the planned part; this run sets its deadline (before any doll reaches ~10⁴ bodies — belts,
handed-out fleets) and kills any plan to ship the exact scan at scale. Two integration
notes for the plane's owner: `start()` is not re-callable (digest changes), and
`add_body` after `start()` breaks `pos` (panic at universe.rs:532) — growth after start
must go through fleet hand-outs only; worth a doc line on `add_body`. Fits PRINCIPLES 3
("Compute only surprises… Nothing is evolved that can be derived when looked at" — the scan
re-derives every body's state per player event), 5 ("The player is the only wildcard, and
their influence travels at c… his direct influence is bounded" — the *influence* is bounded,
O(1) at ~170 µs/kick; the *surveillance* is not, O(N)), and 12 (smoothness: the scan is a
lump, not a flow — one player kick at 10⁴ bodies is a full frame, invisible to the mean,
fatal to p99).

## The lens

The Quant lens priced the tail and missed, until the run forced it, that the scan's product
is not empty (P4): a market microstructure habit — assume the sweep finds nothing — would
have mis-filed the whole seam as pure waste. The per-body price is honest; the "waste"
framing needed the candidate ratio instead. What this lens also nearly missed: the
in-situ path was blocked by an API hazard a trader would call a broken order gateway — the
measurement had to fall back to the synthetic book, and the dossier says which numbers are
measured and which are inference.
