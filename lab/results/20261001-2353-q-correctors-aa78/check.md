Grade: silver

Abstract: Claim: correctors and higher-order splits do not cut the plane's kicks per orbit at the behaviour bar — every kernel floors at 8 (16 at e₀=0.3), so the 16× sits in `step_log2`, not the kernel. Reproduced: `validate.py` (schemes implemented right, τ²/τ⁴ as claimed; equal-kicks saba2 gain 58× here vs the claimed 280×), the S1 moon table digit-for-digit against its stored ref, s4/dyadic JSONs consistent. My adversarial runs strengthen it: μ=3e-3 resonance holds at 8 ko (+1.3% pump); e₀=0.3 floors dkd at 16 ko with every corrector worse. One load-bearing mechanism is wrong (see below). Gain: a 16× (8× at e=0.3) kick-cut candidate, float replica only; adoption is `behave` B14/B17 at step_log2 3–4 on the integer law.

## Reproduction

- `python3 validate.py` (31 s): matches. dkd τ²-then-floor (1.4e-7 → 1.9e-9), saba2/3 τ⁴, whc3 = 2.17e-10 at 160 kicks/orbit vs the dossier's 2.2e-10. Floor-level constants differ up to ~5× (e.g. saba2@32ko: 1.5e-10 vs 3.1e-11) — roundoff-floor chaos across libm builds; the "280× at equal kicks" is 58× here. Same order, same conclusion.
- S1 moons (e₀=0.05), rerun against the author's own saved ref (`dyadic.json:ref_dkd_k10`, rates 3.849e-3/8.406e-2, 0.6/0.8-Hill moons escape everywhere — regime match 100%): every row reproduces to the digit — dkd k=3 PASS (−2.9%/−1.4%), dkd k=2 FAIL (e +42%), saba2 k=2 PASS (−0.4%/+0.2%), saba3 k=1 FAIL (−14.5% rate), whc3 k=3 PASS but costs 40 ko, whc3 k=2 FAIL (−51% rate, e +56%), whc3b k=3 PASS (8 ko). The 8-ko floor and "the kernel buys nothing" hold.
- s4.json (stored): dkd and whc3 give identical worst dE_A at every k (7.6e-1 … 6.0e-2, exactly results.txt); end-state elements agree to ~3 digits (1.5e-3–1.5e-2 rel under chaos). dyadic.json: saba2-dyadic −0.4%/+0.2%, whc3b-dyadic +0.4%/−0.8% vs ref — as claimed.
- predictions.md predates the sweeps (mtimes: predictions 51 m < sweep1 49 m < … < dyadic 29 m; tuning confined to validate.py at 54 m, as declared).

## Adversarial cases

1. **μ=3e-3, 2:1 resonance** (the dossier's unfinished hardest B17 case; 173 s): ref-converged to 6e-5. dkd at 8 ko: pump-ratio deviation +1.3%, regime match; saba2 at 8 ko +3.9%; whc3 +9.4% at 20 ko. Wrong-maker #2 does not materialize: the 8-ko floor extends to μ=3e-3.
2. **e₀=0.3 moons** (the unfinished held-out S1h; B14 judges e₀ up to 0.3; 177 s): dkd fails at 8 ko (m1 rate −7.5%, emax −28%) and passes at 16; saba2, saba3, whc3 and whc3b all fail at 8–40 ko — whc3 fails even at 40. Prediction S1h (correctors degrade less, hold at 24–40) is falsified in the claim-strengthening direction: no kernel beats plain dkd at high e. The universal moon cut under B14 is therefore 8× (16× at low e), not 16× everywhere — the claim needs this qualifier.
3. **1% precession bar** (the dossier's wrong-maker #1): saba2 passes at 8 ko (−0.4%), dkd needs 16 (−0.6%). One octave, exactly as conceded.
4. **Exact telescoping:** on the stable moon, per-step whc3 vs boundary whc3b (proper `run()` path) agree to **2×10⁻¹²** relative at k=3 — they are the same end-to-end map for any `accel(st,t)`, because `Z`'s sub-kicks are evaluated at a fixed `t` and `Z(a,b)⁻¹ = Z(−a,b)` exactly. At e₀=0.3, whc3b k=3 and whc3 k=3 give the same behaviours to 3 digits while costing 8 vs 40 ko.

## The mechanism error (load-bearing point 5)

The dossier's story — "against a moving source the corrector's sub-kicks sample the primary at displaced times, so the conjugation does not telescope; whc3b gives exactly dkd's numbers" — is wrong for this code. `Z` never advances the time; sub-kicks displace the body's position at fixed `t`, and operator composition telescopes **exactly** (verified in 4). The measured "whc3b = dkd" rows in S3-A are an artifact: `sweep3.runA2` calls `Integrator.step()`, which for "whc3b" applies no corrector at all — I verified it is bitwise identical to dkd. The 5×-at-equal-steps Jacobi gain of per-step whc3 is a readout effect (samples relabelled by C⁻¹), not non-telescoping. The conclusion survives and is stronger than claimed: the corrector is *exactly* a state relabelling, so it can never move element-behaviours at any step size — but a gold dossier cannot carry a misdescribed load-bearing mechanism plus an artifact leg.

## Novelty and fit

No prior H entry measures correctors/SABA/WHFast; the run was the integrator's queued `q-correctors` item (H-entry next-list) against board bottleneck 1 and HANDOFF's "a kick costs 29 µs … the bigger lever is fewer kicks". `Config::step_log2` defaults to 7 (128 kicks per radial period) — the claimed one-line lever exists. Fits PRINCIPLES 2 ("'Exact' means deterministic and reproducible… error type over error size") and 18: the right question was "how few kicks does the behaviour need", not "which kernel is higher-order".

## The one experiment for gold

Run `behave` B14 and B17 (and B12's Jacobi on the two-doll changeover, which this replica does not model) on the integer law at `step_log2` 3–4 vs 7. If the gates hold at ≥8× fewer kicks, the lever is adopted on the engine's dominant cost and this becomes gold; if they fail, the replica's bars missed a gated behaviour and that is also a result.

## What the author missed

- The exact-conjugation algebra of their own code (point 5's mechanism), and that runA2's whc3b is dkd by code path — both checkable in minutes and both change what the S3-A numbers mean.
- The e₀=0.3 and μ=3e-3 sweeps were affordable (150–175 s each on this container) and both sit inside B14/B17's judged ranges; leaving the 16× claim unqualified for e was the gap that mattered.
- Floor-level constants presented as reproducible facts ("280×", "identical to 3 digits" for a −0.44% rate) — they are libm- and chaos-sensitive; orders of magnitude only.
- The step floor may also be set by behaviours not gated here (thrust cadence at `thrust_log2 −44`, the pending E9 tide): the dossier gestures at this but does not name the config fields at stake.
