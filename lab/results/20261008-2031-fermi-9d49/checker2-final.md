Working...
Check complete. **Grade: gold** — written to `lab/results/20261008-2031-fermi-9d49/check2.md`; nothing else in the run folder or repo touched.

**What I verified (blind, 30 min):**

1. **Reproduction, bit-exact.** Clean tree, empty patch, all measured code is the committed `crates/shipmem` (78f87d7). All six `measure` runs: identical bits, floors, before/after **and identical checksums** to the author's `measure.jsonl`; `roundtrip_mismatches: 0`, update oracle true, ≤ 2.6 s, 118 MB peak. `fermi_hlive.py` regenerates `fermi_hlive.out` with `diff` clean. I re-derived the analytic constants by hand (b_cross = 16.0 m, Ceres 26.5/day, 8.2×10¹⁷ kg/Myr, 34.36 bits/body, ceilings 9.5/12.9/24.2%) — all correct, units check out.
2. **Predictions.** Pre-registered (mtimes 20:36 → 20:37 → 20:42); 6 of 10 held; two misses disclosed, one of which (P6, wrong by ~9 orders) self-falsified into the run's headline: contacts, not gravity, promote in 2D belts.
3. **Adversarial attacks — all survived, one closed the author's admitted gap:** re-kick boundedness (his P4, unrunnable via CLI for him) I forced with 2M/4M updates: bits per distinct kicked member *falls* (70.7 → 58.2 → 45.4), total Δ sublinear; traders under 2M kicks: **exactly 0 new bits**; widths n-stable at 10⁵.
4. **Novelty:** HANDOFF:70 said H_live "not measured yet"; no prior entry measures this; kills representation.md:90's 12–16 B individual floor (measured 18.7–24.6 B at 1.04× true entropy floor).

**Found that the author missed** (recorded, none flip a verdict): "b_cross < contact radius at every rock size" is false above R ≈ 11 km (gravity promotes first there); a 5.2-vs-6.64 GiB presentation inconsistency; the 12.9% ceiling is rest-state-sensitive (≈4% if the rest is formation-grade).
