# Dossier — run 20261005-0543-redteam-6254 (lens: premise red-team)

## Claim

The design's "both orders give identical bits" premise is unsupported where it is most
loaded: the contact law resolves same-epoch pairs sequentially and is order-dependent at
O(1) (the repo's own integer law reverses a body's velocity outright between two legal
orders), same-epoch pairs sharing one body are 22–82% of all contacts at *every* density,
the design abolished the global tick that made the old batch rule well-defined and
replaced it with a slack-ordered one-at-a-time queue, no canonical same-epoch order is
stated anywhere, and neither r5 nor B8 contains the case — one flipped window rewrites
88% of a 1500-body gas, so replays fork whenever the engine flips a region between orders.

## Bottleneck

Board item 0 (the representation) and B8 (determinism). Not a speed gain: this is a
correctness premise of `docs/representation.md` §3 and `docs/law.md` line 42. What it
deletes if unfixed: the replay/history promise ("history being made and learning from it",
OC#4) and the law's own definition of exact ("bit-identical on every machine, thread
count, evaluation order (sparse or dense)", law.md line 7). Fixing it deletes nothing; it
costs one sentence in law.md plus two r5 scenes.

## Evidence

All commands ≤ 6 s. The Rust example is in this run's patch at
`crates/lattice/examples/order-falsifier.rs`; the gas script is `exp_gas.py` in this folder.

1. **The repo's own law is non-commutative.** Three equal bouncers, body 0 at rest, two
   approaching from opposite sides at the same epoch (both pairs pass the responder's
   approaching test; this `respond` is the one code path "every mode calls, never a law's
   function directly"). `cargo run --release -p emergent-lattice --example order-falsifier`:

   ```
   law Newtonian:      order [(0,1),(0,2)] -> k = [[-8192,0],[0,0],[ 8192,0]]
   law Newtonian:      order [(0,2),(0,1)] -> k = [[ 8192,0],[-8192,0],[0,0]]
   law RelativisticV1: (same two outcomes, worst per-component |dk| = 16384 = 2·|k|)
   ```

   Not rounding: which body carries the velocity inverts. `law.rs`'s own doc says why:
   "sequential impulses (each pair starts from the velocities earlier pairs left)".

2. **The case is common, not exotic.** `python3 exp_gas.py` (P2), 1500-disc gas, one
   window = one cell-update, cell = 2R:

   | events/cell/window | 0.011 | 0.024 | 0.067 | 0.168 | 0.478 |
   |---|---|---|---|---|---|
   | same-epoch pairs sharing a body | 22.5% | 31.2% | 43.9% | 58.1% | 82.3% |

   At 100× sparser than the design's Knudsen ≈ 1 threshold (the sparse regime proper),
   nearly a quarter of contact pairs already share a body.

3. **One flipped window compounds.** Same gas, order flipped in exactly one window
   (window 120 of 240), canonical order everywhere else: diverged bodies 1.4% after 1
   window, 19.2% after 40, **87.7% after 120**; final median |Δv| = 1.23 × median |v|.
   A mode-switch divergence is not local; it rewrites the history (principle 13).

4. **The rule that fixes this exists only in the tick world.** `lattice-event/src/lib.rs`
   line 42: "All events at tick t form one batch: pairs sorted by index, bodies by id";
   `lattice-metal/src/gpu.rs` line 556: components with "bodies by id and its pairs
   sorted, as the reference does for the whole batch". The new design says "There is no
   global clock" (representation.md §1 Time) and "Sparse order: jump to the earliest
   broken certificate, resolve it, notify the dependents. One queue, ordered by slack"
   (law.md line 40) — singular "it", slack-ordered, no batch, no canonical key. `lab/rungs/`
   contains no r5 and no r6 at all, and B8 (engine tests, unfrozen) names no same-epoch
   multi-contact case and no mid-history order flip.

## Predictions

`predictions.md` was written before all runs. P1 held exactly (both laws, O(1)
reversal). P2 held with margin (predicted ≥ 5%, measured 22–82%; the Poisson cell-level
26% figure was replaced by the more relevant pair-level measurement). P3 held in kind,
not in speed: the cascade compounds to 88% but took 40–120 windows, not the predicted
O(10) — reported as partially held.

## Ranked attacks (each with the rung that should have caught it)

1. **Bit-identity of the two orders (premise 4) — decisive, above.** Catcher: r5, which
   the design names in §7 and which does not exist; B8 would catch it only if given the
   3-body same-epoch case and a Knudsen-crossing scene that flips orders mid-history.
   **Fix:** one sentence — same-epoch events touching a common body form one batch,
   resolved in the law's canonical order (cell key, body id, partner id — lattice v1's
   batch rule lifted from the global tick to the cell-update: a body lives in one cell,
   so its same-epoch events are all in that cell's update; a cross-cell pair belongs
   canonically to one of the two cells). Slack orders lookahead, never application.
2. **The view gather (premise 5) — survives, with a proof the docs lack:** for any tube,
   d/dt[c(t_f−t) − r(t)] = −c − ṙ < 0 strictly (|ṙ| < c), so exactly one crossing per
   tube and Newton from a stale seed cannot root-steal; only convergence cost under hard
   burns is open. Catcher for the cost: r6 — also missing from `lab/rungs/`.
3. **Two-body doll at 1PN (premise 1) — survives:** ν ≤ 1/4 structurally, so B11's
   ν ≤ 0.25 spans the entire possible range, and ν-in-energy-map-only at 1PN is the
   Buonanno–Damour result; the p < 20 strong-field window is plunge/absorption
   territory. Gap: no gate covers each *member's* proper-time aging in a binary (B7 is
   single clocks).
