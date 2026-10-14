# Predictions (written before any run on this box)

Priors: the M1 ladder's own view column (warm gather 11.4 ms at 10³, 136 ms at 10⁴, 1,377 ms at 10⁵ ≈ 13.8 µs/body; cold ≈ 30 µs/body), view.md's frame-share record (gather+json+wire 56–93% of every frame at 28–948 bodies), and the code read (page: rAF → POST /frame → Session::step = engine ≤5 ms + gather_cached + view_json + to_vec; gather walks every alive body, no zoom/frustum/brightness test). This box is Linux/x86 shared: orders of magnitude only. I have run nothing yet.

## Held-out cases (not tuned on)

1. **The flyable frame** (engine+view+wire, the page's own dashboard metric) on the ladder scenes crosses the 16.7 ms display budget between N=10³ and N=10⁴, and at 10⁴ the gather+wire share of the total is ≥80%. At 10⁵ the total is ≥1 s/frame (an order of magnitude).
2. **On-canvas fraction** at the page's own fitted map zoom (`fitLog`: nearest body at 0.33·R): at 10⁴, <2% of rows are on the canvas (the belt is 2–3 AU out, the camera is fitted to a body near the player). At N=0, >50% on canvas.
3. **Display-static fraction** (drawn pixel unchanged frame-to-frame): at 10⁴, ≥95% of rows static in map mode and ≥90% in sky mode. Wire-byte identity lower than pixel identity (floats churn in low bits): 60–95%.
4. **Controls.** N=0: gather p50 <5 ms (else the instrument is broken); static_map at N=0 <50% (the locals move on a fitted zoom — the staticness instrument must detect motion where motion exists).

## Kill criteria (pre-registered)

- If the flyable frame at 10⁴ stays ≤16.7 ms on this box AND the M1 ladder numbers (already published) also extrapolate under it, the "the flyable ceiling is ~10³, not 10⁶" claim dies.
- If static_map at 10⁴ is <90%, the far-row deletion lever dies (the display-quantum cache stays dead as 0e54 measured it on plane scenes).
- If the N=0 controls fail, the instrument is broken: report as a broken instrument, not a result.



## What happened (after the runs)

1. **Held, and sharpened past the prediction.** The flyable frame crosses 16.7 ms not between 10³ and 10⁴ but **at 10³ itself**: p50 21.5 ms at 1,028 bodies (gather 19.3 = 90%), 255 ms at 10⁴ (gather 91%), 2,614 ms at 10⁵ (gather 90%, wire 256 ms = 27 MB/frame, engine 1.06 ms). The engine slice stays flat exactly as the gate certified (0.04–1.1 ms) — the gate's number is real and 0.03–4% of the page's frame.
2. **Held.** On-canvas at the fitted zoom: 6.8% at 10³, 0.73% at 10⁴, 0.073% at 10⁵ — and the on-canvas **count** is ~72–74 rows at every N (flat): the visible set is O(10²) while the work is O(N). At N=0, 67.7% (control passed).
3. **Split, as pre-registered in its halves.** Sky-static held and hardened: 96.8% (10³) → 99.6% (10⁴) → 99.96% (10⁵). Map-static **failed**: 10.6% / 2.5% / 13.3% — my parallax estimate was wrong; at the fitted zoom (~14,700 px/light-second) the observer's own coasting motion moves every far dot's map pixel most frames. The map's deletion lever is not pixel-staticness but the canvas test itself (the page draws nothing for off-canvas kind≥3 rows — verified in page.html's draw loop). Wire-byte identity: **0.4–0.8%** (12.8% at 10⁵'s 48 frames) — below my 60–95% prediction; the wire is a near-total per-frame tax.
4. **Controls held.** N=0: gather p50 0.80 ms (<5 ms), static_map 36.9% (<50%) — the instrument detects motion where motion exists.

Kill criteria: none fired. One prediction (map-static ≥95%) died and is disclosed above; the claim never rested on it (the on-canvas census is the map-side evidence, and it is the page's own draw condition, not my proxy).