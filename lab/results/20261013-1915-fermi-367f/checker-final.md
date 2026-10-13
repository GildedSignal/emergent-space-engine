Working...
**Grade: silver** — written to `lab/results/20261013-1915-fermi-367f/check.md`, with the author's wiki page corrected in place.

**What reproduced:** everything deterministic — regen (post-fix) regenerates 8,257 B marginal, 3,003×/145× exchange rates, the 400–1,500 collapse window at rtf 100 (both seeds), the leak 1.9e-2→6.8e-2 per member/game-s, hand-outs ~0.5 ms flat in N. `predictions.md` genuinely predates the ladder; 4/6 held, misses disclosed.

**Adversarial (3 cases, 2 outside the author's range):**
- **8,000 members / rtf 1** (next decade): 240/240 overflow — collapsed; hand-out still flat at 507 µs; marginal bytes *rise* to ~11 kB; but the leak exponent softens to ≈N^0.7, so "N^1.4" doesn't extrapolate and "empties in game-milliseconds" is off by ~2–3 orders (it's game-seconds).
- **800 / rtf 100** (midpoint): fully collapsed (median 9.8); the 400 rung itself medians 77 in regen — the window holds, its lower edge is box-marginal.
- **seed 7**: leak and hand-out consistent.

**Why not gold — one refuted headline:** "the fleet's own advance ∝ N^1.9, quadratic, independent of the live side" is an accounting artifact. `universe.rs:667–670` charges hand-outs *inside* the `fleet` kind ("a hand-out was inside its item"); the run's own prof counters split the 4,311 µs/item at 4,000 as 88% hand-outs vs ~510 µs advance. The advance alone runs 10→104→131→317→466 µs/frame (48→8,000) ≈ **N^0.6–0.8** — walk-tier class. The dossier double-counts the same promotions (once as "flat in N", once inside the N^1.9 column). The break-order conclusion survives re-attributed: the **leak×sticky-promotion stream alone** is the plane's first wall at ~10³ members — which still deletes the "cheaper promotion" plan in favor of ephemeral. Secondary: the belt 10⁹ identity's 5% promotion mix is assumed; the only measured mix is 67% hand-outs (2,163 vs 1,058 kicks — in their own stats).

Gold path named in check.md: re-issue with the prof decomposition and a 3-rung, multi-seed leak refit — all from data the run already holds. Tree left clean; no commits made.
