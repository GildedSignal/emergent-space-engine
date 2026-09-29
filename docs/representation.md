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
  - Lead: integer matrices with determinant 1 give exact, reversible frame changes, but the slowest boost among them is already about 0.75c. With dyadic fractions every speed becomes reachable, but exact composition grows the denominators, and rounding them back costs exact reversibility. Untested.
- **Cells hold the integer mass moments of what they contain,** ships' aggregates included.
  - Geometry is a local rule of the moments: the clock rate (the potential) adds up, and the flow is derived from it.
  - A change travels at most one cell per update.

## How computation becomes cheap: turn hard operations into additions

| Hard operation | Representation | What remains |
|---|---|---|
| Rotation and zoom (multiplication) | log coordinates (rings) | +1 on integer indices |
| Changing scale (doll or level) | dyadic levels as a shared exponent | a bit shift |
| Gravity on a body | a freely falling doll frame | nothing but tides |
| An orbit | rings aligned with its symmetry, with E and L exact | per cycle: φ += Δφ, t += T, τ += Δτ |
| Perturbations | kicks on the invariants | + on E and L |
| Free motion | tubes | one multiply-add, or counting at rational speeds |
| Causality and light cones | c native | cell adjacency |
| Earliest arrival, light-cone spread, scheduling | min-plus (tropical) algebra, the logarithm of ordinary arithmetic (Maslov) | + and min |
| Identical situations (orbits, regions, AI inputs) | memoization (Hashlife) | a lookup |
| Memory | causal order | sequential streaming |
| Numbers | 32-bit words with shared exponents | native on every unit |

**Native forms (29 September, second pass):**
- **Rings are floating point.**
  - A float's exponent is the octave, and its top mantissa bits are the ring within that octave.
  - The ring index of a point is therefore the bits of the integer r², shifted: leading-zero count plus four bits. This needs no square root and no log. Rings then repeat every octave, which is the self-similarity a dyadic tree needs.
  - Block floating point (a cell level shared as the exponent, an integer mantissa) gives floats' range with integers' determinism. It is "where you put the virtual comma", made explicit.
- **Light-cone (null) coordinates u = t − x and v = t + x do for boosts what rings do for rotations.**
  - The interval is the product u·v, so no square root is needed.
  - A boost is the scaling (u, v) → (k·u, v/k).
  - In log form, log k (the rapidity) is added: Bondi's k-calculus.
  - Light moves along grid lines.
- **Squared forms replace square roots.** Store the potential, 2M/r = |β|², not the flow. Compare r² and τ², not r and τ. Contact tests are sign tests on the quadratic.
  - A root is taken only where an exact time is needed: a contact that becomes the next event, or a cycle's first computation. It then costs a few Newton multiply-adds.
- **Bundles:**
  - an event with its velocity is one split-quaternion, and one product changes both;
  - (E, L) kicks are one 2-vector add;
  - (ring, spoke) is one packed 32-bit word, and a single add moves both halves (SWAR);
  - a cycle update (φ, t, τ) is one vector add (NEON: 4 lanes; the GPU: 32).
- **Booleans answer "whether"; integers answer "how much".**
  - Occupancy, validity and overlap are bitmaps.
  - Light-cone spread is bit-parallel: shift and OR move light one cell for 64 cells at once. Julien, 26 September: "overlap of spacetime occupation which is quite boolean like".
  - A direction's octant is 3 bits.
- **Rotation without multiplication:** CORDIC (shifts and adds), where rotations are needed at all.
- **One language underneath:** geometric algebra. Complex numbers, split-quaternions and the conformal extension, which makes translations multiplicative too, are its subalgebras. Each job uses the smallest one.

Real multiplications, square roots and wide integers remain only at surprises: handoffs, a cycle's first computation, contacts and decisions. Compute then equals entropy (principle 3).

## Invariants over conventions

Coordinates are conventions; behaviour lives in invariants. **Store invariants, and use a convention only locally, only where it makes a task trivial, and convert only at a surprise.**
- **The invariants** are rest mass (the norm of momentum), proper time, the interval, E and L inside a symmetric doll, a photon's impact parameter b = L/E, and the relative speed of two bodies. The relative speed is γ_rel = −u₁·u₂, a dot product.
- **A contact is tested in the rest frame of one body,** where it reduces to a line against a circle.

**Merged or derived. Nothing is stored twice:**
- **Potential and flow.** Flow² = 2 × potential, so only the potential is kept. Inside a doll the potential follows from the ring index, so nothing is stored at all.
- **Time dilation, redshift and Shapiro delay** are one lapse, derived.
- **Tides and multipoles** are one object.
- **A doll's edge** follows from its mass ratio.
- **A cell's time unit** follows from its size, since c = 1.
- **A photon** is a body with zero rest mass: one type.
- **A step** is a certificate.
- **A body in a doll** is stored as (E, L, phase, type) plus carries on E and L only, about 12–16 bytes. Its position and velocity are derived. Anonymous bodies take their identity from their slot, and their mass and radius from a type table.
- **A contact and a ring crossing** are one interface resolver: conserve what the interface conserves, solve one quadratic, carry the rounding.

## Interactions: where each lives

| Interaction | Where | Cost |
|---|---|---|
| Orbit in a dominant field; Kerr in the plane (still symmetric; Doran twist) | doll cycle | adds per cycle |
| Tides, dynamical friction, fleets as sources | kicks on invariants from moments | per kick |
| Inspiral, gravitational waves | Peters' ΔE, ΔL per cycle | adds per cycle |
| Comparable masses: binaries, three-body encounters, clusters | Cartesian cells, general stepping | real work, and real entropy |
| Continuous thrust (relativistic rockets) | the rapidity grows linearly in proper time: a straight line in log-null coordinates. In a field, the cell's exact local solution; E and L change by the work done | per crossing while burning |
| Orientation, spin, geodetic precession | an angle transported across crossings | adds |
| Contacts, near-c collisions | the exact lattice law, on demand | entropy |
| Fragmentation, debris, explosions | new bodies and expanding shells at ≤ c | entropy; open (debris) |
| Tidal stress on extended bodies (Roche limit, spaghettification) | the tidal term against the body's strength | a threshold test |
| The view: retarded position, aberration, Doppler, beaming, lensing with multiple images | past light cone per visible body; aberration as a Möbius map of directions; deflection(b) memoized per doll | per visible body per frame (GPU) |
| Signals | photons with inverse-square fall-off | derived |
| Horizon absorption; accretion | the ledger of the doll's mass | at events |

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
