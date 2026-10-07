Working...
Check complete. `check.md` written; nothing else in the run folder touched, no git operations.

**Grade: lead** — reproduced exactly, but the central claims don't survive adversarial accounting.

**What held:**
- Reproduction bit-for-bit across all 8 configs (14 s, well under budget); `fuzz_ok` 300/300; `predictions.md` genuinely predates the decisive run; two failed predictions honestly held.
- Real, new content: first measurement of the encounter certificate's *invalidation* channels (HISTORY only covered finder cost); ~1% amortization with 96–100% on-time encounters on non-drifting configs; margin-bandaids failing; a negative control that fails as it must.

**What broke:**
1. **`late` is measured on a self-selected minority.** The replay `break`s into a "permanent certificate" when the grant-time window is empty — but Δϖ drift and kicks later *create* crossings. Silent unscheduled encounters (author's own stream): precession-absorb **70%**, driftwin **98.3%**, kicks **88.5%**. So "driftwin restores completeness (late=0)" is vacuous — it touches 2/115 encounters, *worse* than the policies it repairs; "kicks: 3.1% late, the only remaining miss channel" is off ~30×.
2. **Mechanism confirmed directly:** one-segment precession pairs with empty windows at k=0 take real encounters at k≈1143 after ~0.9 rad of within-segment drift, with the walk already dead. Driftwin only widens *existing* windows — the representation fix it claims isn't implemented where the failure lives.
3. **Held-out seed 12 (the author's own nomination):** generic gives **late = 39**, not 0 — the "superset held everywhere" headline is seed-fragile.
4. **`hits` double-counts `late`** (true on-time hits for precession-absorb: 0), and **work omits grants** — 8288 window-samplings (2048 Kepler solves each) reported as work 0.0001.

Named gold path in the file: empty-window grants must expire by drift budget; completeness = scheduled/total; grants priced in; ≥2 seeds.
