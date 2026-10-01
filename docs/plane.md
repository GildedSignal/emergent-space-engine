# The plane: the first universe that flies

Status: the next step (Julien, 1 October). "make it fly asap which means simple (not simplest)"; "don't make it crappy on purpose just make it good and functional with the right foundations… temp solutions tend to stay that way"; "the minimal good implementation that works and then we build on it"; iterate by bottleneck, measured on the terrain, with our representation work as the guide. The law is [law.md](law.md); the design is [representation.md](representation.md).

## Scope (first flight)

One star system, whole:
- one star, a few planets, one moon;
- ships on orbits;
- one fleet battle in a Fermi frame around a planet, with lattice contacts;
- the player's ship, flying and thrusting through it;
- the player's view: light gathered at the player's past light cone across dolls, with colour from −p·u, gravitational redshift from the doll clocks included.

The galaxy (one more doll level) is the first scope expansion, not part of this flight.

## Foundations (right now, because everything after leans on them)

1. **One world model.** A tree of dolls. Every body is either a tube in exactly one doll or a member of exactly one frame. There is no third kind.
2. **One clock, one queue.** The root clock is canonical. Every entity holds the time of its next certified event (handoff, kick, encounter, contact epoch, decision). The queue is a min over the dolls, with deterministic ties. Results are independent of processing order, threads and observation: one digest covers the whole universe (B8 at universe level).
3. **The law's contracts as written:** the 16-byte tube; rebinding with its remainder carried and never dropped; each doll's own units (scale as an exponent); the Fermi frame on an exact tube.
4. **Every change is an event, resolved by its exact law:** kicks on (E, L), handoffs by rebinding, contacts by `es-lattice-relativistic-v1`, and the player's thrust (the rapidity grows in proper time; in a field, E and L change by the work done).
5. **Observation is a pure function of the state:** the gather reads, never writes.
6. **Seams for better parts, with no rewiring later.** Body storage behind one interface: plain tubes now, `crates/shipmem` population programs later. Encounters behind one interface: an exact per-doll check now, the Binet cone (`crates/encounters`) later. The three-body regime as a doll kind: the binary doll when it qualifies, else the dense fallback.

## Measured on the whole, from the first flight

Real-time factor (game-seconds per wall-second), events per second, the p99 frame time, bytes per body, the universe's digest. These are measured like the player: heat included, machine state recorded. Every later change is chosen by the bottleneck these numbers show. The gates (B0–B18, E1–E8) stay as guards on the parts.

## Not in the first flight

Populations and compression, encounters at scale, the GPU dense order inside the universe, the SSD tier, AI (off the plan), the galaxy.
