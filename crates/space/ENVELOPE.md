# A geodesic's native representation

The operations are: compile at a change of invariants; sample many times without
evolution; translate/boost and bind at an event; add the same increments per radial
cycle. Absolute radius, angular momentum and nearly-unit total energy are poor
coordinates for these operations. No operation requires their absolute magnitude
to fit in a fixed-point word.

Use periapsis radius R and k=1/(1+e), with x=R/r=k+(1-k)cos(psi).
The scale is a normalized unsigned significand and a signed binary exponent.
Put q=M/R, A=6k+2(1-k)cos(psi), D=k-q(3k²+(1-k)²). Then

    dphi/dpsi = g = 1/sqrt(1-q A)
    dt/dpsi / R^(3/2) = sqrt(k(1-2q)(1+2q(1-2k))) g / ((1-2q x)x²)
    dtau/dpsi / R^(3/2) = sqrt(D) g / x².

Thus scale enters time by multiplying its binary exponent by 3/2 (odd exponents
leave sqrt(2) in the significand). The angles consist of a radial phase and an
azimuthal excess; never subtract two rounded full turns to recover the excess:

    (g-1)/q = A / (sqrt(1-q A) (1+sqrt(1-q A))).

This rationalization preserves precession even when q is much smaller than one
fixed-point quantum. A cycle adds its phase, time and proper-time increments;
readout depends only on the quotient/remainder, never on previous readouts.
For k<=1/2 there is a passage instead: it ends at x=0 at infinity; finite-radius
endpoints have finite times. Infinity is not an enormous finite clock value.

At q=0 the same integrands give the Newtonian shape. Their first derivatives in q
give the weak-field family: g'=A/2, t'=3 sqrt(k)/x,
tau'=sqrt(k)/x² [A/2-(3k²+(1-k)²)/(2k)]. This is a series in compactness,
not a different orbit category. Its coefficients share one memo entry per k;
R and the small q coefficient remain attached to the individual binding.

Widths come from information, not from a largest test radius. A normalized signed
word retains 63 significant bits through root finding and quadrature;
an i16 exponent makes range independent of precision. Products of two
significands fit u128. Checked exponent arithmetic refuses exhaustion explicitly;
no oversized absolute period is ever constructed. Public Cartesian event states
have explicit common length/velocity exponents. The former fixed Q20/Q30 API is
a compatibility boundary and may refuse values its units cannot express.

For hyperbolic k below 2^-28, the key stores k as a 48-bit normalized mantissa
and its own i16 exponent. Exponent zero retains the old Q48 bits above that
boundary. Angular factors use the bounded Q62 projection of k; clock numerators,
the speed scale and the clock gap use its full scaled value. A tiny k may vanish
from an O(1) angular factor, but never from sqrt(k) or q/k. Both inverse paths
(state and invariants) retain this scale; memo keys and universe digests include it.

Rebinding is necessarily a quotient **and a remainder**: a rounded orbit fit is
not injective. For integer event state X and decoder F, store C=X-F(Q(X)). Then
F(Q(X))+C=X exactly. Translation and kicks operate on this reconstructed integer
state. Repetition telescopes; it cannot acquire representation drift. Discarding
C invalidates this proof. This proves the coordinate conversion, not that patched
two-body dynamics conserve the three-body Jacobi integral; B12 must judge that
separate claim after the events layer integrates the tide.

The 16-byte tube holds a catalogue index (32), orientation in turns (32), and
signed periapsis time in a population clock (64). Scale belongs to the indexed
binding; shape memo entries are shared across bindings. Taking exponent bits
from the index would save no bytes while limiting either catalogue or clock range.
Rounding remainders are explicit additional event storage, never hidden in 16 bytes.

## Implementation and consumer boundary

