# Dossier — 20261018-2155-spacex-9292 (spacex)

## Claim

The seen stream's content law survives the burning player: under a continuous burn the far sky's churn is one shared observer-side warp (displayed angle p99 = |dβ| per frame), never emitter-side (0 of ~6.8×10⁶ far row-pairs (≈4.7×10⁶ under burn) move half a display cell in one frame, at every dial flown including L15), so a window record over the cold store serves the wildcard at O(2π/θ_f cells) + O(~350 near rows) per frame and the shipped gather's O(K) walk is deletable under burn too.

## Bottleneck

The board's first focus term: which per-frame walk breaks first as the plane grows. dcf1 (today) named the view gather the ladder's first N-growing term (~5 µs/seen body on the M1; 19-2575 ms here at 10³-10⁵). cc75 (today) killed the far rows' information content — but on a static coast census, leaving the wildcard and the patina's churn unmeasured (its own blind-spot list). This run measures the missing axis: the surprise rate of the wire's own `seen` array under the burning player. Expected gain: the record's update law is now sized on measurement — its per-frame work is bounded by cells + near rows, K-independent, which deletes the per-frame K-walk (10⁵-10⁶× less per-frame work at 10⁵ on the content side; the walk itself is the thing deleted, exactly the row-set deletion 2df1 built, now licensed under burn).

## Evidence

All numbers from `crates/universe/examples/skycensus.rs` (print-only probe, shipped `gather_cached`, the same call the page flies; `work/patch.diff` carries it), plane ladder scene seed 1, rtf 100, 12 ms engine budget, θ_f = 8e-3 (cc75's 800-px floor), near = light-seconds < 100 (cc75's split). Reproduce with `lab/results/20261018-2155-spacex-9292/regen.sh` (~4 min). Logs in `work/`.

- **Coast controls (P1, P2 hold):** 10³: 463/785 far cells occupied, alone 0.63; 10⁴ and 10⁵: **786 = capacity FULL**, alone 0.0038 → 0.0000, 12.4 → 127 rows/cell — cc75's census reproduced on its own rungs. Near set 344-355 rows at every K, flat. Coast far churn p99 2.2e-7 rad/frame (1.8×10⁴ below θ_f/2), crossed-cell 0.0007-0.0009 %/frame.
- **Burn L8 (P3, P4, P5 hold):** β 7.4e-5 → 1.0e-3 over the flight (10⁴). Far churn per frame: displayed p99 4.86e-6 rad ≈ |dβ| 4.92e-6 (the churn IS the aberration); root-frame (emitter-side, from `offset`) p99 2.2e-6. **0 of 2,099,088 far row-pairs move > θ_f/2 in a frame**; crossed-cell 0.0315 %/frame (10⁴). Cells whose far-count changes: p50 6/frame (0.8 % of 786). K-law: crossed-cell per frame 0.032 / 0.032 / 0.036 % at 10³/10⁴/10⁵ — flat, = dβ/θ_f as aberration demands. Long arm (1439 intervals): still 0 past θ_f/2, max 8.4e-5.
- **Burn L15 (the top dial, 128× dβ, held-out):** dβ p50 6.3e-4/frame. Displayed far p99 2.29e-3, max 2.45e-3 — approaching but under θ_f/2; crossed-cell 6.16 %/frame (= dβ/θ_f × geometry); cells changed p50 60/frame (13 % of occupied); root-frame p99 3.65e-4 = 6.3× below displayed (ratio p99 disp/root 6.27). **Still 0 pairs past θ_f/2 emitter-side; 0 past θ_f/2 displayed.** Near set churn 19-25 %/frame.
- **Patina (P6 holds):** |Δ ln shift| per frame p99 = dβ (4.9e-6 at L8; 2.5e-3 at L15) — the Doppler swing per frame is small and shared-side; per-cell colour/count aggregates change on ≤ 13 % of cells per frame at the top dial, ≤ 0.8 % at L8.
- **Context (shared Linux box, orders only):** warm gather 19-27 ms at 10³, 232-236 ms at 10⁴, 2575 ms at 10⁵ (18-26 µs/body; the M1 runs measure 5-7).

## Predictions

`predictions.md` was written before the decisive arms; the burn arms, the stride-10 deltas at 10⁵ and the patina were the held-out cases. P1, P2, P4, P5, P6 held as written. P3 held and its KILL did not fire (0 % emitter-side past θ_f, against the 1 % bar) — but P3's letter under-promised: I predicted emitter-side < θ_f/10 for 99 %; measured is < θ_f/2 for 100 % with p99 at θ_f/11 at L15. One miss in the letter: the near-set churn under burn (5-25 %/frame) is larger than the "O(near) cheap" framing implies — it is the one tier that must be re-served per frame; its size stays K-flat (~350 rows).

## What would make it wrong

- A scene whose far field is not angle-smooth (a dense formation at one bearing, the taleb-09b5 ruin class): the histogram/warp argument assumes smoothness; crossings then concentrate and per-cell churn is no longer bounded by the shared warp.
- Zoom: at belt zoom ~N rows go on-canvas (62c1's checker); the θ_f floor then shrinks with zoom and the churn fraction scales as dβ/θ_zoom — unflown here.
- Bodies going hot (kicked into resolvability): the hot-set trigger (open direction 10's other half) is unmeasured; a kick wave could inject emitter-side churn this census never sees (no kicks hit the far belt in these arms beyond the burn's own).
- The L15 arm is one flight length (500 game-s); at γ ≫ 1 the aberration warp's per-frame magnitude falls (dβ ∝ 1/γ² per game-s at fixed proper thrust), so the top dial flown is near the worst case for churn rate, but the accumulated warp over long flights re-windows the whole sky and the record's re-bin then must be global once — priced by ee30's drain, not measured here.

## Cost of adoption

None as code: the probe is print-only and the tree is restored. The design consequence is 2df1's row-set deletion extended to the burn axis (it was coast-scoped by 649c's bit-reproducibility): store far rows' root-frame angles once, serve the display by composing the shared (β, displacement) warp per frame at O(cells), re-walk only on zoom, feed, or hot-set events. Fit with PRINCIPLES: "Compute only surprises. Cost follows change and entropy. Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (3) — the burn's surprise is one warp vector plus ~350 near rows, not K rows; "the best part is no part" (17) — the walk is the part deleted.

## The lens

SpaceX's delete-first eye sized the idiot index (K bodies walked per frame against O(cells) of information changing) but its blind spot is one-way doors: this census says the deletion is *safe under the wildcard as flown*, and I flew the top dial and a 4× longer burn to attack my own claim — yet one scene, one seed class, no zoom, no kicked-hot bodies. A rocket lens also under-weights the record's failure modes: a stale aggregate under zoom is a player-visible wrong sky, not a lost test.
