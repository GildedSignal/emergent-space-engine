# Gravity law `es-lattice-gravity-v1`: contract

Status: **DRAFT, not frozen.** The integrator freezes it after probe 2, showing Julien the gates first; no gate below binds until then. Drafted 29 September 2026 (H0195) and amended the same day for his decisions, GLM's red-team and premise probe 1 ([evidence](../../artifacts/evidence/gravity-v1-freeze-20260929/PROVENANCE.md)). The v0 contract (exact continuum floors, H0184–H0194) is retired: its evaluator (`crates/geodesic`), the Arb judge (`artifacts/evidence/g2-reference-20260928/`) and `xtask gr-oracle` now serve as the **oracle**, which measures behaviour. None of them is the implementation.

## Principles

- **The law is a cheap, local, fixed integer algorithm,** like the lattice's collision law. "Exact" means bit-identical on every machine, thread count, work partition, silicon and event order. It does not mean equal to continuum GR.
- **The oracle is exact GR.** Gates judge behaviours and error type against it, never bitwise continuum floors.
- **Gravity is a field held by cells; multipoles are the mechanism,** including the aggregate mass of ships (Julien: "they have a lot of mass cumulated they can't just be dismissed like that"). One mass, two and N run the same code.
- **Only changes cost; no per-body clock.** Julien: "you don't advance a ship tick by tick"; "we only care about changes". A body pays only at events: a cell crossing, a certificate expiry, a contact, a command.
- **Observables are derived on demand.** Clocks, redshift, lensing and delays are computed when queried, never evolved.
- **Any silicon.** The GPU may run canonical work wherever it is bit-identical to the CPU (B8).

## Space flows (river coordinates)

In lattice units (positions in quanta, time in chronons, c = Q):

    ds² = −Q² dT² + |dX − β dT|²

β is the flow of space. For one static mass M: β = −Q √(2M/r) · X/r.

**The equations the law discretizes** (red-team finding 1: without them the gates would test whatever gets written). With u = v − β the velocity relative to the flow, γ_u = Q/√(Q² − |u|²), and p = γ_u·u the momentum per unit mass:

    H = Q √(Q² + |p|²) + β(X)·p        dX/dT = u + β        dp/dT = −(∇β)ᵀ p

- u = Q·p/√(Q² + |p|²), so |u| < Q for every massive body by construction. Light is the null case, H = Q|p| + β·p, with |u| = Q.
- **Conserved in a static single-source field:** E = H = γ_u (Q² + β·u) and L = X × p. In the weak field, E ≈ Q² + ½|v|² − MQ²/r.
- **The split probe 1 validated:** H = A + B, with A = Q√(Q² + |p|²) (a straight drift in the flat sheet) and B = β·p (the river: it carries X along β and focuses p by −(∇β)ᵀp). Both integrate exactly for one mass. A kick that only tilts the velocity and keeps u has the wrong limit (no stable circular orbits, zero light deflection); it is a negative control.
- **Clocks:** dτ/dT = √(1 − |u|²/Q²) = Q/√(Q² + |p|²), on demand.
- **The horizon** is where |β| = Q (r = 2M). **Coordinate light speeds** fill the disc of radius Q around β, so dependency bounds use Q + max|β|.
- **With no source,** β = 0 and the law is today's lattice exactly (B0).

## The law (v1)

**Cells.** One quadtree, built by a fixed integer rule from the field, never from a body's state. A cell's side is a power of two set by the field's curvature length ℓ at the cell (ℓ ∝ r for one mass) times a fixed dyadic fraction κ: cells are large where the field is flat and small where it bends. These cells are part of the law. A work partition (threads, regions, CPU or GPU) is not.

**Cell records.** Each cell holds:
- the integer mass moments (monopole up to a fixed order P) of what it contains, as sums that commute: exact and independent of order. Every body deposits, ships included, so a fleet's aggregate is a source;
- a **field record**: the local expansion of the field to order P from a hierarchical multipole solve over the cells (moments up, local expansions down), with moments read at the retarded time, and a certificate "valid until the source moments change by more than ε", with ε a fixed integer threshold. With one static mass, the certificate never expires.

**Open, the first design question: what the cells add.** Moments and the potential Φ add linearly; the flow does not (β ∝ √M, so β₁ + β₂ is not the two-mass flow). The law text must give the rule from a cell's expansion (Φ and its derivatives) to the local β. It must reduce exactly to the Schwarzschild flow for one mass, and be curl-free for static sources: in the Newtonian limit dv/dT ≈ −∇Φ − v × (∇×β), and static masses exert no such velocity-dependent force. The two-mass rung judges it against the 1PN oracle.

