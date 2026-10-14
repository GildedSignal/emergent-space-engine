Working...
Check complete. **Grade: gold** — written to `lab/results/20261014-2012-dynamics-71b4/check2.md`, with five corrections applied to the author's `wiki/kick-cadence.md`.

**Reproduction (bit-exact).** The runner's `regen.sh` only re-ran `agg.py` on cached npz (all physics commands are `[ -f ]`-guarded), so I recomputed everything from scratch: the six decisive 32-body H=400 runs and both machine-1 held runs regenerate with **identical kick counts and identical error arrays (max rel diff 0.0)**, and the machine is deterministic across reruns. Physics audited: exact CRTBP perturbation and jerk, exact rotating-frame Jacobi oracle, correct Strang splitting on exact Kepler drift, interpolated (not snapped) trigger crossings, non-circular fire-log rebuild.

**Predictions.** `predictions.md` (20:26:58) precedes every decisive npz (≥20:27:12). P1–P5 and P7 held; P6 correctly didn't fire.

**Adversarial (beyond the author's domain).** Held-out seed: trigger loses the frontier 4.0× at matched rate with p90 slope 1.1 (median 0.19 — seed-sensitive). H=800: walk persists. **H=1600: the clock walks too (slope ≈1.05)** — "bounded at every rate" is a ≤400-orbit statement. **Dithered quantum (±20%/fire) still walks (0.63)** — stronger than claimed.

**Defect found.** `agg.py` feeds `np.interp` unsorted rates (name-order glob: K16, K32, K8), so every printed "matched-rate excess" actually divides by the K=8 clock. Honest ratios are larger in every case (23×, ~700×, ≥477× vs printed 13/42/11×) — no verdict flips, but the numbers were mislabeled; corrected on the page.

Gold because: bit-exact reproduction, pre-registered predictions held, closes the wiki's explicitly-named contradiction #3 at zero adoption cost, and survived every adversarial axis I threw at it — the two scope qualifiers (finite bounded-control window, seed-sensitive median) are now folded into the page rather than weakening the kill at the horizons where 524e's claim lived.
