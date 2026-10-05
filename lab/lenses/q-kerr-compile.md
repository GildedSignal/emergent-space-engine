# Lens: compiling orbits around a rotating hole (a directed question; the reference for the compiler's builder)

Julien, 5 October: "especially rotating black holes". docs/law.md, "Rotating holes": a tube is still compiled from (E, L), now with the doll's spin χ. crates/space compiles Schwarzschild cycles once from (E, L) by Gauss–Legendre quadrature in Darwin's phase (r = p/(1 + e·cos ψ)); the shape is (k = 1/(1+e), q = M/R); the weak field is a series in q memoized per k; scale is a binary exponent. Read crates/space/src/orbit.rs and scaled.rs, and docs/law.md.

**Question:** what is the same representation for equatorial Kerr, so that the compiler's builder (Astra, from 9 October) starts from a checked reference? In your folder (never edit the crates):
- Derive the equatorial Kerr radial and azimuthal equations in Darwin's phase (Glampedakis and Kennefick 2002 do eccentric equatorial Kerr orbits this way), for bound, plunging and unbound orbits and for photons, prograde and retrograde, including negative-energy orbits in the ergosphere.
- Write a float reference compiler: (E, L, χ) → the cycle's Δφ, Δt and Δτ per radial period, by Gauss–Legendre in ψ. Verify it against direct geodesic integration (mpmath) at χ = 0, 0.5, 0.9, 0.998, both senses, e from 0 to 0.9, near the ISCO and the separatrix.
- Say how χ enters the weak-field series in q (Lense–Thirring appears at q^(3/2)), whether one memo per (k, χ) is enough, and which integrands lose smoothness near the separatrix as χ → 1 (and how many nodes they need).
- Deliver: the derivation, the reference script, and a JSON of test vectors (inputs and the three increments) to 1e-12 relative.

Gold: a reference that regenerates from the shipped script, agrees with direct integration on every family, and states how the existing representation extends without a special case.
