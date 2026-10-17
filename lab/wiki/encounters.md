topic: encounters
status: open
closed-by:
valid-while:
updated: 20261017-1018-second-20261017-0839-inversion-2373-b509
# Finding encounters: the pairwise tier, the slack skin, the Binet cone

## Current best

**The live-path belt anchor is 2b89's velocity word (60-bit-relative, ev = −73, quantum
3.17×10⁻¹⁴ m/s): at it every Dohnanyi conjunction fires the word and mints a compiled key
within b ≲ 5×10⁵ m of 70-m partners, the gate deletes 0%, the exact tier is FULL, and the
10⁹ budget closes on the flux accumulator at every word width; the anchor is a dial
(coarsening 5–15 bits revives f0a2's empty-tier world) — belt-side, untouched by the fleet
row below.**


**[Conflict resolved on the fleet row, 20261017-1018-second: the calendar is measured, it is
sound, it deletes the sweep — and the fleet term it leaves is the population's own conjunction
flow, so the ledger row closes as a constraint on fleets, not on certificates.]** The r8-v2
conjunction calendar already exists in shipped code (`tier::arm_pair`: the `dioph.rs`
first-hit schedule, returning `(armed, due)` with `due` = first in-window passage, possibly
beyond the horizon = slack). Measured on it (`examples/fleetcal.rs`, print-only, decisive
seed 20261017, held-out 777, both reproduce): the arm test costs **1.02–1.16 µs/pair** vs the
exact check's **57.7 µs at one-interval horizon and 414.7 µs at the 8-interval rebuild
horizon** (57×–370×) — and the sweep price that 2373 composed (3.24 µs/pair) was measured at
a 1-orbit horizon no sound 8-interval rebuild can use, so its 36/383/4,500 cores understated the shipped sweep by 129–143×. The calendar is **sound**: 0 dropped, 0 added against
`group_events` on keys and train fleets at both seeds, while the negative controls (safety
0.9/0.5, reach halved) drop 59–6,492 events — the instrument can fail. Keys-fleet capability
is a birth constant as 2373 proposed, **but it is ρ-driven, not σ_e-driven**: armed pairs =
54/4,775/477,050 at F=10³/10⁴/10⁵ (σ_e = 1e-2) and 4,708 at σ_e = 1e-3 (same within 2%),
while the sweep's window shrinks 10× — so tightening formations does not shrink the calendar
floor. The one-period capability evaluation costs 27–51 µs per armed pair; evaluating a
perpetual (same-period) armed pair at interval horizon costs **31 ms** (102,757 exact evals:
the shipped exact machinery walks every orbit of horizon per standing pair) — a standing
contact must be a stored state, never a per-interval re-check. Trains (da = 1e-4) are a
conjunction machine: 9.41 M pairs fire in interval 0 at F = 10⁴ (26% of the 36.2 M window
pairs; 6.80 M at interval 10, 0.72× iv0 — direct re-arm, the pre-registered K4 fallback), each firing 21–34 µs; da = 1e-3 refuses
(reach 21.3 ≥ π, the H* law) so the calendar inherits exactly 2373's refused-train tree ruin.
Kicks: a belt-quantum kick (2⁻²³) moves the median pair's due by < 10⁻³ intervals (slack is
real, re-arm deferrable) but **creates 16.8 (keys) / 1,924 (train; 777: 1,862) newly-armed
pairs per kick** — undelayable real events; the row re-arm itself is 1.1 ms (keys) / 16 ms
(train) per kick if slack is ignored. **Composed at 10⁹ (φ = 1, L = 100-interval fleet
lifetime): keys
calendar birth = 0.95 / 10.1 / 118 cores at F = 10³/10⁴/10⁵ (L = 100) → F* ≈ 4,100 (L = 25:
≈ 1,050; F = 10³ fits at L ≥ 25: 3.8 cores) — ~40× the sweep's ~124, but not 10⁵. [Checker-2:
compose.py's `** 0.5` interpolation assumed a term ∝ F², but the measured term runs ∝ F^1.03–1.07
(0.95→10.08→118.08 cores per decade); the honest refit gives 4,100/1,050, not 6,463/3,232.] The train firing flow alone is 51,344 cores at F = 10⁴ (the
term is ∝ F: no da = 1e-4 train fleet size fits at φ = 1, F* < 1 — stronger than the author's F* ≈ 89), and the kick-created conjunctions at the belt's own 2 events/body/interval
are ~2,500–3,300 cores at any F (keys; ~290,000 train). So the missing ledger row closes with numbers on both sides:
**certificate* term F* ≈ 1.1–4.1 k at L = 25–100 for uniform-phase keys fleets (calendar, slack, standing contacts), and *population*
terms — the conjunction firing flow and kick-created firings — that no certificate deletes
(PRINCIPLES #3: they are the surprises). The 4-core budget at 10⁹ buys uniform-phase keys fleets of ~10³ ships now (birth fits at L ≥ 25) and up to
~4×10³ if fleets live 100 intervals, at belt-like kick rates, or larger ones only if fleets are quiet (φ·kick-rate policy).
**Clustered formations (σ_l ≲ reach — the battle-group shape of taleb-09b5) are the exception: the
birth arm pass pays a near-complete-graph window (checker-2 A5: 1.999 M window pairs at F = 2,000,
σ_l = 0.02, sound 0/0), so the calendar's F* there is ≈ 200 (L = 100; ≈ 50 at L = 25) — barely above
the sweep's ~124. The 65× lift is a uniform-phase result.** [Checker-2 also flags: the dossier's
"2.4×10⁸ cores under per-interval re-check" is an arithmetic slip — the measured 31.7 ms × 4,775 armed
at F = 10⁴ composes to 5.4×10⁴ cores; the conclusion (standing contacts must be stored state) stands.]
The belt-anchor dispute below (f0a2 vs 2b89's velocity word) is untouched by this run: both
priced rock belts.
(Domain of the fleet rows: planar-Kepler replicas, e ≤ 0.5, soundness gates at F = 2,000,
H = 100 orbits — checker-extended to clustered formations (σ_l = 0.05/0.01, 379k–473k
events, 0 dropped), clustered trains and a σ_e = 0.2 fleet, seed 31337, all 0/0; the event
exponent holds at the next decade, γ = 2.00 on (12,800, 25,600); checker-2, seed 424242:
H = 500 orbits, bimodal two-key fleets, clustered σ_l = 0.02 with σ_e = 0.05 at H = 200, the
refusal boundary da = 1.2/1.4e-4 (reach 2.70/3.13 < π, not refused), and eps = 1e-2 kicks
(83 firings/kick, ddue ~4 iv — slack dies at burn-scale kicks) — all 0/0 sound.)
**The formation regime's cure is itself quadratic in fleet size, and the composed 10⁹
ledger carries no term for it (20261017-0839-inversion-2373, inversion; its calendar-fix
proposal is now measured above).** The shipped phase certificate's paid occupancy follows
k̄ = F·(4·e_max + 0.75·da·TAU·H)/TAU — the reach law verified to 3 digits on shipped
`phase.rs` across three decades of F (pred/measured 0.999–1.009, checker-verified at three
seeds) — so the arm pays F²·reach/TAU exact-checked pairs per rebuild. [Checker: the
mechanism — occupancy = density × reach, quadratic when dispersion > ρ — is already measured
on this same build by coorbital-cert's `74a1`/`4ec3` (Θ(n²) at zero encounters, reach =
dispersion × horizon), `5ffb` (0.19–0.45·n² pairs, the cost-blind reach<π trigger),
`c5ab`/`a110` (required rank ~n·σe); this run's additions are the closed-form law, three
decades of F, the refusal boundary H*, and the 10⁹ composition.] The quadratic is driven by
shape dispersion (e/pom spread) or a-spread over a standing horizon, not by radial excursion
per se: a coherent-shape fleet (identical e, pom — the shipped cancellation path,
checker-measured) pays mean_k 0.38 at F = 10⁴, flat in H; one δe kick restores the quadratic
(`c5ab`). mean_k 50/532/6,257 at F = 10³/10⁴/10⁵ (keys fleets, σ_e = 1e-2, uniform phases),
clusters at 97.6–98.9% of the complete graph, trains' k growing linearly with standing
horizon until refusal at H* = (π−w₀)/(0.75·TAU·da) ≈ P_syn/2 where the tree tier carries 96%
of F²/2 as candidates — while the ANSWER stays rank-0 (distance-rank is ρ-bounded and cannot
fail — coorbital-cert `b292`, `7532`; a control, not a result). Composed at 10⁹ (φ = 1,
checked pairs 3.24 µs x86, rebuild every 8 intervals): 36/383/4,500 cores at F =
10³/10⁴/10⁵; F* ≈ 100 at σ_e = 1e-2 (∝ 1/σ_e) — **now superseded on the certificate side by
the calendar row above, which also reprices this run's sweep basis (see the 129–143× horizon
correction).**

