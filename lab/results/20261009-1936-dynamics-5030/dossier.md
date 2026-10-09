# Dossier — 20261009-1936-dynamics-5030 (dynamics lens)

## Claim

The averaged-kick layer's safe cadence is set by **kicks per secular period, not kicks per orbit**: with the WH-like shear kick order, behaviour (class, e_max ≤ 10%, bounded λ) survives down to N_lib ≈ 4–10 kicks per secular period across librating, circulating, retrograde-circulating and e₀ = 0.9 held-out cases (factor-2.2 collapse over case × tide strength), while kicks-per-orbit boundaries scatter 30×; the naive explicit-Euler order is 30–100× tighter and compounds (drift exponent 1.1–3.0 vs 0.01–0.7), and near the Kozai separatrix no cadence certifies the class at all (flips at 1613 kicks/period).

## Bottleneck

Board #1: "fewer kicks per orbit at the same behaviour" — kicks dominate engine cost; `q-cadence` queued, unmeasured. Expected gain: the certificate h_i = T_sec,i/20..T_sec,i/5 read off the compiled frequencies lets weak-tide bodies (T_sec ~ 10³ orbits) go from H0190's 0.3 kicks/orbit (h ≈ 3.3 orbits) to one kick per ~50–200 orbits — 15–60× fewer kicks, ~10⁴× below unaveraged — and it deletes the tuning question: one number per body family, computed from machinery the law already has (law.md: "a resonance is detected from the compiled frequencies").

## Evidence

Model: double-averaged quadrupole tide (H0190 K2's family: first-order quadrupole averaging, circular outer perturber), canonical (j, ω), j_z conserved; flow verified canonical against finite differences (≤ 6e-9), Kozai threshold lands exactly at cos i = √(3/5), C1's e_max = 0.9219 = √(1 − (5/3)j_z²) analytic value. Truth = RK4 on the same flow (dt = 0.004/ε, E-drift ≤ 1e-4) — this isolates the **cadence** axis; averaging-vs-GR is r9's axis (H0196/H0200-era: Clairaut bound τ₀ < 0.0036) and resonance kills averaging outright (r4). 440 map runs: 6 cases × 4 tide strengths (ε 0.3→0.01, T_lib 1.1→227 orbits) × 11 kick intervals h (0.008–512 orbits) × 2 orders, window 20 secular periods, shadow pair for λ.

Key numbers (shear order; "loose" = class exact + e_max ≤ 10% + λ·T_lib ≤ 0.5 + no j-violation):

- Boundary N_lib* by case (min over ε): C2 near-centre libration 4.2–6.7 · C3 small-island libration 5.7–9.4 · C4 prograde circulator 4.5–7.2 · C6 held-out e₀=0.9 12–19.2 · C5 retrograde circulator 66–105 · C1 separatrix-sitter **None** (fails at every cadence, up to N_lib = 1613).
- Not collapsing in raw h: at fixed case, h* = 0.25 → 8 orbits as ε shrinks (∝ T_lib), i.e. a fixed kicks-per-orbit rule is wrong by 30× across tide strengths alone.
- Kick order is load-bearing: Euler loose boundaries C2 161–269, C3 726–1210, C5 262–420, C6 None at ε=0.3; secular-energy drift exponents at N_lib ≈ 100–170: shear 0.01–0.71 vs Euler 1.08–3.00 (C2 Emax 4.1e-5 vs 1.0e-1).
- Period fidelity is the strict metric: ≤ 10% needs N_lib ≈ 6–28 (peak-detector noise outliers 67–76); the retrograde circulator's period never passes in range (needs ≥ ~1400) though its class and e_max pass at ~70.
- λ > 0.5/T_lib onset exists only for C1 (N_lib 21–34) and C5 (13–17); no hard bifurcation at N_lib = π — e_max and class survive below the linear-stability estimate (the discrete island persists).

Reproduce (each ≤ 60 s, from this folder): `python3 kick_cadence.py sanity` (4 s: canonical check, threshold, RK4 conservation, linear T_lib) → `python3 kick_cadence.py tlib` (11 s, writes tlib.json) → `python3 kick_cadence.py sweep` (18 s, writes results.json) → `python3 kick_cadence.py analyze` (< 1 s, writes rows.json, prints the boundary table). Linux/x86 Python+numpy only; orders of magnitude only.

## Predictions (outcomes)

Pre-registered in `predictions.md` before the sweep:

- **P1 (collapse in N_lib, factor ≤ 4): held for regular cases** (factor 2.2) but the families split: retrograde circulator ~10× higher, separatrix uncertifiable. The "no collapse in kicks-per-orbit" half held (30× scatter).
- **P2 (order load-bearing): held.** First analysis pass said otherwise — two bugs in my `analyze` (boundary taken from the wrong sort direction; `per_err` omitted from the pass criterion). Both fixed before final numbers; disclosed here. The corrected table separates the orders by 30–100×, and the drift exponents separate them everywhere.
- **P3 (plateau ≥ 20): held.** 127 shear runs at N_lib ≥ 20 (excl. C1): e_max > 1% or class flip in 12 (all C5 at 22–52 plus C4 marginal 1.1–1.6%); period > 10% in 30.
- **P4 (separatrix breaks higher): held, stronger than predicted** — not "higher floor" but "no floor": class is a coin flip under any cadence tested.
- **P5 (sub-π destabilisation): falsified.** The shear map keeps class and e_max below N_lib = π down to ~4–5; only weak λ growth appears (C1/C5). The linear-stability bound is not the behaviour boundary; KAM-type island persistence is.
- **P6 (cost): held** with the measured constants: h_i ≈ T_sec,i/20 (period-strict) to T_sec,i/5 (class + e_max).

## What would make it wrong

Double averaging: the real law single-averages (the perturber's phase stays live), so evection-type sampling resonances (member apse rate ≈ binary rate) are invisible here — if they bind, the floor rises toward per-orbit cadence in that band; the compiled-frequency detector already sees that commensurability, but the number 4–10 was not measured under it. The window is 20 secular periods: Euler's compounding is unambiguous there, but the retrograde circulator's strict-period failure may partly be my peak-detection on its ragged ω trace. One-DOF quadrupole only: no octupole (e-driving), no mean-motion resonance content — those are exactly the regions the law already excludes from averaging. Cost of adoption: none in code — the rule reads the existing compiled-frequency table; the law's kick scheduler replaces "fixed step in the drift's phase" with "per-body interval h_i = T_sec,i/20, flagged at the separatrix (ω_lib → 0) and at resonance, where averaging is already refused". Fits PRINCIPLES: "behaviours matter, not error size" (the boundary is a class/e_max/λ-type break, and sub-π survival is exactly error-type over error-size); "the simulation tells us what's next, not us" (the compiled frequencies, not a global step, set cadence); "compute only surprises" (a body in secular lockstep is not a surprise until its secular phase says so).

## The lens

The attractor framing found the floor (island persistence, not linear stability) but my first metric pass nearly buried the order result under two analysis bugs — a dynamics lens that trusts its own boundary-extraction code is a harness sharing its bugs (the memo lesson, again). Long-run blind spot: 20 libration periods cannot separate bounded drift from slow logarithmic walking on the chaotic layers below N_lib ~ 20; the B12-style exponent says bounded (0.01–0.71), but a 10³-period run on the two flagged cases (C1, C5) is the named next experiment. Also missed until late: C1 was mislabelled "deep Kozai" — it is a separatrix-sitter (e_max exactly the island-top value); the case list is honest about it now.
