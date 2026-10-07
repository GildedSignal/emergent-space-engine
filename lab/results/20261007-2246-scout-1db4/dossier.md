# Dossier — run 20261007-2246-scout-1db4 (scout lens)

## Claim

A cross-field scan plus a 12-case float falsifier kills the single-constant "synodic clock"
cadence rule (my own pre-registered prediction fails by up to 3 octaves), and measures the
cadence surface instead: a clean far-from-resonance belt body holds B14's 10% precession bar at
**2 kicks per orbit** (fully converged reference, worst seed 4) against the plane's uniform 128
— a 32–64× cut for the weak regime — while tide-dominated moons need 16–32 and near-resonance
belts have **no convergent float truth at all** (reference 256↔512 disagrees by ~90%), so the
cadence rule must be regime-aware and refuse inside resonance.

## Bottleneck

Board focus 1: kicks dominate the engine's cost; the plane pays `2^step_log2 = 128` kicks per
radial period on every forced body (`crates/universe/src/ctx.rs:42`). Expected gain if adopted:
~10–60× fewer kick events per body at gate-grade behaviour, decided per body from quantities the
law already compiles (the cycle memo's frequencies). What it deletes: most of the kick events,
and the premise that one fixed cadence (or one constant times the synodic ratio) can size them.

## Prior art (the scout's ranking)

Requirements as numbers: ≤ 60 s tests; behaviours B14 (precession 10%, bound/escaped), B17
(pump [0.8,1.25], libration ≥ 0.8, regime), B5-type error (walk exponent ≤ 0.2); rule decided
exactly in integers, changed only at body events (q-cadence.md); floats may explore but integers
decide. Fields that faced the same structure:

1. **Astrophysics block/individual timesteps** (Aarseth 1985; Makino 1991; Gadget-2/4; PKDGrav;
   Pham, Rein & Spiegel 2024, doi:10.21105/astro.2401.02849 — verified at source): the step
   follows the local variation of the *force* (acceleration/jerk/snap), never the mean orbit.
   Maps to: cadence from the tide's harmonic content, not from the radial period. **Fit: best.**
2. **MD Verlet-buffer tolerance** (GROMACS manual, verified): list refresh sized by an error
   budget on an observable (energy drift per particle), not by distance. Maps to: cadence
   sized by the behaviour gate, per body. Fit: good (the tolerance part).
3. **Multirate DSP (Nyquist)**: sample the fastest significant forcing harmonic. Fit: the
   mechanism scout-2098 smelled ("aliasing with the synodic phase"), but see below — a single
   constant fails.
4. Aarseth–ZACE next-step-from-predictor, HOLD/SyMBA hierarchies: already the engine's frame
   (law.md line 33); no new lever.

## Evidence

Float premise probe (the lab's idiom; integers decide nothing here). Planar elliptical
restricted three-body, exact Kepler drift (the tube stand-in; drift exactness controlled:
Δa ≤ 5×10⁻¹⁴, Δe ≤ 9×10⁻¹⁴ over 200 orbits with the perturber off) + DKD tide kick
(direct+indirect) at 1/n of the body's current radial period; n ∈ {1,2,4,…,128}, reference
n=512, second control 256. 8 seeds per case. Bars: precession relerr ≤ 10% (B14),
classification match, B17 pump/libration/regime, residual walk exponent ≤ 0.2. Moons:
central = planet (μ=1), perturber = star (μ=1e6, or 1e5 for M6), a_m = f·R_H. Belts:
perturber μ=1e-3 at a=1. N_min = smallest power of two holding all bars (median over seeds).

| case | N_med (worst) | ref ctrl 256↔512 | relerr@16 | prediction | verdict |
|---|---|---|---|---|---|
| M1 moon f=.30 e=.10 μ★=1e6 | 128 (128; rate bar met at 16–32) | 5.6e-2 | 0.101 | 4 | **wrong, +3 oct** |
| M2 f=.30 e=.30 | 16 | 1.1e-1 | 0.071 | 8–16 | half right |
| M3 f=.30 e=.05 | 16 | 3.8e-2 | 0.069 | 4 | wrong |
| M4 f=.40 | (1–4; most seeds escape) | 6.7e-1 | — | 4–8 | wall, not cadence |
| M5 f=.50 | (1–2; escapes) | 5.1e-1 | — | ≥8/unstable | unstable ✓ |
| M6 = M1 with μ★=1e5 | 8–16 | 2.9e-2 | 0.101 | 4 (= M1) | value wrong, **μ-invariance confirmed**: relerr surfaces coincide (0.352 vs 0.339 @8, 0.101 vs 0.101 @16) |
| B1 belt a=.51 (between 3:1, 5:2) | **2** (4) | **1.3e-3** | 0.003 | 8 | wrong, −2 oct: system-27ce's "floor 8" is resonance/e contamination |
| B2 a=.80 far | 6 | 1.0e+0 | — | 4 | unmeasurable (unconverged ref) |
| B3 2:1, 1W outside | 32 | 8.6e-1 | — | ≥32 | direction ✓ (ref unconverged) |
| B4 2:1, 3W outside | 16 | 9.6e-1 | — | ≤16 | value ✓, ref unconverged |
| B5 3:2, 1W outside | 17 (seeds 2–32, scattered) | 1.7e+0 | — | ≥16 | direction ✓ (ref unconverged) |
| B6 exact 2:1 | 16 (worst 128; 2 seeds no n≤128) | 1.1e-1 | 0.901 | refuse | ✓ refuse (a9c2 re-derived; relerr@16 0.90 = regime scattering) |

Reproduce: `gcc -O2 -o falsifier falsifier.c -lm`, then `while read name mup np a e hz muc seeds;
do ./falsifier $name $mup $np $a $e $hz $muc $seeds > csv_$name.csv; done < cases.txt` (58 s; CSVs stored gzipped),
then `python3 analyze.py` (25 s). Files in this folder. Calibration before predictions: none of
my own runs (predictions.md cites only scout-2098 and system-27ce).

Three load-bearing findings:

1. **The weak regime needs ~2 kicks/orbit, not 8 and not 128.** B1's reference is the only
   fully-converged belt one (1.3e-3); there the 10% precession bar is met at n=2 (0.4% error).
   Consistent with H0190 (averaged tides cut kicks 114×): the secular precession is carried by
   the time-averaged tide, which even n=2 samples well. The plane's 128 is a 64× overspend there.
2. **The single-constant synodic rule is dead; the constant is regime-dependent (~400×).** Moon
   and belt relerr surfaces at the same n differ by ~200× (0.101 vs 0.003 at n=16) although both
   are "tide vs orbit" scenes. e does not drive it (16 at e=0.05/0.10/0.30); μ does not drive it
   (M1 ≡ M6 surfaces). What differs: *which harmonic drives the gated behaviour* — the moon's
   precession lives at the quadrupole's 2Ω_syn harmonic, the belt's at the secular average. A
   rule must be derived per regime from the compiled harmonic content (the law already detects
   resonance from compiled frequencies, law.md line 29), not one K·s_syn.
3. **Inside/near resonance, float trajectory-relative cadence experiments are void at any n**:
   256↔512 reference disagreement 71–100% at B2/B3/B4/B5. This is a9c2's cliff seen from the
   truth side — no cadence experiment can be graded there; the law must refuse and escalate
   (resonant normal form / pair event). B6 at exact 2:1: 4–5 of 8 seeds have no n ≤ 128.

## Predictions

`predictions.md` was written before the sweep (cites only prior runs). Held: M5 unstable, B6
refuse, B3 ≥ 32, B4 ≤ 16, M2 8–16 (half), error-type boundedness at N_min. Failed: M1 (4 vs
16–32), M3 (4 vs 16), B1 (8 vs 2), M6's value (4 vs 8–16, invariance itself held). The kill
criterion I pre-registered ("no single (K, s_syn, e) combination predicts both surfaces within an
octave") fired: the hypothesis is killed as a universal rule.

## What would make it wrong

The bars are float stand-ins on my scene scaling; scout-2098's 4–6 for moons used a shorter
horizon and, by its own orbit counts, a different perturber scaling (UNVERIFIED — its dossier's
μ vs moon-orbit counts are internally inconsistent). If the plane's own integer law shows a
different relerr(n) surface (its kicks are orbit-averaged away from resonance, mine are
instantaneous DKD), the moon number could drop toward 4: the correct next experiment is this
sweep repeated with averaged kicks in the weak regime. M4/M5 and B2–B5 numbers must not be
quoted as cadence values (references unconverged or cases unstable) — I marked them above.

## Cost of adoption, fit with PRINCIPLES

Adoption = per-body `step_log2` from the compiled regime (secular-averaged: n≈2; harmonic:
n≈16–32; refuse near resonance), decided in integers at events only — one function
(`step_for`), no new state. Deletes 4–64× of all kick events. PRINCIPLES: "the cheapest compute
is compute not done" (1); "the simulation tells us what's next not us" (22); behaviour gates,
never error size (2, gates judge a representation); errors never compound — the refuse branch
keeps resonance out of cadence's reach (13). A failed experiment kills the configuration (the
single-constant rule), never the method (9).

## The lens (what scout may have missed)

Prior art optimizes convergence of trajectories, not behaviour gates on a compiled law; I did
not test averaged kicks (the plane's actual weak-regime kick form), nor 3-D/inclined cases, and
my horizon (1500–2000 orbits) is shorter than B14's 50 planet orbits for moons. The N_min
assignment is bar-sensitive (walk-exponent noise moves seeds an octave); the robust objects are
the relerr surfaces, the B1 floor, and the reference-convergence void near resonance.
