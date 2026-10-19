Working...
Check complete. **Grade: silver** — written to `check.md`, with one in-place correction to the author's wiki page.

**What I did:**
- **Reproduced** from `work/patch.diff` on the clean tree: `law 4 -23` and the E_ARM=2 census are **bit-identical** to the author's outputs; my strict one-constant refit reproduces every quoted number (r = 0.569/0.285/0.878/0.000; max errors 0.014/0.003/0.088 as disclosed). Anchors and the 8×-vs-512× label correction verified (δc0 ratios 8.02, 510).
- **Adversarial, all outside the author's tested ranges:** κ=2⁻²⁰ → r=0.114, predicts E≥16 within **0.004**; P=8 → r=0.397, within **0.006**; fresh seed 31337 → census mechanism holds (far-misses 0, S₁ 0.512, per-j catches 4 vs 2.2 expected under the geometric). The law genuinely generalizes.
- **Found:** the P=1 arm misses by 0.079 (same order as the disclosed weak-arm 0.088, but undisclosed) — corrected the page in place; the "fit prefers two components on the weak arm" line is contradicted by the author's own table (r₁≈r₂, degenerate); a live refresh-catch channel on fresh seeds; P1's geometric-vs-erf discrimination was swapped for a curve fit (disclosed).
- **Not gold:** reproduced and predictive, but by the lab's own bar it converts a measured-only freeze constant into a law — no 10×, no deletion, no board premise killed — and the one class the freeze actually needs (thin-window, w≈23) is untested. That measurement is the named experiment to gold.

Tree restored to clean (`?? lab/results/` only); nothing committed or pushed.
