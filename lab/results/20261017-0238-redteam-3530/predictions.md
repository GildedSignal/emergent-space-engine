# Predictions (written before the decisive run, after controls only)

Instrument state: C1–C3 pass (quadrature vs RK4-Binet 3.15e-5; e(x) series 2PN 6.3e-8 /
3PN 1.9e-10; nu=0 recovers exact Schwarzschild ISCO r=6, j=sqrt(12), E=sqrt(8/9)-1,
Omega=6^{-3/2}). No nu>0 number has been read yet.

Cases below are the held-out ones (nu = 1/4 equal mass, the flank's worst case inside
B11's own nu <= 0.25). "Doc law" = exact Schwarzschild effective problem + nu energy map
(representation.md L37). Truth = EOB A(u) at 2PN (eccentric, with D_2PN) / 3PN (circular).

1. **ISCO shifts inward and deepens with nu; the doc law barely moves.**
   - Doc law at nu=1/4: r_ISCO = 6 exactly (nu-free construction), E_b/mu = -0.0576 ± 0.0005
     (the energy map's O(nu x) rescale of the Schwarzschild -0.05719).
   - 3PN truth at nu=1/4: r_ISCO = 5.7 ± 0.15, E_b/mu = -0.064 ± 0.005.
   - Relative binding error at ISCO: 8–15%.

2. **Periastron advance: the doc law is nu-free by construction; truth is not.**
   Relative error of the doc law's advance vs 2PN truth at nu=1/4, scaling ~ 1/p^2:
   - p=100, e=0.2: below 0.05%.
   - p=40, e=0.5: 0.1–0.3%.
   - p=20, e=0: 0.2–0.8%; p=20, e=0.6: 2x-4x the circular error (pericentre focus).
   - p=12, e=0.3: 0.7–2%.
   - p=8, e=0: 2–5%.
   All BELOW B11's own tolerance (1% + 16/p) at p=20 (1.8%), and above 1% only inside
   p <~ 12 — the merger scene, where B11 does not look.

3. **The energy map is pathological at plunge.** E_real(E_eff=0) = sqrt(1-2nu) = 0.7071
   at nu=1/4 (binding 29.3% of Mc^2); the 3PN plunge region binds an order less
   (~0.06–0.09 per mu). The map overbinds the plunge by ~3x.

4. **Consistency with r3 v3:** the p >= 20 errors are small enough that r3's 1% bars at
   its own separations (p 20–1000, e <= 0.6) could pass against a 1PN oracle while the
   merger rows fail against a 2PN one — the licence, not the letter, is what is missing.

5. **Q-toggle robustness:** including Q_2PN changes the periastron error by < 30% of the
   signal at p >= 12 (both are O(nu u^2) effects); at p=8 up to ~50%. The conclusion
   (flank unguarded below p~12) survives either way.

Kill criterion for my own claim: if the p=20 circular error exceeds 1.8% (B11's tolerance
there) then the flank reaches inside the gate's own domain and my "unguarded below p~12"
framing is wrong in the useful direction (the gate itself is broken, a stronger finding);
if the ISCO binding error at nu=1/4 is below 3%, the flank is cosmetic and I report the
premise as surviving with a priced licence cost.
