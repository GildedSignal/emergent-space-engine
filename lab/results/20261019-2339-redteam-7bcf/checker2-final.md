Working...
`check2.md` written. Summary of the check:

**Grade: gold** — `lab/results/20261019-2339-redteam-7bcf/check2.md`

**Reproduced:** `bash regen.sh` exit 0 in 16 s, every number byte-identical (one-sample p99 1.1092, mix-quad 0.0332, two-path 9.0×10⁻¹⁵, ops 6800/19/4320, verdict PASS re-derived). Freeze sha256 `a6335a29…89ce` holds; `predictions.md` predates the script and cites the frozen hash.

**Independently verified physics:**
- k matches the exact identity √((1+u)/(1−u)) to 5×10⁻¹³ over 20 000 samples (the instrument's two paths are weakly independent, so I checked the formula itself).
- The central claim re-derived by hand: ∂ln k⁴/∂u∥ = 4γ₀² at the bulk, du∥/dv′∥ = γ₀⁻² under composition → **d ln k⁴/dv′∥ = 4 exactly, any β**. The comoving cancellation is exact.
- The observer-frame swarm has no moment cure: finite density at u→1⁻ with k⁴ ~ C/(1−u)² gives a divergent E[k⁴] (tail index ½) — the recorded n-divergent CV is structural.

**My adversarial cases** (all beyond the frozen range): β 0.999 (γ 22.4) — mix-quad PASS (0.0103/0.0201), CV = 4σ holds; squad separation ±0.6 — mix-quad 0.0041 PASS while bulk dies (1.42); fresh seeds — bar robust. Three domain edges found and folded into the page's freeze sentence: the frozen N=400 license bar saturates on the truth's own sampling floor by σ ≈ 0.12–0.15 (readout itself still 4.9×10⁻⁴ vs a 10⁶ truth), the Gaussian squad model draws superluminal internal velocities at σ ≳ 0.2 (no rejection in `members()`), and ops are linear in squad count (10 squads = 21 600 counted ops > the 20 000 fence the frozen ≤2-squad cases never reach).

**Page:** author's lines match the evidence number for number; I appended a Checker-2 paragraph with the three edges. Topic stays open. Nothing else in the run folder was modified; attack scripts live in /tmp.
