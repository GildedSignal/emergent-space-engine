Working...
Check complete. `lab/results/20261010-0100-fermi-c11c/check.md` written — **Grade: silver**.

**What I did:**

1. **Reproduced everything** from the dossier's commands in a clean tree (patch.diff is empty; `--kick-bench` is shipped code, commits 1932f6c/dbd4add):
   - kick-bench seeds 1/2/3: 58.1/46.6/45.8 µs (author 63.4/57.8/46.5), memo 0.0/0.0 on all; seed-1 digest and replay_digest **byte-identical**
   - bench rtf 100: digest identical, 71 bodies, 5,074 B/body, 328.9 events/s, fleet 60.6/ship 273 µs per item (author 68.7/300.3)
   - `budget.py` on the author's JSONs regenerates budget-out.txt byte-for-byte; every table row re-derived independently (Kepler 3 AU = 1.64×10⁸ s, cap 2.39×10⁷ bodies, 1,516 ns needed, ratio 41.8×)
2. **Predictions:** mtimes confirm predictions.md (01:05:02) preceded both benches (01:05:21, 01:06:16). P1, P2's quantized half, and P4's belt half failed — all honestly reported, but the gold bar ("held-out predictions held") is not met.
3. **Adversarial:** (a) at 55 s the quantized memo hits **16%** on distinct kicks — the "merges nothing" claim is a 20 s-window artifact; (b) members 400 and seed 7 survive; (c) the 42× headline is purely rtf-100 (0.42 machine at rtf 1 — the averaged billion *fits*); (d) dbd4add's committed M1 costs (25/66 µs) bound the M1 at ~2.5–6× cheaper, so the verdict survives re-measurement but "≥ 40×" shrinks toward ~17×.
4. **Novelty:** exact-memo-dead-on-distinct-kicks is pinned by a committed test (dbd4add), and H0210 already recorded "kicks cost 29 µs". New: the first-breaker ranking, the first H_live price (9.4 bits/game-s vs HANDOFF "not measured yet"), B18b re-priced at 5,077 B/body, and the board's 190-cores correction.

Silver, not gold: real and fully reproduced, but it ranks the bottleneck without moving one, and the load-bearing constants were mostly already on the committed record. The gold experiment is named: attribute the ~60 µs inside the resolver and measure one cycle-compile amortization (N co-orbital bodies sharing one compiled cycle) against the 40× bar.

Nothing else in the run folder was touched; no git commit or push.
