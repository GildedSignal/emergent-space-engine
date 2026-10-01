# Lens: encounters without a setup per element change (a Verlet skin on the Binet cone), a directed question

`crates/encounters` (research) found that orbits are points (U, V, W) = (1/p, e·cos ϖ/p, e·sin ϖ/p), and two orbits cross only inside the cone ΔU² ≤ ΔV² + ΔW². The next close pass comes from a continued-fraction recursion. It missed nothing, with events at 1.3× the encounters, but each candidate pair costs 2.5–24 µs of setup every time a kick changes an element. Rung r8 v3 verifies the cone.

**Question:** pad the cone with a skin of width s, and set a pair up again only when the kicks accumulated since its setup exceed s (molecular dynamics' Verlet list). Which s minimises setups per kick plus false candidates on the plane's scene, with ships kicked at the plane's rate? Does the certificate stay exact (no missed encounter) for every s?
- Read crates/encounters and build on copies in your folder; never edit the crate.
- Report setups per kick, candidates per body and misses (which must be 0) as functions of s, on 10³ to 10⁵ bodies. Held out: a dense ring and a fleet.

Gold: setups per kick cut 10× or more with zero misses, and a rule for s from local quantities.
