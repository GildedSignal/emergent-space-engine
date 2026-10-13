# Predictions — verdict (written after the runs, 2026-10-13)

1. **fwd15 control: HELD.** No fault through my window (γ 334 at t=1.79e11, cut by my own 55 s
   wall cap, not by the engine); clock_relerr 1.0e-6 at γ 334. (The pin's longer C1 flight already
   reached the leave; my window adds only the γ≤334 tail.)
2. **brake_g30/g300: HALF-HELD, and the interesting half failed.** No death at any E crossing —
   held. But prediction (a)/(b) both missed the actual behaviour: the held retro key brakes
   γ 30.7→1.21 and then **pumps** back up (γ 186 still rising at my window's end, phase=Brake
   throughout). Brake-to-rest by a held key is impossible: rest is a crossing, not a fixed point.
   Clock_relerr ≤ 1.7e-6 through the reversal — HELD.
3. **turnburn15: HELD in substance.** No Range death; γ fell 30→1.19, periapsis blew out to
   2.1e10 M, and the flight survived 69,660 refusals on the old binding. Near-star passage did
   not occur (the turn raised periapsis, not lowered it — my sign expectation was wrong; the
   brake/pump asymmetry of the held key dominates any perihelion-diving intuition).
4. **fwd2_farstar: MISSED (wrongly).** I predicted alive-at-timeout or Range; it died silently
   (`fault=None`) at the leave: the L2 escape settled onto a bound orbit (k>0.5, E=1.000000)
   whose apoapsis passes 2^40. The leave, not the key wall, ends slow far flights.
5. **Domain mechanism: PARTLY.** The E→1 edge compiles everywhere to 1.6e10 M — held. The Q48
   k<2^-29 story for E≥1e4 is WRONG in detail (measured k ≈ 1/periapsis ≫ 2^-29 there, E-
   independent at E≥100: the shape no longer carries E; the gap does). The refusals are jagged
   in (E, peri) and — per the discriminator — every tested refusal point rebuilds and compiles
   the same key via `from_invariants`: the wall is the state→key fit's arithmetic, not the key.
