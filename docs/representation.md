# Representation: one structure, one law, one number type

Status: **DRAFT** (29 September 2026). This synthesizes Julien's direction from 29 September; see the [register](PRINCIPLES.md) and bottleneck 0 on the [lab board](../lab/board.md). It supersedes nothing until its cheapest falsifier has run and Julien says yes.

## One structure: one grid, with the coordinates chosen per doll

- **Coordinates and grid are one choice.** Pick the coordinates in which the local field's symmetry becomes a translation. In them the grid is always the same thing: a uniform square lattice of cells with a fixed number of bits each.
  - Cell boundaries then follow the symmetry, so each crossing conserves exactly what the field conserves (Noether): energy when the field is static, angular momentum when it is central.
  - A 2D position is a complex number z. Rotating and zooming multiply z, and the logarithm turns those multiplications into additions.
- **Around a dominant mass the coordinates are ln z = ln r + iθ, the rings.**
  - Cell (k, j) spans r_0·2^(k/m) to r_0·2^((k+1)/m) and 2πj/N to 2π(j+1)/N. Choosing N ≈ 2πm/ln 2 makes the cells nearly square (m = 16 gives N = 128).
  - The map is conformal, so every cell has the same shape at every scale. A fixed number of bits per cell then gives the same relative precision everywhere.
  - The ring index *is* the gradient. A doll stores only its mass, its centre and its motion.
  - Crossing a ring conserves E and L. In integers this holds to one quantum, with carries. A ray (a line of constant angle) carries no gravity event.
- **Symmetry makes the future repeat.**
  - With E and L exact, the radial crossings repeat every cycle, and φ advances by a fixed amount per cycle. One cycle is computed once, and the orbit is then known until something breaks the symmetry. That is an exact shortcut, like Hashlife's, and nothing is forced.
  - Perturbations such as tides and neighbours arrive as kicks on E and L. H0190 measured 32 kicks per low orbit, and 0.3 with averaging.
- **Dolls nest as overset discs.** Overset (Chimera) grids are the technique fluid simulations use for moving bodies.
  - A doll covers a disc from its central body (surface or horizon) out to its sphere of influence.
  - It is the freely falling frame of that central body: its parent's gravity reduces to tides inside it (the equivalence principle).
  - The doll moves over its parent's grid and masks the parent's cells beneath it. A handoff happens when a body crosses the disc's edge; handoffs stayed bounded in H0190 K4.
- **Where no mass dominates, the coordinates are plain Cartesian,** with the same grid. There is no central symmetry to lose there.
  - The grid holds the field, and tubes move in any direction. Grid isotropy therefore matters far less than in lattice gases, where the grid carries the motion.
- **Other maps must earn their place.** One candidate is the bipolar map ln((z−a)/(z+a)) for binaries, where each star is surrounded by circles. A map joins only if it turns a class of motion into exact repetition, and regimes are chosen by dimensionless numbers such as mass ratios.
- **Spacetime is 2+1 dimensional, and its natural algebra is the split-quaternions.**
  - An event (t, x, y) is the pure split-quaternion t·i + x·j + y·k, whose norm t² − x² − y² is the interval.
  - Rotations and boosts are the unit split-quaternions, the 2×2 real matrices with determinant 1.
  - Lead: integer matrices with determinant 1 (SL(2,Z)) give exact, exactly reversible frame changes, but only for a discrete set of velocities. Untested.
- **Cells hold the integer mass moments of what they contain,** ships' aggregates included.
  - Geometry is a local rule of the moments: the clock rate (the potential) adds up, and the flow is derived from it.
  - A change travels at most one cell per update.

## One law

- **c is native.** An influence moves at most one cell per cell-update, and a cell's time unit is its light-crossing time. Light cones are cell adjacency.
- **Bodies are tubes relative to their doll's frame.**
  - Inside a cell, a tube follows the cell's exact local solution.
  - At a joint, the crossing rule conserves what the field's symmetry conserves. The crossing is a refraction, not a step.
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
   - How precession error depends on m, the rings per octave. The error is systematic and the same every orbit, which is the right type; its size is unmeasured.
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
