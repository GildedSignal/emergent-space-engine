# The design: a compiled causal automaton on symmetric spacetime

Status: **DRAFT** (29 September 2026). It synthesizes Julien's direction from 29 September ([register](PRINCIPLES.md); bottleneck 0 on the [lab board](../lab/board.md)). It supersedes nothing until the falsifiers in §7 have run and Julien says yes. Once adopted, it replaces [gravity-law.md](gravity-law.md) and [universe-quanta.md](universe-quanta.md), and it absorbs [engine.md](engine.md).

## The thesis

1. **Compute is the information the universe creates.** Predictable evolution costs nothing. Surprises (the player, AI decisions, chaos) cost in proportion to what they create.
2. **Predictability comes from symmetry.** Where a frame makes a symmetry explicit, its invariants are exact, motion repeats, and the repetition is stored once, as a generator. *Symmetry is compression.*
3. **Every quantity is kept in the form in which its change is an addition.**
   - Coordinates are chosen so that the symmetry is a translation.
   - Logarithms are used where things multiply.
   - Bits are used where the only question is "whether".

   Carrying a pattern forward is addition. Building a new one (at a surprise) means solving an equation. Reading one out (when something is observed) takes a multiply-add. So multiplications, roots and wide integers appear only at surprises and observations.

Everything below follows from these three, and so does its cost (§6).

## 1. Spacetime: frames that make symmetry explicit

- **Nested dolls.** Each dominant mass carries a doll: its freely falling frame, a disc running from its surface or horizon out to its sphere of influence.
  - Inside a doll, the parent's gravity is only tides (the equivalence principle).
  - Dolls nest as overset discs (Chimera grids, Steger, 1983). A child slides over its parent's grid and masks it, and a body crossing the edge is handed over.
  - A dense region with no central mass (a battle, a fleet) is also a doll: the free-fall frame of its centre of mass. Inside it, tides are linear, and relative motion has an exact closed form (Clohessy–Wiltshire, 1960). No mode ever freezes gravity.
- **One grid; the coordinates are chosen per doll.** In coordinates where the field's symmetry is a translation, the grid is always a uniform lattice of fixed-bit cells.
  - Boundaries then follow the symmetry, so each crossing conserves exactly what the field conserves (Noether). The precedent is the FHP lattice gas (1986): isotropy came from lattice symmetry.
- **Around a dominant mass, the coordinates are ln z = ln r + iθ: rings.**
  - In 2D, z is complex, and rotation and zoom become additions.
  - Rings are r₀·2^(k/m), cut by N ≈ 2πm/ln 2 spokes (m = 16, N = 128). The map is conformal: every cell has the same shape at every scale, and fixed bits give constant relative precision.
  - Rings are floating point. The octave is the exponent, and the ring is the top mantissa bits, so a point's ring comes from the bits of the integer r².
  - The ring index *is* the gradient: a doll stores only its mass, centre and motion.
  - Crossing a ring conserves E and L; crossing a spoke carries no gravity event.
  - **Binet cells (the primary in-cell solution).** With u = 1/r, the orbit inside band k obeys u″ + (1 − 6M·u_k)·u = M/L² − 3M·u_k². That is a rotation, two additions in integers (Minsky), and it preserves area. Precession, the innermost stable orbit (where 1 − 6M·u_k < 0) and plunges all emerge. Light is the same equation without the M/L² term.
- **Where no mass dominates, the coordinates are Cartesian,** with the same grid.
  - Any further map (for example the bipolar map, for binaries) earns its place only by turning a class of motion into exact repetition. It is chosen by dimensionless numbers.
