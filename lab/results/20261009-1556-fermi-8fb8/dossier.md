# Dossier — H_live in a belt: measured growth law and the 10⁹ verdict

**Claim.** In a belt stored as program + scars, encounter distinctions do not
decide memory: per-body live bits grow only as (0.22–0.25)·log₂(orbits) for
interchangeable bodies and 0.5·log₂(encounters) + 5 bits per element for
identity-*tied* bodies, so 10⁹ belt bodies fit in 8 GB at any play horizon
(0.2–0.4 of RAM at k = 2¹⁰–2²⁰ encounters), and the real memory knob is the
tie fraction f_tie (observed/recorded bodies), not N or the encounter rate.

**Bottleneck.** Board risk "distinctions created per game-second (H_live)…
decide whether 10⁹ fit in 8 GB; not measured yet" (HANDOFF, 6 October;
queue `b-h-live`). This run measures the balance the definition asks for:
creation (kick entropy) against reabsorption (program refit + permutation
gauge). Gain: converts B18-memory's "information floor" from a phrase into a
number with a growth law; deletes the fear that encounter entropy accumulates
linearly (it does not: 99.96% reabsorbs at k = 2¹³).

**Evidence.** Monte Carlo of the law's own store model (law.md "Populations"):
bodies born as an exact stratified program (zero entropy, B18-style), then a
Poisson stream of impulsive element kicks; Gaussian kernel as analytic
control, Rutherford (Pareto-2, 100× range, median-calibrated) as the
realistic tail; scars quantized at the element quantum δ = σ₁/8; entropy by
Miller–Madow-corrected plug-in at N = 2¹⁶ bodies, 14 checkpoints k = 2⁰–2¹³,
3 seeds (1 tuned, 2–3 held out).

| quantity | prediction | measured (3 seeds) |
|---|---|---|
| H_A slope (tied bodies, per element) | 0.50 ± 0.08 | **0.498–0.501**, Gaussian control on the analytic 0.500 |
| H_multiset slope (permutation gauge + 2-param refit) | ≤ 0.35 | **0.17–0.28** (≈ ¼: quantile coupling ∝ σ_k^½) |
| reabsorption gap (H_A − H_multiset at k = 2¹³) | ≥ 2 bits | **7.6–8.5 bits** |
| Rutherford tail inflation of H_A at k = 2¹³ | ≤ 3 bits | **1.08 bits** |
| δ-halving adds | +1.00 ± 0.02 | 0.96–1.00 (atom-correct at k ≤ 2³; ≤ 4% residual estimator bias at k = 2¹³) |
| no-program control | ≈ 11.0 flat | 11.01–11.05 flat (analytic 11.05) |
| created : retained at k = 2¹³ | ≥ 10³ | 3.1–3.6×10³ (tied), 8.8–10.2×10³ (multiset) |
| 2-D correlation penalty | 0.3–1.5 bits | **8.3 bits — prediction missed, see below** |

Laws (Gaussian, per element, σ₁/δ = 8; +1 bit per halving of δ or σ₁):
H_A = 0.499·log₂k + 5.05; H_multiset = 0.216·log₂k + 0.89.

Sizing (5 elements, program 0.13 b, budget 68.7 bits/body = 10⁹ in 8 GB;
upper bounds — the 2-D miss below says 5×H_A over-counts ~2×):

| f_tie | k = 2¹⁰ | k = 2¹³ | k = 2²⁰ |
|---|---|---|---|
| 1 (all tied) | 65.5 b (0.95× RAM) | 76.3 b (**over**) | 101 b |
| 0.1 | 20.4 b | 24.3 b | 33.6 b |
| 10⁻³ | 15.4 b | 18.6 b | 26.2 b |

All-tied crosses the budget at k ≈ 1.9×10³ encounters (~1.7×10³ orbits);
f_tie ≤ 0.1 crosses only beyond ~10¹³ orbits. Creation traffic at 10⁹ bodies
is 0.07–0.7 MB per game-second (T_orb = 10³–10⁴ s) — five orders below the
M1's ~60 GB/s; retained is 0.041% of created at k = 2¹³.

