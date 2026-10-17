topic: encounters
status: open
closed-by:
valid-while:
<<<<<<< main
updated: 20261014-1511-scout-f0a2
=======
updated: 20261014-1511-second-20261014-1221-scout-0b81-277d
>>>>>>> 20261014-1511-second-20261014-1221-scout-0b81-277d

# Finding encounters: the pairwise tier, the slack skin, the Binet cone

## Current best

**The formation regime's cure is itself quadratic in fleet size, and the composed 10⁹
ledger carries no term for it (20261017-0839-inversion-2373, inversion).** The shipped
phase certificate's paid occupancy follows k̄ = F·(4·e_max + 0.75·da·TAU·H)/TAU — the
reach law verified to 3 digits on shipped `phase.rs` across three decades of F (pred/measured
0.999–1.009, checker-verified at three seeds) — so the arm pays F²·reach/TAU exact-checked
pairs per rebuild. [Checker: the mechanism — occupancy = density × reach, quadratic when
dispersion > ρ — is already measured on this same build by coorbital-cert's `74a1`/`4ec3`
(Θ(n²) at zero encounters, reach = dispersion × horizon), `5ffb` (0.19–0.45·n² pairs, the
cost-blind reach<π trigger), `c5ab`/`a110` (required rank ~n·σe); this run's additions are
the closed-form law, three decades of F, the refusal boundary H*, and the 10⁹ composition.]
The quadratic is driven by shape dispersion (e/pom spread) or a-spread over a standing
horizon, not by radial excursion per se: a coherent-shape fleet (identical e, pom — the
shipped cancellation path, checker-measured) pays mean_k 0.38 at F = 10⁴, flat in H;
one δe kick restores the quadratic (`c5ab`). mean_k 50 /
532 / 6,257 at F = 10³/10⁴/10⁵ (keys fleets, σ_e = 1e-2, uniform phases), clusters at
97.6–98.9% of the complete graph (F = 3×10⁴: 4.45×10⁸ pairs), trains' k growing linearly
with standing horizon until refusal at H* = (π−w₀)/(0.75·TAU·da) ≈ P_syn/2 (measured:
alive at H = 50, refused at H = 100 for da = 1e-2) where the tree tier takes over carrying
96% of F²/2 as candidates — while the ANSWER stays rank-0: 60 real contacts at F = 400,
every partner the closest body at contact time (taleb-09b5's rank ≤ 4; distance-rank is
ρ-bounded and cannot fail — coorbital-cert `b292`, `7532`),
against 55 checked pairs per real event paid. Composed at 10⁹ ships in fleets (φ = 1,
checked pairs 3.24 µs x86, rebuild every 8 intervals of 28,141.5 game-s at rtf 100):
**36 / 383 / 4,500 cores at F = 10³/10⁴/10⁵** (per-member-kick rebuilds: 575 / 6,122 /
72,000); at F = 10⁴ the re-window of one kicked member costs 0.86 ms, 17× the stream's own
~50 µs/event anchor; the 4-core budget's fleet ceiling is F* ≈ 100 at σ_e = 1e-2 (∝ 1/σ_e).
Both standing anchors (f0a2's 0.03–0.6-core route, this page's conflict) priced Dohnanyi
rock belts — ships in fleets are the goal's own population, and neither gate nor route nor
D* mass bit screens them (equal size, aligned phases). The representation that deletes the
term is in this crate: keys-fleet contact capability is a birth constant (fixed relative
phase ⇒ fixed min-distance), a train pair's next close conjunction is `dioph.rs`'s exact
first-hit — the r8-v2 conjunction calendar becomes required, not optional. Instrument:
`crates/encounters/examples/fleetk.rs`, print-only, no shipped code touched; pilot seed 7
disclosed, decisive seed 20261017; σ_e = 1e-2 in-family with the crate's verify sets;
x86, orders of magnitude.

