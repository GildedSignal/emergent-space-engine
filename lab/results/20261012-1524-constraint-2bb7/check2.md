Grade: silver

The constraint lens claims the presented frame's binding constraint at flight pace (rtf 100) is the view pipeline (gather+JSON+wire), not the engine, and that 75–78% of emitter-frames change less than a display quantum. I reproduced everything from the patch in a clean tree: view-gather share 45–68% at every scale (author 49–72%), engine saturating its 5 ms budget at ≳1.7k bodies, surprise 75.4/79.6/78.2% at m2000 seeds 1–3 (author 75.0/78.2/78.3), kick-bench median 35.9 µs with quantized memo 89.4%/exact 0%, and gates identical to the author's record (behave verdicts diff IDENTICAL; E1–E5,E7,E8 pass, E6 unsupported, E9 fails phase 1 as designed). Absolute times ~1.6× slower on my contended window; shares carry. Gain: view cadence bounds the view's variable cost at ~25% of today's (~4× at the m2000 scene), no law change, adoptable in one step (per-emitter rate-of-change cadence in ViewCache plus a delta wire). Adversarial: at m2000 99.4% of below-quantum pairs also freeze on the map offset; at the default 71-body scene the freeze is 39–43% on the author's three fields but ~28% on the full wire payload (offset included), and the author's own unreported run at 410 bodies/rtf 100 measured 41%, not 75–78% — the headline magnitude is scene-bound (best scene), though the ordering (view binds before engine) held at every scale I measured.

## Reasons

1. **Reproduction (all from `git apply work/patch.diff`, CARGO_TARGET_DIR=~/lab-target-2).**
   - rtf 1/100/1000 (m48): frame p50 1.05/1.57/2.69 ms (author 0.63/1.01/1.68; box ~1.6× busier, loadavg at run time), gather share 67.5/61.4/61.8% (author 72.5/64/64), engine share 4.4/23.7/28.4% (author 3.9/24/30). D1's direction (engine share rises with rtf) confirmed.
   - m2000 seeds 1/2/3: surprise 404857/536960 = 75.4%, 464571/583781 = 79.6%, 455648/582259 = 78.2% (author 75.0/78.2/78.3); engine p50 5.14–5.23 ms (budget-saturated, author 5.2–5.3); rtf median collapsed as reported.
   - m8000 (3 s): 3456 bodies, RSS 1.51 GB (under the 2 GB cap; author's 1.98 GB at 4253 bodies consistent), gather 7.6 µs/emitter p50 — inside the author's 5.6–10.6 µs band, linear share 53.8%.
   - kick-bench: median 35.9 µs (author 35), p99 79 (86), leavers 92.7 (94); memo quantized hit 89.4% (89), exact 0.0% (0) — matches the 5 October correction.
   - Gates: `behave --law plane` verdict lines byte-identical to the author's `behave-plane.txt` (B13 60/64, B14 timeout 60.1 s, B12 as recorded); `engine-judge` E1–E5, E7, E8 PASS, E6 UNSUPPORTED (missing prepared-mutants.json), E9 fails phase 1 per the author's record. Nothing new fails from the patch; it touches only xtask bench/session.
   - predictions.md (15:26) postdates the baseline (15:25) and predates every decisive sweep (15:27+). D2 held; D1 held in direction, missed in size (predicted engine share 40–80% at rtf 100, measured 24%) — the author reported the miss.

2. **Novelty.** No entry in docs/HISTORY.md (H0001–H0210 range searched) or the docs measures the view pipeline's frame share or a display-quantum freeze rate; `b-readout-cost` sits queued in `lab/queue.txt` unstarted, so this is the first measurement on that ground. Not a rebuild of any H entry; the 5 October memo work it cites is reproduced, not re-claimed.

3. **Goal fit.** It challenges the board's ordering — the frame as flown is bounded by the view, not the engine's kicks — with PRINCIPLES #3 ("Compute only surprises"), #28 ("The view is an instrument"), #33 behind it. The board's #1 (kicks at billion scale) is untouched, and the lens admits it.

4. **Why silver, not gold.**
   - The headline magnitude is the best scene. The author's own `bench-m400-rtf100-surp.json` (in the run folder, not in the dossier) measures **41%** below quantum at 410 bodies at flight pace; my reproduction at the default 71-body scene gives 39–43%. The dossier reports only 75–78% and the rtf-1 15% (that point is also mislabeled "the same scene": it is members 400, not m2000 — at members 48, rtf 1, I measure 41%). The 4× lever estimate is therefore scene-bound; at the small scene it is ~1.7×.
   - The quantum covers three fields, one of which (`angular_radius`) is not on the wire, while `offset`/`light_seconds`/`closing` are serialised every frame and unmeasured. My instrumentation (added on top of the patch, then reverted): at m2000, 99.4% of below-quantum pairs also move less than an angular quantum in offset (headline robust there); at 71 bodies only 65.5% do — whole-wire freeze 27.8% against 42.5% for the author's field set.
   - D1's held-out size prediction failed (disclosed, but a failed prediction keeps it off gold by this lab's precedent, cf. the 1 October law red-team).
   - "Gather + JSON + wire take 49–72%" — that range is gather alone; with JSON and wire the small-scene share is 96% (understates; conclusion unaffected). The dead/live split is decorative: `gather_with` never emits dead bodies, so `compared_dead` is structurally 0 and the "wrecks counted apart" note misdescribes the code.

5. **What survives every attack.** The ordering claim: at no measured scale did the engine out-share the view before its budget saturated; the view is O(presented emitters) per frame with no cadence (verified in `view.rs::gather_with` — the cache memoises only the Newton guess, never the decision to recompute); the engine's saturation threshold is machine-rate-dependent (on my contended box it saturates near 450 bodies, not 1.7k — a rate, not a law, and the author labelled it orders-of-magnitude only).

## The one experiment for gold

Sweep the below-quantum fraction across scene scales (≈70, 400, 1.7k, plus one bright-near-emitter scene) with the quantum defined on the **full wire payload** (offset and light_seconds included), and report the cadence bound as a function of scene. The 41% point at 410 bodies already sits in the folder; reconciling it into the claim (and showing the freeze rate stays high enough across scenes) makes the premise-flip fully evidenced and the 4× honest.

## What the author missed

- The author's own m400/rtf100 measurement (41%) contradicts the headline's generality and is absent from the dossier.
- The wire's map fields (offset) are unmeasured; at small scenes a third of "frozen" emitters still move visibly on the map.
- "At rtf 1 the same scene is 15%" is a members-400 scene, not the m2000 scene; at members 48 the rtf-1 freeze is 41%.
- The engine saturation threshold (≳1.7k bodies) is a machine-rate statement, not a structural one — it saturated near 450 bodies on a 1.6× slower window.
- The dead/live split in the instrumentation cannot fire (gather skips dead bodies; fleet and star ids are counted live unconditionally).
