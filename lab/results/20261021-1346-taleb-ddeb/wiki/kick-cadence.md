topic: kick-cadence
status: open
closed-by:
valid-while: crates/universe@595fdd47 + cbe6's patch (examples/beltcad.rs) + this run's patch (examples/beltcensus.rs)
updated: 20261021-1346-taleb-ddeb

# Kick cadence: how often a body is kicked, and by what rule

## Current best

**NEW (ddeb, taleb — od 1 executed, the deletion's missing half): the fine-class census on the shipped birth law (`ladder_ship`'s belt arm verbatim × `PLANETS`): the plane's belt's fine tail is 17.8% — the Giant's 3:1 zone alone 9.4% of bodies, 4:1 3.4%, 5:2 2.9%, 7:3 1.0%; first-order exactly 0 (the 2:1 zone starts at 3.148 AU: the belt's margin is 0.148 AU) — plus a 41.0% Hill bridge at 5.4–6.3 Hill (below cbe6's certified 6.3–8.8 draws: the plane's Giant, e 0.05 at 5.194 AU, dips to 4.936) and 0.26% strong tide (< 4.1 Hill); 0 crossings by construction; seeds 1–3 ±0.1%; the plane's own 2,700 bodies match (17.6/19.3%).**
Composed desync rate 115 events/body/belt-orbit (both combs) against the 9,000 anchor: **headroom 78×** (90× if the bridge certifies at 16; 170× if zone bodies hold at 64 — checker reads 190–290× there, so the bracket is conservative) — the 17.8% tail pays 79% of the bill, the certified-clean 41% pays 3.3% (checker-instrumented; the dossier's 75/21/4 mis-normalises). Width: robust at the nominal model (×0.5 → 122×; at ×1 D1 stays exactly 0 with the 2:1 included), but the ×2–×4 sweep is blind to the Giant's 2:1 (the candidate window hi·1.06 = 3.18 excludes a_res 3.273): included, ×2 already puts 2.9% of the belt first-order → headroom 0. Worst cell: bins on a zone run 90–98% fine (per-cell cadence bimodal; the population mean is nobody's rate). Frozen at birth to any playable horizon (synodic 3.75–9.6 yr ≫ 10⁶ game-s).
Placement cliff (design arms): a belt [3.0,3.5) is 53.8% first-order (2:1) — uncertifiable at any cadence, headroom 0; [1.4,2.4) is 6.2% fine, 231×. The zone floor for q ≥ 2 (256 vs 64) and the bridge floor (5–6.3 Hill, interior) are the two unflown arms that pin the 78–170× interval.
[checker, reproduced bit-for-bit: seeds 1–5 (4/5 held-out: f 0.1794/0.1785, 78×), widths 0.25–8 (170×/21×, monotone), both arms, the plane's 2,700, and a widened-window probe (2:1 included): D1 = 0 at ×1; the dossier's prose zone centres are off (2.521/2.764/2.917 vs code 2.498/2.821/2.953 — counts untouched).]
**Standing (cbe6, system — the belt's own floor measured on the shipped instrument, the board's named gap: 16 kicks per planet period ≈ 5 per belt orbit ≈ 8 per synodic conjunction PASSes B12's frozen 1e-4 bar on two draws (worst 9.4e-6–1.3e-5), while 8/planet-period (4/conjunction) fails (1.8e-4); n⁻² to the floor, super-quadratic aliasing beyond (×15/×38/×1900); the binding unit is the conjunction.** `beltcad.rs` = the `jacobi` example's scene/rng verbatim + radius-class axis + SEED dial + Δe tracker; belt = interior 2–3 AU radii (6.2–9 Hill from the planet; draws 6.3–8.8), **circular starts — the plane's belt adds Rayleigh e≈0.07, untested here**; strong-class control reproduces 7076 to the digit (5.1e-6@6, 1.8e-5@5) with the cliff as deaths at step 4 (2/6); the secular e-pump is step-independent per ship (a control: only sampling error moves with the step); zero captures/losses/refusals at passing octaves.
Checker-confirmed domain: the step-4 PASS holds at 4× the horizon (worst 1.2e-5 over 400 periods, no walk) and on an exact 3:1 commensurability (7.9e-6); 72 further draws (two 36-ship runs) all pass (8.3e-6–1.6e-5); the strong control's step-4 cliff is robust (8/36 dead).
[checker2: blind reproduction bit-for-bit (all 11 arms, clean tree); the run's named gaps closed from above — the plane's hauler e-draw (e = 0.25·lcg via `e_q48`, e0 0.02–0.23) PASSES at step 4 (worst 3.2e-5, both seeds) and fails at 3; exterior circles 6.5–7.5 AU (never flown, 4.1–6.3 Hill outside) PASS at step 3 (2.6–3.4e-5) and fail at 2 — ≥1 octave coarser, the conjunction unit's direction, though this one point does not discriminate conjunction from own-orbit beyond ~2× at unequal Hill distances; 1000 periods no walk (1.2e-5 at step 4, unchanged); 72 fresh draws max 1.6e-5. Grade: gold.]
Consequence: the class certificate is conjunction-sampled, and one doll-wide Δs delivers ~9,000 kicks/belt-orbit (board's plane-scene anchor) — the desynchronised grid's belt headroom is ~10³ (split8 is 2 orders short; a cross-scene composition, both anchors measured), and it is one constant per class (`ext::constants`): the clocks, fired gate and intervals are already per body.
Standing: **cca6 gold** — the i64 tick wall's lost-ship class deleted by one branch (Ok(None)), 0/229 at steps 7–10, B13 step 9 PASS 1.33e-3, bit-identical brackets.
**7076** — the cadence ladder on the frozen certificates: tide class legal to split8 (B17 cliff at 8/orbit by libration collapse), encounter class only 256/orbit (B13 PASS 64/64 worst 5.30e-3; step 10 passes 3.32e-4); B14 wall is the judge.
**225d/9edc** — the kick comb is 100% news (0 duplicate keys in 2.04M+1.40M kicks at every Δs octave; formation duplication birth-only); the mint (~2.1 KB/binding) is the ratchet's deletion target.
**3570/16ec/49e9 gold** — the boundary comb is 99.88% no-op; the key-range test flown, 100% skip, 202 ns, digest-neutral (20.3×); burn closed by the pinned-decision harness; clock-path boundary 4.4–5.6 µs; the boundary rides every step lever (de7b/f790, welded pairs exact, 3 seeds).
**8ffc/9e75/4093** — the belt's stream is a two-comb train (1+1 events/body/interval, +26% CPU); the crest a freeze (spell ≈ N·C/0.72: 7 s at 10⁵, 21–24 s at 3×10⁵, 19.3 h at 10⁹; burn inverts to overrun).
**3aec/4e2d/e7ef/98cb** — the 10⁹ ledger: closure = cadence cut AND ≤ 4.9 µs/event; kick cost and cadence are one product (÷ ≤ 1.13 µs); split8 composition 10.3 M1 cores, S* ≈ 20×. **3294/f82a** — no sub-quantum fire anywhere flown (rate 1.000, impulses ≥ 2⁷ units); the wave train is genesis phase-lock, deleted at birth by the hash stagger.
Replica/probe priors: non-resonant tide error ρ ≈ 0.5·n⁻²·¹ μ-independent (ad35); far belt ~2/orbit on B14 (1db4); Jupiter-belt replica 8/orbit (06a8); resonance uncertifiable at any cadence (67be); the frontier is regime-split 8× with one doll-wide Δs overpaying everywhere (7f97).

## Refuted

- "The desynchronised grid's belt headroom is ~10³" (cbe6's consequence sentence, the board's
  macro row): the fine-class census prices the composed rescue at 78× (90–170× by floor choice;
  width-robust to ×4) — the 17.8% resonance tail pays 75% of the bill. cbe6's floor itself
  stands; the headroom clause does not (ddeb). 
- "Deep passages need ≥ 128/orbit" as the encounter floor: 256 passes, 1024 passes, 512
  fails one row; the shipped 128 is outside every window (7076 + checker).
- The duplicate-mint delete: 0 identical keys in 3.4M belt kicks at every Δs octave and
  both seeds; formations duplicate at birth only (9edc, 225d, efd4).
- "If BELT_SPLIT does not stretch the boundary comb it dominates": the boundary is the
  kick's own midpoint; every identity exact across three octaves (de7b).
- e7ef's 5.1–8.65-core composition: two combs (+25–26%) and the belt's real delete 38.5%
  recompose to 10.3 M1 cores at split 8 (4e2d); the crest is not an average (8ffc).
- The 42–56 ns kick floor as a 10⁹ requirement; kick cost and cadence as independent gaps
  (e7ef); the kick-cost lever acting on the belt (98cb: b583's search never fires there).
- a4ed's "belts pass 10⁹ at 10×": 17–49× clock artifact — the shipped doll grid is 17–91×
  denser in own-orbit units (4093); the year-scale "trivially affordable" rate is the
  average only (9e75).
- The wave train as a dial output: genesis phase-lock, deleted by the stagger (f82a/ed3a).
- The sub-quantum accumulator as a living belt mechanism at the flown grid (3294);
  deferral under a quantum walks energy (67f2); impulse-quantum sizing (27ce);
  state-fed-back and level-triggered per-body cadence (0713, 54d9, 83f9, 71b4 — the trigger
  walks too, 524e's contrary record is a machine artifact); single-constant synodic rule
  (1db4); conjunction-scheduled belt cadence with zero-kick secular kernel (06a8);
  "manufactured chaos" (f2e3); window-gated 6–9/orbit (9205, unbacked); deferral
  certificate (e5a2); the τ-crossing moon measurement (0102, broken layer); free resonance
  detector (0510); cadence rules near resonance vs the oracle ceiling (67be).

## Open directions

1. **The class census is flown (ddeb, silver-pending): 17.8% resonance (3:1 9.4% of bodies), 41.0%
   Hill bridge (5.4–6.3, unflown for interior geometry), 0.26% strong tide, 0 first-order with a
   0.148 AU margin; composed headroom 78× (90–170× by floor); the [3.0,3.5) belt dies at the 2:1
   (53.8% first-order).** The two unflown arms that pin the interval: the zone floor at the 3:1 on
   cbe6's instrument (16 vs 64 vs 256), and interior draws at 5–6.3 Hill (the plane's own belt's
   outer half). Then the desync constants adopt per class.
2. The stagger's B-gate flight (od 8 prior; exact in the stationary measure) and its
   observer clause; the compute-ahead certificate (headroom 10.8× at 3×10⁵, 308× short at
   10⁹).
3. The kick mint's outright deletion (the ratchet's target; 225d); efd4's birth-scoped
   intern under concentration; unflown edges S ≥ 10, the Trojan formation, near-resonant
   belts as the unsafe edge of both levers.
4. The encounter class's exit from the metronome (7076's od 9: step 8 flyby tubes or the
   exact pair event); B14's judge path (od 10).
5. Secular deletion at scale (5030's T_sec/20..T_sec/5 certificates, unmeasured on shipped
   code); the trigger-walk mechanism (71b4, |g|-weighted firing untested).

## Contradictions

- What ranks needed cadence in belts: behaviour unfolding within the horizon (3a4c) vs
  compiled-frequency resonance gating (1db4, 67be) — reconcilable as "birth scalars fail,
  frequencies gate"; measure both on one sample.
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
- 20261021-1346-taleb-ddeb (taleb, awaiting grade): the fine-class census — 17.8% resonance tail + 41% unflown Hill bridge; composed desync headroom 78× (not ~10³); first-order 0, margin 0.148 AU; a belt at the 2:1 dies (54%).
