# Check — 20261011-0224-spacex-e46b (H_live of a belt)

Grade: lead

## Abstract for the integrator

Claim: a belt's live un-programmable information partitions by distance to strong resonances; scarred fraction ∝ μ^(2/3); ~7+5 bits/body at quantum 1e-6; a standing level, not a rate. Both headline runs reproduce bit-for-bit (17 s, 32 s). But three load-bearing elements fail adversarial checks: (1) the μ^(2/3) fraction law is geometric by construction — a uniform belt binned by the same W convention, no dynamics, gives 50.3/11.3/2.4% vs measured 52.8/11.9/2.8%; (2) the entropy instrument is quantum-blind (q cancels in its histogram; true q=1e-6 entropy is 10.6 e-bits + 7.9 Δa-bits in b0, not 7.0+5.2); (3) the far field fails below Jupiter's μ — the author's own μ=1e-4 log shows 57% of the belt beyond 3W scarred above 1e-4, unreported. What survives: the scar concentrates at resonance for μ ≈ 1e-3, and the standing level is real — flat at 4,718 yr (398 PJ orbits, my rerun), Jacobi 2.1e-6.

## What was reproduced

- `run-jupiter.json` and `run-mu4.json` regenerate **bit-for-bit** (excluding `wall_s`) from the dossier's commands, 17.3 s and 31.6 s, well under 60 s, ~200 MB peak.
- `predictions.md` (02:34) precedes the decisive runs (02:39–02:41). The author honestly reports P1 failing (21% vs <1%) and P3 missing; P2, P4, P5, P7 held.
- The Jacobi control is genuine: `hlive.py:122-131` computes the rotating-frame Jacobi constant (centrifugal term included), mean relative drift 2.1e-6, reproduced.
- The standing-level claim **survives an 8.3× longer horizon than the run**: my rerun at 2,500 PP-units = 4,718 yr = 398 real PJ orbits (N=1024, dE_rel 2.1e-6, counts_med 71 windows, refit on first 35) keeps the lead-binned medians flat: b0 8.5e-4 → 5.6e-4, b1 1.0e-4 → 2.2e-4, b3 4.3e-5 → 4.6e-5. A reabsorption fights a level, confirmed.
- The scar-vs-distance profile at μ=9.54e-4 is real: σ_e 4.1e-2 (b0) → 8.5e-5 (b3), median ~20× down, frac>1e-4 92%→21%; Δa pumps inside 1W exactly as reported.

## Why lead, not silver

