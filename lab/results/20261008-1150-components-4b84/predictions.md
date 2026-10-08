# Predictions (written before the decisive run; 2026-10-08 11:58 UTC)

Component: shipmem's scar layer (live storage of a stirred population). Question: what is the
information floor of the ledger a belt's own stirring creates, per body per game-second, and
which design (naive full-tube-per-touch / integer scar ledger / ledger + refold) tracks it?

Belt toy: a=2.5 AU, half-width 0.25 AU, sigma_e=0.07, sigma_i=0.035, N=10^9 bodies,
total mass M in {3e21, 3e22} kg, rho=2.5 g/cc. Encounters: impulse approximation,
miss distance b uniform in b^2 between 2R and the mutual Hill radius, v_rel from sampled
Kepler pairs. Ledger axes: dE/E, dL/L (sqrt-t diffusion), dvarpi (deflection accumulation),
dt_p/P (phase drift ~ linear in t: dt_p/P = 1.5 (dE/E) t).

Fermi estimates (closed form, c^2 = 1 projection):

1. sigma_{dE/E} per sqrt(orbit) ~ 4e-13 at M=3e21 kg (variance per orbit ~ 1.9e-25), scaling
   linearly in M at fixed N, and as 1/sqrt(N) at fixed M.
2. Geometry constant kappa = measured / closed-form in [0.3, 1.2].
3. Onset of shape-axis scars (sigma > q): fine grid (q = 0.18 * 2^-32 ~ 4.2e-11 of |E|):
   ~10^4 orbits at M=3e21, ~10^2 orbits at M=3e22. Key grid (0.18 * 2^-16 ~ 2.7e-6):
   > 10^13 orbits at both masses — no scar ever in a game lifetime.
4. Ledger bits once above quantum: ~ log2(sigma/q) + 2 bits per shape axis (Gaussian);
   program entropy stays at the birth value (birth spread 0.2 dwarfs the diffusion).
5. The phase axis (t_p) dominates after onset: bits ~ log2(1.5 sigma_E t / q_t) growing
   ~ 1.5 log2 t, NOT bounded without refold; with refold cadence K the total stays
   < log2(1.5 sigma_E K / q_t) + ~6 bits.
6. Held-out cases (not tuned): M=3e22 (10x), grid j=24, horizon sweep 10..10^5 orbits,
   N-scaling spot check at fixed mass. Expect: onsets divide by 100 vs mass, bits curves
   follow the formulas within a factor 2.
7. Bottom line predicted: background H_live of a quiescent self-stirred belt < 1e-3 bits per
   body per game-hour even at 10^6x real time on the fine grid; the 8 GB budget at 10^9 bodies
   is spent by player-driven distinctions, not secular stirring. Naive touched->16-byte-tube
   exceeds the ledger floor by > 10x at all horizons past onset, and by ~10^3x at the key grid
   if any grid coarser than fine is used for tube-vs-program decisions.

Kill criterion for the toy: if measured kappa falls outside [0.1, 10] the impulse model or the
rate model is wrong and nothing above counts; report it instead of the conclusions.
