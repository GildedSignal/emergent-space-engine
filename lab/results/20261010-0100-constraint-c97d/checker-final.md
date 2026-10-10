Working...
Check written: `lab/results/20261010-0100-constraint-c97d/check.md` — **Grade: silver**.

**Reproduction (clean tree, patch applied by me, isolated target dir):**
- Stock benches within 1–5% of every quoted number: l0 p50 0.631 ms / engine 4.65% / gather 72.8%; m4 gather 83.3% (450 µs) — H0210's "83%" to the digit; m400 json 808 µs = 48.9%; kickbench 45–48 µs, leavers 369 µs, memo hit 0.0.
- Instrumented counts match **exactly** (seen 32/76/428, reads ≈45, bodies 28–29, seeds 2 and 7 included — deterministic).
- Galaxy 10⁹: identical 1,088,345 key requests and memo hit 0.987170; RSS 104.8 vs 104.5 MB; render 28.5–40.4 ms across three views vs author's 32.0 — all 200 frames over budget.
- Gates: B13 60/64, B12, B14 60.1 s reproduce (B11 also fails — oracle-domain, unreported by the author, minor).
- `predictions.md` (01:04:11) verified to precede every decisive run (01:04:25 onward); 3 of 5 predictions failed and were reported honestly.

**My adversarial cases:** seed 5 at M=400 (same shares); `--rtf 4` — universe bodies 29→226, gather 3.56 ms = **15.8 µs per body per frame, the claimed linear rate confirmed at an octave more bodies**, engine share still 7.9%; galaxy under concurrent load.

**Why silver, not gold:** the headline constraint is recorded — H0210's limitation "the view gather is 83% of a light frame", H0211/H0213's gather cache (today's 1.55 reads/body is already post-cache), H0214's "the plane's readout" as next work — none cited by the dossier. Genuinely new: the bodies-vs-members decomposition, the per-entry JSON cost, the ~1,200-body and ~9,000-entry caps, the galaxy 10⁹ numbers. Gold experiment: lift the `--members 400` clamp and measure the view at 10³–10⁵ entries (the 190 ms formation projection is an extrapolation with a superlinear hint), plus one analytic-crossing prototype proving the promised ≥10×.

Tree restored to pristine; only `check.md` added; no commits or pushes.
