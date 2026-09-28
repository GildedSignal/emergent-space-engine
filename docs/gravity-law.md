# Gravity law `es-lattice-gravity-v0`: design and the step 2 contract

Status: design. The step 2 gates below were frozen on 28 September 2026 (H0184) and amended before any gate run (H0187). Plan context: [HANDOFF.md](HANDOFF.md), steps 2–4.

## Space flows: river coordinates

Around a mass M we use Painlevé–Gullstrand coordinates, also called the river model of a black hole (Hamilton and Lisle, 2008). With G = c = 1:

    ds² = −dT² + |dx − β dT|²,   β(x) = −√(2M/r) · x/r   (space flows inward at the escape speed)

- Spatial slices are flat.
- T is the proper time of observers falling from rest at infinity.
- ∂_T is a Killing vector, and T differs from Schwarzschild t only by a function of r.

This one choice makes the lattice's special relativity serve unchanged as the local physics of gravity:

1. **Locally, gravity is a Galilean shift.** Let u = v − β be the velocity relative to the flow. At any point, the metric in X = x − βT is exactly Minkowski. So the lattice's relativistic contact law and speed limit apply unchanged to u. Nearby bodies see only the tidal difference in β.
2. **Clocks come from the same Lorentz factor:** dτ/dT = √(1 − |u|²). A static observer (u = −β) gets √(1 − 2M/r).
3. **Distances at the same T are flat distances.** Coordinate discs are physical discs on the slice, so contact geometry is unchanged.
4. **Conserved quantities of a free body** (per unit mass): the Killing energy E = γ_u (1 + β·u) and the angular momentum L = γ_u (x × v), with γ_u = 1/√(1 − |u|²). A contact happens at one point, so its local 4-momentum conservation conserves the pair's E and L.
5. **Horizon.** |β| = c at r = 2M, and inside it every light cone points inward. Crossing takes finite T. A body is absorbed at the first chronon with r ≤ 2M, and its E and L go to the source's ledger. Nothing is computed past the horizon.
6. **Coordinate light speeds** fill the disc of radius c around β, so they reach c + |β| inward. Dependency bounds and light-cone finality must use c + max|β| over the region, not c.
7. **With no source**, β = 0 and the law is today's lattice exactly.
8. **Spin (step 7).** Kerr takes Doran coordinates: a river that also twists. Keep a spin parameter in the interfaces; v0 fixes it at 0.

**Free motion.** Between events a body follows the geodesic of its parent through its last anchor. With no parent, that geodesic is a straight line. Events (contacts, kicks, commands) are the only moments state changes. Queries and observation never change state.

## Step 2 scope

One static source of mass M at the origin, and test bodies and light rays (no back-reaction) in the equatorial plane. No contacts, kicks or other sources yet.

**Units.** These are the lattice's units:
- Positions X are in position quanta (1/Q light-chronon).
- Time T is an integer number of chronons.
- Velocities are in quanta per chronon, and c = Q.
- M is an integer: GM/c² in quanta.
- In these units the metric reads

      ds² = −Q² dT² + |dX − β dT|²,   β = −Q √(2M/r) · X/r  (quanta per chronon),

  with r in quanta. A velocity k corresponds to v/c = k/Q.
- **Ranges** (amended before any gate run, H0187): |x| ≤ 2^96, 1 ≤ M ≤ 2^80, Q ≤ 2^40, and |T − T0| ≤ 2^80. The interface stays i128. Intermediate products exceed i128, so evaluators use arbitrary-width integers.
- **Scale table,** at Q = 2^40 (chronon 83 ps, quantum 2.27·10⁻¹⁴ m):

  | Object | Exponent (base 2) |
  |---|---|
  | Earth: M | 37.5 |
  | Earth: low orbit | 68 |
  | Sun: M | 56 |
  | Sun: 1 AU | 82.4 |
  | Sun: Neptune's orbit | 87 |
  | 10 M☉ hole: M | 59 |
  | Sgr A*: M | 78 |
  | Sgr A*: r = 100M | 85 |
  | 1 year | 58.4 |
  | 1 Myr | 78 |

  Galactic distances (about 2^115) are beyond a single parent's formula. They belong to the step 3 hierarchy with wide origins.

**The canonical position:**

    x(T) = ⌊X(T)⌋ component-wise,

where X(T) is the exact position at time T, in quanta, of the geodesic with X(T0) = x0 and:

- **timelike:** dX/dT(T0) = k0, in quanta per chronon, with |k0 − β(x0)| < Q decided exactly;
- **null:** k0 is a nonzero integer direction of the velocity relative to the flow, so dX/dT(T0) = β(x0) + Q·k0/|k0|. A whole-number k0 can almost never sit exactly at c relative to an irrational flow, so a light ray's anchor gives a direction rather than a velocity.

