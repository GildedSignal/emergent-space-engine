# Dossier — 20261010-1152-fermi-e9a5

**Claim.** The live distinguishing information of a 10⁹-body belt is bounded in practice:
99.99997 % of the kick information a belt creates per orbit is reabsorbed by state
quantization, the live store is ≈ 20 bits/body after one orbit and grows at ~1 bit per
*time-octave* (34 bits after 16 384 orbits), so 10⁹ bodies fit 8 GB with 1–2 octaves of
headroom — and the binding constraint is not the store (floor-insensitive, logarithmic)
but scar-mutation churn (∝ 1/q_v), which the allocator must budget, not the memory.

**Bottleneck.** The board's focus item "fitting 10⁹ in 8 GB … decided by distinctions
created per game-second" and HANDOFF's open risk "H_live: not measured yet". This run
measures it: the answer deletes the "memory might blow 8 GB" worry for smooth scenes,
quantifies where it does break (concentrated regions at 3 dof), and hands the integrator
the q_v sizing rule. Gain: an unmeasured scaling risk becomes a design table; nothing to
build for the smooth case.

**Evidence** (all from `python3 probe.py`, 3.4 s, < 100 MB, seed 20261010, 8 vCPU shared,
loadavg 1.7; outputs `metrics.json`):

Scene: a = 2.2 AU, width 0.5 AU, N = 10⁹, belt mass 2×10²¹ kg (m = 2×10¹² kg each),
in-plane dispersion σ₀ = 20 m/s. Kernel: shearing-sheet 2-D flux dλ = 2(Σ/m)v db with the
exact hyperbolic per-body kick (focusing included). Store = shipmem form P (program +
residual scar); sub-floor kicks accumulate as a random walk and mutate the scar on
quantum crossings.

Controls (both sides):
- Positive: exact kernel vs direct leapfrog integration of the passage — 5.6×10⁻⁴
  (canonical, impulse regime) and 2.7×10⁻³ (cold, focused); Richardson 7×10⁻¹⁴.
- Negative: impulse-only kernel on the cold case deviates 14.6× — the probe can fail.
- Internal: MC σ(t) is floor-invariant as it must be (0.0050 / 0.0051 / 0.0052 m/s at
  q = 10⁻⁶/10⁻⁵/10⁻⁴); Σ-linearity of rates 1.0002 against 2500×.

Numbers (q_v = 10⁻⁶ m/s, the finest tested floor):
- Above-floor kicks: 354 per body per orbit (belt); 8.9×10⁵ in a 2500×-dense region;
  scaling β = d ln λ/d ln q = −1.02 per clean decade (cold swarm −0.994 over 5 decades;
  the fitted −1.3 in metrics.json is grid-floor contamination at q ≥ 10⁻³, stated).
- Churn (scar mutations incl. sub-floor quantum crossings): 384/orbit/body = 3.4×10⁻⁴
  per body per game-second at the plane's 100× ⇒ 3.4×10⁵ events/game-s at 10⁹ ≈ 5 700
  per 60 fps frame — affordable at ~100 ns/event (0.6 ms/frame).
- H_live per body: 20.0 bits after 1 orbit (= 10⁶ game-s at 100×; 2.5 GB at 10⁹),
  34.2 bits after 16 384 orbits (2.7×10⁸ game-s ≈ 8.5 years of play; 4.3 GB at 2 dof,
  6.4 GB at 3 dof). Dense ×2500: 45.5 bits (5.7 / 8.5 GB). Cold swarm: 47.9 (6.0 / 9.0 GB).
- Growth law: 1.00 bit per time-octave (belt, dense — pure 2-dof diffusion), 0.68 for
  the cold swarm (the predicted self-limiting σ ∝ t^⅓ regime once σ ≫ σ₀).
- Reabsorption: creation 3 368 bits/body/orbit vs live growth 9.3×10⁻⁴ bits/orbit —
  99.99997 % of created information is discarded by macrostate quantization.
- Octave rule: each octave of σ_resid/q_v costs n_dof bits/body = 0.25–0.375 GB at 10⁹;
  each octave of coarser floor saves the same. Program side adds 0.126 bits/body
  (components-98bc) and the pending-influence register ~4 bits/body — both negligible.

**Predictions** (`predictions.md`, written before the run): P2 (β = −1.0 ± 0.2) held;
P4 (Σ-linearity, +11–12 bits) held (1.0002, +11.3); P6 (slope ≤ 1.5·n_dof, declining
after crossover) held (0.68 measured). P1 failed by 10³ (354 vs 0.1–0.5 per orbit): a
units slip in my hand conversion (3.44×10⁻⁶/s × 1.03×10⁸ s = 354), caught because the
code was checked against the hand estimate — the hand *formula* was right. P3 missed by
7 % (34.2 vs 26–32): my hand variance kept only the weak Coulomb term and underweighted
the strong-kick tail that dominates ⟨Δv²⟩. P5 partial: the dense scene breaks 8 GB at
3 dof (8.5 GB) but not at 2 dof (5.7 GB).

**What would make it wrong.** (i) Coherent forcing is assumed absorbed by program
re-inference (shipmem's `seal`); chaotic resonance zones grow residuals ~linearly in t
(Lyapunov), doubling the bit slope there — still log-bounded, but B18b's belt rung
should pin the resonance fraction. (ii) Thin-disk 2-D flux, isotropic kick directions,
collisions excluded (b < 12 km: the fragmentation channel is a different store), player
entropy excluded (one body, O(kB/s)). (iii) σ₀ held fixed as the encounter-velocity
floor (the belt's dispersion is assumed damped/re-inferred into programs); monotonic
self-stirring would raise σ₀ itself — H still grows only as log. (iv) The dof count
(2 vs 3) is decided by the law's representation, not information theory; I bracket both.
(v) Poisson neighbors: clumped/forming scenes (the taleb gold's fleets) violate the flux
independence — probed here only as parameter changes (Σ ×2500, cold), not as geometry.

**Cost of adoption.** None in code: the octave and churn rules size q_v and the hot-map
budget in shipmem/plane designs. If the integrator keeps q_v ≈ 10⁻⁶ m/s at 100× warp,
churn is 5.7 k events/frame at 10⁹ bodies; coarser floors buy churn linearly, memory
only logarithmically. In concentrated regions the sub-floor accumulator should go
per-cell (PRINCIPLES 6: "influences below one quantum accumulate … aggregates"), which
divides churn by the cell population.

**Fit with PRINCIPLES.** "The memory floor is information-theoretic" (standing
decision): measured — the store is the residual macrostate entropy, not the kick log;
reabsorption 99.99997 %. "Compute only surprises": the surprise rate is 384
mutations/orbit/body, not 10⁹ states. "this is nowhere near the floor on the size and
information theory says so" (24): confirmed — 34 bits/body against the naive 157.

**The lens.** The Fermi lens's own discipline caught my two code errors (the 2-D flux
factor and the per-orbit conversion) because every constant was derived by hand first;
its blind spot here is correlations (Poisson neighbors, no formations as geometry) and
the representational dof question, both flagged above rather than measured.