**[Prior best retained: f0a2 and 277d's replica measurements, both on their own anchors —
f0a2: at the legacy key's Q48 the gate deletes 1.00000, survivors ≥ 34-km partners,
affordable form a birth-constant route (D* = 1.3 km at the contact-charge floor, wake cut
129×, routing 0.03–0.6 cores at window prices), the one-bit floor unsound (aligned
conjunctions 1.9×10⁻⁶ v_k); 277d: Kepler-true yield 95.5–98.0% at the binding-relative
anchor, r_event 480–700 ns x86, f_r = 0.017–0.025 event-scheduled vs 5–7 per-refresh
(killed), ledger 62–571 cores — mechanism and controls stand; both ledgers are
anchor-conditioned, and neither anchor is the live word; see 2b89's velocity-word paragraph
above for the live-path anchor.]**

## Refuted

- Per-rebuild window sweeping as the fleet representation: deleted by the calendar row above
  (57–370× per pair, lifetime-amortized) — `20261017-1018-second-…-b509`.
- The steady-rate-by-first-due-histogram reading of the calendar: in-window passages come in
  bursts (consecutive dues one period apart during a window transit); only direct re-arm at a
  far interval gives the rate — `20261017-1018-second-…-b509` (K4, pre-registered).
- "F* ∝ 1/σ_e" as a property of the fleet floor: the calendar's armed set is ρ-driven
  (4,775 vs 4,708 at σ_e = 1e-2 vs 1e-3, F = 10⁴); only the sweep's window is σ_e-driven —
  `20261017-1018-second-…-b509`.

## Open directions

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

## Contradictions

- f0a2's "gate deletes 1.00000" vs 2b89's "every Dohnanyi conjunction fires the word":
  anchor-conditioned (legacy E-key vs live velocity word); unresolved, belt-side only.
- (resolved by this run) 2373's "calendar required, price unknown" — now priced: it deletes
  the sweep and leaves the population flow.

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
