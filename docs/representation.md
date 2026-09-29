# Representation: one structure, one law, one number type

Status: **DRAFT** (29 September 2026). This synthesizes Julien's direction from 29 September; see the [register](PRINCIPLES.md) and bottleneck 0 on the [lab board](../lab/board.md). It supersedes nothing until its cheapest falsifier has run and Julien says yes.

## One structure: nested dolls whose grid follows the field's symmetry

- **Criterion (Noether): cell boundaries follow the symmetries of the field they hold.** A crossing can then conserve exactly what the field conserves: energy if the field is static, angular momentum if it is rotationally symmetric. Grid symmetry matters wherever the grid carries physics: square lattice gases failed isotropy, and the hexagonal FHP lattice (1986) fixed it.
- **Around a dominant mass the field is central, so the doll is log-polar.**
  - Rings sit at r_k = r_0·2^(k/m), with m rings per octave. This is the complex logarithm: conformal, so every cell has the same shape at every scale, and a fixed number of bits per cell gives the same relative precision everywhere.
  - The ring index *is* the gradient. A doll stores only its mass, centre and motion; its field is a function of k.
  - Crossing a ring conserves E and L exactly (in integers: to one quantum, with carries). Crossing a ray carries no gravity event.
- **Symmetry makes the future repeat.** With E and L exact, the sequence of radial crossings repeats every radial cycle, and φ advances by a fixed amount per cycle.
  - One cycle is computed once; the orbit is then known until something breaks the symmetry.
  - Nothing forces the orbit: it follows from the law's own symmetry, an exact shortcut like Hashlife's.
  - Perturbations (tides, neighbours) are kicks on E and L. H0190 measured 32 kicks per low orbit, 0.3 with averaging.
- **Each doll is the freely falling frame of its central mass.**
  - A planet's doll falls around its star. Inside it, the star's gravity reduces to tides: the equivalence principle.
  - A doll ends at its sphere of influence. Handoffs there stayed bounded (H0190 K4).
- **Where no mass dominates, symmetry breaks** (binaries, clusters, dense fleets, galactic disks). There, general multipole cells hold the field.
  - Triangles are the candidate: they nest exactly (1 → 4), have 6-fold symmetry, and use integer Eisenstein arithmetic (norm a² + ab + b²).
  - The fraction of bodies living there sets the cost.
- **Cells hold the integer mass moments of what they contain,** ships' aggregates included. Geometry is a local rule of the moments: the clock rate (potential) adds, and the flow is derived. Changes travel at most one cell per update.

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
