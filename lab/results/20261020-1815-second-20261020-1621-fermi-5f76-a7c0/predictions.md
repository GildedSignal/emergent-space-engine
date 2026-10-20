# Predictions — written before the decisive arms (C1 control, D1 deletion, S1 saturation)

Exploratory arm already flown (disclosed, like 5f76's A1 anchor): the backtrace arm BT
(K=10⁴, seed 1, coast, 30 s, `ES_BT=1`) — it NAMES the two ≥2 KiB ladder sites:

- the capped ladder (sizes 3,584..57,344 B, 448×128 B elements) is
  `encounter.rs:188` `candidates.push` in `PlayerNeighbourhood::capture`;
- the short ladder (2,944..11,776 B) is `radial.rs` `Radial::candidates`'s `ids: Vec<u32>`
  grown by `extend_from_slice` past its cloned capacity.

Both are in the player's neighbourhood scan (`encounters_for_player`), i.e. 8994's "pull"
guess and the "re-pull" alternative are both wrong. The two sites are the census's two
array-builds, rung arithmetic closing (two starts at rungs 1–3, one at 4–5).

## The arms (decisive, same instrument, flight args `coast 30 2000 12`)

- **C1** control: instrument only, K=10⁴, seed 1 — my box's A1 (expect player ≈ 193 KB/item,
  ship 1.4–1.5 KB/kick, realloc share 79–80%).
- **D1** deletion: C1 + `with_capacity` at the two named sites (encounter.rs: candidates
  pre-sized to the near-list length when the radial index answered; radial.rs: `ids`
  pre-sized to `unbounded.len() + hit`, both exact upper bounds) — allocation-pattern-only
  change, canonical outcomes must not move (kicks/events/items identical to C1).
- **S1** saturation: instrument only, K=6×10⁵, seed 2 (the K=10⁶ arm the checker named
  exceeds this box's 2 GB/process ceiling at the shipped 2,348 B/body build ≈ 2.35 GB;
  6×10⁵ ≈ 1.4 GB is the nearest feasible point — the cheapest decisive part, said so).

## P1 — the deletion's size (D1 vs C1, the gold experiment's number)

The two ladders carry ~136 KB/item of the ~193 KB/item player term (5f76). Exact bounds
replace each ladder's doubling traffic with one exact alloc: capped ladder ~109 KB/item →
one ~57 KB alloc; short ladder ~27 KB/item → one ~12 KB alloc.

**Prediction: D1's player term lands at 115–135 KB/item (a 30–40% cut, i.e. roughly
"half the ladder traffic"), player-scope realloc calls fall by >80% (≈332 k/flight →
<70 k), realloc share falls from 79–80% to under 40%.**
Kill bar for the SITE-naming claim: if D1's player term does not drop by at least 25%,
the two named sites are not the census's two arrays (the backtrace named something else).

## P2 — canonical neutrality

with_capacity changes only allocation timing, never state (integer-exact law; addresses
enter nothing). **Prediction: D1's kicks, events and all five items[] counts equal C1's
exactly** (same seed). Any difference voids the deletion arm (VOID, not a smaller gain).

## P3 — the player law's shape under the deletion

The 194 KB/item constant is the scan's two ladders + ~57 KB small calls. **Prediction:
D1's player term is again K-flat** (I fly only K=10⁴; the claim is not re-based on this
arm — the shipped constant stands, the deletion is a priced option).

## P4 — the ship marginal's saturation (S1)

Seed-2 series so far: 1.53 (10⁴) → 2.18 (3×10⁴) → 2.99 (10⁵) → 3.88 KB/kick (3×10⁵,
checker; slope ≈ K^0.3, decelerating). **Prediction: S1 reads 4.1–5.0 KB/kick** — still
rising, decelerating further. If it reads ≥ 7.1 KB/kick the 10⁹ row's top hits 100% of
60 GB/s at λ = 8.4×10⁻⁵ and the "still closing" verdict dies; if it reads ≤ 3.88 the
rise has turned and the row's top is pinned at 54%.

## P5 — S1's player constant (free by-product)

**Prediction: player term at 6×10⁵ stays within ±3% of 194** (K-flat law, fifth decade);
peak RSS under 1.8 GB (else the arm does not count — killed process).

## What would make the whole run wrong

The backtrace samples (first 120/bucket + every 400th) could miss a rare phase-only site;
mitigated by the stride. The 6×10⁵ saturation point is one draw short of the named 10⁶ —
if its reading is used as "the" top rather than the top of the flyable range, that is
over-claiming; I will cite it as the nearest-feasible decade point.