It must satisfy these conventions:

- x(T0) = x0 exactly.
- **Symmetries hold for the continuous X, before flooring.** A radial anchor (x0 × k0 = 0) keeps X on its line through the origin, but the floored integers may leave that line (for example M = 1, Q = 25, x0 = (30, 40), k0 = (−3, −4), T = 1 gives (26, 35)). Motion along a coordinate axis keeps the other coordinate exactly 0.
- **The floor must be a fixed function of the anchor, and it must always terminate.** The canonical value is the mathematical floor when a specified certified evaluation decides it. That evaluation uses a fixed precision schedule, fixed operations and fixed rounding directions, and ends at a stated maximum precision. If the maximum precision cannot decide, the value is a stated deterministic function of that final certified interval. The implementer writes this rule down exactly in the crate docs, before the gate run. The rule is part of the law. Refusals are not allowed.
- **Absorption.** Let T_h be the continuous time at which the geodesic first crosses r = 2M. For every integer T ≥ T_h, `position` returns `Absorbed { chronon: ⌈T_h⌉ }`, decided by the same certified scheme. This definition is needed because the geodesic can reach the singularity before the next integer time: M = 1, Q = 25, x0 = (30, 40), k0 = (−3, −4) crosses at T_h = 496/75 and ends at 20/3. After T_h, `proper_time` stays at its value at T_h.
- **Leaving the range.** From the first integer T at which a coordinate of X(T) exceeds ±2^62, `position` returns `OutOfRange { chronon }`. In the engine, a body is handed to another region or parent long before that.
- **Before the anchor.** Queries with T < T0 return `Before`. Evolution is forward only.
- **Chord velocity for contact bins** (used in step 4): k(T) = x(T) − x(T − 1).

**The interface** (crate `emergent-geodesic`, no dependency on other workspace crates). Validation happens once, at construction. Queries cannot fail:

```rust
pub struct Field { pub m: i128 }                                   // static source at the origin, spin 0
pub struct Anchor { pub t: i128, pub x: [i128; 2], pub k: [i128; 2] }
pub enum Motion { Timelike, Null }
pub enum At { Free([i128; 2]), Absorbed { chronon: i128 }, OutOfRange { chronon: i128 }, Before }
pub enum AnchorError { /* out of range, r ≤ 2M, timelike not below c or null not at c relative to the flow, … */ }
/// Opaque and immutable. It holds the validated anchor and its certified invariants.
pub struct Geodesic { /* private */ }
impl Geodesic {
    pub fn new(field: Field, q: i128, anchor: Anchor, motion: Motion) -> Result<Geodesic, AnchorError>;
    /// Canonical: exact floors under the documented rule. Floats never decide it.
    pub fn position(&self, t: i128) -> At;
    /// Diagnostics (f64, not canonical): E, L, orbit class, p, e, radial period in T and in τ,
    /// periapsis advance per radial period.
    pub fn orbit(&self) -> Orbit;
    pub fn proper_time(&self, t: i128) -> f64;
}
```

This contract was corrected twice before any implementation, after Astra's preflights. No threshold changed (H0184).

**Second evaluators** (GPU, fast paths). The canonical rule is the ladder written in `crates/geodesic/README.md`: a fixed precision schedule, fixed operations and rounding directions, fixed iteration limits, and a final-midpoint rule. It is therefore a fixed function of the integer inputs. Any other evaluator must either reproduce it operation for operation, or return a floor only when its own certified enclosure, widened by the ladder's proven maximum final width W, contains no integer. The crate states W and its proof. Otherwise it defers to the ladder.

## Step 2 gates (frozen)

Every test runs in under 60 s, on the M1, in release.

