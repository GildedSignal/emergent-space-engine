Grade: silver

**Abstract.** Claim: SEM energy closure (memo P8) killed in a v2 replica — no useful root, 0.3–7% of steps solved, 5× cost, B13 proxy 2.4× worse. Reproduction is bit-for-bit (both ensembles, all four flyby JSONs). But the replica's kick is sign-flipped (`dp = −w·∇U_P`, a repulsive planet): at k=12 the map diverges 13% in a from an RK4 attractive truth (corrected sign: 5.9×10⁻⁷). With the memo-faithful sign my reruns overturn the kick-variant mechanism (solves 99.98% of ensemble steps, useful λ-root at 99.3%, lever/K ≈ 200; harmless: jump rms 1.10× base) and drop C levels ~10×. The step-scale SEM (P8 literal) kill survives both signs (94–95% unsolved, degenerate λ→0 root) at 5× cost. The adoption decision stands; the mechanism and the numbers do not.

## Reasons
**1. Reproduction (mechanical): exact where it matters.**
- Ensemble k=6 150p: base jump_rms 3.125e-3, final_maxerr 1.413e-2; kick unsolved 0.9642, 6.459e-3, 2.296e-2 — all identical to the author's JSONs to every digit printed. Flybies: unsolved 0.99697/0.99559, kicks 11/11, outgoing elements identical to 7 digits (a 0.8265428/0.8265428, e, ω likewise).
- Control step 10p: claimed 92.8%, shipped code regenerates 94.2% (closest variant: periods=5 → 92.65%); predictions.md discloses a mid-run clip change ("old 0.2 clip"), so this is drift, not fabrication.
- Not regenerable from the shipped script: the wiring numbers (dH_D per drift, "RK4 continuum dC ≤ 7×10⁻¹⁵", the K-walk 6.9×10⁻⁴ diagnostic) — no mode produces them; `run.log` is empty. `metrics.json`'s commands also omit the step-ensemble run whose numbers it quotes; I reran it separately: unsolved 0.9558, jump_rms 2.721e-3, final_maxerr 1.154e-2 — identical to every digit printed.

**2. The replica is not v2: the kick sign is flipped.** `u_grad` returns ∇U_P = −Gm·(x−x_p)/d³ (points at the planet — verified numerically), and line 136 does `dp = −w·u_grad`: **repulsive**. Memo §2.2 and Hamilton's equation for K = H_D − U_P + p_t give Δp = **+**w·∇U_P. Evidence it matters: (a) one-step probe — a ship at rest beside the planet is pushed away; (b) an RK4 attractive-CR3BP truth for the author's own flyby IC (dC 4×10⁻¹³): with the sign corrected the map at k=12 matches RK4 to 5.9×10⁻⁷ in a; the shipped map is off by 1.3×10⁻¹. Every C-error level in the dossier is therefore first-order pollution from integrating the wrong flow, not a scene constant: faithful-sign ensemble (same seed 7 ships, same k) jump_rms 5.86e-4 vs 3.13e-3, final_maxerr 1.47e-3 vs 1.41e-2, exponent −0.007 vs 0.092. The author's diagnosis ("my scene's perturbation is stronger") was wrong; their own prediction of 20–80% solved for KICK was right for the faithful law.

**3. The kick-variant kill collapses under the faithful sign.**
- Solvability: attractive ensemble unsolved 0.0002 (vs 0.964 shipped); deep attractive flyby (my rescan under attraction, q = 19.8 R_p, 7303 kicks in the k=12 truth) solved 100%.
- Root existence, secant-independent (λ-grid over 1190 real steps): useful λ_w-root ∈ [0.2,5] at 99.3% of attractive steps vs 8.9% shipped; median |lever/K_b| = 200 (attractive) vs 0.04 (shipped). The "far-field lever starvation" is an artifact of the sign-inflated K_b, not a property of v2's split.
- Harmlessness: attractive ensemble jump_rms 6.46e-4 = 1.10× base (claimed: 2.07× worse with 2.7× the bias). Deep flyby outgoing elements: kick 1.0e-4 vs base 3.7e-5 (2.7× worse relatively — direction survives — but both are 100× below the shipped levels and far inside B13's 1%).

**4. What robustly survives: the P8-literal (step-scale) kill.** The memo's named candidate (Kane–Marsden–Ortiz Δt-solve) is the `--sem step` variant. Unsolved 94.0% (faithful flyby), 94.7% (faithful deep flyby), ~92.8–99.7% (shipped runs); the mechanism is sign-independent: K(λ_s) ≈ c₂(λΔs)² is sign-definite with only the degenerate root λ→0, so solving means not stepping (paying accuracy with steps), exactly as the dossier says. Cost 5× by construction (5 evaluations/step), over P7's 1.5× bar. So the frozen P8 kill line ("a solution is missing at more than 1% of steps") is triggered on the faithful law too.

**5. Predictions and honesty.** predictions.md (12:08) precedes every decisive artifact (flybys 12:19, ensembles 12:26–12:31); the decisive inversion (KICK solves 0.3–3.6%, predicted 20–80%) is reported prominently — though it was the signature of the sign error, not of the method.

**6. Novelty.** No SEM / Kane–Marsden–Ortiz / energy-closure entry in docs/HISTORY.md; the memo leaves P8 explicitly open ("GLM, optional"). The step-kill is new, decision-relevant evidence for the B12 rebuild. Goal fit: B12 is the headed-next bottleneck; fits principle 9 (a failed expectation kills the configuration, not the method) — and H0183's "diagnose which one broke" cuts the other way here: what broke was the replica.

## The one experiment that would make it gold

Rerun P8 with the attractive kick (one sign bit; my `runattr.py` wrapper) and rewrite the dossier's mechanism and level claims around it: step-scale SEM killed (94–95% unsolved, degenerate λ→0, 5× cost — stands), kick-weight closure **solvable at ~100% but useless** (1.10× jump rms, 2.7× deep-flyby elements, 5× cost — a redundancy kill, not a starvation kill). I have already run every piece of this; the author folding it in with the corrected levels and the RK4-wiring check is one step.

## What the author missed

- The sign of the kick — the single most load-bearing bit of the replica — was never tested against the memo's formula or against any external truth. The RK4 continuum check they ran (C conserved) is the *attractive* flow's invariant; had it been wired to the map (map at high k vs RK4 trajectory) it would have caught the error immediately. Instead the map integrated a repulsive planet for every headline number.
- All level statements (C ~10⁻², K steady offset 6.9×10⁻⁴, jump rms 3–6×10⁻³, exponent ~0.08–0.09, "B13-marginal 1.4×10⁻²") are first-order artifacts of that sign; the faithful levels are ~10× lower and B13 passes with 3.7×10⁻⁵ — which incidentally *confirms* the memo's §2.5 claims about v2.
- Wiring numbers not regenerable from the shipped script; `run.log` empty; the step-ensemble missing from the reproduction commands; control number drifted post-predictions (disclosed clip change, but not flagged in the dossier).
