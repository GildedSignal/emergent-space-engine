checker2 doCheck complete. `check2.md` written; tree restored clean (author patch and my instrumentation reverted; only `lab/results/.../check2.md` and `checker2-final.md` touched).

**Grade: silver.**

**Reproduced from the patch in a clean tree** (box ~1.6× busier; shares carry): view-gather 45–68% of frame at every scale; surprise at m2000 seeds 1–3 = **75.4 / 79.6 / 78.2 %** (author 75.0/78.2/78.3); engine 5 ms budget saturated at ≳1.7k bodies; kick-bench 35.9 µs median, quantized memo 89.4%/exact 0%; m8000 linear at 7.6 µs/emitter, RSS 1.51 GB under the cap; `behave --law plane` verdict lines byte-identical to the author's record; engine-judge E1–E5/E7/E8 pass, E6 unsupported, E9 fails phase 1 as designed. predictions.md timing verified (after baseline, before sweeps); D2 held, D1 held in direction only (author disclosed the size miss).

**Why not gold:**
- The 75–78% headline is the best scene. The author's own unreported `bench-m400-rtf100-surp.json` measures **41%** at 410 bodies at flight pace; my runs: 39–43% at the default 71-body scene, 51% at 451 bodies. The "same scene is 15%" rtf-1 point is actually members-400, not m2000 (members 48 gives 41% at rtf 1).
- The quantum covers 3 fields, one (`angular_radius`) not even on the wire, while `offset`/`light_seconds`/`closing` are serialised unmeasured. My added instrumentation: at m2002 99.4% of below-quantum pairs also freeze in offset (robust there); at 71 bodies only 65.5% — whole-wire freeze 27.8% vs the claimed-field 42.5%.
- D1's held-out size prediction failed (disclosed, but a failed prediction blocks gold by this lab's precedent).

**What survives every attack:** the ordering claim — the view, not the engine, binds the presented frame at flight pace at all measured scales; gather is O(presented emitters) with no cadence (the cache memoises only the Newton guess); plus a machine-rate caveat on the 1.7k saturation threshold (it saturated near 450 bodies on my slower window).

**Gold experiment:** sweep the below-quantum fraction on the full wire payload across scene scales (70/400/1.7k + one bright-near scene), reconciling the 41% point already in the folder.
