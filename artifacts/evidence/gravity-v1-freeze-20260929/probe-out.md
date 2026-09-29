Working...
All results reproduce. Premise probe complete — scripts in `/private/tmp/glm-scratch/gv1/` (`gv1.py`, `run_precession.py`, `run_energy.py`, `run_energy2.py`, `run_capture.py`, `run_light.py`).

# Premise probe: `es-lattice-gravity-v1` (float, PG river, G=c=M=1)

**Formulation.** Canonical PG Hamiltonian `H = β(x)·p − √(μ²+p²)`, `β = −√(2/r)·x̂`, split into two **exactly-integrated** pieces: **drift** A = `−√(μ²+p²)` (straight line in the local sheet, constant `u`; `|u|=1` for light — the contract's "drifts straight in the local sheet") and **kick** B = `β·p` (river advection `r^{3/2}(T) = r^{3/2} − (3√2/2)T` plus exact momentum focusing `w∥ ∝ √r`, `w⊥ ∝ 1/r`). Step S₂ = B(Δ/2)·A(Δ)·B(Δ/2) — kick at step boundaries, self-adjoint (time-symmetric); S₄ = Yoshida composition (w₁ = 1/(2−2^{1/3})). `Δ = η·r^{3/2}`, current state only. Horizon: absorbed when a substep would cross r ≤ 2. `x×w` is conserved **exactly** by construction (measured drift ~1e−12 over 10⁵ steps = roundoff). Oracle side: elliptic advance `4√(p/d)·K(4e/d) − 2π` (AGM) and GL-32 deflection quadrature, each cross-validated against independent RK4 (Binet / null ODE) to ≤6e−11, and the weak-field series where valid (the series is legitimately 6% off at p=20; RK4 adjudicates — elliptic is right). Self-tests: ICs machine-consistent, u≡0 fall rides the exact river law to 9 digits, circular invariants exact.

## Kill criteria (frozen, docs/gravity-law.md §Premise probe)

| # | Criterion (frozen threshold) | Result | Verdict |
|---|---|---|---|
| 1 | No η ≤ 1/64 keeps precession within 1% at p=20 **and** p=1000 | η=1/64: worst rel. err **0.93%** (p=1000, e=0.2, order 2); order 4: worst **1.5e−4**. Clean η²/η⁴ convergence (measured slopes 2.0/4.0) | **PASS** |
| 2 | Energy error exponent > 0.2 over 10⁴ orbits (p=20, e=0.2) | Variable Δ (as specified): exponent **0.47** (η=1/32, o2), **0.98** (η=1/64, o4) over [10³,10⁴]; drift saturates at ~8.65e−4 by ~3×10⁴ orbits (η=1/16: exponent 0.007, saturated). Fixed-Δ control: **1.8e−8 flat** (o2), **2.2e−10 flat** (o4), exponent ≈0.00 | **KILL** as measured at small η (see below) |
| 3 | E=1 capture threshold > 1% from L=4 | All 12 spot classifications correct (δ = 0.02/0.01/0.005 both sides, η=1/64, both orders); bisection L\* = **3.99942** (o2, 0.015%), **4.0000013** (o4, 3.6e−7) | **PASS** |
| 4 | Deflection at b=10 > 1% from GR | b=10: **0.41%** (η=1/64, o2), 1.3e−4 (o4), converging as η²/η⁴ to the oracle (α_GR = 0.590396). Light capture: 15/16 classifications correct at η ≤ 1/64 (one flip at η=1/64 o2, 0.5% below b_c); b\* within **0.08%** (η=1/128 o2), **0.003%** (o4) of 3√3 | **PASS** |

## Key numbers

**Precession** (advance/orbit vs oracle; 24 orbits at p=20, 120 at p=1000):

| (p, e) | Δφ_GR | η=1/64 o2 | η=1/64 o4 | η=1/128 o2 | η=1/128 o4 |
|---|---|---|---|---|---|
| (20, 0.2) | 1.227808 | 3.7e−4 | 3.6e−6 | 9.1e−5 | 2.2e−7 |
| (20, 0.5) | 1.233862 | 4.1e−4 | 9.4e−7 | 9.9e−5 | 7.8e−8 |
| (1000, 0.2) | 0.018935 | **9.3e−3** | 1.5e−4 | 2.3e−3 | 9.3e−6 |
| (1000, 0.5) | 0.018936 | 6.5e−3 | 1.3e−4 | 1.6e−3 | 8.3e−6 |

**Energy (criterion 2) — diagnosis.** The map is exactly symplectic per step; with a **fixed** Δ the energy error is bounded oscillation (1.8e−8 at η=1/32 o2, 2.2e−10 at η=1/64 o4, exponent ≈0.002 — so the split, the river formulation, and my implementation are sound). The mandated rule `Δ = η·r^{3/2}(current state)` makes the composition variable-step: the error walks up to an η-independent saturation level ≈8.65e−4 (reached within ~10³ orbits at η=1/16, still climbing at 4.8e−4 after 2.5×10⁴ orbits at η=1/64). Over the frozen 10⁴-orbit window the fitted exponent exceeds 0.2 exactly at the small η that criterion 1 requires. **As frozen, the two criteria are in tension**: precession wants η ≤ 1/64; the energy exponent at 10⁴ orbits wants η ≳ 1/16. The premise itself (river + drift-kick + exact kicks) is not the culprit — the **step rule** is.

**Capture (E=1, r₀=100).** Absorbed at L = 3.92/3.96/3.98, escaped at 4.02/4.04/4.08, both orders; escapers' r_min ≈ 4.44–4.99 (correctly skimming the r=4 unstable orbit region). L\* within 0.015% (o2) / 3.6e−7 (o4) of 4M.

**Light.** Deflection b=10: 0.592784 (η=1/64 o2) → 0.590395 (η=1/256 o4) vs oracle 0.590396. b=30 (not a kill case): o2 fails 1% at η=1/64 (1.8e−2), passes at η ≤ 1/128 (5.0e−3, 1.3e−3); o4 always passes (worst 1.1e−3). Photon capture threshold b\* = 5.19206/5.19631/5.19529 vs b_c = 5.19615.

**Events per orbit** (η=1/64, order 2): p=20: 484 (e=0.2), 502 (e=0.5); p=100: 418/437; p=1000: 407/425 — under the B9 budget of 512/orbit, but with only 2% margin at (20, 0.5). η=1/128 doubles counts (813–1003, over 512).

## Limitations, and where I might be wrong rather than the premise

- **Criterion 2 attribution:** my evidence says the drift is the state-dependent step rule (fixed-Δ control is clean to 1e−8/1e−10). If the intended integer law's cell clipping makes Δ a staircase of constants, the walk may differ. The saturation at ~8.65e−4 (bounded) means the KILL is about the *exponent within the 10⁴-orbit window*, not divergence — the integrator may legitimately read this as "fix the step rule, keep the premise".
- **The mandated step rule is ill-matched to light at large r:** arc/step = η·√r·r grows unboundedly (massive bodies: arc/r ≈ η·const, safe at all r). A photon anchored at r=10⁴ jumps *over* the lens region at η=1/64 (one 15,600-long chord); deflection measured from r_exit=10⁵ carries b-invariant drift up to 1.6e−2. I measured deflection from the exact turning point to r=800 (exact quadrature tail, ~5e−8) and capture from an exact invariant-constructed state at r₀=1000. The contract's cell-boundary clipping would cure this, but as-written "light follows the same law" with this Δ does not bend distant-anchored light correctly.
- **Marginal cases:** precession at η=1/64 order 2, p=1000 is 0.93% vs the 1% line — float noise or a different periapsis interpolation could cross it; order 4 is unambiguous. The one photon-classification flip (b=0.995·b_c, η=1/64, o2) disappears at η ≤ 1/128 or order 4.
- Float Python probe; no cells, no integer rounding (the real law's error feedback may do better on E). Horizon tests at substep endpoints only (a chord grazing through r<2 between endpoints isn't caught — irrelevant at the 1% level here). Deflection exit-radius truncation corrected analytically (exact-tail formula; the Born-style 2b/r² overcounts by ~200×).

**Run times** (per script, all < 60 s): self-tests 0.07 s; precession+events 4.1 s; energy 10⁴-orbit runs 26.4 s; energy diagnostics (fixed-Δ controls, 3×10⁴-orbit runs) 43 s + 21 s; massive capture 0.2 s; light 0.3 s.

**Bottom line:** the river premise survives precession, capture, and light deflection at the 1% level (3 of 4 kill criteria PASS, with order 4 leaving ~2–4 orders of margin). The energy criterion KILLs as frozen — not the drift-kick/river physics, but the `Δ = η·(current-state dynamical time)` rule, which also cannot steer distant light. Both are contract-level, fixable before the freeze: bind Δ to constants (or fixed per-orbit), and clip light steps by cell boundary as the contract already envisages.
