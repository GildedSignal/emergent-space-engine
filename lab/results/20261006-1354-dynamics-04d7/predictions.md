# Predictions — 20261006-1354-dynamics-04d7 (written before the decisive sweep)

Question: how fast does the belt's exact population store (birth program + scars,
`crates/shipmem` form P) grow under the belt's own endogenous stirring — i.e. the
"distinctions created per game-second" that decide whether 10^9 bodies fit in 8 GB?

Only exposure so far (instrumentation pilot, disclosed): seed 7, N=60, hot tier
(gm=1.5e-7), 15 orbits. The decisive sweep is N=300, seeds 0/1/2, tiers gm=0 (200
orbits), gm=5e-8 (2000 orbits), gm=1.5e-7 (800 orbits), snap-every 20, matching
20261006-1029-dynamics-6875's tiers for comparability. Predictions in families:

- P1 (growth law). bits/body(t) at both quanta is neither flat nor linear: it fits
  A + s*log2(t) with s between 0.5 and 2.5 (lambda shear ~ 1 per doubling +
  sub-diffusive a,e), while f_scarred saturates toward 1 as 1-exp(-rt). If it were
  linear in t the program form is dead on arrival; if flat, stirring never creates
  distinctions (control-like).
- P2 (control). gm=0: bpb == 0 at both quanta, k = 0 at every snapshot (the frozen
  belt is exactly its program; also the instrument's zero).
- P3 (floor anchor). per-scarred-body cost at work quanta stays <= 121 bits (the
  components-98bc draw floor) and approaches it — the cost model must not exceed the
  floor it is anchored to.
- P4 (lambda dominates). the lambda column carries >= 50% of behav-quanta bits by the
  end of the mild tier (shear, not element diffusion, is the distinction generator).
- P5 (ruin horizon). work quanta cross 16 bits/body (2 B/body at 10^9) before 10^2
  orbits even in the mild tier; behav quanta cross it between 10^2 and 10^3 orbits in
  the mild tier (so the ruin horizon is game-months at 1-yr orbits, game-days at
  90-min orbits — the quantum, not the stirring, is the lever).
- P6 (no runaway tail). mild tier over its window: da_p90 stays < 0.05 (inside the
  birth band 0.5 wide); the store's growth is bulk, not a few scattered bodies
  (da_max may exceed p90 by an order; reported).
- P7 (write rate does not decay). rowwrites/kicks >= 0.5 at behav quanta throughout
  the mild tier: once a body is scarred, later kicks keep rewriting its row, so the
  seal work per orbit tracks the kick rate even after the bit total saturates.

Kill criteria for my own claim: if P2 fails (control grows), the instrument is broken.
If P3 fails, the cost model is wrong, not the physics. If bits at behav stay < 2 bits
over the full mild window, "ruin" is empty and the dossier reports the program form as
robust instead.
