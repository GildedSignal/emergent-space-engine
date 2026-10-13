topic: encounters
status: open
closed-by:
valid-while:
updated: 20261012-1827-q-wiki-encounters-e8e3

# Finding encounters: the pairwise tier, the slack skin, the Binet cone

## Current best

**The pairwise tier is exactly sound everywhere measured except two named holes, its cost follows measured laws, and the one standing lever is the slack skin.** The shipped tier (cone candidates → `sections` → Diophantine first-hit → exact check, `crates/encounters`) is built but not wired into the plane (H0216).

**Cost laws (cone tier).** Candidate work per real encounter is `cpe ≈ 1.2–1.3·a^2.53/ρ`, decomposing exactly as a^1.5 local clock × a^1.0 relative-ρ; carrying ρ ∝ a and per-doll (local-orbit) time makes work per encounter radius-flat, residual exponent 0.000 over a 100× ladder (`48e5`, `abd7`). Radial concentration does not break it: degree tail max/mean ≤ 3.9, N-linear, per-kick setup f·N with f = 0.10–1.0 (`48e5`). At 10⁶ the kick→certificate cascade is the only term near a core (0.966 no-skin / 0.077 with skin cores per 10⁴-cell, M1-implied), with measured law `pairs/kick = 0.0346·n·(1+X)/(2(X−1))` (anchor 812.8 at the belt cell): 10⁹ in one belt costs 2×10⁴–10⁵ cores, so the billion partitions into ~10⁵ cells of ~10⁴ bodies — and the global U-index itself does not fit (16 GB at 10⁹) (`90fb`). The cost is a burst, not a load: degree/body ∝ N even at ρ = 1/N, re-pay p99 ≈ 20 ms at N = 10⁴ / 80 ms at 10⁵ single-threaded (`7578`).

**The slack skin (the lever).** 92% of per-kick evals are numeric-window *setup*, so dormant-pair deferral is dead (ceiling 1.1–1.2×; analytic zero-setup windows over-fire 427×) and the lever is setup-skipping (`4643`). Built and sound: windows as ρ-level sets at ρ_eff = ρ + 1.5·s·r²max are exact at s = 4·eps_u — 0 missed / 0 false, setups/kick 14.95 vs always's 188.6 (`317c`, the 12.6× of q-skin, 2 Oct) — and the built `skin.rs` cuts setups/kick 142.3→17.1 at 0/0 against independent truth (`8bfa`), converting to total-evals cuts: fleet 3.6×, wall 3.0–3.7×, p95/p99 down 3–4× (`57c1`); a dual-guard variant cuts kick re-cert 7377→851 µs/kick (8.7×) at ε 1e-9 with zero violations (`ccc6`); τ-grid caching 1.6–2.1× (`a85a`); arc-grid hoisting 1.39× bit-identical (`f521`). The skin's law: the cut equals the mean cache lifetime τ = slack·eps_u·32/((e/p)·g) (42.5× at 0.057 rad/orbit; τ ≈ 2.2e3–1.1e5 epochs at real belt rates) (`73f0`); slack/widen must be sized from the law's precession — slack 0.5/widen 2 misses 5/459 at 0.19 rad/orbit, widen 6 or slack 0.1 restores soundness, widen 12 breaks the exact check (`73f0`); width is per-pair precession, not a resonance split (`8f99`). Boundaries: at 100× the plane's kicks the sound skin costs more than it saves (`317c`); the max-age refresh is unimplemented (`57c1`); the queued skin cannot absorb player burns (skippable 94.6% at δa/a 1e-9 but 0.25% at 1e-3, unsound there) (`e49d`).

