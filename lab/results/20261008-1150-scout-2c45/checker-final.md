Working...
Check complete. `check.md` written with **Grade: silver**; nothing else in the run folder touched, no git commits.

**What I did**

1. **Reproduced** every command in `metrics.json`: both ensembles, all four flyby runs, and the step-ensemble (absent from the commands) regenerate **bit-for-bit** (e.g. kick ensemble unsolved 0.9642, jump_rms 6.459e-3; step ensemble 0.9558/2.721e-3/1.154e-2 — every digit). Control-step drifted (92.8% claimed, 94.2% regenerated; a disclosed mid-run clip change). Wiring numbers (RK4 dC, dH_D, K-walk) are not regenerable — no mode in the shipped script; `run.log` empty. Predictions (12:08) precede all decisive artifacts (12:19–12:31).

2. **Found the replica is not v2 — the kick sign is flipped.** `u_grad = ∇U_P` (verified: points at the planet) but `dp = −w·u_grad` → a **repulsive planet**, contradicting memo §2.2 (`Δp = +w·∇U_P`). My RK4 attractive truth for the author's own flyby IC: the corrected-sign map at k=12 agrees to 5.9×10⁻⁷; the shipped map is off 13% in a.

3. **Reran the decisive configs with the faithful sign** (same seeds/scenes): the kick-closure kill **collapses** — solves 99.98% of ensemble steps (vs 0.964 unsolved shipped), useful λ-root at 99.3% of steps on a secant-independent grid (median lever/K = 200 vs 0.04 shipped), harmless (jump_rms 1.10× base); C levels drop ~10× (5.9e-4 vs 3.1e-3; exponent −0.007). The "far-field lever starvation" is an artifact of the sign-inflated first-order residual. The **step-scale SEM kill (P8 literal, the memo's named candidate) survives both signs** (94–95% unsolved, degenerate λ→0 root, 5× cost).

4. **Novelty** confirmed (no SEM/energy-closure entry in HISTORY.md; P8 was explicitly open).

**Verdict:** real, reproducible work; the adoption decision (drop SEM, judge boundedness) stands — but the central kick-variant mechanism and all quantitative levels are artifacts of a one-bit physics error, so gold is not earned. Silver, one experiment away: fold in the corrected-sign rerun (which I already executed in full).
