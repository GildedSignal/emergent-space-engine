Working...
Check complete. Summary:

**Grade: silver** — written to `lab/results/20261013-1915-system-81ca/check.md`, with an additive checker block on the author's wiki page.

**What I did:**
- **Reproduced** bit-for-bit: applied `work/patch.diff`, re-ran `regen.sh` — all exactness columns identical to `probe-out.txt` (STRONG n=170 worst 9.20e-10, held-out 3.30e-8 at (8, 0.995), iterations 13–15).
- **Independently re-derived the formula** from the Schwarzschild timelike geodesic cubic: with the key's own fields (`q = 1/r_peri`, `k = 1/(1+e)`), `Δφ_cycle = 4·RF(0,B,A)` exactly — the author's code is correct (its `rf` is 2× Carlson's RF, a notation trap I flag). The walk's separatrix refusal `1−q(4k+2) ≤ 0` is exactly the closed form's `B ≤ 0` domain edge.
- **Three independent oracle paths** (mpmath 50 dps `ellipk`, QUADPACK θ-quadrature, DOP853 on the geodesic ODE, all from the key's exact integer fields) confirm both author arms to ≤1e-15 on a 28-key attack grid beyond the author's domain (e = 0.99999 at p = 50; 1−m = 2.8e-4; p = 1.6e7).
- **Confirmed and extended the negative finding**: the walk is off by 35.4 quanta at (8, 0.995) — and by **62.5 quanta at (7.801, 0.9)**, 35.5 at (7.81, 0.9), 14 at (7.01, 0.5), non-monotonically in 1−m (panel noise). Deep-e keys far from the separatrix hold at 0.4–0.6 quanta while costing 300–375 µs.
- **Found one boundary**: the integer certificate (RF-relative ≈1.1e-15) decides Q30 quanta only while advance ≳ 3.4e-6; the strong branch keeps ~3× margin, the weak branch doesn't (harmless — it's first-order there).

**Why silver:** the 3.3–108× compares one channel against the whole compile; the walk's knots carry t/τ (RD/RJ unported) and the readout is unpriced, so nothing is deletable within one step. The walk-break sharpens 21ba's already-recorded separatrix break rather than killing a standing premise. The gold experiment: port RD/RJ + price the readout, measure the whole compile replacement.

Tree restored pristine (both probe files removed; only `lab/results/` untracked, as at start). No commits or pushes made.
