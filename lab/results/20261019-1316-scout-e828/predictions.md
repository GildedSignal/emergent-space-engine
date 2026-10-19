# Predictions — 20261019-1316-scout-e828 (written before the `stream` runs)

Instrument: `epochflux` (e87d's integer replica verbatim: `arm_sections` + `arm_pair`'s
integer setup + `dioph::first_hit`; kicks rebuild the Body from its own state; BOTH
members kicked per kick). Dials: epoch E ∈ {1,2,8,64,256,1024} kicks between
re-certifications; horizon P ∈ {1,16,256,1024} passages ("event due within P"); kick
quantum κ ∈ {2⁻²⁶, 2⁻²³, 2⁻²⁰}·v_max. Seeds 20261018, 777 (held-out: 5, rng 4243).
Population: make_belt cell, 2,000 bodies, ρ = B = 3.34×10⁻⁶ AU, safety 1.1, width 1e-4
(e87d's anchor class). Leak(E,P) = P(certified silent at re-arm [due > P], true due ≤ P
at some blind kick inside the interval).

Pre-registered smoke (already run, disclosed): the replica reproduces e87d's anchors
(armed 0.774 at H=10⁶; w p50 53,946; deep-book flips 0.169–0.174/kick, κ-independent).
New near-book facts in hand: P(k≤16) = 0.0 (0/40,796), armed(128) = 2.2×10⁻⁴,
armed(10³) = 1.5×10⁻³; single-kick flips at H=128 ≈ armed(128)·0.67 and at H=10³ ≈
armed(10³): the re-deal rate, not zero — 08d0's H≤128 protection does not transfer.

- **P1 (controls).** dv=0 stream: k-grid constant, 0 leaks at every (E, P). E=1: 0
  leaks by construction (empty blind interior) — both must hold or the instrument is void.
- **P2 (E-shape — the discriminator).** Per-interval leak(E, P) follows the
  independent-re-deal law 1−(1−f_P)^E with f_P = the measured per-kick flip rate at P:
  linear in E for E ≪ 1/f_P, bending only by saturation. NO zero-leak knee at any E
  (against 08d0); NO √E superlinearity per kick (against 9fd1's toy shape read as a
  per-kick growth) — per-kick leak ≈ f_P, constant in E.
- **P3 (κ-scaling).** f_P within ×3 across the 64× κ sweep at every P ≤ 1024 (the
  re-deal is saturated in κ at belt cell occupancy; a κ¹ coefficient or a 1/κ² knee
  position would falsify this).
- **P4 (P-shape).** f_P ∝ armed(P): the leak's source is re-deal INTO the armed set,
  whose size is the book's near-density (depleted ~10⁵–10⁶× vs uniform-phase because
  dues sit ~10⁵ passages deep).
- **P5 (smallh, decisive for 08d0's near-protection).** Flips/kick at H=16 ≤ 10⁻⁴ and
  at H=128 within a factor 2 of armed(H): no protection window in H on the real book
  (the toy's protection was the clock conflation).
- **P6 (the freezeable composition).** At the belt-real clock ratio (one kick per
  ~2.8×10⁴ game-s per body vs a synodic passage ~10¹² game-s ⇒ r ≈ 2.3×10⁻⁸
  passages/kick), the game-horizon armed fraction is armed(r·E) ≤ 2.5×10⁻⁴·(r·E/128):
  leak per pair per kick ≤ 10⁻¹⁰ at E = 1024. The epoch rule is leak-unbound at
  belt-real ratios; E* is CPU-chosen (churn row = 355/E cores), and the wiki's
  knee-vs-flux contradiction resolves as "no knee, and no leak problem at real ratios".

Honest branches: if P2 fails with leak(E)/E falling (protection), 08d0's knee is real
on the shipped tier and E* freezes from its position; if per-kick leak grows √E,
9fd1's flux law transfers and E* freezes from b(κ).
