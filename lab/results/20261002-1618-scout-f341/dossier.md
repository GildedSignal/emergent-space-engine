# Dossier — run 20261002-1618-scout-f341 (lens: scout)

## Claim

The 4x cut in kicks per orbit needs no new scheme in the smooth regimes — the plane's own
leapfrog at **16 kicks per radial period** holds every measured behaviour with large
margin (held-out moons: precession 0.89% vs the 10% B14 gate; resonance: pump 0.998,
libration 0.999 vs B17) — while higher-order splits and Gauss-node collocation are
refuted there per kick; the one place collocation wins is **inside encounter passages**
(B13-level assists at 12-20 tide reads vs 64+ for leapfrog).

## Bottleneck

Board focus #1: "fewer kicks per orbit at the same behaviour … kicks dominate the
engine's cost". Today the plane steps at 1/64 of the radial period
(`crates/universe/src/step.rs`); a kick is 24-29 µs on the M1 and the handoff names
"fewer kicks (GLM `q-correctors`)" the bigger lever. Requirements as numbers: kicks/orbit
64 → ≤16; behaviours that must not move: B14 (moon precession ≤ 10%, bound/escape
classification), B17 (pump ratio [0.8, 1.25], libration ≥ 0.8, regime match), B13
(assist ΔE/ΔL within 1%), B12-style Jacobi (≤ 1e-4, exponent ≤ 0.2); integer-exact path;
tests ≤ 60 s. Expected gain: ~4x off the dominant engine cost, deleting the safety
margin rather than adding a component ("the best part is no part").

## Evidence (cloud Linux/x86, 2 vCPU; orders of magnitude only)

`cd lab/results/20261002-1618-scout-f341 && python3 falsifier.py` — 36 s total,
`run-log.txt` and `results.json` in this folder. Float replica of the plane's law:
exact Kepler drift (universal variables, free), DKD kick of weight H at the interval
midpoint, H = P/n in phase, rebind per kick — as `step.rs` documents it. Validated:
independent dense RK4 cross-check to 4 decimals over 3 orbits; Jacobi constant of the
truth conserved to ~1e-6; LF error ladder on M2 is cleanly 2nd order
(0.020% → 0.134% → 0.892% → 5.58% at 64/32/16/8 kicks); Y4 ladder 4th order
(5.79% → 0.418% from 12 → 24 kicks); controls on both sides (LF-4096 truth control,
LF-8/16 negative controls that fail B13).

Moon M2, **held-out** (e0 = 0.3, 0.3 R_H, 120 orbits, truth LF-2048, precession
+0.1002 rad/orbit):

| scheme | kicks/orbit | precession err | max e(t) dev | Jacobi drift / exponent |
|---|---|---|---|---|
| LF-64 (today) | 64 | 0.020% | 4.7e-3 | 3.9e-5 / +0.0005 |
| **LF-16** | **16.1** | **0.892%** | 5.8e-2 | 2.0e-4 / +0.0018 |
| LF-8 | 8.2 | 5.58% | 9.4e-2 | 6.8e-4 / +0.0081 |
| Y4-12 (Yoshida 4th order) | 11.8 | 5.79% | 8.2e-2 | 7.1e-4 / +0.0075 |
| Y4-24 | 24.0 | 0.418% | 2.7e-2 | 3.0e-4 / +0.0088 |
| GP-4x4 (Gauss Picard) | 80 | 0.219% | 4.8e-2 | 5.2e-4 / +0.0091 |
| GP-3x8 | 96 | 0.078% | 2.6e-2 | 3.0e-4 / +0.0041 |

- Y4 ≈ LF-8-equivalent behaviour at ~1.4x the kicks: the 4th order's negative-weight
  constants eat its order in this regime. GP needs 96+ kicks (sweeps x nodes) to match
  LF-64. **No scheme beats plain leapfrog per kick on smooth tides.**
- Resonance R1 (2:1, μ = 1e-4, 200 inner orbits, truth LF-1024, control LF-2048):
  LF-16 pump ratio 0.998, libration amplitude ratio 0.999 (B17 pass at 4x fewer kicks);
  LF-8 pump 1.209 (inside [0.8, 1.25] but near the edge), R2 (detuned) 0.912/0.970.
  GP-4x1 passes B17 as written (0.882/2.01) but at 40 kicks — dominated by LF per kick.
