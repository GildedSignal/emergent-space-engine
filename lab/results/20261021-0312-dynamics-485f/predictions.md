# predictions — 20261021-0312-dynamics-485f (carry ledger + rattle structure)

Question 1 (the page's named leftover): does the per-body contact carry (`Body.residual`,
`Body.carry`, the sigma-delta rounding feedback of the shipped response) sit on a bounded
attractor, random-walk, or drift — at storm rate and in the terminal rattle?
Question 2 (the page's engine question): is the standing rattle a gas of many persistent
partners or a set of decoupled pairs (the compiled/deferred-response case)?

Calibration in hand (smoke, s1 to 8192): first contacts t≈4608, storm onset; per-contact
energy errors are FAR below the velocity-quantum scale (res_max ~2×10^5 after ~200 contacts).

Cases not tuned on (the decisive arms run after this file is written; smoke stopped at 8192):

- **P1 (walk law):** through the storm, Σ|residual| grows like contacts^α with α ∈ [0.4, 0.6]
  (random walk with mixing partners). If α ≤ 0.15 after 10^5 contacts, or Σ|residual| stations
  while contacts keep flowing, the bounded-attractor reading wins and P1 is refuted.
- **P2 (rattle regime):** after the quench (t > ~60k), per-body |residual| of hot bodies
  STATIONS or oscillates (persistent partner sets re-feed the same carries): mean |res| over
  the last 16k is ≤ 2× its value at 70k while contacts keep accumulating. If it keeps walking
  with the same storm exponent, the rattle does not bound the ledger and P2 is refuted.
- **P3 (bias):** |Σ residual| (signed, energy withheld) stays < 10% of Σ|residual| at every
  snapshot: the ledger is unbiased, no drift direction. Refuted if |Σres|/Σ|res| > 0.5 late.
- **P4 (rattle structure):** ≥ 90% of window contacts involve bodies with ≤ 40 distinct
  partners per 64-ch window; top single pair < 5% of window contacts; hot bodies' median
  partner count ≥ 10. Reading: the rattle is a crowded overlapping gas (many-partner), not
  decoupled two-body oscillators. Refuted if median partners ≤ 3 or top pair ≥ 20%.
- **P5 (i64 headroom):** max |residual| and max |carry_c| over the whole arm stay < 2^42;
  the i64 ledger has ≥ 2^21 headroom. Refuted if anything approaches 2^50.
- **P6 (momentum mirror):** the momentum carries behave like the energy carry (same exponent
  class, no separate instability).
