# Dossier — 20261011-1600-inversion-e128 (lens: inversion)

## Claim (one sentence)

Inverting the newest merge (the i128 energy register + held-burn cap, green at "L15 reaches β 0.999,
no refusal") shows the merge's green test sits inside an ungated, broken regime: the tube's proper
time — the one clock the burn flushes against and the player reads — stops dilating above γ ≈ 2
(measured dt/dτ → 2.0 while the readout γ is 1262), so a held top-level burn reaches γ that its own
coordinate time cannot afford (3.7× too fast already at the merge's green point β 0.999, 112× at the
freeze), the frozen work gate (∫α·v dt, 3%) is unpassable above β ≈ 0.25 and so certifies none of it,
and the flight ends not at the register (exact throughout, |p_t−(U_P−H_D)| ≤ 6.4e−11) nor at the
system's leave (137× farther) but at γ = 1761 in `Space(Range)` — the tube compile of a near-luminal
state during the kick's rebind.

## Bottleneck

The board's "what must be perfect: navigation, knowledge and dynamics" and Julien's "I want the player
to feel what a human would feel in space" (PRINCIPLES 30): the high-c flight is the product, and its
time is the thing the player feels. The queued build `b-high-gamma` (γ to 10⁶) died on a rate limit
with no dossier; the γ ≈ 2000 refusal is listed as a known limit without a cause. This run measures
the shipped law across the whole regime between the merge's green point and the wall. Expected gain:
it re-aims that build — raising the wall without fixing the tube's time map would optimize a flight
whose clocks are wrong by ~γ/2, and it deletes the belief that the register or the word is the wall.

## Evidence (all from the shipped plane, `main` at a838a284; Linux x86, orders of magnitude only)

Probe: `crates/universe/examples/inversion_highgamma.rs` (in this run's patch; it edits nothing else).
It holds a forward burn from the plane's start and reads, at 141 log-spaced checkpoints: the readout
state, the local γ (the same f = 1−2μ/r conversion `thrust.rs` uses), proper time τ (the same
`orbit_state` the view and the flush read), the register and its constraint, the words, the lag.

- **Commands** (each ~5–7 s):
  - `cargo run --release -p emergent-universe --example inversion_highgamma -- 15 41.7` → `work/l15b.csv`
  - `cargo run --release -p emergent-universe --example inversion_highgamma -- 5 27.6` → `work/l5.csv` (control)
- **The burn is exact in τ** (held-out P2, held): γ_pred = γ₀·cosh(ατ) + (u₀·n)·sinh(ατ) matches the
  readout to ≤ 3e−3 relative from β 0.03 to γ 1262; the exact relativistic work ∫√f·(u·n)·α·dτ
  reproduces ΔE_∞ = γ√f − 1 to 2.3% (trapezoid at 141 points). The register is exact (held-out P4,
  held): `pt_exp` −64 from birth to freeze, `pt` → −2⁶³ = −c²/2 exactly, violation ≤ 6.4e−11, zero
  register refusals.
- **The dilation collapse** (the finding): γ(t) against the SR-exact γ_ext(t) = √(1+(αt)²):
  deficit 1.00 to β 0.5, 1.06 at γ 2.2, 1.77 at γ 7.7, **3.72 at γ 24.7 (the merge's own green
  point)**, 14.6 at γ 149, **87 at γ 1262, 112 at the freeze (γ 1761)**. Local Δt/Δτ at the last
  checkpoints: 1.96, 1.96, 2.00 — the tube's time dilation saturates at γ_eff = 2. At γ 1262 the
  flight has burned t = 7.74e9 ticks of coordinate time; relativity affords γ = 14.5 there, and the
  ship's proper clock should read 1.8e9 ticks, not the 4.21e9 the tube reports. The player's clock
  (the view reads the same `orbit_state`) would show the star's frame running 2× fast instead of
  1262×.
- **The wall** (held-out P3, wrong in an informative way): first refusal at t = 8.45e9, γ = 1761.4,
  β = 0.99999984, r = 7.97e9 doll units. The leave radius is 2^40 ≈ 1.1e12 (137× farther; my
  prediction γ_leave ≈ 2048 never happens). Fault: `Some((Kick(0), Space(Range)))` — the range checks
  of the orbit key in `crates/space/src/orbit.rs` ( periapsis/k bounds) during the kick's rebind of a
  near-luminal state. 3630 refusals by t = 1.7e10; the state freezes at γ 1761 (the known "flying
  past γ ≈ 2,000 is refused", now with a cause).
- **The gate** (held-out P1, conclusion held, shape corrected): work/ΔE_N crosses the frozen 3% bound
  at β ≈ 0.25 (measured 1.030 at β 0.247) and is 27× off at γ 1262. Shape: the gate's work grows as
  γ−1 while the Newtonian energy it compares against saturates at c²/2 — the criterion is the
  Newtonian limit of the law and cannot fail more clearly. Control: at level 5 (β ≤ 3.4e−4) the same
  instrumentation gives |work−ΔE|/ΔE < 1e−6 — the gate's own regime, PASS, both sides of the
  instrument covered.
- **The merge's own assertions hold beyond their tested point** (held-out P5, held): event lag < 2^24
  while healthy, the thrust step cap holds (steps 2^18 → 2^22), no burn lumping, until the compile
  refuses.
- Determinism: the first decisive run (`work/l15.csv`, before I fixed a broken column of my own
  probe's work integral) and the rerun (`l15b.csv`) agree on every engine column; the engine was
  never edited.

## Predictions

`predictions.md` was written before the decisive run (tuned only on a β ≤ 0.063 smoke). What
happened: P2 and P4 held exactly; P5 held; P1's conclusion held (gate fails low) but its shape was
wrong (γ³ predicted; actually (γ−1)/(c²/2) — the Newtonian energy saturates); **P3 was wrong**: the
leave does not stop the flight — the tube compile refuses first, 137× short of the leave in r. The
dilation collapse itself was not predicted: I expected the law to be right in coordinate time and
the wall to be the edge; the measurement says the law is right in the tube's τ and τ itself is not
the ship's proper time above γ ≈ 2.

## What would make it wrong, cost of adoption, fit

- **Wrong if** the tube's `orbit_state(t).proper_time` is not intended as the ship's proper time
  (then the view and the flush both misread it, which is still a bug, but a different one), or if the
  root tick is not the star-frame time (the design asserts "one tick is the same physical time in
  every doll", and my γ, τ and the work integrals are doll-invariant across the handoffs the flight
  crosses). The mechanism inside the compile — the weak-field energy map saturating (a state with
  readout γ 1262 compiled as a geodesic of E_∞ ≈ 2, whose time then runs dt/dτ ≈ 2) — is
  [INFERENCE] from the measured asymptote; the integrator can confirm it directly in `crates/space`.
- **Cost of adopting:** none for this dossier (a measurement); the fix it points at is in the tube's
  time map / compile's energy mapping, not the register, and it must precede `b-high-gamma` or that
  build will spend its window raising a wall behind which every clock is ~γ/2 wrong.
- **PRINCIPLES:** 30 — "I want the player to feel what a human would feel in space, it's about
  immersion": the one instrument of that feeling, the clock, saturates at ×2. 2 — "error type over
  error size": a silent saturation is the worst type. 34 — "the oracles are guards, not shepherds":
  the work gate guards only β < 0.25, and the merge's no-refusal test guarded nothing above it.

## The lens

Inversion found this by taking the newest merge and asking what its green test silently assumes: that
"no refusal at β 0.999" means the physics holds there. What the lens may have missed: I measured one
scene (forward burn, no turns, one seed) and read the engine only through its public readouts; the
compile-side mechanism is inferred, not pinned; and the lens's focus on the merge left untested the
reverse burn, the turn keys at high γ, and what the player *sees* (the `seen` shifts and Doppler),
which may be computed from the retarded states and could still be right even while the clock is
wrong.
