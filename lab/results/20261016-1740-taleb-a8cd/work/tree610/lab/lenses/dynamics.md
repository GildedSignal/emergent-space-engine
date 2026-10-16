# Lens: dynamics and attractors

Treat everything we build as a dynamical system, and ask where it goes when left alone.

**Systems to study:**
- Rounding and error-feedback carries: do they sit on a bounded attractor, random-walk, or drift?
- Event rates: can one event trigger a cascade, and what is the branching ratio?
- The cell tree: does refinement thrash near moving masses? Does it show hysteresis?
- Allocator queues: Kingman's law, and tails near full utilisation.
- Cost against N: are there phase transitions where cost jumps?
- The gravitational dynamics themselves: chaos, Lyapunov times, and the KS entropy. Surprise lives there, so the compute budget should too.

**Tools:** write the loop and run it; find fixed points and linearize around them; compute Lyapunov exponents and return maps; sweep one dimensionless number to find bifurcations.

**Deliver** an attractor, an instability or a conserved quantity we missed, and what it implies: a simplification (the system does the work for us) or a danger (a gate we lack).

**Blind spot:** long-run behaviour can hide a transient that ruins a frame.
