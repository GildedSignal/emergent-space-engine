# Dossier — 20261007-1420-redteam-9fbd (premise red-team)

## Claim

The frozen gates never sample the strong field (every light and bound seed starts at p, b = 10), and there the design's m=16 Binet budget fails its own 1% standard for the one orbit class that cannot average across bands — near-circular massive orbits: apsidal precession error **+9.6% at r = 7M and −6.1% at r = 8M** (first order in 1/m; +3.6%/−3.2% at m32) — while everything else I attacked *survives*: strong-field light deflection stays within 0.1% down to b = 1.05·b_crit and −0.9% at 1.003·b_crit (deflection 5.4 rad, nearly two full loops), and capture/plunge classification is exact in every case, including two separatrix-skimming orbits.

## Bottleneck

Not a compute bottleneck: a **certification** one. r1's `prec` criterion (≥ 99% of seeds within 1% of GR precession) passed at m16 on a sampler that draws p ∈ [10, 1000] log-uniform and e ∈ [0, 0.7] uniform — the joint probability of (p < 10, e < 0.05) in that sampler is ≈ 0.2%, so the gate tolerates 1% failures while **every** close-in near-circular orbit is wrong by 6–10%. PRINCIPLES 30: "what really matters is navigation, knowledge and dynamics those need be perfect". A ship parked on a circular orbit at 7–8M (stable, well outside the ISCO at 6M — core black-hole gameplay) sees its rosette march (10.3 rad/orbit at r = 7) wrong by ~10%: petals visibly misaligned within a dozen orbits, and any navigation compiled from the law inherits the error. Gain: correctness at ~zero compute; the fix is a seed-range fix in r1/B19 plus a per-doll m (or a dwell-weighted u_k) in the strong field — the strong-field disc 6–10M is a tiny area, so finer rings there cost almost nothing.

## Evidence

`docs/representation.md` §1 (Binet cells) and §2 ("Light is the same equation without the M/L² term"; lensing "from each doll's memoized deflection(b)"). r1's frozen rule (lab/rungs/r1-rings.md): bands r_k = 2^(k/m), u_k at the geometric centre, u and u′ continuous across joints, per-band u″ + (1 − 6u_k)u = 1/L² − 3u_k² (massive) / −3u_k² (light). Same rule in law gate B3 ("deflection within 1% over 64 seeds", b ∈ [10, 1000]). I integrate that exact rule in float64 (RK4, dφ = 1.5e-4 light / 3e-4 massive; step-doubling control 2×10⁻¹⁰ rad) against the exact Schwarzschild Binet equations.

**Light** (b_crit = 3√3 M ≈ 5.196; every secondary image and the photon ring lives below b = 10 = 1.92 b_crit — no gate samples there):

