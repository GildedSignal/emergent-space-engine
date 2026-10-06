# Predictions (written before the decisive run)

Run: 20261006-1029-system-06a8, lens: the whole system.
Claim under test: the kick cadence and the encounter finder are one schedule —
kicks as per-pair conjunction events (secular, zero-kick kernel between them)
match the fixed-cadence Wisdom–Holeman shape's behaviour with fewer
perturbation evaluations per ship-orbit, away from resonance.

Scene (float replica, heliocentric 2D, GM_sun = 4π², Jupiter μ = 1e-3, a_p = 5.2, circular):
48 non-resonant seeds (a ∈ [2.3, 4.4] away from 2:1 and 3:2 by > 0.25 AU, e₀ ∈ [0.02, 0.3]),
16 resonant seeds at 2:1 (a = 3.276 ± {0, .02, .04}, e₀ = 0.02, two phases),
8 edge seeds (a ∈ [4.45, 4.6], synodic period ≳ horizon), 40 yr horizon.
Truth: RK4 h = 2.5e-4 yr (convergence checked at h/2 on a subset).

Configurations:
- A_n: exact-Kepler drift + second-order (DKD) Jupiter kicks at n equally spaced
  phases per ship-orbit, n ∈ {4, 8, 16, 32}. This is the law's current shape.
- B_m: zero-kick secular kernel between events (Laplace–Lagrange quadrupole
  precession, e const), and m sub-kicks inside a ±30° synodic window at each
  conjunction, m ∈ {4, 8}. Events found from the synodic phase along the
  candidate's own trajectory. This is the proposed shape: the kick layer
  becomes the encounter layer's schedule.
- B0 (negative control): B with all events removed (pure secular).

Tolerances per seed (probe-level, B14-flavoured): |Δa|/a ≤ 0.005, |Δe| ≤ 0.05,
|Δϖ| ≤ max(0.1 rad, 10% of truth's precession). Band passes at ≥ 90% of seeds.
Resonant band (B17-flavoured): e-pump ratio e40/e40(truth) ∈ [0.8, 1.25].

Pre-registered predictions, cases not tuned on:

1. Positive control: A_32 passes the non-resonant band (else the harness is broken → VOID).
2. Negative control: B0 fails the resonant band (e stays ≈ e₀ while truth pumps;
   reproduces the lab's q-secular-v2 kill inside my own truth). If B0 passes
   everywhere, my truth cannot detect the resonant effect → VOID.
3. Non-resonant band: the loosest passing A needs ≥ 8 evals/orbit; B passes at
   ≤ 4 evals/orbit → measured gain ≥ 2×. I expect 2–6×, not 10×, at this
   scene's synodic rates (conjunctions every 1.8–5 ship orbits).
4. Held-out, failure edge: the edge band (a ∈ [4.45, 4.6], no conjunction
   inside the horizon, strong tide) is where B under-samples: B fails or
   degrades there while A still passes. If so, the conjunction schedule is
   valid only inside the perturber's secular regime — the edge belongs to the
   doll changeover (board item 2), not to the cadence.
5. Held-out, resonance: uncertain by construction (the resonant term's phase is
   not the conjunction phase). Either B_8 holds pump ratio in [0.8, 1.25] with
   ~4 evals/orbit (then the one schedule covers resonance too, deleting the
   two-regime split), or it fails and resonance keeps its own regime exactly as
   law.md line 68 already legislates. Reported as it falls.
6. Held-out, e₀ = 0.3 tail: B's advantage grows with e₀ (deeper conjunction
   windows carry more of the interaction).

Kill criterion for the claim: if the loosest passing A uses ≤ 2× the evals/orbit
of the loosest passing B on the non-resonant band, the cadence-as-schedule lever
is dead at this scene; the structural unification claim then stands or falls on
argument alone (lead).