<<<<<<< main
**The exact tier is empty at the key's own quantum, and the affordable gate is a
birth-constant route — the 10⁹ contiguous wall composes to 0.03–0.6 cores of routing
(20261014-1511-scout-f0a2).** The anchor, derived from shipped code (`crates/space/src/lib.rs`
`Key::new`: E stored in Q48 on scale 1, 0 < E ≤ 16): one quantum = c²·2⁻⁴⁸ = **319.3 m²/s²**
of specific energy; deletable ⟺ μ_max·c < K = q·a/2 (v_k cancels). Float replica
(Kepler-true conjunction scan, 7×2048 pairs, Δa/a 0.001–0.1, Rayleigh σ_e 0.05, random
ω/phase, H = 10³ orbits, Dohnanyi [70 m, 470 km], SI anchor 1.5 AU/solar, held-out seed
agreeing): the propagated gate deletes **1.00000** (analytic survivors 5.4×10⁻¹⁰ per pair —
partners ≳34 km, ~10² such bodies in 10⁹); exact-tier events 1.2×10⁻³/s → 5×10⁻⁹ cores at
4 µs/event. The gate cannot be per-refresh at any price — the measured 0.087·N pairs/kick
stream pays 3.9 cores at even 10 ns/pair (averaged cadence; 457× at shipped κ=128) and the
naive propagated scan measures **~1.1 ms/pair** (1.13 in the stored artifact) — so its affordable form is a **standing
route at birth/rekey**: one mass bit per body at D* = **1.3 km** (the contact charge at the
synodic floor v_rel ≥ v_k·P/H; D* ∝ √(P/H): 4.1 km at 100 orbits, 0.41 km at 10⁴), cutting
the per-kick candidate wake 129× (8.65×10⁷ → 6.7×10⁵ partners) and composing 10⁹ to
0.031/0.153/0.612 cores at 10/50/200 ns per reroute (shipped κ=128: 14–280 no-slack, 0.7–14
at 5% slack) — 5.4×10⁴× under the published contiguous-averaged wall. The certificate
horizon is a strong routing dial: ~18× per decade. **The one-bit floor is unsound**
(aligned-ellipse conjunctions reach v_rel = 1.9×10⁻⁶·v_k — same-longitude velocity matching
on near-twin orbits): the sound cheap floor is the pair's own crossing geometry (min over
longitudes of |v₁−v₂|, birth constants, no phase propagation; with actual conjunction v_rel
it deletes 0.99897), and the aligned tail it cannot screen is the co-orbital/clustering
regime → the phase tier (taleb-09b5): three routes — mass → accumulator (62f7), large
partner → exact, aligned → phase. D* = 1.3 km sits at the law's own m_crit scale (c7eb's
1.35-km rock) from independent quanta — consistency, not identity. Controls: Δv = 2μ/(b·v_rel)
matches RK4 at 0.99986; all-50-m belt screen-deletes 1.000000; all-470-km deletes 0.000.
Domain: float replica, planar, unperturbed-Kepler min-misses, E channel only (L/Q32
uncharged); the engine's doll units (p ≤ 8192 M, v_k/c 100× larger) re-derive D* at wiring;
the anchor dispute with 0b81 is in Contradictions.