| b/b_crit | α exact (rad) | err m16 | err m32 | err m64 |
|---|---|---|---|---|
| 1.9245 (=10, r1's floor) | 0.5904 | −0.02% | −0.01% | −0.00% |
| 1.5 | 0.9021 | −0.03% | −0.01% | −0.01% |
| 1.2 | 1.5192 | −0.06% | −0.01% | −0.00% |
| 1.05 | 2.6955 | −0.10% | −0.03% | −0.01% |
| 1.01 | 4.2295 | −0.33% | −0.09% | −0.03% |
| 1.003 | 5.4168 | −0.88% | −0.25% | −0.08% |
| 0.97, 0.90 | captured | captured | captured | captured |

Integrator validated against the asymptotic series where it converges: b = 100 → 0.041223 vs 0.041221; b = 30 → 0.148248 vs 0.148004 (difference = the finite-launch tail). The cross-band cancellation that let m16 pass r1 extends all the way to the photon ring. **This premise survives my strongest attack.**

**Massive near-circular** (radial period Δφ; precession = Δφ − 2π; r1's sampler never draws p < 10):

| case | Δφ exact | err m16 | err m32 | err m64 |
|---|---|---|---|---|
| r = 7M, e = 0 (precession 10.34 rad/orbit) | 16.6237 (=analytic 2π/√(1−6/7)) | **+9.60%** | +3.64% | +0.90% |
| r = 8M, e = 0 | 12.5664 (=4π) | **−6.13%** | −3.16% | −1.60% |
| p = 20, e = 0.5 (inside r1's sampler) | 7.9142 | −0.04% | −0.01% | −0.00% |
| p = 8, e = 0.3 and p = 12, e = 0.5 | genuine plunges (L² = 8 has no turning point; L² = 12 is exactly the separatrix, E² = 0.8906 > barrier 8/9) — all four models agree, 4/4 | | | |

Mechanism (measured, not assumed): a near-circular strong-field orbit sits inside **one** band and inherits that band's frozen frequency ω_k = √(1 − 6u_k); the relative precession error is the orbit's offset from its band centre amplified by dlnΔφ/dlnu = 3/(p − 6) — which is 0.5 at p = 12 (invisible), 3.0 at p = 7 (10% from a 2–3% band offset). The m16 value at r = 7M equals the closed-form single-band prediction 2π/√(1 − 6·2^(−2.84375)) = 17.6167 exactly. Eccentric orbits and photons cross many bands and the per-crossing phase errors cancel (that is why r1 and my light table pass); near-circular orbits cannot. The repo's own record corroborates: the viewer found "near-circular precession 1–7% off" (H0209-era); my strong-field cases give 6–10%.

Reproduce: `cd lab/results/20261007-1420-redteam-9fbd && python3 falsifier.py` — 27 s, one process, < 100 MB, numpy 1.26, deterministic; full numbers in `metrics.json`. Machine state: shared Linux x86_64 runner, load 0.56 (see `metrics.json`).

## Predictions

`predictions.md` was written before the run. P1 held (r1's edge passes). **P2 and P3 failed badly** — I predicted 3–20% light-deflection error at b/b_crit = 1.2–1.05; actual is −0.06%/−0.10%: the premise survives where I attacked hardest, and I report that with the same weight as the wound. P4 held (zero capture misclassification, including two separatrix cases the gates never test). P5 held (p = 7 error > 2%; actual +9.6%). P6 held (error ×0.26–0.52 per doubling of m — first order in band width, confirming the mechanism). Held out for the checker: b/b_crit ∈ {1.5, 1.1, 1.02, 1.01}, m = 64 everywhere, (p = 8, e = 0.3).

## What would make it wrong

If the shipped `es-space-v2` compiler does not freeze u_k at band centres (e.g. it integrates the true per-band ODE at higher effective resolution or uses a dwell-weighted u_k), the m16 numbers do not describe the live law — but r1's frozen rule is the design's stated mechanism and the measured mechanism (single-band frozen ω_k) is verified against closed form. If players never hold near-circular orbits at r < 10M, the wound is invisible — implausible for a game whose goal headlines black holes and GR-native navigation. Adoption cost: add a strong-field near-circular stratum to r1's `prec` (p ∈ [6.5, 10], e ∈ [0, 0.05], tolerance unchanged at 1%) and check B19's apsidal seed range (its frozen text does not state p bounds; prograde χ = 0.998 orbits down to r → M make dω²/du arbitrarily large — likely worse than Schwarzschild); then either per-doll m in the strong field (the 6–10M disc is a tiny area) or a corrected ω_k. Gates may be strengthened, never weakened.

## Fit with PRINCIPLES

- "what really matters is navigation, knowledge and dynamics those need to be perfect" (30) — a 10% precession error on close circular orbits is a navigation error the player can see.
- "Gates are frozen before the first run and never weakened after. Failures stay machine-readable. Gates judge a representation" (AGENTS) — the sampler range, not the tolerance, is the defect; the fix strengthens the gate.
- "A failed expectation is not automatically a failed method: diagnose which one broke" (H0183 / PRINCIPLES 9) — m16-strong-field is the configuration that dies; the band method survives everywhere it can average.
- "Measure before claiming, and never strawman" — my strongest prediction failed and the premise there survives; reported as such.

## Ranked attacks (the lens deliverable)

1. **[RUN, this dossier] Strong-field near-circular precession below every sampler floor** — +9.6%/−6.1% at m16, r = 7/8M. Rung that should catch it: **r1 `prec` — none does** (sampler excludes p < 10 and has no near-circular stratum; B19's apsidal seeds unstated). Player-visible: wrong rosette on close black-hole orbits; navigation.
2. **Two-body doll unjudgeable exactly where it matters.** r3 v2's precession exclusion "left 0 seeds (the 1PN oracle's next term is about 8·M/p)" (H0206): the ν-only-in-the-energy-map premise is verified only where 1PN ≈ truth (p ≳ 40) and unmeasured for comparable-mass close binaries, the interesting ones. **No rung catches it**; needs a 2PN quasi-Keplerian truth (Damour–Schäfer). Not run here: out of 60-minute reach; a rung, not a float probe, is the right instrument.
3. **"Costs of about zero for undisturbed bodies" is already contradicted by the plane's own record:** the plane recompiles an orbit on ~99% of kicks and 92% of per-kick evals are window setup (taste log, 5–6 October; the memo artifact). Cited, not rerun — re-measuring it would double-count one harness. The slack skin (12.6×) is the live lever.
4. **Dense ≡ sparse bit-identity** was measured once (a battle free-fall frame, bit-identical, re-anchoring 0.44% over 10 periods) but **r5 is absent from lab/rungs/** — the premise rests on one demonstration plus components that share a harness (the 5 October lesson). A rung should exist; no new evidence here.
5. **The view's gather (premise 5) survives and is strengthened**: deflection(b) memoized per doll is accurate to 0.1% at 2.7 rad and −0.9% at 5.4 rad (this run), so predicted lensing crossings are sound even at the photon ring; multiplicity at caustics (images popping in pairs) remains unmeasured and **r6 is absent from lab/rungs/**.
6. **The river/tilt negatives and premise 1's tested domain** — river refraction is already killed (H0205), and the EOB 1PN map passed r3 v3 where judgeable; both stand as recorded.

## The lens

A red-team overweighted exotic cases would have shipped only the photon-ring attack — which *failed*: the design is stronger there than its documentation argues. The wound appeared where I did not aim first (near-circular massive orbits at moderate r, i.e. ordinary gameplay), and only because the amplification 3/(p−6) is large exactly where the samplers stop. What this lens may still miss: Kerr (B19's χ = 0.998 prograde ISCO at r → M makes dω²/du unbounded — the Schwarzschild 10% is likely a lower bound), and the interaction of the band error with kicks (a 10%-wrong base cycle also corrupts the stored ∂/∂E, ∂/∂L that kicks ride).
