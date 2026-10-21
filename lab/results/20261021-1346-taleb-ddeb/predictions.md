# Predictions (written before the decisive run)

Instrument: `crates/universe/examples/beltcensus.rs` — calls the shipped `ladder_ship` belt arm
verbatim (a uniform [2,3) AU, Rayleigh e σ=0.07 redrawn above 0.4), classifies every belt body
against the plane's three planets (Cinder 2⁻²¹, Home 2⁻¹⁸, Giant 2⁻¹⁰) with cbe6/7076's measured
class floors, and counts. Held-out cases = seeds and placement arms not tuned on.

Fermi estimates (before running anything):

1. **Crossing/encounter class (B13's 256/orbit): exactly 0** at every seed. Belt periapsis
   ≥ 1.2 AU > Home's apoapsis 1.007 AU; belt apoapsis ≤ 3 AU × 1.4 = 4.2 AU < Giant's periapsis
   4.936 AU; Cinder interior to Home. Prediction: 0/999,702 per seed.
2. **Strong-tide class (conjunction < 4.1 Hill of the Giant): a birth e-tail, ≤ 2e-3.**
   Only bodies with e ≳ 0.31 at a ≳ 2.9 reach < 4.1 Hill; Rayleigh σ 0.07 puts P(e>0.31) ≈ 1.3e-4,
   and the phase must align. Prediction: 0 at most seeds, ≤ 200 bodies at N = 1e5-scale.
3. **Resonance class: 8–16% of the belt, dominated by the Giant's second-order 3:1** at
   a = 2.52 AU (zone ≈ [2.48, 2.56] at pendulum width); first-order zones (2:1 at 3.27 AU
   half-width ≈ 0.125 AU) start at 3.148 > 3 AU, so **the first-order (uncertifiable, 67be)
   fraction is exactly 0**. Home/Cinder zones are ~0.06× narrower (sqrt μ): < 0.5% combined.
   Prediction: f_res ∈ [0.08, 0.16], 3:1 zone alone > 50% of it.
4. **Composed rescue: the desync grid's belt headroom stays ≥ 100×** with the tail at the
   encounter-class floor: rate = 5.3/belt-orbit clean, ~15 with the tail, against the shipped
   9,000/belt-orbit (both combs → ~30 against 9,000: ≥ 250×). Prediction: headroom
   (kick comb) ∈ [400×, 900×].
5. **Placement cliff (the design arm, not shipped law):** a belt born [3.0, 3.5) crosses the
   Giant's first-order 2:1 (3.273 AU, zone [3.15, 3.40]) → f_res > 25%. Prediction ~35%.
   A belt [1.4, 2.4) crosses Home's 2:1 (1.587) and 3:2 (1.31): f_res > 15%.
6. **Frozenness:** synodic periods with the Giant are 3.75–9.6 yr ≈ 1.2–3.0e8 game-s; a 10⁶
   game-s session (≈ 14 h at rtf 100 for 20 h wall... conservative: any playable session) gives
   < 0.01 conjunctions per body: the census is frozen on any playable horizon, no flight needed.
7. **Worst cell:** the 3:1 zone is ~0.08 AU wide inside a 1 AU belt: a cell covering it runs
   100% fine-class locally (bimodal per-cell cadence), ~5× the belt-average rate; no cell is
   256/orbit by crossing.

What would make the rescue die: f_res > ~50% (at the 256 floor) or any first-order fraction
≈ 10%+ (uncertifiable at any cadence per 67be — that class has no floor to compose with).
