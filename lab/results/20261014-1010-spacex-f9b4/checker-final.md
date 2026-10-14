Working...
Check complete. **Grade: silver** — written to `lab/results/20261014-1010-spacex-f9b4/check.md`, with the author's wiki page corrected in place. Tree restored clean (patch reverted, my probes removed).

**What I did and found:**

1. **Reproduction — exact.** Applied `work/patch.diff` in a clean tree myself; every deterministic column (panels, crossings, increments to 16 digits) is bit-identical to the author's CSVs across all arms; `ref.py` reproduces the headline: c:4 **69/73**, ladder 69/73, disjoint misses as claimed, panels 4.96× median at e ≥ 0.9, passages 114→24 / 184→53 / 124→25. Only timings wobble (within the stated ±30%, conservative direction).

2. **The certificate is real GR.** I built two references sharing no code with the author's (`4K(m)/√(A+B)−2π` closed form; Darwin-constant ODE quadrature). They agree with each other to 18 digits and confirm the ladder control band (2.8–6.6×10⁻¹⁰), the known (8, 0.999) m→1 degradation, and my adversarial verdicts.

3. **Identity — stronger than claimed.** Probe off: all 73 keys bit-identical to unpatched HEAD; suite green (74 tests, 0 failed — the dossier's "53" undercounts).

4. **My adversarial keys cut both ways:**
   - **The rule wins where the author never looked:** (7.205, 0.6), (8.001, 0.999), (8.005, 0.999), (7.999, 0.998) — c passes at ~3–8×10⁻¹⁰ where the ladder fails at 10⁻⁸; independently confirmed. p = 10⁶–10⁷: 68→18 panels, ~10⁻¹² agreement; refusals identical in every arm.
   - **But the rule-alone miss is a band, not one key:** (6.65, 0.3) fails 7.14×10⁻⁹ where the ladder passes — placement-immune there too (c:8 unchanged at 21 panels). Page corrected from "single disjoint miss" to a band.

5. **Why silver, not gold:** the pre-registered candidate was a:4; it failed P1 at a held-out key, and the delivered arm c is a post-hoc repair tuned on that failing key (honestly disclosed, but the dossier still calls c "the frozen candidate" — predictions.md froze a:4). Gain is 4.96× panels / ~3.5× time, under the 10× bar. The named gold experiment: freeze c's constants, pre-register fresh, sweep the residual band (δ ∈ [0.01, 0.1] × e ∈ [0.1, 0.6]), the 10⁶–10⁷ decade, and wire the passage certificate.
