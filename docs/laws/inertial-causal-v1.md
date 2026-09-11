# Inertial causal law v1

Law identifier: `es-inertial-causal-v1`. This is the exact scalar reference law for
inertial motion and causal events. It establishes neither an integrated gravitational
engine nor a billion-ship performance qualification. Gravity, acceleration, curved
null paths, resource dynamics, and political behavior are outside this law.

## Canonical state and units

- Use two spatial coordinates with `c = 1`; one coordinate-length unit is the distance
  light travels in one coordinate-time tick. A scenario defines the mapping to years.
- A canonical event tick is a signed `i128`. Positions and velocities are normalized
  arbitrary-precision rational numbers. There is no position lattice or FP32 shortcut.
- An inertial segment is `(epoch, origin, velocity)` with `velocity·velocity < 1`.
  Its worldline is `origin + velocity * (t - epoch)`, including continuous rational
  interpolation between event ticks. Evaluation and rebasing are algebraically exact.
- Tick differences and squared distances are computed after conversion to arbitrary
  precision. The difference between `i128::MIN` and `i128::MAX` never uses `i128`
  subtraction. Interval midpoints also avoid signed overflow.
- Public structs support canonical serialization. Consumers must validate intervals
  and velocities after untrusted deserialization. Constructors validate them; event
  queries reject invalid intervals, radii, and nonsubluminal velocities.

## Proper time

For a constant velocity, define the canonical rate

`rate(v) = floor(2^32 * sqrt(1 - v·v)) / 2^32`.

Compute the floor exactly using arbitrary-precision integer square root; no floating
estimate determines this quantity. The rate is a property of the segment, and elapsed
proper time is exactly `(to - from) * rate(v)`. It is not rounded again at observations,
checkpoint boundaries, or rebasing. Consequently subdivision gives exactly the same
answer as a single long query. The pure scalar rate may be recomputed by a query;
doing so does not create additional numerical quantization.

The canonical rate lies below the special-relativistic value by less than `2^-32`.
Its elapsed-time difference from that continuum reference can therefore grow by up
to duration times `2^-32`; this is a law approximation, not arithmetic drift. An
extremely near-lightlike valid velocity can have canonical rate zero. This limitation
is explicit and tested; a later law or velocity-domain gate is required before claiming
physically accurate clocks arbitrarily close to light speed or across cosmic durations.

## Contact ticks and domain splitting

`TickInterval {start,end}` names inclusive **event ticks**, and is valid when
`start <= end`. For swept contact, tick `k` owns the continuous-time bin `(k-1,k]`.
Two worldlines contact when their squared separation is at most the supplied squared
combined radius. `first_contact` returns the first owned tick with any such contact.

This convention catches a collision or tangent that begins and ends between integer
samples. A tangent exactly at integer time `k` belongs to tick `k`, never tick `k+1`.
The left edge of the first bin remains open even at `i128::MIN`, with its geometric
time represented rationally. Splitting `[a,b]` into `[a,m]` and `[m+1,b]` neither drops
nor shifts the earliest contact. Persistent overlap can occupy successive bins; the
caller handles the event and updates worldlines or collision state before searching
future bins. Initialization must handle overlaps at the scenario's starting state;
subsequent searches normally start at the following tick.

Detection minimizes the exact rational squared-distance quadratic over a half-open
prefix of the queried bins, then binary-searches the first successful prefix. It does
not sample endpoints alone, compute approximate roots, or require finite-precision
root equality. A finite domain takes at most 128 binary-search divisions, independent
of the represented elapsed duration. The scalar arithmetic cost still depends on the
size of the rational values; this is not a constant-cost population claim.

`worldtube` returns the exact axis-aligned spatial envelope over the closed continuous
interval `[start,end]`; broad-phase users querying contact bins must include the prior
bin edge in their own swept envelope. Its closed-envelope semantics do not silently
replace the contact query's half-open bin semantics.

## Light and event causality

Emission `(te,xe)` can affect reception `(tr,xr)` exactly when `tr >= te` and
`|xr-xe|² <= (tr-te)²`. All comparisons are rational and exact. The arrival query
returns the first integer receiver tick satisfying this predicate, within its finite
inclusive domain. A stationary colocated receiver can receive at emission time.
Subluminal inertial receivers remain within an emission's future light cone once
they enter it, which makes the binary search sound.

The query establishes delivery eligibility. The scheduler separately owns simultaneous
event ordering, duplicate delivery prevention, semantic event identity, and updates
after a collision or received control message. No information may be delivered before
the returned tick merely because a floating candidate predicted an earlier arrival.

## Required evidence

Module tests cover affine/rebase equivalence over the full tick range, exact proper-time
subdivision, independent dyadic square-root bounds, point crossings and 2D tangencies
between samples, tangent boundary ownership, domain splitting, an independently solved
linear-contact grid, exhaustive integer signal-arrival comparisons, invalid velocity
and radius handling, canonical serialization, and overflow-hostile causal geometry.
These verify this inertial law only. They are not evidence of a validated gravity law,
general compression certificate, population-scale memory bound, or astronomical
long-term physical behavior.
