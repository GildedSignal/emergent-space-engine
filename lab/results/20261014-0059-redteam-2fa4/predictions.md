# Predictions (written before the decisive run)

Attack: representation.md §2 "Observables are emergent … −p·u *is* the colour … Its
direction in the observer's frame *is* the aberration" — as shipped, three readout
seams compose velocities/rates non-relativistically. The lens target is #5 (the view
gathered at the past light cone); the page's named unmeasured hole is "moving
observers, the seen/Doppler instruments".

The three seams (view.rs / observe.rs, quoted by line):

- S1 **fleet members** (`view.rs:395-399`): a member's clock rate is
  `rate0 · √(1 − 2μ/r_doll)` — the planet's rate times the gravitational lapse at the
  member's radius. The member's own kinetic factor √(1 − v²) never enters (for every
  non-fleet body it does, via `state_rate`'s `√(f − v_r²/f − v_t²)`).
- S2 **nested-doll Doppler numerator** (`observe.rs:272` `vel = vel + v`): the
  root-frame velocity used in `(1 − n·vel)` is a Galilean sum up the doll chain, while
  the rate denominator is composed exactly (`rate /= 1 + v·vb`). Binds only for a
  depth-2 body with fast levels (the handoff page's "fast grandchild", extended from
  keys to seen values).
- S3 **a burning observer** (`view.rs:288` `vo = vo + dv`): the owed burn is added to
  the observer's velocity Galilean (the clock side `clocks_with` re-derives the rate
  with dv in the chain, so only the colour numerator/aberration use the Galilean vo).
  Exact in the root doll (one level); binds only nested + burn.

## Held-out predictions (not tuned on)

1. **The body path is exact (the premise survives where it is flown).** On the
   `stream` scene (B15's own scene class: bare straight tubes at 1e8 root units,
   gravity ~2×10⁻⁸), with the observer at 0.9c and emitters at 0.9c in every geometry,
   the shipped `Seen.shift` and `Seen.direction` agree with an independent closed-form
   SR oracle (my own crossing solve + Doppler/aberration, written from the scene's
   analytic worldlines, not from the engine's readouts) to **better than 10⁻⁵ relative**
   (shift) and **better than 10⁻³ degrees** (direction). If this fails, the finding is
   bigger than predicted: the exact path is not exact.
2. **S1's error is γ(member), not a subtler mix.** The shipped fleet rate exceeds the
   true member rate by exactly γ(β_m) (no cross-term with the planet, because the
   member's velocity enters nowhere in the rate), so `shift` is high by γ and
   luminosity by γ⁴: **1% colour at β_m ≈ 0.14, 5% at 0.31, 40% at 0.90; luminosity
   −4× that at each point** (γ⁴). The plane's flown battle speed (2⁻¹⁵ c ≈ 3×10⁻⁵)
   sits at 5×10⁻¹⁰ — invisible today.
3. **No rung, gate or example judges a seen value.** `r6` is cost-only; B7 judges
   bodies' derived rates; every view example (`view_rel`, `view_cost`, `tail_view`)
   counts readouts, none compares `Seen` values to an oracle. (Literature check, not a
   run: verified by reading `docs/law.md` and `crates/universe/examples/`.)
4. **The engine's own contact-law domain makes S1 reachable**: `es-lattice-relativistic-v1`
   is tested at β 0.3–0.9 (contact-carry's page), so relativistic members are
   in-domain for the law while their seen colour is Newtonian — the dense order is
   exactly where the emergent-observable premise is computed least relativistically.

## What would make the attack fail

If (1) holds at ≤10⁻⁵ and no seam crosses 1% inside any domain the engine supports,
the premise "observables are emergent [and exact]" survives entire, and the dossier
reports that with the numbers — a survivor is worth reporting.
