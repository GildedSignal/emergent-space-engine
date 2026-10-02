Grade: silver

Reproduced bit-for-bit from the dossier's commands in a clean tree (symba, mercurius, wh-fixed, wh-dense, soi-switch, truth, janus — every printed digit and every metrics entry identical). Claim verified: at 64 kicks/orbit no float changeover reaches B12's 0.2 here — symba 0.41 with only 18/32 seeds completing; mercurius 0.47, max err 2.3e-5, 1.7 switch events/pass. But the 600× is queue-events only: total force-evals per pass are 2053 (mercurius) vs 1681 (symba) — equal work, not a deletion. TRACE roundtrip vacuity re-verified by my own reimplementation (≈ wh-fixed; errors O(0.1) pass at any eps). JANUS result exactly reproduced. Adversarials strengthen the kill: every checked symba exclusion is error-driven (truth stays), symba corrupts outright at 0.08 R_H, and at mu=3e-6 symba ≈ no changeover (expo ~5) while mercurius holds 2.7e-8. Held down from gold: two headline held-out predictions failed (symba ≤0.1, trace ≤0.2), the stored trace row is not regenerable from the shipped code, the truth-control claim is overstated (6.7e-8, not 2e-11), and kill #2 tested a cumulative-error ratchet — my per-step variant stays cheap (28.6 retries/pass) yet still fails at 0.59.

## Reasons

**1. Reproduction (clean tree, `git apply work/patch.diff` — it only deletes a doc line in `force.rs`, no behavioral effect).**
- `python3 changeover.py` (truth + schemes): truth per-seed values identical (incl. seed 1 = 1.3e-8, seed 7 = 6.7e-8); symba seed-by-seed identical (expo 0.28/1.01/0.54/10.28, events 38664/28596/27880/9296); mercurius identical (0.60/0.56/0.59/0.36).
- `python3 analysis.py`: medians match stored metrics.json to the last digit — symba 0.4115731539552824 (ens 0.594, worst 1.2, 18/32), mercurius 0.468136196260884 (2.26e-5, 1.7 ev/pass, 1375 inner, 29/32), wh-fixed 0.464 (0.37, 15/32), wh-dense 6.066 (1.8, 11/32), soi-switch reproduced.
- `python3 janus.py`: identical JSON — smooth bit-reversible (5.2e-3 worst dC/C), position-only heaviside bit-reversible but 30.6× worse (0.158), velocity-dependent radial **not** bit-reversible. The reversibility algebra checks out (mid-state positions coincide under p-flip with exact integer maps).
- Judge port verified against `xtask/src/behave/fit.rs` (identical windowing, floor, NaN rules) and `handoff.rs` (B12 recipe, 200 periods, P/8, median, err_max 1e-4).

**2. Predictions.** File times hold: predictions.md 00:22:44 < truth.json 00:25:54 < decisive runs 00:43. Held: mercurius [0.2,0.7]=0.47 with ~2 handoffs and hundreds of fevals; soi 0.6–1.0 ensemble (0.94); JANUS #10 fully (the strongest). Failed: #1 symba ≤0.1 (0.41), #2 trace ≤0.2 (0.74), #5 wh-dense ≤0.3 (6.1), #7's "<1e-12" (6.7e-8), #8 bins; #9 (moon) never ran. The dossier reports #1/#2 honestly; #5 appears only as a table footnote. The addendum's seed-group replacement is truth-measured, as claimed. Not disclosed: changeover.py was edited at 00:32:38 *after* predictions — full.log shows the first run crashed (Kepler overflow in mercurius); the edit adds the crash guard that turns crashes into `ok=False`. Legitimate hardening, but the addendum should have said so.

