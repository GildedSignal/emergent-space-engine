# Predictions (second author, written before the decisive runs)

Task from the checker: re-adjudicate prediction 4 of run 20261012-0138-taleb-74a1 ("neighbours
roughly ∝ da, ratio ≈ 16 from 5e-4 to 8e-3" — measured 1.78×, window saturated at n²/2 by
da=2e-3, reported as held) and add the unsaturated regime below the ceiling. Provenance fix: every
command below runs through `tee -a ../run-log.txt` with wall-clock stamps, from the shipped crate
(byte-identical to `wt/cx-b-coorbital-cert` = adce00d6) plus one additive probe case (`disp2`),
diffed in `probe-second.diff`.

Not held out (checker's numbers, reproduction targets): `truth` (D200=0, T200=199, missed none),
`disp` (1,116,443 / 1,892,762 / 1,983,425), `scale`+`n8k` (phase 399,623/1,892,762/7,882,639/
31,860,946; tier 49,500/99,000/198,000/396,000; bcheck 63,721,892 vs 792,000), `ulp`
(499→124,750; 1,999→1,999,000; max_k 1→n−1), `panic` (phase.rs:35), `cone` (31,860,946→396,000),
branch test suite 11/11. The only genuinely held-out experiment is `disp2`, never run before
this file.

## The model (from the shipped phase.rs, no fitting)

reach = angular + 2·centre + (n_hi−n_lo)·H/2; shared shape (all e=0, ϖ=0) ⇒ centre=0, angular =
2·asin(ρ/2) ≈ 1e-4. Δn = 1−(1+19·da)^(−3/2), H=5. Mid-time phase arc L = 0.099 + (Δn)·H/2
(each shell drifts apart by Δn·mid). Uniform-density estimate:
**pairs ≈ C(n,2)·min(1, 2·reach/L)**, C(2000,2)=1,999,000.

Sub-ρ subtlety I owe the record: with the scene's shared λ grid, bodies (s,i),(s',i) sit at
distance |s−s'|·da at t=0. Below da ≈ ρ this scene is a genuinely dense blob with real contacts —
the ladder therefore crosses two regimes, and both are predictable.

## P1 — DISP2 ladder (m=100, k=20, n=2000, H=5, ρ=1e-4), held out

| da | model pairs (±10%) | conc = reach/TAU | contacts (exact) |
|-------|--------------------|------------------|------------------|
| 1e-5 | 32,571 | 1.29e-4 | 13,500 |
| 2.5e-5| 74,588 | 2.99e-4 | 5,400 |
| 5e-5 | 142,609 | 5.82e-4 | 1,900 |
| 1e-4 | 271,591 | 1.15e-3 | 0 or 1,900 (min distance = ρ exactly at t=0; strict d<ρ is a float tie — either answer is consistent, disclosed) |
| 1.2e-4| 320,719 | 1.37e-3 | 0 |
| 2e-4 | 504,511 | 2.27e-3 | 0 |
| 4e-4 | 890,265 | 4.51e-3 | 0 |
| 5e-4 | 1,051,780 (checker measured 1,116,443 here: +6.2%, the 20-shell union is trapezoid-density, not uniform — tolerance covers it) | 5.62e-3 | 0 |

Phase fires at every point (conc ≪ 0.5): the π fallback is unreachable in this regime.

Contact counts: boundary contacts at t=0 only — cross-shell same-index pairs with j·da < ρ,
j apart = Σ_{j·da<ρ}(20−j)·100 = 13,500 / 5,400 / 1,900 at 1e-5 / 2.5e-5 / 5e-5; separation
grows monotonically over [0,H] (outer shells lag), so no interior minima.

## P2 — the ∝da regime below the n²/2 ceiling (the checker's named experiment)

- Log-log slope of neighbours over the clean zero-contact ladder {1.2e-4, 2e-4, 4e-4}: model 0.85;
  accept 0.80–0.92. Over {1e-5 → 2e-4}: model 0.91; accept 0.85–0.97. Slope < 1 is *structural*,
  not noise: L itself grows ∝ da (window must cover a drifting arc); slope = 1 − window/arc → 1
  as da→0. The claim "work follows dispersion × horizon, not contacts" is exactly this: below
  da≈ρ the window is angular-sized (contact scale, 4,038-pair floor at da→0, work ≈ 2.4× contacts
  at 1e-5); above it, dispersion-sized, ×H.
- No ceiling: pairs(4e-4) < 60% of 1,999,000 (model 44.5%); pairs(5e-4) in [50%, 60%]; the old
  saturated points 2e-3 / 8e-3 regenerate 1,892,762 / 1,983,425 (95% / 99%), ratio 8e-3 ÷ 5e-4 ≈
  1.78 — prediction 4 as written (ratio ≈16) was saturated at both ends, and its honest
  re-adjudication is: linear-with-drift-correction below da ≈ 5e-4, ceiling above.

## P3 — safety in the blob regime (held out)

All sub-ρ contacts are found: at 1e-5 / 2.5e-5 / 5e-5 the certificate's emitted event-pairs ⊇
the 13,500 / 5,400 / 1,900 predicted contact pairs; zero missed (boundary contacts at t=0 are
in the certificate's contract). Cost there stays ≈ 2.4× / 13.9× / 75× the contact count — the
certificate is near-tight when dispersion is below the contact scale and degenerates as
dispersion×H/2 takes over.

## Commands (each ≤ 60 s except n8k)

cd lab/results/20261012-0311-second-20261012-0138-taleb-74a1-4ec3/work/enc
CARGO_TARGET_DIR=../../target cargo build --release
../../target/release/probe <case>   # truth disp disp2 scale n8k ulp panic cone
CARGO_TARGET_DIR=../../target cargo test --release
