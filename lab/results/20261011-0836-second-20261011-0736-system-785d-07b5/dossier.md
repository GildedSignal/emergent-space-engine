# Dossier — run 20261011-0836-second-...-07b5 (second author on 20261011-0736-system-785d)

## Claim

The checker's two named gaps are closed: (1) the record now regenerates — `final.py`
recomputes every `final.json` number from the shipped artifacts (13 of 14 exactly;
the j2 W entry was an authoring slip, corrected 0.0229 → 0.0305, so the 3:2 width
overprediction is 2.7×, not ~2×); (2) the named gold experiment ran in its cheapest
decisive form — the certificate as the **only** resonance gate (classifier and B17's
W table deleted), wired into a stand-in of the plane's cheap path built from the
run's own scripts (the crates are off-limits in the lab) — and the outcome is
**one-sided: on r4 v3's cases (2:1, 3:2) the guard form (switch at excursion ≥ q_e/2)
has zero behaviour misses in 6,762 truth-failure events while the old W-gate misses
542–1,120, so the deletion is free there; but the certificate is cleanly refuted as
one-per-family at 4:3 (32 misses, 12 even at guard level, worst pump 7× the cap —
the 5:4 resonance sits inside the scan grid), and the switch-at-q_e form under-predicts
at quanta above the saturated excursion cap even at 2:1/3:2 (66 misses, all but one
marginal).** The claim holds as a **declared-domain** gate: j ∈ {1, 2}, quanta ≤ cap,
guard form, with a zero-cost domain test (next resonance outside the zone, from
compiled frequencies).

## Bottleneck

Board focus lines 1–2 (the changeover near a secondary; fewer kicks). The original
run's claim: the gate is one certificate, excursion(δ) = min(2·ṗ_coh/|θ̇(δ)|,
c_H·μ^(1/3)), deleting the resonance classifier and the width table. This run
decides whether the engine can adopt that deletion.

## Evidence (Linux x86, 8 vCPU shared, float64; orders of magnitude only)

**Record regeneration** (each ≤ 70 s): in a clean tree, after making `OUT`
file-relative (the only edit to the shipped scripts — the originals hardcoded
another runner's absolute path, which alone broke regeneration):

- `python3 probe.py selftest / quad / calib` — quad.json and calib.json
  **bit-identical** to the shipped files; selftest passes (μ=0 ringing 4.395e-4,
  no drift).
- `python3 probe.py scan 1 0.001` and `scan 2 0.0003` re-run fresh: **bit-identical**
  to the shipped npys (all arrays).
- `python3 analyze.py` → metrics.json; `python3 final.py` → final.json:
  c_H, cH_spread, all six capped_law entries, P4a (= 0), kappa (5 values),
  regime-boundary ratios (1.20/1.04/0.53) all reproduce exactly under the recovered
  definitions (c_H = median band at δ=0 ÷ μ^(1/3), mean over μ; W = full width
  2·Δ(P1/P2) at the interpolated crossing of 2ṗ/|θ̇| with the cap). Two corrections,
  recorded in `final.json:regen_notes`: the j2 W entry (0.0229) reproduces only with
  the **2:1** conversion factor 1.5·0.5 (gives 0.0228); with the correct 3:2 factor
  1.5·(2/3) it is **0.0305** — the "3:2 overpredicted ~2×" of the original dossier
  is 2.7×; and the boundary ratio 0.53 vs 0.52 is a rounding of 0.5253 (immaterial).
  Held-out-only capped law added: n = 270, 99.26% in [0.3, 3] (the shipped n = 327,
  99.39% includes the calibration case).

**The gate experiment** (`python3 gate.py`, < 1 s; new data: `python3 probe.py
quadj 3 0.0003 0.001`, `scan 3 0.0003`, `scan 3 0.001` — 35 s each, Edrift ≤ 1e-12):
the certificate alone decides the changeover; outside the zone the averaged law
predicts e within [e₀−q_e, e₀+q_e] (no truth used), inside it the system goes to
the exact handler (the reference integrator itself, so every miss is the gate's
fault — the doll's own fidelity is r4 v3's question). c_H re-derived per geometry
from the exact-resonance column alone (median band at δ=0, 8 seeds — the engine's
one-column calibration; the analytic derivation of the cap stays open). Miss =
truth fails at quantum q_e while the gate keeps the system outside.

| case | c_H | cap | truth-fail events | miss cert | miss guard | miss old-W | miss old-W/2 |
|---|---|---|---|---|---|---|---|
| 2:1 μ=3e-4 | 1.106 | 0.074 | 1,149 | 10 | **0** | 190 | 322 |
| 2:1 μ=1e-3 | 1.117 | 0.112 | 1,453 | 30 | **0** | 0 | 125 |
| 2:1 μ=3e-3 | 1.114 | 0.161 | 1,685 | 0 | **0** | 0 | 0 |
| 3:2 μ=3e-4 | 0.927 | 0.062 | 1,088 | 16 | **0** | 201 | 342 |
| 3:2 μ=1e-3 | 0.944 | 0.094 | 1,387 | 10 | **0** | 151 | 331 |
| **4:3 μ=3e-4** | 0.779 | 0.052 | 1,130 | **32** | **12** | 288 | 446 |
| 4:3 μ=1e-3 | 18.76 | 1.876 | 1,570 | 0 | 0 | 210 | 420 |

- **The deletion is free on the declared domain**: guard-form misses are **zero**
  across 6,762 failure events on 2:1/3:2; the old gate (zone |Δ(P₁/P₂)| ≤ W,
  W = 2.5·μ^(2/3)) misses 542 (or 1,120 at W/2) — it ignores the quantum, so it
  misses 14–32 systems per small quantum. At each case's design quantum
  (calib q_e) both gates' doll fractions are comparable (cert 0.87–1.00 vs
  old-W 0.73–1.00); the certificate's zone tracks the quantum, the W zone does
  not move.
