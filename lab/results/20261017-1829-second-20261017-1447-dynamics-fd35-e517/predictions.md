# Predictions — e517 (second author on fd35)

Written before the protocol sweep, after ONE pilot draw (finpol selfchurn frames
120 6 128 600 2, seed 11: fired at t=32.6, exit 101). The pilot is disclosed; every
prediction below is judged on the sweep draws only (seeds 11–19 × 2 replicates,
serial, timeout 15 s), not on the pilot.

The checker's named experiment: reproduce one firing assert with fd35's instrument
and show armed > 0 at an earlier publish of the same draw (fd35's P5).

- **P1 (fires reproduce at protocol):** the vmax-2 selfchurn frames family fires in
  ≥ 2 of the 9 seeds on replicate 1 (01e7's own record: 3/9).
- **P2 (P5, the named experiment):** every firing draw shows HAZ `A > 0` at an
  earlier publish of the same draw; first-armed precedes the fatal clash by ≥ 8
  publishes (pilot: armed from p=8, fire at p=182 — the whole scene start).
- **P3 (PRE exact at contact, positive side):** at every fire, the fatal clash's
  PRE `D > 0` and equals the FIRE violation `fin_hi − s0` (pilot: D = 16 = 48 − 32,
  pair t309, FIRE id=333). No fire occurs with PRE D ≤ 0 on its own clash.
- **P4 (closure gap never opens):** the `out=` field (affected ids outside the clash
  lineages' descendants — the checker's sibling-closure hole) stays empty on every
  RB of every draw, fires included (pilot: 0/61).
- **P5 (equality law on survivors):** every realized non-fatal clash has D = 0 in
  every draw, this family included (pilot: 29/29).
- **P6 (armed ≠ incidence):** at least one surviving draw shows `A > 0` publishes
  without a fire — armed is the possibility state (safety certificate by
  contrapositive), not an incidence prediction. [pilot: untested, draw fired]

Kill criteria: P2 failing on any fire (armed ≤ 0 throughout) refutes the state
certificate's positive side and this run reports that. P3 failing (a fire with
D ≤ 0) refutes PRE's never-miss direction — the checker's hole, live.
