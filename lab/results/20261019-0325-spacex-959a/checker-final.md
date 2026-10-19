Working...
Check complete. **Grade: gold** — written to `lab/results/20261019-0325-spacex-959a/check.md`.

**What I did:**
- **Reproduced**: applied `work/patch.diff` myself in the clean tree, rebuilt, and verified the runner's regen numbers against the dossier (all within load wobble). Verified the four END digests against **e6c9's own work logs on its results branch** — bit-identical, not just self-reported.
- **Five adversarial arms**, the first outside the author's tested range:
  - **10⁶ × 8 frames** (e6c9's check2 exact command, sums arm): serve p50 **0.130 ms** vs e6c9's 143 ms rebuild form (~1100×) — the flat-in-K law holds at the goal's K and beats the author's ~0.2 ms extrapolation. The 27/786 cells_wrong is e6c9's documented probe id-aliasing, identical in the rebuild form; drift 7.9e-15; steady ops 16–54/frame.
  - **Same-box 3×10⁵ control** (regen flies none): 35.52 ms → **245×**, audits zero, digest identical.
  - **The author's named missing 300-frame control**: wrong cells 59/118 — identical counts and END digest to the sums arm; the long-window class is shared.
  - **Fine-floor control**: 1.74 ms vs sums 1.21 (sums actually 1.4× faster there); the 2/2 residue shared.
  - **Seeds 2/3 + seed-2 control**: flat 0.14/0.17 ms; seed 2's 5/10 wrong cells reproduced identically by the rebuild control.
- **Novelty**: e6c9's wiki entry explicitly named this deletion as the open direction ("deletable to O(cells) by running sums… no new mechanism") — this run built, pre-registered and measured it; new current best, not a repetition.
- **Page corrections** (in place): fine-floor cell range was measured-occupancy 4,759–4,764, not "4,759–6,284" (capacity); added the fine-floor 2-cell residue with the fact that the rebuild control shares it.

**Recorded misses**: "Missed: none" overstates prediction 3 (the author's own fine-floor arm broke its letter); regen flies no 3×10⁵ control despite predictions promising one; the 10⁶ arm was one 248-s flight away; the cancellation corner (hot body) remains unflown — the named next experiment before arguing adoption from these numbers.

Tree restored clean (patch reversed, scratch removed), no commits made.
