Reading prompt from piped stdin (waiting for EOF; ctrl+c to abort)…
Working...
Ranked prior art for the step rule (all claims verified at source today except UNVERIFIED ones):

1. **Logarithmic-Hamiltonian / Sundman transform** — Preto & Tremaine 1999 (arXiv:astro-ph/9906322); Mikkola & Tanikawa 1999 (MNRAS 310, 745).
   Time becomes a canonical coordinate; constant step in fictitious time with dt/ds = 1/(T+B); symplectic in extended space, physical steps adapt. Map to us: g = dynamical time of the **cell's field** (from its moments); the cell owns g, Δt = g·h falls out at events; exact for Kepler, near-exact for our split river pieces.
   Fails: g must be smooth; time-dependent potentials perturb the energy shell. Test: criterion-2 energy run with constant-h log-H river split — falsified if E exponent > 0.2 (expect the fixed-Δ flat ~1e-8 behavior).
2. **Time-symmetric implicit steps** — Hut, Makino & McMillan 1995 (ApJ 443, L93).
   h = ε[σ(yₙ)+σ(yₙ₊₁)]/2, fixed-point iterated → self-inverse map. Map: σ read from the cell's certificate at both event endpoints.
   Fails: still not symplectic; iteration tolerance is an irreversibility source. Test: 10⁴-orbit energy run with symmetrized σ; falsified if exponent > 0.2.
3. **Hierarchical splitting, individual steps (HOLD/HUAYNO)** — Pelupessy, Jänes & Portegies Zwart 2012 (arXiv:1205.5668).
   Split Hamiltonian by interaction strength into a tree; each node steps itself; kicks exchange on the slower partner's step; pairwise momentum exact. Map: this is our cell/multipole hierarchy verbatim; certificate expiry = the slow partner's kick.
   Fails: tree rebuild after encounters; steps still a staircase. Test: binary + distant third body, steps only from the hierarchy; E bounded over 10⁴ orbits.
4. **Power-of-two block rungs** — GADGET-2, Springel 2005 (MNRAS 364, 1105); rung mechanics UNVERIFIED at source today.
   Δ = Δmin·2^k; promotion/demotion only at kick boundaries. Map: the contract's cell clipping made canonical — Δ is a staircase of constants owned by the cell.
   Fails: rung transitions inject non-symplectic kicks → secular drift. Test: staircase Δ = 2^⌊log₂(η·r^3/2)⌋ in the energy probe; falsified if exponent > 0.2.
5. **Kepler-drift maps ("drift in parent's field")** — Wisdom & Holman 1991 (AJ 102, 1528).
   Bodies move exactly under the dominant field; interactions kicked at shared steps. Map: step 2 already is this (exact PG river drift); the step becomes the next cell boundary — geometry, not body state.
   Fails: encounter regions need switching (Chambers 1999 hybrid). Test: distant photon r₀ = 10⁴ with boundary-clipped steps; falsified if b-invariant deflection drift > 1%.
6. **Asynchronous variational integrators** — Lew, Marsden, Ortiz & West 2003.
   Each element keeps its own Δt in a priority queue; a firing element drifts shared nodes to event time and applies only its impulse; exact momenta. Map: literally "cells own the step"; bodies are nodes shared by cells — our event core as a priority queue.
   Fails: energy not exactly bounded when Δt is Courant-chosen, not variationally. Test: body crossing a 16:1 step-ratio cell pair; E bounded over 10⁵ crossings.
7. **Event-driven safe time** — Lubachevsky 1991 (J. Comput. Phys.); parallel bounded-lag version 1992.
   Each region executes only provably-safe events via an earliest-possible-influence bound; zero ticks. Map: our dependency bound Q + max|β| is exactly his lookahead d(i,j); events = crossing ∪ expiry ∪ contact ∪ command.
   Fails: event storms in dense clusters; lookahead collapses when regions touch. Test: events/orbit vs p for crossing-limited steps; falsified if > 512 at p = 10M (B9).
8. **Bit-reversible integer MD** — Levesque & Verlet 1993 (J. Stat. Phys. 72, 519).
   Integer positions, velocity = position difference; exactly invertible, roundoff-proof. Map: the rounding recipe for our integer law, not the step rule.
   Fails: uniform fixed step only — per-body-per-chronon cost violates "no ticks". Test: reversal test passes trivially; the cost count is the falsifier.
9. **Games, patched conics** — KSP/Elite: on-rails conics between SOI-boundary events, warp gated by the next transition (UNVERIFIED at sources).
   Shipped proof that analytic drift + geometry events suffices at scale; fails perturbations (n-body wrong — the Principia mod exists to fix it). Test: none; treat as evidence, not method.
10. Time-polynomial multipoles, lattice-gas gravity: no established gravitational primary source found (UNVERIFIED) — step 5's "moments polynomial in T" is frontier, not settled art; don't lean on it for the freeze.

**Recommendation.** One construction composes 1+3+5+7: the cell owns the step and the adaptivity lives in time, not the map — constant fictitious step h_s per cell on power-of-two rungs (HOLD-style exchange between hierarchy levels), g = the cell field's dynamical time; body events = cell crossing, rung boundary, certificate expiry, contact, command; light's g is pure geometry (cell size / Q).

**What we are getting wrong.** The literature's sharpest result is negative: a step that is an explicit function of the body's instantaneous state is never symplectic — Calvo & Sanz-Serna 1993 (SIAM J. Sci. Comput.): F\*ω = ω + dh∧dH, so h = h(H) or the map is not symplectic — even inside a self-adjoint composition; our probe's 0.47–0.98 exponents are that theorem in action. Every working scheme moves adaptivity into extended time, the hierarchy, or the mesh. And photons have no dynamical time: only geometry can limit light's step, which our own probe found at r = 10⁴.
