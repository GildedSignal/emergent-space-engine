# Predictions (written before the decisive run)

Question: what creates live distinguishing information (H_live) in the game's belt
at 10⁹ bodies, and does it stay under the 8 GB budget?

The decisive run is `h_live_fermi.py`: a Monte Carlo that (a) reproduces r8 v2's
belt sampler and counts true encounters, (b) checks the impulse formula against
exact hyperbolic two-body scattering, (c) counts sphere-of-influence (SOI)
transits of a planet embedded in the belt, (d) scales everything to 10⁹ at fixed
annulus and at fixed density, and (e) computes quantum-crossing times for ship,
asteroid and dwarf-planet masses.

Cases I have NOT tuned on:

- **P1 (r8 anchor, held out).** My analytic rate formula predicts the median true
  encounter rate over the 16 r8-v2-like belts is ~7×10⁻³ per body per orbit
  (Σ·2ρ·v_rel·T with Σ = N/3.93, v_rel ≈ √2·σ_e·v_K, median ρ = 5.5×10⁻⁵,
  median σ_e = 5.5×10⁻³). The Monte Carlo will land within a factor 3 of that,
  and belt-0-style counts (427 encounters, N=10⁴, 20 orbits) sit inside the
  belt-to-belt spread (0.3–3 × 10⁻³ per body per orbit at the belt extremes).
- **P2 (impulse validity, held out).** The impulse approximation δv = 2Gm/(b·v)
  matches the exact hyperbolic deflection within 30% while deflection < 0.5 rad,
  and overestimates by ≥ 2× once deflection passes ~2 rad (small-angle breakdown).
- **P3 (SOI transits, held out).** A planet with μ_p = 10⁻³ at a_p = 1.25 inside
  the belt [1, 1.5] (R_SOI = a_p(μ_p/3)^{1/3} ≈ 0.069): the fraction of bodies
  whose radial range overlaps the SOI band is ~2R_SOI/W ≈ 25–30%, and the
  belt-averaged transit rate is 0.01–0.05 per body per orbit. Every transit is a
  full rebind (deflection at the SOI edge is order 1 for any quantum coarser
  than 10⁻⁵ v_K).
- **P4 (mutual-encounter H_live ≡ 0 at ship masses, held out).** With ship mass
  10⁶ kg (μ ≈ 5×10⁻²⁵) and a 1 M☉ star, the accumulated velocity diffusion needs
  more than 10⁵ session-lengths to cross a q_v = 10⁻⁵ v_K quantum, at ANY belt
  density up to 10⁹ in the fixed annulus. The critical mass where every ρ-scale
  encounter crosses the quantum is μ_crit ≈ q_v·ρ·σ_e/2 ≈ 5×10⁻¹³
  (≈ 10¹⁸ kg, dwarf-planet scale), not ship scale.
- **P5 (contacts, held out).** At 10⁹ bodies in the fixed annulus with physical
  radii 10 m, the contact rate is below 10² per game-second universe-wide.

If P1 fails by > 10×, my encounter-rate model is wrong and the diffusion layer
built on it is suspect: I must find which term (geometry, v_rel, or the
conjunction model) broke before trusting anything downstream.
