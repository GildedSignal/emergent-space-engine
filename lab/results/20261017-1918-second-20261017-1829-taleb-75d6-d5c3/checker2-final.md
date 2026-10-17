Working...
Check complete. **`check2.md` written: Grade: gold.**

**What I verified:**

1. **Reproduction** — Runner's `regen.sh` exited 0; I re-applied `work/patch.diff` to a clean tree and recomputed every headline number from the raw CSVs with my own code (independent of `analyze.py`): K2 ratios, same-tick differentials, K5 ρ, seed-2 ratios, all controls — all match. `analyze.py` is clean (128 bodies, no selection; the reference cancels exactly in K5). Common-tick readout is real (identical `tick` columns across all arms).

2. **Predictions** — `predictions.md` predates the decisive artifacts (mtimes). Criteria K1–K5 all resolved; P1/P7 wrong and disclosed. One gloss found: P2's registered quantity (K2_sym(ln a) ≥ 3) failed on every seed but was counted "right" via its core.

3. **Three adversarial cases, each outside the author's range:**
   - **Seed 3** (75d6's checker's held-out seed): both shapes fire ≥3× on e (4.31/4.34) and ω; ρ = 0.97 — mechanism holds stronger; v1's 86–200× confirmed instrument-bound.
   - **Three orbits**: differential decays monotonically (2.09→1.53→1.31 ×10⁻⁷) — one-time typing confirmed on a longer arc.
   - **ref10** (author's named missing rung): nothing fires ≥3× at s1h1 (2.50–2.91); the ω firing is ladder-marginal exactly as the author's own caveat predicted — so the asked-for "illegal at the 3× bar" phrasing must not be frozen; the ref-free 3.0–3.4× band is the freezable statement.

4. **Novelty** — symmetric arm, K5 decomposition, and the v1 horizon bug are all new; the bug verified against 75d6's frozen branch (arms at mult=2 tick 30,946,906,758,455 vs reference at mult=1 tick 15,473,453,379,227).

5. **Page corrected in place**: the blanket "2.5–3.0×" band widened to 2.4–4.3× across seeds; the misleading "e 2.4–2.5×" clause fixed (seed-2's e fires 3.7–3.9×, in the run's own analysis.json); direction 1's ref10 request answered. Tree restored; `check.md` untouched.
