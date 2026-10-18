topic: encounters
status: open
closed-by:
valid-while:
<<<<<<< main
updated: 20261018-1025-quant-c9c7
=======
updated: 20261018-1025-scout-fbf9

>>>>>>> 20261018-1025-scout-fbf9
# Finding encounters: the pairwise tier, the slack skin, the Binet cone

## Current best

<<<<<<< main
**[20261018-1025-quant-c9c7] The row's one missing constant is measured and it inverts the closure reading:
pairs re-checked per kick on the shipped U-scan tier is 0.484·N at the belt's own mix — the
window is SATURATED (the scan is the whole band at every N, 10⁴→10⁶, exponent 0.999; the
Rayleigh e-tail's e_max/p ≈ 0.19 exceeds the band's whole U-span 1/2−1/3 = 0.167), so the
count is linear in N and NOT O(1) even at fixed density (the fixed-density control fails its
own flatness: 0.695·N vs 0.484·N), and cells cannot bound it (reach spans ~10⁵ cells of
10⁴).** fe6b's 0.0346·n is the *unsaturated* regime: reproduced at its own spec
(0.0824→0.0843·N at 10⁴→10⁶ = 0.0346·N·(1+X)/(2(X−1)) with X = 1.52 ≈ 1.5), while the belt
mix carries 5.7× more candidates (σ_R 0.07 vs 0.01). Composed at 10⁹ rtf 100: candidate
rescans are 10⁷–10⁹ cores (scan-only floor 106 s/kick at 0.22 µs/entry; exact re-cert
4.8 µs/pair) — the rescan framing of the row is dead by 5–7 orders, and the "~10¹–10²
cores at cells of 10⁴" worry (346 pairs/kick) understates the constant 14×. The closure is
measured the same run on the flow/slack side: at the belt quantum (2⁻²³) the candidate set
is bit-stable (gained+lost ≈ 0 of ~10⁵–5×10⁵ pairs per kick), 92.3–92.5% of pairs are
slack-skippable with 0 violations (changed 1.3%; armed pairs 0.85% of candidates; n = 10⁴
and 3×10⁴, seeds 20261050 and 777), and stored slack dies at 10⁻⁵-class kicks (4.5%
skippable; 0.04% at 10⁻³) — churn reduces to cd3b's mint flow (≤1.9 cores) plus
burn-priced re-arm. Replica element tier (Binet cone, ρ = 1e-4; eps_u ∝ ρ enters reach only
at ~10⁻⁴ ≪ the 0.04–0.19 e/p terms, so the candidate law is anchor-insensitive; the arm
flow is cd3b's priced row); measured N ≤ 10⁶, extrapolated 10³× structurally (quant;
instrument `examples/churn.rs` + the parameterized shipped `kick`, `regen.sh`).
**[Checker, 20261018: reproduced bit-identically (every deterministic field; regen 38 s), and
the domain extends past the author's: σ 0.2 → 0.849·N and σ 0.4 (the shipped redraw cap) →
0.940·N — saturation deepens monotonically with dispersion, so a stirred belt worsens the
rescan verdict; n = 3×10⁶ → 0.519·N (local exponent 1.02), so the honest constant is
0.48–0.52·N (per-body e heterogeneity plus the √ln N crawl of e_max/p), not exactly 0.484;
fe6b's law confirmed at a second X ([1,2], σ 0.01: 0.050/0.053·N vs the formula's 0.0519 —
the X identification is real); the slack cliff located: 0.925 (2⁻²³) → 0.83 (3e-7) → 0.55
(1e-6) → 0.19 (3e-6) → 0.045 (1e-5), 0 violations at every rung. One label slip in
dossier/predictions (not this page): the fixed-density control's "anchor density 4×10⁴/AU²"
is the control band's own density; the 10⁶-in-[2,3) anchor is 6.4×10⁴/AU² — the control ran
at lower density and its fraction still rose, so the P2 kill is stronger than stated.]**


**[Checker 2, 20261018 (blind): every deterministic field reproduced bit-identically, 38 s.
Four independent adversarials confirm the mechanism and bound its domain: n = 3×10⁶ (out of
range) → 0.519·N, scanned still 100% (the constant crawls with e_max/p exactly as the
√ln N disclosure says — the 10⁹ rescan cost is worse than 0.484·N, not better); σ = 0.02 →
0.162·N vs the σ-linear unsaturated prediction 0.164·N (the two regimes connect as
claimed); fe6b's law at a second X ([1,2]: 0.0511·N vs 0.0519); and a 10×-wider band [2,12]
still measures 0.15–0.154·N (seeds 20261050/777) — so "NOT O(1) at fixed density" holds for
every belt-like band, and becomes O(1) only asymptotically once 2·reach < U-span, far
outside any belt geometry. The named 10⁶-pair slack probe now exists: n = 10⁵, nk = 20,
963,298 decisions, skippable 0.9219, 0 violations.]**
=======
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
>>>>>>> 20261018-1025-scout-fbf9

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

