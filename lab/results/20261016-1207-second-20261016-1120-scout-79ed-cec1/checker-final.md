Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's wiki page corrected in place.

**What held under attack:**
- Reproduction exact (runner's clean-tree regen matches dossier, report.json, detail.json; all three sha256 hashes match; freeze 12:18 → predictions 12:18 → run 12:47 ordering holds).
- The rule verdict survives everything I threw at it: refit circles 351/351 at ≤2.9e-14 on my denser ±0.999 grid (centre: 163/351, worst 3.8e-1 — the author's grid *understates* the centre failure); m64 passes both failing strong rows (verified: 6.1e-5/2.2e-4 and 5.5e-4/3.2e-4); the 1e-12 repeat bar, light, ISCO, sampler uncontaminated; contamination sweep shows zero hyperbolic-turn selections in any sampler walk.

**What inverted:** the headline "law defect". The walker's hyperbolic-turn branch records `u_new = up + 2√(A·B)` — valid only for A,B>0. For the infalling turn (A,B<0) the true turn is `up − 2√(A·B)`; the b=6 photon turns at u=0.22453 (GR: 0.2247; RK45 agrees) but the walker teleports it to 0.648 → capture. The bisected barriers were the bug's signature: √54 and √18=4.2426 are exactly where the GR turn point crosses u=1/6 into hyperbolic bands. With the one-line fix: capture **0/10 at every m ∈ {8,16,32,64}, both arms**; b̂ → 5.1960 = 3√3 and L̂ → 3.9995, clean second order; H0205's disputed "capture passes" is vindicated. The author's RK45 calibration ran only at u=0.15 (rotation band) — never through the decisive event.

**Net:** the certificate still fails (strongf m16 4/6, m32 5/6; m8 period), but on the true blocker set — no law fix for turning is needed, and the refit adoption question is one fixed re-execution from closed. That experiment is named in `check.md`; the page's capture mechanism paragraph, adoption state, refuted list and open direction 1 are corrected.
