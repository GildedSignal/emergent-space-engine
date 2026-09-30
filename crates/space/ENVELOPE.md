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
dyadic arithmetic throughout. Readout solves to that clock's arithmetic quantum,
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
each, held in four i128s). It is 64 additional bytes per live event, plus its units
and event reference; not an uncharged per-body ledger. The proof applies at the
binding event. Transport through later physical motion is the events owner's
remaining obligation: discarding the remainder at a handoff voids the proof.

Bound here means an exterior periodic radial orbit (p>6+2e). Its periapsis
approaches 4M, not 3M; 3M is the photon circular limit. Plunges, radial L=0 paths,
unstable circular generators and horizon arrival times are not supplied by this
periodic compiler. Passage endpoints must be resolvable by the finite phase word;
an unresolvable radius ratio is refused, never replaced by infinity.

This derivation is an implementation proposal, not a new freeze or qualification.
