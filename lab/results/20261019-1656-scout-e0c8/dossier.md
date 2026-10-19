# Dossier — 20261019-1656-scout-e0c8 (scout)

## Claim

In-place absorbability of the shipped cadence's clock-kick by the compact belt row is **dead
as the row is built, and the killer is representational**: on shipmem's own grids one
doll-step tide kick costs ~1,057–1,090 bits/body raw, **~1,020–1,041 of them on the t_p
column alone** (δt_p p50 3.5×10⁹ quanta of the 44-bit clock grid — the kick moves periapsis
by hours on a grid that resolves ~6 ms), while the same physics costs only **~38–49 bits in
element space** (p/e/ω columns) — a **22–28× deletion available by folding the kick into
element/action-angle space (rates: δP is a ~15-bit number) instead of storing its projection
on an absolute periapsis-time grid**.

## Bottleneck

budget-1e9 open 2's successor (the ledger's largest memory-side unknown): 0659 measured
promotion fraction p = 1.0 — every clock-kick item promotes a body to live (~1.3–5.1 KB)
unless the compact row can take the quantized dv without the live round-trip. This run
prices that "in-place update" path: ~1.1×10³ bits/body/kick against the driven-worst 126
bits and the self-stirred 21–40 — so **the ledger's one-promotion-per-kick budget stands on
the current row**; the 10³-scale memory row cannot close through compression of the row as
built, only through changing the kick's landing representation (expected gain once wired:
the t_p term deletes wholesale; the survival cost is the ~38–49-bit element-space departure,
with δP/δn itself a ~15-bit quantity).

## Evidence (all from `python3 absorb.py`, 1.2 s, seed 20261019, N = 4,096)

Float64 first-order replica on shipped constants: belt per shipmem's birth law (`belt.rs`:
p uniform over the [2048,2560) band taken as [2,2.5), e Rayleigh 0.07 redrawn above 0.4,
uniform angles); perturber per `scenario.rs` `restricted` (μ = 1/999, circular; two arms:
inside sep = 1, outside sep = 4); one doll step Δt = 27.4k game-s = 8.68×10⁻⁴ yr (0659's
wave spacing 14.3k/41.7k/69k gs; SI-s assumption disclosed); grids per `belt.rs` (p 25-bit,
e 32-bit, ω 32-bit, t_p 44-bit over the period); bits = Rice-coded |quanta| on held-out
members (codec.rs's uv-length measure).

| arm | column | \|δ\| p50 (quanta) | bits raw | one-slope | VoP-harm |
|---|---|---|---|---|---|
| inside | p | 1.52×10³ | 12.41 | 12.41 | 12.14 |
| inside | e | 7.08×10⁴ | 18.08 | 17.36 | 17.61 |
| inside | ω | 6.35×10⁴ | 18.45 | 18.44 | 18.22 |
| inside | **t_p** | **3.54×10⁹** | **1040.74** | 955.52 | 1021.21 |
| inside | TOTAL | — | **1089.67** | 1003.72 | 1069.17 |
| outside | p | 68.8 | 8.74 | 8.73 | 8.58 |
| outside | TOTAL | — | **1057.25** | 990.52 | 1057.85 |

- **Predictor classes fail**: the shipped codec's own shape (one shared slope: DFOR/CHORD)
  recovers ≤ 8% (1,003.72 of 1,089.67); the classical variation-of-parameters harmonic
  predictor (10 shared coefficients, the Gauss-equation form — post-hoc arm, disclosed)
  recovers ≤ 2%. Scrambled-magnitude control: 1,107.31 (inside) / 1,072.86 (outside) —
  within 2% of raw: **no structure exists at the grid scale for any shared predictor to
  recover; the departure's range is ~10⁹ quanta** (δt_p is dominated by the short-period
  phase term, δt_p ≈ −δ(M/n), p50 ≈ 5.9 h [INFERENCE for the split; the magnitude is
  measured]).
- **The finding is structural, not magnitude-tuned**: the outside arm's tide is ~22× weaker
  in p (68.8 vs 1.52×10³ quanta) yet t_p still costs 1,019.58 bits — any kick with
  \|δP\|/P above a few 2⁻⁴⁴ blows the column; the grid resolves periapsis to ~6 ms while a
  doll-step tide moves it by hours.
