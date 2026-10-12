Working...
That was the stale wait loop — the probes had already completed (10 lines, exit 0). The check is finished and delivered.

## Check complete: `Grade: silver`

`check2.md` written to the run folder; nothing else in `lab/results/20261012-0616-…-07b4/` touched, no git writes, this run's `check.md` never read.

**What I did (45-min window):**

1. **Reproduction** — full run in a clean scratch tree: `metrics-real.json` and `analysis.json` **bit-identical** to stored (6 diffs, all `wall_s`). Positive control passes. Provenance verified: `orig-metrics.json` and `hlive_scout.py` are `cmp`-identical to the scout's published branch, so the matched-rate negative control really runs the scout's own code. Refit the toy's stored rows by hand: `alpha_partial` correction −0.418 → −0.817 is right (the stored fit ate the ε-saturation plateau).
2. **Predictions** — mtime ordering holds (predictions 21 min before metrics); 7/7 held with the two caveats the dossier itself discloses.
3. **Attacks** — five adversarial probes, all in budget:
   - **σ_e = 0.2:** safety factor collapses to **1.75×** (vs 2.8–8.7×) — direction safe, α≈0.81 still in band, but "3–9×" is low-e-specific;
   - **b_det ×/÷2:** D@1e-3 moves 95/99/121 — truncation second-order as claimed;
   - **512 vs 256 steps:** K 31.36 vs 31.32 — detection complete;
   - **stream-vs-snapshot identity:** exact at every ε, including the m=1e-6 clipping regime;
   - **one sentence contradicted by the run's own JSON:** "zero single kicks reach a quarter cell" is false (103 kicks ≥ quarter-cell in C6; own `esc_frac_multikick`=0.985).
4. **Novelty/goal fit** — no prior H-entry measures this law on real conjunction geometry; the Γ-anchor correction (18–60×), m=1e-8 saturation onset and the field fix are new; directly serves the board's "10⁹ in 8 GB" item and PRINCIPLES 6/24.

**Why silver, not gold:** the engine's wired belt remains unrun, the 10⁹ store rests on N≤1500 extrapolation (the named gold experiment — real geometry at N=10⁵–10⁶ at fixed Σ — is feasible in this harness and left undone), and the record carries one self-contradicted sentence plus two soft numbers ("2.7×" is actually 6.2×; the "(the toy: 82%)" contrast is a rate artifact). None of these flip a conclusion; the thesis — accumulation-dominated escapes, B18 store 1.7–2.4 B/body, no 10⁹ memory risk from belt dynamics — survives every attack I ran.
