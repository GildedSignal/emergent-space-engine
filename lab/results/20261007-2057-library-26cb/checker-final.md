Working...
Check complete. `check.md` written to `lab/results/20261007-2057-library-26cb/`; nothing else touched (adversarial scripts live in `/tmp/hlive-check/`).

**Grade: silver.**

Verdict in brief:

- **Reproduced bit-identically** in a clean tree (9.7 s, deterministic integer counts); `patch.diff` empty, no repo edits. `predictions.md` (21:06:08) predates the probe script (21:09:59) and its output (21:10:08) — genuinely held out.
- **The physics core holds.** LL implementation independently verified (b₂/b₁ → (5/4)α to 0.13% at α=0.1 via 200k-point quadrature); seed-stable to ±1% over 5 seeds; μ_J=0 leak control exactly 0.0; all budget arithmetic reproduces; all 7 lens quotes exist in the 4,580-quote cache. Novel: HISTORY.md and HANDOFF confirm H_live was unmeasured.
- **Why not gold:**
  1. Pre-registered P1 failed in magnitude (predicted 0.01–0.1 bits/orbit, measured 1.43) — honestly reported, but the lab's own precedent caps this at silver.
  2. The 0.27/orbit headline is a **1.5× undercount**: the probe samples 2 kyr at 10-yr steps against an 8.6–17.6 kyr secular cycle; converged sampling (30 kyr, 2-yr dt) gives 0.397/orbit. The sampling-invariant statistic is sum|d| ≈ 0.38–0.40. Bits/orbit stays ~1.37, so the author's own kill criterion (≥1.5) still does not trip — I verified rather than assumed.
  3. The hot-tail κ is parameterized, so the headline threshold f·κ ≳ 3×10⁻³ is arithmetic on an assumption. Gold experiment: measure κ on the design's own kick layer.
- **Notable attack finding:** an outer belt (a∈[3.5,4.9]) makes 53% of bodies resolve encounters (min gap −1.66 AU vs 0.29 AU tidal radius) — the "exactly zero E-key changes" is specific to a belt truncated inside the perturber, so the B18b rung must pin the belt's extent.
- **Minor integrity ding:** predictions.md pre-registered a 1% LL control with "failing ⇒ VOID"; the dossier reports 5.4% as a pass without flagging the reframe — though my independent check shows the LL core is correct, so the result stands.
