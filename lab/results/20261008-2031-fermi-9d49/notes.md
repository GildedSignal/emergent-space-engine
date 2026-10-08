# Derivation notes (H_live, run 20261008-2031-fermi-9d49)

## Definitions
- A **distinction** is a first quantum crossing: the moment a body's state leaves its program's
  prediction by ≥ 1 quantum of the law's grid. After it, the body carries its own record
  (scar in place, or individual). Subsequent events mutate that record in place (~0 new bits;
  re-anchoring per law.md is compute, not memory).
- H_live(t) = Σ programs + Σ scars + Σ individuals. Per body it **saturates**; only the census moves.

## Measured (the shipped store, round-trip exact; commands in dossier.md)
| form | bits/body | source |
|---|---|---|
| convoy program member | 17.29 (floor 13.73) | measure.jsonl |
| formation member | 29.60 (floor 19.92) | measure.jsonl |
| one kick on a convoy member | +70.7 (formation +76.7) | bits_after − bits_before, 2×10⁵ kicks |
| individual, shared doll key (traders) | 149.73 (floor 145.51) | measure.jsonl |
| individual, no structure (random) | 196.62 (floor 189.51) | measure.jsonl |

Floor check (claim-check duty): convoy floor 13.73 bits vs analytic entropy of geometric(12)
launch gaps ≈ 12 + log₂e ≈ 13.4 — the crate's entropy accounting reproduces.

## Budget arithmetic
4 GiB (ABP's open body cap) / 10⁹ bodies = 34.4 bits/body.
- all convoy 2.01 GiB ✓; all formation 3.45 GiB (edge) ✓
- scarred members: f ≤ 24.2%; individuals: f ≤ 12.9% (trader-like) … 9.5% (random)
- all individual: 17.4–22.9 GiB ✗ (2–3× over the whole 8 GB)

## Rates (game-seconds; belt = B18b geometry: 8.4×10⁶ bodies, 2.2–3.2 AU annulus,
q_rel = 10⁻⁶, v_orb(2.7 AU) = 18 km/s, v_rel = 5 km/s, orbit 4.4 yr)
1. **Mutual gravity never promotes.** b_cross = 2Gm/(q_v·v_rel) = 16 m for 1-km rocks vs
   contact radius 2 km; ratio ∝ R² → worse for smaller rocks. All mutual gravitational kicks
   are sub-quantum and sum exactly on the grid (r2): 0 bits until a crossing that never comes.
2. **Contacts promote** (2D sweep, v_rel does not cancel): rate/body = S_n·4R·v_rel.
   1-km rocks: one contact per 72 yr game time → belt turnover in ~centuries.
   1-m rocks: 7.2×10⁴ yr. Scales linearly in rock radius.
3. **Embedded masses** (the movers): promotion rate of others = S_n·4GM/q_v (v_rel cancels;
   units [m⁻²][m³s⁻²][sm⁻¹] = s⁻¹). Belt turnover in T needs M ≥ N·q_v/(4GS_n·T):
   8×10¹⁴ kg per Gyr, 8×10¹⁷ kg per Myr. One Ceres: 26 promotions/game-day, belt individual
   in ~870 yr. A 10¹⁵ kg fleet alone: 0.01 promotions/yr (dead; alive only as aggregates, P6).
4. **Resonance chaos:** first-order widths W = 2.5μ^(2/3) ≈ 0.024a vs spacing (2/3)/j² ≈ 0.027a
   (j≈5) → 91% axis coverage; bounded claim: f_chaos × N promotions once each, within ~orbits
   (strong-zone separatrix kicks are already ≥ quantum) to 6×10³–6×10⁵ yr (weak chaos).
5. **Births/deaths:** program births ~0 bits/member; individual births player-rate: dead terms.

## The closure the engine needs
Contacts both promote (the pair becomes individual) and recycle (creation events emit fragment
**programs**; ejections retire). Steady state: dH_live/dt = promotions×~88–150 bits
− retirements×~150–197 − recycling. Without recycling/retirement, promotion is monotone and a
dense 2D belt (or a 10⁹-body universe of belts with f_chaos ≳ 0.1–0.3) exhausts the 4 GiB body
budget in 10²–10⁶ yr of game time depending on rock radius and embedded masses.

## What the dashboard (b-h-live) should count
Not events (6×10⁴ kicks/game-second create ≈ 0 bits): count promotions (first crossings),
retirements, program births, and bytes at the census level. The rate is only meaningful
accumulated over long windows (per belt: 10⁻⁸–10⁻⁵ promotions/s).

## Machine state
Linux x86 cloud runner, 8 vCPU; measure.rs records empty load/swap/therm/power fields on this
runner (no sensors exposed). Orders of magnitude only, per lab rules; integrator re-measures on M1.
