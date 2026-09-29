# Representation: one structure, one law, one number system

Status: **DRAFT** (29 September 2026). It synthesizes Julien's direction from 29 September; see the [register](PRINCIPLES.md) and bottleneck 0 on the [lab board](../lab/board.md). It supersedes nothing until its cheapest falsifier has run and Julien says yes.

**The idea.** Choose, for every quantity and every region, the representation in which its work is trivial:
- **Spacetime** is nested dolls whose grid follows the local field's symmetry. Orbits therefore repeat, and are paid for once.
- **The law** is tubes that refract at joints, with c native. Decisions are the only kinks.
- **Numbers** hold only the information their behaviour needs, in the form their operations want (linear or logarithmic), at native widths.
- **Evaluation** has two orders: sparse certificates where little happens, dense lockstep where much does.

Booleans answer "whether", additions carry motion, lookups carry repetition, and multiplications happen only at surprises. Compute follows entropy (principle 3).

## 1. Spacetime: nested dolls, one grid, coordinates per doll

- **Coordinates and grid are one choice.** Pick the coordinates in which the field's symmetry becomes a translation. There, the grid is always a uniform lattice of fixed-bit cells.
  - Boundaries then follow the symmetry, so each crossing conserves exactly what the field conserves (Noether).
  - The precedent: square lattice gases failed isotropy, and the hexagonal FHP lattice (1986) fixed it.
- **Around a dominant mass the doll is log-polar:** ln z = ln r + iθ. In the 2D plane, z is a complex number, and rotating and zooming (multiplications) become additions.
  - The rings are r_0·2^(k/m), and N spokes with N ≈ 2πm/ln 2 keep cells nearly square (m = 16, N = 128).
  - The map is conformal, so cells have the same shape at every scale, and fixed bits give the same relative precision everywhere.
  - The ring index *is* the gradient: a doll stores only its mass, centre and motion.
  - Rings are floating point: the octave is the exponent, and the ring within the octave is the top mantissa bits. The ring of a point comes from the bits of the integer r² (a leading-zero count plus a shift), with no root and no log.
- **Crossing a ring conserves E and L** (to one quantum in integers, with carries). A spoke carries no gravity event.
- **So the future repeats.** The radial crossings repeat every cycle, and φ, t and τ advance by fixed amounts.
  - One cycle is computed once, then memoized: identical invariants share it, an exact shortcut as in Hashlife.
  - Perturbations are kicks on E and L. H0190 measured 32 per low orbit, and 0.3 with averaging.
- **Dolls nest as overset discs,** as fluid simulations do for moving bodies (Chimera grids).
  - A doll runs from its central body (surface or horizon) to its sphere of influence.
  - It is that body's freely falling frame, so the parent's gravity reduces to tides inside it.
  - It slides over its parent's grid and masks it. Handoffs happen at its edge; H0190 K4 found them bounded.
- **Where no mass dominates, the coordinates are Cartesian,** with the same grid. The grid holds the field, and tubes move in any direction.
  - A new map, such as the bipolar map ln((z−a)/(z+a)) for binaries, earns its place only by turning a class of motion into exact repetition.
  - Maps are chosen by dimensionless numbers, never by categories.
- **Cells hold integer mass moments,** ships' aggregates included. Geometry is a local rule of the moments: the potential adds, and flow² = 2 × potential. Changes travel at most one cell per update.
- **The natural algebra of 2+1 spacetime is the split-quaternions.**
  - The event (t, x, y) is t·i + x·j + y·k, whose norm t² − x² − y² is the interval.
  - Rotations and boosts are the unit split-quaternions.
  - Geometric algebra is the one language underneath: each job uses its smallest subalgebra.

## 2. The law

- **c is native.** An influence moves at most one cell per cell-update, and a cell's time unit is its light-crossing time. Light cones are adjacency, and they spread as bits: a shift and an OR move light one cell for 64 cells at once.
- **Bodies are tubes in their doll's frame.**
  - Inside a cell, a tube follows the cell's exact local solution.
  - At a joint, the tube refracts, conserving what the symmetry conserves. Contacts use the same interface resolver: conserve, solve one quadratic, carry the rounding.
  - Orbits, turning points, precession, lensing and horizons emerge.
