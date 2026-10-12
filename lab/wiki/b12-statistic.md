topic: b12-statistic
status: open
closed-by:
valid-while:
updated: 20261012-1904-q-wiki-b12-statistic-838c

# Gate B12's statistic (bounded against compound drift)

## Current best

**No separating statistic is freezable at the gate's horizon; two instruments are validated at ~50× it; the freeze turns on one decision — buy the horizon or declare it.**

B12 judges handoffs on the Jacobi constant (16 ships crossing a Jupiter-like doll edge ≥ 20 times, CRTBP; error ≤ 1e-4 relative; 200 planet periods). The question is error *type*: bounded against compounding (PRINCIPLES 13).

**v1's growth exponent is dead, measured many ways.** It reads level and saturation, not compounding: the float reference itself fails at every tolerance (medians 1.23–1.81) while iid noise passes (0.157) and a periodic bounded error passes (0.057) (20261006-0737-redteam-b12-stat-e5fe); on saturating series bounded scores 49–57 against a leak's 0.32–0.48 (inversion 3/3 on the corrected model, 2/2 physical — 20261009-2257-dynamics-a47e, 20261009-2348-…-09fb; law.md's P2: bounded 0.493 vs compound 0.305); and it false-kills bounded laws — 21/32 bounded plant-seeds on B12's own scene (20261009-0208-…-618f), +0.62 on a provably bounded transient (20261008-2206-library-73ca). The plane's standing conviction (exponent 1.026, 20261005-1404-q-plane-judge-65fd) is an instrument artifact: on the ships it answers (6 of 14) the Jacobi error's structure function is flat (β 0.052, z 0.02, max 3.1e-6; robust at step 9: β 0.000, 8e-8) — "the plane does not violate principle 13 on these traces"; its real exposure is coverage, 8/14 ships with no answer (20261012-1227-dynamics-bd4e; 20261007-1550-…-32f9).

**Root cause, measured twice.** On chaotic ships a real bounded error is a smooth function of the state — long-correlated like a leak (lag-8 autocorr 0.94–0.99 vs the leak's 0.96; 20261007-1550-…-32f9) and the bounded control is a walk in observation space (20261011-0134-scout-7567). At the gate's 200 P horizon no per-series statistic separates: exponent, Allan slope and rank panels each false-flag the bounded control (0.411 / 0.475 / z = 13.9; 20261011-0134-scout-7567).

**Two instruments separate, at ≥ 10⁴ periods:**
- **The α-profile** (decade-local growth exponents of the running max of |ΔC/C₀|, verdict on the settled top decade, threshold 0.2): zero misclassifications on B12's own CRTBP scene — bounded α_top 0.00–0.01 (32/32 seeds), compounding 0.94–1.22 (32/32) — at a 10⁴-orbit horizon buying four decades (20261009-0208-second-…-618f, gold). Domain: planted integrator laws on the gate's scene, not the frozen corpus; needs ≥ 4 decades, so it cannot run at 200 P (20261008-2206-library-73ca).
- **The exact-integer Allan rule R1** (leak ⇔ AVAR(T/4) > AVAR(T/32) on the Jacobi series integerized at 2⁴⁰): catches a planted per-kick compounding bias 8/8 ships on the law's cheap path (Wisdom–Holman), good controls ≤ 1/8, scale-invariant 2³²–2⁴⁸, ~20 integer lines, floats never decide (20261009-2348-second-…-09fb, gold). Window: T ≳ 16–32·τ_c (same run), and T ≥ 4·P_max else slow bounded modes alias as leaks (20261009-2257-dynamics-a47e). Domain: a planted bias on a WH toy, not the frozen corpus or the real plane.
- The measured detection horizon for the planted leak class on the real frozen ships is **10⁴–10⁵ periods — 50–500× the gate's** (20261011-0224-second-…-cc25).

**What survives regardless of the statistic** (20261007-0528-dynamics-f819, gold): the per-ship Kendall/permuted-z N(0,1) null construction is honest (permutation sd 0.95–1.03); and the phase channel is certified by the 1e-4 magnitude cap, not by any time statistic, on scenes with O(1) rotating-frame gain — the freeze must say so. What already works in the v2 code (20261012-1715-redteam-b12-v2-5dcb): the corpus, the injection check, the pairing, and the per-ship leak fit (recovers −2.00e-10/horizon exactly); the pooled verdict is the broken part.

Domain of everything above: the 16-ship CRTBP corpus (μ = 2⁻¹⁰), horizons 200 P (gate) to 10⁴ P (validated instruments), echo-based planted errors on Linux/x86, not the M1; the plane judged on its 6–8 answered ships.

## Refuted

- v1's single-window Jacobi growth exponent as the deciding statistic (20261006-0737-…-e5fe; 20261009-0208-…-618f; 20261009-2348-…-09fb; the prior page counts six golds, taste log 5–6 October).
- The recurrence ratio + per-cell drift replacement: the shipped test fails today — leak 1.094 below bounded-a 1.103; a slow leak defeats it (20261006-0737-…-e5fe).
- The Allan-deviation slope, worst-seed rule: dead band −0.77 with the wrong sign (bounded max +0.586 above leak min +0.037); the 96/96 was a white-synthetic artifact (20261007-1420-library-240c; killed by 20261007-1550-…-32f9).
- The plain variogram: bounded-white reads 0.847, 16/16 false (20261007-1420-library-240c).
- The arrow-of-time pooled Kendall z as frozen: a bounded 3e-9 offset switched mid-horizon reads −1.26 plain vs +6.40 fma — a machine-dependent verdict; time-localized bounded signatures fail at most switch times (design 20261006-1545-q-b12-design-9242, ungraded; red-team 20261007-0528-dynamics-f819).
- The v2 pooled one-sided rank score (`wt/cx-b12-v2`): a 5-ship leak + bounded-blip majority passes (arrow +3.1); a fleet-wide blip passes at −13.57 (no lower bound on `arrow ≤ 5`); rate-blind to 5×10⁴ the declared rate; the independent-rank 5-sigma null miscalibrated; the affine slow-state adjustment admits only the linear class (20261012-1715-redteam-b12-v2-5dcb).
- The derived-cap + 10×-horizon composite: on the real frozen ships echo false-fails (ratio 2.23 at 1.4e-14, under the floor), bounded false-fails (5.15; a-diffusion saturates only at the law's AXIS_CLIP), the derived cap degenerates to the reading clip on all 16 ships, compound missed (20261011-0134-scout-7567; refuted by 20261011-0224-…-cc25).
- Hurst-type Ĥ: its own pre-registered kill criterion fired; false-alarms on settle-to-bias series (20261012-0138-library-060f).
- The structure-function median β: orders the P2 controls (bounded 0.149 / compound 0.451 / drift 0.631) and acquits the plane, but classifies the slow 1e-12-per-period leak as bounded (β 0.176) — the recurrence ratio's killer again (20261012-1227-dynamics-bd4e).
- The multi-τ Allan variants R2/R3: their pre-registered false-positive kill fired (2/8 good control) (20261009-2348-…-09fb).
- Two-sided pooled |arrow| as a fix: it fails more bounded laws, the blip being bounded (20261012-1715-…-5dcb).

## Open directions

1. **Buy or declare the horizon.** Every validated instrument separates only at ≥ 10⁴ periods (618f, 09fb; cc25 measured 10⁴–10⁵); the gate runs 200. Either judge at the longer horizon on a cheap path (both instruments are one pass over a series the engine already samples; R1 is ~20 integer lines, machine-independent), or freeze a stated discrimination horizon (060f's surviving requirement: the instrument must declare it). This one decision unblocks the freeze; the race is settled among the runs compiled here — a checker's full-branch sweep found six more silver candidates, each with a measured limit in its own check.md, not yet folded in: recurrence-memory on the frozen ships (20261008-1719-dynamics-c13b), the return-matched memory curve (20261010-1947-quant-9c2f), window-mean vs max slope (20261010-1029-library-6cfc), variance-ratio + trend (20261011-0006-dynamics-a2a5), blocked-difference F (20261011-1234-library-069c), two-sided CUSUM (20261012-1438-library-e9f9). The census counts only after they are folded in.
2. **Per-ship verdicts, per-ship nulls** (20261012-1715-…-5dcb): the pool cancels minority leaks; permute dt labels within each ship's pairs for the null, bound every ship's z and |leak fit| ≤ DETECTABLE_LEAK. The corpus, injection check, pairing and leak fit already work. This also closes the teaching-to-the-test hole: the corpus is public and frozen, so a law can place its regime boundary to arm a cancelling majority.
3. **Own the invariant** (20261009-2257-dynamics-a47e): J is exact only in the CRTBP; a real doll tree has no exact J — the redesign must pick the invariant per handoff class.
4. **The echo platform split:** echo fails B12 on Linux (e5fe; 32f9's rerun: 0 of 14 above the floor) yet sits at 1e-15 below the floor on bd4e's traces — the oracle's convergence is machine-dependent, and floats must not decide verdicts (law.md records it; unresolved).
5. **Declare what the gate judges** for errors that rise through the whole horizon (slab τ=100P reads +51: within-horizon indistinguishable from a leak by any 200-period statistic — 20261012-1715-…-5dcb).

## Contradictions

- 20261009-0208-…-618f (gold) separates 64/64 seeds on B12's own scene; 20261011-0134-scout-7567 (silver) holds no per-series statistic separates on chaotic ships. Not a direct clash — 10⁴ P vs 200 P horizons, planted integrator laws vs the frozen corpus — but no run has put a validated instrument on the frozen corpus across that boundary, so the domain edge is asserted from two sides, not measured across it.
- Echo's B12 verdict is platform-dependent (fails on Linux in e5fe/32f9's reruns; below-floor on bd4e's same-scene traces) — unresolved oracle behavior, not a statistic question.

## Runs
- 20261012-1715-redteam-b12-v2-5dcb (red-team, pending grade): the v2 pooled statistic passes a minority leak at the declared rate; null miscalibrated; affine assumption measured; platform-noise at the cutoff.
- 20261005-1404-q-plane-judge-65fd (silver): the plane fails B12 at every cadence, exponent 1.026 — later re-read as an instrument artifact.
- 20261006-0737-redteam-b12-stat-e5fe (silver): the exponent reads level and noise, not compounding; the recurrence-ratio replacement fails a slow leak.
- 20261006-1545-q-b12-design-9242 (missing): the arrow-of-time pooled Kendall z design; its checker died on a 429.
- 20261007-0528-dynamics-f819 (gold): the arrow's null is honest; a bounded offset's verdict flips plain/fma; the cap certifies phase.
- 20261007-1420-library-240c (silver): Allan-deviation slope, worst seed; 96/96 on synthetic classes.
- 20261007-1550-second-20261007-1420-library-240c-32f9 (gold): Allan killed at the gate's conditions; real bounded error is long-correlated like a leak.
- 20261008-2206-library-73ca (silver): the α-profile; the window slope false-kills a bounded transient at +0.62.
- 20261009-0208-second-20261008-2206-library-73ca-618f (gold): the α-profile separates 64/64 seeds on B12's scene at 10⁴ orbits.
- 20261009-2257-dynamics-a47e (silver): saturation sets the exponent's slope; the exact-integer Allan rule proposed.
- 20261009-2348-second-20261009-2257-dynamics-a47e-09fb (gold): R1 catches a planted per-kick bias 8/8 on the law's cheap path; multi-τ killed.
- 20261011-0134-scout-7567 (silver): no per-series statistic at the gate's horizon; derived-cap + 10× composite proposed.
- 20261011-0224-second-20261011-0134-scout-7567-cc25 (silver): the composite refuted on the real ships; detection horizon 10⁴–10⁵ periods.
- 20261012-0138-library-060f (silver): Hurst Ĥ killed by its own criterion; "state the discrimination horizon" survives.
- 20261012-1227-dynamics-bd4e (silver): the plane's B12 failure is an instrument artifact; β passes the slow leak.
