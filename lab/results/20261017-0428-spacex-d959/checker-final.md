Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's `wiki/read-stream.md` corrected in place where it overstated.

**What I did:**
- **Reproduced everything from a clean tree**: applied `work/patch.diff` myself (the runner had restored the tree post-regen); all regen numbers match to the digit; digest identity confirmed on all 13 `ladder_digest` cases (regen's timeout reached only 10; I re-ran the wave N=3000 and both belt-crossing cases on patched and pristine builds — identical digests).
- **Held-out adversarial case**: readwave at N=30,000 (between the author's points) lands exactly on the linear law — `ctx.rs:89` = 135,245 = 45,161 + 3×30,028, every other site exact, scan flat at 160,663.
- **Closed the author's P2 gap**: they promised burn-flight N-scaling but answered from the settle. I ran burn/coast at 10⁴ vs 10⁵: flight totals are bit-identical across N, and the scan is N-flat even in the burn flight (99,113 at both N) — the headline survives its strongest test, and that's now on the page.
- **Corrections**: the per-event arithmetic was ~6% low (true law is exactly 3.0 + 1.0 + 1.0 = 5.0 readouts/event — the 3.0 *is* the 3 planets; the author divided Δcount by N instead of Δbodies); `observe.rs:190` is the scheduler's `root_state_raw` read, not the ramp; "13/13 md5 equal" overstated the stored 5-case artifacts; "knee re-derived" softened to same-order-not-cross-run; the view-gather "3 source-reads per emitter" undercounts ~3× (measured ~8.5).

**Why silver, not gold**: the pre-registered P1/P2 failed honestly (that failure is the result, but gold's letter requires held-out predictions to hold — the 1 October precedent), and the knee's actual regime (the 20k-gs steady burn where `b = 11.48` was measured) is uncensused. The one experiment to gold: census the steady-burn stream, then build the per-drain shared source readout and measure the cut on the flown path.