- **G2.1 Canonical exactness.** `position` must equal an independent reference evaluator on every case of a frozen adversarial set. The reference is written separately and shares no code with `emergent-geodesic`. It uses a different formulation at least twice the working precision, and refines until its floors are stable.
  - Cases:
    - ≥ 20,000 random (anchor, T) pairs across the classes: bound, unbound, plunging, radial and null;
    - ≥ 1,000 constructed cases whose exact coordinate lies within 2^-40 of an integer;
    - T = T0;
    - near-circular orbits;
    - orbits near the innermost stable circular orbit and near the separatrix (whirl orbits);
    - orbits near the horizon;
    - T up to 10^4 radial periods ahead.
  - Pass: 100% agreement. A case the reference cannot settle counts as a failure of the gate, not as an exclusion.
  - **Climb, don't jump** (amended before any run). Rungs run in order, and each must pass before the next:
    - R0, exact answers: T = T0; motion along an axis; far-field hops whose proven deviation from the straight line is below the straight line's distance to the nearest integer, which must floor to the straight line;
    - R1: radial infall and circular cases;
    - R2: an exhaustive small world (Q = 25, M = 1, x ∈ [−8, 8]², k ∈ [−4, 4]², T − T0 ∈ 1..8, every valid anchor);
    - R3: 100 random cases per class;
    - R4: the ≥ 1,000 near-integer cases;
    - R5: the full set.
  - **Reference answers are precomputed** by the judge (python-flint/Arb ball arithmetic), hashed and frozen as evidence before the evaluator's first gate run. The 60 s cap applies to the comparison, not to the precomputation.
  - **Fallback cases.** A test-only reduced schedule (16/32/64 bits) forces the final-midpoint rule on near-integer cases. There the result must be one of the two integers adjacent to the true value's nearest integer boundary, and identical across 3 runs and across thread counts.
  - **Planted bugs.** Before a gate counts, it must fail on its planted bug in a throwaway branch:
    - G2.1: a flipped outward rounding in one chart;
    - G2.2: the river-time correction's sign flipped;
    - G2.3: a stateful cache;
    - G2.4: an off-by-one absorption chronon.

- **G2.2 Oracle agreement.** The diagnostics must agree with the H0178/H0183 oracle functions evaluated at the anchor's own (p, e) or impact parameter:
  - periapsis advance per orbit, radial period in coordinate time and radial period in proper time: relative difference ≤ 10^-9;
  - static and circular clock rates: ≤ 10^-12;
  - light deflection: ≤ 10^-8;
  - Shapiro delay: ≤ 10^-7.
  - Measured from integer positions alone, the advance per orbit must fall within ±4/r_p radians of the oracle, where r_p is in position units.
- **G2.3 Observation invariance.** On 1,000 cases, `position` at T_final is bitwise equal whether or not 100 intermediate queries are made first.
- **G2.4 Horizon.**
  - Radial infall from rest (k0 = 0) at r0 ∈ {10M, 100M} is absorbed at ⌈T_h⌉, with T_h from the closed-form infall time the reference computes.
  - For timelike E = 1 anchors moving inward on the radial branch connected to infinity (outside the potential barrier): |L| ≤ 4M·(1 − 10^-6) is absorbed, and |L| ≥ 4M·(1 + 10^-6) escapes.
- **G2.5 Cost**, on one M1 performance core:
  - **G2.5a, natural anchors** (the random classes of G2.1): median ≤ 50 µs and p99 ≤ 500 µs per `position` call. Reason: 1M orbiting ships, each kicked by tides every few minutes, then cost ≤ 0.3 core at 1× real time.
  - **G2.5b, every case including near-integer ones:** max ≤ 5 ms.
  - Rendering uses non-canonical floats and does not count. Measure under the conditions the player will actually have, with heat and load included, and record the thermal, power, swap and load state (fanless MacBook Air M1, 7-core GPU).

## Division of the work

- **`crates/geodesic`** (gpt-6-astra): the canonical evaluator. It covers the orbit classification and the elliptic-function forms of r, φ and T along timelike and null Schwarzschild geodesics in river coordinates, the inversion T → orbital phase, certified integer interval arithmetic and the written floor rule.
- **`xtask` step 2 gate** (gpt-6-sol): the independent reference evaluator, the adversarial case set and the G2.1–G2.5 harness, reusing the oracle's functions.
- **The integrator:** this contract, the reviews, the merge and the journal.

## Later steps (direction, not frozen)

- **Step 3: many bodies.**
  - The parent is the dominant source, chosen by a dimensionless ratio with hysteresis.
  - A body follows its parent's river; a moving parent carries its river along.
  - Other sources act as tides: multipole moments stored as polynomials in time and read at the retarded time. The tides accumulate in carries, and an integer kick is applied each time one velocity quantum builds up.
- **Step 3: the kick rule**, measured by the math researcher's probe (`artifacts/evidence/reanchor-probe-20260928/`):
  - The unknown acceleration is integrated continuously along the exact formula. A kick falls at the first integer chronon where its rounded integral changes.
  - Re-anchoring rounds by error feedback on the carried E and L. This stayed bounded at 0.7 quanta, where plain rounding random-walks and floor rounding drifts L secularly.
  - Known tides are averaged into the formula (Lie–Deprit).
  - Integer splits between bodies use largest-remainder apportionment.
  - Messages between regions are commutative monoids: carries under +, frontiers under min.
- **Step 4: the law in the engine.** Per chronon, x(T) comes from the formula. Contacts are resolved in the flow frame, with a canonical integer β at the contact (exact isqrt of 2MQ²/r). The speed limit becomes |k − βQ| ≤ Q, and finality uses c + |β|.
