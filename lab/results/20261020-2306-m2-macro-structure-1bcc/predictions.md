# Predictions — 20261020-2306-m2-macro-structure-1bcc (written before the decisive probes)

The two representations under test (see dossier for the derivation):

- **R1, the fibration**: the belt as N bodies fibred over F occupied cells of a coarse
  orbit-key base; one kick stream (one full rebind, the 43–53 µs law-dominated term) per
  cell per epoch, members apply the shared integer delta and fork out at the measured
  straddle rate. Moves the kicks row (~10³ at stake) and the families row together.
- **R2, the lattice wheel**: the belt's event times are integer ticks on one dyadic root
  lattice (steps are powers of two anchored on multiples); the schedule's information is
  the set of occupied (tick) buckets, so the calendar is a timing wheel, not a per-body
  store. Moves the scheduler's 156 B/body (the calendar row's measured constant).

The unmeasured number both hinge on: **F(b)** — how many distinct orbit-key cells the
shipped belt actually occupies, at the law's own 11+11-bit memo grid and at coarser
widths b, and whether the occupancy survives real kicks.

## Predictions (each falsifiable by the probe below)

- **P1 (the shipped memo grid is belt-saturated):** at N = 10⁶ belt births, distinct
  `MemoCode` cells F(0) ≈ 0.2–0.5·N (the [2,3) AU × Rayleigh-e band spans ~2⁷⁰⁰ · 2¹·²
  cells at 11 relative bits per axis; occupancy per cell ~0.3). So "the memo cell is the
  family" is FALSE as shipped: the belt needs a coarser family word by several bits.
  Kill the other way: if F(0) ≤ 0.01·N the shipped grid already families the belt and
  R1 is adoptable at the law's own width (a stronger result).
- **P2 (a coarsening exists that pays ≥ 50× with the fork rate bounded):** F(b) falls
  roughly 2^(−2b) (two independent axes) until it saturates at the occupied band's cell
  count (order 10²–10³ cells at 4–6 fraction bits). I predict a width b ≤ 6 with
  F(b) ≤ 0.01·N at N = 10⁶; at that width the per-cell spread δx (dominated by the
  phase ring, ~10⁸ root, not by δa) keeps the a877 fork rate at w11 near the measured
  belt ring value (~1%/kick), so the composed kick cost ≈ (F + fork·N)·refit is
  ≥ 50× under the shipped per-kick cost. Kill: no b ≤ 6 reaches F ≤ 0.01·N, or the
  measured occupancy is so heavy-tailed (a few cells hold everyone) that the ring
  differential is irrelevant and the real fork driver is elsewhere.
- **P3 (cells survive kicks; exact keys scatter inside them):** in a flown plane
  (N = 10⁵, real frames), the belt's per-body exact `OrbitKey`s scatter under the shipped
  61-bit word (every kick splits streams — a877's mechanism), but the 11-bit cell
  occupancy F(t) stays flat (kicks move keys by far less than a cell width), and
  `catalogue_live` grows only with distinct bindings. Kill: F(t) grows ≥ 2× over the
  flight (the cells themselves churn — the fibration's base is unstable and R1 dies at
  belt scale regardless of word width).
- **P4 (the schedule is already a wheel wearing a calendar):** the belt bodies' pending
  event ticks cluster on few distinct values (the doll's shared grid, stagger or not):
  distinct pending ticks ≪ N (I predict ≤ a few hundred at N = 10⁵, and the tick
  histogram's support is dyadic — tick values divisible by large powers of two). The
  calendar's N-entry store then carries ~log(tick)-scale schedule information. Kill:
  distinct pending ticks ≈ N with one body each (phases fully de-synchronized; a wheel
  degenerates and R2's memory claim dies).

## The probes

- `cargo run --release -p emergent-universe --example fibers -- draw 1000000` — the birth
  census, no engine population (keys computed by the law's own `OrbitKey::bound` +
  `MemoCode::encode` on `ladder_ship`'s exact draws): F(b) for b ∈ {0,1,2,3,4,5,6},
  occupancy histogram, exact-key control.
- `cargo run --release -p emergent-universe --example fibers -- flight 100000 10 2000` —
  the flown census: distinct cells, exact keys, catalogue_live, kicks, and the pending-tick
  histogram over real frames at N = 10⁵.

Controls: the exact-key census (must be ≈ N: births are distinct orbits — if not, the
draw path is wrong); the base plane at extra = 0 (the belt ids must match
`ladder_ship`'s; the census must be empty of non-belt bodies).
