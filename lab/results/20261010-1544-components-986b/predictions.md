# Predictions (written before the probe runs; Fermi + scaling, no tuning)

Component: storage (populations + scars). Measure: H_live rate — bits of
distinguishing information per body per orbit, relative to the birth program,
at quantization q. Probe: N bodies on exact Kepler drift (the law's tubes),
impulse kicks at every conjunction (validated against exact two-body
integration), equal-mass bodies at fixed total belt mass mu_b.

Held-out expectations (not tuned):

1. **Growth shape is diffusive, sub-logarithmic in cost.** The offset spread
   sigma(t) ~ sqrt(Gamma * delta^2 * t), so bits(t) = log2(sigma(t)/q) grows
   like 0.5 log2 t + const. No linear-in-t term. If bits(t) grows linearly
   (>1 bit per doubling of t anywhere beyond the first step), the 10^9 fit is
   in doubt and I must find the linear source.
2. **Mass scaling: +2 decades of variance per +1 decade of mass.**
   bits(mu_b) - bits(mu_b/10) ~ 6.6 bits at fixed t and N (delta^2 per kick,
   kick count unchanged at fixed density).
3. **N-scaling at fixed mu_b: relaxation slows as 1/N.** Doubling N at fixed
   total mass and band halves the variance rate; bits(N=2048) - bits(N=1024)
   ~ -1 bit at the same checkpoint (sqrt of variance ratio 1/2).
4. **Coulomb log:** the rate at screen rho differs from the rate at rho/4 by
   ~log2(4) ~ 2 bits (ln divergence), not by orders of magnitude.
5. **Control (mu_b = 0):** measured bits stay at the float noise floor,
   < 0.05 bits/body at q = 1e-6, flat in t. If it rises, the instrument leaks
   and every other number is VOID.
6. **Kernel:** the impulse vs exact two-body integration agrees within a few
   percent in |dv| for weak encounters (deflection < 0.1 rad); for strong
   ones (deflection > 0.3 rad) I switch to exact integration by default.
7. **Extrapolation:** a physical belt (mu_b ~ 1e-9, N = 1e9) accumulates
   < 1e-3 bits/body over 1e4 orbits — the 8 GB budget is decided by births
   and structure, not encounters. The risk concentrates in *lanes*
   (concentrations): if the loose-fleet lane (100x the belt's line density)
   shows ~x bits/orbit/body, a formation of 1e8 ships exhausts its ~34-bit
   budget (4 GiB / 1e9) in ~34/x orbits, which I expect to be < 1e3 orbits
   for the heaviest lane I can run — the number the allocator needs.
8. **Mean drift is shared.** The population-mean offset (secular drift)
   carries most of the raw growth; the *centered* entropy (what scars must
   store, after the program absorbs the shared drift) is well under half the
   raw value at every checkpoint.