- **Observables are emergent, never computed.**
  - A clock's reading is the length of its tube.
  - A photon carries its momentum, and an observer is a tube with a velocity. Where they meet, the one operation of observation, −p·u, *is* the colour: gravitational redshift, Doppler and time dilation together. The photon's direction in the observer's frame *is* the aberration.
  - Lensing is photon tubes refracting at rings. Multiple images are multiple tubes.
- **Decisions are the only kinks.** AIs are deterministic parts of the law, recomputed when what they see crosses a threshold. The player is the only seed.

## 3. Steps are certificates, evaluated in two orders

- **A step is a certificate:** the interval over which a description reproduces the law.
  - The error budget is at most one floor unit at each event, carried forward so that it never compounds.
  - Shortcuts reproduce the law exactly wherever possible, so simplifications add speed, never error.
- **The sparse order** is where little happens: certificates, the causal frontier, and one queue ordered by slack, on the CPU.
- **The dense order** is for chaos, which is normal: many necessary interactions in a short time.
  - The selector is events per cell per light-crossing, a Knudsen-like number.
  - Near 1, cells run in lockstep, in cache, on the GPU and NEON. A tick wastes nothing there, because everything changes every tick.
  - Time scales separate: during a burst, the field's certificates hold, so the burst is pure special relativity in one frame, the lattice law's home.
  - The broad phase is bits (occupancy bitmaps, an AND for overlaps, a radix sort of cell keys). The narrow phase is exact predicates on narrow, cell-relative numbers.
  - Events farther apart than c × the window resolve in parallel waves.
  - The burst stays in cache (the 12 MB L2 of the performance cores, GPU threadgroup memory), so it is compute-bound, not memory-bound.
  - Its floor is the entropy it produces: H0173 measured about 4 bits per collision. The log of surprises is kept; the rest replays.
- **Both orders give identical bits** (engine.md rule 12).

## 4. Numbers as information

