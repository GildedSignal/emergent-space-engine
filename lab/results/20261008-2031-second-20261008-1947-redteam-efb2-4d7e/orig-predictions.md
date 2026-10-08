# Predictions — 20261008-1947-redteam-efb2 (written before the decisive run)

Attack: representation.md §2 "Observables": *"Newton's method finds the crossing, starting from the previous frame's."*
Premise: the previous frame's light-cone crossing is a good warm start. Held-out cases: high closing γ
(the game's signature scene: flying toward a system at high c; the queue targets γ to 10⁶) with emitters on
curved worldlines (a fleet holding formation, a compact binary).

Setup: system frame, observer coasts toward the system at β; 32 emitters on a ring R = 0.2 light-s,
orbital speeds β_o ∈ {0, 0.01, 0.05, 0.3}; observer frame rate 60/s proper time, 200 frames; D0 = 100 ls
(4 ly for γ = 10⁶ so the system stays ahead). Newton from the previous frame's root, cap 32 iterations,
tol max(1e-9, 4·eps·|t_a|) s. Truth control: bisection (F is strictly monotone: |emitter speed| < c).
Positive control: the same Newton warm-started by rate extrapolation (store the arrival-map slope at the
root, advance the guess by Δt_a/slope).

Kinematics: root travel per frame Δt_e ≈ 2γ²·Δτ·(1 ± β_o); the linear signal in F shrinks as (1−β),
leaving the orbital ripple dominant once Δt_e ≳ T_orb/4. Onset γ* = sqrt((T_orb/4)/(2Δτ)).

Predictions:

- P1 (control, inertial emitter β_o = 0): Newton converges in ≤ 2 iterations at every γ up to 10⁶.
- P2 (anchor to H0213): at β = 0.9, warm Newton needs ≤ 6 iterations, 0 failures, all β_o ≤ 0.3
  (consistent with the plane's working 0.9c gather).
- P3 (the kill): failure rate rises from ~0 below γ* to > 50% within a factor ~3 above γ*.
  γ* ≈ 31 at β_o = 0.01; ≈ 14 at β_o = 0.05; ≈ 5.6 at β_o = 0.3.
- P4 (fix): rate-extrapolated warm start converges in ≤ 4 iterations with 0 failures at every γ and β_o.
- P5: at γ = 10⁶, β_o = 0.05: the doc's mechanism fails ≥ 90% of solves (root is ~10³ orbits stale per
  frame), so each visible emitter costs the full 32-iteration cap.
- P6 (wrong-root check): Newton never converges to a root bisection disagrees with (F monotone);
  mismatch count 0 on every 10th solve.

If P3/P5 fail to materialise (Newton robust everywhere), the premise survives and I report that.