- **Where the switch-at-q_e form fails**: all its 66 misses on 2:1/3:2 sit at
  quanta **above the cap** (the zone collapses to zero when q_e > cap, exactly
  where the saturated excursion says "safe everywhere"); all but one are marginal
  (severity ≈ 0, e barely crossed the tube), the one real case is 3:2 μ=1e-3 at
  q_e = 0.117 (truth band 0.32 at δ = +0.032, the grid edge). The guard margin
  (q_e/2) absorbs all of them.
- **4:3 refutes one-per-family**: the 5:4 resonance lies at δ ≈ +0.027, inside the
  ±0.032 grid; its pumping (worst band 0.358, 7× the cap 0.052) is invisible to a
  4:3 quadrature, so the certificate keeps those systems outside — 32 misses,
  **12 even at guard level**. At 4:3 μ=1e-3 (overlap) c_H = 18.8, the cap
  swallows every quantum: zero misses but doll-fraction 1.00 — fails safe with
  zero cadence information, the same degeneration the checker found at 3:2 μ=3e-3.
- **The domain test is free**: the next family (j+2)/(j+1) crosses at Δ(P₁/P₂) =
  1/((j+1)(j+2)) → δ = 0.222 / 0.083 / **0.027** for j = 1/2/3; the certificate's
  domain is "next resonance outside the zone" — true for 2:1 and 3:2 (the 3:2
  margin is one grid at best), false for 4:3 on this grid. All from compiled
  frequencies, zero added work.
- **Controls hold exactly**: μ = 0 gives ṗ_coh = 0 → excursion ≡ 0 → no switch
  anywhere (including exact resonance); the far controls (pr 2.15/1.9) stay
  outside (excursion 2.7e-3–2.9e-2 vs calib quanta 0.021–0.109). c_H at 4:3
  reproduces the checker's adversarial values (0.779 vs 0.78; 18.76 vs 18.8),
  and the exact-resonance bands match its quadrature re-run.

## Predictions

`predictions.md` was written before the 4:3 scans and the gate runs. Outcome:
**PA failed as written** (I predicted zero switch-level misses at 2:1; there are
40, all at q > cap, all marginal) — its guard half held (zero guard misses, as
predicted). **PB confirmed** (4:3 μ=3e-4 misses at the large-q end via the 5:4
resonance — and stronger than predicted: the guard breaks too). **PC confirmed**
(4:3 μ=1e-3 fails safe, degenerate). **PD partially held** (comparable doll
fractions at design quanta; the quantum-aware shrinking becomes the failure mode
above cap). **PE confirmed exactly.**

## What would make it wrong

- The exact handler is the reference integrator itself, so pump ratio and regime
  inside the zone are 1.0 by construction; the experiment measures the gate, not
  the doll. Wiring into the real plane's kick layer (the checker's full ask) could
  still surface cost or arithmetic the stand-in hides — the crates must do that
  run.
- c_H is calibrated per geometry from the exact-resonance column (one column, 8
  seeds), not derived from the quadrature; the analytic Hill-scale derivation
  remains open. Eccentric/inclined perturbers untested.
- The miss instrument is the running-mean tube; θ-regime (libration) of ~10–15
  librating systems per case is not covered at large quanta (kept outside while
  librating, e still inside the tube) — B17's "regime matches" needs the doll
  there, or the regime criterion needs the zone, not just the tube.
- Float probe; the integer law must re-derive c_H on its own grid (lab rules).

## Cost of adoption

Small and now bounded: adopt the certificate as the only gate **with the guard
form and the declared domain** (j ∈ {1,2} below overlap, next resonance outside
the zone — a compiled-frequency check), cap calibrated per geometry at exact
resonance. Deletes the classifier and the W table on that domain; 4:3-and-closer
geometries keep a width-style gate or go straight to the doll (the degenerate
fail-safe already does this). The corrected W derivation (0.0305 vs B17's 0.0112
at 3:2) says the convention is not the certificate at 3:2 — the crossing is a
2:1 result that degrades with j.

## Fit with PRINCIPLES

- "Regimes are chosen by dimensionless numbers" (4): the gate is a number against
  a quantum, no class — now with an explicit, computable domain.
- "The cheapest compute is compute not done. Delete before optimizing" (1): the
  classifier + width table are deleted on the declared domain, and the deletion
  is measured to be free (0 vs 542 misses).
- "A failed experiment kills that configuration, never the method" (9): 4:3 kills
  the one-per-family configuration; the certificate survives domain-bounded.
- "Oracles are guards, not shepherds" (34): the guard form (q_e/2) is the guard;
  the switch-at-q_e form is a shepherd and under-predicts above cap.

## The lens

A second author inherits the checker's framing, and this frame — "wire it and see
if behaviours survive" — is the right one; what it hid from me: I nearly repeated
the author's over-claim in PA (predicting zero misses from the F-statistics
without asking what happens above the cap — the cap's own collapse is the blind
spot of a headline built on the [0.3, 3] window). The most valuable number here
cost 70 seconds: the 5:4 resonance at δ = +0.027, knowable from two compiled
frequencies before any integration is run.
