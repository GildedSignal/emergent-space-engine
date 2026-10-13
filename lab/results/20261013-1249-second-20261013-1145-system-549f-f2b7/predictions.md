# Predictions (written before the decisive runs; run order disclosed)

Run order so far (all recorded in the dossier): wiring v1 (the free word, written at the kick,
`a(B − len/2)`) is built and its gate outcome is already known — it FAILS the three frozen readout
gates of `tests/motion.rs` (across-boundary velocity jump 5.07e-2 vs the 1e-4 bound; the 3× map-ratio;
the step-squared fall), while `the_readout_between_kicks_is_bounded` (2e-3) and the clock gates pass.
That is a measurement, not a prediction; the predictions below are for the runs not yet made.

## P1 — the fresh word (v2: written at `boundary_clock`, `a(B)`) passes the readout gates.

The word the census priced is the freshest possible; its error is the census's (median 2.8e-10,
max 3e-9 plain, 1e-8 dive), far under every gate. I predict all four readout gates of `motion.rs`
pass, and the clock gates stay green (the law is untouched: the word only rides kick records).
Kill: any gate fails — then the stored word cannot serve the readout at any write point, and the
549f claim dies in its strongest form.

## P2 — digest identity holds for both wirings.

The Kick record is not hashed into the digest and `observe` never writes (the lib test holds), so
v1 and v2 digests match the shipped tree bit for bit on the three census flights.
Kill: any digest differs — the word leaked into the law.

## P3 — the frame gain on the shipped bench.

51bf measured the per-read field evaluation at 81% of the readout, the readout at 97% of the
crossing loop, the crossing loop at 95–97% of the gather. I predict the wired gather (from-scratch
and memo) drops by 40–60% per emitter on `view_cost` (not the full 81%: the second tube decode at
the mid stays deleted too, but `secondaries`' doll-chain walk is only part of the per-read cost;
the `base.cartesian(t)` decode remains). The multiplicity census (reads per window per body) I
predict is 2–6 on the plane at rtf 100 — the write amortizes.
Kill: the gain is under 20% — then the deletion 7b86 priced is not where the row's time is, and
the word buys the view nothing.

## P4 — the strong-field cadence (the engine CAN host it: a 2^-4-solar doll with a 1 M surface;
doll units normalise GM = c = 1, so r = 20 M is periapsis 20, beta_circ 0.224).

The clock's step rule (dt/ds = f'(H_D + p_t + c) on the constraint, i.e. f'(U_P + c)) depends on
the PERTURBING potential, not the central field, so I predict the steps do NOT shorten as the ship
descends: the window stays the doll's `ds·f'(c)`-scale — about P_moon/128 in the moon's period —
which at r = 20 M is ~2 ship orbits per window. Then the word is stale by whole orbits and its
error is the term's own size or larger (Delta-a/a of order 1), and the word at r <= 20 M needs a
refresh the plane's law does not give — unless the read gate (tau <= 2 len) sends those reads to
the raw tube, in which case the term is dropped exactly where 7ab4 says it is visible.
Kill (the other way): if the steps DO shorten (Sundman through H_D), the word holds and the
strong-field caveat dies.

## P5 — the boundary write's price.

One field evaluation per step at `boundary_clock` (it runs none today): the law's field
evaluations go from 1 to 2 per step per clock-stepped body. I predict this is still a net win
on the bench (P3) because reads per window exceed 2 on the plane, but it is no longer free —
the 549f dossier's "write costs zero extra field evaluations" holds only for the failing v1.
