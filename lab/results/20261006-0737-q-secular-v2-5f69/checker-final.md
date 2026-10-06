Working...
The single-body probe exceeded the window under shared CPU load — it was optional corroboration; the truth's belt is already covered by four other lines (planet-level 1.93e-5, h-convergence, identical verified equations, and the 008e checker's six-body exact probe at 2e-4). check.md stands as written, claiming only what was observed.

**Check complete. `Grade: silver`** — written to `lab/results/20261006-0737-q-secular-v2-5f69/check.md`.

**What I reproduced** (clean scratch tree; `work/patch.diff` is empty — nothing to apply):
- `selector.py` + `laws.py ll` + `analyze.py` → metrics.json identical (admitted 822, frac_rings 0.14453125, leaked 24, every float to 17 digits); `laws.py rings` → **rings_z.npz bit-identical** (`np.array_equal` True).
- Full verification chain number-for-number: drift self-test 1.79e-15; helio(1e-12) vs bary(1e-14) = 2.12e-9 (my regenerated ladder pair); hand-WH 2.63e-5/1.73e-5 monotone in h; `verify.py ce` identical (truth zp vs exact 1.93e-5, LL-new 0.0212 vs old 0.0540); even the author's [C] format crash reproduces.
- Pre-registration honored: predictions.md predates every belt artifact; the decisive prediction (rings 0.40–0.75) failed honestly at 0.1445.

**My attacks hardened the kill:** rate-only 0.346 / evec-only 0.156 — both under the 0.50 bar; and I completed the author's broken `rings_tc` (one transpose fix): **truth-driven rings = 0.253, mid/outer bins 0%** — the first-order averaging, not the LL driver, binds — closing 008e's Touma–Tremaine escape route. My exact belt probe first "disproved" the truth (|Δz̄| ~ 1.2) but the control (truth-conv raw z agreeing to 2e-8) exposed a transcription bug in my own probe — the truth's scene equations verify to 1.93e-5 everywhere testable.

**Why silver, not gold:** the author's decisive held-out prediction failed, and the driver-vs-averaging decomposition was left broken at step 0 in the submitted record — though this check closed it (0.253), so the kill is adoptable now; with that number accepted into the record it is gold-grade.
