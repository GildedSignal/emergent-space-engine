Working...
Check complete.

**Grade: silver** — written to `lab/results/20261017-2038-components-3570/check.md`, with the author's wiki page corrected in place (the overstated coverage headline and the event-cut scoping).

**What held under reproduction and attack:**
- `regen.sh` exit 0; re-applied `work/patch.diff` myself after the window's other runs had reset the shared tree. Regen: no-op **0.9992** at 2× the author's game-time coverage, all rates identical (news 0.079%, parity 0.97, kick/boundary 1.99×, CPU share 0.29).
- Adversarial outside the tested domain: **N=3×10⁴** coast → 99.96% no-op; the **burn** arm (player wildcard, never flown by the author) → 99.91%. The premise survives every regime flown.
- My decomposition of the news class the author left undecomposed: **269/275 news events are Passage trajectories on ~25 fixed bodies at ms=8** — the near-surface class (ms≤1, 41% of boundaries) produces almost none (7/275). This strengthens the deletion design beyond what the dossier claimed.
- The no-op test is not tautological: `plan_interval_inner` genuinely re-derives the step (`step_for` + hysteresis + aligned grid). Predictions predate the decisive run (20:50:16 < 20:51:24); P2's failed surface half was pre-registered and honestly reported.

**Why not gold:**
1. The dossier's headline "~270,000 game-s ≈ 9.6 intervals" is the nominal flight length; the author's own `run10k.out` reads **90,341.8 game-s ≈ 3.2 intervals** — a 3× coverage overstatement the log contradicts (the lab's explicit grade-losing rule; also copied into the wiki page, now fixed).
2. The deletion is priced, not built: the load-bearing exact key-range conversion is unmeasured — no run shows the kick-time test predicting the 0.12% news class. The named gold experiment: fly the kick-time key-range certificate and take the belt to 1 event/body/interval with gates re-frozen.
3. Minor: absolute µs are probe-inflated (25–32 vs 8ffc's 12.6–13.2), and the pre-registered decisive command (`10 100`) differs from the flown one (`150 1800` — longer/harder, recorded in check.md).

Tree restored to the state I found it (clean except `lab/results/`); no commits, no pushes.
