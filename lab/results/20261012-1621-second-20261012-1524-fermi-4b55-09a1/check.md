Grade: gold

**Abstract for the integrator.** Second-author run fixes the silver's broken record. Reproduced bit-for-bit: soi_truth.py (my own run, 46 s) and both original scripts (regen.sh, runner + log); the Newton sign-flip is verified calculus. The corrected claim stands: Γ_SOI = 1.31×10⁻² transits/body/orbit; at 10⁹, H_live ≈ 21 bits/s (rebinds 10.2; player ~10, assumed; contacts 0.9) ≈ 9.3 kB/h; mutual encounters inert (m_crit ≈ 4.3×10¹⁸ kg); only post-repopulation mixed entropy can approach 8 GB. Attacks: dt 0.0375 (+0.31%); seeds 44/45 (±2%); sampler exact; occupancy-duration identity closes; σ_e ×10 lifts the truth only ×1.3; μ scaling smooth. The Newton and anchor cross-checks collapse off-regime (0.34×, 4×) — noted on the page. Adoption cost: none in code.

## Reproduction

- Clean copy of `soi_truth.py` to /tmp: 45.8 s, `soi_truth_results.json` **identical** to the stored record (diff empty). The runner's regen.sh (exit 0, regen.log) additionally regenerated both originals bit-for-bit, confirming the superseded values it reconciles: stale P3 54.40, sign-bug 5.985×10⁻³ (1197 hits), stale headline 42,462.4 bits/s.
- The sign-flip diagnosis is correct calculus, not just an empirical patch: residual `dth = λ_body − n_pp·t` has derivative `n_b − n_pp = −dn`, so the shipped `t −= dth/dn` walks away from the root; `t += dth/dn` is Newton. The 460× decomposition also checks out (written headline 4.7×10³ vs corrected rebinds 10.2 bits/s; instrument bug 2.19×; text slip 10³).
- File times order correctly: predictions.md 16:23:57 → soi_truth.py 16:25:16 → dossier 16:28:11 → wiki 16:28:42. Predictions preceded the instrument and every output.

## Adversarial cases (mine, /tmp/check2/, ~60 s total)

1. **dt finer than the author's finest** (0.0375 vs their 0.075): 2627 episodes, 1.3135×10⁻² = **+0.31%** vs the adopted 1.3095×10⁻². The truth value is converged, not resolution-limited.
2. **Hot belt σ_e = 0.05, ×10 the tested value (outside the author's range):** brute truth 1.7315×10⁻² — Γ_SOI rises only ×1.32 for ×10 eccentricity, so the 10⁹ table and the co-dominance verdict are robust in σ_e. But the two cross-instruments degrade: sign-fixed Newton **0.34×** the truth (1165 vs 3463; my transcription reproduces the author's 2380 exactly at cold settings, so this is a genuine regime limit — event-driven conjunction Newton misses transits once the epicycle term matters), analytic anchor 4.0× (was 1.7×). Neither carries the headline; both were presented as agreeing instruments without a domain caveat — corrected on the page.
3. **μ scaling** (author tested only 10⁻³): μ = 10⁻⁴ → truth 2.97×10⁻³, μ = 10⁻² → 6.23×10⁻²; smooth, sub-linear in R_SOI, anchor 1.5–2.0×. The "k secondaries → k×" extrapolation is untouched; the μ dependence is now measured (roughly ∝ R_SOI^1.5).
4. **Occupancy-duration identity** (independent of episode logic): mean 60.5 bodies inside the SOI; 2619 episodes × 2.90 doll-time mean duration / 125.66 = 60.4 — closes; durations are chord-like (2R_SOI/v_syn ≈ 2–3) and dt-stable (2.90/2.89 at 0.15/0.075). No threshold fragmentation; episodes are genuine transits.
5. **Shared-instrument audit:** the belt sampler (shared verbatim by every run on this topic) is exact — a uniform (mean 1.2500, var 0.02082), e Rayleigh(5.5×10⁻³) (rms 0.00778 = σ√2). Fresh seeds 44/45: −1.8%/−0.5%.
6. **Table arithmetic** recomputed independently from the rate: 0.0798 rebinds/s, 10.22 bits/s, total 21.1, 76.4 orbits = 398 game-years — all match; the one-code-path claim is real (dossier, JSON and log agree digit for digit).

## Predictions

All six pre-registered groups held: truth ∈ [1.0, 1.6]×10⁻² (1.310), dt drift < 5% (0.7%/0.3%), seed 43 ± 10% (+2.2%), sign-fixed Newton within 15% (0.91×) and strictly above as-shipped (2380 > 1197), windows ± 10% (±0.5%), table as predicted. The genuinely new measurements (dt ≤ 0.15, second seed, analytic anchor) are the ones that held with real content; the truth bracket and Newton bounds necessarily enclosed the first checker's known values — the pre-registration says so honestly, and the [1.0, 1.6] bracket is wide enough to have fired.

## Novelty and the page

No H-entry in docs/HISTORY.md measures H_live (grep: none); the wiki index holds memory-h-live at 0 runs — this is the topic's first page, and the physics decomposition is properly credited to the silver (20261012-1524-fermi-4b55). Every number I checked on the page matches the JSON (Γ, dt/seed/window deltas, 0.91×/1.7×, 10.2/0.9/21.1, 76.4/398, 15.75 MB, 3.75 GB, 4.25×10¹⁸ kg). Two overstatements corrected in place (additions, no rewording): the cross-checks' cold-belt-only domain, and the 128 bits/rebind + ~10 bits/s player terms being stated assumptions.

## Goal fit

Board bottleneck `memory-h-live` ("what representation stands at the floor"; HANDOFF: H_live "not measured yet"). This supplies the first measured anchor and shows the silver's premise wrong by 460×, flipping "player nil" to co-dominant — a premise correction, adoptable in one step (`b-h-live` inherits three decisions; nothing to build). PRINCIPLES #24 "the memory floor is information" — now 21 bits/s of live distinctions, ~9 orders under the singleton store; #10 "Measure before claiming" — the silver's lesson closed: every headline number has exactly one generating path, and it regenerates.

## Why gold

Reproduced bit-for-bit; the pre-registered predictions held, including the genuinely held-out ones; the correction moves the topic's headline by 460× and its record is now regenerable end-to-end — the exact experiment the first checker named as "the one experiment for gold", done with controls the first checker did not run (dt convergence below 0.3, second seed, analytic anchor, code-generated table). My attacks confirm the number and its robustness (σ_e-insensitivity strengthens the 10⁹ extrapolation). Gold stands on the measured record, not on the cross-instruments, whose regime limits are now flagged on the page.

## What the author missed

- The cross-instruments' domain: the 0.91× Newton and 1.7× anchor are cold-belt-only; at σ_e = 0.05 they score 0.34× and 4.0×. The dossier's "what would make it wrong" lists σ_e for the contact term but not for the cross-checks that vouch for the truth.
- The truth's insensitivity to σ_e (×1.3 for ×10) is itself a result the dossier leaves unstated — it is the strongest single argument that the 10⁹ table survives belt-weather unknowns.
- μ-dependence (∝ R_SOI^~1.5) unmeasured: the secondary census needed for k× scaling also needs this power law.
- 128 bits/rebind and ~10 bits/s player are assumptions carried at full weight into a headline that calls them "co-dominant"; a one-line sensitivity (they bound H_live between ~11 and ~100 bits/s) would have made the claim self-grading.