**Soundness holes, both with one-step fixes.** (1) *Horizon edge:* encounters in progress at horizon open/close are silently dropped — 20.2% of true encounters (284/1407) on a dilute fleet, the dropped set pinned to the two edges while truth grows 6×; two unconditional t=0/t=H edge checks catch every observed miss (`5c01`; this falsifies `8af8`'s "0 missed on every scene" — its truth shared the blind axis). (2) *High e:* the shipped fixed-k check misses 5.4–7.1% at e ∈ [0.60, 0.95] — `make_belt` caps e at 0.5, so frozen verify sets never looked there (`8cee`); the 12+12-bit Catalogue-key window's sound domain ends at e ≈ 0.969, where the pad's 1/g term crosses periapsis (206/289 missed at e ∈ [0.95, 0.985]; one-line inner-edge fix) (`969a`, `5d90`). Also: differential apsidal precession kills the standing "never" certificate at t_tang = (distance to orbit-tangency)/Δϖ̇ — every realized encounter lands after its tangency (12/12) — so sections must live in the pair's co-precessing frame, an O(1) angle update per pair; it matters at p ≈ 50 M (40–400 orbits), not in the weak field (`71a5`). Found engine bug: `hit()`'s cross·cross overflows i128 and reports phantom encounters (all 19 plane contacts in one scene) (`cdf8`, lead — the run's own claims died, the bug is real). Untested: a GR doll's apsidal advance breaks the circle-rotation timing and the cone (`4e7c`, lead; direction only, record doctored).

**The player seam.** `PlayerNeighbourhood::find` is an exact O(N) clone-and-eval scan at 1.5–1.9 µs/body: one player event crosses the whole 16.7 ms frame at ≈10⁴ bodies (`d7bd`). A provably-safe same-doll pre-filter is priced out — the only airtight bound rejects 0.07% of pairs; the exact tier is ~4 µs/pair, linear in population (~4 s per player item at 10⁶ same-doll bodies): the deletion belongs to phase certificates at the seam, not per-pair filters (`f79a`). One kick's wake in the cone tier is O(N) single-thread (6.6–6.9 ms at N = 10⁴, slope ~1.04; a full frame at N ≈ 2.4×10⁴), but 98% of it (window setups) has deadlines ≥ tens of orbits away — deadline-ordered scheduling turns the burst into a stream; only the cone re-scan (1.3–2.1%) must land in the kick's frame; the deadline must be phase-aware (1/|Δn| is the synodic period: 11.3% of pairs first conjunct within 10 orbits) (`e49d`).

**Structural ruins and their escapes.** Co-orbital concentration is the sibling page's ruin (`coorbital-cert`). Two more live here. *Fleet engagement* (two tight swarms on crossing orbits): 100% cross-pair saturation, 2 analytic Cross sections per pair, 0 numeric setup evals — a Θ(n_A·n_B) store (~144 TB at 10⁶×10⁶) that neither the clump trigger (cross Binet separation 0.29 vs eps_u 3.9e-4) nor a node-interchange guard (p50 6.3e-2, ~630× the ρ/v_rel window) can cheapen, while the tier is exactly sound there (0/0 over 40,000 pairs; 51–55 evals/hit flat in n) (`2e81`). The escape, measured: when concentrated packets cross, contacts are Θ(n_A·n_B) (exponent 1.94, per-pair p ≈ 0.021 flat) — the events themselves are the workload and no discovery certificate can help — so one aggregate event per packet crossing replaces enumeration: per-ship flux λ_i = ρ_B·2R·L_i through the opposing packet's density grid, O(n) at 257·(n_A+n_B) evals, zero free parameters, totals 0.87–1.04 of exact truth (`62f7`). *Tier routing*: coplanar pairs split by the crossing fraction χ_t = Δa/(e₁a₁+e₂a₂) (exact identity, 0 violations in 166k pairs); conjunction-anchored checks (radial, Öpik) miss 40–97% of true close approaches in deep crossing, so per-pair synodic CF pays only where ν = W·ε ≪ 1 and the deep tier routes to the phase-neighbour mechanism (`532c`).