Commands (each ≤ 60 s where possible; ~56 s per (seed, kernel) pass):
`python3 h_live_belt.py main` (seed 1, both kernels) · `heldout` (seeds 2–3)
· `twodim` · `kickentropy` · `python3 size.py` (laws, table, boundary).
Scripts and JSONs are in this folder.

**Predictions.** `predictions.md`, revision 2, written before the decisive
run (the first policy-B definition was ill-posed — (rank, residual) is a
bijection, so its joint entropy is identically H(x); replaced by the honest
multiset branch; a double-√2 scale bug was fixed and the control then matched
the analytic 11.05). Held-out seeds confirmed every growth-law number. One
prediction **failed**: the 2-D correlation penalty is 8.3 bits, not 0.3–1.5.
Cause, understood after the run: both elements' walk *magnitudes* share the
same Poisson encounter count (a common latent), so per-element scars are far
from independent. Held as a miss against the estimate, and as good news for
the store: a joint scar code (encode the shared encounter-count scale once,
then directions) costs ~2× less than per-element coding — my 5×H_A sizing is
conservative by about that factor.

**What would make it wrong.**
- Kicks here are exogenous and iid; real encounter rates depend on elements
  and co-orbital structure (taleb-09b5). Autocorrelated walks change
  constants, not the √k exponent; resonant *trapping* (a coherent pump, r4)
  would show up as a systematic drift — absorbed by the refit while it stays
  inside the program family, so the failure mode is family exhaustion, not
  diffusion: the Rutherford tail mismatch is ≤ 1 bit at k = 2¹³ but the
  ¼-slope law is measured to 2¹³ only; 2²⁰ in the table is the formula
  extrapolated, not measured.
- The permutation gauge needs interchangeability to be operationally true:
  every observation, news item or recorded event that ties a body must enter
  a tie ledger, or two bodies the player can tell apart get silently
  reshuffled. f_tie is a gameplay number (player screens, c-bounded news),
  not physics; I estimated 10⁻⁴–10⁻², unmeasured.
- The dense-gas regime is different (H2557: a nudge spreads ~4 bits per
  collision): there the store still keeps only state, but every body's state
  is freshly random each collision time, so H_live sits near the no-program
  floor, log(spacing/δ) — bounded, but the program buys almost nothing.
  Belts, not gases, are where program + scars pays.

**Cost of adoption.** No code change (this sizes, it does not build). For
`shipmem`/B18-memory: the measured floor for a belt is ~15–19 bits/body at
k = 2¹³ (f_tie ≤ 10⁻³), against 157 naive — the gate's "≤ 2× floor + 2 bytes"
becomes computable. Design consequences: (1) scar coding should exploit the
shared encounter-count latent across elements (~2×); (2) recompile cadence
only has to track the multiset refit — cheap; (3) the allocator's H_live
meter is a tie ledger, incremented by observations and event records.

**PRINCIPLES fit.** "this is nowhere near the floor on the size and
information theory says so" (24): the floor is now measured, and it is
log-growing, not linear. "his direct influence is bounded and propagates at c
at most" (5): f_tie, the tie fraction, is that influence made quantitative —
encounters without observation are reabsorbed exactly because no
differentiation exists. "the floor is what the player can differentiate"
(register): the same statement, now with the growth law attached.

**The lens.** Fermi arithmetic gave the ½ law and the sizing, but missed the
shared-count coupling (8.3 bits) that only the joint measurement showed —
the estimate's error was informative, not the run's. This lens also treats δ
and σ₁ as fixed knobs; the quanta co-evolve with the representation
(bottleneck 5). N = 2¹⁶ for the 60-second cap; the estimator is float + bin,
not the integer law (r2 says integer kicks accumulate exactly — the walk is
then a lattice walk with the same exponent).
