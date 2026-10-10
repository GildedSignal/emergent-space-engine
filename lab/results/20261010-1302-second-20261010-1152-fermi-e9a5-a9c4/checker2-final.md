Working...
Check complete. `check2.md` written to the run folder — **Grade: gold**.

**What I did (45-min budget):**

1. **Reproduction** — `python3 probe.py` in a clean /tmp copy: `metrics.json` byte-identical to the record modulo the `env` block (only loadavg differs); 15.0 s wall, 618 MB RSS as recorded; `patch.diff` empty, no tree edits.
2. **Predictions audit** — mtime order confirms predictions.md preceded the decisive run; all six held within their stated bands (P1 cold-belt 40.29 raw in 38–42; P2 bias 1.453±0.015 in 1.2–2.0, constant per-σ; P3 ±1.0 % vs ±4 % allowed; P4–P6 exact).
3. **Six adversarial attacks, all confirming:**
   - kNN (distribution-free) entropy of end-state residuals agrees with the +1.45-bit-corrected plug-in to **0.013 bits** on all four scenes; kurtosis ≤ 0.08.
   - Kernel vs leapfrog at extreme b (1.2×10⁴–3×10⁶, both σ): ≤ 5.6×10⁻⁴ (belt), worst 1.7×10⁻² at the t≈1 crossover — closes the author's declared gap.
   - WIDTH 0.05–2.0 AU: λ⁺ moves < 0.5 % — verdict insensitive to the cutoff.
   - Colder σ₀=10⁻⁴: 41.78 bits, same as cold_belt (robust from below).
   - Epoch doubling past the record: cold_belt breaks 3-dof 8 GB at ~2¹⁶ orbits, matching the declared 1.3-octave margin.
   - Second seed: 0.008-bit drift. Plus every derived digit (GB, slopes, 2500.000 linearity, churn chain, time conversions, reabsorption) recomputed from the record.
4. **Novelty/goal fit** — HANDOFF line 70 lists H_live as "not measured yet"; the board names this exact bottleneck; no H entry covers scar-growth measurement. Store model is Opus's shipmem, belt program is components-98bc; the missing half is now measured.

**Grade rationale:** reproduced bit-for-bit, all held-out predictions held, my attacks strengthened rather than broke the claims, adoptable within one step at zero code cost. Missed items (per-component 8 GB verdict, play-time vs 10¹⁰-simulated-year horizon, single seed, q_v provenance) are recorded in check2.md but none undermine the claim.