- **Element space is the right water** (PRINCIPLES 19): p+e+ω raw = 48.94 bits (inside) /
  37.68 (outside) — 22–28× under the total; δP itself = 1.5·δa/a ≈ 1.5×10⁻⁵ ≈ 2⁻¹⁶·2 — a
  ~15-bit number whose projection onto t_p through the body's phase (uniform M) is what
  scatters to ~10⁹ quanta. Store the deltas/rates (Peterson 2024, Gauss equations for local
  action-angle elements: an explicit formula for an impulse's effect in action-angle space —
  the exact operation the row needs; UNVERIFIED beyond the abstract), derive t_p on read.
- Controls: μ = 0 → max\|da\| 5.5×10⁻¹⁴ AU, max\|dω\| 3.9×10⁻¹² rad (exact zero at float
  scale); elements round-trip 1.4×10⁻¹⁵; step-halving (512 vs 256) median shift 0.0000.
- Resonance census (weak instrument, disclosed): inside arm 3.93% of bodies within
  \|Δn/n_p\| < 10⁻³ of a J:K (J ≤ 9), 22.0% within 5×10⁻³, 93.4% within 2×10⁻² (the J ≤ 9
  rationals are dense over this belt's period range); outside arm 0.00% at all three.

## Predictions (`predictions.md`, written before the run)

- **P1 FAILED** (honest miss, the run's content): predicted \|δp\| p50 ∈ [0.5, 40] quanta;
  measured 1.52×10³ (inside) / 68.8 (outside — inside the band on the weaker arm). My band
  came from a head-conversion error of the p quantum (0.5/2²⁵ = 1.5×10⁻⁸, not 1.5×10⁻⁵);
  the physics (δa ≈ 2.25×10⁻⁵ AU) matches the Gauss-equation estimate throughout.
- **P2 HELD**: t_p dominates (1,040.74 bits ≥ 15; it is 95.5% of the total).
- **P3 FAILED**: one-slope recovers 7.9% (< 60%); the post-hoc VoP harmonic arm also fails
  (1.9%) — consistent with P5's reading below, not with "structure missed by one slope".
- **P4 HELD** at the 10⁻³ band: 3.93% ≥ 0.3% (inside); instrument weak (93% within 2×10⁻²).
- **P5 FAILED as a control, and the failure is the finding**: scramble costs only +1.6% over
  raw — by my pre-registered rule this **voids the instrument as a structure detector**;
  the magnitude claims above stand on the μ = 0, round-trip and step-halving controls, which
  passed exactly. The two failures (P3, P5) agree: the departure is grid-noise-dominated;
  there is nothing for a shared predictor to win.

## What would make it wrong

The tide model is one circular perturber at the record's μ, not the plane's full set, and
Δt rides 0659's measured wave spacing under an SI-s assumption — but the t_p blow-up is
driven by the grid (2⁻⁴⁴ of the period ≈ 6 ms) against ANY kick of realistic size (the
22×-weaker arm still pays 1,020 bits), so the claim is robust to both. The bits are a float
instrument with a Python stand-in of the codec's Rice residual coder, not the shipped
encoder — orders of magnitude, and the column ranking (t_p ≫ e ≈ ω > p) is what matters.
First kick vs the birth program only: accumulation over repeated kicks, and the interaction
with the shipped `mix()` finalizer, are unmeasured (named next). Adoption cost: none (a
measurement); the design consequence — the kick lands as element/rate deltas, t_p is derived
— is a law.md/step-5 change owned by the integrator, and the 21–40-bit self-stirred row
measured by 07b4 already shows the smooth belt's floor, which this run does not touch.
Fit with PRINCIPLES: "if you find yourself fixing things that's oftentimes a signal that it
is the wrong representation" (19); "influences below one quantum accumulate" (6) — here the
influence is above one quantum on every column, so the fold must land where it is small
(element space), not be compressed where it is large (t_p).

## The lens

The scout's prior-art frame produced the mechanism (variation of parameters: Gauss 1810;
Lagrange planetary equations — farside.ph.utexas.edu/teaching/celestial/Celestialnode164;
Peterson, J. Guid. Contr. Dyn. 2024, action-angle impulse formulas — UNVERIFIED beyond
abstracts; LSM overlay: O'Neil 1996, UNVERIFIED at source) but the literature's requirement
(knowledge of elements for propagation) is not the game's (a compressed row under quantized
kicks at 10⁹); the lens may have missed fields that store clocks under drift (GPS ephemeris
t_oc references? spread-spectrum code tracking?) — unsearched under the time budget. The
lens also nearly missed the real story by planning to read predictor quality (P3) where the
magnitude (P1/P2) was the answer — the pre-registration caught my own wrong band first.
