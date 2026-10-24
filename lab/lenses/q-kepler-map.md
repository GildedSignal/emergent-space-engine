# Lens: tabulate the conjunction (a Kepler map for the belt)

Read `lab/wiki/index.md`, `lab/wiki/belt.md` and `lab/wiki/kick-cadence.md` first. The lab measured that the belt's dynamics are carried by real conjunctions with the planets, not by the secular field (zero-kick secular phasors: 14.5% of bodies pass, 6 October), and that conjunctions are not predictable in closed form. Julien, 24 October, on computing with memory: look answers up in memory instead of recomputing them.

The question: is the outcome of one conjunction tabulable? Celestial mechanics has a precedent: the Kepler map (Petrosky; Chirikov and Vecheslavov), one step per perihelion passage, Δ(energy) as a function of the perturber's phase, which reproduces long-term chaotic diffusion. Build, in the lab's two-planet belt replica (exact integration as the truth, verified as the secular runs did), a table of (ΔE, ΔL, Δφ) per conjunction as a function of the body's orbit (a few bits of e and a) and the conjunction phase, with interpolation. Then run the belt by table lookups, one per conjunction, against the exact integration, on the behaviour gates' terms (rates within 5%, e-vector within 10%, the fraction ending in a resonance, a planted one-signed bias that the test must catch). Price the table (bytes, entries) and the cost per conjunction.

The certificate: a body uses the map only outside a few Hill radii of every planet; inside, exact integration. Report the fraction of bodies and of conjunctions that stay inside the map's domain.

Gold: the verdict either way, with a verified truth, a control that fails, and the multiplier on kicks per belt body against today's ~9,000 per orbit and the 8-16 that hold the gates.