**Motion: events only.**
- The events are a cell crossing, a field-certificate expiry, a contact (from step 6) and a command. Nothing is scheduled between them.
- Inside a cell, the path is the A/B split with a **constant step fixed by the cell** (from its side and field record), never by the body. It runs from the entry crossing to the exit crossing, which is found exactly. The sub-steps are the in-cell solution: they are not events, and nothing is stored between them.
- **Or a generator.** A body in a static single-source field may instead carry an analytic generator (its orbit as a fixed integer formula), re-anchored only at events, if it passes the same gates.
- At each event, the integer state is re-anchored with error-feedback carries on p, and hence on E and L.
- **Light** follows the same law with |u| = Q. Its path is clipped at every cell boundary, so no chord can jump over a lens.
- **The horizon:** a body whose in-cell path reaches r ≤ 2M, tested along the path and not only at sub-step ends, is absorbed at that chronon. Its E and L go to the source's ledger, and nothing is evaluated inside.
- **Queries** evaluate the path and never change state.

**Body state:** integer X and velocity k relative to the flow (as in lattice v1, so β = 0 is today's lattice), mass, cell, the carries on p, and the chronon of its last event. An integer k cannot hold |u| = Q off-axis (red-team finding 5), so the law text states how light is held.

**The implementer writes the law in the crate before the first gate run:** κ, P, the β rule, the cell's step rule and the in-cell order, the exit-root rule, the rounding recipe, the light representation and the horizon test. That text is the law. It must lie inside the envelope probe 2 measured; otherwise, re-probe first (red-team finding 11).

## Rungs (same code at every rung; each passes before the next)

1. **One static mass,** test bodies and light, in the equatorial plane. Ranges: per component |x_c| ≤ 2^96, 1 ≤ M ≤ 2^80, Q ≤ 2^40, |T − T0| ≤ 2^80 ([universe-quanta.md](universe-quanta.md)); intermediates may use wide integers.
2. **Two masses:** a binary, then a mass and a fleet whose aggregate moments are a source. Oracle: 1PN two-body, after a new protocol on unseen cases replaces the retained e = 0.5 period failure (H0183).
3. **N bodies:** clusters and galaxy-like populations with ships, moving sources included (retarded moments with source-velocity terms). Oracle: 1PN N-body, and statistics over seeds.
4. **Scale:** cost against N up to 10^9 (B10).

## Premise probes (float, GLM)

**Probe 1 (done)** tested the H0195 draft's per-body step Δ = η·r^{3/2}(current state). Precession, E = 1 capture and deflection at b = 10M passed at 1% (order 4 with 2–4 orders of magnitude of margin). Energy growth killed it: exponents 0.47–0.98 over 10^3–10^4 orbits, while a fixed-step control stayed flat (1.8×10^-8 at order 2, 2.2×10^-10 at order 4). Distant light jumped the lens in one 15,600-long chord, and orbits took 407–502 steps at η = 1/64, 2% under B9. It kills the state-dependent step rule, never the method (principle 9). [probe-out.md](../../artifacts/evidence/gravity-v1-freeze-20260929/probe-out.md)

**Probe 2 (the cheapest falsifier, required before the freeze; running).** A float re-probe of cell-owned step rules on radial shells [2^k, 2^{k+1}): C1, a shell-constant step with exact advance to each shell boundary; C2, the same with time-symmetric switching; C3, one fixed step as the control. Kill criteria, frozen before the run in `artifacts/runs/gravity-v1-reprobe/prompt.md`:
- energy: a growth exponent above 0.2, or a maximum |ΔE/E| above 10^-6, over 10^4 orbits at p = 20M (e = 0.2 and 0.5);
- precession: no η ≤ 1/32 within 1% at both p = 20M and p = 1000M;
- distant light: photons anchored at r = 10^4 M with b = 10M and 30M more than 1% from GR;
- capture: any misclassification at L = 4M(1 ± 0.01);
- cost: more than 512 events per orbit at p ≥ 20M.

The integrator folds the cheapest passing configuration into this contract. The red-team's other edges stay unprobed so far: p = 10M, e up to 0.9 and a near-separatrix whirl, periods, horizon timing, the tilt-only negative control, and two masses under the chosen β rule.

## Gates B0–B10 (proposed; frozen after probe 2)

Every test runs in under 60 s, measured the way the player runs it, with the thermal, power, swap and load state recorded. **The cases:** the oracle's G2.2 anchors (bound, (p − p_sep)/p ≥ 10^-4), its G2.4 horizon cases, its light anchors, and the straddling cases below. **Many seeds:** each behaviour gate B2–B6 also draws at least 256 seeds from a frozen sampler over the dimensionless numbers (p/M, e, b/b_c, |L|/4M, M/Q), and passes on the whole distribution, never on one seed's data. **Rungs** within step 1: circular → radial infall → eccentric → light → horizon → long runs.

| Gate | What must hold |
|---|---|
| **B0 Flat reduction** | With no source, a lattice v1 scene run through the gravity code reproduces lattice v1's digests |
| **B1 Error type** | Over 10^4 orbits, on at least 8 seeds: the growth exponent of \|ΔE\| and \|ΔL\| is ≤ 0.2 (fitted over log-spaced windows on the last 90% of the run), and no excursion changes a behaviour: bound stays bound, and the law's own periapsis and apoapsis stay within 1% of their first-orbit values |
| **B2 Precession** | Prograde, and \|Δφ_law − Δφ_GR\| ≤ 1% of Δφ_GR + 10^-6 rad per orbit for p ∈ [10M, 10^4 M]. Below 10M: zoom-whirl present, with the whirl count within ±1 of the oracle's |
| **B3 Periods** | The radial period in coordinate time is within 0.1%, with periapsis found on the path by a stated rule |
| **B4 Light** | Deflection within 1% for b ≥ 10M, light anchored at r ≥ 10^4 M included; capture iff b < 3√3·M outside a ±1% band, with cases at b/b_c ∈ {0.9, 0.97, 1.03, 1.1} |
| **B5 Capture** | E = 1 inward: absorbed iff \|L\| < 4M outside a ±1% band, with cases at \|L\|/4M ∈ {0.5, 0.9, 0.97, 1.03, 1.1, 1.5}. Every old E = 1 anchor sat inside the band |
| **B6 Horizon** | Absorbed at the first chronon the path reaches r ≤ 2M, and the absorption chronon is within one of that cell's steps of the oracle's ⌈T_h⌉; nothing is evaluated at r < 2M |
| **B7 Derived clocks** | An identity, not a band: the rate derived at a state equals the oracle's formula at that state (static √(1 − 2M/r), circular √(1 − 3M/r)) to one isqrt rounding. Rates are never evolved |
| **B8 Determinism** | Bit-identical across 3 runs, 1, 4 and 8 threads, CPU and GPU, different work partitions and event orders. The law's cells are part of the law. Queries never change results |
| **B9 Cost per body** | Isolated at p ≥ 10M, per azimuthal orbit (2π): events plus in-cell steps ≤ 512, with field evaluations per step stated; median ≤ 2 µs per step on the M1, CPU or GPU |
| **B10 Cost against N** | Frozen scenes of 10^3 to 10^6 bodies (stars, planets and ships), each under 60 s. Fit cost per game second against N and extrapolate to 10^9: Julien's "a billion", not "a million". Passes iff the fitted exponent is ≤ 1.1 and the 10^9 extrapolation fits the M1 (all cores plus the GPU) at a real-time factor ≥ 1× on the frozen reference scene. Memory per body is reported and extrapolated too; the approved plan's 4 GiB is an open budget |

## Division of the work

- **The law's author** owns the written law and `crates/gravity`: cells, multipoles, the β rule, the in-cell solution and the Metal path. Astra, or Claude Opus while Codex's weekly usage is above 75% (80% on 29 September), with Astra reviewing.
- **Sonnet:** `xtask behave` (built; gates G1–G6 with planted laws). This contract is superseded by `docs/law.md` once that exists.
- **GLM:** the red-team and probe 1 (done), probe 2 (running), then mutants.
- **The integrator:** this contract and its freeze, adjudication, merges and the journal. Julien can veto the gates before the first run.

## Later (direction, not frozen)

- **One engine:** the law enters the engine. Contacts happen in the flow frame, with the local β taken from the cell's field (for one mass, an exact isqrt of 2MQ²/r).
- **Kerr:** Doran flow, with twist. **Inspiral:** field energy loss. **Merger:** a single event.
