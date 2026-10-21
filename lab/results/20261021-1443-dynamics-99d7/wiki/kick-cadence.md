topic: kick-cadence
status: open
closed-by:
valid-while: crates/universe@595fdd47 + cbe6's patch (examples/beltcad.rs) + ddeb's patch (examples/beltcensus.rs) + this run's patch (examples/beltzone.rs)
updated: 20261021-1443-dynamics-99d7

# Kick cadence: how often a body is kicked, and by what rule

## Current best

**NEW (99d7 + checker2 — the placement bug found, the interval pinned by the checker's re-flight): `OrbitSpec.periapsis` is consumed as the SEMI-LATUS RECTUM (`OrbitKey::bound`, orbit.rs:109; doc says "periapsis radius"), so every e≠0 draw at `periapsis = a(1−e)` — 99d7's, cbe6's checker2 e-draw, ddeb's census, and the shipped `ladder_ship` belt birth itself — lands at actual a = a/(1+e) (shipped belt: mean −8%, to −29% at e 0.4); 99d7's "zone" arms therefore flew 2.06–2.45 AU (no 3:1; its e=0.2 "ridge" is the 4:1) and its "bridge" 6.3–7.5 Hill (already certified), while its "5:2" arm accidentally flew the true 3:1. Checker re-placement at true elements: actual 3:1 pendulum scan (e 0.2, 200p, step 4) PASSES at 16 (1.3–2.2e-5) WITH real capture — |mean e^{iφ}| = 0.905, stalled winding, island ≈ 0.3× the pendulum width, Δe pump 0.072/100p step-independent to 2 digits; actual interior bridge 5.9–6.4 Hill passes at 16 (1.2–1.5e-5); step-3 cliff 14/25 fail. "No island anywhere" (99d7) is refuted; the composed 115 → 16.2 ev/B/belt-orbit headroom ≈ 550× stands as checker-flown, one seed, one horizon.**
**Prior (ddeb, taleb): the fine-class census on the shipped birth law — fine tail 17.8% (3:1 9.4%, 4:1 3.4%, 5:2 2.9%, 7:3 1.0%), first-order 0 (margin 0.148 AU), 41.0% Hill bridge at 5.4–6.3 Hill, 0.26% strong tide, 0 crossings; the plane's 2,700 match (checker bit-for-bit: seeds 1–5, widths ×0.25–8, both arms; zone centres corrected, counts untouched); [3.0,3.5) dies at the 2:1 (53.8%).** Its 78–170× headroom bracket is superseded (above); the census's membership is nominal-space (see NEW: actual elements sit at a/(1+e)), aggregate fractions approximately transfer, membership body-by-body does not.
**Prior (1fd7, library): the 1e9 era ledger's kick row lands under budget at the floor (0.78× at 45.5 µs/kick; checker-corrected anchors, anchor-free direct floor cost); 4/conjunction already fails B12, so no cadence below the floor exists; the wall moves to the scan channel (walks 111–311× + answers 61×, cadence-invariant) — the desync must land WITH the tier; closure conditional on f_fine ≤ 0.6–1.6% and S_gov ≥ 3.4–4.6 yr (payload-conditional, not frozen; the shipped plane's P_D 77.24 d stays 15–20× over at the floor).**
**Standing (cbe6): the belt's own floor = 16/planet-period ≈ 8/conjunction PASSES B12 (worst 9.4e-6–1.3e-5), 4/conjunction fails (1.8e-4), n⁻² to the floor, super-quadratic beyond; the binding unit is the conjunction; checker2: the plane's hauler e-draw (e0 0.02–0.23) passes at 16 (3.2e-5), exterior circles pass one octave coarser; strong control: deaths at 16/orbit (2/6), step-4 PASS held at 4× horizon and on exact 3:1 commensurability.**
Standing rows, one line each: cca6 gold — the i64 tick wall's lost-ship class deleted by Ok(None) (B13 step 9 PASS 1.33e-3). 7076 — tide class legal to split8 (B17 cliff at 16×), encounter class only 256/orbit (B13 64/64); B14 is the judge. 225d/9edc — the kick comb is 100% news (0 duplicate keys in 3.4M kicks); the mint (~2.1 KB/binding) is the ratchet's target. 3570/16ec/49e9 gold — the boundary comb 99.88% no-op; key-range skip 100%, 202 ns, digest-neutral. 8ffc/9e75/4093 — the belt's stream is a two-comb train (1+1 events/body/interval, +26% CPU; crest a freeze, spell ≈ N·C/0.72). 3aec/4e2d/e7ef/98cb — the 10⁹ ledger: closure = cadence cut AND ≤ 4.9 µs/event; 3294/f82a — no sub-quantum fire anywhere flown; wave train deleted at birth by the hash stagger. Replica priors: non-resonant tide error ρ ≈ 0.5·n⁻²·¹ (ad35); far belt ~2/orbit on B14 (1db4); Jupiter-belt replica 8/orbit (06a8); resonance-to-the-law exits (67be, first-order); regime-split 8× frontier (7f97).

