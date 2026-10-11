Working...
Check complete. `check.md` written to the run folder — the only file I changed there.

**Grade: silver.**

**What reproduced (everything):** In a clean tree after verifying the only script edits were `OUT` made file-relative plus the new `quadj` stage (patch.diff is empty): selftest passes; quad.json and calib.json **bit-identical** to the original run's shipped files; all four re-run scans (j1 μ=1e-3, j2 μ=3e-4, both j3) **array-identical** (only `wall_s` differs); `final.py` regenerates final.json with exactly the two declared diffs (the W.j2 slip 0.0229→0.0305 — which I verified is the 2:1 conversion factor 0.75 applied to the 3:2 case — and the 0.52→0.53 rounding); `gate.py` regenerates gate.json **identically**, and every dossier table number matches. predictions.md mtimes precede all 4:3 data and gate.json. The record gap from the 5 October lesson is genuinely closed.

**Predictions:** PA failed as written and was disclosed prominently; PB, PC, PE held exactly; no kill criterion triggered.

**My adversarial cases (5):** chief findings —
1. **The 5:4 location is wrong**: δ = +0.0440 by the dossier's own formula, **outside** the ±0.032 grid, not "+0.027 inside". The proposed zero-cost domain test's j=3 entry is mis-computed, and with correct arithmetic its "false for 4:3" verdict survives only by an unstated ~7% margin. The mechanism (5:4 wing pumping the grid edge) survives qualitatively.
2. **The 4:3 refutation is above-cap**: all 12 guard misses sit at q > cap; at quanta ≤ cap the guard is clean on **all seven cases including 4:3** — so the declared j ∈ {1,2} restriction protects against the wrong axis (the real one is q vs cap; j2 μ=1e-3's own design quantum already exceeds its cap).
3. **Fresh-seed attack passed** (seeds shifted 0.3 at j2 μ=1e-3): 1,417 failure events, guard misses still 0.
4. Regime-miss disclosure understates 4× (47–63 librating systems per case, not 10–15, though confined to above-cap quanta).
5. The cost table's "cert 0.87–1.00" quotes the switch form, which is **empty (0.00)** at j2 μ=1e-3's design quantum — ironically the strongest argument for the guard form.

**Why silver, not gold:** the adoption instrument (the domain test) has wrong arithmetic and an unstated margin, and the named gold experiment — wiring into the plane's kick layer — remains undone (impossible in the lab; the stand-in's handler is the reference integrator, so interior behaviours are 1.0 by construction). The measured result stands: guard-form certificate, 0 vs 542–1,120 misses on 2:1/3:2, deletion free; one experiment from gold, named in the check.
