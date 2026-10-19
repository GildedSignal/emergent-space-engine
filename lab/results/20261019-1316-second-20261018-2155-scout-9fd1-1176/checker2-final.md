Working...
**Grade: gold** — written to `check2.md`; blind-second-check note appended to the author's proposed page; tree restored (patch reversed, my example removed).

**What I did and found:**

1. **Reproduction.** Applied `work/patch.diff` on the recorded base (c41a9892, clean tree) and re-ran all four modes: `grid.csv`, `heldout.csv`, `anchors.txt`, `flips.txt` all **bit-identical** to the stored files. The replica claim is real — the instrument's `rots_ticks` is verbatim `arm_pair`'s integer setup (`tier.rs:560–565`) calling the shipped `arm_sections`/`first_hit`/`cone_pairs`/`make_belt`. Controls hold (dv0 zero misses to E≤256, E=1 zero everywhere, no-arm 1.000, dv=0 flips bit-exact).

2. **Predictions.** Pre-registered before the decisive run; P1/P5/P6 held (held-out seed bit-identical), P2 held in its main assertion, P3/P4 failed in letter and are reported as failures with correct readings — honest pre-registration, not post-hoc.

3. **Six adversarial arms, all beyond the flown dial, all confirm the claim:** non-dyadic E {3,5,7,12} (no cadence aliasing — the author tested only powers of two dividing T); κ=2⁻²⁸/2⁻³⁰ (leak still nonzero at every E≥2, 128× below the weakest flown kick); κ=2⁻¹¹ (miss 0.49/0.755 at E=2/4 ≈ 1−1/E exactly); P=64 (saturates at 9.47×10⁻⁵/touch, 10.5× under budget); thin corner (w 38,117, δc0=0.442w, no knee). Every number in the first checker's in-page note that I re-ran reproduces exactly.

4. **Novelty.** Executes verbatim the published page's open direction 1 (9fd1's named experiment) and closes the page's registered knee contradiction; the toys (08d0, 9fd1) were idealizations, this is the tier's own due structure. Moves board item 2: the leak budget never binds (140× margin at every E), so E* is cost-limited — the 355-core row → 3.5×10⁻⁴ cores at E_cell≈10⁶, pending the one named armed-staleness run.

**Caveats recorded in check2.md:** 1−1/E is the full-re-roll envelope, not the quantum behaviour (E=2 belt-real miss is 0.16 vs the envelope's 0.5); the row-level readout is conditional on the unmeasured staleness channel; the two-sections-one-clock ×2 and P-uncertainty caveats are disclosed and my P=64 arm shows the margin survives even at that extreme.