**3. Adversarial cases (mine).**
- *Exclusions are error, not physics:* on seeds 1, 6, 12, 13, 25 (symba's 14 exclusions incl. mercurius's 2) the truth stays at r ≈ 1.2–4.5 for 200 periods. Symba's 0.41 median is over its 18 survivors while it corrupts 44% of seeds (max err up to 222). Under B12's real rule (cannot answer = fail) the smooth-cascade replica is far worse than the handoff, beyond the exponent comparison.
- *Extreme deep pass (periapsis 0.08 R_H, below symba's deepest shell 0.11 R_H):* symba replica fails outright (max err 77); mercurius holds 2.8e-5 (21.6k fevals); wh-dense 2.6e-3. The author's seeds stop at 0.17 R_H — the regime the lens named (0.1 R_H) went untested and it breaks the incumbent replica.
- *Mass scaling (mu=3e-6, 6 eccentric-crossing seeds, 100 periods):* symba med expo 4.8 ≈ wh-fixed 5.0, max err 1.6e-4; mercurius 0.56 with max err 2.7e-8. The ranking sharpens: the smooth cascade at this budget is no better than nothing at Earth mass.
- *Per-step TRACE:* the shipped Jacobi check compares against the **initial** C0 (cumulative), so after the first pass every step ratchets to the H/256 floor — the 2M-retry degeneration is that ratchet, not a property of Jacobi checking. My per-step variant (same eps=1e-6) does not degenerate: 28.6 retries/pass, 141 kicks/orbit — and still fails hard (med expo 0.59, worst err 1.0, ok 16/32). TRACE dies on accuracy either way, but the dossier's mechanism for kill #2 is wrong.
- *Roundtrip TRACE reimplementation* (variant not shipped): at eps=1e-10 it fires twice in 32 runs and equals wh-fixed (0.46); the author's 191-retry version differs only by eps choice. Kill #1 (self-adjoint DKD roundtrip = roundoff only) is sound and robust in eps.

**4. Novelty.** No HISTORY entry compares changeover mechanisms on B12; events3's soi kill is cited and used as the negative control (reproduced: ens 0.94). The reversibility refinement of law.md's "state-selected switch" line (positions at the symmetric mid-state keep bit-reversibility; smooth-in-position is what keeps the bound) is new and measured. Board focus item 2 is directly addressed.

**5. Goal fit and PRINCIPLES.** "Errors never compound" (13): the exponent table is exactly the error-type measurement the gates demand, and the answer is negative at this budget — a real result. "Less is more" (1): the honest deletion here is TRACE-retry at this budget ("retries that fire everywhere are the anti-pattern" — verified by the ratchet). Two caveats on framing: the 600×-fewer-events claim is doll-queue accounting while total force-evals per pass are ~1.2× *more* than symba's; and "time-dependent selection must be banned outright" does not follow from the reversibility demo — the demo's own heaviside map B kicks at interval-start time and is bit-reversible; that ban comes from the shadow-bound argument, not from JANUS.

**6. Build integrity.** `run_trace.json` and `run_trace_roundtrip.json` are the *roundtrip* variant, but the shipped `Trace` class is the Jacobi variant — the stored trace row and metrics.json's trace entry cannot be regenerated from the delivered code (the r4-v3 smell, smaller: disclosed in the table, and reimplementable from the docstring). The Jacobi row's own numbers (2M retries, 3 seeds) have no stored artifact. The dossier's claim that its replica "stacks all level kicks at the step's midpoint (no drifts interleaved)" mis-describes the shipped Symba, which interleaves drifts properly — the "lower bound on the plane" argument rests on the time-vs-phase stepping alone.

## The one experiment to gold

Run the *shipped plane's* phase-stepped cascade (crates/universe) and the per-step-Jacobi TRACE on these same frozen 32 seeds. If the incumbent also misses 0.2, "no float changeover at the budget reaches the bar" is a property of the mechanism, not the replica, and TRACE is fully dead by accuracy rather than by a ratchet — adoptable in one step.

## What the author missed

- The cumulative-vs-per-step distinction in the Jacobi check (the actual cause of kill #2's degeneration).
- The sub-shell extreme (0.08 R_H) — named by the lens, untested, breaks the cascade replica outright.
- Mass generality: at mu=3e-6 the cascade ≈ no changeover; the whole ranking question is mu-dependent.
- The exclusions are themselves the behaviour result (error-driven; B12 counts cannot-answer as failure), stronger than the exponent medians.
- The roundtrip variant should ship with its stored row (or at least its eps).
- The JANUS demo contradicts its own time-dependence ban (map B is time-dependent and reversible); state the ban as an error-bound claim.
- The truth control is not ≤2e-11 (max 6.7e-8; two seeds exceed B12's own 1e-9 convergence bar — under B12's rules they would be excluded).
