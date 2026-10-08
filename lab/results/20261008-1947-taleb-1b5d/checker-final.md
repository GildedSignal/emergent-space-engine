Working...
Check complete. **Grade: gold** — written to `lab/results/20261008-1947-taleb-1b5d/check.md`, nothing else touched (all reproduction and attack runs in `/tmp/check1`; `work/` originals unmodified).

**What I did and found:**

1. **Reproduced all four dossier commands bit-exactly**: A_gold_T4_s1 (miss@4 35.12% → 0% with rebuilds), B_e06_s1 (96.3%, p50 147, max 202, rebuild identical), D_battle_s1 (inter-cluster 100%, max rank 129 ≈ N/2), geo.py (correlations 0.994–0.998). Controls PASS both ways. Verified the truth instrument independently: v_cap dilation is a sound bound, and my 2× resolution control gives identical pair sets with dmin agreeing to 2×10⁻¹⁵.

2. **Ran four adversarial cases** — all strengthened the claim:
   - e=0.1 scattered apsides: 94% already missed — the failure domain is wider than tested (asteroid-typical e).
   - e=0.6 *aligned* apsides: 0% missed, max rank 3 — the domain boundary is Δϖ, not e; confirms the proposed Δλ*(e, Δϖ) trigger reads the right variables.
   - N=512: p50 rank 300 vs 147 at N=256 (2.04×) with 89 encounters — linear-N scaling confirmed on a thick sample.

3. **Verified the mechanism analytically**: for the battle case, Δλ* = 4e ≈ 1.6 rad (measured 1.556) and rank = N·Δλ*/π ≈ 127 (measured 121–129) — the formula is exact, not fitted.

4. **Novelty**: no HISTORY entry bounds the certificate's domain; the gold sits in the 6 Oct taste log as regime-free.

5. **Flagged weaknesses, none blocking**: rank metric counts self (+1 inflation at the k=4 boundary), geo.py's prediction is half-scale (only scale-invariant correlations quoted), Kepler-only truth (no librations), and `probe.py` was edited after `results_A.json` — but the current code regenerates every stored number exactly, which I verified.

The premise of an adopted gold (a-concentration trigger ⇒ rank-k suffices) is shown wrong with 95–100% silent loss where the trigger fires hardest, and the fix is one closed-form gate plus expiry — adoptable within one step, before `crates/encounters` builds.
