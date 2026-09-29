# Bottleneck board

Owned by the integrator and rewritten in place. **Target:** the fastest and most robust engine and compiler for relativistic many-body physics at game scale. That means billions of bodies on one fanless 8 GB M1, exact and deterministic, computing only surprises (see [PRINCIPLES](../docs/PRINCIPLES.md)).

## Bottlenecks, ranked (29 September)

0. **The representation, from scratch** (Julien, 29 September). It is one question, and the others below may be its consequences.
   - The engine is "a causal cellular automaton that runs as fast as possible or maybe that is guided by light speed".
   - "we need to make light speed hardware native… light speed is basically how fast the causal chain is updated".
   - "a 'simple' tube is tracing a straight line through spacetime which means that space time needs to be represented in such a way that it is possible while respecting gr".
   - "we want to guess in a way that is perfect how the simulation will run to bypass it"; "steps are there to solve a problem of how much error we are ok with… we want them consistent across the different types of simplifications… We need to expand what steps mean".
   - "rethink our units from scratch, time and spatial ones", "tied to hardware and end goal"; the number representation from first principles; "how we travel [memory] limiting useless movement".

   - Later the same day he added:
     - "We need to make this whole thing GR native that's THE unlock"; "GR is just one thing".
     - Sheets as nested dolls of a fixed bit size, whose size is linked to the spacetime gradient ("we can infer it from the size").
     - AI and player decisions as the seeds of change.
     - "the floor is what the player can differentiate like frame rate in early cinema"; units from the hardware.
   - Later still:
     - The sheets encode GR only: "collisions is just how you move inside them". Contact compute is a separate, on-demand structure that is never stored in the geometry.
     - The ship-versus-asteroid threshold must be cheap.
     - AIs create emergence that is hard to predict.
     - Local laws, but global algorithms are allowed: "make the memory dance tighter from a causal pov".
   Derive it from the requirements (the goal, the behaviours, the M1) before any known method. Candidates to test, not adopt:
   - fixed-bit cells in a dyadic tree, where the level acts as a shared exponent (block floating point, OCP microscaling);
   - geometry partly encoded by the tree's shape;
   - AIs as part of the deterministic law, recomputed only when what they see changes, so the player is the only seed;
   - one chosen floor (spatial), with time derived through c = 1 and velocity precision derived from the certificate's length;
   - each cell a freely falling local frame, with bodies stored as small offsets from it;
   - c as one cell per update, so each cell's time unit is its light-crossing time;
   - exact shortcuts in the spirit of Hashlife;
   - a bit-reversible integer law, so errors cannot compound;
   - asynchronous variational integrators, which keep energy bounded across cells with different steps.
1. **What cells add for many sources.** Mass moments add; the river flow does not, because β ∝ √M. We need a rule from a cell's multipole expansion to its local β that:
   - is exactly Schwarzschild for one mass;
   - is curl-free for static sources;
   - is right to 1PN for two masses.

   See "Open" in [gravity-law.md](../docs/gravity-law.md).
2. **Stepping owned by cells, or no stepping.** Probe 1 killed per-body steps: the energy error walked, and distant light jumped over the lens. We need bounded energy error, correctly bent distant light, and ≤ 512 events per orbit. Probe 2 (29 September) killed cell-owned staircases: every shell crossing injects energy error (up to about 3×10⁻³), as Calvo and Sanz-Serna predict. One fixed step passes the physics at about 350–700 steps per orbit, and light costs 20,000–77,000 steps. The live path is no steps at all: analytic generators in the dominant field, with multipole residuals as kicks (H0190: 32 kicks per orbit, 0.3 with averaging), and integration only where no generator exists.
3. **Cost at a billion.** 10^9 orbiting bodies at today's rates would need about 190 cores. We need 10–100× less: fewer events per orbit, cheaper events, and never computing what nobody can observe.
4. **Smoothness and the allocator.** The worst frame and the p99 on a fanless M1 that throttles when hot. Least-slack scheduling fed by surprise rates; five modes to become one engine.
5. **Units, widths and memory: one question.** The quanta couple position, velocity and time. The position quantum is c·δt/Q = 2.3×10⁻¹⁴ m, so 32 bits span only 49 µm, and an AU needs 83 bits. That is set by the worst case, a near-c 50 cm missile, and applied everywhere.
   - Can each cell own dyadic quanta sized by its content, with cell-relative coordinates and positions derived from generators, so that most state fits in 32-bit packets?
   - The M1 GPU is native at 32 bits, emulates 64, and has no 128 and no fp64.
   - The memory floor is information-theoretic.

## Known: don't redo it, build on it

- Exact continuum geodesics as the implementation ran 1,600× over budget (H0194). They are now the oracle.
- Per-body dynamical-time steps make energy error walk ([probe 1](../artifacts/evidence/gravity-v1-freeze-20260929/probe-out.md)). The fixed-step control stays flat.
- One GEM quadrupole failure (H0139) is not a ban on multipoles (H0196).
- Premise probe H0190:
  - averaging tides cuts kicks 114×;
  - J2 must be in the formula;
  - binaries need a two-body parent.

## Leads from earlier work (unexplored; a lens may pick one up)

- The polymath scan (GLM, 28 September): commutative-monoid messages between regions; largest-remainder splits; choosing the error-feedback kernel by its low-frequency error; a replay-bisect tool; an LSM- or CRAM-style body store.
- Mechanisms from arch-v3 not yet running: gate-bite mutants; adversarial mining into a shadow corpus; blind panels of 3–5.
- Prior-art scout (29 September, `artifacts/runs/prior-art-timestep/out.md`): Calvo and Sanz-Serna (1993) show that a state-dependent step is never symplectic. The working schemes put the adaptivity in time (Sundman, logarithmic Hamiltonian), in the hierarchy (HOLD) or in the mesh (AVI).
- Julien, 29 September: local sheets and no teleportation make the engine an asynchronous cellular automaton that follows causal chains instead of cataloguing. Positions are re-derived, never global. 32-bit packets per region. Memory laid out in causal order, as Crash Bandicoot laid out its levels. Are the quanta sensible? (see bottleneck 5)

## Taste log (the integrator's decisions on gold, newest first)

- **29 September, r2 (carry width): KILL of sd16, sd24 and sd32.**
  - **What it showed:** a 32+32-bit pair holds float64 increments exactly (zero phase error). Carries cannot recover information below their own resolution. Kicks on the law's own grid accumulate exactly at any width.
  - **Integrator's error:** two criteria demanded trajectory identity with float64 (conjunction order; the worst-seed kick-residual exponent), which the checker proved unpassable.
  - **Fix:** positive controls in `verdict.py`, and criterion-writing rules in the README.
  - **Design consequence:** increments and kicks are integers native to the law, so widths are set by behaviour (r1 and the law's gates), not by matching floats.
- **29 September, premise red-team: silver.**
  - **Adopted:** the rule that resonance kills averaging (design §3, rung r4); r3 v2's truncation fix; Clohessy–Wiltshire is first order only; Minsky's map is a conjugated rotation.
  - **Why silver, not gold:** its model B, the half claiming "kicks survive", was a dense integration, not the design's kick layer. Claims must be measured on the design's cheap path.
  - **Why it was good work:** a converged truth, predictions written before the decisive run, the rung gap audited, and honest misses.