`orbit::Orbit` and `Passage` implement this representation; the old `Cycle`, `Key`
and `LegacyTube` preserve the v2 fixed-unit ABI for the events owner to migrate.
`Tube` is the new contract. A `Catalogue` holds scale and chirality; `TubeEvent`
also retains rounding of the population's periapsis clock. The old events clock,
binary and photon adapters still use v2; they are not evidence for a v3 extension.

The weak expansion is used for q <= 2^-18. Strong panels normalize clock ratios by
the minimum x and retain 48 weighted bits; a conditioned panel uses normalized
dyadic arithmetic throughout. If the minimum angular denominator is at least 1/4,
its root uses the native u64 square root (Q31, relative error <2^-30) and two-point
Gauss panels; more conditioned panels retain the wide root and four-point rule.
For a two-point panel of width h, the continuum remainder is h^5 B4/180, where
B4 bounds |f''''|/4! on that panel. This is not a claimed global error bound.
Readout solves to that clock's arithmetic quantum,
with a bounded bisection fallback. Every branch is integer and defined by input,
so errors repeat with the same shape; no sampled state advances another sample.
`at_phase` takes the cycle counter separately, preserving exact shape repetition
even when a single absolute time significand cannot resolve its fractional phase.

Memo coarsening uses x_apo=2k-1 with its own exponent: this retains relative
information near e=1. On the 7..15 bit rectangular search, 11 shape + 12 scale
significand bits is the coarsest sum passing the original bound gates. The wider
weak sweep uses 12+12. The implemented `MemoCode` has 44 live bits: 11+11 stored
fraction bits (leading bits implicit), six shape-exponent bits, 16 radius-exponent
bits. Weak shapes use only the 17 shape bits plus a tag, and share Taylor tables.
This is a measured width in this quantizer family, not a global optimality proof.

Rebinding's residual is four signed differences of i64 readouts (at most 65 bits
each, held in four i128s). It is 64 additional bytes per retained remainder, plus
its units and event reference; this can become per-body storage and must be charged.
The proof applies at the
binding event. Transport through later physical motion is the events owner's
remaining obligation: discarding the remainder at a handoff voids the proof.

Bound radial generators satisfy p>6+2e; their periapsis approaches 4M.
Incoming plunges and radial L=0 paths use `plunge::Plunge`, derived in
[PLUNGE.md](PLUNGE.md), with an explicit surface or horizon endpoint.

The v4 boundary supplies exact circular generators down to r>3M, including unstable
circles: their constant-radius angular clock needs no radial integration. The inverse
uses exact algebraic energy, discriminant and exterior-branch predicates in
Q(sqrt(X.X)) for conditioned roots. Compilation alone uses 256 fractional scratch
bits, takes the root gap's square root before narrowing, and refuses unresolved gaps.
Symbolic E=1 has k=1/2. Its half-quantum neighbourhood rounds to that even
parabolic word; other k values are floored to keep the event inside its apoapsis.
An adapter perturbation below that quantum does not invent asymptotic speed.

For passages, psi remains the inner phase. At x=2^-10 it continues in x=R/r with
an independent binary exponent. Here dpsi/dx=-1/sqrt((1-x)(x-(2k-1))); panels
that shrink x by 15/16 preserve relative clock/radius information as
x tends to zero. Radius and velocity use that x directly, not the rounded angle.
Infinity still has no finite arrival clock. Q48 k is retained: inverse fits whose
discarded shape exceeds 2^-20 of k return Range, including the high-e bank cases.
This is an explicit precision refusal, not a claim to extend that shape envelope.

## Exact migration boundary for the events owner

- `events::records`: replace the old E/L `CyclePool` and population Tube with
  `tube::Catalogue` and the root `Tube`. Doll/type belong to the owning population.
  `OrbitKey::bound(Scalar p,e_Q48)` accepts orbital input; `Rebinding::from_state`
  accepts Cartesian integer position/coordinate velocity with explicit exponents.
- `events::clock`: replace Q20 `Words` periods with `Scalar` and population clock
  exponents. `Scalar::fixed_ceil` rounds deadlines outward; `fixed_floor` rounds
  the other endpoint. Never convert a planetary period back through u64 Q20.
  The child's centre must use the new catalogue's orbit and proper-time readout.
- `events::edge`: certify relative trajectories in the new units. Native crossings
  are shape-table indices; they are not the old absolute-Q62 radial band numbers.
- `events::handoff`: reconstruct `TubeEvent` before translation/boost; fit the new
  state, then `TubeEvent::bind` accounts for orientation and periapsis-clock rounding.
  **The remainder is exact at its named event only.** Its transport through future
  motion is not implemented. It must enter the authoritative dynamics; a constant
  Cartesian offset is not a proved transport law. The current boost is still the
  low-speed approximation. B12 remains the independent test of the whole operation.
- `events::kicks`: change the reconstructed state, preserving the exact momentum
  ledger; re-fit atomically. The old Q48-E/Q32-L tangent is not a derivative of the
  new shape key. Derivative prediction never substitutes for authoritative rebinding.
- B13/B14: `Passage` supplies finite trajectories and asymptotic bend, but the
  integrated parent tide, Hill/resonant generator and their selector remain missing.
- B11 and photons still use the preserved v2 compatibility path. Their present
  passing gates do not certify a large-scale binary/photon extension.

Readout still uses normalized i128 products. The draft law asks for wide integers
only during compilation; narrowing this path remains open. A 16-byte handle does
not imply 16-byte total storage per body when catalogue bindings are unique.

This derivation is an implementation proposal, not a new freeze or qualification.

## Native light and binaries (v5; supersedes the v2 paths above)

Null passages use the same `Passage`, `OrbitKey`, shape and exponent-backed tail.
At periapsis R, q=M/R, the null radial cubic factors as
(1-x)[(1-2q)(1+x)-2qx²], x=R/r. Its second root gives
k=4q(1-2q)/(sqrt((1-2q)(1+6q))+1-2q)². Thus the same angular
integrand applies; the null clock numerator is sqrt(1-2q), its time scale
is R, its proper-time numerator is zero, and its speed factor is
1/sqrt(1-2q). Capture is decided on exact dyadic b² <= 27M², before
rounding roots. `OrbitKey::photon` returns None for capture.
`light::Capture` compiles the exterior captured arc in r/b, with a binary
exponent and zero proper time. Its coordinate clock has no finite value at
the horizon: requested endpoints must stay outside 2M. No horizon chart is
claimed. Both readouts are pure functions, including at retarded times.
For q <= 2^-18, the rationalized angular answer is
4q + (15π/4-4)q²; clocks retain the native null integrand, not massive clocks.

`events::Binary` retains ε and L with exponents, fits the native key from
E_eff-1 = ε + νε²/2, and reads its period with 1+νε. Weak invariant fits
use x=L²/r so neither small turning root is lost to fixed scratch precision.
`light::moving_deflection` aberrates the incoming direction into the lens
frame, rotates by its native passage bend and aberrates back. The SR formula
is exact; dyadic products, square roots and trigonometric readout have their
specified integer rounding. Float conversion belongs only to the judge boundary.

Unused v2 scatter, memo and tangent adapters are deleted. `Cycle` and
`LegacyTube` remain solely for `xtask galaxy`; `Key::darwin` also supplies
shipmem's frozen population fixtures. Their owners must migrate those live
consumers before deletion. Native inverse clocks now resolve the word-root
panels to 2^-36 relative rather than stopping at 2^-28. The independent real
panel witness uses the actual two-point remainder, h⁵ sup(|f''''|/4!)/180;
it is a diagnostic, not a global numerical certificate.

Porting the velocity/derivative guard exposed the two-point partial-clock
slope error (p=20, e=0.3). V5 strong panels now use four-point Gauss with the
same native word-root arithmetic and cuts; the native guard keeps its original
1e-5 derivative tolerance. Weak moving bends are rationalized before direction
subtraction, retaining their exponent even below the Q61 angle quantum.
