Working...
Check complete. `check.md` written: **Grade: silver**.

**Reproduction — exact.** Out-of-place rerun (author's record untouched, hashes re-verified identical at close): `events.csv` md5 `bd310ef8…` equals the inversion's own blob on its `claude/lab-20261007-0800-inversion-7532` branch — the primary record, not just self-consistency; `watch-out.jsonl`/`lead.csv` bit-identical; 152 s, < 300 MB. Every dossier number re-derived from the jsonl and `lead.csv`, including the lead-time model (A 0.0016/0.0016, C 0.363/0.377, D 0.632/0.674). The definition premise verified from primary sources: the gold pre-registered rank "by current distance, min of both directions"; the inversion measured mean-longitude rank; this run implemented the gold's actual watch.

**My four attacks** (the author's instrument copied to /tmp with a λ-window knob and tunable cadence):
1. **Dense convoy** (300 bodies in 0.02 rad, ρ ≳ k·spacing): exact-policy misses **5.71%** — the author's own 0.5% kill threshold fires 11×; grazing contacts (d≈0.9ρ) with ≥5 nearer bodies. The zero-miss claim needs an unmeasured density gate (πρ²·n_local ≲ k), in the gold's own subject (co-orbital concentration).
2. **High-e** (σ_e=0.3): zero misses — the certificate is more robust than tested; refresh failure worsens (92%, leads 0.03 orbits).
3. **n-scaling**: churn per body 12.4 → 18.2 → 24.1 at n = 600/1200/2400 — **√n, not the linear law** (which predicts 24.8/49.6). The cost model's n-extrapolation is wrong (conservatively).
4. **Cadence control** (1024 vs 256 samples/orbit): churn 20.0 vs 19.0 — saturation is real physics, not coalescing undercount.

**Why silver, not gold:** the central zero-miss headline lacks its validity condition and falls to the first density attack; the churn law's n-dependence is inferred and wrong; the O(1)-per-entry incremental rebuild is asserted, not built — one builder rung (incremental, churn-paced, density-gated watch measured end-to-end vs the quadratic tier, convoy included) from gold. Predictions were genuinely pre-registered with honest failures, and the inversion's 60–88% headline is definitively dead on the primary record — the surviving corrections (global watches, churn-paced refresh) are real design inputs.
