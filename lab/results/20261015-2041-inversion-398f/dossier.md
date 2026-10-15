# Dossier — 20261015-2041-inversion-398f (inversion)

## Claim

The nladder memory story has a blind axis — every quoted win (8b89's rss 979→20 MB, standing
arcs → the centres) was measured at cuts ≤ 20k game-s, at most one settle wave — and the one
per-body term that grows with play, the causal history stack (`PlainBodies.history`: one
336-B `Segment` per retired binding, each pinning its full compiled arc under shipped ctl),
is measured down that axis: **the belt saturates flat (1.04 segments/body at 32k/48k/96k,
arm-independent; digest identity ctl==all at 96k) while the infalling comet class grows
linearly with play — ~80 → ~835 segments per comet from 3k to 32k (exponent +1.0; ~28 MB
retained per comet, rss 2,816 MB on a 171-body scene against the 10,000-body belt's 62 MB) —
and the prune cannot stop it: a segment leaves only past `until + 2·light_distance(body→observer)
+ 2²⁶`, inert (~10⁷ game-s) at the class's ~10⁴ AU, so the growth is the light cone's own
memory bill (PRINCIPLES 23), not a bug; `ES_LAZY_ALL` shrinks each retired segment ~75× but
bounds nothing.** No single-cut flight can certify this adoption's memory claim.

## Bottleneck

Memory per live body at 10⁹ (the board's first live question) — specifically the adoption
now one flight from gold (8b89, silver: both checkers name "compose ALL + `ES_RETAIN_HOT`,
fly 10⁵ coast + burn, close it in one flight"; those are 20k cuts). The history stack is the
term those flights cannot see: depth-driven, class-dependent, causally forced. The finding
re-prices the adoption (per-segment 336 B under ALL vs a pinned ~25 kB arc shipped) and names
the exact term any 10⁹ ledger must charge every doll-commuting population: crossings ×
segment size, retained for 2·r/c game-s each.

## Evidence

All numbers regenerate by `regen.sh` (patch + build + flights + `table.py`); Linux x86
8-vCPU shared box, orders of magnitude only. Base = 8b89's patch plus this run's 15-line
instrument (`Universe::history_census`: per-body history segments, plan items — printed at
the canonical cut; the count is read without minting). Anchors reproduced before any deep
flight: 10⁴ coast ctl digest `5e8c9e24…5fbab6f` = e0f9's published; ALL identity at 20k;
belt 48k ALL digest `f8b52855…` = d6ba's published 48k anchor.

**P1 — the belt saturates (held).** `10000 coast 1 1000`, ALL, and ctl at the deepest cut:

| cut | arm | seg/body | max | bpb | rss | digest |
|---|---|---|---|---|---|---|
| 32k | all | 1.04 | 37 | 974 | 34 MB | `cb1747c6…` |
| 48k | all | 1.04 | 36 | 1,004 | 37 MB | `f8b52855…` (= d6ba's) |
| 96k | all | 1.04 | 36 | 976 | 46 MB | `e75c90f2…` |
| 96k | ctl | 1.04 | 36 | 1,668 | 62 MB | `e75c90f2…` (**identity**) |

Exponent 3k→96k in segments: −0.00. The count is arm-independent (ctl = all at 96k): the
prune governs the stack, not the seam. Keep-behind at the belt's 2.5 AU ≈ 2·2.5·499 s +
2²⁶ ticks ≈ 2,800 game-s ≪ the 26k settle period — every wave drains. **P3 held on the belt:
digest identity at 96k, 4× the deepest prior identity cut.**

**P2/P4 — the far class grows linearly; shipped pins each segment's arc.** `stargraze`
(seed 3, rtf 1000), ctl = shipped verbatim:

| scene | cut | segments | per comet | rss | bpb |
|---|---|---|---|---|---|
| N=100 | 3k | 7,957 | ~80 | 273 MB | 20,206 |
| N=100 | 32k | 83,496 | ~835 | 2,816 MB | 165,751 |
| N=25 | 32k | 21,257 | 850 | 716 MB | 76,492 |
| N=25 | 64k | 42,186 | 1,687 | 1,421 MB | 147,536 |

Growth exponent 3k→32k: **+0.99** (46.5 → 479.9 per census body; the per-body column is
diluted by the ~71–74 non-comet bodies — per comet: ~80 → ~835, and N=25 reproduces 850 at
32k: the per-comet cost is intensive, ~26–28 MB each at 32k under ctl, `bytes_of`'s
4,096-B Live-passage placeholder under-booking the true pin). Max segments on one body:
2,770. The 100-comet scene out-weighs the 10,000-body belt ~45× in rss.
**Mechanism, read off shipped code** (`universe.rs:572,1273,1299`): `light_distance` is the
body's distance from the observer; a segment is prunable only past
`until + 2·light_distance + 2²⁶`; at ~10⁴ AU that is ~10⁷ game-s — inert at any playable
depth. Every doll crossing retires a binding that stays for the cone. This is causally
forced (a reader inside the cone may still ask for any retired binding), so it is the
representation's truth, not a leak to "fix" — the question is what a segment must *store*.

**The deletion's share, flown at depth on the far class (P5, reported).**
`25 stargraze 64000` under ALL: digest `14a740d4…` = ctl EXACTLY (identity holds at depth
on the far class too), the history stack IDENTICAL (42,186 segments — arm-independent on
comets as on the belt), standing arcs 1,072 B, **rss 23 MB against ctl's 1,421 MB (62×)** —
every retired segment rides at the slot, not the pinned arc. The count still doubles with
depth under ALL exactly as under ctl: shrunk 62×, bounded not. The bill without retention:
841k cycle re-mints (p50 3.6 µs) + 376k passage re-mints (p50 580 µs) inside a 255-s wall
flight — the no-retention tax `ES_RETAIN_HOT` exists to pay down. Belt bill under ALL grows
~linearly with cut (1.46M promotions at 32k → 4.28M at 96k; 150k passage re-mints).

## Predictions

`predictions.md` was written before any deep flight (only the 20k anchor smoke preceded it).
P1 held exactly (1.04 flat; bpb band ±3%). P3 held on both classes (belt identity at 96k; comet N=25 identity at 64k: `14a740d4…` ctl==all). P2 held:
the comet stack does not saturate — the pre-registered "≥ 1.5× growth 32k→64k" is decided by
the 3k→32k exponent +1.0 and the 64k row doubles it again (850 → 1,687 per comet, ×1.985 over ×2 depth — linear past the first settle too; 426.1 vs 214.7 per census body = 1.985× ≥ the registered 1.5×); P4 held (ctl grows; the class, not the deletion,
drives it). P5 held (linear bill).

## What would make it wrong

- If the 64k row (N=25) reads flat against 32k — i.e. the stack stops once the stream
  settles — the "unbounded" reading dies and the finding reduces to a large bounded constant
  (~835 segments ≈ 23 MB/comet shipped, ~280 kB under ALL) on the far class; the
  single-cut-certificates-nothing conclusion survives either way.
- The ~25 kB/segment pin is composed from the census's own arc sizes (w 10–20) and d6ba's
  checker's Live-passage census (25.6 kB); `bytes_of` under-books it, so ctl bpb columns are
  lower bounds.
- rss includes the engine baseline (~50–60 MB); the per-comet arithmetic subtracts none of
  it, so per-comet costs are upper bounds — the belt comparison holds the baseline fixed.
- The player's own history is exempt (`light_distance` = 0 for the player): the game's
  actual wild commute (the player flying out and back) is unmeasured here — the measured
  class is NPC comets on shipped scenes.

Adopting the finding costs nothing as code; it prices an adoption and names a certificate
requirement (depth clause + far class). Fit with PRINCIPLES: #23 "Nothing past c" — the
retention horizon is the light cone; #6 "Store the generator, not the generated" — a retired
segment under ctl stores the generated arc, under ALL the generator; #24 "The memory floor
is information" — the causal past is information the cone can still be asked for, and the
floor question is whether re-derivation can serve those asks cheaper than retention.

## The lens

Inversion flew down the cut axis where every prior run on this page flew across scenes and
arms at ≤ 20k. What the lens may have missed: the census reads at one canonical cut, so a
stack that grows and drains within a flight reads flat (the belt's 1.04 could hide a pulse —
d6ba's arc-level census says it does not); the far-class law is measured on comets only, and
the exempt player is the class the game will actually stress; and the ALL arm's comet depth flight ran at N=25 only (the N=100 64k arm would need
~5.7 GB and was killed to respect the 2 GB budget; the N=25 arm reads 62× lighter than ctl
at identical digest and identical stack).
