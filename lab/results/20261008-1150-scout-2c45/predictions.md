# Predictions — held out before the decisive runs (written after wiring smoke tests only)

Smoke tests already run (wiring, not decisive): invariants (H_D per drift 1e-15; C = 2(J−K) to 4e-16;
RK4 continuum dC 1e-15), and 10-period control runs that showed: STEP variant ~93% unsolved,
KICK variant (old 0.2 clip) ~96% unsolved. The runs below (ensemble 12 chaotic ships 150 periods
k=6/k=8; deep flyby q in [15,60] R_p at k=8 vs k=12 truth) have NOT been run.

1. **Baseline (v2, no closure) on the ensemble:** per-encounter C-error jumps of order 1e-5–1e-4
   (rms), with a nonzero mean bias (memo §1.1 regime); C error level ~1e-3; windowed-max exponent
   between 0 and 0.8 (wandering regime of memo §2.5 — I do NOT predict a clean exponent).
2. **STEP variant (P8 literal: solve the step's own scale):** stays >90% unsolved on the ensemble
   (no useful root: the shadow offset is sign-definite in the step size, degenerate root at lam=0).
   Its C-error growth is then statistically the same as baseline. KILLED per P8's own line
   (solution missing >1% of steps).
3. **KICK variant (solve the kick-weight lam_w so K=0):** solves most steps AT encounters
   (lever |dU_P/dt|·dt large) but stays ill-conditioned in the far field; overall solved fraction
   between 20% and 80%. Where solved, per-encounter net jumps collapse (>=10x below baseline),
   so C-error growth by decade falls below baseline; final windowed max within 3x of baseline
   (far-field walking still sets the floor).
4. **Solvability concentrates:** unsolved steps for KICK cluster near pericenter of encounters
   ((p−v_p)·grad U_P -> 0) — the memo's "fails where dU_P/dt = 0" — but ALSO in the far field
   (my addition: weak lever), which the memo does not mention.
5. **Cost:** KICK and STEP both ~5 step-evaluations per step (secant, 3 iterations) = ~5x today's
   per-step cost — over the memo's P7 bar of 1.5x if applied to every step.
6. **Deep flyby (B13 proxy):** baseline k=8 within ~1% of the k=12 truth on outgoing (a, e, om);
   KICK k=8 within 2x of baseline's error (the closure distorts the impulse by the O(h) amount it
   solves for; kicks in the flyby ~150–400).

Kill criteria (frozen): KICK is killed if it (a) solves <10% of steps overall, or (b) makes C
growth WORSE than baseline, or (c) flyby outgoing-element error >5x baseline at equal k.