- M3, **held-out** (0.6 R_H): the truth itself escapes at 2 orbits; every scheme
  classifies escape correctly (B14's first clause). Escape *times* scatter ±50% even
  between LF-64 and the LF-2048 truth: a chaotic quantity, never a gate (r2's lesson,
  and B14 already words it as classification).
- Flyby F1, **held-out** (hyperbolic passage in the planet's doll, periapsis 5 radii,
  v∞ ≈ 0.77 v_orbit, kick layer = star tide; truth LF-8192): LF-64 dE/dL error
  0.006%/0.008% at 64 reads; **LF-16 fails B13 (6.6%/7.4%)**; **GP-4 (one window over
  the passage, 4 Gauss nodes, ~5 sweeps = 20 tide reads) gets 0.134%/0.379%**, GP-3x1
  12 reads: 0.42%/1.19%. Collocation is the winner exactly where the tide is smooth on
  the window scale and the whole passage is one window.

## Predictions

`predictions.md` (original pre-registered, plus an amendment written after the smoke
killed the headline configuration and before the decisive run). Scorecard: **held** —
flyby (GP-4 ≤ 0.5% dE at ~4x fewer reads), Y4-12 < 5% on M1 (4.4%; 5.79% on M2, a hair
over); **failed, and the failures are the result** — "GP 1 window/orbit wins" (101%
error: the tide oscillates at the orbital frequency, a full-period window aliases),
"LF-8 fails B14" (it passes at 5.6%), "LF-8 leaves B17" (it stays inside), "GP-3x8 at
24-32 kicks" (true cost 96: sweeps x nodes). The premise "a better scheme is needed"
is what broke; the margin was the bottleneck.

## What would make it wrong, cost of adoption, PRINCIPLES fit

- Wrong if: the integer law at `per_period_log2 = 4` fails B14/B17 on the engine's own
  scenes (my evidence is a float replica, single seed per case, Newtonian tide, 2D); or
  if the e(t) deviation (5.8e-2 at LF-16 vs 4.7e-3 at LF-64) is a behaviour the gates
  should catch and do not; or if resonance seeds nearer the separatrix need 32. The
  integer rung decides: freeze criteria, run B14/B17 at 16 and 32 kicks per orbit with
  the existing planted negatives.
- GP-for-passages is wrong if the fixed-sweep integer form (3 sweeps, say; converged
  form took 4-5, warm start did not reduce it — impulses are quasiperiodic) drifts the
  assist, or if it chatters against the changeover. Its aliasing failure mode is
  measured, not guessed: never span an orbit of a bound body with one window.
- Cost of adoption: LF-16 is a constant (`step.rs` `per_period_log2`), zero new code,
  reversible, integer path unchanged (H is already a power-of-two fraction of the
  radial period; kicks remain sums). GP passages add one compiled structure (node
  weights are dyadic-rounded, fixed sweep count, pure function of state — observation
  stays pure; the impulses are law, not observation).
- Fit: "The cheapest compute is compute not done. Delete before optimizing" (P1);
  "we don't want errors that can compound" (P13 — Jacobi exponents ≤ 0.008, no secular
  growth at 16/orbit); "a fix signals the wrong representation" (P19 — the fix here is
  deletion); "A failed experiment kills that configuration, never the method" (P9 —
  GP-window-per-orbit and Y4-at-6 are killed configurations, recorded).

## Candidate ranking (the scout's survey; all not measured here are UNVERIFIED)

1. **Stepping policy from the gates (adopted answer):** run the existing law at the
   largest step the frozen gates allow. No source needed; the gates are the spec.
2. **Gauss-node Picard collocation of the kick layer** (measured; adopted for
   passages only). Cousins, verified at source: IAS15, Rein & Spiegel 2015
   (arXiv:1409.4779) — 15th-order Gauß-Radau collocation, iterated; Everhart's Radau.
   Mechanism maps to cells: impulses at Gauss epochs in drift phase, iterated to a
   fixed point; later nodes feel earlier impulses (the phase feedback r4 found
   missing). Killed configuration: window ≥ one orbit of a bound body.
3. **Symplectic correctors** (WHT 1996; WHFast, Rein & Tamayo 2015): ~zero extra kicks
   per orbit for ~2 orders of error (UNVERIFIED here). Still the best untested bet for
   closing the e(t)-deviation gap at 16/orbit — this is exactly the queued
   `q-correctors` lens; my falsifier is its control.
4. **Higher-order splits** (measured: Yoshida-4; SABA/SBAB of Laskar & Robutel 2001
   UNVERIFIED): order confirmed, constants hostile at coarse kicks; free drifts do not
   rescue them. Killed at 6/orbit outright.
5. **MD-style impulse MTS with force interpolation** (Biesiadecki & Skeel 1993;
   r-RESPA family): wrong structure — it amortizes a slow force across inner steps,
   and we have no inner steps to spend (the drift is free). Not tested.
6. **Event-triggered / self-triggered stepping** (control theory): the right frame for
   *when* 16 becomes 64 (slack-gated refinement near certificates) — a policy, not a
   scheme; the sparse order already points there. UNVERIFIED.

## The lens

The scout lens ranks by fit to requirements and hunts across fields, and it made me
tune for kick-minimal *schemes* where the answer was a *policy*: the falsifier's
negative controls (LF-8 passing gates I predicted it would fail) did the redirect. What
it may have missed: correctors untested (owned by the directed lens); single seeds per
case (a 256-seed integer rung is the adoptable form); 2D Newtonian tide only (the GR
tide's frequency content could differ); and it never measured the engine's own
`--kick-bench` at the new step, so the µs side of the 4x is inferred, not measured.
