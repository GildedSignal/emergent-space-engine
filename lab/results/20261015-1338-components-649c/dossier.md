# The in-band view gather: priced, and floored exactly (the far rows are free between the tube's own quanta)

**Claim.** The flyable loop's per-frame view gather — the pilot's instrument, the one O(N) per-frame walk left in the shipped plane — costs 19-24 µs a body every frame (≥97-99.8% of the flown frame at 10⁴-10⁵; the nladder page's rtf-0.7 crawl), while between the tube's own time quanta its output on far rows is **bit-reproducible from one cached emission point plus the fresh observer state** (measured exact to 1e-16 for 715/715 and 9,714/9,714 far rows, 213+ and 260 frames), and a burn (L8, L15) changes only the observer side, which the closed form takes fresh: far-row drift is identical coast vs burn. The per-frame read set is the near set, O(310) rows at every N. Idiot index at 10⁵: 100,028 readouts a frame against ~310 + N/horizon ≈ 314 — ~300×; at the display quantum the far rows' measured free-run horizon is 2.7e4 frames (p99, map half-pixel), so the floor cost is ~1-4 ms against the shipped ~1.9-2.4 s.

## Bottleneck

Board: "bodies in the flyable engine" — the per-frame walks term ("which term breaks first as the plane grows … per-frame walks"); nladder open direction 5 (the in-band gather crawl, unpriced); view open directions 2 and 3 (the sky's near field; the burn burst, "the served set is then O(visible); measure it"). PRINCIPLES #3 ("Nothing is evolved that can be derived when looked at (clocks, redshift, **views**)") and #28 ("The view is an instrument"). The gain: the flyable N ceiling moves from the gather's 10³ back to the engine's own 10⁶+ (the row-set deletion's missing half), and the burn burst is deleted at the physics level rather than paid.

## Evidence (all numbers from `regen.sh`, this Linux box; orders of magnitude per the lab rule)

Instrument: `crates/universe/examples/view_floor.rs` (this run's patch), one flight per arm in the page's own loop order (`gather_cached` → keys → `frame_to`), `plane_extra` ladder scene, rtf 100, 12 ms engine budget. The floor instrument freezes each row's emission geometry at one frame (emitter position when the light left + Doppler denominator) and recomputes the row each frame with the **fresh** observer state through `view.rs`'s own `aberration` and shift form — the definition of a no-readout row.

| N | mode | gather p50 (µs/body) | readouts/emitter | engine p50 | rtf achieved | far rows: drift p99 (rad/frame) | near rows |
|---|---|---|---|---|---|---|---|
| 10³ | coast | 20.1 | 1.67 | 0.055 ms | 77 | 6.1e-8 (horizon 2.7e4 frames, map ½px) | 308 @ 8.7e-3 |
| 10³ | burn8 | 22.0 | 1.96 | 1.94 ms | 68 | **6.0e-8 (identical)** | 308 @ 2.8e-3 |
| 10⁴ | coast | 24.0 | 1.96 | 0.057 ms | **6.7** | **8.5e-18 (p99 exact; max 1.6e-9)** | 309 @ 8.1e-3 |
| 10⁴ | burn8 | 23.8 | 2.00 | 1.43 ms | 6.9 | **8.5e-18 (identical; max 4.158e-7 vs 4.156e-7)** | 309 @ 2.0e-3 |
| 10⁴ | burn15 | 24.1 | 2.00 | 10.5 ms | 5.7 | **8.5e-18 (identical; bit-frozen 4e-16 deep into the burn)** | 309 @ 7.5e-6 |
| 10⁵ | coast | ~23 (2.46 s/frame wall) | (regen) | ≤0.06 ms | **0.68** | **3.084e-17 (99,701/100,028 rows exact over the whole curve)** | 322 @ 7.7e-3 |
| 10⁵ | burn8 | 24.8 (2,477 ms p50) | 2.00 | 6.4 ms | **0.66** | **3.084e-17 — digit-identical to coast** | 322 @ 7.2e-3 |

1. **Exactness, not approximation.** Over a 999-frame curve (10³, freeze at frame 100) all 715 far rows hold err ≤ 3.3e-16 for ≥213 consecutive frames; the first emission step lands 355-542 game-s after freeze; afterwards the error envelope grows at the orbital rate (steps of the tube's own time quantum, staggered across rows). At rtf 10⁴ (167 game-s a frame) the same rows move every frame (drift 1.06e-5 rad/frame = orbital speed × frame), confirming the residual is the emitter's quantum, not the instrument. At 10⁴, 9,714/10,028 rows never step in 260 frames (433 game-s).
2. **The per-frame direction motion of a far row is observer parallax, closed-form.** The frozen-row prediction (stale emission, fresh `position`+`beta` through `aberration`) reproduces the shipped gather's direction to 1e-16 while it moves 6e-8 rad/frame — the walk recomputes what the cache already knows.
3. **The burn is observer-side.** Coast vs L8: far-row drift 6.10e-8 vs 6.02e-8 (10³), 8.540e-18 vs 8.540e-18 (10⁴, max 4.156e-7 vs 4.158e-7); readouts/emitter 1.67→1.96 (≤2.0; L15: 2.00, µs/body 1.00× coast). View open 3's "the served set is then O(visible)" is wrong at the physics level: aberration and Doppler are observer-side functions the closed form evaluates exactly on a frozen row; the burn adds only the near set (~310 rows), the same O(locals) as the sky's near field (open 2).

The 10⁵ coast flight is the crawl, reproduced: 80 frames in 196.6 s of wall — rtf 0.68 achieved against 100 asked, the engine's own slice ≤ 0.06 ms a frame (burn8: 2,477 ms p50 gather against 6.4 ms engine, rtf 0.66; the gather is 99.7% of the flown frame). The burn15 arm is the strongest: at level 15 (engine p50 10.5 ms) the far rows hold 4e-16 through the burn and the emission step lands at the same curve frame (~k 226-229) as in the coast and L8 arms — an arm-independent, seed-aligned step of the tube's own time quantum, not any observer effect.

## Predictions

Written before the decisive grid (`predictions.md`). Held: 1 (linear µs/body 20.1→24.0, readouts 1.67→2.00), 2 (engine ≤0.06 ms coast; gather 99.76% of the flown frame at 10⁴, 99.7% at 10⁵ burn8; rtf 6.7-6.9 at 10⁴, 0.66-0.68 at 10⁵), 3 (burn8: readouts 1.96≤2.2, µs/body 1.09×, far rows bit-frozen through the burn), 4 held with margin: readouts/emitter 2.00 ≤ 3.0, µs/body 1.00× coast, far rows bit-frozen 4e-16 through the burn with the emission step at the same curve frame as coast, 5 (near rows depart ≤2 frames; count 308-309 at 10³ and 10⁴ — N-independent), 6 (10⁴ horizon ≥ 5,000 frames — measured: p99 exact over the window, no departure at all; at 10⁵ 99,701 rows exact with coast and burn8 digit-identical at 3.084e-17). Held everywhere; no kill criterion fired.

## What would make it wrong

- The far-row exactness is the belt domain (2-3 AU, quiescent, pre-first-wave at 10³; 10⁴ crosses no wave either — 433 game-s ≪ 13,051). A wave tick (every ~2.8e4 game-s) steps every far row at once — that is an engine event the readout then rides legitimately (one readout per row per kick, the same event the kick itself pays). Near a doll handoff or during the player's own rebinds the frozen-row denominator may drift faster; unmeasured.
- The horizon numbers are rtf-100 frame quanta (1.67 game-s/frame); at other rtf the horizon in frames scales, in game time it does not (the drift is game-time physics).
- The display quanta (map ½pixel 1.6e-3 rad, sky 2.7e-4) are my definition of the pixel scale (1920 px, 360° map / 60° sky); 2df1's wheel used its own slack. The exactness result (1e-16) does not depend on any quantum.
- The near set (~310) is this scene's (a few hundred ships about Home and the Moon per `plane_extra`); a battle scene changes its size, not the structure of the claim.

## Cost of adopting, and fit

Adoption is 2df1's row-set deletion (already built for the map) with two upgrades from this run: (i) the far-row due rule can be the **emission-step event** (the tube's own quantum / the kick events), not a drift estimate — bit-exact between steps; (ii) the burn needs no far-row re-reads at all (re-aberrate client-side from the frozen geometry + fresh observer state: exact). What remains Θ(N): the birth/death feed (2df1's p99 owner, the engine's event feed — already open direction 1) and the fill. PRINCIPLES: "Compute only surprises… Nothing is evolved that can be derived when looked at (clocks, redshift, **views**)" — the shipped gather computes non-surprises 60 times a second on every body; this run measures the surprise rate of a view row directly (zero between the tube's quanta, exactly).

## The lens

The components lens priced one component (the view's per-frame read) against its floor. What it may have missed: the cost the deletion moves to the client (re-aberrating O(visible) rows per frame in the page — a wire/draw question, not an engine readout, but the page pays it); and the scan seam's memory fence (d7bc) interacts with any policy that holds per-row state per observer — a second observer doubles the cache, not the readouts. The mechanism of the tube's time quantum (which unit steps at 355-542 game-s) is bracketed by measurement but not pinned to a constant in `crates/space` — a scout can name it in one read.