4. **Cost table's kick rate (premise 6):** 6×10⁴ kicks/s for 10⁹ ships implies one kick
   per body per ~4.6 h regardless of scene; any region whose neighbour moments churn per
   orbit (a belt, a fleet) implies one kick per body per orbit, ~10²–10³× more. No rung
   measures kick rate against local density. Catcher: a B15 scene with a dense belt
   (none exists).
5. **Binet cells as rotations (premise 2) — already dead in-house:** the in-band map
   "carried a first-order slope error in every cell holding a turning point" and was
   replaced by `space-darwin16-v1` (law.md line 20); the surviving core (memo keyed by
   (E,L), cycles repeat exactly) is sound. Residual: same-key orbits freeze relative
   drift, bounded at ~10⁵–10⁷ orbits (below player visibility) — noted, not a kill.

Principle tensions: the fix above restores principle 22 ("the simulation tells us what
is next not us, subtle but deadly" — as written, slack priority decides same-epoch
physics); the dense order's lockstep is a tick against principle 14's letter but not its
spirit ("no work for no reason" — everything changes every tick there), one line, no
action.

## What would make it wrong

If the design intended "earliest broken certificate" to carry lattice v1's batch rule
implicitly and slack to order only lookahead, then the code needs nothing and the finding
reduces to "write the sentence" (silver, not gold). The measured non-commutativity would
be moot only if same-epoch events on one body were unreachable — they are 22–82% of
pairs. The cascade number is float and law-agnostic; the integer demonstration (item 1)
is the repo's own responder.

## Cost of adoption

One ordering sentence in law.md; r5 gets two scenes (same-epoch 3-body double contact;
Knudsen-crossing flip mid-history, digest vs a single-order run). The canonical key and
the per-cell batch are already implemented in the tick-world crates; the only new
derivation is cross-cell pair ownership, one rule.

## Fit with PRINCIPLES

- Against: "basically we don't want errors that can compound that's the goal" (13) — one
  flipped window diverges 88% of a gas; "the simulation tells us what's next not us"
  (22) — slack order deciding same-epoch outcomes is us, not the simulation.
- For the fix: "Exact means bit-identical on every machine, thread count, evaluation
  order (sparse or dense)" (law.md) is only reachable through a law-owned batch order.

## The lens

A red-team sees failures where the text is silent; silence may be a plan the integrator
already holds (the batch rule is two sentences away in lattice-event). I checked the
crates before claiming the hole, and measured the common case rather than the exotic
one — but I did not run the full engine to see whether `lattice-event`'s calendar already
feeds `respond` whole batches per epoch in a no-tick configuration; if it does, the gap
is documentation plus r5, not code.
