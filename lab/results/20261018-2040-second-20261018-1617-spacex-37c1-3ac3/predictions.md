# Predictions — 20261018-2040-second-20261018-1617-spacex-37c1-3ac3

Written before any probe arm, sweep or flight ran (the code compiles and the crate's
shipped tests pass — that is all that has been observed). The experiment is the one the
checker of 20261018-1617-spacex-37c1 named for gold: 6362's closed-form root normal on the
shipped v1 operator, at a ship-scale-radius lattice scene — contact-speed open direction 1's
adoption gates (a) and (b), with 37c1's shipped arms as the negative controls and its
resolve-window rate (~0.1–0.2/ρ) as the plane-scale context.

The fix under test: at the receding gate (d·w ≥ 0), fire when Δ = |w|²·reach² −
(|w|²|d|² − (d·w)²) ≥ 0 and resolve through the shipped `exchange` machinery with the
quantized root normal n = (P << k) − S·w (k ≤ 20 bits, one u128 isqrt). The oracle: the
same machinery over a 48-bit root normal (one big-integer Newton isqrt). Δ < 0 keeps the
shipped skip bit for bit.

- **P1 — gate (b), the frozen criterion arms.** On every driven crossed-in-bin ship-scale
  arm (reach 512 and 1024 quanta, closing β 0.5/0.9/0.99, lateral offsets b/reach ∈
  {0, ¼, ½, 39/40}, crossing phases s* ∈ {0.1, 0.5, 0.9}, masses (1000,1000) and (1000,1)):
  the shipped rule skips (contact logged, both velocities unchanged — 37c1's ghost); the
  miss control b = 21/20 is never detected; the fix exchanges with recovery ≥ 99% and
  angle ≤ 5×10⁻³ rad against the oracle. The equal-mass head-on 0.9c arm is the exact
  integer velocity swap (recovery 100.000%). Worst recovery where predicted: the most
  grazing arm (b = 39/40) at the smallest reach.
- **P2 — gate (a), the composition.** The toy's shared-reflection guarantee carries to the
  shipped 4-normal Householder composition: over 20,000 random adversarial receding bin-end
  states (half ship-scale reach 256–2048, half the battle window 1.1–2.1×10⁶, |w| to 0.63Q,
  masses 1–4): zero classification disagreements (Δ ≥ 0 ⟺ the oracle's root exists),
  w·P = 0 exact on every pair, recovery min ≥ 99%, angle max ≤ 5×10⁻³ rad.
- **P3 — the ship-scale gas.** 200 bouncers, radius 256–512, in a box, 300 chronons,
  velocity scales 0.15Q and 0.45Q (closing to ~0.9c). Prediction: at fix off the pure-ghost
  fraction of contact chronons is ≥ 90% (ρ = reach/|w| ≪ 1 — the driven-pair law's regime,
  where 8144's law says nearly every detected contact ghosts); at fix on it drops below 5%
  (the residue: Δ < 0 after mid-batch velocity changes), every ledger stays exact, the world
  stays subluminal, and every PAIR line recovers ≥ 99% against the oracle.
- **P4 — the flown plane (37c1's record, fix on).** ship400 at the shipped speed (0 ghosts
  in 37c1): fix on fires nothing, the benchmark digest is bit-identical to fix off. sd2
  (12.2% ghosts in 37c1, seed 1): the census is identical to 37c1's up to the first fire,
  then fires convert ghosts into oracle-matched exchanges (recovery ≥ 99%); the dense arm's
  census with the fix on is `cmp`-identical to the sparse arm's (the fix preserves the
  steppers' bit-identity — it sits inside the shared resolve).
- **P5 — the contamination split (held out against 37c1's numbers).** At 400 members the
  fires with τ* < −1 (mid-batch-contaminated, the resolve instant bent by an earlier pair in
  the component) are ~10% of fires (37c1: 5/46 skips had τ* ≤ −1). These fire on the current
  integers' linear root; the oracle shares that approximation (the kinked path is not
  recoverable from the gate's integers), so they are reported separately, not folded into
  the recovery headline.

**Kill criteria.** Any gate-(b) arm with recovery < 99% or angle > 5×10⁻³ rad kills the
adoption claim (the composition does not carry the toy's guarantee — a real result, it
would confine the closed form to the Newtonian operator). Any ledger imbalance or subluminal
violation after a fire kills it outright. A fire on a miss control, or digest drift on the
no-ghost plane arm, kills the no-op/control claims. Ghosts remaining at fix on in the gas
beyond the Δ < 0 residue would mean the firing rule is incomplete (a naming, not a kill, if
each remaining ghost has Δ < 0).

**Not claimed.** No adoption here (the integrator freezes rungs; this run supplies the
frozen scene's integers and its measured verdict). Positions stay at the bin end (the root
tick's ≤ 2-quanta offset is a schedule choice, 6362's P4). The plane at today's speeds
needs no fix (37c1's result, unchanged); the fix is for the ship-scale/missile regime and
the day fast crossers fly in the lattice frame.
