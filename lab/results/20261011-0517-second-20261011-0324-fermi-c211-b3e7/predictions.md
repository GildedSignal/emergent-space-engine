# Predictions — kick-magnitude rung (written before the sweep)

The checker named the experiment: the 61-bit scar and f_cum ≤ 0.55 are measured at one
hardcoded magnitude (t ±2^16, E/L/ω ±2^10). I sweep the delta exponents (modes k0 = shipped
… k5, plus `uniform` = a fresh law-orbit draw for E/L, uniform ω, t ±2^46 — the family jump;
probe: pairwise |ΔE| med 2^35 p99 2^40, |ΔL| med 2^37 p99 2^39 over the law's orbit range).
Cases below are **not tuned on**: every number is a prediction from the representation
(Elias–Fano ordinal + per-field zigzag deltas packed at width ≈ b+2).

- **P1 — the scar constant is not magnitude-invariant.** S(mode) ≈ EF + Σ_c(b_c+2):
  k0 61 (the shipped 61.2), k1 85, k2 109, k3 133, k4 157, k5 ≈ 172 (ω wraps mod 2^32, its
  delta width saturates ≈ 33), uniform ≈ 172. Tolerance ±15%. If S instead stays ≈ 61 the
  original constant is confirmed; if it grows super-linearly in b (exception cascades) the
  admission premise is in danger.
- **P2 — the admission rule stays linear at every magnitude**: bits/body ≈ 1 + S(mode)·f
  within ~10% for f ∈ {0.01 … 1} where form P is chosen; break-even f* = 33.4/S:
  0.55 (k0) → ≈ 0.19 (uniform). The *structure* survives, the constant is the small-kick corner.
- **P3 — the packed ceiling grows too**: B(f=1) from 53.5 (k0) to ≈ 150–165 bits/body
  (k4/uniform), bounded by the field widths (48+48+32+32 ≈ 160 + headers). The checker's
  "capped at 53.5" is as magnitude-specific as the 61.
- **P4 — saturation is magnitude-independent**: 40k updates on 4096 members → new scars ≈ 4096
  at every mode (one scar per member-ever-kicked; the ordinal set, not the delta, saturates).
  dH/kick at 10k updates ≈ S·(distinct fraction) ≈ 0.91·S.
- **P5 — reabsorption works at every magnitude**: a member restored to its program value
  releases ≈ S bits (dH_bits_per_reabsorb ≈ −S); magnitude changes the amount, never the fact.
- **P6 — timings flat in magnitude**: hot update ~100–130 ns, seal ~100–300 ns/update (≤2×
  worse at family-jump: wider residual words), b_compact ~1 µs/update. If seal cost grew
  ~linearly with b the H_live ledger would need re-pricing.
- **P7 — the 0.5% headline restated from the table** (arithmetic, not experiment): the
  81-minute corner is 23.9× over at RTF 1/32k (= 191 cores); sustainable population
  10⁹/23.9 = **4.2%** of a billion; at RTF 100 with the 0.3 averaged cadence 10⁹/22.4 =
  **4.5%**; at RTF 100 unaveraged 10⁹/2387 = **0.04%**. "0.5%" was 1/191, a division error.
- **P8 — verdict order unchanged**: with S ≤ 172 and encounter-driven f_cum growing at
  2.7×10⁻⁴/h (RTF 100, year orbits, 0.012 kicks/body/orbit), the memory gate is crossed only
  after ≳ 700 h of play even at family-jump magnitude; compute (24× over at the 81-min corner)
  still breaks first.

Kill criteria for the original claim: any mode ≤ family-jump whose curve departs from
1 + S·f by > 15% (non-linear admission), saturation failing (multiple scars per member), a
round-trip mismatch, or reabsorption failing at magnitude. Any of those kills the
admission-rule premise, not just the constant.