**Candidate-tier shape.** The law's own 12+12-bit Catalogue key is a conservative candidate tier: one key-sorted list, zero window misses on 8 scenes incl. precessing rosettes, kick maintenance local (median 2 cells), 2.7× median cut vs the O(N) Cartesian scan (`969a`); stacked with the shipped timing tier it recalls every fine-truth encounter in the sound domain with tier-2 work bit-identical and key-only breadth free, passing r8 v4's frozen gates (1.400/1.296 ≤ 2.0; 1.10 checks/hit ≤ 1.5) (`5d90`). Quantized (periapsis, k) buckets are a conservative cone index (zero misses, superset ×1.02–1.49) (`136a`) — but their Δϖ-band section cache is refuted as zero-miss: tolerance ≈ 1e-5 rad, 9.3% of encounters silently missed at the fine band, window widening useless (the arc geometry θ_c binds; only re-setup recomputes it) (`ca96`). One unified rule — `cone ∧ wrap(Δλ₀) ≤ |Δn|(1+3ē²)H + 5(eᵢ+eⱼ) + skin` on one U-sorted scan — deletes the concentration trigger, the second certificate and the fleet category; its index must bound each slow-band bin's |Δn| by its occupants' exact mean-motion extremes, which makes it emit exactly the naive per-pair rule (0 drops/adds over 23 scene-instances, recall 1.0; belt evals +28–90%) (`8716`, `88ee`). Killed shortcuts: the CF/Diophantine next-conjunction calendar (median percentile rank 0.48 ≈ random, exact-window hit ≤ 7.6%; conjunctions cluster whenever 2e·n > |Δn| — ~90% of belt pairs; only weak recurrence survives, miss 0.48–0.67× median at the best convergent offset) (`189e`, `30a7`); the three-number synodic-strobe record (its 33–146× inverts under real kicks to a 1.1–20× loss, 96× at ε 1e-4; 43k–3.97M evals per real encounter vs scanning's 38–41k) (`9834`, `5c16`); the time-priority τ book (static keys miss 99%; the O(N·k) gain asserted, not measured) (`c716`).

**Load and the steady state (allocator inputs).** "No work per orbit in the steady state" is false under endogenous kicks: elastic stirring keeps a kick floor and certificate re-setup churn runs 15–50× real encounters at the m=16 grid (`43d5`, `6875`); the 0.1-encounters/body/orbit "attractor" is dead — rate 0.105→0.247 still climbing between orbits 400 and 800 — so a static encounter budget is wrong by >2.5× in one session (`1b1f`); instead rates decay as λ ∝ t^-0.25 with e_rms ∝ t^0.4, collapsing to λ = 0.345·e^-0.215, mildly self-exciting (b ≈ 0.35, subcritical; tails ≈ 1.8× Poisson) (`79ef`); no avalanche — corrected branching 1.01–1.11× baseline (`6565`). Swarms on Ψ = μ_g/(aσ_e)³: a Poisson gas (λ ∝ Ψ^0.95) ending at a birth-burst/capture regime; real game swarms sit at Ψ ≲ 10⁻⁶ where mutual encounters are deletable; the impulsive-conjunction representation is valid only inside b ≲ 3 r_H (`ec74`).

**The event itself.** A flyby must be an event entered by analytic detection at ≥ 1.5·SOI (wired as the doll door), after which the plane's in-doll rule holds B13's 1% gate (15/15, worst 2.4e-3, 65–120 events flat in e_h; star-doll cadence 0/60, one-event Öpik ≤ 7/41) (`4ea2`). The contact impulse coefficient is validated on the crate's own truth encounters (measured/predicted median 0.998 over 1091 RK4 runs; the prior (2/3)·2atan(μ/qv²) form ~18× high and cosψ-blind), giving m_crit ≈ 1.3×10⁻¹⁷ M☉ (~1.35-km rock) — below it, belt encounters never cross a period tick (0/1000 50-m rocks in 1.7×10⁴ orbits) (`c7eb`). The kick layer's resonance gate and the encounters CF pass read the same synodic rotation, so the standalone frequency detector is deletable as a pairwise gate — recall 46–92%, not the claimed 94–98% (`aa29`).

**Domain.** All of it is planar-Kepler replicas on Linux/x86 (orders of magnitude only; the integrator re-measures on the M1), n ≤ 10⁶ anchored (arithmetic beyond), scan cohorts to 3×10¹⁰; the tier is not yet wired into the plane's runtime (H0216); 3-D inclination, kick-perturbed λ(t) and the GR doll are untested in every run here (`4e7c`, flagged also by the coorbital page).

## Refuted

- Dormant-pair deferral (the taleb-3ec1 lead): 92% of per-kick evals are setup; ceiling 1.1–1.2×; analytic windows over-fire 427× (`4643`).
- The CF/Diophantine conjunction calendar (board lead, 30 Sept): loses to random at belt scale (`189e`, `30a7`).
- The three-number synodic-strobe record: inverts to a 1.1–20× loss under real kicks (`9834` → `5c16`).
- The Δϖ-band section cache as zero-miss: tolerance ≈1e-5 rad, 9.3% silent miss at the fine band (`136a` → `ca96`).
- The unified index's ΔU-linearized |Δn|: misses 66/495 on a constant-p bimodal-e belt; replaced by occupants' exact mean-motion extremes (`8716` → `88ee`).
- The static/priority candidate book: static keys miss 99–99.6%; selectivity never measured (`c716`).
- The provably-safe same-doll scan pre-filter: airtight bound rejects 0.07% — do-not-spend (`f79a`).
- The 0.1-encounters/body/orbit attractor: nonstationary, rate still climbing at 800 orbits (`1b1f`).
- The slack-0.5/widen-2 pairing at strong rotation: 5 misses/459 (`73f0`).
- The Catalogue key's sound domain reaching e ≈ 0.9995: it ends at e ≈ 0.969 (`969a` → `5d90`).
- "The shipped cone tier missed 0 encounters on every scene" (`8af8`, coorbital page): its truth shared the horizon-edge blind axis (`5c01`).

## Open directions

Ranked by what each would change:

1. **Ship the skin whole** — the measured lever (3.0–3.7× wall, soundness priced): the max-age refresh (`57c1`), slack/widen sized from the law's precession (`73f0`, `8f99`), the phase-aware deadline (`e49d`), and the player-burn path the queued skin cannot absorb (`e49d`).
2. **Close the two soundness holes in shipped code** — the two unconditional horizon-edge checks (`5c01`); high-e scene families in every frozen verify set plus the key window's inner-edge fix past e ≈ 0.969 (`8cee`, `5d90`). Also fix the i128 overflow in `hit()` (`cdf8`).
3. **The co-precessing frame for sections** — O(1) angle update per pair from the tubes' exact Δφ per cycle; load-bearing in the strong field (40–400 orbits at p ≈ 50 M) (`71a5`).
4. **Crossing-packet routing by flux aggregation** — one aggregate per packet crossing deletes pair enumeration exactly where the events are the workload (`2e81`, `62f7`); wire as the engagement branch of the unified rule (`88ee`).
5. **The allocator's encounter budget** — burst law (`7578`), nonstationary rate law (`1b1f`, `79ef`), no-avalanche bound (`6565`), deletable swarm gas (`ec74`), deadline-streaming of the kick wake (`e49d`).
6. **Wire the tier into the plane** (H0216): the player seam sets the deadline — 16.7 ms at ≈10⁴ bodies today (`d7bd`, `f79a`).
7. **The untested domain** — 3-D inclination, kick-perturbed λ(t), the GR doll (`4e7c`).

## Contradictions

None unresolved among these runs. Three silver/gold conflicts were resolved by their own second checkers (`969a`→`5d90` on the sound domain; `136a`→`ca96` on the cache; `9834`→`5c16` on the strobe record) and are kept as Refuted lines. One cross-run lesson stands as the page's H0183 example: `8af8`'s "0 missed" and `5c01`'s 20% horizon-edge miss agree because they shared the truth's blind axis — agreement between harnesses is not independence.

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
