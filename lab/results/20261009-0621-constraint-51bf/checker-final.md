Working...
Check complete and written to `lab/results/20261009-0621-constraint-51bf/check.md`. **Grade: silver.**

**Reproduced** (patch applied on a clean tree, release build):
- Universe digest `6ce636fa…` bit-identical across pre-edit binary, instrumented binary, and raw-crossing mode — the instrumentation is observation-only, confirmed by rebuilding without the patch.
- Gather share 0.653 paced / 0.674 unpaced (author 0.668/0.675); engine 0.22/0.20. My p50 frame was 1.3 ms vs the author's 4.6 ms under lighter load — shares identical, which itself confirms the dossier's "shares are the robust statistic".
- Split: bodies 0.950–0.951, observer 3.2%, fleets 1.8%, field share of readouts 0.813–0.815; unpaced view digest matches the author's base bit for bit.
- Kick-bench identical (0% exact memo, 926 fresh shapes, 94.49% quantized); raw-crossing exploit loses as reported (field 234→58 ms, bodies loop +50%).
- Predictions pre-registered before the instrumented runs (file-time order); all four bounds held.
- Three adversarial cases of mine — rtf 1 (gather 0.72/engine 0.04), rtf 1000 (0.64/0.29), seed 7 (0.62/0.26) — no inversion; anatomy stable.

**Why not gold:** the headline is on the record already — H0210's limitations say "the view gather is 83% of a light frame", H0211/H0213 built the gather cache, and plane.md foundation 7 already names a gather among unbounded frame claims; the dossier cites none of it. What is new and real: the post-cache level, the anatomy (81% in per-emitter-per-Newton-step field re-reads), the coupling lesson from the failed exploit, and the per-body N-scaling term. No lever is built or measured — the ~3× gain is projected. One experiment to gold: build the shared-field-per-doll lever and re-measure the frame split with the digest unchanged.

**Author also missed:** the per-frame view digest is not canonical (wall load leaks in via engine-budget overflow — my raw digest differs from theirs while base matched), and only one rtf/seed was measured. Tree left with the patch applied for `run.sh` to restore; nothing committed or pushed.
