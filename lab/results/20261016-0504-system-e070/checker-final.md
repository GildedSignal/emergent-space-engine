Working...
Check complete. **Grade: silver** — written to `lab/results/20261016-0504-system-e070/check.md`, with the author's wiki page corrected in place where it overstated.

**What held (reproduced bit-exact, plus my own re-flights):**
- Off-arm identity: patched tree with envs unset → digest `5b2d998b…` byte-equal to pristine (re-flown independently, not just regen's word).
- All 7 arms: digests and every table number identical across author ↔ runner-regen ↔ my re-runs.
- The belt wave: seed- and N-independent tick (2,873,098,240), linear a decade beyond the author's range (1e6: fe_max 42,460 = 10.01×/decade), recurring at T, 2T, 3T over 55k game-s.
- The stream split: locals carry ~68–72% of all kicks at both seeds I tested (~70–82× the belt per body).

**What broke under attack:**
- **Seed 3** (unflown by the author): the no-locals control drops the worst frame 689 → 441 — at seed 3 the locals *bind* the worst frame (≥284 of 689 events, 41%), so "the locals contribute 3–6%, ~50 events" is a seed-1 fact sold as a main-tree fact. The refutation of 917c stands at 1e5+ and seed 1's 1e4, not universally at the ladder's low end.
- **The stagger arm is decorative**: at bits 24 it re-times 16 of 40,200 local kicks; at bits 20 (my probe) it is a *complete* no-op. "Moves the peak by exactly 0" measures the belt's composition, not the stagger's power — the no-locals arm is the only load-bearing control.
- Arithmetic slips in exactness claims: 14,177 vs the true 14,151.4 game-s; "exactly half of cf45's 2.814e4" is 0.6% off; "matches a9d7's 3.55e-5" is 1.5×.

**The gold experiment** (named in check.md): a seed-ensemble no-locals sweep (≥8 seeds × {1e4, 1e5}) plus one wide stagger (bits ≥ 26) — one afternoon on the existing instrument decides whether 917c's lever is dead or merely domain-bound.

Tree restored to pristine; nothing else in the run folder touched beyond `check.md` and the page corrections.
