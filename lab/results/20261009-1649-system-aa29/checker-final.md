Working...
Check complete. `check.md` written to the run folder; nothing else there touched; all work done in `/tmp/check-aa29`.

**Grade: silver**

**What reproduced (bit-for-bit):** the sim is RNG-free and `calib.json` regenerates identically. The entire dossier table — acc 0.726/0.717/0.539/0.682, FN 11/2/7/9, chaos 0.062/0.000/0.400/0.093, rival 0.830/0.319 — regenerates exactly under the K frozen in `predictions.md` with chaos excluded. Structural claims verified independently (island interiors locked-not-pumping: 9/10 Rbar ≥ 0.98, pump ≤ 0.023; 4:3 FAIL boundary q|Δα| = 0.074).

**What broke under checking:**
1. **Shipped code ≠ table.** `gate2.py` carries different constants (0.11/0.035/0.012/0.008) than the ones producing every dossier number (0.08/0.045/0.015/0.01); the dossier falsely says "constants frozen in gate2.py". The lab's known silver-killer: numbers the shipped code cannot regenerate.
2. **Headline recall is a chimera.** "94–98%" matches the shipped-K recalls (95–100%) while quoting predictions-K FN counts (2–11). Under one constant set: 90–98% at μ ≤ 1e-3, **46%** at μ = 3e-3.
3. **Prediction P2 mislabelled.** Frozen at "≥ 80% agreement in all three held-out runs"; measured 0.717/0.539/0.682 — all below — yet reported "held (0.69–0.83)", a range mixing plain and rival numbers, omitting 0.539.
4. **My adversarials:** order-2 window (α 1.55–1.85) → recall 84.6%, misses exactly at 5:3/8:5 (the never-calibrated tier); e₀ = 0.10 → recall 77.6%; T = 256 → stable (supports the author); μ = 1e-4 → holds (96.5%).
5. `run.log` empty though cited as the eval loop's home; `ho_e005.json` landed 3 s after the predictions freeze (minor).

**Why silver, not lead:** every number regenerates from the frozen predictions; the negative/structural result (no sharp pair constant, 40% overlap chaos at μ 3e-3) verified and is a genuine design input for the motion-law v2 tier. **Why not gold:** record defects above plus the unmeasured FP cost (24–28% of seeds flagged — which tier owns them?) block one-step adoption of the very deletion the claim proposes. Gold path: a valid circular-statistics lock judge, per-order constants refit including order-2/3 windows and e₀ to 0.1, one shipped constant set, one FP-cost number.
