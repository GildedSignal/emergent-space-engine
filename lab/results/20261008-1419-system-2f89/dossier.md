# Dossier — run 20261008-1419-system-2f89 (lens: the whole system)

## Claim

The SEM step (solve each step's physical time so the extended constraint K = H_D − U_P + p_t is
exactly zero at the step's end; Kane–Marsden–Ortiz 1999, applied to the v2 fictitious clock)
**is killed on the v2 clock: for 44% (k = 6) to 58% (k = 8) of steps the equation has no
solution at all** — the per-step residual is one-signed in the step size, so "solve Δt so K = 0"
degenerates to Δt → 0, and a Newton left to try walks to its bracket (measured fail rate 100%
at k = 8, mean |α − 1| = 2.5). The kill line (memo P8: no solution at more than 1% of steps) is
exceeded ~50×.

## Bottleneck

Not the board's cost bottleneck but its **instrument bottleneck**: B12 is being rebuilt
(q-b12-design) because it cannot tell a bounded state-dependent offset from growth. The system
view that picked this run: the fictitious clock `s` and the energy register `p_t` are **two
carriers of one constraint** — K = H_D − U_P + p_t ≡ 0 (Opus motion memo §2.2). The v2 split's
residual of K is exactly what B12 reads (C = 2J − 2K, with J exact by the kick's form; verified
here to 5.6e-17 per kick in float). If the loop could be closed exactly through the step's own
time, the law would pass B12 by construction and the memo's "keep the offset small" strategy
(§2.5) would be deleted. This was the memo's one open candidate (§2.6) and P8, the one probe it
assigns to GLM. **The answer is no, and the reason is structural**: v2's per-step residual is a
shadow offset ≈ α²·C₂(x, v, t)·ds² + α³·C₃·ds³, a function of the state whose sign does not
change when the step is scaled, except where the cubic term competes (encounters, coarse k:
55.7% of steps there do have a root, against 42% at k = 8). A step-size solve can only reweight
the two terms; it cannot project the residual away where one term dominates.

## Evidence

Linux x86 cloud, orders of magnitude only. Commands (from `lab/results/20261008-1419-system-2f89/`):

- `python3 p8.py smoke` — the kick conserves J = p_t + Ω·L to **5.55e-17** per step; the
  continuous symmetry ∂_tU_P = −Ω·(x×∇U_P) verified numerically (the memo's discrete Noether).
- `python3 p8.py b12 8 plain 200` — plain v2, k = 8, 16 ships, 200 periods, planet radius ×10⁻³:
  median windowed-max exponent **0.064**, worst |ΔC_obs| **4.97e-7**, 0 lost (85 s).
- `python3 p12 6...` → `python3 p8.py b12 6 plain 200` — k = 6: exponent **0.061**, worst
  **4.46e-6** (residual scales ~ds², as the memo says).
- `timeout 420 python3 -u p8.py b12 8 sem 200` — SEM: **fail_rate 1.0**, mean |α−1| **2.49**,
  exponent 0.131, worst 2.76e-7, 54,263 steps (420 s ≈ 5× plain per step, as expected for
  2 propagations per Newton iteration).
- Root census (the decisive diagnostic, 300 steps of the most chaotic ship, K evaluated at
  α ∈ {0.25, 0.5, 1, 2, 4}): **k=6: 55.7% of steps have an interior root, 44.3% are one-signed;
  k=8: 42.0% root, 58.0% one-signed**; |K(α=1)| median 4.0e-11 (k=6), 6.1e-13 (k=8). Script in
  the transcript; ≤ 6 s.

Controls: plain v2 lands in the memo's bands (my ensemble is milder than B12's frozen ships —
worst error ~10× below its 1.2e-5 at k = 8 — but the harness sees growth, ships at exponent
0.5–1.6, and split error 8 orders above the roundoff floor; not VOID). Two disclosures: (1) my
first and second executions of the SEM/B13 runs were killed by my own 280 s/420 s `timeout`
with Python's stdout still buffered (empty files); the k = 8 SEM run completed on the third
attempt and the root census replaces the killed k = 6 SEM run as the decisive measurement;
(2) the B13 SEM fidelity comparison and a B14 moon scene never ran (time); the kill does not
rest on them — the no-solution criterion alone is exceeded ~50×.

## Predictions

[predictions.md](predictions.md) was written before the decisive runs. What happened:

- Predicted failures concentrated at encounters with rate 0.01–2% (kill line 1%): **wrong in
  magnitude, right in place** — the rate is 44–58% (or 100% as a solver outcome), and roots do
  concentrate at encounters (coarse k has more of them). My predicted "wide uncertainty" band
  did not contain the truth; the mechanism I named (dU_P/dt = 0 degeneracy) was the local version
  of a global one-signedness I did not anticipate.
- Predicted "SEM exponent < 0.5 at k = 6, B13 within 2 ships of plain": untestable after the
  kill; the k = 8 SEM exponent (0.131) is meaningless as SEM (α never converged) — it is plain
  v2 with bracket-walking step scales, and it still did not blow up (worst 2.8e-7), which is
  itself evidence for v2's robustness to step abuse, a held-out observation I had not predicted.
- Predicted 0–1 lost ships: 0 lost everywhere. Held.

## What would make it wrong / the cost of adopting it

- The kill is for the SEM solve **on the step's own time** with the whole step scaled. A
  different projection direction (the kick weight alone, or KMO's discrete-action step, or a
  half-step solve) could have roots where mine does not; I did not test those (time), and the
  α²-sign argument makes me doubt them but does not forbid them. This dossier kills the
  configuration as posed, not every exact-constraint scheme (a KILL kills configurations).
- If a future variant works, the cost is real: the solve multiplies per-step cost ~5× in this
  replica, and in integers the step's physical time becomes the output of a fixed-iteration
  Newton — still deterministic, but the memo's "no step choice" becomes "a solve, not a choice".
- What stands after the kill: v2's residual-of-K strategy is not just convenient, it is the
  only local option found; **B12's rebuild (q-b12-design) should not wait for an
  exact-constraint law**, and B12-v2's statistic should aim to certify "bounded, state-function
  offset" (the memo §1.7's distinction) rather than exact conservation.

## Fit with PRINCIPLES

- "A failed expectation is not automatically a failed method: diagnose which one broke" (H0183;
  #9): the failure is the equation's root structure, measured, not the method of probing it.
- "Errors never compound" (#13): SEM was the attempt to make the constraint error exactly zero;
  the representation refuses — the right reading is that v2's error type (a state-function
  shadow offset) is the floor for this family.
- "Compute only surprises" (#3) / "less is more" (#1): closing the loop exactly would have
  deleted a strategy, not added compute; the kill retires the question at the cost of one
  afternoon's probe.

## The lens

What this lens may have made me miss: I came for a unification (clock and register as one
constraint) and the unification held — but its exact closure is forbidden by a sign structure
only visible in the α-family of the split, which no per-component view (the clock's builder, the
register's builder) would have measured. The hard special case that could break my kill: a
many-planet or strong-field scene where the cubic term always competes (encounter-dominant
dynamics) might put the root fraction back above 99% — the kill is then scene-dependent, and my
census covers one circular-restricted scene. Also unmeasured: whether roots, where they exist,
are reachable by a bracketed solver in integers at fixed iterations; I only measured their
existence.
