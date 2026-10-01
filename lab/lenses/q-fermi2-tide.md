# Lens: the reference for the Fermi frame's phase 2 (the Schwarzschild tide along eccentric orbits), a directed question

Battles live in Fermi normal coordinates along an exact compiled tube (crates/engine/src/tube.rs, `Frame::on_orbit`; docs/law.md, "Dense order"). Phase 1 uses the Newtonian tidal tensor. Phase 2 needs Schwarzschild's, along eccentric equatorial geodesics, bound and unbound. Candidate gate E9 (`git show wt/judge2:xtask/src/engine_judge/schwarzschild.rs`) judges it with pairs of nearby geodesics.

**Question:** build the reference the phase-2 builder will use: the tidal tensor in the parallel-transported tetrad along an equatorial Schwarzschild geodesic, in closed form in (E, L, r), plus the tetrad's rotation angle (Marck 1983; Ishii, Shibata and Mino 2005; Xin and Mummery; TidalZAMO).
- Derive it, then verify it two independent ways: geodesic deviation integrated along the orbit, and finite differences of nearby geodesics. Cover circular orbits (the analytic check), eccentric ones (e from 0.1 to 0.9), near-ISCO, whirl and unbound orbits.
- Deliver a Python script with the closed form, and a JSON of test vectors (inputs, tensor components, rotation angle) that agree to 1e-12 relative in double, against mpmath.
- Say which expressions are rational in (E², L², 1/r, M), and so exact in integers, and which need a square root.

Gold: the closed form verified both ways on every orbit family, with its integer-friendly form named.
