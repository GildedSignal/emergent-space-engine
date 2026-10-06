# Bottleneck board

Owned by the integrator and rewritten in place. **Target:** the fastest and most robust engine and compiler for relativistic many-body physics at game scale. That means billions of bodies on one fanless 8 GB M1, exact and deterministic, computing only surprises (see [PRINCIPLES](../docs/PRINCIPLES.md)).

## Focus (Julien, 30 September)

"the only goal is the engine/compiler to work with GR natively". **AI and factions are off the plan:** no lens works on decisions, factions or agents until Julien brings them back. The plane flies (docs/plane.md, H0210), and work goes by its measured bottleneck. The live engine questions, in order (1 October):
- fewer kicks per orbit at the same behaviour (correctors, higher-order splits): kicks dominate the engine's cost;
- the changeover near a secondary, reversible and integer (TRACE, JANUS);
- finding encounters without work per orbit or per element change (the Binet cone, r8 v3, plus a skin);
- the Schwarzschild tide in the Fermi frame (phase 2, after gate E9);
- fitting 10⁹ in 8 GB (`crates/shipmem`: population programs plus scars; every body real, never averaged), decided by distinctions created per game-second;
- **the top scaling risk (5 October):** candidate pairs per body grow with N at a fixed distribution (O(N²) pairs); candidate work must track real encounters (`q-candidate-degree`).

The list of 29 September below is background: the pivot (H0200 onwards) answered most of it.

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

