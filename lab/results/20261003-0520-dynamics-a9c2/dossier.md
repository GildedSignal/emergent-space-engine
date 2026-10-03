# dossier.md — 20261003-0520-dynamics-a9c2 (lens: dynamics and attractors)

**Claim.** For the law's kick layer near the 2:1 resonance (B17's cases), the affordable
budget is bimodal — one or two kicks per orbit hold B17-grade behaviour for 256 orbits
everywhere outside resonance, and no rate up to 64/orbit holds it anywhere inside, down
to μ = 3e-5 — and the layer's own dynamical instability (a finite-time Lyapunov
exponent measured for free on its state) does NOT predict which side a configuration
is on (AUC 0.54): representational failure is invisible to surprise rate, so the
changeover trigger must stay the compiled-frequency resonance test.

**Bottleneck.** Board focus 1 (fewer kicks per orbit) and 2 (the changeover). The
bimodality says the allocator's job near resonances is binary detection, not budget
sizing: there is no gradient for a surprise-rate allocator to ride. The 1–2/orbit
number confirms H0190's direction at the float layer (its averaging already reached
0.3/orbit; this adds that plain un-averaged WH kicks already need only 1–2). What it
lets us delete: any per-region kick-rate policy graded by local activity.

**Evidence** (cloud Linux, 2×EPYC 7763, load 0.12, numpy 2.5.3; orders of magnitude only).
Planar elliptic restricted three-body, e₂ = 0.05, e₀ = 0.02, two starting phases,
5 μ ∈ [3e-5, 3e-3] × 14 detunings in thirds of W = 2.5μ^(2/3) plus a far control = 140
configs, 256 orbits. Truth: Yoshida-4 at T₂/1024 (convergence checked: e_max 0.12 →
0.041 → 0.022 as dt halves; the layer is the converged limit's neighbour). Layer:
exact Kepler drift + tide-only WH kick at K ∈ {1,2,4,8,16,32,64} per particle orbit.
Gate (B17 flavour): e-pump ratio in [0.8,1.25] (or |Δe|≤0.03 when e_max_ref ≤ 0.05) AND
resonant-angle regime (librate/circulate) match. Twins at 1e-12 (truth) and 1e-9
(layer K=16) give both λ.

- K* table by μ and detuning (`summary.json`, `Kstar_table`): outside |Δ| ≥ 2W, K* = 1–2
  at every μ, including the far controls. Inside, 50/140 configs unmeetable at K ≤ 64;
  the failing set is the resonance band plus one far control that sits on the 3:2
  (a = 0.77) — i.e. exactly the resonance crossings, asymmetric in k (e₂ forcing).
- Mechanism (consistent with r4 v2): the truth librates (32/140, net winding ≈ 1.1 rad,
  e pumped 2.8× at μ = 3e-5) while the layer at K = 64 stays at e₀ and circulates
  (winding ≈ 10 rad). First-order kicks along the unperturbed orbit give a circulating
  resonant angle and zero net pumping at every μ tested — the kill extends from r4's
  arc-integrated kicks to the plain WH layer, down to the quiet edge μ = 3e-5 where
  λ sits at the floor and nothing local warns of failure.
- λ as trigger: AUC(λ_layer → unmeetable) = 0.539, Spearman(λ_layer, λ_ref) = 0.11.
  The static 2:1-detuning mask also scores 0.52 because it is symmetric while the
  failing band is not — frequency detection of all p:q (as the law already specifies)
  remains the right test.

Reproduce (each ≤ 60 s where stated; the sweep itself ≈ 5 min):
- `python3 sweep.py smoke` (~50 s, 6 configs, sanity)
- `python3 sweep.py full` (~5 min) → `results.npz`
- `python3 analyze.py` (< 1 s) → `summary.json` (printed)
- convergence probe and gate split: see the heredocs in `run.log`'s session
  (truth e_max at dt_frac 256/512/1024 = 0.120/0.041/0.022; K=64: e-gate fails 49,
  e-ok-but-regime-flips 29, both-ok 62; truth librating 32/140).

**Predictions** (`predictions.md`, written before the decisive run): P3 (self-measured
λ predicts unmeetable, AUC ≥ 0.85) REFUTED — the central miss, reported as held. P5
(μ = 3e-5 all cheap) REFUTED — the failure is quiet at the smallest μ, which is the
most useful surprise. P2 partially held (out-of-band unmeetable at μ ≥ 1e-3: 10 ≥ 3;
in-band cheap: 31 ≥ 3) but its λ-conditioned numbers are void because the λ floor is
biased. P1/P4 void: the Cartesian twin carries Kepler shear (floor 0.048/orbit even
for regular orbits), so absolute λ levels and windowed toggles are not meaningful as
measured; the λ-based parts need an element-space twin (next run).

**What would make it wrong.** The layer here is a float WH probe with sampled kicks,
not the integer law with orbit-averaged kicks; the law's averaged kick (H0190) may
behave differently at the band edge (r4 says no, at the centre). One seed pair per
(μ, detuning) — the asymmetric band edge could move with phase. λ in element space
could still work where the Cartesian twin failed; if it reaches AUC ≥ 0.85, the
self-trigger revives. Cost of adopting: none for the numbers (they only bound), the
negative is a design constraint.

**Fit with PRINCIPLES.** "Compute only surprises" (§3) — the surprise here has no
local dynamical signature; the compiled frequencies are the surprise carrier near
resonance. "The simulation tells us what's next not us" (§22) — it does so through
its frequencies, not through its instability. "A failed experiment kills that
configuration, never the method" (§9): what dies is surprise-rate-graded budgets and
the λ-self-trigger near resonances; the dynamics lens keeps the bimodality result.

**The lens.** The attractor-hunting lens found bimodality (a phase transition in cost)
but its twin-in-Cartesian-space habit biased λ; an element-map metric (the law's own
integers) is the fix it missed. Blind spot confirmed: the ruinous transient here is
not a frame spike but a quiet, permanent misrepresentation with no instability signature.

**Grade suggested: LEAD** (real, cheap to keep, two refutations and one bimodal cost
law; not gold: float probe, not the integer law; H0190 already holds the cheap-kick
record; the λ refutation is the kind of negative the allocator design needs).
