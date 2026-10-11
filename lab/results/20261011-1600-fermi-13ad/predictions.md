# Predictions (written before the decisive run)

Question: what is H_live's creation rate (irreducible scar bits per game-second) at 10⁹ bodies,
and which channel dominates? Channels: (A) ship–ship gravitational encounters, (B) contacts,
(C) encounters with massive bodies (planets/moons), (D) decisions.

## Fermi decomposition (pre-registered)

Belt: B18b's frozen geometry (p one octave, e Rayleigh σ=0.07, a ∈ [1,2) doll units, G=M=1).
Encounter skin ρ = 10⁻⁴ (r8's mid). (E,L) memo key: 32 bits ⇒ assume ~16 bits each over the
doll's bound range: q_E ≈ 0.5/2¹⁶ ≈ 7.6×10⁻⁶ (belt E-range 0.25 → ~2.3×10⁻⁵ within-belt).
I will sweep the key resolution 2¹²–2²⁰ to cover the unknown split.

## Predictions, held out (not tuned on)

1. **Channel A is dead by quantization.** Impulse ΔE ≈ v·2μ/(v_rel·d). One quantum of E at
   d = ρ = 10⁻⁴ needs μ ≈ q_E/5×10⁴ ≈ 10⁻¹⁰ of the doll's mass ≈ 3×10²⁰ kg (a moon).
   A ship (10⁶ kg ⇒ μ = 5×10⁻²⁵) is ≥ 5 orders below one quantum at d = 10⁻⁴, and still
   ≥ 4 orders below at contact range (d ≈ 5×10⁻¹⁰). **Prediction: quantized Δ(E,L) = 0 for
   every ship–ship gravitational encounter, at every distance.** If this holds, the encounter
   skin ρ can sit anywhere above the contact radius without creating scar memory, and channel A
   contributes exactly 0 bits at any N.

2. **Rate law.** Encounters per body per orbit at B18b geometry scales ≈ linearly in N
   (exponent 0.95–1.1 measured over N = 2×10³–5×10⁴), ≈ linearly in ρ, ≈ linearly in σ_e.
   Absolute value at N = 10⁴, ρ = 10⁻⁴, σ_e = 0.07: **between 0.01 and 0.3** (my two
   hand derivations disagree 10× — that disagreement is why this is measured, not asserted).

3. **r8 anchor.** At r8 v2 belt-0-like parameters (N = 10⁴, a ∈ [1,1.5], σ_e ≈ 10⁻²–3×10⁻²,
   ρ ∈ [10⁻⁵, 3×10⁻⁴]), my measured rate bracket must contain r8's truth: 427 encounters /
   (10⁴ bodies × 20 orbits) = 2.1×10⁻³ per body per orbit for some (σ_e, ρ) in r8's box.
   If my machinery cannot reproduce that within a factor of 3 anywhere in the box, my rate
   model is wrong and I report that.

4. **Contact channel at 10⁹** (ρ = R/a ≈ 4×10⁻¹⁰ for a 100 m ship at 1.5 AU): rate per body
   per orbit = rate(10⁻⁴) × 10⁻⁶ × 10⁵ ≈ **10⁻³–10⁻²** if scalings 1–2 hold. Total ≈ 10⁶–10⁷
   contacts per orbit in one 10⁹ belt.

5. **Bits per scarring event (channel C).** For planet-mass encounters (μ = 10⁻³), the entropy
   of the quantized kick (ΔE_q, ΔL_q) is **20–60 bits** — bracketing B18b's frozen 50-bit churn
   kick. For ship–ship (μ ≤ 10⁻²⁰): 0 bits (prediction 1).

6. **Session verdict.** At rtf 100: a 1.5 AU belt completes one orbit per 5.7×10⁵ game-seconds
   (≈ 6.6 days of play), so channel B creates ~10⁴–10⁵ scar-bits per game-second at 10⁹
   (≈ 1–10 MB per play-hour): inside the 4 GiB budget. A close-in belt (0.05 AU, orbit ≈ 10⁴
   game-seconds) multiplies this by ~50: **0.05–0.5 GB per play-hour — the budget survives
   only a ~10–100-hour session unless mortality or re-programming reabsorbs**. Individuation
   is the quantity to watch, not body count.

7. **What would falsify the "bounded" hope:** measured contact/scar rate at 10⁹ × bits/event
   × session length > 4 GiB with no reabsorption, or the rate exponent vs N > 1.1
   (superlinear individuation).
