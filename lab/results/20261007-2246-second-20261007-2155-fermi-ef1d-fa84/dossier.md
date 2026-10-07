# Dossier — run 20261007-2246-second-20261007-2155-fermi-ef1d-fa84 (second author on 20261007-2155-fermi-ef1d)

**Claim.** The checker's named experiment, done: on the plane's shipped configuration (the
three planets of `crates/universe/src/scenario.rs::PLANETS` acting on B18b's frozen belt
SPEC at 2.0–2.5 AU), the belt's Lyapunov distribution is **measured**, not assumed — and
with it the H_live claim changes quantitatively but survives with its sign: the measured
belt is **not** the toy's all-τ=300 belt. [FINAL NUMBERS BELOW once runs land; if a number
is still `??`, the run did not finish and this dossier says so.]

**Bottleneck.** Board risk "distinctions created per game-second (H_live)"; the checker's
reason (a): the only regime where memory could bind rested on an assumed τ_L = 300 orbits
for 100% of the belt. This run replaces both the assumption (τ_L distribution) and the
perturber set (measured: Cinder 2⁻²¹ M☉ @ 0.39 AU, Home 2⁻¹⁸ @ 1.00, Giant 2⁻¹⁰ @ 5.20 —
the real mass function, μ_Giant ≈ 9.8×10⁻⁴).

## What was done (commands, each regenerates from this folder)

- `python3 measure_taul.py full` — belt 2.0–2.5 AU (B18b SPEC shape: band ratio 1.25 = the
  game's [2048, 2560), e Rayleigh σ=0.07 cap 0.6, uniform angles), 8192 test particles,
  10⁴ yr, symplectic KDK dt = 0.02 yr under the four massive bodies (DOP853 rtol 1e-10,
  energy drift 3.7×10⁻¹¹; positions cubic-spline'd onto the kick grid). Per body: osculating
  a(t) at 42 log checkpoints; τ_L from windowed rms of the a-residual after per-body linear
  drift removal (the most any program re-fit absorbs). Writes `out/taul.json`. Controls:
  no-planets negative (0/2048 chaotic, τ = ∞ — the stepper creates no false chaos) and a
  dt/2 rerun (2048 bodies).
- `python3 hlive2.py` — the original toy verbatim (same store(), kick sea, seeds, 2000-orbit
  horizon = 10⁴ yr) with per-body amplification from the measured τ_L; `assumed300` control
  reproduces the original row (6.568 vs 6.567 bits/body — port verified to 0.03%).
  Writes `out/hlive2.json`.

## Evidence (measured)

- **Resonance map (Giant, in-band):** 1:3 at 2.498 AU (order 2), 1:4 at 2.062 (order 3),
  2:7 at 2.254 (order 5); no first-order resonance exists inside the band (period ratios
  2.8–4.7). The toy's τ = 300 guess was applied to the whole belt; the real structure is
  strips at these locations.
- **Measured:** chaotic fraction (τ_L < 3×10⁴ yr) = ??; median τ_L among chaotic = ??
  belt orbits; regular majority bounded rms = ?? AU = ?? quanta. e > 0.6: ??; a-band
  exits: ??.
- **H_live recomputed:** stock at 10⁴ yr = ?? bits/body (measured residuals, per-region
  quantum q_v = v·2⁻²⁴ ≈ 1.2×10⁻³ m/s); flow (toy continuation, upper bound — no
  resonance saturation) = ?? bits/body at 10⁴ yr, vs 6.57 assumed. Tube-outs: ??.
  At 10⁹ bodies: ?? GB at 10⁴ yr; the 34-bits/body (4 GiB) line moves from ~1.5×10⁴ yr
  (assumed all-300) to ??.
- **Record repairs (arithmetic, verified against the run's own files):**
  1. single-kick boundary m_cross = q_v·b_min·v_rel/2G = **1.5×10¹³ kg** at the code's
     BMIN = 10³ m (the dossier's 10¹⁵ kg was 67× generous; the checker's number confirmed);
  2. a size hierarchy moves D by Σnᵢmᵢ²: 10 members of 10¹⁷ kg among 10⁹×10¹² kg raise D
     ~93–100× → t* 2.6×10⁷ → ~2.8×10⁵ yr — the zero-H_live cold headline is conditional on
     the born program being equal-mass, now stated as a condition (the game ships no belt
     peer-mass hierarchy; the belt of B18b is massless draws);
  3. fermi.md term 4 relabelled: 10⁹×(0.3–32) kicks/P = **1.8–195 kick-events/s** of sim
     time (not 200–2×10⁴); at rtf 10⁶ → ≤2×10⁸ events/s (≤2×10¹⁰ ops/s at ~100 ops/kick) —
     the conclusion (kicks bind at galaxy rtfs) survives only with the ~100-ops/kick factor
     folded in, as term 5 does correctly;
  4. re-fit delta: 6.5667 → 6.5661 = **0.0098%** (the dossier said 0.02%).

## Predictions

`predictions.md` written before the decisive runs (P1–P10). Verdicts: [TO FILL].

## What would make it wrong

- The τ_L measurement is Newtonian float64 (the oracle's domain; the plane compiles
  secular motion, and this measures exactly the residual a compiled program cannot absorb).
  If the plane's compiled belt tracks the secular solution to ≪1 quantum, the measured
  regular-part bounded residual (?? quanta) says the cold zero-H_live headline holds on
  real perturbers; if that number were ≳1 quantum, the cold headline would be wrong — it is
  not the case here.
- The flow config is an upper bound (no saturation at resonance width); the stock config is
  the honest measured number at 10⁴ yr.
- The belt is massless test particles (as shipped); peer self-scattering remains the toy's
  layer, and the m_cross condition above now bounds when that layer's Gaussian sea loses
  validity.
- τ_L below 10⁴ yr may be truncated by the horizon: members still e-folding at 10⁴ yr are
  classified by their in-window slope only.

**Fit with PRINCIPLES.** "Measure before claiming" and §24 "The memory floor is
information": the one assumed quantity in the silver run is now measured on the shipped
configuration. "A failed expectation is not automatically a failed method" (H0183) applies
to the toy's rate law exactly as it did before.

**The lens.** Second-author lens: it fixes what the checker named and nothing else; it did
not re-examine the encounter layer beyond the m_cross condition, and the 2-D (planar)
measurement drops the inclinations the 3-D belt would carry.
