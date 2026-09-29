# Rung r2 — carry width (run 20260929-1857-rung-r2-carry-width-e3af)

**Claim.** A 32-bit value word plus a 32-bit sigma-delta carry per quantity stores a
float64 orbit generator *exactly* (phase error identically zero, conjunction order
exact), while 16 and 24-bit pairs walk linearly; and the kick criterion as frozen is
unpassable at any width against a float64 kick stream — the residual is the input
graining, not the carry mechanism.

**Bottleneck.** Board #5 (units, widths, memory: one question) and #0 (representation,
§4 of representation.md). Expected gain: the increments question closes at 2×32 bits per
quantity = 320 bits/body exactly on the rung's budget; it deletes any wider accumulator
for memoized cycles. Verdict: **KILL** — `sd32` fails only `kickgrow`; `sd16`/`sd24` fail
`phase` and `kickgrow`; negatives fail every behaviour gate (correctly killed, no VOID).

## Metrics (canonical, `metrics.json`; cloud Linux/x86, orders of magnitude only)

| config | phase | order | drift | kickgrow | bits | verdict |
|---|---|---|---|---|---|---|
| sd16  | 1.0 | 1.0 | 1.0 | 2.459 | 160 | fail phase,kickgrow |
| sd24  | 1.0 | 1.0 | 1.0 | 1.9777 | 240 | fail phase,kickgrow |
| sd32  | 0.0 | 1.0 | 1.0 | 1.8167 | 320 | fail kickgrow |
| trunc16 | 1.0 | 0.0    | 0.0 | 1.0826 | 80 | negative: killed |
| round16 | 1.0 | 0.0156 | 0.0 | 1.0826 | 80 | negative: killed |

Mechanism (author's choice, stated): **first-order** sigma-delta. Per body, per quantity:
one shared exponent (block floating point) and two w-bit registers — value + carry —
together one 2w-bit fixed-point accumulator. Increments: the pair holds the generator
once and the wide phase counter advances by exact integer adds. E, L: the pair
accumulates kicks gridded at the pair's unit (round-half-even), spill = carry overflow.
All differences are computed exactly (integers/Fractions); the fitted exponent is
Theil–Sen over medians of 10 log-spaced windows on the last 90% (a global least-squares
fit on a stochastic path is estimator-dominated: it reads 2.4 on pure √N data).

## Evidence

- **Increments are exact at 32.** A float64 generator has ≤ 53 significant bits; with a
  per-quantity power-of-two exponent, the 64-bit pair (value = top 32, carry = low 32)
  holds it exactly — verified per seed: `X*F == x`. So |φ_stored − φ_true| ≡ 0 at every N
  (exponent 0, picture: sd32 has no curve), and conjunction order matches the reference
  for all 64 pairs. The pairing is why "we love 2" (principle 16): the dyadic block
  exponent is what makes 32+32 exact for a 53-bit float.
- **16/24-bit pairs compound linearly** (error = N·ρ exactly, exponent 1.0 on every
  seed): magnitudes 4×10⁻³ rad (sd16) and 3×10⁻⁸ rad (sd24) after 10⁶ cycles. sd24 is
  invisible in behaviour but the wrong *type* (principles 2, 13).
- **Kicks vs a float64 stream: no width passes.** Per-seed median residual exponents:
  sd16 0.95 (linear — see below), sd24 0.51, sd32 0.54 (random walks of the graining
  residues; σ(10⁶ kicks) = 4×10⁻¹²·v₀ and 6×10⁻¹⁷·v₀). The frozen worst-seed criterion
  reads 1.8–2.5 because a single path's fit is noisy; the median is the growth law.
- **sd16's walk is linear, and it is a principle-6 failure:** at w=16 the pair's unit is
  v₀·2⁻³⁰, so 16.7% of kicks fall below half an LSB where rounding is biased: measured
  bias −2.2×10⁻¹²·v₀/kick → −2.2×10⁻⁶·v₀ over the run (still ≪ the 1% drift band, so
  `drift` passes at every width: sigma-delta carries do preserve the secular change,
  1.0 for all SD configs vs 0.0 for the negatives, which lose *every* kick — max kick
  = 0.03 LSB — and freeze E, L while the reference moves 10⁻²).
- **Gridded-source diagnostic** (held-out prediction 5): if kicks arrive as integer
  multiples of the pair unit — the engine's real interface, cells holding integer mass
  moments — the residual is **exactly 0** at every width (verified at 16 and 24 bits;
  at 32 the only difference is the float64 *rendering* of the reference). The walk
  belongs to the float64 stream, not the carry.

**Commands** (each ≲ 20 s): `python3 lab/results/20260929-1857-rung-r2-carry-width-e3af/rung_r2.py`
(writes metrics.json, detail.json) · `picture.py` (picture.svg) ·
`python3 lab/verdict.py lab/rungs/r2-carry-width.md lab/results/20260929-1857-rung-r2-carry-width-e3af/metrics.json`
→ `Verdict: KILL; no candidate passed every criterion; killed: sd16, sd24, sd32`.
Oracle port sanity: Mercury p=3.75e7, e=0.2056 → 5.02654885×10⁻⁷ rad/orbit vs 6π/p =
5.02654825×10⁻⁷; periods match the frozen Darwin series to 1.5×10⁻⁵ at p=1000.

## Predictions (`predictions.md`, written before the run)

1–4 held: sd32 exact (phase 0, order 1.0), sd24/sd16 phase linear at exponent 1.0,
negatives killed everywhere including drift = 0.0. Two misses: (a) I predicted sd16
flips some conjunction orders — none flipped (quantization displacement ~5×10⁻⁶ synodic
periods vs ~10⁻⁴ minimum event gaps); (b) I predicted worst-seed kickgrow ≈ 0.5 — the
per-seed *median* is 0.5, but the frozen worst-seed statistic is estimator-noisy (1.8–2.5).

## What would make it wrong; cost; fit

- The conjunction model reads out a uniform memoized rate Ω = Δφ/Δt between
  periapsides; a real anomaly interpolation could order near-ties differently — but at
  sd32 the stored order equals the reference order *by construction* (exact pairs), so
  that zero is robust. If generators were ever computed above float64 precision, 32+32
  would stop being exact and the phase criterion would need re-deriving.
- The kick conclusion holds only for float64 streams consumed at the accumulator. The
  decision the rung exposes for the integrator: grid kicks at the source (storage then
  exact at any width, and the width question moves to the perturbation model's own
  quantum), or keep float64 streams and treat the √N graining walk (2⁻⁴⁷·v₀ scale at 24
  bits) as the budget. Either way the frozen `kickgrow ≤ 0.2` cannot distinguish
  widths today.
- Adoption cost: none for the increments result — it is one line of law ("a memoized
  cycle is a 2×32-bit pair per quantity, block-exponent per body"), 320 bits/body on
  budget. PRINCIPLES: "basically we don't want errors that can compound" (#13) — the
  only guaranteed way is exactness at width, and 32+32 is where it starts; "influences
  below one quantum accumulate" (#6) — true at 24/32 bits, false at 16.

## The lens

A directed rung; no lens. Author-chosen details that could have skewed things: first
(rather than second) order — irrelevant here since the pair sums exactly and the
residual is input graining, which no modulator order can recover; the Theil–Sen
exponent estimator (stated, with the global-fit alternative's failure shown); the
uniform-rate conjunction readout; Δφ stored as the full sweep 2π+advance. I did not
test second order, nor non-dyadic (π-friendly) grids, which could change where the
*conjunction* walk starts but not the phase result.