1. **"The allocator's law, measured" is a definition, not a measurement.** The scarred fraction is the fraction of the belt within ±W of the four listed resonances — pure geometry of the binning convention. A uniform belt with zero dynamics, binned identically, gives 50.25% / 11.32% / 2.43% at μ = 9.54e-4 / 1e-4 / 1e-5 against the measured 52.8% / 11.9% / 2.76%. "Predicted 11.7%, measured 11.9%" is arithmetic self-consistency. The dynamical claim that would matter — the scar-size profile collapsing in W-scaled distance across μ — is contradicted by the author's own data: refit σ_e at 3–5W is 8.5e-5 at μ=9.54e-4 but 3.4e-3 at μ=1e-4 (40×), i.e. there is no scale-invariant profile.
2. **The bit-count instrument cannot see the quantum.** `bits()` divides by q, then histograms 4096 bins over ±max|v| — q cancels, so the JSON reports identical H at q=1e-6 and q=1e-8 (7.0 vs 7.0). Quantum-true entropy (integer-quantize, then entropy), same data, same seed: b0 e-scar 10.62 bits (not 7.0), Δa 7.86 (not 5.23) — ~18.5 bits/body total, 1.5× the headline. The dossier's own caveat "at 1e-8 the same scars cost ~6.6 more bits" is contradicted by its own JSON (naive bits grow, H does not — the author never noticed the instrument is q-invariant). The "~11×" holds only against a 16-byte-tube strawman (128/18.5 ≈ 7×); against their own per-field naive figure the gain is 1.7–2.6×.
3. **The far-field claim fails at the second μ, from the author's own log, unreported.** At μ=1e-4 the dossier table shows only b0 and the >10W row. The omitted b3/b4 rows: 2,316 of 4,096 bodies (57%) beyond 3W carry refit σ_e 3.4e-3 / 6.2e-4 with 52% / 40% above 1e-4. Only >10W (8%) is clean. So "programs hold beyond 3W" and the "~0.4 GB at μ=1e-4" extrapolation (which assumed only 11.9% scarred) are contradicted by the run's own output; the memory-relevant scarred fraction at μ=1e-4 is ~96% of the belt.
4. **Third μ (my run): the partition itself disappears.** μ=1e-5, N=8192: refit σ_e is flat at ~1.3e-3 across every bin including >10W (16% above 1e-4 there; b5 σ 2.7e-4). Doubling resolution to 700 steps/orbit leaves it unchanged (2.77e-4 vs 2.74e-4) — not integrator noise; the first-order program or unlisted higher-order resonances dominate, and distance to the four strong resonances is no longer the coordinate. The fraction still tracks μ^(2/3) — because it is geometry.
5. **The headline horizon is mislabeled 6.28×.** `PP = sqrt(AP³/GM)` is Jupiter's inverse mean motion, not its period. The run is 566.2 yr = 47.7 real PJ orbits; the dossier says "300 PJ orbits ≈ 3,560 yr" and "flat over 300 perturber orbits". The log's own `t_final_yr: 566.2` contradicts the headline (a headline the log contradicts). Physics numbers are internally consistent; every horizon statement is 6.28× overstated. The saturation claim happens to survive (my 4,718-yr run), but not as evidenced.
6. **The shipped code cannot regenerate a stored artifact, and an edit between decisive runs is undisclosed.** `hlive.py` mtime 02:40 sits between run-res (02:39) and run-jupiter (02:41); the current script regenerates run-res's params/stats/scar_bits bit-for-bit but its `traj` has a different schema (`t_yr`/`pj` series vs lead-bins) — the growth instrument was rewritten between runs and the dossier does not say so. The old-schema traj also labels t/PP as "pj", carrying the 2π error.
7. **The noref baseline is a wrong-constant strawman.** The "textbook" A(a) = 0.75·n·μ·α·b_{3/2}^{(1)} is ~7× the free-precession rate the truth itself exhibits (probe on 925 far-field bodies: ω/A = 0.137; against the standard Murray–Dermott ¼·n·μ·α·b it is 0.41). "Reabsorption is mandatory" survives (even the ¼ constant is ~2.4× off the measured rate), but the stated mechanism ("first-order rate error × e") is misattributed. P6 is borderline: rms σ moves 30.5% on b1 at doubled resolution (claimed ≤14%, threshold 25%); medians do stay ≤~14%.

Per "What not to do": a headline the log contradicts, a stored artifact the shipped code cannot regenerate, and an undisclosed edit between runs — the run loses its grade. Combined with two headline numbers broken by adversarial checks, this is not one experiment from gold; the claims themselves must be rebuilt.

## Novelty

H_live is named and unmeasured in HANDOFF ("not measured yet", line 70) and required by plane.md's dashboard (line 36) and B18's "measured information floor". components-98bc (gold) measured the birth program (0.126 bits/body); this is the first measurement of the scar layer under a live perturber. q-secular-v2's kill (14.5% vs 50%) is consistent with, and distinct from, this run's b0 result. Novel, on a listed bottleneck.

## What the author missed

- The μ-scaling "confirmation" is the bin definition confirming itself; the falsifying control (does the *profile* collapse in W units?) was in their own μ=1e-4 log and went unreported.
- The entropy instrument was never checked against a known distribution: any smooth density on 4096 bins over ±max returns ~7–12 bits regardless of the quantum — the q1e-8 field in their own JSON returning identical H should have been the alarm.
- The 2π in PP: `hstep` (correct years) and `n_steps` (PP missing 2π) were both in hand; one subtraction would have caught the 566-vs-3,560 mismatch the log itself prints.
- The lens was right that the memory floor is information, but the "11×" compares against a 16-byte tube nobody proposed storing per scar; the honest per-field gain (1.7–2.6×) still leaves scars ~15× cheaper than birth-era naive storage — a good result undersold by a wrong multiplier.

## What the next run picks up (the surviving lead)

A belt at a Jupiter-like perturber does carry its live information as a resonance-local standing level, robust over 4 kyr with a Jacobi-clean truth, ~10–18 bits/body at quantum 1e-6 (correctly measured). Next run: quantize before entropy; label horizons in real PJ orbits; include the true LL constant and a second-order/forced-mode program (e_J ≠ 0); report all bins at both μ before any allocator rule. That is the instrument `b-h-live` needs; adopt nothing from this run's extrapolations.

## Provenance of this check

Reproductions and adversarial runs in `/tmp/check` (rj, rmu4, rres, rmu5, rmu5b, rlong, hlive_q quantum probe, rate probe); run folder untouched except this file. No commit, no push. Wall: ≤81 s per process, peak ~200 MB.
