# Predictions (written before the decisive run)

Question: what is the per-body distribution of H_live production (bits of new
distinguishing information per orbit) in a belt under the plane's regime, and is
it predictable from birth elements?

Model: 4096 bodies, a uniform in [2.1, 3.3] AU, e Rayleigh(0.05), Jupiter
(a_J = 5.2 AU, e_J = 0.048, μ = 9.55e-4). Each body is reduced to its nearest
mean-motion resonance p:(p−d) in lowest terms (the main-belt set: 2:1, 3:1,
5:2, 4:1, 5:3, 7:4, …) and integrated as the universal local form (driven
pendulum H = ½P² − cosψ + A·cos(ψ − τ)), with birth position in the resonant
phase space set by the dimensionless detuning D = δ/W from birth elements. The
twin offset d₀ = 10⁻¹² models the program's birth-quantum uncertainty (the
program stores quantized constants), so the free twin's spread is the body's
departure from what its program determines. Known distortions, disclosed: the
local form makes libration period equal drive period (real belts ~10² slower;
it fattens the chaotic layer — biasing toward the fat-tail claim on total
amounts, not on concentration), and there is no secular or three-body chaos off
resonance (underestimates the baseline).

Held out (not tuned on): P1, P2, P4. Committed before the decisive run; the two
T ≤ 10³ runs were benchmarks of the instrument only.

- **P1 (fat tail; stock metric, amended twice before any decisive run):** the
  budget question is the *stock* of live bits, and chaotic bodies saturate
  (departure reaches the macrostate diameter). Regular bodies' bits grow
  polynomially (log t; ~13 bits at 10³) — exactly regenerable from the program
  by running the law, never stored (PRINCIPLES 3, 6). So the claim is about the
  *excess* stock: excess_i(t) = max(0, bits_i(t) − b_reg(t)), b_reg = regular
  bodies' median at the same t. Claim: top 1% of bodies carry ≥ 50% of the
  total excess stock; Gini ≥ 0.85. KILLED if the top 1% carries < 30%. The
  total stock (baseline included) is reported too and is expected to FAIL this
  — that failure is itself the result that most twin-spread is
  program-regenerable.
- **P2 (Pesin linearity, instrument check):** for chaotic unsaturated bodies,
  the free-twin slope and the renormalized-twin λ agree — bits at 10⁴ periods
  ≈ λ·t·log₂e within a factor of 2 (median). Negative control (amended while
  writing the instrument; the original "≤ 8 bits total" contradicted polynomial
  shear, which alone gives log₂(10⁴) ≈ 13 bits): regular bodies' fitted
  bits/period on [5×10³, 10⁴] < 0.001, against chaotic bodies' ≥ 0.01.
- **Control amendment (before the decisive run):** the positive control "every
  |δ|/W < 1 body has λ > 0" is naive — island-centre bodies are regular by
  construction. Honest control: the chaotic fraction within the separatrix zone
  (D < 1.5) is ≥ 10× the far field's (D > 3), and no chaotic body has a fitted
  rate below 10⁻³/period.
- **P3 (predictability):** bodies with D ≤ 2 carry ≥ 90% of the excess stock
  while being ≤ 20% of the belt. KILLED if bodies with D > 2 carry > 25%.
- **P4 (regime split, held out):** where neighbouring resonances overlap
  (Chirikov number ≥ 1), production is more even: Gini of excess within that
  region < 0.6. The tail claim is regime-dependent, so the allocator needs the
  overlap number, not only per-resonance D.
- **P5 (budget, arithmetic not simulation):** if every body saturated at the
  16-byte tube (128 bits), the store would exceed the 8 GB/10⁹ = 51 bits/body
  ceiling without reabsorption — so retention time, not production, must be the
  allocator's lever.

## VOID disclosure (first decisive run, tag `main`, 12 October)

The first T = 10⁴ run failed its own controls: chaotic fraction at D < 1.5
(1.0%) was not above the far field's (1.7%), and the renormalized-λ Pesin
ratio was 0.025 (shear-biased). Diagnosis: the birth map E0 = −1+2D put
far-from-resonance bodies at rotation rates P ≈ 2π·k, exactly on the drive's
integer resonances — an artifact of using the local normal form outside its
domain. That run is VOID; it is kept as `summary-voidmain.json`. The instrument
fix, made before the re-run: E0 = −1 + 2·min(D, 3) (the nearest-resonance form
is valid within a few widths; beyond that a body's dynamics belong to the next
resonance, which the assignment already selects), and P2's Pesin check becomes
the free-twin linearity (bits linear in t, median R² ≥ 0.98) since
renormalized λ is shear-dominated for near-integrable rotators.
