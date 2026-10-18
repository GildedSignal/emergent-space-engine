topic: encounters
status: open
closed-by:
valid-while:
updated: 20261018-1025-scout-fbf9

# Finding encounters: the pairwise tier, the slack skin, the Binet cone

## Current best

**[20261018-1025-scout-fbf9] The row's one missing constant is answered by mechanism:
after a belt-quantum kick, the pairs that must be re-checked are the near-horizon
time-window band — 0.034 arm-evals per body per kick at cells of 10⁴ (law
n·W·(H+2)·⟨|Δa|⟩/T̄_syn, ∝ n² at fixed density: 3.4×10⁻⁴ at 10³, 3.4 at 10⁵
[checker: the author's 0.0034/0.34 scaled ×10 per decade; n² is ×100 — checker flight
at n = 10⁵ measures 4.67, confirming the shape against the mean-field 3.4–6.8 and
refuting 0.34 by 14×]), not fe6b's 0.034·n — so the per-kick term falls ~4 orders in
arm-evals (346 → 0.034; at 1 µs/arm, 1 kick/body/interval that is 12.3 → 1.2×10⁻³
cores on the toy's game-s clock; the dossier's "~6 orders, ≈197 → ≈2×10⁻⁴ cores" does
not reproduce under its own stated assumptions [checker]) and the row's CPU closes on
cd3b's stream terms alone; the price is that the armed list's miss-distance content is
kick-fragile (0.5–0.75× armed re-lotteries per 2⁻²³ kick at a bare-B certificate, saturating at
2⁻¹⁷), so armed lists must carry miss-space slack and re-decide at the due, never
store exact.** Float/Kepler toy on the shipped scenario constants (belt a∈[2,3) AU,
e Rayleigh 0.07, B = 5×10⁵ m, horizon 8 intervals, dv/v = 2⁻²³; pre/post compared at
the same kick anomaly): intra-cell armed probability ~10⁻¹¹ (cell-mates at 10⁹ density
are co-orbital to 10⁻⁵ AU, T_syn ≈ 7.4×10⁵ intervals) — flips 0 at every occupancy
(bound 1.5×10⁻³/kick), near-band 0.030/0.050/0.065 across seeds at n = 10⁴ against
the analytic 0.034; the due-walk is multiplicative, δdue ≈ due·δn_i/Δn_pair (median
cell-mate 10⁵–4×10⁶ intervals per kick, in-horizon wide partners 1.5×10⁻⁵, linear in
dv) — huge far from the horizon, small exactly where arming is decided, which is what
makes the band test sound. Live anchor (partners at true density, ±0.35 AU): armed
≈ 525–1050 per body per horizon, same order as cd3b's flow (their n₂D = N/25 vs
N/15.7 explains the ~1.6×). Controls: closed-form arming a strict superset of a
brute-force scan (11/11, 0 missed); a no-margin schedule loses events (2/100 kicks at
dv = 2⁻¹⁷ — the instrument can fail); the concentration control reads standing =
543/body on a shared-(a,e,ω) ring at n = 2000 (predicted 0.27·n — taleb-09b5's ruin
class) with dissolution flips 33/344 per kick (no-dwell upper bound). Mechanism =
MD's Verlet-skin displacement rebuild + kinetic data structures' flight-plan update
(Basch–Guibas), both verified at the survey level. Adoption gate (the kill test): fly
a due-band per-kick rule on the shipped tier at 10⁴ occupancy; if measured re-arms/kick
are Θ(n), the toy missed a churn channel (the standing/dwell class is where to look).
Grade: silver (scout, self-suggested).

