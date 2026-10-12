Grade: silver

**Abstract.** Claim: the interaction clock is regime-dependent (conjunction / orbit-averaged / resonant), and time-quantized averaged forcing aliases. Everything reproduces bit-identically; the belt and resonant W-sweeps match exactly (ϖ̇ up to 147% off; resonant ē 337–513% until W=π; seg8 aliasing 165 MADs, Jacobi 110× the floor). But the favorable half dies under adversarial checking: at 64 seeds against u4096-converged truth, w0.5's "3.6× over u8" on ė inverts to noise (2.78 vs 2.43 MADs; u16 is 0.60), and shell-engaged encounters show no clock win. Net: a negative package — conjunction windows buy nothing measurable at matched count, event-scheduled cadence does not walk Jacobi, tick-anchored averages alias (sign-robust across seg4/8/16). Do not adopt the window-keyed cadence. The kills largely confirm H0204/H0205.

## Reproduction

Compiled from source in a clean tree (empty `patch.diff`, no repo edits). Eleven cells rerun — encounter {u64,u8,u16,u32(64),w0.25,w0.5,w1.0,u2048}, belt {u2048,u8,w0.5,w0.5seg8} — **bit-identical** to `work/`. `analyze.py` regenerates the dossier's table (u64 0.00/0.00; encounter w0.5 0.12/0.55; u8 0.12/1.99; belt w0.5seg8 8.28/165.5, Jacobi 1.44e-1 vs floor 1.30e-3). Sweep claims verified from the author's CSVs: belt ϖ̇ rel-err 43.4/2.9/33.9/66.4/94.3/142.2/146.9/66.6/0.0% across W — non-monotonic as claimed, W=0.25 an isolated dip; resonant ϖ̇ 84.5%→0.7% at W=1.5, ē 337–513% until W=π. P4 holds (w0.5 Jacobi 2.84e-1 vs u64 2.72e-1; belt 1.29e-3 vs 1.30e-3). Truth convergence: my 16-seed u4096 agrees with u2048 to 0.03 MADs on ē (the dossier's 2.43-MAD scare was its 4-seed check), and u8192(8) sits 1.0 MAD from u4096 — truth is solid.

`predictions.md` (12:37) predates the code (12:41) and decisive CSVs (12:43–12:49); scoring is honest (P2, P3-recovery reported as failures). One record inaccuracy: the scene correction (encounter e₀ 0.20→0.05, μ 1e-3→1e-4) is claimed "logged in predictions.md" but that file still specifies the old scene. Minor: the belt u2048 truth cell runs >60 s, not ≤60.

## Adversarial cases (all in this replica, my patched copies in /tmp)

1. **64 seeds, encounter (the P1 headline).** Against u4096(16) truth: d(ė) u8 = 2.43, w0.5 = 2.78, u16 = 0.60, w0.25 = 6.08, u32 = 0.39, w1.0 = 0.44 MADs. The 16-seed 0.55-vs-1.99 (3.6×) **inverts**: w0.5 is indistinguishable from count-matched u8 (despite 28% more kicks) and 4.6× worse than u16. "w0.5 matches u16" fails; only "w1.0 matches u32" survives. The bolded impulsive-regime win was 16-seed median luck, inside the author's own stated 2.4-MAD noise caveat yet promoted to the claim sentence.
2. **Genuinely impulsive scenes.** The shipped "encounter" scene never engages the proximity shell (q = 1.1875 vs shell ≈ 0.097 around the planet) — "impulsive" rests on a force-variation ratio alone. At e₀=0.15 (shell engages): u8 and w0.5 both at 0.02 MADs ė — no clock effect; the scene's ė MAD is 27× the grazing scene, weakly discriminating. At e₀=0.20 even with μ=1e-4, 6–11 of 16 seeds eject in every variant including truth — degenerate again.
3. **Aliasing robustness.** Belt seg4/seg8/seg16: d(ė) 4.7/165.5/104.8 MADs, Jacobi 5.7e-2/1.4e-1/2.1e-1 vs floor 1.3e-3 (44–158×). The kill is sign-robust — any tick-quantized segment length is far off the floor — but the magnitude is non-monotonic; the "8-per-orbit subharmonic" is one member of a family, not a law of 8.

## Novelty

The belt/resonant kills re-measure known structure: H0204 already established averages-only-away-from-resonance with conjunction phase kept near it; H0205 killed instantaneous conjunction kicks (2–9× over-pump); the encounters/secular component split is the existing design. Genuinely new measured facts: the tick-anchoring aliasing artifact (principle 14 observed numerically, sign-robust), P4 (event-scheduled cadence does not walk Jacobi — Calvo–Sanz-Serna does not bite this schedule class), and the quantified e/ϖ dichotomy (ė conjunction-local 0.1–8% at any W; ϖ̇ in the average). The 64-seed inversion *strengthens* the negative story beyond what the dossier claimed: the conjunction clock buys nothing measurable at matched count even in the encounter regime.

## Goal fit

On-goal (board bullet 1, cadence; feeds the queued q-cadence rung). But the "conditional adoption" (window-keyed cadence for impulsive-regime bodies, deleting the 64/orbit floor there) rested on the inverted P1 and must not be adopted from this evidence. What the integrator should take: q-cadence's window variant is dead as a *cost* lever in a clean replica; event-scheduled variable cadence is symplecticity-safe; the secular term must be orbit-anchored, never tick-quantized. Fits principle 14 ("no work for no reason, so no ticks") and 19 (the uniform cadence was a fix for not asking when the interaction happens — and so was the window clock, in the impulsive claim's strong form).

## The one experiment for gold

Rebuild the between-window averaged term **orbit-anchored** in this replica (kick schedule keyed to orbital phase, not a fixed time fraction of the orbit) and sweep: if it removes the artificial subharmonic at every segment length while closing the belt ϖ̇ break (147% → u64-level), the run delivers a deployable secular-side rule (component-level, adoptable in one step); if it cannot, the averaged term must be continuous — a hard constraint on the motion-law v2 design. Either outcome, on top of the already-solid kills, clears gold's bar.

## What the author missed

- The 16-seed medians carry ~0.3–0.6 MAD SE against a truth 4-seed-checked at 2.4 MADs; deviations of that size were quoted as bolded findings (3.6×, "matches u16") instead of being held at the author's own noise floor.
- The "impulsive" scene never enters the SyMBA shell, so the regime where the conjunction clock was claimed to win was never actually tested; the genuinely impulsive scenes are weakly discriminating or degenerate (the original scene-correction problem, reproduced at μ=1e-4).
- k/orbit counts only kick evals; every w variant still drifts 64×/orbit and evaluates window membership per micro-step — the cost column is not the plane's cost, which depends on the skin predicting windows from elements (flagged in "what would make it wrong", but the table reads like total cost).
- The aliasing mechanism was asserted at one segment length; two patched builds would have shown the non-monotonic family and sharpened the rule from "8" to "any tick anchor".
