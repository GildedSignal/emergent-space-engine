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
4. **Every change is an event, resolved by its exact law.** Motion is the compiled drift plus kicks (law.md: Wisdom–Holman, with SyMBA's smooth changeover near a secondary; no switch at the sphere of influence), and rebinding happens when the dominant body changes. Contacts follow `es-lattice-relativistic-v1`. The player's thrust grows the rapidity in proper time; in a field, E and L change by the work done.
5. **Observation is a pure function of the state:** the gather reads, never writes.
6. **Seams for better parts, with no rewiring later.** Body storage behind one interface: plain tubes now, `crates/shipmem` population programs later. Encounters behind one interface: an exact per-doll check now, the Binet cone (`crates/encounters`) later. Kick sources behind one interface: the parent's tide, secondaries and neighbours' moments now; averaged secular kicks for stable hierarchical orbits as an option.
7. **Bounded work per presented frame** (1 October, after GPT's point on tails: "make expensive work bounded, movable, predictable, or avoidable"). The frame has a hard deadline (16.67 ms at 60 Hz). The engine gets a budget per frame and spends it in causal-deadline order: an event's deadline is when its light reaches the player's past light cone or another consumer (the slack queue of representation.md §3). Nothing takes an unbounded synchronous claim on the frame, whether a cycle compile, a rebinding burst, a decompression or a gather. Keys about to be needed are compiled ahead in idle time. The budget changes *when* work is done, never *what*: outcomes are independent of schedule, so any budgeted order gives identical bits. Overflow (a burst whose deadlines all fall inside the frame) is pending Julien's call: a brief dip of the real-time factor, or a visible degradation.

## Measured on the whole, from the first flight

- **Smoothness, as a service level, not as FPS:**
  - frame time p50, p95, p99 and p99.9;
  - hitches per gameplay hour above 16.7, 33 and 50 ms;
  - the worst hitch and its frequency;
  - the real-time factor's median and its lowest 1%.

  A percentile alone can hide a 200 ms freeze once a minute, which is 0.028% of frames.
- **Throughput and footprint:** events per second, bytes per body, and the universe's digest.

All of these are measured like the player: heat included, machine state recorded. Every later change is chosen by the bottleneck these numbers show. The gates (B0–B18, E1–E8) stay as guards on the parts.

## Not in the first flight

Populations and compression, encounters at scale, the GPU dense order inside the universe, the SSD tier, AI (off the plan), the galaxy.
