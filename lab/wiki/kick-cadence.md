topic: kick-cadence
status: open
closed-by:
<<<<<<< main
valid-while: crates/universe@595fdd47 + cbe6's patch (examples/beltcad.rs) + ddeb's patch (examples/beltcensus.rs) + this run's patch (examples/beltzone.rs)
updated: 20261021-1443-dynamics-99d7
=======
valid-while: crates/universe@595fdd47 + cbe6's patch (examples/beltcad.rs) + ddeb's patch (examples/beltcensus.rs) + this run's patch (examples/zonecad.rs)
updated: 20261021-1443-second-20261021-1346-taleb-ddeb-f867
>>>>>>> 20261021-1443-second-20261021-1346-taleb-ddeb-f867

# Kick cadence: how often a body is kicked, and by what rule

## Current best

<<<<<<< main
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
=======
**NEW (f867, second author on ddeb — the checker's named experiment flown, the interval pinned):
EVERY fine class of the plane's belt floors at the step-4 dial — which the engine counts at
~33 kicks per Giant-period (≈11/belt-orbit ≈16/conjunction; checker-measured: 329 kicks per
10 planet-periods per ship, `stats.kicks`; cbe6's own record 19,772/100P/6 ships = 32.95 —
the "16/GP ≈ 8/conjunction" label, cbe6's and inherited here, is one octave low) — on B12's
frozen 1e-4 bar: the 3:1 zone including its centre (worst scaled Jacobi 0.9–3.2e-5), the
interior bridge to 4.1 Hill (1.2–2.9e-5), the e-tail to e=0.4
(2.0–8.1e-5) — n⁻² ladder (×4.3/octave), step 3 fails everywhere, no walk at 4× horizon, zero
deaths/refusals, Δe cadence-independent inside the zone (the resonant pump is real dynamics).
Instrument = cbe6's beltcad verbatim (control reproduces cbe6 to the digit), belt drawn from
the shipped birth law (`ladder_ship`), kept by ddeb's census predicates.** Composed rate
**~21.9 events/body/belt-orbit (both combs) → headroom ≈410×** — checker-recomposed at the
measured dial rate (~33 kicks/GP for every class; the author's 10.73/838× prices every class
at the 16/GP label; one octave finer ≈205×; the plane's own 2,700 scale identically; seeds
1/2/3 identical). The belt is ONE cadence class: 99.7% of bodies at the step-4 dial (~33/GP;
strong <4.1 Hill, 0.26%, kept at 64 unmeasured — cbe6's 1.5–3 Hill control died at step 4;
first-order none, D1=0, 0.148 AU margin). **67be's uncertifiability scopes to FIRST
order; q=2 at game scale is conjunction-certifiable.** Width-insensitivity: the bill no longer
depends on the zone-width model — only first-order EXPOSURE does (checker: ×2 window → 2.9%
first-order → headroom 0): placement, not cadence, is the cliff.
[f867 checker: the dial-rate label is off 2× and it is load-bearing — Δs = 2⁻⁵·P_G (≈33
kicks/GP) is the certified constant; 2⁻⁴·P_G (≈16.5/GP) is the FAILING step-3 dial (clean belt
1.8e-4, zone 5.6e-4–1.9e-3). ddeb's 78× is nearly unchanged by the correction (its bill was
256/own-orbit-dominated); f867's 838× halves to ≈410×. The retraction itself is unaffected:
the PASS/FAIL ladder is dial-based, physics-absolute.]
**Standing (ddeb):** the census fractions — 17.8% resonance (3:1 9.4%, 4:1 3.4%, 5:2 2.9%),
41.0% Hill bridge, 0.26% strong tide, first-order exactly 0; the plane's own 2,700 match;
frozen at birth on any playable horizon; the placement cliff ([3.0,3.5) dies 53.8%
first-order; [1.4,2.4) 6.2% fine, 231×).
**Standing (1fd7):** at the measured floor the kick-comb row of the 1e9 single-doll era ledger
lands UNDER budget (0.78× at the page-measured 45.5 µs/kick; payload-conditional bars f_fine ≤
0.6–1.6%, S ≥ 3.4–4.6 yr — the shipped plane's own forcing P_D 77.24 d stays 15–20× over); the
scan channel is cadence-invariant, so the desync must land WITH the tier, not instead of it.
**Standing (cbe6):** the step-4 dial is the belt's own floor and the binding unit is the
conjunction (~16 per conjunction at the true rate; cbe6's "16/planet-period ≈ 8/conjunction"
headline label is one octave low — its own 19,772 kicks/100P/6 ships = 32.95/GP) — now extended
by f867 from cbe6's clean circles to the whole shipped belt population, resonant zone included.

Checker-confirmed domain (cbe6): step-4 PASS at 4× horizon; exact 3:1 commensurability passes
(7.9e-6); the e-draw to 0.23 passes at step 4 (3.2e-5) — f867 extends to the shipped Rayleigh
draw at its zone/bridge/e-tail classes and to e=0.4.
Consequence: the class certificate is conjunction-sampled at ONE constant for the belt
(2⁻⁵ of the planet-period grid — checker-corrected from 2⁻⁴; see the bracket above), and one
doll-wide Δs overpays it ~400-fold (the anchor is the board's measured 9,000/orbit): the
desync's belt constant is measured, not assumed — landing it in `ext::constants` is the
remaining step.

## Refuted

- **"The composed belt headroom is 78×, not ~10³" (ddeb's headline correction): refuted by
  measurement — the zone (q≥2) floor is not 256/own-orbit but the belt's own step-4 dial
  (~33 kicks/Giant-period; the 3:1 and its centre measured; weaker q≥3 zones borrow it
  conservatively — checker flew the 5:2 directly: 2.6e-5 PASS at step 4, fails at 3), and the
  headroom pins to ≈410× at the dial-true rate (f867 + checker). The artifact was B13's
  encounter floor borrowed for the resonance class. ddeb's census fractions, its bit-for-bit
  record, and its placement cliff stand.**
- **"The desynchronised grid relieves the 1e9 ledger beyond its kick row": refuted by
  composition — the scan channel (walks 111–311× + answers 61×) is cadence-invariant; the wall
  moves to the tier's row, the ledger does not close (20261021-1346-library-1fd7).**
- **"The desync's rescue is scene-unconditional": refuted — closure iff the governing synodic
  period ≥ 3.4–4.6 yr (payload-conditional; the shipped plane's own forcing is P_D 77.24 d:
  its kick row stays 15–20× over at the floor) (1fd7 + checker).**
- "Deep passages need ≥ 128/orbit" as the encounter floor: 256 passes, 1024 passes, 512
  fails one row; the shipped 128 is outside every window (7076 + checker).
- The duplicate-mint delete: 0 identical keys in 3.4M belt kicks at every Δs octave and
  both seeds; formations duplicate at birth only (9edc, 225d, efd4).
- "If BELT_SPLIT does not stretch the boundary comb it dominates": the boundary is the
  kick's own midpoint; every identity exact across three octaves (de7b).
- e7ef's 5.1–8.65-core composition: two combs (+25–26%) and the belt's real delete 38.5%
  recompose to 10.3 M1 cores at split 8 (4e2d); the crest is not an average (8ffc).
- a4ed's "belts pass 10⁹ at 10×": 17–49× clock artifact — the shipped doll grid is 17–91×
  denser in own-orbit units (4093); the year-scale rate is the average only (9e75).
- The wave train as a dial output: genesis phase-lock, deleted by the stagger (f82a/ed3a).
- The sub-quantum accumulator as a living belt mechanism at the flown grid (3294);
  deferral under a quantum walks energy (67f2); impulse-quantum sizing (27ce);
  state-fed-back and level-triggered per-body cadence (0713, 54d9, 83f9, 71b4 — the trigger
  walks too, 524e's contrary record is a machine artifact); single-constant synodic rule
  (1db4); conjunction-scheduled belt cadence with zero-kick secular kernel (06a8);
  "manufactured chaos" (f2e3); window-gated 6–9/orbit (9205, unbacked); deferral
  certificate (e5a2); the τ-crossing moon measurement (0102, broken layer); free resonance
  detector (0510); cadence rules near resonance vs the oracle ceiling (67be — now scoped to
  first order by f867).

## Open directions

1. **The census and the floors are flown (ddeb + f867): one dial, the belt's step-4 (~33
   kicks/Giant-period), for 99.7% of the belt; headroom ≈410× at the dial-true rate (838× at
   the inherited 16/GP label) measured on cbe6's instrument.** Remaining edges: the
   libration-scale horizon (checker flew 800 P: zone worst 2.6e-5, centre 3.4e-5, bounded —
   ≥3× margin, no walk; a B12 v3 Allan rule on the zone series would close it further);
   per-zone floors for q≥3 (borrowed
   conservatively from the 3:1 — checker flew the 5:2 directly: PASS 2.6e-5 at step 4);
   the strong tail <4.1 Hill (0.26%, bill share 0.11 events);
   and landing the constant in `ext::constants` on the plane (the composed ≈410× is a
   restricted-scene number; Cinder/Home/Moon tides are ~50× weaker at belt distance, cbe6's
   bound). Then the desync's belt row composes with 1fd7's tier row.
2. The stagger's B-gate flight (od 8 prior; exact in the stationary measure) and its
   observer clause; the compute-ahead certificate (headroom 10.8× at 3×10⁵, 308× short at
   10⁹).
3. The kick mint's outright deletion (the ratchet's target; 225d); efd4's birth-scoped
   intern under concentration; unflown edges S ≥ 10, the Trojan formation, near-resonant
   belts as the unsafe edge of both levers.
4. The encounter class's exit from the metronome (7076's od 9: step 8 flyby tubes or the
>>>>>>> 20261021-1443-second-20261021-1346-taleb-ddeb-f867
   exact pair event); B14's judge path (od 10).
6. Secular deletion at scale (5030's T_sec/20..T_sec/5 certificates, unmeasured on shipped
   code); the trigger-walk mechanism (71b4, |g|-weighted firing untested).

## Contradictions

- What ranked needed cadence in belts: behaviour unfolding within the horizon (3a4c) vs
  compiled-frequency resonance gating (1db4, 67be) — reconcilable as "birth scalars fail,
<<<<<<< main
  frequencies gate"; measure both on one sample. 99d7 + checker2 sharpen it: the gate's
  frequency label must be the TRUE island's (the pendulum flag over-covers ≈3× at e 0.2,
  and the island captures — so membership gates, capture re-derives).
=======
  frequencies gate"; measure both on one sample. f867 sharpens it: the gate is first-order
  only at game scale (q=2 holds at the conjunction floor).
>>>>>>> 20261021-1443-second-20261021-1346-taleb-ddeb-f867
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
- 20261008-0945-library-51bf (lead): no dimensionless number orders the needed kick rate; per-body tuning caps at 1.92×.
- 20261009-0621-system-7f97 (silver): integer-plane frontier regime-split 8× (bulk 16/period, passages ≥ 128); one doll-wide Δs overpays everywhere.
- 20261009-1936-dynamics-5030 (silver): averaged-layer cadence is kicks per secular period (N_lib 4–10, shear order); Euler compounds; Kozai uncertifiable.
- 20261010-1152-dynamics-ad35 (silver): non-resonant tide error is systematic ~0.5·n^-2.1, μ- and R-independent; 4/16/64 disagreement is seed noise.
- 20261010-1302-library-a2ec (silver): per-body certificate t* = √(2q/a_bound) oracle-tight 1.65×; unpriced as shipped (3.5–30× cost).
- 20261010-1816-dynamics-3a4c (silver): belt cadence set by behaviour unfolding within the horizon; no birth-element Chirikov scalar ranks it.
- 20261010-2052-library-2d94 (silver): Whalley–Wilmott deviation band cuts 2.8–6.7× open loop; closed-loop trigger is clairvoyant, certificate breaks.
- 20261010-2141-dynamics-cd52 (silver): cold belt has no clean fixed-cadence point; sub-resolution conjunctions corrupt at every cadence.
- 20261010-2314-library-e5a2 (lead): deferral certificate's headline is a units artifact; its own kill criterion fired.
- 20261010-2314-second-20261010-2141-dynamics-cd52-f2e3 (gold): no-clean-point confirmed bit-exact; "manufactured chaos" refuted — λ real, monotone in K = Δa/R_H.
- 20261011-0224-library-213e (silver): certificate-sized windows cost 33/132/704 evals/orbit at e = 0/0.3/0.7 (1.5–2.4× the headline).
- 20261011-0836-spacex-0c44 (silver): no fixed cadence passes plane gates; cost lever is one full cycle rebind per kick (43 µs).
- 20261011-0924-second-20261011-0836-spacex-0c44-c01c (gold): fixed-cadence search dead; B14 budget law-dominated (×2 per step); refusals multiply with cadence.
- 20261011-2235-library-54d9 (gold): state-fed-back per-body cadence walks (1,548× at matched cost); precomputed-from-constants stays on curve.
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
- 20261008-0615-library-83f9 (silver): level-triggered scheduling from field derivatives killed; 560k/500k kicks vs the clock's 160k.
- 20261008-1419-dynamics-5cbd (silver): quiet belt interior k = 16–32/orbit set by secular resolution, not surprise time.
- 20261008-1613-library-524e (silver): impulse-quantum trigger 3.4× fewer kicks at matched error, no differential walk.
- 20261010-1816-system-67f2 (gold): deferring a kick walks energy linearly (1.01 vs 0.07); no operating point; timing error forbidden.
- 20261012-1227-system-8685 (silver): interaction clock regime-dependent; tick-quantized averages alias; conjunction windows buy nothing.
- 20261014-2012-dynamics-71b4 (pending grade): 524e-vs-54d9 resolved: the impulse-quantum trigger walks in a bounded kernel (slope 0.89–0.92, D 8–23× clock, checker2-corrected ratios); 524e's machine had no bounded control.
- 20261015-0724-system-3294 (this run, awaiting grade): no sub-quantum regime anywhere in the flown plane — fire rate 1.000, impulses ≥ 2⁷ units, four arms; the belt interval is the doll grid (28,141.5 s median); the train genesis-locked (50% of fires in 0.9% of the interval) and shearing 3× per wave; cadence, kick cost, wave tail and scar rate are one dial spanning ~4 orders at 10⁹.
- 20261015-1338-second-20261015-0724-system-3294-f82a (awaiting grade): 3294's record regenerates to the digit; belt impulses 2⁻²³ of speed (fire-gate cannot bind before the behaviour gates); staggered genesis flattens the train (57×→1.0×) and deletes the 10⁵ tail for free.
- 20261016-1835-fermi-4093 (fermi, this run): the crest, not the average — belt silent
- 20261016-2138-fermi-e7ef (fermi, this run): the 10⁹ CPU ledger closes on measured levers (kick 9–23 µs suffices, floor irrelevant at 10⁹); encounters-on-graded-levers and memory floors do not close; the ladder wall = 6–8 GB ÷ plateau, exactly.
- 20261016-1835-fermi-4093 (silver): the crest, not the average — belt silent below 11.4 k game-s, first kicks at ≈ interval/2, the budget clamps at ~230 events/frame; a4ed's 10⁹-passing sentence is a 17–49× clock artifact; N1's 20-s window is pre-crest.
- 20261016-2138-second-20261016-1835-fermi-4093-9e75 (this run): the freeze measured directly — spell 7.0–7.1/21.9–22.1 s at 10⁵/3×10⁵, law ratio 1.01–1.04, deficit replaces the saturated lag, crest linear in N (3.08–3.09), 10⁶ = 72–73 s, 10⁹ = 20.1–20.3 h / 185–187 cores at rtf 100; the burn arm has no freeze — the crest overruns the budget instead (max ~2.5 s, truncated, 5.9 GB).
- 20261016-2229-second-20261016-2138-fermi-e7ef-98cb (this run): the composition flown — freeze cured (21.1→0.1 s spell, 99% delivered), ÷8.00 interval direct, b583's lever absent from the belt (fires N-independent, Ĉ flat); 10⁹ still 22.5/8.8 x86, 13.2/5.1 M1 cores.
- 20261017-0005-dynamics-8ffc (this run, awaiting grade): the crest decided — a two-comb
- 20261017-0552-fermi-4e2d (fermi, this run): the 10⁹ ledger recomposed — 10.3 M1 cores at flown legality (2.6× over), encounters closed on the adjudicated anchor (source-verified), dwell window [~100, ~115] gs at split 8 (razor); one dial (split ≥ 21×) closes CPU and memory together.
- 20261017-1149-fermi-de7b (fermi, this run): the boundary comb rides the step lever (3 octaves, per-body identities exact, 100% of bodies); the 10⁹ pinned-boundary floor is dead; riding stands — 9.96 M1 cores at split 8, S* ≈ 19.9×.
- 20261017-1240-second-20261017-1149-fermi-de7b-f790 (second author): the named misses closed — BELT_SPLIT flown directly (8× both combs, identities exact, 9,700/9,700), seeds 2–3 identical, record byte-reproduced; gold stands.
- 20261017-2038-components-3570 (components, silver): the boundary comb census — 99.88% no-op, 27.8% of belt resolver CPU for 0 bits; key-range design priced; checker: no-op holds at N=3×10⁴ (99.96%) and on the burn arm (99.91%), news class = Passage bodies (~25 fixed, 269/275), coverage headline corrected; gold awaits the kick-time key-range test flown.
- 20261018-0143-components-16ec (components, gold): the key-range test flown as a
- 20261018-0431-second-20261018-0143-components-16ec-49e9 (second author): the burn question closed — pinned-decision harness (`schedule` at a canonical tick) proves the fast path digest-neutral on thrusting populations (1198b23e ×4, 100% skip, 338 passages read), the divergence mechanism measured both sides (equal tick → equal digest; unequal → unequal), the slow_cycle refusal branch flight-proven (5,126 refused, digest identical), and the decomposition regenerates (clock_share 0.166–0.187 from one command).
- 20261019-1906-spacex-9edc (spacex, awaiting grade): the kick comb is 100% news — 0/2.04M
- 20261019-1906-spacex-9edc (spacex, silver): the kick comb is 100% news — 0/2.04M identical
- 20261019-2017-second-20261019-1906-spacex-9edc-225d (second author): the named experiment run
- 20261020-0036-scout-7076 (scout, awaiting grade): the cadence ladder flown on the frozen certificates — tide class legal to split8 with margin (B17 cliff at 16×: libration 0.981→0.023), encounter class legal only at 256/orbit (B13 64/64 at step 8; the standing red is cadence-curable; collapse 42/15/3/1 coarser); Carlson's 4.9 µs bar stays the only closure path.
- 20261020-1326-inversion-3b88 (inversion, awaiting grade): B13's step-9 inf = the i64 tick wall on near-escape orbits (period 3.2e19 > 2^63 ticks; 1-2 of 229 draws per octave, the gate-window lottery decides the verdict); the cure is law-side, not cadence.
- 20261020-1503-second-20261020-1326-inversion-3b88-cca6 (second, awaiting grade): the named experiment flown — Ok(None) deletes the wall's lost-ship class (0/229 at steps 7–10; B13 step 9 PASS 1.33e-3; steps 8/10 rows bit-identical); 77 crate tests pass under the fix (`--lib --tests`: 77/0/4; checker2 — the author's "46" is a partial sum, and the plain full command hits the pre-existing Linux link failure of the nladder example); record repaired, clean-tree regen exit 0.
- 20261007-0128-b-b17-parallel-cee8 (missing): checker died at a 429; never graded.
- 20261007-0341-scout-9abe (silver): jerk-triggered 2.5–4 kicks/orbit off resonance; resonance contrast later shown artifact.
- 20261008-0458-second-20261008-0338-library-f045-0102 (silver): kills library-f045's τ-crossing moon-cadence measurement; broken Kepler layer.
- 20261010-1302-library-a2ec (silver): per-body certificate t* oracle-tight 1.65×; unpriced as shipped.
- 20261010-2052-library-2d94 (silver): Whalley–Wilmott band cuts 2.8–6.7× open loop; closed-loop trigger clairvoyant.
- 20261010-2314-library-e5a2 (lead): deferral certificate's headline is a units artifact.
- 20261010-2314-second-20261010-2141-dynamics-cd52-f2e3 (gold): no-clean-point confirmed; "manufactured chaos" refuted — λ real, monotone in K.
- 20261011-0224-library-213e (silver): certificate-sized windows 33/132/704 evals/orbit at e = 0/0.3/0.7.
- 20261011-0836-spacex-0c44 (silver): no fixed cadence passes plane gates; cost lever is one full cycle rebind per kick.
- 20261011-0924-second-20261011-0836-spacex-0c44-c01c (gold): fixed-cadence search dead; B14 budget law-dominated.
- 20261011-2235-library-54d9 (gold): state-fed-back per-body cadence walks; precomputed-from-constants stays on curve.
- 20261012-1340-second-20261012-1227-system-8685-2eb1 (gold): orbit-anchored discrete secular kicks kill tick aliasing; K ≥ 16.
- 20261002-1618-scout-f341 (silver): smooth regimes need no new scheme — leapfrog 16/orbit holds every gate.
- 20261003-0520-components-13ae (silver): evection harmonic holds 10% apsidal to 0.20–0.25 R_H at 0.3–2.9 events/moon-orbit.
- 20261003-0520-dynamics-a9c2 (silver): frequency crossings set the cadence cliff; λ-trigger chance-level.
- 20261003-2306-system-27ce (silver): plane over-provisioned (flying 1/128, floor n = 8); impulse-quantum sizing falsified.
- 20261004-0555-quant-5022 (silver): 1/64 is the uniform cliff on the near-2:1 band; quiet floor 2 events/orbit.
- 20261004-0555-spacex-450b (silver): no splitting order buys the 4×.
- 20261004-1525-scout-2098 (silver): moon frontier 4–6/orbit through 0.3 R_H robust.
- 20261004-2311-spacex-de5b (silver): WHFast correctors 0×, Yoshida-4 1.33×.
- 20261005-0543-library-bb03 (lead): "no schedule beats uniform-time" refuted — left-endpoint artifact.
- 20261005-1404-q-plane-judge-65fd (silver): shipped plane fails frozen gates at every cadence.
- 20261006-0220-redteam-fermi2-v2-b7a4 (gold): strong-field tide cadence law; 3047→421.
- 20261007-0933-system-0510 (silver): conjunction calendar 0.57 events/orbit; free resonance detector falsified.
- 20261007-1032-second-20261007-0933-system-0510-53f6 (silver): (de, dϖ) form fails tails; e-vector fixes rate.
- 20261008-0615-library-83f9 (silver): level-triggered scheduling killed; 560k/500k vs 160k.
- 20261008-1419-dynamics-5cbd (silver): quiet belt interior 16–32/orbit set by secular resolution.
- 20261008-1613-library-524e (silver): impulse-quantum trigger 3.4× fewer kicks at 100-orbit horizon.
- 20261010-1816-system-67f2 (gold): deferring a kick walks energy linearly; no operating point.
- 20261012-1227-system-8685 (silver): interaction clock regime-dependent; conjunction windows buy nothing.
- 20261014-2012-dynamics-71b4 (pending): the impulse-quantum trigger walks too (slope 0.89–0.92); 524e's machine had no bounded control.
- 20261015-0724-system-3294 (awaiting grade): no sub-quantum regime in the flown plane — fire rate 1.000, impulses ≥ 2⁷ units; the belt interval is the doll grid.
- 20261015-1338-second-20261015-0724-system-3294-f82a (awaiting grade): belt impulses 2⁻²³ of speed; staggered genesis flattens the train and deletes the tail.
- 20261016-1835-fermi-4093 (silver): the crest, not the average — belt silent below 11.4 k game-s; a4ed's sentence a 17–49× clock artifact.
- 20261016-2138-fermi-e7ef (silver): the 10⁹ CPU ledger closes on measured levers (kick 9–23 µs suffices); encounters and memory floors do not close.
- 20261016-2138-second-20261016-1835-fermi-4093-9e75 (silver): the freeze measured — spell 7/21–24 s, law ratio 1.01–1.04, crest linear in N, 10⁹ = 20 h.
- 20261016-2229-second-20261016-2138-fermi-e7ef-98cb (silver): the composition flown — freeze cured; 10⁹ still 22.5/8.8 x86 cores.
- 20261017-0005-dynamics-8ffc (silver): the two-comb train decided — 1+1 events/body/interval, +26% CPU.
- 20261017-0552-fermi-4e2d (silver): the 10⁹ ledger recomposed — 10.3 M1 cores at split 8; one dial closes CPU and memory together.
- 20261017-1149-fermi-de7b (silver): the boundary comb rides the step lever; the pinned-boundary floor dead.
- 20261017-1240-second-20261017-1149-fermi-de7b-f790 (second author): BELT_SPLIT flown directly; seeds identical; gold stands.
- 20261017-2038-components-3570 (silver): the boundary comb census — 99.88% no-op, 27.8% of resolver CPU for 0 bits.
- 20261018-0143-components-16ec (gold): the key-range test flown — 100% skip, 202 ns, digests identical on coast.
- 20261018-0431-second-20261018-0143-components-16ec-49e9 (second author): burn closed — the fast path digest-neutral on thrusting populations.
- 20261019-1906-spacex-9edc (silver): the kick comb is 100% news — 0/2.04M identical re-fits.
- 20261019-2017-second-20261019-1906-spacex-9edc-225d (second author): the resolution coupling dead across the flyable range; formation duplication birth-only.
- 20261020-0036-scout-7076 (awaiting grade): the cadence ladder on the frozen certificates — tide class to split8, encounter class only 256/orbit.
- 20261020-1326-inversion-3b88 (awaiting grade): B13's step-9 inf = the i64 tick wall on near-escape orbits; the cure is law-side.
- 20261020-1503-second-20261020-1326-inversion-3b88-cca6 (second, gold): Ok(None) deletes the wall's lost-ship class; record repaired.
- 20261021-0607-system-cbe6 (system, this run): the belt's own floor on the shipped instrument — 16/planet-period ≈ 5/orbit ≈ 8/conjunction (PASS both draws), 4/conjunction fails; conjunction-sampled certificate, ~10³ desync headroom vs the doll grid.
- 20261021-1346-library-1fd7 (library, silver): the desync ledger composed — the kick row
- 20261021-1346-taleb-ddeb (taleb, awaiting grade): the fine-class census — 17.8% resonance tail + 41% unflown Hill bridge; composed desync headroom 78× (not ~10³); first-order 0, margin 0.148 AU; a belt at the 2:1 dies (54%).
- 20261014-2012-dynamics-71b4 (pending grade): 524e-vs-54d9 resolved: the impulse-quantum trigger walks in a bounded kernel (slope 0.89–0.92, D 8–23× clock, checker2-corrected ratios).
- 20261015-0724-system-3294 (awaiting grade): no sub-quantum regime anywhere in the flown plane — fire rate 1.000, impulses ≥ 2⁷ units; the belt interval is the doll grid.
- 20261016-2138-second-20261016-1835-fermi-4093-9e75 (silver): the freeze measured — spell 7/21–24 s, crest linear in N, 10⁹ = 20 h.
- 20261017-2038-components-3570 (silver): the boundary comb census — 99.88% no-op, 27.8% of belt resolver CPU for 0 bits.
- 20261020-0036-scout-7076 (awaiting grade): the cadence ladder flown on the frozen certificates — tide class to split8, encounter class only 256/orbit.
- 20261021-0607-system-cbe6 (system, gold): the belt's own floor on the shipped instrument — 16/planet-period ≈ 8/conjunction (PASS both draws), 4/conjunction fails; conjunction-sampled certificate.
- 20261021-1346-library-1fd7 (library, silver): the desync ledger composed — the kick row under budget at the floor; the wall moves to the scan channel; closure bars payload-conditional.
- 20261021-1346-taleb-ddeb (taleb, awaiting grade): the fine-class census — 17.8% resonance tail + 41% Hill bridge; first-order 0, margin 0.148 AU; a belt at the 2:1 dies (54%).
- 20261021-1443-dynamics-99d7 (dynamics, silver per checker2): arms flown displaced (OrbitSpec latus-rectum semantics); checker re-flight: zone and bridge certify at 16 at true placements, capture real (Δe 0.072/100p); headroom ≈550× checker-flown.
- 20261015-0724-system-3294 (silver): no sub-quantum regime anywhere in the flown plane — fire rate 1.000, impulses ≥ 2⁷ units, four arms; the belt interval is the doll grid (28,141.5 s median); the train genesis-locked and shearing 3× per wave.
- 20261015-1338-second-20261015-0724-system-3294-f82a (silver): 3294's record regenerates to the digit; belt impulses 2⁻²³ of speed; staggered genesis flattens the train (57×→1.0×) and deletes the 10⁵ tail for free.
- 20261016-1835-fermi-4093 (silver): the crest, not the average — belt silent below 11.4 k game-s; a4ed's 10⁹-passing sentence a 17–49× clock artifact.
- 20261020-0036-scout-7076 (silver): the cadence ladder flown on the frozen certificates — tide class to split8, encounter class only 256/orbit.
- 20261020-1326-inversion-3b88 (silver): B13's step-9 inf = the i64 tick wall on near-escape orbits; the cure is law-side.
- 20261021-0607-system-cbe6 (gold): the belt's own floor on the shipped instrument — 16/planet-period ≈ 8/conjunction; conjunction-sampled certificate, ~10³ desync headroom vs the doll grid.
- 20261021-1346-library-1fd7 (silver): the desync ledger composed — the kick row under budget at the measured payload; the wall moves to the scan channel.
- 20261021-1346-taleb-ddeb (silver): the fine-class census — 17.8% resonance tail + 41% Hill bridge; composed headroom 78× on borrowed floors; first-order 0, margin 0.148 AU; a belt at the 2:1 dies (54%).
- 20261021-1443-second-20261021-1346-taleb-ddeb-f867 (second author on ddeb, this run): the checker's named experiment — every belt fine class floors at the step-4 dial (zone 3:1, its centre, bridge to 4.1 Hill, e-tail to 0.4, and checker-flown 5:2); headroom ≈410× dial-true (author's label: 838×); ddeb's 78× retracts, its census and cliff stand.
