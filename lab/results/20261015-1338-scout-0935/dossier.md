# Dossier — gravity is news at strong field: the payload is complete, the cheap readout is not

## Claim (one sentence)

**At strong field (r = 12–200 M, β ≤ 0.5, sustained and curving burns) the (x,v,a) version
payload is complete — the exact GR field of a thrusting source (Kinnersley, via Carlip's
retarded Kerr–Schild form) is computable from the source's retarded position, velocity and
acceleration alone to 1.3e-10–5.7e-9 — while the cheap non-radiative readout (Carlip's b3)
is not: it must add the nonlinear −2m/R term (2m/r of error: 17% at 12 M) and the
acceleration-dependent terms (a burn channel ≈ (1–4)·a·r, percent-level at 20 M for
engine-class burns), so the strong-field doll's readout is the full retarded-field
evaluation, which is itself a closed ~tens-of-flops function of the same payload.**

## Bottleneck

Gravity-news open direction 4 (the page's named unmeasured question): the payload decision
((x,v,a)) rests on Carlip's weak-field expansion and d947's scalar toy; the strong-field
consumer (r = 20 M "where the O(v²) extrapolation corrections and the direct tide grow")
was unmeasured, and it gates law.md's causality primitive (line 33, "gravity is news") in
the black-hole regime the engine is built toward (PRINCIPLES #30: "we need to build
towards GR that's the goal"). Expected gain: not a 10× on a cost axis but a wrong-premise
kill or a certification of the one representation the whole news design rides on; it also
deletes the need for any jerk slot or strong-field payload extension — the ring carries
(x, v, a) at every field strength.

## Evidence

All numbers from `work/` (float Linux, seconds of compute; exact-GR oracle). Reproduce:
`bash regen.sh` (~2 min).

**The instrument (controls both sides, all green before any scene ran):**
- The oracle metric is Carlip's eq. b1 (Kinnersley's photon rocket, exact GR, arbitrary
  source acceleration, constant mass): g = η − 2m σσ/r³, σ null from the retarded solve.
  For uniform source motion it must equal a Lorentz-boosted static Schwarzschild–KS:
  measured max relative difference **2.0e-16** at β ∈ {0.01, 0.1, 0.3} (this control
  caught two real transcription bugs in my own b1a: a lowered-index error and r = λ·σ
  computed contravariantly — the instrument that produced every earlier number was
  rebuilt until this passed).
- Γ two independent ways: central differences of the metric vs Carlip's published
  connection (eq. b1a): **≤ 2.0e-10** through β = 0.3 under burn. Static limit:
  pull = m/R²(1 − 2m/R), hand-derived, matched to 2.9e-11.
- The consumer locus is an exact geodesic (RK4 on the t-parameter geodesic, Γ by FD);
  the scar compares each readout arm's implied acceleration at sampled events against
  −Γⁱ₀₀ (a momentarily static probe — the consumer's own kinematics belongs to the doll,
  not the news channel). Arms use **retarded data only**.

**Free fall (the aberration cancellation survives at strong field, unchanged):**
- ρ(R2b — quadratic extrapolation + b3 velocity prefactor + nonlinear term) =
  **(0.8–1.9)·β_s², flat in r from 200 M to 12 M** (2m/r from 0.01 to 0.167). Carlip's ε
  corrections are velocity-only: field strength drops out entirely. News ≡ inst for free
  fall holds at 12 M as exactly as at 200 M.
- ρ(R2 — the plain quadratic extrapolation) at small β = **2m/R exactly** (1.01e-2 at
  200 M, 4.18e-2 at 50 M, 1.11e-1 at 20 M, 2.01e-1 at 12 M): the missing nonlinear term,
  not the extrapolation, is the strong-field correction that binds.
- ρ_perp(R1 — naive retarded, the Laplace control) = **(0.6–1.0)·β_s at every radius**
  (P1 held; the negative control behaves).

**Burn (the thrust channel at strong field):**
- ρ(R0) − ρ(R2) ≈ **½·a·r** (gentle arm, 0.10 v_c per 0.25 P, at r₀ = 20 M: measured
  2.1e-3 vs predicted 2.3e-3): the thrust-blind tube's ½aT² lag at T = light time, with
  **no strong-field amplification** — 7ab4's weak-field law composes (P3 held).
- The b3 readout's own burn channel (β → 0): grows ~linearly in a, ≈ **(1–4)·a·r**
  (r = 50 M: 7.4e-4 → 1.08e-2 for a × 4; r = 12 M: 2.3e-3 → 1.2e-1). This is the
  acceleration-dependent ("radiative") part of the exact field that b3's display omits.
  Percent-level at 20 M for engine-class burns — the same order as 7ab4's measured
  rebind scar at r = 20 M (1.4e-2), reached here by an independent channel.
- Jerk: with the a-slot's staleness over one light window ≲ O(1) (a doubling per 40 time
  units at r = 20 M), the row sits at the constant-burn level (ρ(R2b) 2.9e-2); an
  extreme program (a growing ×21 per light window) costs ~4× over the β² floor. No new
  payload data is needed in either case (see RX below).

**The decisive arm (RX):** the exact Kinnersley field evaluated **from the retarded
broadcast (x, v, a) alone** (the analytic b1a at Γⁱ₀₀ — a closed function of retarded
position, velocity, acceleration and m; no integration, no history): residual vs the FD
oracle **1.3e-10 – 5.7e-9** across β ∈ {0.1, 0.3, 0.5}, r ∈ {12, 20, 50, 200} M, burns
from gentle to 4× gentle. **The payload is complete at strong field: nothing beyond
(x, v, a) ever enters the exact field.**

**Held-out (pre-registered in predictions.md, run after):** β = 0.2, r = 16 M free fall:
ρ(R2b) = 6.79e-2 vs the law's 5.6e-2 (1.2×, within the measured prefactor spread); the
same scene under gentle burn: 6.28e-2 — the burn adds nothing at fixed β; hard burn at
r = 30 M: R0−R2 = 6.3e-3 (order ½ar, 2.5×); retro burn and the sane jerk row: at the
constant-burn level. One scene (the first jerk row) was invalid as parameterized (my
window cap ignored the jerk's growth; the source went superluminal) — reported as a
build bug, fixed, rerun; its stress limit is reported above.

## Predictions

predictions.md was written before the decisive sweep. Outcome: **P1 held** (Laplace
control ≈ β_s at every radius), **P2 held with a refinement** (R2b sits 100–800× under R2
at β ≤ 0.03, but at β ≥ 0.1 both are β²-dominated and the gap closes — the refinement:
the missing 2m/R term, not ε, is what separates R2 from R2b at small β), **P3 held**
(½a·r, coefficient within 1–2.5×), **P4 split**: the kill criterion (ρ(R2b) > 1e-2 at
β_s = 0.1, r₀ ≥ 12, gentle burn) **fired** — gentle r₀ = 12 M measured 4.4e-2 — so the
cheap (x,v,a)+b3 readout is *not* complete at strong field; but the payload itself is
complete (RX at 1e-10). The verdict is a readout requirement, not a payload change.

## What would make it wrong, adoption cost, fit

- **Wrong if:** the FD-of-metric and the analytic b1a shared a bug (both consume my
  retarded solve and worldline — but the boost control pins the metric to machine
  precision against a construction that never touches the retarded solver's downstream);
  or if Kinnersley's null-dust source does not model the engine's thrusting aggregates
  (it is the exact solution for an arbitrarily accelerating point mass; the engine's
  "ships' aggregate mass can become a source" is exactly this family — PRINCIPLES #6).
- **Adoption cost:** small and local. law.md line 33's primitive gains one clause: the
  strong-field readout evaluates the full retarded field from the version payload (a
  closed expression — my `gamma_analytic` is a reference, ~40 flops at Γⁱ₀₀), with the
  −2m/R term mandatory below ~50 M and the acceleration-dependent terms material at
  r ≲ 20 M for engine-class burns. No payload change, no cadence change, no new slot.
- **Fit (PRINCIPLES):** #23 "Nothing past c" — every arm consumes retarded data only;
  #30 "we need to build towards GR that's the goal that we should not loose track of" —
  the black-hole consumer is now certified at the representation level; #2 "Exact physics
  is the oracle, not the implementation" — here oracle and implementation coincide for
  tens of flops, so the cheap exact form *is* the engine candidate; #3 "Compute only
  surprises" — the field is a function of the delivered version, never evolved.

## The lens

The scout trusts the literature, and the literature's display (Carlip's b2/b3) omits the
radiative terms — I nearly mistook my R2b arm's burn channel for a payload deficiency
until the RX arm separated payload from readout formula. Not tested: 3-D inclination and
burn directions out of plane (the engine is 2D — fine), a *moving* strong-field consumer
(the doll's own kinematics was deliberately excluded from the scar; the moving-probe
terms are the handoff page's business, not the news channel), back-reaction of the
consumer (test particle), the source's mass program (ṁ ≠ 0, the rocket's mass loss — the
b1a dm/ds term is implemented but never exercised), and the plane's doll units, where
v_k/c is ~100× the SI anchor: the r-scales (12–200 M) re-derive at wiring. The Shapiro
channel (physical vs flat light cone inside the KS construction) is carried entirely by
the exact arm and invisible to the b3-family arms — a decomposition worth one run if the
strong-field doll ever needs the cone itself, not just the field.

## Commands (each ≤ 60 s except the sweep, ~35 s)

```
cd lab/results/20261015-1338-scout-0935/work
python3 news_strong.py              # instrument self-test (static limit, FD vs b1a)
python3 sweep.py                    # decisive grid: free-fell 4x4 + burns 3x2  (~35 s)
python3 sweep.py heldout            # the pre-registered held-out rows
python3 extra.py                    # beta scan, burn/jerk scaling, RX completeness
```

Raw outputs: `sweep.json`, `sweep_heldout.json`, `scaling.json`, `beta_scan.json` (in `scaling.json`).
