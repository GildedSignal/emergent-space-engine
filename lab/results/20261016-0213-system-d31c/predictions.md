# Predictions (written before the decisive experiment)

The run: one shared "planets at t" readout (`PlanetsAt`, armed only inside `Universe::start` by
`ES_PLANETS_AT_T`) serving both read paths of the birth plan pass — `Ctx::secondaries`/`tide`
(the Cartesian projection) and `ext::constants`' `source()` (the element projection) — on shipped
main, `ES_BIRTH_SPLIT` print-only timers aboard. This is nladder's named next rung
(library-cfe5's "one shared readout for both paths", predicted there at ≲13 µs/body).

Cases tuned on: none. The arms are flown before looking only at N=10⁴ seed 1 to shake out build
errors; every number below is a prediction about cases I have not measured.

- **P1 (the cut):** with the memo on, the birth plan pass (`Universe::start`'s replan+apply loop)
  falls to **11–16 µs/body** on this box at N=10⁴/10⁵, seeds 1/7 (from 32.4–33.5 shipped;
  cfe5's secondaries-only hoist reached 22.8–23.2). The difference from 22.8 is the `source()`
  read: I predict it is 6–11 µs/body, i.e. the same order as the secondaries read it mirrors.
  Kill: if pass_on > 20 µs/body the "two paths, one readout" thesis is dead at the belt (the
  source read is not the bill), whatever the digest says.
- **P2 (attribution):** with the memo on, `secondaries` and `constants` drop below **5% of the
  pass** (timer shares), and the remaining pass is per-body math (own-state readout, kepler,
  field, the clock's y/ticks arithmetic) — no further shared-state read path remains. If a
  third read path still holds ≥ 20%, the representation has more than two mechanisms to unify.
- **P3 (identity):** digests after `settle` to a pre-wave cut (3,000 game-s) are **bit-identical**
  across `ES_PLANETS_AT_T` off/on at every N and seed flown, including the held-out seed 11 and
  N=3×10⁴ (never flown by me before this file), and the universe crate's test suite passes with
  `ES_PLANETS_AT_T=1`.
- **P4 (shape):** the memo-on pass is flat in N (10⁴ → 10⁵ per-body change within ±15%, no
  per-N term), matching 404b's flatness of the shipped pass.

Held out before the run: seed 11 at N=10⁴ and 10⁵; N=3×10⁴ seed 1.
