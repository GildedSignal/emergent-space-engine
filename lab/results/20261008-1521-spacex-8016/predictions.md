# Predictions (held-out: seeds 2 and 3, never run while tuning; all tuning was on seed 1)

Bench: `bench kick <seed>` and `bench frame <seed>` in this folder (standalone crate, path deps,
no crate edits). The classification re-implements `step::quantize` exactly and is validated by
0 mismatches against the law's own `new_entry` behaviour on seed 1 (818 kicks).

Cloud box is shared and noisy (per-kick µs swung 95→375 between two seed-1 runs); predictions are
therefore about ratios and counts, not absolute times.

1. **Every distinct ship kick fires.** Carried (sub-quantum) kicks: 0 on seeds 2 and 3 as on
   seed 1. The sigma-delta carry engages nowhere in the flying plane (|dv| p50 ~ 2^23 quanta).
2. **The entry heuristic keeps matching**: 0 mismatches on seeds 2 and 3.
3. **The exact-orbit compile is the largest single line of the kick**: compile-only within ±20%
   of from_state (i.e. the Cartesian→element inversion premium is < 25% of the rebind), and the
   rebind (from_state) is 45–65% of total kick process time.
4. **Shareable per-(doll, tick) context is real but minor**: 5–15% of kick time; dedup 2–5 kicks
   per distinct (doll, tick).
5. **Frame split (rtf 100, unlimited budget)**: ship items carry the most event cost (40–60%),
   fleet slices 20–40%, player 10–30%; player per-item cost is 3–10× the ship per-item cost.
6. **|dv| in velocity quanta (log2)**: p50 between 21 and 26 on all seeds.

Kill criteria for my claim: carried kicks > 5% on any held-out seed, or compile-only < 20% of
kick time on any held-out seed. Either kills the "compile is the idiot" story.