<<<<<<< main
1. **ANSWERED (20261018-1025-quant-c9c7): the constant is 0.484·N at the belt mix and the
   window is saturated** — not O(1) at fixed density, not bounded by cells; rescans are
   10⁷–10⁹ cores at 10⁹ and the row closes only on arm-by-flow + stored slack (92.5%
   skippable, 0 violations at the quantum; dead at 10⁻⁵-class kicks). What stays open on
   this branch: the rare-violation hunt (0 violations over ≤ 2.5×10⁵ pair decisions at
   n ≤ 3×10⁴; checker2 extended to 9.63×10⁵ decisions at n = 10⁵ — still 0) and the
   burn-scale re-arm price on the live word.
2. **The mint term's semantics (this run): does every b≤5×10⁵-m conjunction re-mint a key
   (1.87 cores at rtf 100), or does efd4's intern hold it near zero?** One flight with a
   mint counter on the live anchor decides.
1. **The conjunction calendar as the shipped fleet arm** (this run): wire standing contacts
   as stored state (31 ms per interval-horizon re-evaluation of a perpetual pair is the
   exact machinery's own horizon-walk), the due-queue as the only waker, and slack-deferred
   re-arm after sub-quantum kicks. One design step; every constant is now measured.
2. **The population contract for fleets** (new, from the closed row): at 10⁹ the 4-core
   budget buys F ≈ 10³ at belt kick rates; the conjunction flow (trains) and kick-created
   firings are policy terms (φ, da, kick rate) the ledger must now state — the integrator's
   call, not a certificate's.
3. (unchanged) The belt-anchor dispute f0a2 vs 2b89; the refused-train (da ≥ 4e-4) tier;
   cross-group fleet×belt routing (`7532`).
=======
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
>>>>>>> 20261018-1025-scout-fbf9

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
- 20261008-0338-redteam-4e7c (lead): GR-doll apsidal advance breaks the rotation timing and the cone; record doctored — the GR domain is untested, direction only.
- 20261008-0945-taleb-48e5 (silver): radial concentration does not break the cone: cpe ≈ 1.2·a^2.6/ρ; degree tails ≤ 3.9; the ρ-adoption mechanism falsified.
- 20261008-1058-second-20261008-0945-taleb-48e5-abd7 (gold): cpe decomposes exactly as a^1.5 local clock × a^1.0 relative-ρ: ρ∝a plus per-doll clocks makes it radius-flat.
- 20261008-2031-dynamics-87da (lead): the pair-timing rotation identity is real (2.7e-10) but the 95–98% "never" tables are uniform-sampling artifacts.
- 20261008-2113-scout-6652 (silver): the Wide window's closed-form h(λ) replacement misses zero, but its unmargined 17-sample routing falsely kills 3/6 high-e sections.
- 20261009-0401-second-20261009-0208-fermi-fe6b-90fb (gold): cascade anchored at 10⁶: pairs/kick = 0.0346·n·(1+X)/(2(X−1)); skin 0.077 cores/cell; U-index 16 GB at 10⁹.
- 20261009-0521-library-189e (gold): the CF/Diophantine conjunction calendar killed at belt scale: median rank 0.48 ≈ random; conjunctions cluster when 2e·n > |Δn|.
- 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 (gold): contact impulse validated (median 0.998 over 1091 RK4); m_crit ≈ 1.3×10⁻¹⁷ M☉; 50-m rocks never cross a tick.
- 20261009-1345-system-136a (silver): quantized (periapsis,k) buckets are a conservative cone index (zero misses, superset ×1.02–1.49); Δϖ-band caches amortize ×43–312.
- 20261009-1504-second-20261009-1345-system-136a-ca96 (gold): the Δϖ-band cache refuted as zero-miss: tolerance ≈1e-5 rad, 9.3% silent miss; the arc geometry θ_c binds.
- 20261009-1649-system-aa29 (silver): the kick resonance gate and the CF pass read one synodic rotation; the standalone detector is deletable; recall 46–92%.
- 20261009-1858-library-c716 (silver): time-priority τ book: static keys miss 99%; τ frac≤4 is 0.6–0.8; the O(N·k) gain is asserted, not measured.
- 20261009-1936-system-8716 (silver): the cone ∧ wrap(Δλ₀) rule unifies the tiers, recall 1.0 — but its ΔU-linearized index misses 66/495 on bimodal-e belts.
- 20261009-2043-second-20261009-1936-system-8716-88ee (gold): occupants' exact mean-motion extremes make the unified index emit the naive rule: 0/0 on 23 scenes; trigger deletable.
- 20261009-2120-library-30a7 (silver): naive CF/beat next-conjunction prediction misses ~90% (fA 0.067); the "≥3× skin" prescription falsified; corroborates the calendar kill.
- 20261009-2212-dynamics-79ef (silver): stirred-belt rate decays λ∝t^-0.25, collapsing to λ=0.345·e^-0.215; mildly self-exciting (b≈0.35, subcritical); tails 1.8× Poisson.
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
- 20261009-0401-second-20261009-0208-fermi-fe6b-90fb (gold): cascade anchored at 10⁶: pairs/kick = 0.0346·n·(1+X)/(2(X−1)); skin 0.077 cores/cell; U-index 16 GB at 10⁹. *[20261014-1137: the per-cell label corrected — 0.966/0.077 is the partitioned total; the law, anchor and verify controls all stand.]*
- 20261014-1137-fermi-1738 (awaiting grade): the 10⁹ encounter ledger audited: 90fb's per-cell constant is the partitioned total (max-rtf 5,216 reproduced), effb's ×10⁵ double-bills; the honest cube spans 0.077 to 3×10⁷ cores on cadence/topology/skin; the remaining engine lever is the contiguous belt's candidate count.
- 20261014-1221-scout-0b81 (silver): the quantum gate measured — one Q48 of E against each pair's strongest conjunction; author model: 99.96% deleted, ledger 0.5–3.1 cores; checker: the miss model is 6×10²–9×10³× too large at Δa ≤ 0.05 (Kepler-true misses quasi-periodic), corrected 95.5–97.8% and 37–369 cores — mechanism and controls stand, the budget claim does not; phase-free group certificates vacuous (1/K→0); the mass spectrum is the content dial.
- 20261014-1511-scout-f0a2 (awaiting grade): the exact tier empties at the shipped key's own Q48 (gate deletes 1.00000, survivors ≥34-km partners); the affordable gate is a birth-constant route (D* = 1.3 km, wake cut 129×, 10⁹ → 0.03–0.6 cores of routing); the one-bit floor unsound (aligned conjunctions 1.9×10⁻⁶·v_k) — pair-geometry floor + phase tier; the anchor dispute with 0b81 opened.
- 20261006-1029-dynamics-6875 (silver): endogenous kicks hold work at 2.3–3.6×10⁵ evals per real encounter; the steady state does not exist.
- 20261006-1135-spacex-317c (gold): skin windows as ρ-level sets at ρ_eff = ρ+1.5·s·r²max: exact at s=4·eps_u; setups/kick 14.95 vs 188.6.
- 20261006-1249-library-8f99 (silver): skin width must follow per-pair precession; the 55× resonance-split headline is confounded.
- 20261006-1436-autoresearch-cdf8 (lead): both claims die, but a real engine bug: hit()'s cross·cross overflows i128.
- 20261006-1436-scout-eab7 (silver): element-space skin makes setup track churn; envelope unsound in churn at κ 1e-3.
- 20261007-0621-autoresearch-f521 (silver): hoisting j's arc grid plus dropping unused acceleration terms cuts setup 1.39×, bit-identical certificates.
- 20261007-0711-taleb-2e81 (gold): fleet engagement is a second ruin: Θ(n_A·n_B) store (~144 TB at 10⁶×10⁶); trigger and node guard blind.
- 20261007-1234-dynamics-da90 (lead): replay completeness measured on a self-selected minority; 70–98% of unscheduled encounters are silent.
- 20261007-1550-dynamics-71a5 (gold): differential precession kills the "never" certificate at t_tang = travel/Δϖ̇; sections belong in the co-precessing frame.
- 20261007-1801-dynamics-532c (silver): coplanar pairs split by χ_t = Δa/(e₁a₁+e₂a₂); conjunction-anchored checks miss 40–97% of deep crossings.
- 20261007-1843-dynamics-1b1f (silver): the 0.1-encounters/body/orbit attractor is dead: rate 0.105→0.247 still climbing at 800 orbits.
- 20261007-2002-library-b2d5 (silver): practitioner lessons plus a candidate-cost law (fixed-extent slope 1.0); the dilution headline is confounded.
- 20261007-2344-second-20261007-2246-system-969a-5d90 (gold): timing tier on the key window: recall 1.0, tier-2 work bit-identical; sound domain ends at e≈0.969.
- 20261008-0338-redteam-4e7c (lead): GR-doll apsidal advance breaks the rotation timing and the cone; record doctored — the GR domain is untested.
- 20261008-0945-taleb-48e5 (silver): radial concentration does not break the cone: cpe ≈ 1.2·a^2.6/ρ; degree tails ≤ 3.9.
- 20261008-1058-second-20261008-0945-taleb-48e5-abd7 (gold): cpe decomposes exactly as a^1.5 local clock × a^1.0 relative-ρ.
- 20261008-2031-dynamics-87da (lead): the pair-timing rotation identity is real but the 95–98% "never" tables are uniform-sampling artifacts.
- 20261009-0521-library-189e (gold): the CF/Diophantine conjunction calendar killed at belt scale: median rank 0.48 ≈ random.
- 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 (gold): contact impulse validated (median 0.998 over 1091 RK4); m_crit ≈ 1.3×10⁻¹⁷ M☉.
- 20261009-1345-system-136a (silver): quantized (periapsis,k) buckets are a conservative cone index; Δϖ-band caches amortize ×43–312.
- 20261009-1504-second-20261009-1345-system-136a-ca96 (gold): the Δϖ-band cache refuted as zero-miss: 9.3% silent miss.
- 20261009-1649-system-aa29 (silver): the kick resonance gate and the CF pass read one synodic rotation; the standalone detector is deletable.
- 20261009-1858-library-c716 (silver): time-priority τ book: static keys miss 99%; τ frac≤4 is 0.6–0.8.
- 20261009-2043-second-20261009-1936-system-8716-88ee (gold): occupants' exact mean-motion extremes make the unified index emit the naive rule: 0/0 on 23 scenes.
- 20261009-2120-library-30a7 (silver): naive CF/beat next-conjunction prediction misses ~90%; corroborates the calendar kill.
- 20261009-2212-dynamics-79ef (silver): stirred-belt rate decays λ∝t^-0.25, collapsing to λ=0.345·e^-0.215; mildly self-exciting.
- 20261010-0541-dynamics-6565 (silver): belt encounters do not avalanche: corrected branching 1.01–1.11× baseline.
- 20261010-1920-autoresearch-ccc6 (silver): dual-guard skin cuts kick re-cert 7377→851 µs/kick at ε1e-9, zero violations.
- 20261010-1947-second-20261010-1920-spacex-cb3f-f79a (gold): the same-doll pre-filter is priced out: rejects 0.07%; exact tier ~4 µs/pair linear.
- 20261011-0517-quant-d7bd (silver): PlayerNeighbourhood::find is an exact O(N) scan at 1.5–1.9 µs/body.
- 20261011-0736-dynamics-ec74 (silver): impulsive conjunctions valid only inside b ≲ 3 r_H; swarms a Poisson gas.
- 20261011-0924-library-9834 (silver): synodic strobe: a frozen pair's indicator is a rotation-hitting sequence; 78–91% deletable — frozen only.
- 20261011-1102-second-20261011-0924-library-9834-5c16 (gold): the three-number record inverts under real kicks: amortized work 1.1–20× scanning.
- 20261011-1234-taleb-62f7 (gold): crossing packets make contacts Θ(n_A·n_B) (exponent 1.94): per-ship flux replaces enumeration, 0.87–1.04 of truth.
- 20261011-2132-autoresearch-a85a (silver): caching j's τ-grid and k=32→16 cuts per-kick re-certification 1.6–2.1× with identical events.
- 20261011-2132-second-20261011-2028-system-3b42-214f (gold): the same-key straggler tier freezes as a closure-scaled arc window.
- 20261009-0401-second-20261009-0208-fermi-fe6b-90fb (gold): *[20261014-1137: the per-cell label corrected — 0.966/0.077 is the partitioned total; the law, anchor and verify controls all stand.]*
- 20261014-1137-fermi-1738 (awaiting grade): the 10⁹ encounter ledger audited: the honest cube spans 0.077 to 3×10⁷ cores; the remaining engine lever is the contiguous belt's candidate count.
- 20261014-1221-scout-0b81 (silver): the quantum gate measured — author model 99.96% deleted / 0.5–3.1 cores; checker: the uniform miss model is 10²–10⁴× too large, corrected 95.5–97.8% and 37–369 cores; phase-free group certificates vacuous (1/K→0).
- 20261014-1511-second-20261014-1221-scout-0b81-277d (silver, this run): the checker's gold experiment done exactly — Kepler-true yield 95.5–98.0% (validated +0.02% vs brute), r_event 480–700 ns x86, f_r 0.017–0.025 event-scheduled vs 5–7 per-refresh (killed), ledger 62–571 cores: ceiling 14–24×, flux split mandatory; all-10-km control 0.003; real-mass ×52 → 0.377.
- 20261014-1221-scout-0b81 (silver): the quantum gate measured — one Q48 of E against each pair's strongest conjunction; mechanism and controls stand; phase-free group certificates vacuous (1/K→0); the mass spectrum is the content dial.
- 20261014-1511-scout-f0a2 (awaiting grade): the exact tier empties at the shipped key's own Q48 (legacy E anchor); the affordable gate is a birth-constant route (D* = 1.3 km, wake cut 129×, 10⁹ → 0.03–0.6 cores of routing); the one-bit floor unsound. *[Live-path anchor measured 20261017: the shipped binding stores no E — see this run's Refuted.]*
- 20261014-1511-second-20261014-1221-scout-0b81-277d (silver): the checker's gold experiment done exactly — Kepler-true yield 95.5–98.0% (validated +0.02% vs brute), r_event 480–700 ns x86, f_r 0.017–0.025 event-scheduled vs 5–7 per-refresh (killed), ledger 62–571 cores: ceiling 14–24×, flux split mandatory; all-10-km control 0.003; real-mass ×52 → 0.377.
- 20261017-0839-fermi-2b89 (fermi, this run): the live anchor measured — ev = −73, quantum 3.17e-14 m/s, every Dohnanyi conjunction fires and mints a key from 2¹¹–2¹² quanta; the exact tier is full on the live path; 10⁹ closes on the flux accumulator at every width; the anchor is a word-width dial (5–15 bits between 277d's and f0a2's worlds).
- 20261017-0839-inversion-2373 (inversion, silver): the phase certificate's k priced — quadratic in F for every fleet with shape dispersion, 36–4,500 cores at 10⁹ fleets; the composed ledger's encounter row is population-dependent and missing.
- 20261017-1018-second-20261017-0839-inversion-2373-b509 (second, pending grade): the
- 20261018-0543-library-5567 (library): the fleet row dies by representation — the shipped Fermi-frame fleet carries F=10⁵×10⁴ at ≤ ~1 core (0.89 µs/member/game-s measured, member-flat slices, scale-free epoch composition); dissolution at spread > r_p/32 measured; three wiring debts named.
- 20261018-0932-fermi-cd3b (fermi): the belt row's event flow at 10⁹ is cheap and small (0.22 contacts/s, 1.1e3 conjunctions/s, ≤1.9 cores worst-case mint) — the row is 100% certificate churn riding the kick cadence; the stream composes to 5.3–8.4 M1 cores.
- 20261018-1025-quant-c9c7 (quant): the churn constant measured — 0.484·N candidates/kick at the belt mix, window saturated by the e-tail (fe6b's 0.0346·n is the unsaturated regime, X ≈ 1.5); rescans 10⁷–10⁹ cores at 10⁹; slack 92.5% skippable, 0 violations at the quantum.
- 20261017-0839-inversion-2373 (inversion): the formation regime's cure is quadratic in fleet size; the phase certificate's paid occupancy law k̄ = F·(4·e_max + 0.75·da·TAU·H)/TAU verified to 3 digits.
- 20261017-1018-second-…-b509 (silver): the calendar measured: arm 1.02–1.16 µs/pair vs 57.7–414.7 exact; sound 0/0; the armed set is ρ-driven; a standing pair re-evaluated per interval costs 31 ms — store it.
- 20261018-0543-library-5567 (silver): the fleet row dead by representation: the Fermi-frame fleet carries F = 10⁵ × 10⁴ at ≤ ~1 core; checkers extended to m = 6,144 and priced the all-battle bound.
- 20261018-1025-scout-fbf9 (silver, self-suggested): the churn constant answered — 0.034 re-arms/body/kick at n = 10⁴ (∝ n² at fixed density), not 0.034·n; the term falls ~4 orders in arm-evals (checker-corrected; the author's ~6-orders headline does not reproduce); armed lists are miss-space fragile (0.5–0.75×/kick at bare B); kill test = one shipped-tier flight.
