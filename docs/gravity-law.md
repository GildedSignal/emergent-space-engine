# Gravity law `es-lattice-gravity-v0`: design and the step 2 contract

Status: design. The step 2 gates below were frozen on 28 September 2026 (H0184), before any gravity code ran. Plan context: [HANDOFF.md](HANDOFF.md), steps 2–4.

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
- Positions are integers in 1/Q light-chronon.
- A velocity k is in position units per chronon, with c = Q.
- Time T is an integer number of chronons.
- M is an integer: GM/c² in position units.
- Ranges: |x| ≤ 2^62, 1 ≤ M ≤ 2^40, Q ≤ 2^40, and |T − T0| ≤ 2^62. Use i128 internally.

**The canonical position:**

    x(T) = ⌊X(T)⌋ component-wise,

where X(T) is the exact position at time T of the geodesic with X(T0) = x0 and dX/dT(T0) = k0/Q, a timelike or null anchor. It must satisfy these conventions:

- x(T0) = x0 exactly.
- Radial anchors (x0 × k0 = 0) stay exactly on their line through the origin.
- **The floor must be a fixed function of the anchor, and it must always terminate.** The canonical value is the mathematical floor when a specified certified evaluation decides it. That evaluation uses a fixed precision schedule, fixed operations and fixed rounding directions, and ends at a stated maximum precision. If the maximum precision cannot decide, the value is a stated deterministic function of that final certified interval. The implementer writes this rule down exactly in the crate docs, before the gate run. The rule is part of the law. Refusals are not allowed.
- **Absorption:** the first integer T > T0 with r(T) ≤ 2M, decided by the same scheme. After it, `position` returns `Absorbed`.
- **Chord velocity for contact bins** (used in step 4): k(T) = x(T) − x(T − 1).

**The interface** (crate `emergent-geodesic`, no dependency on other workspace crates):

```rust
pub struct Field { pub m: i128 }                                   // static source at the origin, spin 0
pub struct Anchor { pub t: i128, pub x: [i128; 2], pub k: [i128; 2] }
pub enum Motion { Timelike, Null }
pub enum At { Free([i128; 2]), Absorbed { chronon: i128 } }
/// Canonical: exact floors under the documented rule. Never refuses, never uses floats to decide.
pub fn position(f: &Field, q: i128, a: &Anchor, m: Motion, t: i128) -> At;
/// Diagnostics (f64, not canonical): E, L, orbit class, p, e, radial period in T and in τ,
/// periapsis advance per radial period, proper time elapsed at t.
pub fn orbit(f: &Field, q: i128, a: &Anchor, m: Motion) -> Orbit;
pub fn proper_time(f: &Field, q: i128, a: &Anchor, t: i128) -> f64;
```

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
- **G2.2 Oracle agreement.** The diagnostics must agree with the H0178/H0183 oracle functions evaluated at the anchor's own (p, e) or impact parameter:
  - periapsis advance per orbit, radial period in coordinate time and radial period in proper time: relative difference ≤ 10^-9;
  - static and circular clock rates: ≤ 10^-12;
  - light deflection: ≤ 10^-8;
  - Shapiro delay: ≤ 10^-7.
  - Measured from integer positions alone, the advance per orbit must fall within ±4/r_p radians of the oracle, where r_p is in position units.
- **G2.3 Observation invariance.** On 1,000 cases, `position` at T_final is bitwise equal whether or not 100 intermediate queries are made first.
- **G2.4 Horizon.** Radial infall from rest at r0 ∈ {10M, 100M} is absorbed at the chronon the reference computes from the closed-form infall time. At E = 1, L ≤ 4M·(1 − 10^-6) is absorbed and L ≥ 4M·(1 + 10^-6) escapes.
- **G2.5 Cost.** Over the G2.1 set, on one M1 performance core: median ≤ 50 µs and p99 ≤ 500 µs per `position` call. Reason: 1M orbiting ships, each kicked by tides every few minutes, then cost ≤ 0.3 core at 1× real time. Rendering uses non-canonical floats and does not count against this.

## Division of the work

- **`crates/geodesic`** (gpt-6-astra): the canonical evaluator. It covers the orbit classification and the elliptic-function forms of r, φ and T along timelike and null Schwarzschild geodesics in river coordinates, the inversion T → orbital phase, certified integer interval arithmetic and the written floor rule.
- **`xtask` step 2 gate** (gpt-6-sol): the independent reference evaluator, the adversarial case set and the G2.1–G2.5 harness, reusing the oracle's functions.
- **The integrator:** this contract, the reviews, the merge and the journal.

## Later steps (direction, not frozen)

- **Step 3: many bodies.**
  - The parent is the dominant source, chosen by a dimensionless ratio with hysteresis.
  - A body follows its parent's river; a moving parent carries its river along.
  - Other sources act as tides: multipole moments stored as polynomials in time and read at the retarded time. The tides accumulate in carries, and an integer kick is applied each time one velocity quantum builds up.
- **Step 4: the law in the engine.** Per chronon, x(T) comes from the formula. Contacts are resolved in the flow frame, with a canonical integer β at the contact (exact isqrt of 2MQ²/r). The speed limit becomes |k − βQ| ≤ Q, and finality uses c + |β|.
