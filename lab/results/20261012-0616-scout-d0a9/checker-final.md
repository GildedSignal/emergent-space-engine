Working...
Check complete. `check.md` written to the run folder; nothing else there touched (all reproduction ran from `/tmp/check-d0a9` copies).

**Grade: silver.**

**Reproduced exactly** — `hlive.py` and `analyze.py` regenerate `results.json`/`curves.json` bit-for-bit (~30 s each); `fermi.py`'s table verified by independent arithmetic. Every quoted evidence number checked: kick rms, payload bits (1.00→4.74), saturation fractions (0.99/0.84/0.23/0.006 at qfac 4/8/16/32), control (1.22×10⁻¹⁵/orbit, zero scars). Predictions were genuinely pre-registered (06:29 vs results 06:37). First measurement of a live HANDOFF risk ("H_live … not measured yet").

**Two adversarial findings block gold:**

1. **The mechanism claim is falsified.** "Scar count grows as the range law ~√k, so the rate decays and the memory self-saturates even with no recompaction" — a 40,000-orbit Gaussian probe (13 s) shows the scar count is *linear*: rate = √(2/π)·σ_s/Q per orbit per body, to three significant figures (0.1994 / 0.0997 / 0.0499 at qfac 4/8/16). The sigma-delta carry is a renewal process — every quantum of total variation crosses a cell; the √k range law counts distinct cells, not crossings. The author's own sweep already sits on 0.8/qfac. So the naive identity under-counts the post-saturation stream, recompaction is load-bearing, and the km-quantum row is fragile. The belt headline survives regardless (qfac ~10⁵ at view-floor: nothing flows in any epoch).

2. **Shipped-artifact bug.** `analyze.py` averages the MC curve over the wrong axis (`mean(axis=0)`, orbits instead of bodies), so the stored `gauss_mc_cum` "curves" are 256 per-body fractions. The saturation table (`mc_end`) is computed on a separate correct line, but the "whole curve within ±0.13" claim is not regenerable from the shipped code (correct bound ±0.17), and the P7 ratios 0.76–0.83× were read off the broken curve (correct: 0.84–0.96×; verdict unchanged).

**Confirmed as right:** first-passage saturation itself — measured k50 (5–6, 15–21) matches the correct MC, and extending the MC to qfac 64 gives k50/qfac² → 0.20, so `t_sat ≈ (Q/σ_s)²` holds in form and constant.

**The one experiment for gold:** fold the total-variation stream law back in, fix the axis bug, restate the km-quantum row — then the design note is adoptable as-is.
