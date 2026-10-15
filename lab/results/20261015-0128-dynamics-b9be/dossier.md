# Dossier — 20261015-0128-dynamics-b9be

## Claim

On the shipped law, in the co-orbital scene, at the engine's Q and 512 P: **trapping statistics are preserved (capped captures 54/144 plane vs 54/144 float oracle, dwell quantiles equal within the oracle's own tolerance pair, and unchanged at 32× coarser kick cadence) — but survival is not: the plane loses 48/144 ships at conjunction epochs where the oracle's closest approach never drops below 28 Rp (sampled), a false-death behaviour class the shadowing discussion missed.**

## Bottleneck

Not a board bottleneck: this is the chaos-shadowing page's open direction 1 (its only untested arm). Gain: closes the "repeat the dwell arm on the shipped law" question with a measured answer, and hands the integrator a new separating statistic (conjunction survival) plus a rung-instrument warning (dwell cannot separate even a 32× coarser law).

## Evidence

Scene: `xtask`'s `restricted::JUPITER` CRTBP (μ = 1e-3, sep 5.27e8 M), the B12–B14 judge's own. Ensemble: 144 ICs = 12 synodic angles × du ∈ {±0.35…±1.45}·w, w = √(8μ/3) (tadpole half width). Instrument: in-band ⇔ |a/sep−1| ≤ w on osculating heliocentric a, sampled P/8; dwell = maximal continuous in-band run; classes = captured (censored at 512 P) / escaped / dead. Probe: `xtask/src/behave/trojan.rs` (in `work/patch.diff`), driven through `Plane::restricted` (shipped plane, default step_log2 = 7) and `restricted::reference` (float64 DP54).

| arm | captured | escaped | dead | max-dwell p50 (P) | ep p90 (P) |
|---|---|---|---|---|---|
| float 1e-12 | 54/144 | 90 | 0 | 5.4 | 13.0 |
| float 1e-10 | 54/144 | 90 | 0 | 5.4 | 12.6 |
| plane step 7 (shipped) | **54/144** | 42 | **48** | 13.2 | 13.6 |
| plane step 2 (32× coarser) | 50/144 | 62 | 32 | 8.2 | 12.6 |

- Oracle closest approach: min 28.2 Rp, p10 92.5 Rp over all 144 ships (P/8 sampling; sampling underestimates true periapsis closeness — see Wrong below).
- Death attribution (`PLANE_TRACE=1`, 16 P run): every traced loss prints `handoffs=0 refused=0 lost=1` at conjunction epochs (synodic ≈ 13 P; losses at samples ≈ 87, 97 of 129). Not a doll-edge handoff, not a kick refusal: the universe's `lost` counter. Two ships are lost at t ≈ 0 (build refusal).
- Reproduce: `regen.sh` (~6 min: 3.9 s + 1.6 s + 310 s + 10 s + aggregate); attribution: `PLANE_TRACE=1 TROJAN_OUT=/tmp/tr.jsonl TROJAN_ARM=plane TROJAN_STEP=7 TROJAN_PERIODS=16 TROJAN_WORKERS=8 cargo test --release -p xtask trojan_probe -- --ignored --nocapture` (~8 s).
- Machine: Linux x86, 8 vCPU shared, 8 workers, peak RSS ≪ 2 GB. Wall: plane step 7 = 310.6 s for 144 ships (≈ 2.2 s/ship single-thread-equivalent at 512 P — the plane's own cost, orders of magnitude only).

## Predictions (predictions.md, written before the 512 P runs)

- **P1 (instrument, float 1e-10 vs 1e-12): PASS** — identical classes (54/90/0), quantiles equal. The statistic is tolerance-robust: chaos decorrelates trajectories (2951 vs 3111 episodes) but not the class counts.
- **P2 (the page's question, plane vs float): PASS as pre-registered** (capped within 2×, p90 within 1.5×). The toy's rounding distortion does not appear at engine Q here. My stated mechanism held: error-feedback carries + bounded handoffs are noise-like, not the toy's per-event state rounding.
- **P3 (negative control, step 2 must separate): FAIL — even 32× coarser cadence preserves dwell statistics** (50 vs 54 captured, p90 equal). As pre-registered: the dwell statistic cannot separate laws in this scene; as a rung instrument it is a control, not a gate. What DOES separate is deaths (32 vs 48 vs 0).
- **P4 (plane kills ships the point-mass oracle keeps): PASS**, 48 vs 0, concentrated at |du| ≥ 0.85 (the chaotic layer), none at 28 Rp sampled distance in the oracle.
- **P5 (differences live in the tail, not the median): FAIL** — the difference is not in the dwell tail at all; it is a class difference (dead vs escaped). Honest miss: I looked for the toy's signature and the law's error showed elsewhere.

## What would make it wrong

- The oracle's closest approach is sampled at P/8; a true periapsis under 1 Rp between samples would make some plane deaths real surface hits the oracle cannot see. The 28 Rp minimum over the whole ensemble makes this unlikely for most of the 48 but does not exclude it; the deciding experiment is an `until_crossing`-style periapsis-resolved oracle pass over the 48 dead ships (B12's own `watch` machinery, one short run).
- Deaths are localized only to ±6% of horizon (descending-prefix probes); epoch clustering at conjunctions is read from the 16 P trace, not from the 512 P run.
- One ensemble, one μ, one horizon; the toy's distortion was strongest near critical K. μ = 1e-3's layer may be too thin; μ = 1e-2 (a super-Jupiter) would stress it harder.
- If `Universe::lost` turns out to include a benign category (e.g. bodies parked, not destroyed), the "false death" reading softens; the trace API counts them together.

## Cost of adoption, PRINCIPLES fit

Nothing to adopt in the engine: no representation change measured. The page's consequence runs the other way: the shadowing clause needs no certificate for trapping statistics on the shipped law in this regime, but the co-orbital layer needs a survival certificate (a false-death gate in B12's family: "no ship lost that the oracle keeps outside the surface"). Fits principle 2 ("error type over error size": the error is a wrong behaviour class, not a magnitude) and principle 3 (the deaths are surprises the engine computes and the truth never has — work with no reason). Cost: the periapsis-resolved oracle pass (~1 run) before any gate freeze.

## The lens

The dynamics lens went hunting for the toy's sticky-tail distortion and found class-space instead: the attractor here is a sink (lost), not a trap. What I may have missed by framing everything as dwell statistics: the escape-time distribution of the *surviving* layer (I only reported quantiles), and return maps of the synodic angle that could show whether the plane's captures sit on the same tori as the oracle's or on shifted ones.
