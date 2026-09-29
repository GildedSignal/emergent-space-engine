# Bottleneck board

Owned by the integrator and rewritten in place. **Target:** the fastest and most robust engine and compiler for relativistic many-body physics at game scale. That means billions of bodies on one fanless 8 GB M1, exact and deterministic, computing only surprises (see [PRINCIPLES](../docs/PRINCIPLES.md)).

## Bottlenecks, ranked (29 September)

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

(none yet)
