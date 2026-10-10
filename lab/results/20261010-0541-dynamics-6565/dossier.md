# Dossier — 20261010-0541-dynamics-6565 (lens: dynamics and attractors)

## Claim

Belt encounters do **not** avalanche: up to encounter-disk area fraction τ = 2 the arrival stream is an inhomogeneous Poisson riding the belt's slow temperature convergence (real Fano at or below a drifting-Poisson null in 7/8 runs), and an encounter *quenches* its participants (branching ratio ≤ 0 everywhere), so the smoothness risk from encounter physics is the slow rate drift, not cascades — while *elastic* encounter physics (the engine's gravitational encounters) runs away measurably, which is the actual gate we lack.

## Bottleneck

Board #4 (smoothness/allocator p99; "least-slack scheduling fed by surprise rates") and the lens bullet "can one event trigger a cascade, and what is the branching ratio?" The allocator's design assumed an answer nobody had measured: if encounters self-excite, one event detonates a burst and every frame budget needs a cascade reserve; if they don't, the queue needs no cascade feedback at all. Expected gain: deleting the (unbuilt) burst-reserve machinery, or, if a critical τ existed, a dimensionless concentration gate before the player (the only wildcard, whose influence creates concentrations — the taleb-09b5 scenario) trips it.

## Evidence

Model: Wisdom–Tremaine local shearing sheet, exact closed-form epicyclic motion, encounters = hard disks of radius R (area fraction τ = NπR²/L²), impulse with restitution ε = 0.7, N = 1000–2000, Ω = 1, T = 100–150 orbits, deterministic per seed. All commands in `run_sweep.sh` (each run 2–130 s); numbers in `post_table.txt`; raw streams in `*.events.bin.gz` (< 2.5 MB each).

post.py table (steady-state window after burn-in; branching = excess events involving either partner in the 30-orbit window after an event, minus per-body baseline):

| run | τ | n_ss | Fano(1Ω) | drift-Poisson null [p05,p50,p95] | branching | λ/body/orbit | per-body CV |
|---|---|---|---|---|---|---|---|
| t0005_s21 | 0.005 | 4,097 | 1.39 | [3.3, 4.1, 4.9] | −2.9 (obs 4.3, base 7.2) | 0.75 | 0.55 |
| t002_s21/s22 | 0.02 | ~86k | 9.5 / 10.4 | [56, 60, 65] / [73, 77, 82] | −168 / −178 | 27.1 | 0.12 |
| t01_s21/s22 | 0.1 | ~320k | 11.5 / 7.5 | [14, 15, 16] / [5.3, 6.2, 6.9] | −33 / −32 | 21.9 | 0.06–0.09 |
| t05n_s21 | 0.5 | 142k | 9.6 | [8.8, 9.7, 11.0] | −43 | 25.1 | 0.17 |
| t20n_s21/s22 | 2.0 | ~106k | 7.0 / 16.6 | [16, 17, 18] / [19, 20, 22] | −37 / −30 | 19.2 | 0.10–0.22 |

1. **No cascade.** Real Fano sits inside or below the drifting-Poisson null in 7/8 runs (only t01_s22 exceeds p95 by 7%). Collapsing same-pair bounce trains (≤ 1% of events at τ ≥ 0.005) changes nothing.
2. **Quenching, not ignition.** Branching is negative at every τ: after an encounter, the pair's subsequent-event rate is 16–69% *below* per-body baseline (restitution cools the participants; shear re-pumps them on ~orbit timescales). The stream is more regular than Poisson at short lags.
3. **The overdispersion that exists is the drift.** Raw Fano 7–17 tracks the belt's own slow temperature convergence (e_mean climbing ~26% over the τ=0.02 steady window), not bursts: counts per 2 Ω have CV 4–5% with no burst spikes.
4. **Unique attractor, no hysteresis.** τ=0.1 starts at e₀ ∈ {0.01, 0.3, 1.0} all land at e ≈ 6.4–7.0 by t=150 Ω (±5%).
5. **Elastic encounters run away.** ε=1.0 at τ=0.1 (run `e_elastic`, 13 s, shipped binary): e_mean grows 0.01 → 172 (epicycle ≫ box width) and the 400k event cap detonates in 60.6 Ω. With no restitution-like damping, a self-interacting belt heats secularly; its encounter rate grows superlinearly until the patch approximation dies. The engine's gravitational encounters are elastic; only τ_eff ≪ threshold (or a regulator: planets, real collisions) keeps a belt's rate stationary.
6. **Estimator calibration (canary).** A synthetic Poisson stream through the identical code gives Fano(1Ω)=1.097, a flat event-triggered profile, and the flat pair-repeat baseline the real runs are read against.

## Predictions
`predictions.md` was written before the sweep. P4 (attractor, no hysteresis) **held** (±5% ≪ ±30%). P2's pre-registered "cascade side" (my stated prior: Fano>3 AND b>0.5 at τ=2) **failed — b < 0 at every τ**; the "no-cascade side" (b<0.15) held everywhere. P1 **failed as written**: I predicted raw Fano ∈ [0.8,1.6] at τ=0.02, measured 9.5–10.4 — the confounder is the slow rate drift, and after the drift control the same run is null-consistent. P5 (null calibration) held. Lesson: with 10³-count bins, any smooth rate drift dominates Fano; a clustering gate needs a drifting null, never a homogeneous one.

## What would make it wrong

- Encounters here are contact-scale hard disks with restitution; the engine's are gravitational scatterings with focusing cross-section ∝ 1/v². Focusing changes the equilibrium (Safronov) but not the quench-vs-ignite dichotomy at contact scale; still, the branching sign should be re-measured once `crates/encounters` defines the engine's real encounter radius.
- 2-D patch, N ≤ 2000: no density waves from outside the patch; at τ ≤ 0.02 the equilibrium epicycle (~18) is a large fraction of the box, so those points are marginal for the local approximation (the branching and null comparison are internal to the run and unaffected).
- Runs are quasi-steady (e still drifting ~10%/50 Ω at low τ); the drift itself is one of the reported findings, but τ ≥ 0.5 equilibrium values are converging, not converged.
- Adoption cost: none for code — this deletes a worry. The one number worth carrying into the design: encounter arrivals may be treated as independent given the local rate; the allocator should *track the slow rate* (recompute the local encounter rate on ~10-orbit scales) and needs no cascade reserve. The gate we do lack: nothing today refuses an elastic self-interacting belt above the runaway threshold — if the player concentrates a clump to τ_eff ~ 0.1 with pure-gravity encounters, its event rate grows secularly and the frame budget follows. A dimensionless number (τ_eff and the cooling-per-encounter) decides it, in the spirit of "regimes are chosen by dimensionless numbers".

## Fit with PRINCIPLES

- "Compute only surprises. Cost follows change" (§3): the surprise *statistics* are Poisson-with-drift, so rate tracking, not burst reserves, is the cheap representation.
- "i care about the p95/99 results" (§12): the tail lives in the drift, and in elastic runaway, not in avalanches.
- "A failed expectation is not automatically a failed method" (§ H0183): P1's failure was my instrument's (homogeneous null), not the belt's.

## The lens

Dynamics-lens bias: I went hunting for an instability (my P2 prior said "cascade side wins") and found its opposite — a quenching, self-regulating process plus a *slow* instability (elastic heating) that a burst-hunt would miss. The blind spot named in the brief ("long-run behaviour can hide a transient that ruins a frame") inverted here: the transient is the drift; the frames are safe. What this lens nearly dropped: that the engine's encounters are elastic, where the same instrument shows the runaway — that, not cascades, is where a frame dies.
