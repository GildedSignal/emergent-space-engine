Grade: silver

**Abstract.** Claim: on the shipped plane the frame is view-bound, not engine-bound — the view pipeline is 67–82% of the median frame at rtf 100, and the gather touches every body every frame (~4.2 µs per bare tube, ~11.7 µs per bound body, 1.3–10.2 µs per fleet member), saturating a 16.7 ms frame at ~2–4×10³ bodies. Reproduced on a clean tree: identical bench digest; view_gather 70.1% vs 68.9% (p50 3.44 vs 3.42 ms); the probe within 1% everywhere (per member 5.93/7.85/10.20 vs 5.90/7.87/10.12 µs; 163 vs 162 ms at 16,000 members); kick-bench memo rates exact (0% / 94.49%). Gain at the goal is possible-vs-impossible, not 10×. Cost: the diagnosis is free; the fix is one module, already promised (plane.md foundation 7, PRINCIPLES #5).

## Reasons

**Reproduction (clean tree, `work/patch.diff` applied, release, same box class).**
- `universe --bench --seconds 30 --rtf 100`: digest identical (`41343a143a92f956…`); frame p50 4.216 vs 4.166 ms; view_gather share 70.1% vs 68.9% (p50 3.444 vs 3.421); engine p99 5.02 vs 5.13 ms (both over the 5 ms budget). Overflow frames 18 vs 39 — machine state, as the dossier's own machine_before/after records anticipate.
- `constraint_probe 100`: per-emitter floor 4.955/4.169/4.159 µs flat in n (stored 4.275/4.061/4.215), 1.03 readouts per emitter, n=4800 refused identically; plane_late 11.776 vs 11.713 µs per live body, fixed player readout 12.0 µs; members sweep 5.933/7.854/10.203 vs 5.900/7.870/10.118 µs per member, gather 163.2 vs 161.9 ms at 16,000 members.
- `universe --kick-bench --rtf 100 --seconds 20`: 949 kicks, exact memo 0.0, quantized 0.9449 — bit-for-bit the stored rates; kick µs medians higher under my residual load (113 vs 76 µs), same order.
- `universe --bench --seconds 10 --rtf 100 --members 480`: view_gather 53.6% vs 54.0%, engine p99 6.05 vs 5.66 ms, rtf lowest 1% = 0.0 in both; `--members 4800` provably clamps to the same 410-body run (stored m480 and m4800 JSONs are identical in bodies and stats) — the instrument-gap claim is verified in the data and at `xtask/src/universe/mod.rs:32`.
- Code confirms the mechanism: `view.rs:300–332` enumerates every alive body with a `state_rate` Newton readout, `view.rs:336–368` walks every fleet member (`f.motions` collected per frame), no culling and no angular floor; `session.rs` ("Shared by the page and the benchmark") does gather + JSON + wire every frame, so the bench scope is the page's loop.

**Predictions.** `predictions.md` (03:32) predates the probe outputs (03:42); the bench JSONs were copied in one event (03:41:49) so their creation order is not in the record, but the baseline section cites only pre-prediction runs, and P1 (linearity) and P4 (≥10×) failed in the specific ways an honest prediction does — a tuned author would have written the superlinear cache walk and the 2.8× premium they measured. P2, P3, P5 held; P4, the held-out magnitude, missed (2.8×, direction held) and was reported as missed.

**Adversarial cases.**
1. *400 members at rtf 1* (not run by the author; the speed the player actually flies): view_gather p50 0.810 ms vs engine p50 0.083 ms — the view is ~10× the engine and the largest computed term at real time too; P3 holds at the extreme, and the claim does not depend on the 100× stress mode.
2. *The readout decomposition*: my `readout_only` re-run gives 4.395 µs per call (stored 4.186) against a 4.16–4.96 µs per-emitter total — the readout is ~100% of the floor, so the "~89%" share is if anything understated; but the "3.7 µs" call cost and the "~0.5 µs" Seen construction are not in the saved record.
3. *The gates claim*: verified against the code rather than re-run (99 s). "No gate measures the view against N" is true — law.md's B-table has nothing view-vs-N and the plane's behave stops at B14 — but the supporting sentence is wrong (below).

**Novelty.** H0210's limitations already recorded "the view gather is 83% of a light frame", the gather cache landed (H0211, H0213: 1.2 readouts per emitter at 0.9c), and law.md's open rung list has r6 (view). What was not known and is now measured: the per-emitter floor and its readout dominance, the 2.8× bound-body premium, the fleet-loop scaling to 16,000 members with a superlinear per-member cost (1.3 → 10.2 µs), the saturation point against the goal (2–4×10³ vs 10⁹), and both instrument gaps (the 400-member clamp; no view-vs-N gate). Prior art is a share, not a scaling law; this is a fair delta, not a re-derivation.

**Why silver, not gold.**
- The held-out magnitude P4 missed (2.8× vs ≥10×); by the lab's own precedent (the 1 October red-team was denied gold for one failed held-out prediction) that alone caps the grade.
- Nothing is moved or deleted yet. The fix (an event-driven gather) was already promised by the design — plane.md foundation 7 even names the gather: "Nothing takes an unbounded synchronous claim on the frame, whether a cycle compile, a rebinding burst, a decompression **or a gather**" — so the run quantifies a live violation of a frozen principle rather than showing a premise wrong; the author concedes in the lens section that the frame-level ranking does not refute the engine-side questions at 10⁹.
- Two load-bearing sentences carry errors: "B15 judges readouts per emitter on 24 emitters" (that is the view unit test, `crates/universe/tests/view.rs` — ~24 bodies, warm ≤ 1.3 readouts per body; gate B15 is "gravity is nearly free", law.md); and "the gather is the only O(N)-per-frame term" (view_json and wire are also O(N) in seen entries — the whole pipeline is, and the dossier reports the pipeline total anyway). Also the fix is cited to "plane.md foundation 6"; it is foundation 7 that names the gather, and 10⁹/(2–4×10³) is 5.4–5.6 orders, not six.

## The one experiment that would make it gold

Build the event-driven slice of the gather on the dominant term — the fleet loop — behind display quanta (direction, colour, brightness, angular radius) with the crossing memo predicting each member's next visible change, and rerun this probe's 400/4,000/16,000-member sweep: per-frame view cost must stop tracking N (at 16,000 members the gather is 163 ms; the quanta path needs ~10²×) with the view still within one display quantum of the exact gather, judged by a frozen view-vs-N gate seeded from these numbers. That deletes the per-body readout at 60 Hz, closes both instrument gaps, and moves the frame's remaining constraint to the engine's p99 burst, which the allocator already owns.

## What the author missed

- The rtf-1 counterfactual (adversarial case 1) was one 10-second run away and strengthens the claim: the view dominates at the speed the player flies, not only at 100×.
- The readout decomposition's absolute numbers (3.7 µs, 0.5 µs) are unsaved and unreproducible; only the share is.
- The design citations are off by one (foundation 7, not 6) and the "B15" label points at a unit test, not a gate.
- JSON and wire scale with seen too; at 16,000 members they would add roughly the gather's cost again (~5.5 µs per body measured at 76), so the pipeline's true break is earlier than the gather-only numbers suggest — the claim is conservative, but the ceiling is understated.
- The n=4800 bare-tube refusal (`Space(NoBoundOrbit)`) caps the "flat floor" claim at 2,400 emitters; the stream scenario cannot express the 9,600 the predictions promised, which itself is a third instrument gap worth naming.
