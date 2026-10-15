# Predictions (pre-registered before the decisive run)

Written after reading the shipped code (`crates/lattice/src/relativity.rs:236`, `law.rs:336/598`,
`chronon.rs`), before running any probe. Not tuned on any probe output.

## The claim under test

`docs/representation.md` §2: "Contacts use the exact integer special-relativity law
(`es-lattice-relativistic-v1`), in the frame of one of the two bodies."

## Closed form derived from the code (the prediction)

Detection (`hit`, bin predicate) fires in the first bin whose window intersects the reach
interval, for an approaching pair; the responder (`resolve_law`, both laws, `relativity.rs:236`
/ `law.rs:598`) skips any pair with `dot(d_end, w) >= 0`, where `d_end` is the separation at the
bin's end. With first-touch time `u` (in chronons, from the detection bin's start) and
`ρ = effective reach / |w|` (effective reach = √(reach² − b²), `|w|` the coordinate closing rate
in position quanta per chronon):

- **skip (no impulse, ever) ⟺ frac(u) + ρ ≤ 1** (closest approach inside the detection bin);
- so at a fixed ρ the pass-through probability over arrival phases is **max(0, 1 − ρ)**;
- equivalently the pair ghosts when its closing speed exceeds **its effective contact depth per
  chronon**: `|w| ≥ effective reach`, i.e. on the fleet lattice (Q = 2²⁰, 1 lattice unit =
  2⁻²⁰·1.477 km = 1.409 m, chronon = 4.925 µs) `v* ≈ reach_m × 2.03×10⁵ m/s`.

## Held-out cases and what I expect there

1. **Boundary grid** (equal masses, head-on, b = 0, ρ × first-touch phase α = frac(u) swept):
   measured exchange ⟺ α + ρ > 1, on the shipped reference stepper (`Chronon`,
   `Law::RelativisticV1`, Q = 2²⁰), at every point, independent of reach and |w| separately.
2. **Scale invariance**: the boundary depends only on ρ, not on reach, |w|, or mass separately
   (two arms with the same ρ, reach 7 vs 709 quanta ≈ 10 m vs 1 km, agree).
3. **Game thresholds** (50% ghost at ρ = 0.5, i.e. closing speed 2× the depth per chronon):
   - 0.5 m missile + 50 m ship (reach 50.5 m ≈ 36 quanta): β* ≈ 3.4×10⁻² c — at the game's
     design speed (~c) it never collides;
   - 5 m + 5 m ships (reach ≈ 7 quanta): β* ≈ 6.8×10⁻³ c (≈ 2,000 km/s);
   - 50 m + 50 m (reach ≈ 71 quanta): β* ≈ 6.8×10⁻² c;
   - belt conjunctions (~km/s ≈ 10⁻⁵ c): ρ ≫ 1, exchanges fine — but contacts there are
     near-absent anyway.
4. **Positive control** (ρ = 5, α = 0.5): equal-mass head-on pair exchanges by swapping
   velocities exactly (the v1 reflection), `rev` increments on both bodies.
5. **Negative control** (ρ = 0.05): Contact detected, both velocities and revisions unchanged,
   and no exchange in 200 later chronons (the consumed bookkeeping never re-fires a receding
   pair).
6. **The 0.9c content** ("the stream of B15's scene at 0.9c is the content the game exists
   for"): every ship-scale contact in that regime is deep at ρ ≪ 10⁻² — no collision the player
   can cause by ramming at high c lands.

## What would make this wrong

- The responder resolves mid-bin crossings some other way (no skip at τ* ≤ 1): falsified by
  control 5 exchanging.
- The boundary depends on reach or |w| separately, not just ρ: falsified by arm 2 disagreeing.
- The stepper's detection bin differs from my reading (e.g. detection requires the pair still
  approaching at the bin's end too): then fast pairs would not even be logged, which is a
  different (worse) failure — I check the Contact event/`encounters`-equivalent log too.

## Rung audit (predicted before the run)

- r5 (dense order, frozen at engine Q): its scenes are exchanging contacts by construction
  (contact-carry measured per-contact energy bookkeeping ≠ 0), i.e. ρ > 1 arms only — the skip
  regime is outside its grid. It judges bit-identity between orders, both of which skip
  identically. Prediction: **no rung, gate or engine test sees the skip** (chaos-shadowing's
  own audit found the same for the ledger).