Each stored number holds the information its behaviour needs, in the form its operations want, at a width the silicon handles natively.
- **The form follows the dominant operation.**
  - Quantities mainly added are linear fixed point: positions within a cell, times, E and L under kicks.
  - Quantities mainly multiplied are logarithmic (a logarithmic number system): potentials M/r, clock rates, Doppler factors (whose logarithm, the rapidity, adds up under boosts, as in Bondi's k-calculus), scales and radii. There, multiplication is addition, a power is a shift, and **a square root is a one-bit shift.**
  - A float's bit pattern already approximates its log₂ (Mitchell, 1962), and a 16-entry table corrects it.
  - Converting between the two forms is a lookup, done only at interfaces.
- **Squared forms elsewhere.** Compare r² and τ². Contact tests are sign tests on the quadratic. A root is taken only for an exact event time, with a few Newton multiply-adds.
- **The width follows the information.**
  - Store invariants and epochs. Phases are derived exactly from time. Fine positions are computed from exact invariants only when an interaction needs them.
  - Orbits indistinguishable at the stored width are one record: the quantization merges what the player cannot tell apart.
  - Floors per body: about 2–5 bytes for a structured body given its family (a fleet member, a belt asteroid); about 12–16 bytes for an individual in a doll. Today's `Body` takes 88 bytes.
- **Noise shaping lets stored numbers be narrow.** The carries are sigma-delta modulators. A 1-bit audio converter reaches 20+ bits in band by pushing rounding error to high frequency. Our carries push it within an orbit, where it averages out. How narrow E and L can be is a measurement.
- **The silicon.**
  - 32-bit words, and 32×32 → 64-bit products as hi/lo pairs.
  - 16-bit halves: NEON runs 8 lanes per instruction, and the GPU keeps more threads in flight.
  - Leading-zero count and popcount are single instructions. A 128-byte line holds one cell summary.
  - Block floating point: the cell level is the shared exponent, which is the "virtual comma" made explicit.
  - Wide numbers only at rare events, on the CPU.
- **One floor is chosen:** the finest spatial distinction the player can see (the early-cinema frame rate). The time floor follows from c = 1.

## 5. Hard operations made cheap

| Hard operation | Representation | What remains |
|---|---|---|
| Rotation, zoom | log coordinates (rings) | +1 on indices |
| Changing scale | levels as a shared exponent | a shift |
| Gravity on a body | a freely falling doll | tides only |
| An orbit | symmetric rings, E and L exact | per cycle: φ, t, τ += constants (one vector add) |
| Perturbations, inspiral (Peters' ΔE, ΔL) | kicks on the invariants | + on E and L |
| Boosts, square roots, potentials | logarithmic numbers | additions and shifts |
| Causality, arrival times, scheduling | c native; min-plus (tropical) algebra, the logarithm of arithmetic (Maslov) | bits, + and min |
| Repetition | memoization | a lookup |
| Memory | cells along a space-filling curve in causal order; families until an event singles one out | streaming |

## 6. Stored once, or not at all

- **Invariants over conventions.** Coordinates are conventions, used locally and converted only at surprises. The invariants are rest mass, proper time, the interval, E and L in a doll, a photon's b = L/E, and γ_rel = −u₁·u₂ (a dot product).
- **Merged:**
  - potential and flow;
  - time dilation, redshift and Shapiro delay: one lapse, emergent;
  - tides and multipoles;
  - a photon is a massless body;
  - a step is a certificate;
  - a contact and a crossing are one resolver.
- **Derived from something else:**
  - a doll's edge, from its mass ratio;
  - a cell's time unit, from its size;
  - an anonymous body's identity, from its slot;
  - mass and radius, from a type table.

## 7. Interactions

| Interaction | Where it lives | Cost |
|---|---|---|
| Orbits; Kerr in the plane (still symmetric, with Doran twist); inspiral | doll cycles | additions per cycle |
| Tides, dynamical friction, fleets as sources | kicks from moments | per kick |
| Comparable masses: binaries, three-body encounters, clusters | Cartesian cells, stepping in the dense order | real entropy |
| Thrust (relativistic rockets) | rapidity linear in proper time; in a field, the cell's local solution, with E and L changed by the work done | per crossing while burning |
| Orientation, spin, geodetic precession | an angle carried across crossings | additions |
| Contacts, near-c collisions, fragmentation, explosions | the lattice law in the dense order; expanding shells at ≤ c | entropy (debris is open) |
| Tidal stress (Roche limit, spaghettification) | tidal term against strength | a threshold test |
| The view: retarded positions, aberration, beaming, lensing | past light cone per visible body; deflection(b) memoized per doll | per visible body per frame, on the GPU |
| Signals; horizon absorption; accretion | photons with 1/r² fall-off; the doll's mass ledger | at events |

## 8. What carries over from what we built

| Built | Role here |
|---|---|
| `es-lattice-relativistic-v1` (exact integer special relativity, carries, walls) | the contact resolver; its carries become the rounding rule everywhere |
| `lattice-event` (event core, queue) | the sparse order. Its density-sized cells give way to dolls plus on-demand contact bins |
| `lattice-metal` (GPU lockstep, 32-bit cell-relative) | the dense order |
| `allocator` (regions, least slack) | the one queue, fed by surprise rates |
| chronon mode | the test judge. The hybrid and regions modes merge into the two orders |
| `gr-oracle`, the Arb judge, `gravity-gate`, ladder v7 | the behaviour and cost judges. The chaos rungs exercise the dense order |
| H0190 (kicks, averaging, handoffs) | the dolls' perturbation layer |
| families (archived H0182); the hyperedge IR (archived H0016) | fleets sharing frames and invariants; the causal event graph |
| [universe-quanta.md](universe-quanta.md) (a global Q = 2^40) | replaced by per-cell block floating point and one floor |
| gravity v0 (exact geodesics); the v1 drift-kick draft | oracle material; superseded by dolls |

## 9. Weakest joints, and the cheapest falsifier

1. **Accuracy per crossing.** Weak-field precession and turning points against m, the rings per octave. The error is systematic and the same every orbit (the right type); its size is unmeasured.
2. **The many-source rule.** The potential adds and the flow is derived; it must pass 1PN for two bodies.
3. **Crossings between levels,** within the error budget.
4. **Moving sources.** Energy exchange must be physical (gravity assists), not numerical.
5. **How narrow the invariants can be** under noise-shaped carries.

**The falsifier** (float, one static mass, each script under 60 s, kill criteria frozen before the run):
- log-polar rings, with m swept;
- E and L conserved at each ring;
- the cycle's periodicity checked;
- a dyadic square grid as the control.

It is judged by the behaviour gates of [gravity-law.md](gravity-law.md): precession at p = 20M and 1000M, E = 1 capture at L = 4M, deflection from r = 10⁴ M, E and L over 10⁴ orbits, and crossings per cycle.
