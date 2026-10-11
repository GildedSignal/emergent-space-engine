# Predictions — 20261011-1600-inversion-e128 (written before the decisive run)

The inverted merge: the energy register (`p_t` i128 at a birth-fixed exponent) + the held-burn
step cap, green on "L15 from tick 0 reaches β 0.999, no refusal" — a test that checks no physics
above β 2e-4 (the work gate's burns are ≤ 2e-4 c). Target regime: γ to 10⁶ (b-high-gamma, dead on
a rate limit); known wall "flying past γ ≈ 2,000 is refused".

Probe: `cargo run --release -p emergent-universe --example inversion_highgamma -- <level> <log2 tmax>`
holds a forward level-`L` burn from the plane's start and reads, at 141 log-spaced checkpoints:
local γ (from the readout and f = 1−2μ/r), proper time τ, the exact closed form
γ_pred(τ) = γ₀·cosh(ατ) + (u₀·n)·sinh(ατ) (derived from `thrust.rs`'s exact local boost, α = 2^(thrust_log2+L)),
the frozen gate's work ∫α·v_x·dt against ΔE_N = v²/2 − μ/r, the exact relativistic work
∫√f·(u·n)·α·dτ against ΔE_∞ = γ√f, the register (pt, pt_exp, carry), its constraint violation
p_t − (U_P − H_D), the velocity word's exponent, the event lag, refusals.

Tuned only on the smoke run below β 0.063 (t ≤ 2^30.5, one build check). Everything above that
is held out.

## P1 — the frozen work gate cannot certify the high-c regime (the instrument hole)
The gate's criterion ΔE_N = ∫α·v_x·dt is the Newtonian limit of the law's exact burn; they differ
by γ³ (the law converts Δη = α·dτ to coordinate velocity exactly; the gate's integrand misses the
dt/dτ and the dv/dη factors). Predicted: the relative departure (ΔE_N − work_gate)/work_gate
grows ≈ γ³ − 1, crosses the gate's 3% bound at β ≈ 0.14 (γ ≈ 1.01), and reaches ~10³–10⁴ at the
leave. Control side: the same instrumentation at level 5 over a ≤ 2e-4 c burn reproduces the
gate's PASS (< 3%).

## P2 — the law itself is exact where the gate is blind
γ_pred(τ) matches the readout's local γ to ≤ 1e−4 relative from the smoke regime to the leave.
(If it departs > 1e−4 below β 0.5, my closed form is wrong and the probe is VOID pending
diagnosis — that is the probe's own kill criterion.)

## P3 — where the flight actually stops
No register or word refusal anywhere. The flight ends by leaving the system: the leave radius is
2^40 root units, and with α = 2^−29/tick the coordinate time to cross it gives
sinh(ατ_leave) ≈ 2^(40−29), so γ_leave = √(1 + 2^22) ≈ 2048 (±2%: the start radius 2^30.2 is a
0.2% correction, the initial retrograde velocity a transient of v₀/α ≈ 1.5e4 ticks).
The "flying past γ ≈ 2,000 is refused" wall is the system's edge, not the register, not the word.
Predicted: alive=false at t ≈ 2^40 ticks with the leave/edge loss cause, refusals = 0 throughout,
and NO state anywhere near the i128 register's bounds.

## P4 — the register under a 10⁶× energy growth
pt_exp stays at its birth value (−64) while the binding's velocity word exponent grows with the
speed; the constraint violation |p_t − (U_P − H_D)| stays ≤ 1e−10 (doll units; the quantum is
2^−64); |p_t| ends ≈ c²/2 = 0.5 doll units ≈ 9.2e18 quanta — ~2^67 of headroom left in the i128.
The register was never the binding constraint; its birth-set quantum is fine because H_D is
Newtonian in form (v²/2 caps at 0.5), so the energy it holds never grows with γ.

## P5 — the merge's own assertions hold beyond their tested point (honest uncertainty)
The event lag stays < 2^24 ticks and the step (speed/64/α, capped) grows only to ~2^23 ticks at
β→1, so the burn never lumps between β 0.999 and the leave. I am least certain here: the cap was
tuned where the merge test stopped, and the readout-ahead machinery (the pending kick's ramp) has
never been read at γ > 22. Either outcome (lag holds / lag breaks past 0.999) is a result; the
probe records it.

## What would make each wrong
- P1 wrong: the gate passes above β 0.3 → my γ³ derivation is wrong (then the gate covers more
  than I claim, and the hole is smaller).
- P2 wrong: the closed form departs > 1e−4 → either my form or the law is off; diagnose against
  the flush-by-flush rapidities before claiming anything.
- P3 wrong: a refusal (fault string) before the leave → the wall is a word/register failure after
  all; the γ at refusal and the fault reason become the finding.
- P4 wrong: pt_exp changes, or the violation trends → the birth-fixed exponent is load-bearing in
  a way the docs do not say.

## Commands
- Decisive: `cargo run --release -p emergent-universe --example inversion_highgamma -- 15 41.7`
- Control: `cargo run --release -p emergent-universe --example inversion_highgamma -- 5 28.5`