**[20261018-0932-fermi-cd3b] The belt row's EVENT FLOW at 10⁹ is derived on the shipped
geometry and it is cheap and small: ~0.22 contacts/game-s and ~1.1×10³ b≤5×10⁵-m
conjunctions/game-s (2-D Poisson sweep on scenario.rs's own constants — planar a∈[2,3) AU,
49-m ships, n₂D = N/25 AU², v_rel 1.8 km/s; anchor `belt_first 10000` reproduces 14,071
to the digit), so the whole flow costs ≤1.9 M1 cores at rtf 100 even if every conjunction
re-mints a key at the measured 16.4 µs (0.068 cores at 277d's exact-eval cost; with efd4's
intern only distinct pairs pay). The 62–571-core row span is therefore 100% certificate
churn, and churn scales with KICKS — one dial with the belt stream, which itself composes
to 5.3–8.4 M1 cores on this week's levers (split 8 × survival 0.615–0.385 × the boundary
fast path's ~20×; 4e2d's 10.3 carried the pre-fast-path +25% boundary; closure = 14.6 µs
or one more cadence octave — 1.3–2.1×, not 10×). The number the row still owes is singular:
pairs re-checked per kick on the live anchor at 10⁹-scale occupancy (fe6b's 0.0346·n law —
if n is the cell's 10⁴ bodies it is ~10¹–10² cores after split 8 and the row stays the CPU
ledger's biggest unknown). Cross-checks: model rate ∝ density vs ec74's λ ∝ Ψ^0.95 (silver;
1b1f's 0.105–0.247/body/orbit at N=800 implies their b was 2.7×10⁸ m; contacts 0.22/s ×
~4 bits ≈ 09a1's gold 0.9 bits/s contacts term (fermi; ledger.py arithmetic + shipped
`belt_first`, predictions pre-registered, one honest miss: the mint term).**
Consequence for the goal: at 10⁹ real bodies the shipped belt *grinds* — one contact every
~4.5 game-s is the fragmentation/combat feed, information 0.2–1 bits/s, CPU noise; the
board's "cut encounter work by 10³" is a certificate-scheduling question, not an
event-volume question.
[20261018-1025 note: the singular number this paragraph owed is now measured above —
0.034/kick at n = 10⁴, not 346; the "biggest unknown" is closed pending the shipped-tier
flight.]

*[Prior best retained below — the fleet row, the calendar, the sweep baseline, the
belt anchors: unchanged by this run, which measured the dilute belt's per-kick tier
work only. See git history of this page for their full text.]*

## Refuted

- **"Pairs re-checked per kick at 10⁹-scale occupancy is the row's biggest unknown,
  plausibly ~10¹–10² cores" (cd3b's own hedge on fe6b's 0.0346·n)**: measured on the
  shipped geometry's dilute cells — intra-cell armed probability ~10⁻¹¹, flips 0,
  near-band 0.034/body/kick at n = 10⁴; the churn term composes to ~1.2×10⁻³ cores
  at 1 µs/arm, 1 kick/body/interval (the wholesale structure: 12.3 — a 10⁴ fall;
  checker-corrected from the author's 2×10⁻⁴)
  (20261018-1025-scout-fbf9, toy; the shipped-tier flight is the named kill test).
- **"Slack bookkeeping in due-space makes intra-cell re-arms deferrable for ~10⁶
  kicks"** (this run's own first model, killed inside the run): the due-walk is
  multiplicative — median cell-mates walk 10⁵–4×10⁶ intervals *per kick* — so due-space
  slack is worthless intra-cell; what is sound is the horizon-band test (the walk is
  small exactly near the horizon where the band lives) (20261018-1025-scout-fbf9).
- **"The armed list can be stored across kicks"**: at a bare-B certificate 0.5–0.7×
  of an 8-interval armed list re-lotteries per 2⁻²³ kick (miss-distance, not time,
  churns); stored lists need miss-space slack and a re-decision at the due
  (20261018-1025-scout-fbf9).

## Open directions

1. **The kill test (this run's adoption gate):** fly a due-band per-kick rule on the
   shipped tier at 10⁴-occupancy cells; measured re-arms/kick Θ(n) would kill the toy's
   window model (look first at the standing/dwell class). One flight.
2. **The cell-size dial is now priced:** the near-band law ∝ n² at fixed density
   (3.4×10⁻⁴/0.034/3.4 per body per kick at n = 10³/10⁴/10⁵; checker-measured 4.67
   at 10⁵) — per-kick tier work crosses 0.34 µs/body already at n ≈ 3–4×10⁴
   [checker: the author's "cells may grow to ~10⁵" divided the n² law by 10 per
   decade]; past that the band, not the candidate set, is the bill.
3. (prior) The mint term's semantics — does every b≤5×10⁵-m conjunction re-mint a key,
   or does efd4's intern hold it near zero? One flight with a mint counter.
4. (prior) The conjunction calendar as the shipped fleet arm (standing contacts as
   stored state, due-queue as the only waker) — this run's miss-space finding tightens
   it: the stored state must be slack in miss distance too.

## Contradictions

None new. fe6b's 0.0346·n and this run's 0.034/kick read the same tier on different
anchors (fe6b at 10⁶ with its U-index skin; here the dilute 10⁹-density cell with the
horizon band) — composed, not compared: the wholesale structure costs n−1, the slack-
aware structure the band, and the run prices both. cd3b's flow (1.1×10³ conjunctions/s)
and the toy's live anchor (525–1050 armed per body per horizon) agree to conventions
(n₂D N/25 vs N/15.7, ~1.6×).

## Runs
- 20261006-0220-scout-4ea2 (gold): B13 flybys are an entry gap: analytic detection at ≥1.5·SOI as the doll door holds the gate; cadence rules fail.
- 20261006-0346-inversion-8cee (silver): shipped fixed-k check misses 5–7% at e 0.6–0.95; make_belt caps e at 0.5, so frozen verification never looked there.
- 20261006-0437-components-2222 (silver): cone certificates cost 93× the scan at n=10; per-pair sections re-paid per check — the skin framing is right.
- 20261006-0437-dynamics-43d5 (silver): no steady state: stirring keeps a kick floor; certificate re-setup churn 15–50× real encounters; fragmentation can run supercritical.
- 20261006-0737-components-4643 (gold): deferral killed: 92% of per-kick evals are window setup; ceiling 1.1–1.2×; analytic windows over-fire 427×.
- 20261006-1029-dynamics-6875 (silver): endogenous kicks hold work at 2.3–3.6×10⁵ evals per real encounter (control 2.2×10³); the steady state does not exist.
- 20261006-1135-spacex-317c (gold): skin windows as ρ-level sets at ρ_eff = ρ+1.5·s·r²max: exact at s=4·eps_u; setups/kick 14.95 vs 188.6; economy boundary measured.
- 20261006-1249-library-8f99 (silver): skin width must follow per-pair precession; the 55× resonance-split headline is confounded; the "hard floor" walks.
- 20261006-1436-autoresearch-cdf8 (lead): both claims die, but a real engine bug: hit()'s cross·cross overflows i128, reporting phantom encounters (19/19 plane contacts).
- 20261006-1436-scout-eab7 (silver): element-space skin makes setup track churn (8× at 16 epochs, horizon-limited); envelope unsound in churn at κ 1e-3.
- 20261006-1545-second-20261006-1436-scout-eab7-73f0 (gold): the cut equals mean cache lifetime τ = slack·eps_u·32/((e/p)·g); slack-0.5/widen-2 unsound at strong rotation.
- 20261006-2240-b-encounter-skin-8bfa (silver): slack skin built in crates/encounters: 0/0 vs independent truth; setups/kick 142.3→17.1; total evals still rise 1.5×.
- 20261007-0341-second-20261006-2240-b-encounter-skin-8bfa-57c1 (silver): the setups cut converts: fleet total evals 3.6×, wall 3.0–3.7×, p95/p99 down 3–4×; max-age refresh unimplemented.
- 20261007-0621-autoresearch-f521 (silver): hoisting j's arc grid plus dropping unused acceleration terms cuts setup 1.39×, bit-identical certificates; ~20 lines.
- 20261007-0711-taleb-2e81 (gold): fleet engagement is a second ruin: Θ(n_A·n_B) store (~144 TB at 10⁶×10⁶); trigger and node guard blind; tier exactly sound.
- 20261007-1032-quant-7578 (silver): the certificate's cost is a burst, not a load: degree/body ∝ N at ρ=1/N; re-pay p99 20–80 ms at 10⁴–10⁵.
- 20261007-1234-dynamics-da90 (lead): replay completeness measured on a self-selected minority; 70–98% of unscheduled encounters are silent on the author's own stream.
- 20261007-1550-dynamics-71a5 (gold): differential precession kills the "never" certificate at t_tang = travel/Δϖ̇ (12/12); sections belong in the co-precessing frame.
- 20261007-1801-dynamics-532c (silver): coplanar pairs split by χ_t = Δa/(e₁a₁+e₂a₂); conjunction-anchored checks miss 40–97% of deep crossings; CF pays only sparse.
- 20261007-1843-dynamics-1b1f (silver): the 0.1-encounters/body/orbit attractor is dead: rate 0.105→0.247 still climbing at 800 orbits; static budgets wrong ×2.5.
- 20261007-2002-library-b2d5 (silver): practitioner lessons plus a candidate-cost law (fixed-extent slope 1.0); the dilution headline is confounded by per-band density growth.
- 20261007-2246-system-969a (silver): the law's 12+12-bit Catalogue key is a candidate tier: zero misses on 8 scenes; 2.7× median cut vs O(N).
- 20261007-2344-second-20261007-2246-system-969a-5d90 (gold): timing tier on the key window: recall 1.0, tier-2 work bit-identical; sound domain ends at e≈0.969 (206/289 missed beyond).
- 20261008-0945-taleb-48e5 (silver): radial concentration does not break the cone: cpe ≈ 1.2·a^2.6/ρ; degree tails ≤ 3.9; the ρ-adoption mechanism falsified.
- 20261008-1058-second-20261008-0945-taleb-48e5-abd7 (gold): cpe decomposes exactly as a^1.5 local clock × a^1.0 relative-ρ: ρ∝a plus per-doll clocks makes it radius-flat.
- 20261008-2113-scout-6652 (silver): the Wide window's closed-form h(λ) replacement misses zero, but its unmargined 17-sample routing falsely kills 3/6 high-e sections.
- 20261009-0401-second-20261009-0208-fermi-fe6b-90fb (gold): cascade anchored at 10⁶: pairs/kick = 0.0346·n·(1+X)/(2(X−1)); skin 0.077 cores/cell; U-index 16 GB at 10⁹.
- 20261009-0521-library-189e (gold): the CF/Diophantine conjunction calendar killed at belt scale: median rank 0.48 ≈ random; conjunctions cluster when 2e·n > |Δn|.
- 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 (gold): contact impulse validated (median 0.998 over 1091 RK4); m_crit ≈ 1.3×10⁻¹⁷ M☉; 50-m rocks never cross a tick.
- 20261009-1504-second-20261009-1345-system-136a-ca96 (gold): the Δϖ-band cache refuted as zero-miss: tolerance ≈1e-5 rad, 9.3% silent miss; the arc geometry θ_c binds.
- 20261009-1649-system-aa29 (silver): the kick resonance gate and the CF pass read one synodic rotation; the standalone detector is deletable; recall 46–92%.
- 20261009-2043-second-20261009-1936-system-8716-88ee (gold): occupants' exact mean-motion extremes make the unified index emit the naive rule: 0/0 on 23 scenes; trigger deletable.
- 20261009-2120-library-30a7 (silver): naive CF/beat next-conjunction prediction misses ~90% (fA 0.067); the "≥3× skin" prescription falsified; corroborates the calendar kill.
- 20261010-0541-dynamics-6565 (silver): belt encounters do not avalanche: corrected branching 1.01–1.11× baseline; the elastic runaway is real; τ=2 rows mislabelled.
- 20261010-1029-taleb-5c01 (gold): silent misses are a horizon-edge hole: 20.2% of true encounters; two unconditional edge checks catch every observed miss.
- 20261010-1920-autoresearch-ccc6 (silver): setup cut 1.4–2.1× and a dual-guard skin cuts kick re-cert 7377→851 µs/kick at ε1e-9, zero violations; 10–15× undelivered.
- 20261010-1947-second-20261010-1920-spacex-cb3f-f79a (gold): the same-doll pre-filter is priced out: airtight bound rejects 0.07%; exact tier ~4 µs/pair linear — do-not-spend.
- 20261011-0517-quant-d7bd (silver): PlayerNeighbourhood::find is an exact O(N) scan at 1.5–1.9 µs/body: one player event crosses the frame at ≈10⁴ bodies.
- 20261011-0736-dynamics-ec74 (silver): impulsive conjunctions valid only inside b ≲ 3 r_H; swarms a Poisson gas (λ ∝ Ψ^0.95); game swarms deletable.
- 20261011-0924-library-9834 (silver): synodic strobe: a frozen pair's indicator is a rotation-hitting sequence; three numbers per pair; 78–91% deletable — frozen only.
- 20261011-1102-second-20261011-0924-library-9834-5c16 (gold): the three-number record inverts under real kicks: amortized work 1.1–20× scanning; 43k–3.97M evals/encounter vs 38k.
- 20261011-1234-taleb-62f7 (gold): crossing packets make contacts Θ(n_A·n_B) (exponent 1.94): events are the workload; per-ship flux replaces enumeration, 0.87–1.04 of truth.
- 20261011-2132-autoresearch-a85a (silver): caching j's τ-grid and k=32→16 cuts per-kick re-certification 1.6–2.1× with identical events, zero misses everywhere.
- 20261011-2132-second-20261011-2028-system-3b42-214f (gold): the same-key straggler tier freezes as a closure-scaled arc window (cand/enc 5.3–5.6 in n); U(L)|E never turns bound.
- 20261012-1340-quant-e49d (silver): one kick's wake is O(N) (6.8 ms at 10⁴) but 98% defers by deadline; the skin cannot absorb player burns.
- 20261014-1137-fermi-1738 (awaiting grade): the 10⁹ encounter ledger audited: 90fb's per-cell constant is the partitioned total (max-rtf 5,216 reproduced), effb's ×10⁵ double-bills; the honest cube spans 0.077 to 3×10⁷ cores on cadence/topology/skin; the remaining engine lever is the contiguous belt's candidate count.
- 20261014-1221-scout-0b81 (silver): the quantum gate measured — one Q48 of E against each pair's strongest conjunction; author model: 99.96% deleted, ledger 0.5–3.1 cores; checker: the miss model is 6×10²–9×10³× too large at Δa ≤ 0.05 (Kepler-true misses quasi-periodic), corrected 95.5–97.8% and 37–369 cores — mechanism and controls stand, the budget claim does not; phase-free group certificates vacuous (1/K→0); the mass spectrum is the content dial.
- 20261014-1511-scout-f0a2 (awaiting grade): the exact tier empties at the shipped key's own Q48 (gate deletes 1.00000, survivors ≥34-km partners); the affordable gate is a birth-constant route (D* = 1.3 km, wake cut 129×, 10⁹ → 0.03–0.6 cores of routing); the one-bit floor unsound (aligned conjunctions 1.9×10⁻⁶·v_k) — pair-geometry floor + phase tier; the anchor dispute with 0b81 opened.
- 20261017-0839-inversion-2373 (inversion): the formation regime's cure is quadratic in fleet size; the phase certificate's paid occupancy law k̄ = F·(4·e_max + 0.75·da·TAU·H)/TAU verified to 3 digits.
- 20261017-1018-second-…-b509 (silver): the calendar measured: arm 1.02–1.16 µs/pair vs 57.7–414.7 exact; sound 0/0; the armed set is ρ-driven; a standing pair re-evaluated per interval costs 31 ms — store it.
- 20261018-0543-library-5567 (silver): the fleet row dead by representation: the Fermi-frame fleet carries F = 10⁵ × 10⁴ at ≤ ~1 core; checkers extended to m = 6,144 and priced the all-battle bound.
- 20261018-0932-fermi-cd3b (fermi): the belt row's event flow at 10⁹ is cheap and small (0.22 contacts/s, 1.1e3 conjunctions/s, ≤1.9 cores worst-case mint) — the row is 100% certificate churn riding the kick cadence; the stream composes to 5.3–8.4 M1 cores.
- 20261018-1025-scout-fbf9 (silver, self-suggested): the churn constant answered — 0.034 re-arms/body/kick at n = 10⁴ (∝ n² at fixed density), not 0.034·n; the term falls ~4 orders in arm-evals (checker-corrected; the author's ~6-orders headline does not reproduce); armed lists are miss-space fragile (0.5–0.75×/kick at bare B); kill test = one shipped-tier flight.