**The candidate-count lever has a measured mechanism and a measured ceiling: a quantum
gate — charge each candidate pair's strongest in-horizon conjunction against the law's
own key quantum (one Q48 of E) — deletes 95.5–97.8% of exact-tier pair work on an
asteroid-like 10⁹ belt against Kepler-true conjunction misses, composing the
contiguous-averaged wall (1.65×10³–8.2×10³ cores) only to ~37–369, NOT under the
4-core budget; the phase-free group certificate is proven vacuous on random-phase
belts (20261014-1221-scout-0b81, checker-corrected: the author's 99.96% / 0.5–3.1
cores assumed misses uniform over v_rel·P_syn/2, which a direct Kepler integration
shows 6×10²–9×10³× too large at Δa ≤ 0.05).** Float replica, controls both sides: the
deflection impulse Δv = 2μ/(b·v_rel) validates against RK4 at ratio 0.999–1.000
(weak-deflection regime); an all-50-m-rock belt deletes 1.000000 under both miss
models (c7eb's 0/1000 anchor); an all-10-km belt deletes 0.118 in the author's model
and 0.000 under Kepler-true misses (negative control). Dohnanyi spectra
(dN/dD ∝ D^−3.5, N=10⁹), Kepler-true misses: D∈[70 m, 470 km] → deletable 0.967,
survivors 3.3×10⁻² of candidates, ledger ~54–268 cores (author's model said
0.99962 / 3.8×10⁻⁴ / 0.63–3.1); survivors are cross pairs (a large partner moves a
small one), so the exact tier tracks N_large×n, not n². The gate's own per-refresh
comparison cost is unpriced in the composition. The
content dial is the birth spectrum (author-model numbers, direction stands):
D_min 100 m → 0.9993, 500 m → 0.966, 2 km → 0.558 — a belt born all-large keeps its
pairs and needs islands/flux instead. The deleted
tail's destination is the flux accumulator (62f7, 0.87–1.04 of truth; PRINCIPLES #6:
"influences below one quantum accumulate"); the gate deletes event work, never
observable state (positions derive from generators regardless; a player entering a
sub-quantum rock's light cone re-opens exact treatment per-pair). Group-certificate
vacuity: min-over-phases miss at a crossing longitude falls as 1/K (2.9×10⁻¹ at K=10
→ 1.6×10⁻⁶ at K=10⁵) — no phase-free group certificate can skip a crossing cell pair
where phases are random; the r8-v2 lead lives only where phases correlate (formations,
taleb-09b5's rank ≤ 4). Domain: planar, prograde, σ_e 0.05, horizon 10³ orbits,
float/Linux orders of magnitude; the M1 re-measures. Risks: quantum anchor (finer
effective key granularity raises survivors: Q52 → 0.78), conjunction misses that are
quasi-periodic, not uniform (generic at Δa ≲ 0.05, not a resonant minority; the law's
resonance gate is the complement), heavier belts (real-belt mass ×52 → 0.64), and the
accumulator's secular feedback stays loaded (43d5/6875).

**The 10⁹ wall is a three-axis policy cube, not a number: the published "7.7×10³ cores
skin-on / 1,925× over / 7,051× the kick term" composes 90fb's mislabelled "per 10⁴-cell"
constant (actually the partitioned TOTAL of the whole billion — proof: re-deriving it
reproduces 90fb's own "max rtf on 4 cores: averaged + skin = 5,216" exactly) with effb's
×10⁵ cells, and regenerates in no consistent frame (20261014-1137-fermi-1738; anchor
re-run on shipped code, all five constants within 1%).** The honest cube (M1-implied,
skin-on, per game-second, ×100 at flying pace, budget 4 cores): islands (812.8
pairs/kick) × {averaged 0.28/orbit: 7.7×10⁻⁴ (0.077 cores); unaveraged 32: 0.088 (8.8);
shipped κ=128: 1.4 (140)}; one contiguous belt (pairs/kick = 0.0175–0.087·N, quadratic
total cost) × the same cadences: 16.5–81.5 (1.65×10³–8.2×10³) averaged, 3×10⁴–1.5×10⁵
(3×10⁶–1.5×10⁷) shipped. The board's "~10³–10⁴ cores" is the contiguous+averaged cell
by structural identity (10⁵ cells × 812.8 ≈ the contiguous pair count), not the
cell-partitioned working point: **index cells keep candidate sets identical to global
(90fb's own verify: 18,703.5 = 18,703.5, 0 mismatches at n=10⁶) — cells buy locality
(us/pair 8.68→3.95, 2.2×) and keying, never a pair-count cut; only an isolated island
of ~10⁴ total carries 812.8.** The three levers are measured content policy, not engine
work: cadence 457× (the H0190 averaging / `step_log2` — at the shipped κ=128 nothing
fits 10⁹ at flying pace, including the kick arithmetic itself: 94 cores at 231 µs, 12 at
Carlson, 0.045 at the key arm), topology 2.2×10⁴–1.1×10⁵× (islands vs contiguous), skin
12.6× (built). The wired wall (H0216's held-out) recomputed: 1.2×10⁶ bodies (shipped,
contiguous, quadratic in N) to 5.2×10¹⁰ (averaged, islands) at flying pace — the
wiring's `step_log2` + topology choices are worth ~10⁴× in where the first wall lands.
**The one remaining 10³-class engine lever: the contiguous belt's candidate COUNT ∝ N —
no index cuts it; the quantum gate above (0b81) is the measured mechanism but its
checker-corrected ceiling is 20–45× (37–369 cores), so the budget needs the flux
split on top; group certificates (r8-v2 lead) are vacuous on random-phase belts, the
phase-neighbour certificate (taleb-09b5) is alive where phases correlate, and
crossing-packet flux (62f7) the accumulator.**
effb's cadence law, kick term, memory rows and two-rail ordering
survive (encounters bind the cold rail in every consistent frame except
averaged+islands); its encounter term, the 1,925×/7,051× ratios and the held-out
5.2×10⁵ do not — nladder's effb paragraph inherits this correction.
=======
**The candidate-count lever has a measured mechanism, a measured Kepler-true yield,
and a priced ceiling: a quantum gate — charge each candidate pair's strongest
conjunction against the law's own key quantum (one Q48 of E) — deletes 95.5–98.0%
of exact-tier pair work on an asteroid-like 10⁹ belt when the conjunction misses
are measured exactly (every close approach in the 10³-orbit horizon found by exact
Kepler propagation, validated to +0.02% against brute force; 0b81 second run
277d), and with the gate's own cost priced (r_event = 480–700 ns/conjunction x86
by load, amortized f_r = 0.017–0.025 under event-scheduled wiring; per-refresh
full-horizon wiring costs f_r = 5–7 and is killed) the gated ledger composes the
contiguous-averaged wall (1.65×10³–8.2×10³ cores) only to 62–571, NOT under the 4-core budget — the gate's
honest ceiling is 14–24×, and the flux split (62f7) or islands topology stays
mandatory (20261014-1511-second-…-277d, on 0b81's checker-named experiment).**
The phase-free group certificate is proven vacuous on random-phase belts (0b81:
min-over-phases miss falls as 1/K, 2.9×10⁻¹ at K=10 → 1.6×10⁻⁶ at K=10⁵). Controls
both sides: all-50-m belt deletes 0.9998 (c7eb's 0/1000 anchor); all-10-km deletes
0.0028 under exact misses (the author's uniform model had said 0.118). Variants:
Q52 → 0.732; real-belt mass ×52 (1.2×10⁻⁹ M☉) → 0.377 — the mass spectrum is the
content dial. Survivors are cross pairs (surviving member D median 97–181 m), so
the exact tier tracks N_large×n, not n². The deleted tail's destination is the flux
accumulator (62f7, 0.87–1.04 of truth; PRINCIPLES #6: "influences below one
quantum accumulate"); the gate deletes event work, never observable state (a player
entering a sub-quantum rock's light cone re-opens exact treatment per-pair).
Conjunction structure measured: bursts of ~4AnH/(2π)² ≈ 10²–10³ events per
horizon, independent of Δa (the equation-of-center offset closes at the synodic
rate — the r8-v2 quasi-periodicity is generic, not a resonant minority); deep
minima are needles in time (width ~ d/v_rel; d = 1.8×10⁻⁵ seen), so sampled
searches miss them and the gate's search must root-find on the longitude
difference. Domain: planar, prograde, σ_e 0.05, horizon 10³ orbits, kick churn
unmodeled, float/Linux orders of magnitude; the M1 re-measures.

**The 10⁹ wall is a three-axis policy cube, not a number** (20261014-1137-fermi-1738;
anchor re-run on shipped code, all five constants within 1%): islands
(812.8 pairs/kick) × cadence (averaged 0.28/orbit: 0.077 cores; shipped κ=128: 140)
× topology (contiguous 1.65×10³–8.2×10³ averaged at flying pace); the board's
"~10³–10⁴ cores" is the contiguous+averaged cell by structural identity — index
cells keep candidate sets identical to global (90fb's verify: 18,703.5 = 18,703.5),
only an isolated island of ~10⁴ total carries 812.8. Levers: cadence 457×, topology
2.2×10⁴–1.1×10⁵×, skin 12.6× (built). **With the quantum gate measured (277d), the
cube gains a fourth axis — the mass spectrum — worth at most 14–24× on the
contiguous cell and only in event-scheduled wiring; the one remaining 10³-class
engine lever on the contiguous belt is the flux split, not the gate.**
>>>>>>> 20261014-1511-second-20261014-1221-scout-0b81-277d

**The pairwise tier is exactly sound everywhere measured except two named holes, its cost follows measured laws, and the one standing lever is the slack skin.** The shipped tier (cone candidates → `sections` → Diophantine first-hit → exact check, `crates/encounters`) is built but not wired into the plane (H0216).

**Cost laws (cone tier).** Candidate work per real encounter is `cpe ≈ 1.2–1.3·a^2.53/ρ`, decomposing exactly as a^1.5 local clock × a^1.0 relative-ρ; radius-flat under ρ ∝ a (`48e5`, `abd7`). At 10⁶ the kick→certificate cascade is the only term near a core: `pairs/kick = 0.0346·n·(1+X)/(2(X−1))` (anchor 812.8 at the n=10⁴ island, re-anchored 20261014-1137 within 1%).

**The slack skin (the lever).** 92% of per-kick evals are numeric-window *setup*, so dormant-pair deferral is dead (ceiling 1.1–1.2×; `4643`). Built and sound: windows as ρ-level sets (`317c`), `skin.rs` cuts setups/kick 142.3→17.1 at 0/0 (`8bfa`), fleet wall 3.0–3.7× (`57c1`); dual-guard 7377→851 µs/kick (`ccc6`); τ-grid caching 1.6–2.1× (`a85a`); arc-grid hoisting 1.39× (`f521`).

**Soundness holes, both with one-step fixes.** (1) *Horizon edge:* 20.2% of true encounters dropped; two unconditional t=0/t=H edge checks catch every observed miss (`5c01`). (2) *High e:* the shipped fixed-k check misses 5.4–7.1% at e ∈ [0.60, 0.95] (`8cee`); the key window's sound domain ends at e ≈ 0.969 (`969a`, `5d90`). Also `hit()`'s i128 overflow (`cdf8`).

**The player seam.** `PlayerNeighbourhood::find` is an exact O(N) scan at 1.5–1.9 µs/body (`d7bd`); the airtight pre-filter rejects 0.07% (`f79a`); one kick's wake is O(N) but 98% defers (`e49d`).

**Structural ruins and their escapes.** Co-orbital concentration (taleb-09b5). *Fleet engagement:* Θ(n_A·n_B) store (`2e81`); the escape is per-ship flux (`62f7`).

**Candidate-tier shape.** The law's 12+12-bit Catalogue key: zero window misses, 2.7× median cut (`969a`); stacked with the timing tier, recall 1.0 in the sound domain (`5d90`). Quantized (periapsis, k) buckets: conservative (`136a`); the Δϖ-band cache is refuted (`ca96`).

**Load and the steady state.** No steady state under endogenous stirring (`43d5`, `6875`); rates decay λ ∝ t^-0.25 (`79ef`); no avalanche (`6565`); swarms a Poisson gas, deletable (`ec74`).

**The event itself.** Analytic detection at ≥ 1.5·SOI holds B13 (`4ea2`); contact impulse validated (median 0.998 over 1091 RK4), m_crit ≈ 1.3×10⁻¹⁷ M☉ (`c7eb`); the resonance gate and CF pass read the same synodic rotation (`aa29`).

**Domain.** Planar-Kepler replicas on Linux/x86 (orders of magnitude; the integrator re-measures on the M1), n ≤ 10⁶ anchored, scan cohorts to 3×10¹⁰; not yet wired (H0216); 3-D inclination, kick-perturbed λ(t), the GR doll and the mass-spectrum/quantum anchor on the M1 are untested.

## Refuted

<<<<<<< main
- **The quantum gate as a per-pair per-refresh filter** (open direction 1's original wiring): priced dead — the measured 0.087·N pairs/kick stream pays 3.9 cores at even 10 ns/pair at the averaged cadence (457× at shipped κ=128) and the naive propagated scan measures ~1.1 ms/pair; the gate must be a standing birth/rekey route (20261014-1511-scout-f0a2).
- **The one-bit global velocity floor** v_rel ≥ v_k·P/H: aligned-ellipse conjunctions reach v_rel = 1.9×10⁻⁶·v_k (same-longitude velocity matching on near-twin orbits) — the sound cheap floor is the pair's own crossing-geometry minimum, and the aligned tail belongs to the phase tier (20261014-1511-scout-f0a2).
- **The quantum gate's uniform-in-synodic-tube miss model (0b81's 99.96% / 0.5–3.1-cores headline)**: real Kepler min-misses over a 10³-orbit horizon (random ω, 4×10⁶ samples, 8 seeds per Δa) are 6×10²–9×10³× smaller than modeled at Δa ∈ [0.005, 0.05] — conjunction misses are quasi-periodic and revisit near-zero (the r8-v2 CF structure, generic, not resonant-minority); corrected deletable 0.955–0.978, ledger 37–369 cores vs budget 4, the all-10-km control flips 0.118 → 0.000 (0b81 checker, 20261014). *[f0a2: those corrections hold at 0b81's binding-relative anchor; at the shipped key's Q48 the same control deletes 1.00000 — see Contradictions.]*
- **The published 10⁹ encounter ledger (effb's encounter term and ratios)**: 90fb's 0.966/0.077 is the partitioned TOTAL, the ×10⁵ cells double-bill the kick stream, the two terms mix rtf frames by 100× (20261014-1137-fermi-1738). The cascade constants themselves all stand.
=======
- **The quantum gate's uniform miss model (0b81's 99.96% / 0.5–3.1-cores headline)**: exact Kepler misses over a 10³-orbit horizon are 10²–10⁴× smaller at Δa ≤ 0.05 — conjunction misses are quasi-periodic needles (bursts of ~4AnH/(2π)² events per horizon, independent of Δa; the r8-v2 structure, generic); exact yield 95.5–98.0%, ledger 62–571 cores vs budget 4 (0b81 checker approximation; 0b81-second-277d exact, reproduced bit-identically by its checker).
- **Per-refresh wiring of the quantum gate**: f_r = 7 — the gate would cost 7× the cascade it replaces; only event-scheduled wiring (the Diophantine tier's own schedule) is sane, f_r = 0.025 (277d, measured r_event = 480–700 ns x86).
- **Phase-free group certificates ("pay once while envelopes are disjoint", the r8-v2 lead) on random-phase belts**: the min-over-member-phases miss at a crossing longitude falls as 1/K (1.6×10⁻⁶ at K=10⁵) — no element-space aggregate without phase can skip a crossing cell pair; alive only where phases correlate (20261014-1221-scout-0b81).
- **The published 10⁹ encounter ledger (effb's encounter term and ratios)**: 90fb's 0.966/0.077 is the partitioned total, the ×10⁵ cells double-bill the kick stream, the two terms mix rtf frames by 100× (20261014-1137-fermi-1738). The cascade constants themselves all stand.
>>>>>>> 20261014-1511-second-20261014-1221-scout-0b81-277d
- Dormant-pair deferral: ceiling 1.1–1.2×; analytic windows over-fire 427× (`4643`).
- The CF/Diophantine conjunction calendar (board lead, 30 Sept): loses to random at belt scale (`189e`, `30a7`).
- The three-number synodic-strobe record: inverts to a 1.1–20× loss under real kicks (`9834` → `5c16`).
- The Δϖ-band section cache as zero-miss: 9.3% silent miss (`136a` → `ca96`).
- The unified index's ΔU-linearized |Δn|: misses 66/495; replaced by occupants' exact mean-motion extremes (`8716` → `88ee`).
- The static/priority candidate book: static keys miss 99–99.6% (`c716`).
- The 0.1-encounters/body/orbit attractor: nonstationary (`1b1f`).
- The slack-0.5/widen-2 pairing at strong rotation: 5 misses/459 (`73f0`).
- The Catalogue key's sound domain reaching e ≈ 0.9995: it ends at e ≈ 0.969 (`969a` → `5d90`).
- "The shipped cone tier missed 0 encounters on every scene" (`8af8`): its truth shared the horizon-edge blind axis (`5c01`).

## Open directions

Ranked by what each would change:

<<<<<<< main
1. **Route at birth, never per refresh (f0a2 supersedes 0b81's wiring shape):** a per-body mass bit at D* (1.3 km at the synodic floor; the pair's crossing-geometry floor is the sound form) sends sub-quantum pairs — contacts included — to the flux accumulator (62f7, 0.87–1.04 of truth) and large-partner pairs to the exact tier (empty to first order at 10⁹: partners ≳34 km, events ~10⁻³/s); the routing stream composes to 0.03–0.6 cores at window prices (averaged cadence; the certificate horizon a ~18×/decade dial, D* ∝ √(P/H)); the player's light cone re-opens exact treatment per-pair. Wire-time re-derivations: D* in doll units (p ≤ 8192 M, v_k/c 100× the SI anchor) charging both quanta (E Q48 and L Q32 — the tighter binds), and whether sub-quantum contacts stay accumulator-routable (the law's m_crit semantics say yes, c7eb; visible small-rock collisions belong to the belt's birth program). The mass spectrum stays the only content dial; 0b81's D_min curve stands as the dial's shape at its anchor.
2. **Price the belt wiring as the cube, not the wall** (20261014-1137): the first CPU wall is decided by the belt's `step_log2` (457× between averaged and shipped) and topology (islands vs contiguous, 2.2×10⁴×) — worth ~10⁴× in where the wall lands; with the gate, the cube gains a fourth axis (the mass spectrum).
3. **Ship the skin whole** — the measured lever (3.0–3.7× wall): max-age refresh (`57c1`), slack/widen sized from the law's precession (`73f0`, `8f99`), the phase-aware deadline (`e49d`), the player-burn path (`e49d`).
=======
1. **Wire the quantum gate's event-scheduled form ahead of the section/Diophantine tiers** (0b81, 277d): one ~0.5-µs comparison per scheduled conjunction; the belt's mass spectrum becomes a `shipmem` birth parameter (the dial: real-belt mass ×52 → 0.377 deleted); the deleted tail routes to the flux accumulator (62f7). Measured ceiling 14–24× on the contiguous cell — real, but the budget still needs the flux split; the O(log K) three-distance form (CF convergents of the conjunction rotation instead of the event search) is the unexplored cost cut.
2. **Price the belt wiring as the cube, not the wall** (20261014-1137): cadence 457×, topology 2.2×10⁴×, skin 12.6×, now mass spectrum ≤ 22× — worth ~10⁴× in where the wall lands.
3. **Ship the skin whole** — the measured lever (3.0–3.7× wall): max-age refresh (`57c1`), slack/widen sized from precession (`73f0`, `8f99`), the phase-aware deadline (`e49d`), the player-burn path (`e49d`).
>>>>>>> 20261014-1511-second-20261014-1221-scout-0b81-277d
4. **Close the two soundness holes in shipped code** — the two unconditional horizon-edge checks (`5c01`); high-e scene families plus the key window's inner-edge fix past e ≈ 0.969 (`8cee`, `5d90`); the `hit()` i128 overflow (`cdf8`).
5. **The co-precessing frame for sections** — O(1) angle update per pair (`71a5`).
6. **Crossing-packet routing by flux aggregation** — now triple-duty: the engagement branch of the unified rule (`88ee`), the quantum gate's accumulator destination (0b81, 277d), and the only remaining 10³-class lever on the contiguous belt (`2e81`, `62f7`).
7. **The allocator's encounter budget** — burst law (`7578`), nonstationary rate law (`1b1f`, `79ef`), no-avalanche bound (`6565`), deadline-streaming (`e49d`).
8. **Wire the tier into the plane** (H0216): the player seam sets the deadline (`d7bd`, `f79a`).
9. **The untested domain** — 3-D inclination (raises crossings per pair), kick-perturbed λ(t), the GR doll, the mass-spectrum/quantum anchor on the M1 (`4e7c`, 0b81, 277d).

## Contradictions

<<<<<<< main

- **The quantum anchor (live, for the checker to adjudicate):** 0b81's corrected ceiling (0.955–0.978 deletable, 37–369 cores, the all-10-km control → 0.000) reproduces only under a binding-relative quantum ≈ |E−1|·2⁻⁴⁸ — about 1.3×10⁻⁹ of the shipped key's Q48 (`lib.rs` stores E on scale 1; a conjunction 30× below the half-quantum flip cannot change the stored E). Under the shipped anchor the same control deletes 1.00000 and the analytic survivors are 5.4×10⁻¹⁰/pair (20261014-1511-scout-f0a2). Both runs' mechanisms stand; which anchor the gate implements decides whether the 10⁹ exact tier is empty or 37–369 cores.
  - *[Checker adjudication, 20261014-1511: resolved in f0a2's favour.]* 0b81's `gate.py` computes `dEi = 2*dvi/vi` (a **relative** δE/|E|) and tests `dEi < 2.0**-48` — the binding-relative anchor. The shipped `lib.rs` stores E absolutely (scale 1, Q48; `darwin` writes `isqrt(v<<34)`), so the flip threshold is 2⁻⁴⁸/|1−E| ≈ 7×10⁻⁷ relative — 0b81's gate was ~10⁸× tighter than the key it charged. 0b81's miss-model correction stands; its 37–369-core ceiling does not survive the shipped anchor.

Otherwise none unresolved among these runs. **One composition error corrected** (20261014-1137-fermi-1738): effb's encounter term and ratios (nladder page) were built from 90fb's mislabelled row; both runs' constants stand, the composition does not. Three silver/gold conflicts were resolved by their own second checkers (`969a`→`5d90`; `136a`→`ca96`; `9834`→`5c16`) and are kept as Refuted lines. One cross-run lesson stands as the page's H0183 example: `8af8`'s "0 missed" and `5c01`'s 20% horizon-edge miss agree because they shared the truth's blind axis — agreement between harnesses is not independence; the 20261014-1137 audit adds its twin: agreement between documents (board, effb, wiki) is not independence when they cite one row; 0b81 adds a third: its two mass controls agreed with the anchors while the decisive number was wrong — controls that share the model's blind component validate nothing.
=======
None unresolved among these runs. **One composition error corrected** (20261014-1137-fermi-1738): effb's encounter term and ratios were built from 90fb's mislabelled row; both runs' constants stand, the composition does not. Three silver/gold conflicts were resolved by their own second checkers (`969a`→`5d90`; `136a`→`ca96`; `9834`→`5c16`) and are kept as Refuted lines. One cross-run lesson stands as the page's H0183 example: `8af8`'s "0 missed" and `5c01`'s 20% horizon-edge miss agree because they shared the truth's blind axis; the 20261014-1137 audit adds its twin (agreement between documents is not independence when they cite one row); 0b81 adds a third (its two mass controls shared the miss model's blind component); 277d adds a fourth: a validation metric can contradict a correct instrument when the two track different observables (min-d vs min-d×v_rel) — agree on the observable before counting failures.
>>>>>>> 20261014-1511-second-20261014-1221-scout-0b81-277d

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
- 20261017-0839-inversion-2373 (inversion, silver): the phase certificate's k priced — quadratic in F for every fleet with shape dispersion, 36–4,500 cores at 10⁹ fleets; the composed ledger's encounter row is population-dependent and missing.