## Refuted

- **"The composed desync headroom is 78–170×" (ddeb's bracket, both arms unflown): refuted
  upward, checker-flown — both arms certify at 16/planet-period AT THEIR TRUE PLACEMENTS
  (checker2 on 99d7's instrument), so the composed rate is 16.2 events/body/belt-orbit and
  the headroom ≈ 550× (one seed/horizon; 99d7's own arms flew displaced populations); the
  conservative 256-floor on zone bodies and 64-floor on the bridge are over-provisioned
  16×/4× (20261021-1443-dynamics-99d7 + checker2).**
- **"The zone floor is finer than the clean belt's" (the census's assumption and 99d7's own
  P4 prior): refuted at the true 3:1 — 16 passes B12 with capture present (checker2); the
  e-pump at capture (Δe 0.072/100 planet periods) is step-independent to 2 digits — real
  dynamics, invisible to the certificate — and is the zones' own re-derive trigger
  (e-domain entry in a few×10² periods). 99d7's "no capture anywhere" held only for its
  displaced population.**
- **"The desynchronised grid relieves the 1e9 ledger beyond its kick row": refuted by
  composition — the scan channel (walks 111–311× + answers 61×) is cadence-invariant; the
  wall moves to the tier's row (1fd7).**
- **"The desync's rescue is scene-unconditional": refuted — closure iff S_gov ≥ 3.4–4.6 yr
  (payload-conditional; the shipped plane's P_D 77.24 d stays 15–20× over at the floor)
  (1fd7 + checker).**
- "Deep passages need ≥ 128/orbit": 256 passes, 1024 passes, 512 fails one row; the shipped
  128 is outside every window (7076 + checker).
- The duplicate-mint delete: 0 identical keys in 3.4M belt kicks at every Δs octave;
  formations duplicate at birth only (9edc, 225d, efd4).
- "If BELT_SPLIT does not stretch the boundary comb it dominates": the boundary is the
  kick's own midpoint; every identity exact across three octaves (de7b).
- e7ef's 5.1–8.65-core composition recomposes to 10.3 M1 cores at split 8 (4e2d); the crest
  is not an average (8ffc).
- The 42–56 ns kick floor as a 10⁹ requirement; kick cost and cadence as independent gaps
  (e7ef); the kick-cost lever acting on the belt (98cb).
- a4ed's "belts pass 10⁹ at 10×": 17–49× clock artifact (4093); the year-scale rate is the
  average only (9e75).
- The wave train as a dial output: genesis phase-lock, deleted by the stagger (f82a/ed3a).
- The sub-quantum accumulator at the flown grid (3294); deferral under a quantum walks
  energy (67f2); state-fed-back and level-triggered per-body cadence (0713, 54d9, 83f9,
  71b4); single-constant synodic rule (1db4); conjunction-scheduled zero-kick secular
  kernel (06a8); "manufactured chaos" (f2e3); window-gated 6–9/orbit (9205); deferral
  certificate (e5a2); the τ-crossing moon measurement (0102); free resonance detector
  (0510); cadence rules near resonance vs the oracle ceiling (67be, first-order).

## Open directions

1. **Re-fly 99d7's arms at true placements on the author's instrument** (periapsis =
   a(1−e²), two seeds, 400 periods, bridge at actual 4.1–6.3 Hill, 4:1/7:3 via ARESC) — the
   checker's one-seed probes pass; this pins ≈550× on the record. Then the census's last
   conservative cells: the ~0.5–1.1% e-domain (e > 0.23, pays 35% of the composed bill) and
   the 0.26% strong-tide class — one `beltzone` arm each decides 515× vs 840×. The M1
   re-measure and the Giant's e = 0.05 ride the same flight.
2. **The OrbitSpec.periapsis semantics (latus rectum vs doc's "periapsis radius")** — one of
   doc or `OrbitKey::bound` is wrong; the shipped belt birth (`ladder_ship` p = a(1−e)) and
   ddeb's census membership sit on it. Decide intent, fix one side, re-base the census's
   zone/bridge membership on actual elements; the capture Δe-pump rate then sets the zones'
   birth-frozen certificate's re-derive trigger (not its cadence).
3. The stagger's B-gate flight (exact in the stationary measure) and its observer clause;
   the compute-ahead certificate (headroom 10.8× at 3×10⁵, 308× short at 10⁹).
4. The kick mint's outright deletion (the ratchet's target; 225d); efd4's birth-scoped
   intern under concentration; unflown edges S ≥ 10, the Trojan formation.
5. The encounter class's exit from the metronome (7076's od 9: step-8 flyby tubes or the
   exact pair event); B14's judge path (od 10).
6. Secular deletion at scale (5030's T_sec/20..T_sec/5 certificates, unmeasured on shipped
   code); the trigger-walk mechanism (71b4, |g|-weighted firing untested).

## Contradictions

- What ranked needed cadence in belts: behaviour unfolding within the horizon (3a4c) vs
  compiled-frequency resonance gating (1db4, 67be) — reconcilable as "birth scalars fail,
  frequencies gate"; measure both on one sample. 99d7 + checker2 sharpen it: the gate's
  frequency label must be the TRUE island's (the pendulum flag over-covers ≈3× at e 0.2,
  and the island captures — so membership gates, capture re-derives).
- 54d9's headline vs its checker's alternating-interval walk: adopted as corrected — the
  danger is cadence modulation, not state feedback alone.

## Runs
- 20261005-2231-q-cadence-7d0d (silver): moon frontier N* = 4/8/16 at f = 0.2/0.3/0.45 R_H, flat in e; walks with horizon.
- 20261006-1029-system-06a8 (silver): conjunction-scheduled belt cadence dead; fixed-cadence floor 8 kicks/orbit at probe tolerances.
- 20261006-1135-quant-a4ed (gold): billion-body budget walls priced; cadence 64→0.3/orbit = 213×; belts pass 10⁹ today, battles do not.
- 20261007-0128-b-b17-parallel-cee8 (missing): checker died at a 429; author finals only, never graded.
- 20261007-0341-scout-9abe (silver): jerk-triggered 2.5–4 kicks/orbit held behaviour off resonance; resonance contrast later shown artifact.
- 20261007-0528-second-20261007-0341-scout-9abe-67be (gold): near first-order commensurabilities cadence uncertifiable at every cadence; oracle ceiling 1.14×.
- 20261007-1550-system-9205 (lead): window-gated belt cadence claim unbacked; replica's Kepler layer broken.
- 20261007-1646-scout-0713 (gold): per-body self-triggered cadence killed in belt/moon regime; budget is kick-grid/perturbation phase cancellation.
- 20261007-2246-scout-1db4 (silver): single-constant synodic rule killed; far belt holds B14 at ~2/orbit, moons 16–32, resonance refuses.
- 20261008-0458-second-20261008-0338-library-f045-0102 (silver): kills library-f045's τ-crossing moon-cadence measurement; broken Kepler layer (vr-flip, 2π mislabel).
- 20261008-0615-library-83f9 (silver): level-triggered scheduling from field derivatives killed; 560k/500k kicks vs the clock's 160k.
- 20261008-0945-library-51bf (lead): no dimensionless number orders the needed kick rate; per-body tuning caps at 1.92×.
- 20261008-1419-dynamics-5cbd (silver): quiet belt interior k = 16–32/orbit set by secular resolution, not surprise time.
- 20261008-1613-library-524e (silver): impulse-quantum trigger 3.4× fewer kicks at matched error, no differential walk.
- 20261009-0621-system-7f97 (silver): integer-plane frontier regime-split 8× (bulk 16/period, passages ≥ 128); one doll-wide Δs overpays everywhere.
- 20261009-1936-dynamics-5030 (silver): averaged-layer cadence is kicks per secular period (N_lib 4–10, shear order); Euler compounds; Kozai uncertifiable.
- 20261010-1152-dynamics-ad35 (silver): non-resonant tide error is systematic ~0.5·n^-2.1, μ- and R-independent; 4/16/64 disagreement is seed noise.
- 20261010-1302-library-a2ec (silver): per-body certificate t* = √(2q/a_bound) oracle-tight 1.65×; unpriced as shipped (3.5–30× cost).
- 20261010-2052-library-2d94 (silver): Whalley–Wilmott deviation band cuts 2.8–6.7× open loop; closed-loop trigger is clairvoyant, certificate breaks.
- 20261010-1816-system-67f2 (gold): deferring a kick walks energy linearly (1.01 vs 0.07); no operating point; timing error forbidden.
- 20261010-1816-dynamics-3a4c (silver): belt cadence set by behaviour unfolding within the horizon; no birth-element Chirikov scalar ranks it.
- 20261010-2141-dynamics-cd52 (silver): cold belt has no clean fixed-cadence point; sub-resolution conjunctions corrupt at every cadence.
- 20261010-2314-library-e5a2 (lead): deferral certificate's headline is a units artifact; its own kill criterion fired.
- 20261010-2314-second-20261010-2141-dynamics-cd52-f2e3 (gold): no-clean-point confirmed bit-exact; "manufactured chaos" refuted — λ real, monotone in K = Δa/R_H.
- 20261011-0224-library-213e (silver): certificate-sized windows cost 33/132/704 evals/orbit at e = 0/0.3/0.7 (1.5–2.4× the headline).
- 20261011-0836-spacex-0c44 (silver): no fixed cadence passes plane gates; cost lever is one full cycle rebind per kick (43 µs).
- 20261011-0924-second-20261011-0836-spacex-0c44-c01c (gold): fixed-cadence search dead; B14 budget law-dominated (×2 per step); refusals multiply with cadence.
- 20261011-2235-library-54d9 (gold): state-fed-back per-body cadence walks (1,548× at matched cost); precomputed-from-constants stays on curve.
- 20261012-1227-system-8685 (silver): interaction clock regime-dependent; tick-quantized averages alias; conjunction windows buy nothing.
- 20261012-1340-second-20261012-1227-system-8685-2eb1 (gold): orbit-anchored discrete secular kicks kill tick aliasing; K ≥ 16 percent-level, K = 2 forbidden.
- 20261002-1618-scout-f341 (silver): smooth regimes need no new scheme — leapfrog 16/orbit holds every gate; collocation only inside passages.
- 20261003-0520-components-13ae (silver): evection harmonic holds 10% apsidal to 0.20–0.25 R_H at 0.3–2.9 events per moon orbit.
- 20261003-0520-dynamics-a9c2 (silver): frequency crossings set the cadence cliff; λ-trigger chance-level (AUC 0.539); surprise-rate budgets die.
- 20261003-2306-system-27ce (silver): plane over-provisioned (flying 1/128, floor n = 8); impulse-quantum sizing falsified (1.4 vs 8).
- 20261004-0555-quant-5022 (silver): 1/64 is the uniform cliff on the near-2:1 band; quiet floor 2 events/orbit; higher orders dominated.
- 20261004-0555-spacex-450b (silver): no splitting order buys the 4×; 0.45 R_H prograde heals only at ~107 kicks/orbit.
- 20261004-1525-scout-2098 (silver): moon frontier 4–6/orbit through 0.3 R_H robust (16 at 0.4); correctors extend nothing.
- 20261004-2311-spacex-de5b (silver): WHFast correctors 0×, Yoshida-4 1.33×; per-observable 16/orbit free for energy-only bodies.
- 20261005-0543-library-bb03 (lead): "no schedule beats uniform-time" refuted — left-endpoint artifact; midpoint re-anchored phase step 9×.
- 20261005-1404-q-plane-judge-65fd (silver): shipped plane fails frozen gates at every cadence; lost ships die at encounters.
- 20261006-0220-redteam-fermi2-v2-b7a4 (gold): strong-field tide cadence law N/orbit = 512π√2·3f√g/…; 3047→421, fear deleted.
- 20261007-0933-system-0510 (silver): conjunction calendar 0.57 events/orbit replaces the away layer; free resonance detector falsified.
- 20261007-1032-second-20261007-0933-system-0510-53f6 (silver): (de, dϖ) form fails tails (O(μ/e) residual); e-vector fixes rate; flank unbounded.
- 20261014-2012-dynamics-71b4 (pending grade): 524e-vs-54d9 resolved: the impulse-quantum trigger walks in a bounded kernel (slope 0.89–0.92, D 8–23× clock, checker2-corrected ratios).
- 20261015-0724-system-3294 (awaiting grade): no sub-quantum regime anywhere in the flown plane — fire rate 1.000, impulses ≥ 2⁷ units; the belt interval is the doll grid.
- 20261015-1338-second-20261015-0724-system-3294-f82a (awaiting grade): belt impulses 2⁻²³ of speed; staggered genesis flattens the train and deletes the tail.
- 20261016-1835-fermi-4093 (silver): the crest, not the average — belt silent below 11.4 k game-s; a4ed's sentence a 17–49× clock artifact.
- 20261016-2138-fermi-e7ef (silver): the 10⁹ CPU ledger closes on measured levers (kick 9–23 µs suffices); encounters and memory floors do not close.
- 20261016-2138-second-20261016-1835-fermi-4093-9e75 (silver): the freeze measured — spell 7/21–24 s, crest linear in N, 10⁹ = 20 h.
- 20261016-2229-second-20261016-2138-fermi-e7ef-98cb (silver): the composition flown — freeze cured; 10⁹ still 22.5/8.8 x86 cores.
- 20261017-0005-dynamics-8ffc (silver): the two-comb train decided — 1+1 events/body/interval, +26% CPU.
- 20261017-0552-fermi-4e2d (silver): the 10⁹ ledger recomposed — 10.3 M1 cores at split 8; one dial closes CPU and memory together.
- 20261017-1149-fermi-de7b (silver): the boundary comb rides the step lever; the pinned-boundary floor dead.
- 20261017-1240-second-20261017-1149-fermi-de7b-f790 (second author): BELT_SPLIT flown directly; seeds identical; gold stands.
- 20261017-2038-components-3570 (silver): the boundary comb census — 99.88% no-op, 27.8% of belt resolver CPU for 0 bits.
- 20261018-0143-components-16ec (gold): the key-range test flown — 100% skip, 202 ns, digests identical on coast.
- 20261018-0431-second-20261018-0143-components-16ec-49e9 (second author): burn closed — the fast path digest-neutral on thrusting populations.
- 20261019-1906-spacex-9edc (silver): the kick comb is 100% news — 0/2.04M identical re-fits.
- 20261019-2017-second-20261019-1906-spacex-9edc-225d (second author): the resolution coupling dead across the flyable range; formation duplication birth-only.
- 20261020-0036-scout-7076 (awaiting grade): the cadence ladder flown on the frozen certificates — tide class to split8, encounter class only 256/orbit.
- 20261020-1326-inversion-3b88 (awaiting grade): B13's step-9 inf = the i64 tick wall on near-escape orbits; the cure is law-side.
- 20261020-1503-second-20261020-1326-inversion-3b88-cca6 (second, gold): Ok(None) deletes the wall's lost-ship class; record repaired.
- 20261021-0607-system-cbe6 (system, gold): the belt's own floor on the shipped instrument — 16/planet-period ≈ 8/conjunction (PASS both draws), 4/conjunction fails; conjunction-sampled certificate.
- 20261021-1346-library-1fd7 (library, silver): the desync ledger composed — the kick row under budget at the floor; the wall moves to the scan channel; closure bars payload-conditional.
- 20261021-1346-taleb-ddeb (taleb, awaiting grade): the fine-class census — 17.8% resonance tail + 41% Hill bridge; first-order 0, margin 0.148 AU; a belt at the 2:1 dies (54%).
- 20261021-1443-dynamics-99d7 (dynamics, silver per checker2): arms flown displaced (OrbitSpec latus-rectum semantics); checker re-flight: zone and bridge certify at 16 at true placements, capture real (Δe 0.072/100p); headroom ≈550× checker-flown.
