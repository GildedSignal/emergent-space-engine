Grade: silver

**Abstract.** Claim: in a belt under one planet (μ=10⁻³) the quiet interior needs k=16–32 kicks/orbit for the 10⁻⁴ Jacobi bar, set by secular resolution — not by surprise time — while the chaotic annulus and the encounter class (36% of a belt reaching 0.95·a_p) saturate per-body Jacobi on truth and law alike. Reproduced bit-for-bit: both decisive artifacts (`atlas.npz`, `backup.npz`) regenerate exactly from the shipped commands; every derived number I reconstructed (classes 166/102/16, quiet truth p95 3.3e-5, encounter median 0.2, honest rule 11,936 vs 18,176 = 1.52×, wall fit 1.197·μ^0.236, LOO ≤ 0.008) matches. Kills q-cadence's surprise-time premise and hands q-b12-design the saturation input; nothing to build. Silver, not gold, for three record misreports (below), none load-bearing.

**Reproduction (clean tree, patch.diff is empty).**
- `python3 surprise.py selftest` (23 s): exact as claimed (max|dE| 1.33e-15, hyperbolic 5.3e-15, μ=0 control 0/6 finite, Jacobi 1.84e-6 @ h=2π/4096).
- `python3 runs.py atlas`: identical finite fractions (10/19/28/44%), identical crash (json.dump TypeError after the npz save — disclosed in atlas.log); regenerated `atlas.npz` (incl. hchk) is **bit-for-bit identical** to the shipped one.
- `python3 backup.py` → `backup_new.npz`: **bit-for-bit identical**; `analyze_cadence.py` output identical. My independent rerun of the truth on a 60-body encounter subset matched shipped maxdc with max|diff| = 0.
- `analyze_atlas.py` / `analyze_cadence.py` on shipped npz: every printed number matches the dossier.

**Predictions.** Pre-registration order holds (mtimes and log order: predictions at T−29 min, decisive atlas T−15, cadence T−8/−3; the mid-run `surprise.py` edit is the disclosed elems-bug fix). Held: exponent 0.236 ∈ [0.23, 0.30]; teeth 12×; min T_div 25 < 40. Failed and honestly reported as the headline: (3) floor 16–32, not 4; (5) continuum, no bimodality (47% vs 89%); (4) untestable. Not run: (6) μ=3e-4 transfer — disclosed.

**Adversarial checks (mine).**
1. Wall extrapolation at μ=10⁻² (10× beyond the fit, T=1000): measured 1−a = 0.375; the fit extrapolates 0.405 (off 0.03, ~6 bins), Wisdom-exterior 1.3μ^(2/7) = 0.375 exactly. The wall law is robust in order; the exponent stays unresolved.
2. Truth convergence through encounters (hdiv 1024→2048, 60 bodies): median maxdc 0.20 → 5.1e-2 (~h² on the median, erratic per body: only 48% of bodies shrink >1.5×). Still 500× above the bar at 2048; ~20× more refinement needed. So the saturation is instrument — in the continuum C_j is exactly conserved through encounters for this model — and the dossier's "partly physics" is imprecise: what is physics is the *cost*. The B12 conclusion (per-body Jacobi dead there at practical truth budgets) is confirmed and sharpened.
3. The quiet classification transfers: an e₀=0.02 shadow atlas (the scene's eccentricity; the shipped atlas used e₀=0) on a∈[0.60, 0.755] gives 0/128 divergences over 2000 orbits. The k_req floor is genuinely not chaos.
4. The "24" rung: the ladder is {2,4,8,16,32,64}; "16 → 24 → 32" is the per-bin *median* of per-body ladder k_req (16/24/32/32/32) — regenerable from the shipped data (60 bodies @16, 105 @32, 1 @64), but not printed by any shipped script.

**Novelty.** HISTORY H0212 and the board record cadence as the live lever ("six runs agree correctors buy nothing, so cadence is the lever"; q-cadence queued for the hoped 4×). This run kills surprise-time scheduling for the regular belt and prices the honest-rule ceiling at 1.52× — new on the record, and the wall law itself is honestly attributed (Wisdom; run 0c67's 1/4 law). B12's miscalibration and redesign (HANDOFF line 71, queue item 1) receive a measured input. Fits PRINCIPLES §22 ("the simulation tells us what's next not us") and is a useful negative for §3 ("Compute only surprises" — here the surprise rate does not price the compute).

**Why silver, not gold.** Three record misreports, none load-bearing:
- "Matches Wisdom's 1.3·μ^(2/7) exactly at μ=10⁻⁵" is false: measured 0.080 vs Wisdom 0.048 (factor 1.65). It lands on Wisdom only at μ=10⁻² (my check).
- Prediction (1)'s "wall within 0.02 of 0.80" holds only under the predictions' own wall definition (outermost fully-quiet bin = 0.795), not the analysis definition actually used (0.765); the definition switch is not disclosed when reporting (1) as held.
- Prediction (2)'s "≥60% of bins censored" clause failed (49% fully censored at μ=10⁻³) and was silently dropped from the "held" summary.
Minor: "102/284 fail at k=64" is 104 (NaN=fail) or 95 (NaN excluded) — no quiet body is NaN, so k_req is uncontaminated either way; "tracking ≈ 0.75μn(a/Δa)² in square root" is only qualitative (measured ln–ln slopes 0.35–1.33 vs 0.5 depending on Δa); the Jacobi definition carries an O(μ²) inconsistency (`xb = r − μ·c`, missing 1/(1+μ)) that floors the metric at ≈1.8e-6 — irrelevant to a 10⁻⁴ bar but unreported; several headline numbers are regenerable only by re-derivation, not by a shipped command.

**The one experiment for gold.** Own the truth-convergence ladder through the encounter class (hdiv 1024/2048/4096, medians and per-body spread — rung 1 is above): it decides whether B12-v2 can be per-body at any practical truth budget in the encounter class or must be class-statistical by construction, and with the three record corrections above it makes the run adoptable as gold inputs to q-cadence, q-b12-design and B18b belt scenes.

**What the author missed.** The Wisdom misstatement and the two dropped prediction clauses (gold dies on exactly this); the definitional μ² Jacobi floor; that encounter "saturation" is convergent instrument error, so the class gate's necessity is a cost statement, not a conservation statement; the μ=10⁻² point, which both bounds the wall fit's extrapolation and lands on Wisdom; the per-body k_req tail at 64 inside the "quiet" class near the annulus edge.

*Checker's environment: numpy 1.26.4, Linux 8 vCPU, all processes < 200 MB; commands ≤ 60 s except the two sweeps (~3–4 min each), as in the dossier.*
