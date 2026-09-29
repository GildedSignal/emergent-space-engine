# Representation: one structure, one law, one number type

Status: **DRAFT** (29 September 2026). This synthesizes Julien's direction from 29 September; see the [register](PRINCIPLES.md) and bottleneck 0 on the [lab board](../lab/board.md). It supersedes nothing until its cheapest falsifier has run and Julien says yes.

## One structure: spacetime as nested frames

- **Spacetime is a dyadic tree of cells (sheets).**
  - A cell's size is a fixed function of the local spacetime gradient only: κ × the curvature length.
  - Collisions never refine the tree. Its shape therefore encodes the gradient to within a factor of 2, almost for free.
- **Each cell is a small freely falling frame,** where special relativity is exact.
  - It stores its connection to its parent: the clock rate (the potential, which adds up across sources) and the flow (the velocity of space, derived locally from the clock rate).
  - Both are stored as small remainders. The cell's level acts as their shared exponent.
- **Cells hold the integer mass moments of everything inside them,** ships' aggregates included.
  - Geometry is a local rule of the moments.
  - A change travels at most one cell per update.

## One law

- **c is native.** An influence moves at most one cell per cell-update, and a cell's time unit is its light-crossing time. Light cones are cell adjacency.
- **Bodies are tubes relative to their cell's frame.**
  - Inside a cell, a tube follows the cell's exact local solution: a straight line when the cell's content is a constant flow.
  - At a joint, the crossing rule conserves what the static field conserves (energy, and momentum along the joint). The crossing is a refraction, not a step.
  - Orbits, turning points, precession, lensing and horizons emerge; none is imposed.
- **Clocks** read the length of a tube measured against the local flow, derived only when asked.
- **Decisions are the only kinks in tubes.**
  - AIs are deterministic parts of the law. An AI is recomputed only when what it sees crosses its perception threshold.
  - The player is the only seed.

## One kind of step

A step is a certificate: the interval over which a description reproduces the law.
- The engine has one error budget: at most one floor unit at each event, carried forward so that errors never compound.
- Shortcuts reproduce the law exactly wherever possible, as Hashlife does. Simplifications then add speed, never error.

## One number type

- **32-bit integer words everywhere.**
  - Products are 32×32 → 64-bit hi/lo pairs.
  - Wide numbers are built from 32-bit limbs, only at rare events on the CPU.
  - A unit that cannot compute this exactly stays advisory.
- **A position** is two 16-bit offsets inside its cell: one word.
- **A velocity** is relative to the cell's frame. Its number of bits is set by how long its certificate lasts.
- **A time** is relative to the cell's epoch.
- **Only one floor is chosen:** the finest spatial distinction the player can see (the early-cinema frame rate). The time floor follows from c = 1.

## Contacts

Contacts get a separate structure, built on demand where the swept regions of two tubes may overlap. It lives in cache and is discarded after use. The exact integer lattice law (`es-lattice-relativistic-v1`) resolves contacts inside it.

## Memory and the allocator

- **Memory layout.**
  - Cells are laid out along a space-filling curve, in causal order.
  - A cell's bodies are contiguous packets (the M1 has 128-byte cache lines and 16 KB pages), so the causal frontier sweeps memory in order.
  - Stars and fleets stay generators or families until an event singles one out.
- **The allocator** is one queue: each cell's next event and deadline, ordered by slack.

## Weakest joints (test first)

1. **Accuracy per crossing.**
   - Weak-field precession and turning points under piecewise cell content: constant, linear, or multipole.
   - Angular-momentum drift on a Cartesian grid.
2. **The many-source rule.** The clock rate adds up and the flow is derived locally; it must pass 1PN for two bodies.
3. **Crossings between cells of different levels,** within the error budget.
4. **Moving sources.** Energy exchange must be physical (gravity assists), not numerical.

## Cheapest falsifier (draft; kill criteria frozen before the run)

- **The model:** a float model of one static mass.
  - Dyadic cells sized by the gradient; sweep κ.
  - Cell content of order 0 and order 1.
  - Refraction at joints.
- **Judged by** the behaviour gates of [gravity-law.md](gravity-law.md):
  - precession at p = 20M and 1000M;
  - E = 1 capture at L = 4M;
  - deflection of light from r = 10⁴ M;
  - energy and angular momentum over 10⁴ orbits;
  - crossings per orbit.