- **Matter and geometry, the loop of GR, as a local rule.**
  - Cells hold integer mass moments of everything, ships' aggregates included.
  - **Two bodies are one doll.** At 1PN, the effective-one-body map makes their relative motion a test body in Schwarzschild with M = m₁ + m₂; the mass ratio ν enters only through the energy map. Hierarchical systems are therefore dolls all the way down. Non-hierarchical regions (cluster cores) go to the dense order. Mass moments source the kicks and the aggregates.
  - A change travels at most one cell per cell-update. Kerr in the plane keeps rotational symmetry (Doran's flow adds a twist).
- **Time.** c = 1 cell per cell-update, so a cell's time unit is its light-crossing time. Each doll orders events in its own far time, and each cell keeps an epoch. There is no global clock.
- **Algebra.** 2D space is complex numbers. 2+1 spacetime is split-quaternions: the event (t, x, y) is t·i + x·j + y·k, with norm t² − x² − y² (the interval). Rotations and boosts are the unit split-quaternions. Geometric algebra is the language underneath; each job uses the smallest subalgebra.

## 2. The law: one law, GR native

- **Bodies are tubes in their doll's frame.**
  - Inside a cell, a tube follows the cell's exact local solution.
  - At a joint, it refracts, conserving what the symmetry conserves.
  - Orbits, turning points, precession, lensing and horizons emerge; none is imposed.
- **One interface resolver.** A ring crossing and a contact are the same operation: conserve what the interface conserves, solve one quadratic, and carry the rounding. Contacts use the exact integer special-relativity law (`es-lattice-relativistic-v1`), in the frame of one of the two bodies.
- **Decisions are the only kinks.**
  - Thrust grows the rapidity linearly in proper time; in a field, E and L change by the work done.
  - AIs are deterministic parts of the law. An AI is recomputed only when what it sees crosses its perception threshold, and identical situations share a memo.
  - The player is the only seed.
- **Observables are emergent.**
  - A clock reads its tube's length.
  - A photon carries its momentum. At the moment of observation, −p·u *is* the colour: gravitational redshift, Doppler shift and time dilation at once. Its direction in the observer's frame *is* the aberration.
- **Light is gathered at the observer, never broadcast.** An AI's perception is the same gather at its own past light cone: one component.
  - Each visible tube crosses the observer's past light cone once; Newton's method finds the crossing, starting from the previous frame's. Lensing adds crossings, from each doll's memoized deflection(b).
  - An emitter carries a spectral type. A blackbody is seen at k·T with beaming k⁴, which in log form are additions. A type × log k table gives the sprite.
  - Aggregates are one sample each, and the screen caps the work at about one sample per pixel. Nothing bounces.
- **The error model.** The law is the integer algorithm, and exact GR is only the oracle that judges behaviours. There is one error budget: at most one floor unit per event, carried forward so that it never compounds. Shortcuts reproduce the law exactly, so they add speed, never error.

## 3. The compiler: what is compiled, what is paid

- **A step is a certificate:** the interval over which a description reproduces the law.
- **Generators.**
  - A doll orbit is a cycle: its radial crossings repeat, and each cycle adds constants to φ, t and τ. Identical invariants share one memoized cycle, as in Hashlife.
  - Perturbations (tides, neighbours, inspiral by Peters' formula) are kicks on E and L. A cycle's derivatives are stored with it, so a kick updates the cycle by a multiply-add.
  - Fleets are families. Stars and asteroids stay a seed until an event singles one out (Elite, 1984).
- **Two evaluation orders of the same event graph, with identical bits.**
  - **Sparse:** where events per cell per light-crossing (a Knudsen-like number) ≪ 1. Certificates, the causal frontier, and one queue ordered by slack, on the CPU.
  - **Dense:** where that number is near 1, which is chaos, the normal case of many necessary interactions in a short time.
    - Cells run in lockstep, in cache (on the GPU and NEON). A tick wastes nothing when everything changes every tick.
    - The broad phase is bits (occupancy maps, an AND, a radix sort of cell keys); the narrow phase is exact predicates on narrow numbers.
    - Events farther apart than c × the window resolve in parallel waves.
    - Its floor is the entropy it produces (about 4 bits per collision, H0173). Only the surprises are logged; the rest replays.
- **Causality is min-plus (tropical) algebra,** the logarithm of arithmetic (Maslov). Arrival times compose by + and are chosen by min. Light-cone spread is bit-parallel: a shift and an OR move light one cell for 64 cells at once.
- **The allocator** is that one queue. Priority is slack; the view has the hardest deadline; idle time computes ahead and recompresses.

## 4. Numbers: information-theoretic and native

- **The form follows the dominant operation.**
  - Quantities that are added are linear fixed point: in-cell positions, times, E and L.
  - Quantities that are multiplied are logarithmic: potentials, clock rates, Doppler factors, scales. There, a product is an addition and a square root is a one-bit shift. A float's bits already approximate log₂ (Mitchell, 1962), and a 16-entry table corrects them.
  - Converting between the two forms is a table lookup, done only at interfaces.
- **Squared forms elsewhere.** Compare r² and τ². Contact tests are sign tests. A root is taken only for an exact event time.
- **The width follows the information.**
  - Store invariants and epochs. Derive phases and fine positions, and only when needed.
  - Orbits that are indistinguishable at the stored width become one record.
  - Floors per body: about 2–5 bytes for a structured body given its family; about 12–16 bytes for an individual in a doll. Today's `Body` takes 88 bytes.
- **Carries are sigma-delta modulators** (Inose and Yasuda, 1962). Rounding error is pushed within an orbit, where it averages out, so stored numbers can be narrow. Bresenham's error term (1962) is the same trick, so tubes at rational speeds and carries are one mechanism. Minsky's circle (HAKMEM, 1972) keeps an orbit closed with two additions, because the map preserves area.
- **The virtual comma is explicit:** block floating point, with the cell level as the shared exponent.
- **The split between law and implementation.** Number forms and widths are law, fixed from rung r2. SWAR, NEON, AMX and bundles give the same bits, so they are implementation, deferred until B10 profiles on the M1.
- **Native per bundle, not per number.**
  - Several fields are packed into one word with guard bits, operated on once, and unpacked (SWAR).
  - Packing x + y·2³² gives two products from one multiply.
  - The M1's one-step operations to design around: add, logic and shifts; bit-field extract and insert; conditional select; leading-zero count; high-half multiply; CRC32.
  - On NEON: 16-lane add and min, TBL lookups, CNT, saturating adds, SDOT.
  - On the GPU: SIMD-group min, sum and prefix.
  - On AMX: outer products, for many kicks at once.
  - Wide integers only at rare events, on the CPU.
- **Memory.** Cells lie along a space-filling curve in causal order, and a cell's bodies are contiguous packets (128-byte lines, 16 KB pages). The frontier streams through memory, as Crash Bandicoot did.
- **One floor is chosen:** the finest spatial distinction the player can see, like the early-cinema frame rate. Time follows from c = 1.

## 5. Stolen from the compute-starved

Bresenham, the DDA integrators of the 1950s, sigma-delta, CORDIC (shift-and-add rotation), Minsky's circle, Mitchell's logarithms, the Apollo Guidance Computer's per-variable scaling, Clohessy–Wiltshire, Elite's seeded galaxy, Wolfenstein's observer rays, Crash Bandicoot's traversal-ordered memory, Hashlife. They had skin in the game (principle 26).

## 6. Where compute goes (estimates, 10⁹ ships)

| Work | Rate | Cost |
|---|---|---|
| Undisturbed orbits | only when looked at | ≈ 0 |
| Tidal kicks, with averaging | ~6×10⁴ per game-second | ~50 ns each, incremental: < 1% of a core |
| A cycle's first computation | new invariants only | tens of crossings, then memoized |
| The view | ≤ 1 sample per pixel per frame | GPU |
| Chaos and contacts | bursts | the dense order: entropy, the p99 risk |
| AI decisions | when their view changes | likely the largest total, and unknown |

The same things on the current path cost 340–120,000 steps per orbit, 20,000–77,000 steps per light path (probe 2), and 88 bytes per body (the current `Body`).

## 7. The falsifier ladder

Kill criteria are frozen in [lab/rungs/](../lab/rungs/). Each rung is run in the cloud by the GLM lab, gets a mechanical verdict, and has a negative control that must be killed. Only r1–r3 gate the law.

1. **r1 rings.** One static mass. Binet cells and river refraction, with m swept; a square grid and a tilt-only kick as negative controls. Judged on precession, periods, deflection, capture, the innermost stable orbit, shape over 10⁴ cycles, exact cycle repetition, and crossings per cycle.
2. **r2 carry width.** Sigma-delta storage of the per-cycle increments and of kicks, at 16, 24 and 32 bits.
3. **r3 two-body doll.** The effective-one-body map at 1PN, handoffs between dolls, and gravity assists.
4. **r5 dense order.** A Clohessy–Wiltshire frame with lattice contacts, bit-identical between the sparse and dense orders (integer, on the existing crates).
5. **r6 view.** Newton iterations and samples per frame for the gather.
6. **r7 AI cost.** A float faction toy: the recompute rate against the perception threshold, and the memo hit rate.

## Merge candidates (for Julien)

1. **Proposed by the planning pass:** the view and AI perception are one gather: an AI sees its past light cone exactly as the player does.
2. **Proposed by the planning pass:** the frontier and the allocator are one component: the slack queue is the min-plus frontier, ordered by deadline.
3. **Fleets, battles and families are one kind of doll:** a free-fall frame with members.
4. **Kicks are the non-symmetric remainder** of the same moments that set the field.
5. **Dolls and cells may be one spacetime tree** in per-doll coordinates.

## 8. What carries over

| Built | Role here |
|---|---|
| `es-lattice-relativistic-v1` | the contact resolver; its carries become the rounding rule everywhere |
| `lattice-event` | the sparse order; its density cells give way to dolls and on-demand contact bins |
| `lattice-metal` | the dense order (already 32-bit and cell-relative) |
| `allocator` | the one queue, ordered by slack |
| chronon mode | the test judge; the hybrid and regions modes merge into the two orders |
| `gr-oracle`, the Arb judge, `gravity-gate`, ladder v7 | the judges of behaviour and cost |
| H0190 (kicks, averaging, handoffs) | the dolls' perturbation layer |
| families (H0182), the hyperedge IR (H0016) | fleets sharing frames, and the causal event graph |
| gravity v0; the v1 drift-kick draft | oracle material; superseded |