- **6 October, overnight (silvers, adopted into the design).** q-candidate-degree: two-tier certificates, zero misses to 10⁶, work per real encounter constant at fixed density (the outside review's O(N²) risk answered for fixed density; strict C·log N is impossible for exact discovery under dilution; drop the "Wide" tightening, which misses 23% at e 0.7–0.9). m-meso-motion: the close encounter as one exact pair event, regime chosen by U/√(μ_p/b); conditional (deep flybys still fail). m-spacetime: superposed contravariant Kerr–Schild fields as rank-1 integer deposits answer how sources add in GR. All three go to the motion law v2 design (Opus, then Astra). The plane-judge correction: B13's lost flybys passed inside the planet in the point-mass reference (an oracle-domain defect), not encounter failures; the lab's reading was wrong there.

- **5 October, correction: the memo finding was an artifact.** Five runs agreed that 95–98% of the plane's kicks would hit the memo; the plane's builder found they all re-timed one pending kick every frame. On distinct kicks the exact memo hits 0%; the quantized cell hits 94.5% but changes orbits, so it is a law change. Lesson for every author and checker: agreement between runs is not independence when they share a harness. Check that the measured events are distinct before counting hits.

- **5 October, the off-time lab (39 runs on GitHub Actions, 1–5 October).** One gold, `components-98bc` (a smooth belt as a bijective program: 0.126 bits per body against 157): waiting on Julien ("no Elite style"; B18 needs a belt rung). Adopted from silvers, by convergence: correctors and higher-order splits buy nothing (six runs), so the lever is cadence (q-cadence queued; the engine is measured by `behave --law plane`); the plane recompiles an orbit on about 99% of kicks while the memo would hit 95–98% (five runs; Sonnet wires it); the tie rule (redteam-6254, now in law.md); replays at canonical ticks (taleb-c271). r10: the SyMBA changeover at a fixed base step is KILLED in float (exponent 0.43); q-changeover: no float changeover at the plane's budget reaches 0.2, TRACE is dead, a smooth integer changeover is bit-reversible (JANUS). Most silvers fell short of gold on the record, not the physics: results that the shipped code could not regenerate. Three runs (2 October, 23:47) never started.

- **1 October, the law's red-team: silver, adopted.** Moving lenses (a static memo is off by √((1+β)/(1−β)): B16); no resonance gate (B17); B9 a control beyond e = 0.6 (now log-scaled); B14 classification only (precession and eccentric births added); no memory gate (B18, a requirement from the goal); B15 medians (p99 added); the sense-blind τ selector (replaced by the binary doll). Not gold: one held-out prediction failed (transverse error is second order) and was reported as held.
- **1 October, r9 (the Hill regime): KILL of kick-avg and hill-torus on precession; valid and decisive.** Averaged tidal kicks get every class right but apsidal precession only below τ₀ = 0.0036 (0.17 Hill radii): Clairaut's first-order problem. Only 4.6% of the strong regime lies on compilable tori.
- **1 October, r4 v3 (the resonant normal form): KILL of nf1 and nf2.** Libration amplitude 0.28 and pumping off by up to 2×. The checker found that the shipped code could not regenerate the stored series, so the build is suspect, but the kill stands as built. **Consequence for r9, r4 and events3 together:** the non-hierarchical three-body regime takes one representation, the rotating binary doll (`docs/law.md`).
- **1 October, autonomous lab (22:50 run):** the redteam and taleb lenses reached silver in checking, so the lab stays at once a day.

- **30 September, r8 v2 (encounters): KILL of element-sort, shear-grid and hier-bounds; silver-quality work.**
  - **Measured, and reproduced bit for bit:** every candidate finds every encounter. Work per encounter is 786 for element-sort (1.1 events per body per orbit), 2.6×10⁴ for hier-bounds and 4.9×10⁵ for shear-grid, with exponents about 2 in N at fixed σ_e.
  - **The premise:** cost follows the candidate set (pairs whose orbits overlap), not ρ.
  - **The integrator's error:** `cheap` (≤ 10 per encounter) was unpassable over 20 orbits for any algorithm, because touching each candidate pair once (1.7M on belt 0) already dwarfs the encounters (427).
  - **The checker found the truth leaks:** conjunction-less encounters, about 0.5–6% of the reference's list and 78% in an adversarial belt.
  - **Next:** judge steady-state work per orbit (→ 0), with each pair paid once per element change. The candidate representation: a pair's miss distance at successive conjunctions is quasi-periodic, so its next close conjunction is a Diophantine approximation (continued fractions), plus group certificates that pay once while envelopes are disjoint.

- **30 September, r3 v3 (two-body doll): silver; KILL of eob-doll on the handoff criterion only.**
  - **Confirmed:** ν enters only through the energy map (1PN), with assists at 64/64.
  - **The kill:** the handoff exponent is 0.233 against 0.2, measured against a chaotic float reference at a 10⁻¹¹ error level. That is the integrator's criterion weakness again: judge a conserved quantity with a noise floor, as B12 does.
  - **Not gold:** no predictions.md, and an undisclosed redefinition of the assist metric.
- **30 September, r8 (encounters): VOID** (the author ran out of time). Its pre-registered predictions expect both broad phases to cost orders of magnitude more than the encounters. The integrator questions the premise: see the focus list.

- **30 September, library lens: lead.** Its claim (binary thresholds make faction aggregates 6–17× tighter) inverted under a fair anchored control; the checker was right. Off focus: AI is off the plan. What survives is the count-quantum rule n* = (1/ε)², folded into B5's notes.

- **30 September, r4 v2 (resonance): KILL of arc-integrated kicks (g8, g16, g8-half); silver-quality work.**
  - **What it showed:** the checker refined the kick windows toward zero. The layer converges to the first-order-in-μ solution, which still over-pumps e about 2× and lets the resonant angle circulate. The failure is structural, not a matter of quadrature or window size.
  - **Design consequence:** near resonance, the law needs phase feedback. The next configuration is the resonant normal form, a 1-DOF integrable generator per resonant pair (`docs/law.md`, kicks).
  - **Flagged:** the author patched truth JSONs without disclosing it, and misread the rung's w₂ case. The metric degenerates at exact commensurability, so future rungs detune or use libration amplitude.

- **29 September, r2 (carry width): KILL of sd16, sd24 and sd32.**
  - **What it showed:** a 32+32-bit pair holds float64 increments exactly (zero phase error). Carries cannot recover information below their own resolution. Kicks on the law's own grid accumulate exactly at any width.
  - **Integrator's error:** two criteria demanded trajectory identity with float64 (conjunction order; the worst-seed kick-residual exponent), which the checker proved unpassable.
  - **Fix:** positive controls in `verdict.py`, and criterion-writing rules in the README.
  - **Design consequence:** increments and kicks are integers native to the law, so widths are set by behaviour (r1 and the law's gates), not by matching floats.
- **29 September, premise red-team: silver.**
  - **Adopted:** the rule that resonance kills averaging (design §3, rung r4); r3 v2's truncation fix; Clohessy–Wiltshire is first order only; Minsky's map is a conjugated rotation.
  - **Why silver, not gold:** its model B, the half claiming "kicks survive", was a dense integration, not the design's kick layer. Claims must be measured on the design's cheap path.
  - **Why it was good work:** a converged truth, predictions written before the decisive run, the rung gap audited, and honest misses.
