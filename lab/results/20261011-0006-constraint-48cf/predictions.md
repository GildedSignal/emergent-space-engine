# Predictions (written before the decisive runs)

Claim under test: **the readout, not the engine, holds the frame at goal scale, and its cost is a tick (independent of change).**

Already measured (exploratory, will not be tuned on):
- plane rtf 100, 71→417 bodies: view_gather share 66%→55% of frame; engine share 21–25%; engine p99 5.9–6.6 ms vs the 5 ms budget.
- galaxy 10⁹ ships: store 104 MB; render median 32.3 ms (far), 36.9 (mid), 26.2 (deep) at 960×540, 4 threads; 19–22 ns/sample; all 200 frames over 16.7 ms.

Held-out cases (not yet run):

1. **P1 — cost vs change.** `galaxy --bench --rtf 100` (10× slower motion, same scene, same 60 Hz pace): if the readout computed only change, median_ms should drop ~10×. **Predicted: it stays within ±20% of 32.3 ms** (far view), because the render is a full recompute per frame — a tick by PRINCIPLES #14.
2. **P2 — samples vs pixels.** `galaxy --bench --w 480 --h 270` (¼ of the pixels, same tubes): **predicted median_ms drops by less than 40%** (≈ stays in the 20–30 ms band), i.e. per-sample splat work dominates per-pixel reduce/tone-map; cutting pixels will not buy smoothness, cutting per-tube work will.
3. **P3 — store scaling shape.** `galaxy --bench --ships 100000000 --tubes 100000` (10× fewer ships via tubes): **predicted peak RSS and render median drop sublinearly (render ∝ tubes, not ships)**, confirming "store the generator" already holds and memory is not today's constraint (store ≈ 100 B/tube-equivalent vs 2293 B/live body on the plane).

If P1 or P2 fails in the cheap direction (cost does track change / pixels dominate), the constraint claim is wrong and the readout is already surprise-driven; then the constraint is the engine's kick path (76 µs, 0% exact memo hits).
