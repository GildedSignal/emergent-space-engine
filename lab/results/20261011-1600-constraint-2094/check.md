Grade: silver

**Abstract.** Claim: on the plane as flown the frame's constraint is the view gather (linear 15.4 µs/emitter, 65–70% of every frame), not the engine (protected by its 5 ms budget); the next representation to change is the view's. Reproduced exactly: `gather_scaling` 15.45 vs 15.41 µs/emitter at 100k emitters, 1.98 readouts both; bench gather share 69.5% both. Adversarial: the "scene saturates at 428 bodies" finding is false — xtask clamps `--members` at 400 (m480/m4800 have identical digests); with the clamp raised the scene reaches 3744 bodies in 10 s, gather still 60.7% of a collapsed frame, player item 24.5 ms > the engine's whole budget. Gain: names where the next 10× lives (doll-level gather). Cost: a view-layer redesign awaiting Julien's perception floor.

## Reasons

**1. Reproduction (clean tree, patch applied).**
- `gather_scaling`: my run vs the author's, µs/emitter at 100/1k/10k/50k/100k emitters: 14.96/15.02/15.45/15.45/15.45 vs 14.93/15.03/15.41/15.40/15.40; readouts 1.98 both; dead linear over three decades. Peak RSS 620 MB. The headline law is real.
- Baseline bench (`universe --bench --rtf 100 --seconds 30`): gather p50 3.45 ms / share 69.5% (author 3.46 / 69.5%), engine 0.239 ms / 17.6% (author 0.243 / 17.4%), json 9.1%, wire 3.8%. No hitches above 16.7 ms. Matches.
- Gate artifact claim verified: the plane law answers only B12–B14 (xtask/src/behave/plane.rs); G1–G6 PASS under `--law space` (work/behave-space-g.txt); B12 FAIL and B13 60/64 match HANDOFF's known state; B14 at 60.1 s is marginal on this box. No new breakage.
- Arithmetic checked: 15.4 µs × 10⁹ = 4.3 h/frame; (16.7 − 5 − 1)/15.4 µs ≈ 650 emitters.

**2. Predictions.** Written 16:05, before every held-out run (m480 16:06, m4800 16:07, scaling 16:15; the 16:03 baseline is disclosed as tuning). Kill criterion did not trigger. Predictions 1, 3, 4, 5 held; the held-misses are honestly reported — but see below: prediction 2 was reported as a miss only because the clamp hid the real 4800-member scene from the author.

**3. One finding is wrong, and it is load-bearing for the sweep.** The dossier: "the scene saturates at 428 bodies … the battle's collision frontier, not the member count, sets the hand-out rate … a finding for future N-work." Truth: `--members` is clamped to `clamp(4, 400)` (xtask/src/universe/mod.rs:32, since the plane's first flight, 080ff709). m480 and m4800 are the same configuration run twice — identical digests (`3db02d3d…ca2ce` both), identical encounters (229), the author's own digest_note states the test. The "collision frontier" mechanism was invented for a CLI clamp. I raised the clamp (one line) and ran `--members 4800 --seconds 10`: **3744 bodies and climbing, gather share 60.7%, frame p50 51 ms, hitches 67 497/hour, player item 24.5 ms — prediction 2 (player item exceeds the engine's whole 5 ms budget at ~4800) held after all.** The core claim survives this intact — the gather owns the frame at 3744 bodies even harder — but a gold dossier cannot carry a fabricated mechanism presented as a finding, nor a held-out sweep that was secretly one configuration.

**4. Novelty.** The gather's dominance is known: H0210's limitations already say "the view gather is 83% of a light frame", H0211 built the cache, H0213 measured 1.2 readouts/emitter at 0.9c in the plane — which also contradicts this run's "1.98 readouts/emitter is the floor" (the plane itself measured lower; the floor claim is overstated, though the author's own "micro-optimising buys ≤ 5×" bound absorbs it). New and real: the isolated linear per-emitter law over three decades, the ~650-emitter ceiling, the 4.3 h/frame extrapolation to 10⁹, and the frame-collapse mode (engine defers, the frame tracks the gather's max). The board's order ("kicks dominate the engine's cost") is confirmed inside the engine; the run correctly shows the frame is the gather's — but that correction was half-recorded already.

**5. Goal fit.** Real: smoothness is principle 12 ("i care about the p95/99 results i want the game to be smooth"), the gather's per-body cost violates principle 3's economy at scale ("Nothing is evolved that can be derived when looked at (clocks, redshift, views)"), and the doll-level gather direction is OC#30's own letter ("the zoom level is the minimap"). But it diagnoses and proposes; nothing is adopted (the interim — budgeting the gather — is named, not built or measured). It moves no bottleneck 10× by itself.

## The one experiment for gold

Raise the clamp (`clamp(4, 400)` → e.g. 40 000, one line), rerun the sweep at true 480–4800 members, and fold in what it shows — my 10-second version already has the numbers: the frame collapses with the gather still at ~60%, the player item past the whole engine budget, the engine still deferring. Add the corrected "saturation" finding (a CLI clamp, not scene dynamics) and the re-derived readout floor against H0213's 1.2. Every physics claim in the dossier survives that experiment; with it run and reported, this is gold.

## What the author missed

- The `--members` clamp: the identical digests sat in the author's own JSONs with a note explaining exactly what identical digests mean. Two "held-out" runs were one run; the "finding" was an input clamp; a false mechanism ("collision frontier") was printed for it.
- Prediction 2 was reported as a held-miss when it actually held at the true N — the clamp cost the author their own strongest confirmation.
- H0213's 1.2 readouts/emitter against "1.98 is the floor" — the floor claim needed a search of HISTORY before being made.
- The plane's own per-emitter arithmetic: 3.46 ms / 76 bodies = 45 µs per emitter at the first flight vs 15.4 µs marginal — a ~2 ms fixed cost (or costlier plane emitters) the 650-emitter ceiling ignores; unexamined.
- The gather probe measures one geometry (stream, β 0.9, Across); doll-chain depth dependence of the readout was never varied.
