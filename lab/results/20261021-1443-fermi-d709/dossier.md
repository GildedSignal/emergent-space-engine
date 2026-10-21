# The belt's boundary comb priced: a 29–38-core row at 10⁹, and the lever that becomes mandatory as the kick falls

The belt's BOUNDARY comb — the second half of the clock stream, unpriced in every composed 10⁹ total — fires at 0.98–0.99× the kick rate (3.57–3.66×10⁻⁵/body/game-s, belt-pure) and costs **8.7–9.9 µs x86** per item (N-flat 3×10⁴→10⁵, three flights, seeds 1–2), so at 10⁹ bodies and rtf 100 it is a **29–38-core row** on the shipped cadence and **5.7–7.7 cores after the mandatory split8×survival cut** — by itself at or above the whole 4-core budget — and its share of the two-comb stream *rises* from 14.5% today to **68% at the ledger's own 4.9 µs/event kick bar**, so deleting it (15d7: its certificates never fire on the belt's own stream) is worth **2× on the closure bar**, not the 1.2× era-time saving the record carried.

## Bottleneck

`budget-1e9` line 1: "the belt's boundary items are unpriced" — the dominant CPU row (the stream) was composed from kicks only, and od 5 names the pricing. This run prices it and folds it into the closure: the correction is ≥2× on the closure bar (the row alone exceeds the 4-core budget after the cadence cut), which decides the priority of 15d7's deletion against `wt/cadence`/`kickcost`.

## Evidence

Instrument: `Stats` gains ship-class per-comb wall timers (`ship_kick_ns`/`ship_boundary_ns`, classified by the plan's first item outside the timed window — the same item `resolve_body` resolves), read by `crates/universe/examples/brow.rs` (the ladder population `scenario::plane_extra`, settled to canonical cuts, no budget/frames). Numbers regenerate with `regen.sh` (build + 3 flights + arithmetic, ~4 min); raw flights in `out/`.


- **The regen pass (fresh flights, `regen.sh` exit 0 in 109 s)** composes the steady window (gs 33k–89k, two full clock periods): kick 179.9–203.3 + boundary 29.8–38.0 = 209.7–235.6 cores shipped; after split8 36.6–41.3 + 6.1–7.7 = 42.6–47.9 x86 (24.7–27.8 M1-anchored); steady rate_b/k 0.991–0.993.
| flight (89k game-s ≈ 3 clock periods, coast) | kick µs | boundary µs | rate_b/k | boundary row @10⁹ rtf100 | after split8 (÷4.92) | M1-anchored (×0.58) |
|---|---|---|---|---|---|---|
| n=3×10⁴, seed 1 | 56.2 | 8.96 | 0.981 | 30.2 cores | 6.1 | 3.6 |
| n=10⁵, seed 1 | 50.7 | 8.66 | 0.991 | 29.2 cores | 5.9 | 3.4 |
| n=10⁵, seed 2 (held out) | 50.8 | 9.93 | 0.991 | 36.0 cores | 7.3 | 4.2 |

- **Rate law (steady window gs 33k–89k):** λ_k = 3.59×10⁻⁵, λ_b = 3.57×10⁻⁵ per body per game-s (1e5 s1) — one comb each per 2.79×10⁴ game-s clock period, as step.rs:717-718 inserts them. The page's λ = 4×10⁻⁵ is the population average (locals fire faster); the belt-pure rate is 0.90× of it.
- **Era alternation reproduced:** kick-era chunks wall 6.1–7.1 s, boundary-era 1.1–2.3 s (8365's 5.6/1.6 s walls), and the comb costs are payload: 50.7/8.66 µs ⇒ the 5.8× wall ratio is the cost ratio at equal counts.
- **The instrument discrepancy resolved:** 8365's 5.9–8.6 µs stands (my direct full-item timer: 8.66–9.93); 3aec's "boundary 18.4 µs x86" is not the belt's own coast item (2.1× above every flight here, both seeds, both rungs).
- **The combs are the stream:** opens 561–626, handoffs ≤ 14, lost ≤ 5 over 89k game-s, against 600k–650k combs.

## Predictions

Written before the flights (`predictions.md`): rate_b/k = 1.00±0.05 ✓ (0.981–0.991); boundary cost 6–10 µs x86 ✓ (8.66–9.93) with 8365's number confirmed and 3aec's refuted on this stream ✓; kick cost 40–50 µs — measured 50.7–56.2, the top of the band (this box runs ~10–20% hot vs the record's 44.7–45.9, inside the record's ±22% machine floor; the ratio cost_b/cost_k = 0.14–0.20 is the load-independent part and matches 8365's 0.13–0.19); N-flat within ±20% ✓ (−10%/−3% from 3×10⁴ to 10⁵); composed row 21–35 cores ✓ (29.2–36.0, seed 2's 36.0 just over the top of my band). Nothing in the kill direction: the row clears the 10-core kill criterion at 3×.

## What would make it wrong

- The timer classifies by the plan's first item before `resolve_body`; a kick item that resolves as something else (a `NoBoundOrbit` refusal, a crash) would land in the kick bin — on this stream refusals are 0 and lost ≤ 5, so the bin error is < 10⁻⁵.
- Settle (not frames) is the path: if the frame path's boundary items cost differently (the held-scan margin), the row moves — but the comb's work (readout, norm, anchor, requeue) is path-independent, and the era walls match the frame-record's alternation.
- The split8 and M1 corrections are the page's own factors (4.92×, 0.58), not measured here; the row's x86 band is what this machine certifies, orders of magnitude only per the lab rules.

## Cost of adopting, and fit with PRINCIPLES

Adoption is a row in the ledger, not code: every composed total that contains the stream gains the boundary term at the measured cost ratio 0.14–0.20 of the kick item — after split8 that is +3–8 cores x86 depending on the stream anchor (the page's totals band 22.5–43.4 becomes ≈ 25.5–50.7; the split8 stream row 39.3 → 45.2–46.6 at the shipped kick anchor). The design consequence lands on 15d7's open deletion: "The cheapest compute is compute not done. Delete before optimizing" — the boundary comb's certificates never fire on the belt's own stream and are derived-when-looked-at, so the row is deletable work, and the closure arithmetic now says the deletion is *required*: with the comb kept, the two-comb bar is 2.46 µs/event blended (half the page's 4.9), and the boundary row alone (5.9–7.3 cores x86 after split8, 3.4–4.2 M1-anchored) spends the whole 4-core budget before the kick spends anything. Alternative to deletion: absorb the boundary's certificates into the kick item (its work is 17% of a kick's), which the ledger should price next.

## The lens

Fermi (rate × cost, composed to the row): the estimate was written first and held. What the lens may have missed: the machine's ~10–20% heat vs the record (cost ratios, not absolute µs, are the portable constants); and I did not fly burn (thrust changes the kick item, not the comb cadence — the boundary row is cadence-owned, so the coast row is the row).
