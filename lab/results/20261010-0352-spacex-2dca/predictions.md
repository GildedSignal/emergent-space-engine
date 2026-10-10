# Predictions (written before the decisive runs)

Question: H_live = distinctions (real encounters) per body per orbit at fixed belt density, the cost per distinction (re-certification), and the ceilings those imply for 10⁹ bodies on the 8 GB M1 (compute → RTF ceiling, memory → write traffic and steady-state scar store).

Cases below are NOT tuned on (I have not run `steady` or `kick` in this checkout; the only priors are r8 v2's taste-log numbers for a different, denser belt: 427 encounters, 20 orbits, 1.1 element-sort events/body/orbit).

- P1 (rate): `steady 1000 50` at rho=1e-4, sigma_e=1e-2 gives hits_per_body_orbit in [0.005, 0.08] (point guess 0.02).
- P2 (linearity in density, same annulus): `steady 10000 50` gives hits_per_body_orbit ≈ 10× the n=1000 value (within a factor 1.5; this is the fixed-density scale-invariance control — at fixed physical density the per-body rate must not grow with N).
- P3 (cost): `kick` at n=10⁴, rho=1e-4, horizon 1000 orbits: us_per_kick in [50, 5000] (point guess 800 µs; pairs_per_kick in [50, 800]).
- P4 (compute ceiling): with per-distinction cost from P3 and rate from P1, the RTF at which 10⁹ belt bodies (main-belt-like density, a ≈ 2.5 AU) saturate 4 performance cores is BELOW 10⁶ — the galaxy-doll RTF cannot keep every belt body live; the affordable live fraction at RTF 10⁶ is < 1%.
- P5 (which limit binds): memory write traffic for scars (≈ 16–48 B per distinction) at the compute ceiling is < 10% of the M1's ~60 GB/s — compute binds before bandwidth.
- P6 (memory floor): the static program store (0.126 bits/body, gold components-98bc) is ≤ 0.1% of 8 bytes/body at 10⁹ — the 8 GB question is decided entirely by the dynamic term (scars in the retention window), not by the program.
