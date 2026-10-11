Working...
Check complete. **Grade: silver** — written to `lab/results/20261011-0006-dynamics-a2a5/check.md`; nothing else in the run folder touched (only `__pycache__` bytecode refreshed by import).

**Reproduction — exact.** Warm rerun of the author's command (88 s) and a cold regeneration from seed in a fresh tree (4m58 s) are both **bit-identical** to `metrics.json` — all 21 rows, `se_null`, flips, ships. The EXP statistic is a faithful port of `xtask/src/behave/fit.rs::growth_exponent` (verified line by line). `work/patch.diff` is empty; the work is self-contained. File times confirm `predictions.md` (00:12) preceded the decisive artifacts (00:29–00:35).

**What held.** VR+trend passes every positive plant and fails every negative (7.0σ separation); the leak sweep proves VR exactly drift-blind (0.0049 across all ten leak rates); P2/P3/P6/P7 held; P1/P4/P5 failed and are honestly reported with mechanisms. Novelty clean: the killed predecessor (recurrence ratio) is in `handoff.rs`; variance-ratio/HAC is new. Directly targets HANDOFF's named instrument risk.

**Why not gold.**
- P1 failed outright; and the demo is on the author's scene, not the gate's frozen 16-ship harness (the dossier says so itself).
- My strongest attack: a genuine walk at 1–2.6× the bounded amplitude leaves VR **INDETERMINATE** at the registered τ*=200 — the FAIL rests on trend t = 3.7–4.1 against a threshold of 3, a test the author himself shows is inflated by the folded |·| series. The "no amplitude floor" claim overstates; the real advantage is calibration.
- Two more attacks found boundaries: a genuinely bounded AR(1) with decorrelation ≈ T/3 falsely fails (dossier implied 10⁴ periods), and a leak that reverses at mid-horizon (growing to 20× the background) passes both statistics — undisclosed.

The named gold experiment: repeat on `handoff.rs`'s frozen harness with τ* pre-registered from event cadence, trend on the signed error, and these adversarial families as controls.
