Check complCheck complete. **Grade: silver** — written to `lab/results/20261018-0035-redteam-22d1/check.md`, page corrected in place, `checker-final.md` closed out.

**What reproduced (independent from-scratch implementation):**
- All 27 Jaccards digit-for-digit (static controls 1667/319 vs e59e included).
- W1/W3 onset columns to 4 decimals; re-derived their correction term R(√(1+β²)−1)/β analytically — that machinery is exact.
- Arm B by hand: exact Shapiro 8.5084 vs quadrature 1.79%; limb differential 0.782 s = 4M·ln((b−R_p)/(b+R_p)) — robust because r_E, r_O cancel.
- Price 81 ns/row this box (dossier 69–79; order of magnitude).

**What fell (the decisive adversarial case, outside the instrument's valid domain):** the W2/W2p **onset** columns — including the headline "+125 s, unbounded in d" — are artifacts. `min_dist_vs_t`'s retarded-time quadratic substitutes the occluder's *current* distance for the worldline's perpendicular offset, making it exact only at t_O = 0 (where the correct Jaccards sit). Bisection proof: at t_O = 98, d = 100, β = 0.9, the author's form gives t_ret = −40.148 vs true −2.016. True sprite onset errors: **+0.24…+0.62 s, bounded in d**. The tell was in their own log: W2 and W2p "different wirings" reporting +125.1344 and +125.1206 — convergent wrong numbers mean shared broken instrument.

**What the correction strengthens:** W2's genuine parity break is geometric and d-independent — the sprite sits at retarded distance γd, its arc is the true arc shrunk by exactly 1/γ (0.866/0.436, matching measured 0.865–0.875/0.436–0.452), centres aligned since atan(βγ) = asin β. P2's bounded form was right; P3's refutation stands. The snapshot kill and the worldtube-is-the-law conclusion survive on exact evidence.

**One experiment to gold:** fix the two wirings, rerun, restate the W2 leg (bounded O(R/β) timing + 1/γ arc deficit), re-freeze the rung's sprite-negative at the corrected rates.
