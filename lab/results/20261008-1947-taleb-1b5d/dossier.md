# Dossier — the phase-neighbour certificate breaks silently outside aligned circular formations

## Claim

The gold `20261006-0346-taleb-09b5` invariant ("every real encounter lies within
partner rank 4 along the orbit") holds only for aligned-apsides, near-circular
formations with a certificate lifetime below the synodic crossing of the k-th
phase gap; on lawful fleet states with the **same** a-concentration but eccentric
or apsidally scattered orbits, rank-k silently drops 95–100% of real encounters
(partner ranks ≈ N·|Δλ\*|/π, growing linearly with N), rebuilds cannot fix it,
and inter-formation encounters (battles) are 100% dropped — so the certificate's
trigger must read the conjunction mean-longitude displacement and the phase
cluster structure, not a-concentration.

## Bottleneck

Board item 3/6 (encounters without quadratic work; the top scaling risk). The
adopted design replaces the quadratic window tier with an O(n·k) phase-neighbour
certificate. This run does not kill that certificate; it bounds its domain and
gives the trigger, one step before `crates/encounters` builds it. Gain: avoiding
a silently-wrong encounters layer of the kind that already failed B13 once
(H0214: 7 of 64 flybys lost); the fix costs one closed-form gate.

## Evidence

Machine: GitHub Actions Linux, 8 vCPU, load 1.17, 13.8 GB free, 42 d uptime.
Truth: Kepler two-body motion (μ=1, a=1, P=2π), all-pairs min distance < ρ/a =
10⁻³ over [0,T] by time-sliced KD-tree with query dilation ρ + v_cap·dt
(v_cap = 2·max body speed bounds every relative speed, so no sub-ρ minimum can
fall between slices) and vectorized ternary refinement; every trough of every
hit run is refined. Controls both ways: a hand-planted conjunction pair must be
found (PASS), radially-separated circular orbits must yield nothing (PASS);
resolution control at 8× finer slicing finds the identical pair set (2/2).
Certificate: circular rank in mean longitude λ = M₀ + ϖ, pair found if either
side's rank ≤ k; "rebuild" = re-rank each P/4.

Aligned near-circular formations (the gold's regime; N=1024, ϖ aligned, uniform λ):

| case | miss@4 at build | miss@4 with P/4 rebuilds | max rank |
|---|---|---|---|
| S=10⁻⁴, T=4P | 0.4% | 0% | 5 |
| S=10⁻³, T=1P | 1.8% | 0% | 6 |
| S=10⁻³, T=4P (2 seeds) | 35.1% / 36.2% | 0% | 13–16 |
| S=10⁻², T=4P | 49.8% | 0.33% | 15 |

Eccentric scattered-apsides swarms (same tight a, S=10⁻⁴, ϖ uniform, T=2P):

| case | miss@4 | miss@16 | rank p50 / max | rebuild helps? |
|---|---|---|---|---|
| e=0.3, N=256 (2 seeds) | 95% / 100% | 90% | 58–79 / 101–103 | no (identical) |
| e=0.6, N=256 (3 seeds) | 96–100% | 92–96% | 121–166 / 202–214 | no |
| e=0.6, N=128 (2 seeds) | 100% | 100% | 34–96 / 95–99 | no |
| e=0.8, N=256 | 100% | 93% | 206 / 244 | no |

Two-ϖ-cluster battle (e=0.4, ϖ ∈ {0, π}, N=256, 3 seeds): inter-cluster
encounters miss@4 = **100% in every seed** (max rank 128–135 ≈ N/2); the
intra-cluster remainder mostly sits at rank ≤ 4.

Mechanism (per-pair, `work/geo.py`): the partner rank equals N·|Δλ\*|/π where
Δλ\* is the pair's mean-longitude separation *at conjunction* — the Kepler M−f
offset evaluated at the Binet crossing longitudes. Correlation measured vs
predicted across encounter pairs: 0.994 (e=0.6), 0.998 (e=0.8), 0.998 (battle);
Δλ\* p50 = 1.78 rad (e=0.6), 2.59 rad (e=0.8), 1.56 rad (battle). Ranks halve
with N (128 vs 256), i.e. required k grows ∝ N·e: any fixed k is quadratic in
disguise outside the aligned regime.

Exact commands (each ≤ 60 s, from `lab/results/20261008-1947-taleb-1b5d/work/`):

    python3 probe.py '[{"name":"A_gold_T4_s1","N":1024,"T_periods":4,"rho":0.001,"slices_per_period":2048,"e_base":0,"sig_e":0,"w_mode":"aligned","sig_a":0.001,"lam_mode":"uniform","seed":1}]' r1.json   # 14 s
    python3 probe.py '[{"name":"B_e06_s1","N":256,"T_periods":2,"rho":0.001,"slices_per_period":16384,"e_base":0.6,"sig_e":0,"w_mode":"uniform","sig_a":0.0001,"lam_mode":"uniform","seed":1}]' r2.json  # 10 s
    python3 probe.py '[{"name":"D_battle_s1","N":256,"T_periods":2,"rho":0.001,"slices_per_period":16384,"e_base":0.4,"sig_e":0,"w_mode":"two_cluster","sig_a":0.0001,"lam_mode":"uniform","seed":1}]' r3.json  # 10 s
    python3 geo.py   # per-pair displacement analysis, 45 s

Raw records: `work/results_A.json` (5 cases), `work/results_B.json` (8 B cases
plus the 3 battle cases), `work/results_D.json` (the same 3 battle cases),
`work/results_geo.json`; probe `work/probe.py`.

## Predictions

`predictions.md` was written before the sweep. P1 (drift vs lifetime: 0% at
S=10⁻⁴, 5–40% at S=10⁻³ T=4P, ≥50% at S=10⁻², rebuild zeroes all but residue)
held: 0.4%, 35–36%, 49.8%, residue 0.33%. P2 (geometric misses at e≥0.3,
linear in N, no rebuild fix) held: 95–100%, max rank halving 202→99, rebuild
identical to the digit. P3 (inter-cluster 100% missed, intra-cluster fine)
held on all seeds. P4 (an a-concentration trigger fires hardest exactly where
misses are total — S=10⁻⁴ is the tightest case measured) held by construction
of the cases. My kill criteria (miss@4 ≈ 0 at e=0.8, or inter-cluster rank ≤16)
did not trigger.

## What would make it wrong

The gold's actual workload parameters are unreadable here (its branch is not
fetchable from this job), so "regime reproduced from the board's description"
could misdescribe it — but the gold's claim as recorded is regime-free. The
truth is pure Kepler: mutual gravity is absent, so horseshoe/Trojan librations
(a real co-orbital behaviour) are untested; N ≤ 1024 (ranks scale linearly, so
larger N only worsen k); encounter counts in eccentric cases are 20–30 per seed
(thin, but stable across seeds and the mechanism correlation is 0.99+). If the
engine's formations are guaranteed aligned-apsides and near-circular by
construction (no scattered swarms, no battles of two co-orbital fleets), the
eccentric findings are out-of-domain — that would narrow, not overturn, this
result; the drift-lifetime bound then remains the only live correction.

## Cost of adopting, and fit

Adoption is one gate plus a maintenance rule, not a new tier: (1) trigger on
the conjunction displacement — k_needed ≈ N·max|Δλ\*|/π with Δλ\* from (e, Δϖ)
closed form (Binet crossing longitude + Kepler M(f)); if k_needed exceeds the k
budget, those pairs go to the existing Binet-cone tier; (2) certificate expiry
by synodic drift (rebuild when the k-th gap is crossed, T_cert ≲ k·P/(1.5·S·N)),
maintained by adjacent swaps in the sorted λ ring so maintenance work tracks
real conjunctions — rank order changes with **no** element change, so "paid
once per element change" is false as stated; (3) one certificate per phase
cluster (gap detection), never per a-cell alone. PRINCIPLES: "a failed
expectation is not automatically a failed method" — this kills no method, it
sizes a trigger; "Floats may explore; only integers decide" respected (the
findings are rank counts and miss fractions, orders of magnitude); the
falsifying test was built first and cheapest ("even baby spartans started
small"). The miss is exactly the ruin class the board already met at B13:
silent, not slow.

## The lens

Taleb asked where the adopted certificate is concave and who pays: the answer
is that its cost win is average-case while its miss is worst-case-total, and
the player pays at the first fleet battle. This lens may have missed the
constructive speed question (how expensive the Δλ\* gate is per pair — it is
closed-form and per-certificate, not per-pair, but I did not measure it) and it
did not test gravitational (librating) co-orbitals, which need an integrator.
