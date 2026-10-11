# Predictions — run 20261011-1332-dynamics-8269 (written before any run)

**Question.** What is the belt's rate of production of live distinguishing information
(H_live)? The board names it unmeasured; B18's floor and the b-h-live build need it, and
the Opus memo (R2, line 129) claims that under the kick law "every kicked body carries a
full scar", i.e. churn = kick rate. Dynamics-lens decomposition: per body, is the
perturbed motion (i) quasi-periodic (λ = 0: a bounded attractor; a program/generator can
hold it forever; scars ≈ 0), (ii) chaotic (λ > 0: information at the Lyapunov rate), and
does the secular invariant a random-walk only at resonances (hitting rate = scar flux)?

**Instrument.** Planar restricted Sun–Jupiter–Saturn (prescribed Kepler orbits, no
mutual J–S interaction — approximation, noted in the dossier), test bodies advanced by a
symplectic Kepler map (exact Kepler drift under the Sun + planetary kicks with the
indirect term, kick-drift-kick). Per-body Lyapunov exponent by shadow renormalization
(d0 = 1e-9, renormalized each Jupiter orbit). "Filtered" elements = running mean over a
41-Jupiter-orbit window (suppresses synodic/short-period terms; a proper-element proxy).
Hitting = |filtered a(t) − filtered a(0)| first crossing of ±q. Scene matches
q-secular's: 1024 bodies, a₀ uniform 2.0–3.3 AU, e₀ Rayleigh σ = 0.07 truncated at
0.25, angles uniform, planar.

**Controls (both must behave, else VOID):**
- C1 quiet ring (a₀ = 3.10 ± 0.004, e₀ Rayleigh 0.01, N = 256): the instrument's floor.
  Predict: median late-window λ < 3×10⁻³ per Jupiter orbit; filtered-a hit fraction at
  q = 1e-4 AU under 5% by the end; osculating (unfiltered) a still oscillates with
  synodic amplitude A_syn ≥ 3×10⁻⁴ AU (bounded, phase-locked — predictable, so not
  information).
- C2 planted chaos (a₀ = 2.502 ± 0.003, the 3:1 resonance, e₀ Rayleigh 0.05, N = 256):
  the instrument must see known chaos. Predict: median late λ at least 5× C1's, and at
  least 30% of bodies hit q = 1e-3 AU in filtered a within 6000 Jupiter orbits.

**Decisive run R1 (the belt), T = 6000 Jupiter orbits (≈ 7.1×10⁴ yr), dt = P_J/50:**
1. Chaotic fraction (late λ > 10× C1 floor): between 15% and 60%; concentrated at the
   3:1 (2.50), 5:2 (2.82), 7:3 (2.96), 2:1 (3.28) bands, the inner edge (2.0–2.2,
   secular resonance g ≈ g_Saturn + overlap), and not zero anywhere-flat between them.
2. Filtered-a hit fraction at q = 1e-3 AU by the end: between 10% and 50%. Late-window
   hit flux (new hits per body per 1000 orbits, t ∈ [3000, 6000]): below 3×10⁻¹ per
   body per 1000 orbits, i.e. the scar flux is at least ~10× below the averaged kick
   rate (0.3 per orbit) and orders of magnitude below the 64-kick law's rate.
3. Quasi-periodic majority (λ at the floor): filtered a bounded — hit fraction at
   q = 3×10⁻⁴ AU under 20% even by the end; their filtered e deviates boundedly (the
   secular amplitude builds in the first ~1000 orbits, then stops: no late flux at
   q_e = 1e-3).
4. Scaling: hit fraction and late flux fall steeply with q (roughly as a power q^−α,
   α < 2, from diffusion + a resonance-width geometric term), NOT flat: quanta above
   the secular amplitude buy real memory.
5. Consequence claimed if 1–4 hold: scars should be written on filtered-quantum
   crossing, not on kicks; the belt's live memory grows only through the chaotic
   minority's hitting flux, and the program survives ~10²–10⁴ orbits between
   re-programs instead of dying at the first kick (the memo's key coupling, refuted for
   memory though confirmed for the naive store).

**Held-out cases I did not tune on (checker's ground):** e₀ Rayleigh 0.15 (excited
belt); q = 1e-2 and 1e-4 AU endpoints; Jupiter alone (no Saturn); dt halved (P_J/100)
— λ and hit fractions must not move by more than ~2×; T extended to 12000 orbits — the
quiet majority's hit fraction must not double (transient, not slow diffusion, is the
early signal); the λ floor claim itself (C1 at T = 12000 must stay flat).

**Kill criteria for my own claim:** if C1 shows filtered-a diffusion (hit fraction at
1e-4 above 20%), the filter is broken or the quiet belt genuinely drifts — either way
no adoption claim; if C2 shows no separable λ, the Lyapunov instrument is too noisy at
this T and only the hitting-rate half of the claim can stand; if the chaotic fraction
comes out above 80% (chaos everywhere), the "program survives" claim dies and the belt
is memory-hard at any quantum.
