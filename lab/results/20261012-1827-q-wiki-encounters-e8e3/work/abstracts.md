
===== 20261006-0030-library-39a2 =====
GRADE-LINES: ['Grade: lead', 'graded lead with *more* library evidence (a real 770-doc Readwise export, five verified quotes) and no measured engine gain; this run has less of the first and the same none of the second', 'grade']
ABSTRACT-130w: Grade: lead **Abstract.** Claim: five lessons from Julien's library aim the allocator/cadence family at unmade decisions, each with a kill-test; two anchors verbatim-verified. Reproduced: fresh Gutenberg fetches are bit-identical to the cached texts (md5 `f476f74e…`, `12742dc1…`); the three quotes are verbatim at :15802, :190, :2653 inside genuine texts (Halsted omnibus #39713; Lefèvre #60979), part/chapter anchors correct; all five books are on `goodreads.csv`; predictions (00:34:16) predate the fetches (00:36:37). But the held-out P1 failed (2/5 verifiable vs ≥4/5 predicted) and P2–P6 are untested proposals: every load-bearing change is already queued or in the docs (least-slack is board #4 verbatim; `q-cadence` and `q-gravity-at-c` own lessons 1 and 4; plane.md §7 owns 3; law.md's open simultaneity owns 5). No engine number was measured. Lead. ## Reasons 1. **Reproduction: clean.** The dossier's commands run


===== 20261006-0220-scout-4ea2 =====
GRADE-LINES: ['Grade: gold', 'graded behaviour the neglected-pull-outside-the-door mechanism predicts']
ABSTRACT-130w: Grade: gold **Abstract.** Claim: B13's near-parabolic failures are an entry gap — the flyby must be an event detected analytically at ≥1.5·SOI, then the plane's in-doll rule holds the 1% gate. Reproduced bit-for-bit: plane 60/64 with the two failing ships at handoffs=0 (kicks 2 and 113); falsifier L3@1.5 59/60, worst 1.4e-2, set B 15/15 at worst 2.4e-3, 65–120 events flat in e_h; star-doll cadence alone 0/60; one-event Öpik ≤7/41. My held-out fresh seed: 58/58, worst 4.9e-3; slow+deep corner 8/8; door sweep 1.0/1.25/1.5 monotone, corroborating the door mechanism. Gain: deletes the per-passage cadence as the flyby's clock (premise shown wrong). Cost: wire crates/encounters detection as the doll door at ≥1.5·SOI; judge by B13. ## Reasons **1. Reproduction (clean tree, no patch to apply — `work/patch.diff` is empty).** - Plane: `PLANE_TRACE=1 …/xtask


===== 20261006-0346-inversion-8cee =====
GRADE-LINES: ['Grade: silver', 'grade below gold even when honestly reported']
ABSTRACT-130w: # Check — 20261006-0346-inversion-8cee Grade: silver ## Abstract Inverted on the r8/q-candidate "zero misses": the shipped encounter check (`crates/encounters`, fixed k = 24/64/256 Δr·Δv sign brackets) misses real encounters exactly where no frozen belt ever looked — 17/241 (7.1%) and 9/167 (5.4%) at e ∈ [0.60, 0.95], 2/3890 on a clustered-phase fleet wall; work per encounter inverts 309 → 505,314 evals (1,600×) across families. All five scenes reproduce bit-exactly; I re-confirmed 16/28 misses with the independent dense finder (all held) and a fresh-seed scene misses 6.3%. `make_belt` caps e at 0.5, so the verification premise is shown wrong. Adopt now: two scene families in every frozen encounter verify set. The certified-step guard is specified but not built — one experiment from gold. ## Reproduction - Built `enc` (byte-identical copy of


===== 20261006-0437-components-2222 =====
GRADE-LINES: ['Grade: silver', 'grades exactly there']
ABSTRACT-130w: # Check — 20261006-0437-components-2222 Grade: silver **Abstract.** Claim: the Binet cone cannot drop in behind `Encounters` as a per-check query. Reproduced: scan 3.4–4.0 µs per candidate, linear (49 ms at n = 12289, exponent 1.01, 5 ms budget dies at ~1250 members); certificates 3.3–10 ms per check, 93× the scan at the plane's n = 10, break-even near n ≈ 3000, only 5× better at 12289; cone candidates saturate (886→904). Decomposed: the U-sweep + cone test is 243 ns; all cost is per-pair `sections`/`first_hit` re-paid per check — the skin framing is right. One correction: of the two "missed encounters", only one is real (present-inside, minimum in the far future, not the past); the other is a scan phantom contact. The belt control the author discarded was valid and exposes


===== 20261006-0437-dynamics-43d5 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** In the law's drift+kick belt, "no work per orbit in the steady state" is false: elastic stirring keeps a Poisson-like kick floor forever, certificate re-setup churn runs ~15–50× real encounters at the m=16 grid, and debris fragmentation turns supercritical at net fragment production > 0. Reproduced bit-identically (elastic s1; frag N2048 K0/K3; controls both sides); held on held-out seed 4, half-density N384, and a 4× horizon. Adoptable now: edit law.md's encounter paragraph, assume Poisson arrivals in the allocator, add the contact-rate × net-fragments readout. Silver: cone-margin 99.9% is a threshold artifact (honest 82–84%), churn ~2× lower, H4 slopes slip (+8.1e-4 → +1.0e-3 at N4096), and the Allan<2 prediction failed on all three seeds, not one. ## Reproduction (clean tree, empty patch.diff) - `conjmap.py --N 768 --orbits 240


===== 20261006-0519-rung-r8-encounters-v4-0e5d : NO check.md (verdict: "Verdict: VOID; the checker's metrics file is missing or unreadable") =====


===== 20261006-0521-rung-r8-encounters-v4-6cd5 : NO check.md (verdict: "Verdict: VOID; the checker's metrics file is missing or unreadable") =====


===== 20261006-0737-components-4643 =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** Kill of the taleb-3ec1 deferral lead on the belt kick workload: pairs are indeed dormant (99.7% of first in-window passages >100 orbits ahead, median 26,000 — reproduced bit for bit), but 92% of per-kick evals are numeric-window *setup*, which calendar wakes re-pay at every kick; deferral's measured ceiling is 1.1–1.2× evals (1.5× wall on my rerun), not the predicted 5×. Analytic zero-setup windows over-fire 427× (276–528× across my probes). The lever stays the slack skin (12.6×, HANDOFF). Adoption is a design decision, nothing to build: drop the wake calendar. Blemish: the dossier's wall-clock digits match no archived log (they regenerate in family); the deferred harness has a disclosed exactness hole the structural argument does not lean on. ## Reproduction Applied `work/patch.diff` to the clean tree, built `dormant`


===== 20261006-1029-dynamics-6875 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the encounters design's steady state ("no work per orbit in the steady state", law.md; r8 v2's "→ 0") does not exist under endogenous kicks. Reproduced bit-exact: all 11 JSONs regenerate identically from the shipped `belt_sim.py` (gm=0 control flat, drift exactly 0; overlap +39–67%, encounters flat; resched/conj 53–61 early → 65–75 late; work/real encounter 2.3–3.6×10⁵ vs 2.2×10³ control). My longer adversarial rerun (1600 orbits) strengthens it: σ_e slope climbs 0.21→0.33 without saturating (κ=0.13), work/encounter 4.3×10⁵. Avalanche wake bounded (+2.9% over 200 orbits, no cascade). Silver on the record, not the physics: the shipped `analyze.py` (edited after the data) cannot regenerate the dossier's headline table, and its Fano column is encounter-based though P4 registered conjunction Fano. Cost to adopt: two design rules (per-quantum re-pay; births re-absorb the heated


===== 20261006-1135-spacex-317c =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** Claim: the slack skin's missing window-width term is ρ_eff = ρ + 1.5·s·r²max (windows are ρ-level sets; drift pads ρ, never edges; Cross shortcut disabled), making the deferred certificate exact at s = 4·eps_u — plane-regime belt 0 missed/0 false of 163, setups/kick 14.95 vs always's 188.6, us/kick 2547 vs the published always's 3312 — while at 100× the kicks it costs more than it saves (fleet 37.9k vs 23.8k µs/kick; belt unfinished in 300 s). I reproduced fleet 1e-4 bit-for-bit (0/1179, checks/kick 485.9), the ring truth control exactly (0/0 of 1506 both sides), and re-seeded adversarial cases (fleet 1e-4: 0/1337; fleet 1e-6, unmeasured by the author: 0/1255, break-even cost). Adoption: one rule plus deleting Cross from deferred certificates; it bounds the 6-October gold's "the lever" to


===== 20261006-1249-library-8f99 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the encounter skin's slack width must be per-pair — re-setup floor at 0.11·a (non-resonant) vs 2.2·a (5:2 resonance), a 55× split. Reproduced bit-for-bit (5 s, <100 MB, deterministic; all dossier numbers match `probe-out.json`); all five library quotes verbatim in the cached corpus. The prescription (width = measured drift per pair, re-estimated at each re-setup; escalate high-drift pairs out of the tier) is sound, cheap and sizes q-skin. But the headline split is confounded: my controls at 2.55/2.85/2.404 (off the strong resonances, same distance from the μ=0.03 perturber) all show the same ~2.2·a floor, and nr's "hard floor" walks linearly (0.11·a at 60 orbits → 0.43·a at 240, e bounded: precession, not amplitude). Adopt the mechanism, not the numbers. ## Reasons **1. Reproduction: exact.** `python3 slack_probe.py` in


===== 20261006-1436-autoresearch-cdf8 =====
GRADE-LINES: ['Grade: lead']
ABSTRACT-130w: Grade: lead **Abstract.** Everything reproduces — all six digests byte-identical, timings within noise — but both central claims fail. First, the saved filter measures A at 1889 vs 1497 ns/item, 26% *slower*: it decodes every skipped pair for its self-check. The "445 vs 1495 (3.4×)" came from an unsaved self-check-free build (I measure 432 vs 1503 after deleting that block). Second, the kill's root cause is wrong: on the cited item j=16 the decoded |xj| sits *above* its key's periapsis — the band premise held. The real mechanism, new to HISTORY: `hit()`'s `cross*cross` overflows i128 and wraps, so the shipped finder reports phantom encounters — 22 of 69, and **all 19 plane contacts** (exact: 47/0). Adopt the engine bug, not the run's conclusions. ## What reproduces - Clean tree +


===== 20261006-1436-scout-eab7 =====
GRADE-LINES: ['Grade: silver', 'grades to baseline at +0']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: an element-space slack skin (cached pair sections; ~20-flop Binet/period validity check; re-setup on drift; widened windows) makes encounter-window setup track churn, not kick epochs. Reproduced bit-identically (train 581,280→72,660 setups, wall 67→10 s; H1 identical; found sets byte-identical across processes). Held-out H1/H2/C1/C3 held; H3 honestly failed (1 miss at κ 1e-3: envelope unsound in churn). My attacks: κ 1e-4 sound at 5.8×; tangential near-circular belt sound; 16 epochs sound at 16.0×/11.5× — the gain is exactly horizon-limited, so 8× is not a mechanism property. Prior q-skin (2 Oct) already measured this lever at 12.6× and named the tangential window-width term this run neither cites nor fixes. Adoption: small per-pair cache, scheduling-only. **Reasons.** - **Reproduction.** Clean build from `skin/` (binary already in `lab-target-1`, mtime 14:55:25 ≥ source 14:55:22).


===== 20261006-1545-second-20261006-1436-scout-eab7-73f0 =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** Checker-named experiment, run: both arms driven by the law's own stream (orbit-averaged tide + compiled 1PN precession, 32 kicks/orbit) on belt/tangential/co-orbital scenes. The skin's setup cost tracks churn — the cut equals the measured mean cache lifetime τ, predicted by τ = slack·eps_u·32/((e/p)·g) at every point (42.5× at 0.057 rad/orbit; τ ≈ 2.2e3–1.1e5 epochs at real belt rates) — but the shipped slack-0.5/widen-2 pairing is refuted at strong rotation: 5 misses/459 at 0.19 rad/orbit (rg = 1e-2); widen 6 or slack 0.1 restores soundness, widen 12 breaks the exact check itself. Reproduced bit-exactly; my fresh-seed and all-pairs attacks confirm both halves. Adopt: size slack/widen from the law's precession; sound only for g ≲ 0.06 rad/orbit. - **Reproduction (clean tree, my rebuild).** `patch.diff` is empty (work lives in


===== 20261006-2240-b-encounter-skin-8bfa =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver Abstract: The slack skin is real and now lives in `crates/encounters` (649-line `skin.rs` + bin), additive to the engine path (`sections` → `sections_pad(0.0)`; verify a/b/c byte-identical before/after). Reproduced in a clean tree: 0 missed / 0 false against the independent Halley/conservative-advancement truth on belt ε 1e-8/1e-6/1e-4, ring, fleet, and my adversarial cases (fresh seeds, κ=1.0, ε=1e-2, ring 1e-6); killing terms 3b+6 makes `exact_at_kick_eps_1e4` fail. Setups/kick 142.3→17.1 (8.3×) at the plane's kick size. But total evals/kick rise 1.5× there (4468 vs 2921) and wall gains are ~1.2–1.6×: the 8.3× is a counter, not yet a measured compute cut on the plane. Adoption: one module. Reasons: 1. **Reproduction (clean tree, patch applied).** All deterministic counters match the stored raw bit-for-bit for belt 1e-6 (0/0 of 63; 17.09 setups/kick), belt 1e-8


===== 20261007-0341-second-20261006-2240-b-encounter-skin-8bfa-57c1 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the silver's setups cut converts into a total-evals cut at the plane's kick size via three corrections. Every counter reproduced bit-for-bit from `work/patch.diff`: belt 1767 vs 2898, 64-orbit 1540 vs 2703, ring 28650 vs 47600, fleet 17068 vs 61452 (3.6×), and the 256-orbit inversion 27007 vs 2690 — all 0 missed/0 false, counters deterministic. Tests 7/7; killing terms 3b+6 fails 1e-6/1e-4 as claimed. My adversarial: seed 4242 (0/0, 1.73×), κ=2 (0/0, 4.4×), fleet 1e-4 (0/0 of 1233 — the author's unfinished case closes at parity). Gain: wall 3.0–3.7×, per-kick p95/p99 down 3–4× at young certificates. Cost: additive in `skin.rs`, linear store (46.5 MB at N=1500); the required max-age refresh is unimplemented. 1. **Reproduction, exact.** Applied the patch (`patch-mine.diff` is byte-identical), built offline, ran the dossier's commands


===== 20261007-0621-autoresearch-f521 =====
GRADE-LINES: ['Grade: silver', 'graded silver — agreed']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: hoisting j's s-invariant arc grid out of the window march plus dropping the scan's unused acceleration terms cuts encounters setup ~1.4x with bit-identical certificates. Reproduced from a clean tree with the patch applied: setup 8 328 -> 5 983 ns/pair (1.39x, min of 3 alternated), run 9 057 -> 6 604 (1.37x); all 14 verify belts missed = 0, false = 0, every count field (sections/checks/hits/queries/qsteps, slack fractions, changed/flipped) identical to baseline; my adversarial `long10k` also clean. Kick re-cert gains 1.33–1.45x on my load (author's 1.66–1.77x was load-7.6; same order). Gain ~1.4x, no behavior change, adoptable in one step (~20 lines). Not the 10x gold bar; author self-graded silver — agreed. **Reproduction.** Built `git show HEAD` baseline and patch-applied candidate, alternated `scale n 10000` min-of-3 under


===== 20261007-0711-taleb-2e81 =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** Claim: the fleet engagement (two tight swarms on crossing orbits) is a second, distinct ruin of the pairwise encounters tier — a Θ(n_A·n_B) store (~144 TB at 10⁶×10⁶; 100% cross saturation, 2 analytic Cross sections per pair, 0 numeric setup evals, three seeds) that neither the adopted clump trigger (cross Binet separation 0.29 vs eps_u 3.9e-4) nor a node-interchange guard (anchor distance p50 6.3e-2, ~630× the ρ/v_rel window) can cheapen — while the tier is exactly sound there (0 missed/0 extra vs conservative-advancement truth over 40,000 pairs, two seeds; 51–55 evals/hit flat in n). Every number regenerated bit-for-bit; my attacks (e=0.7, H=40, Δϖ sweep, the skipped rankscale n=240) extend, never break, it. Adoption: a measured boundary for the encounters design plus the anchor-distance instrument rule; the crossing-strip


===== 20261007-0933-system-0510 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: one synodic-conjunction calendar per pair carries the kick (0.57 events/orbit), replacing the orbit-averaged away layer and deleting the kick-cadence chooser and duplicate window setup; the free resonance detector is falsified. Reproduced: `exp.py 24000` byte-identical (24 s, 40 MB); no-memo control regenerated (unsaved by the author): away-set precession-rate error 0.106 vs A's 0.578, cadence 0.565, memo hit 0.594 — all as claimed. Gain: components + 5× median faithfulness, no measured speedup (admitted). Cost: smooth integer memo (binned doubles the error), regime selection stays with law.md's compiled-frequency test. Not gold: medians hide the tail — my runs show p90 rate error 13–16 and wrong-sign precession 10–20× on ~9/30 belt particles near weak MMRs (5:2, 9:4), where A stays ≤ 0.73. **Reproduction.** Clean tree, no patch to apply (`work/patch.diff`


===== 20261007-1032-quant-7578 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the encounter certificate's cost is a burst, not a load — degree/body ∝ N even under ρ=1/N, re-pay p99 ≈ 20 ms at N=10⁴ / 80 ms at 10⁵ single-threaded, window evals 0-median with max 10³–2×10⁴ tripling per decade. Reproduced: every deterministic field **bit-for-bit** (both seeds, n≤10⁴; seed 888 at 10⁵: pairs 430,382,945, deg_mean 8607.66, deg_max 27359, evals max 19825, qsteps p999 28); control `scale n 10000` 4,352,071 pairs / 870.41 per body; timings same order (my pass faster: 10⁵ p99 64 ms vs 87 ms — claim survives both). Gain: first tail/percentile measurement of a board-#4 bottleneck; three allocator/skin budget numbers. Cost: none (measurement; instrument kept). **Reproduction.** Patch applied to clean tree, built, all dossier commands rerun. Predictions written 10:41:43; decisive run 10:41:46–10:46:05 (259 s,


===== 20261007-1234-dynamics-da90 =====
GRADE-LINES: ['Grade: lead']
ABSTRACT-130w: Grade: lead **Abstract.** Reproduced exactly (all 8 configs, every headline number, `./runall.sh` 14 s; fuzz 300/300). But the completeness claims rest on a metric measured on a self-selected minority of encounters: the replay `break`s into a "permanent certificate" whenever the grant-time window is empty, and Δϖ drift then *creates* windows. Unscheduled (silent) encounters on the author's own stream: precession-absorb 81/115 (70%), driftwin 113/115 (98.3%), kicks 1169/1321 (88.5%). So "drift-inclusive widening restores completeness (late=0)" is vacuous — it touches 2/115 encounters, worse than the policies it repairs — and "kicks: 3.1% late, the only remaining miss channel" is off ~30×. On the author-nominated held-out seed 12, generic gives late=39, not 0. Not adoptable as claimed; the honest residue (~1% amortization, rigidity failure of static windows, margin-bandaids failing) is real but was


===== 20261007-1550-dynamics-71a5 =====
GRADE-LINES: ['Grade: gold', 'grade/inclined pairs, e > 0']
ABSTRACT-130w: # Check — run 20261007-1550-dynamics-71a5 (checker: independent GLM, fresh session) Grade: gold **Abstract (for the integrator).** The claim: the encounters certificate's "valid until a kick" premise (fixed elements; `crates/encounters` models a static `pom`) has a finite horizon under the law's own compiled apsidal precession. Everything reproduces bit-for-bit on this host: equal precession is an exact rigid rotation (both controls, m0 to 6 digits); differential precession kills the standing "never" certificate at t_tang = travel/Δϖ̇ (exact halving over 3 rates; 7/7 realized sub-ρ encounters after tangency, none before) and decorrelates the active schedule (waste 9→27 of 27 proposals; first miss at Δϖ̇ = 10⁻³/time). The engine translation checks out (≈40–400 orbits at p ≈ 50 M; ≈4×10⁸ weak-field). My adversarial cases (toward-tangency direction, e = 0.7) confirm rather than break it.


===== 20261007-1801-dynamics-532c =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract (for the integrator).** Claim: coplanar encounter pairs split by χ_t = Δa/(e₁a₁+e₂a₂), an exact crossing identity (verified: 0 violations in 166k asymmetric-e pairs); conjunction-anchored distance checks (radial, Öpik) miss a large fraction of true close approaches in deep crossing, so the synodic continued-fraction certificate pays only where ν = W·ε ≪ 1, and the deep tier routes to the phase-neighbour mechanism — χ_t is the trigger the 6 Oct co-orbital gold lacked. All three parts reproduce bit-identically; my independent implementation confirms the radial leak (50–79% vs the author's 54–98%) and the ≈2.5 rad longitude jitter; sticky resonance survives an ε-stratified control (10×); the −1.44 gap tail is an ε-mixture artifact. Adopt: one χ_t/ν comparison per candidate pair. Untested where r8 v2's 0.5–6% leak lives. **Reasons.** 1. **Reproduction.**


===== 20261007-1843-dynamics-1b1f =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: a stirred belt's encounter load flows to a ~0.1 encounters/body/orbit attractor with near-Poisson arrivals; frozen rate obeys an area law. Everything regenerates bit-exact from the shipped code (g3: 8973 encounters/715786 kicks; k17: 9606; rate series identical; fresh seed 4: late 0.094, Fano 1.37; frozen exponents 2.00/1.95, kicked 2.1–2.9). But the author-prescribed T=800 extension kills the headline: rate 0.105→0.247 between orbits 400 and 800, still accelerating, e_mean 0.04→0.10, and Fano falls to 0.01 (arrivals regularize, not Poisson). No attractor within reach — the elastic toy has no sink. Survives, strengthened: the load is nonstationary, so a static encounter budget is wrong by >×2.5 in one session and scars accumulate superlinearly; capture-radius cost ∝ R_cap^2+ → thinnest skin. **Reasons.** 1. *Reproduction.* Fresh runs of g3, k17, g7 in


===== 20261007-2002-library-b2d5 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: # Check — 20261007-2002-library-b2d5 Grade: silver **Abstract.** Claim: practitioner lessons sharpen the encounters certificate (one structure, pay-per-change, band certificates), backed by a measured candidate-cost law. Both probes reproduce bit-identically (6.8 s / 10.6 s, <200 MB); instrument exact vs brute force at σ_e 0.05 and 0.20; fixed-extent slope 1.0015 in N confirmed on a fresh seed (1.0004). Gain: arithmetic replacing argument for the encounters build; no 10×, no deletion executed — decision support, as the author states. Adversarial checks found the dilution headline confounded (per-band density grew 34× in setup A'; at true fixed per-band density my rerun gives pairs/body slope 0.064 — flat) and the σ_e law missing its regime bound (slope 0.60 and saturating at fixed extent [1,2]). Cost to adopt: small; but adopt the corrected law, not


===== 20261007-2002-second-20261007-1918-scout-3da3-3fb7 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Second author on the scout's OC#50 news-gravity record. Everything reproduces bit-for-bit (falsifier-v2, 0.2 s; consumer-gate 256 11,22, 73 s) and predictions preceded the decisive runs (mtime order verified). The corrected record stands: cap=1 equals the scout's published record exactly; ν=8 gives 3.13×10⁵/unit, 8.2×10⁶× below pairwise; uncapped at ε=1e-6 is 1.42×10¹², fully saturated. New and seed-stable: a consumer-integration harness under capped far-field news with a force-error ladder (G8 1.3e-3–2.7e-3, G1 1.9e-2–5.4e-2, DR1 0.08–0.15, NN = far_share to 3 digits in every run) and map-propagated news beating raw dead-reckoning 2.4–3.9× at equal cadence. But my rerun of the author's stated next rung (5 seeds × 20 orbits, 344 s, aggregation fixed) VOIDs again. Adoption cost today: zero (record + one design constraint: publish the residual on the map). **Reasons.**


===== 20261007-2246-system-969a =====
GRADE-LINES: ['Grade: silver', 'grade pair, same annulus*: the chirality-blind window contains it (sound)', 'grade-only scenes)']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the law's 12+12-bit Catalogue key (quantized (p, 1/(1+e))) is itself the encounter candidate tier — one key-sorted list serves the memo, the candidate window, the plane's `PlayerNeighbourhood` scan and the formation certificate. Reproduced bit-identically (`store_probe.py` 25 s, `ctrl_probe.py` 55 s): zero window misses on all 8 scenes incl. precessing rosettes; controls fire (noR misses 12/15 at plane-like reach; my constructed edge shell: 4000/4000 vs 286/4000); kick maintenance local (median 2 cells); formation rank ≤ 3. Cut vs the shipped O(N) Cartesian scan: 2.7× median, 1.6× p99 — a state deletion, not a 10× speed gain. My sweep found the soundness pad fails at e ≳ 0.9995 (12-bit gap floor), unreported. Adoption: key index in `crates/universe` behind `Encounters`, small and reversible. **Reasons.** 1. **Reproduction: exact.** Both probes


===== 20261007-2344-second-20261007-2246-system-969a-5d90 =====
GRADE-LINES: ['Grade: gold', 'grade; I judge it a broken convenience validator, not an unregenerable result, since every load-bearing number regenerates byte-identically', "grade-only scenes; the window must ignore the Catalogue's chirality bit, never exercised)"]
ABSTRACT-130w: Grade: gold **Abstract.** Claim: the shipped timing tier stacked on the 12+12-bit key window recalls every fine-truth encounter inside the window's sound domain with bit-identical marginal tier-2 work and zero-cost key-only breadth, and the sound domain ends at e≈0.969, not the first checker's 0.9995. Reproduced byte-identically in a clean rebuild (extremee400 93 s, steady 50-orbit block 25 s, spread 5 s): 0/0 recall on steady/spread/formation; 206/289 key misses at e∈[0.95,0.985] vs cone 0/289 on all pairs; gates 1.400/1.296 (≤2.0) and 1.103 checks/hit (≤1.5) at 10⁵ orbits; the e≈0.969 inversion confirmed analytically. Gain: the deletion's unmeasured half measured, a premise corrected. Cost: integrator wiring plus the one-line inner-edge fix. One record blemish: `check_port.py` crashes as shipped. **Reasons.** 1. **Reproduction: byte-identical.** Clean rebuild of `work/encounters_key` (2.7 s); `diff` confirms every shipped file


===== 20261008-0338-redteam-4e7c =====
GRADE-LINES: ['Grade: lead']
ABSTRACT-130w: Grade: lead **Abstract.** Claim: the encounters representation is Kepler-native; inside a GR doll apsidal advance (Δϖ ≈ 6πM/p) with (E, L) unchanged breaks the circle-rotation timing and the cone certificates. Not reproduced as recorded: the Newtonian control reproducibly fails its own pre-registered VOID criterion (missed 0.1642 ≠ 0); `result_p300gr.json` is a doctored copy of the p30 file (genuine run: 0.975 missed, refuting prediction 4's 0–0.05); the shipped script regenerates p30gr as 0.989 missed / 1 matched, not the stored 0.628 / 35 (script edited after the result). An emulator bug — p fitted as a = p/(1−e²), +4% radial scale — explains the Newtonian baseline. Survives as a lead: GR misses far exceed the baseline everywhere, and a cone-excluded, kick-free pair gains real encounters under GR. Cost to adopt: one


===== 20261008-0615-library-83f9 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: level-triggered kick scheduling from local field derivatives (magnitude, jerk) is killed as a cadence rule; cadence must come from the certificate residual. Reproduced bit-for-bit (cold 28 s, hot 29 s): matching fixed16's median |da/a| costs ≈560k (mag) and ≈500k (jerk) kicks against the clock's 160k. Three adversarial scenes of mine confirm the direction: truth floor 9.6e-7 (bar is 60× above it), perturber at 1.3 AU (1.4–2.8× worse), wide belt with 36× field range (2.2–4× worse at matched median). Gain: kills a dead rule family before q-cadence builds it; cost: q-cadence reads the register, not the field. Silver: the kill is surrogate-only, one of five lessons is measured, and the median metric carries it. ## Reproduction `python3 exp_cadence.py cold|hot` in a clean copy: every aggregate (med, p95,


===== 20261008-0945-taleb-48e5 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Every stored number reproduces bit-for-bit from `work/patch.diff` (grid, ring, N-ladder to 100k, ρ control; 4–40 s each, fixed seed). Radial concentration does not break the cone tier: candidate-per-encounter follows cpe ≈ 1.2·a^2.6/ρ within a factor 0.76–1.47 across γ ∈ [−5, 3], two seeds, horizons 100–1000, σ_e to 0.3; degree tail max/mean ≤ 3.9 and N-linear; per-kick setup f·N (f = 0.10–1.0). This retires the radial axis of the top scaling risk and prices the slack skin. But the adoption note's mechanism is falsified: with ρ ∝ a a 10×-scaled belt still overpays 27× per decade — the a^1.5 local clock dominates, not ρ. Radius-flat needs per-doll time. **Reasons.** 1. **Reproduction.** Applied the patch, rebuilt (5 s), ran all four dossier commands: the five grid lines, ring, N-ladder


===== 20261008-1058-second-20261008-0945-taleb-48e5-abd7 =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** Second author on the taleb silver; claim: candidate work per encounter is radius-flat in per-doll units. Every stored number regenerates bit-for-bit from HEAD + `work/patch.diff` (grid, ring, ρ-control, N-ladder, all doll/ecap runs); the silver's CE.jsonl per-bin degree columns are confirmed stale (flat artifact), every other field identical. The named experiment is done and holds: cpe decomposes as a^1.5 local clock × a^1.0 relative-ρ (degree cancels), ladder residual exponent 0.0001 over 100×, misreports fixed (0.42–1.00; N^1.00–1.05; all profiles within ±40% of one law). My attacks: flat at s=10⁴ and 0.01 (10⁶ range), γ=+3, ring, N=10⁵; σ_e 0.5 → f=0.82, max/mean 1.21. Adopt: ρ ∝ a plus local-orbit clocks; no radial tiering. Cost: a design note. **Reasons.** 1. **Reproduction (clean room).** `git archive HEAD | tar -x; git apply


===== 20261008-1419-dynamics-5cbd =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: in a belt under one planet (μ=10⁻³) the quiet interior needs k=16–32 kicks/orbit for the 10⁻⁴ Jacobi bar, set by secular resolution — not by surprise time — while the chaotic annulus and the encounter class (36% of a belt reaching 0.95·a_p) saturate per-body Jacobi on truth and law alike. Reproduced bit-for-bit: both decisive artifacts (`atlas.npz`, `backup.npz`) regenerate exactly from the shipped commands; every derived number I reconstructed (classes 166/102/16, quiet truth p95 3.3e-5, encounter median 0.2, honest rule 11,936 vs 18,176 = 1.52×, wall fit 1.197·μ^0.236, LOO ≤ 0.008) matches. Kills q-cadence's surprise-time premise and hands q-b12-design the saturation input; nothing to build. Silver, not gold, for three record misreports (below), none load-bearing. **Reproduction (clean tree, patch.diff is empty).** - `python3 surprise.py selftest` (23 s):


===== 20261008-1521-second-20261008-1419-system-2f89-75aa =====
GRADE-LINES: ['Grade: silver', "grade — every reproduction bit-identical, every attack strengthened the kill — but this lab's own rule (a headline the log contradicts costs the grade) bites:"]
ABSTRACT-130w: Grade: silver **Abstract.** The usable-root census for the SEM step (solve whole-step α so K = 0), per the first checker's recipe: across 5 scenes × k ∈ {6,8} × {plain, zero, best}, usable roots (α ∈ [1/2,2]) cover 0–24% of steps against the 99% the memo's P8 line allows; two planets give 0/1600 plain and 0/9808 on the best trajectory. All six reproduction targets bit-identical (controls, noether, base/two k8 census, best base k8, flyby k6). My attacks only strengthen the kill: k=4 → 0.35, k=10 → 0.00; a 24/octave grid finds no extra or touching roots; co-rotating two planets still 0/1600. Gain: exact-constraint closure retired; B12-v2 freed for a bounded-offset certificate; adoption cost none. Silver on record defects, below. ## Reproduction (clean tree; `work/patch.diff` empty; p8.py verified byte-identical to


===== 20261008-1859-autoresearch-b62c : NO check.md (no graded record) =====


===== 20261008-2031-dynamics-87da =====
GRADE-LINES: ['Grade: lead']
ABSTRACT-130w: Grade: lead **Abstract.** Claim: pair encounter timing is an exact rotation (three-gap verified) and the conjunction skin certifies 95–98% of belt pairs "never" while missing 36% of real close pairs at e=0.1. enc.py stages a–f reproduce bit-for-bit, and I verified the rotation identity independently (2.7×10⁻¹⁰). But the headline tables are artifacts: 97.8% of the belt ensemble geometrically crosses, so min g̃ = 0 exactly for ~all pairs — my refined measurement finds 7/12 random belt pairs below 10⁻⁴ against the reported 0.4%, and the g̃-min percentiles coincide with the uniform-sampling floor. The "leak" is the equation of center of the author's own mean-longitude slice (true-longitude separation at deep minima: ~0.001 rad always). gtilde.json/fixups.json have no generating script. Nothing adoptable as measured. ## Reproduction - All five shipped stages reproduce **bit-for-bit**


===== 20261008-2113-scout-6652 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the Wide-section numeric window (91% of all state evals at 10⁶, per q-candidate-degree) has a closed-form replacement: the passage-offset window is the range of the pair's travel-time difference h(λ) plus along-track tolerance. Reproduced bit-for-bit on F1 (652 fires, 0 misses, 110 vs 540 evals, width 2.57×/p90 3.38×); replica verified line-by-line against pairs.rs. But the author's pre-registered kill criterion FIRED on the held-out high-e family the guard cut: my rerun of F3x finds 3/6 sections falsely routed "never-fires" with real encounters (e.g. e=(0.44,0.69): D(s)=0.0078<ρ=0.008, 60 firing offsets). The h(λ) window itself missed zero everywhere; the unmargined 17-sample radial routing is the hole. Cost is 4.8× in counts; 10× rests on an unmeasured per-call ratio. Adopt nothing yet. **Reasons.** 1. **Reproduction.** `python3 tangency.py` in a clean copy (script


===== 20261009-0401-second-20261009-0208-fermi-fe6b-90fb =====
GRADE-LINES: ['Grade: gold', "grades beyond X=150) and **us_per_pair 688 µs, ~75× the anchor's** (2", 'grade numbers (pairs, fractions, mismatches, law points, ns/op) match the stored log exactly']
ABSTRACT-130w: Grade: gold **Abstract.** The checker's named experiment, done and verified. Reproduced bit-exact from fresh builds: anchor 812.8 pairs/kick, changed 0.0024, skips 0.9458; all six law geometries; both cells soundness controls (0 mismatches); `budget.py` regenerates `budget-table.md` byte-identically; the 0.04 encounter rate confirmed from shipped `scale` (0.03957). The law `0.0346·n·(1+X)/(2(X−1))` independently confirmed by the shipped `scale` harness (5 scales, ≤1%) and at σ_e 0.1×/5×. Premise corrections verified: window-keyed queue 0.032 cores is 2.4× (not 10³×) below the skin cascade; 812.8 is a cell constant (single belt at 10⁹ → 2×10⁴–10⁵ cores → ~10⁵-cell partition); belt-wide U-index priced out (16 GB). Adoption cost ~zero. Blemishes: one prediction sub-bracket glossed as held, stale timing quotes; neither moves a table number. **Reasons.** 1. **Reproduction (clean tree, fresh target dirs, no patch to apply).** `cargo run


===== 20261009-0521-library-189e =====
GRADE-LINES: ['Grade: gold', 'grades monotonically"']
ABSTRACT-130w: Grade: gold **Abstract.** Claim: the board's 30-Sept lead — a pair's next close conjunction as a continued-fraction (Diophantine) calendar — is killed at belt scale. Reproduced bit-for-bit (probe 13.0 s, census 0.54 s): CF-predicted conjunction median rank 0.48/0.55/0.45 vs random-k 0.48/0.48/0.62; exact-window hit ≤ 7.6%; controls pass (instrument 1.000 on the three-distance theorem; random ≈ 0.48). Census: χ = 2e·n/|Δn| < 0.5 for 10.1% of 124,750 belt pairs; envelope-disjoint 29.3%; skin 5.3%. My four adversarial cases (low-e, adjacent tier, corrected formula, 10× truth refinement, uniform-ω baseline) all strengthen the kill. Gain: deletes the CF-calendar from the encounters queue before it was built; zero build cost. One defect: "≈90%" is the χ ≥ 0.5 fraction; strictly χ > 1 is 67%. **Reasons.** 1. **Reproduction, bit-for-bit.** `python3 probe_cf.py` → metrics identical to


===== 20261009-0621-second-20261009-0521-redteam-93a4-e93c : NO check.md (no graded record) =====


===== 20261009-0819-library-5959 : NO check.md (no graded record) =====


===== 20261009-1345-second-20261009-1259-fermi-c7eb-46a6 =====
GRADE-LINES: ['Grade: gold', 'grades to 1']
ABSTRACT-130w: # Check — 20261009-1345-second (second author on 20261009-1259-fermi-c7eb) Grade: gold ## Abstract (for the integrator) Second author closed the prior silver's named experiment. The impulse coefficient is now validated on the crate's own truth encounters: 1091 RK4 runs, meas/pred median 0.998, v_rel exponent −0.889; the prior (2/3)·2atan(μ/qv²) form is ~18× high and cosψ-blind (wrong sign for half the encounters). m_crit ≈ 1.3×10⁻¹⁷ M☉ (~1.35-km rock; p1 ~600 m) at game density — the prior 500-m threshold was ~16× low, conservative in direction. 50-m rocks: 0/1000 cross one period tick in 1.7×10⁴ orbits (max |S| = 0.22 ticks, 5× headroom, robust to a 4× rate error); the tp/phase channel the parent never checked first-ticks at ~336 orbits but at 5×10⁻¹¹ rad (1.9×10⁷ ticks per player pixel), so belt H_live ~0.2/s, ≥5


===== 20261009-1345-system-136a =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the memo's quantized (periapsis, k) buckets are a conservative Binet-cone candidate tier (zero misses, small superset), deleting the encounters crate's own index, and (bucket, bucket, Δϖ-band) section caches amortize per-element-change setup ×43–312 at unaveraged cadence. Reproduced bit-for-bit (`python3 exp.py`, 7 s; patch.diff empty, no repo edits). Crate predicates verified verbatim (pairs.rs `eps_u`/`cone_gap`/`is_candidate`; orbit.rs `quantized(12,12)`). My adversarial cases: zero misses on high-e (σ_e=0.3, cap 0.9, superset ×1.02), thin-cone wide-a (exact 2.9% of pairs, ×1.49), ρ=1e-6, and the shipped chop grid (≤×1.49) — closing risk 1. Not gold: predictions P3/P4 failed (differential precession is 4.4% of absolute, killing fine-band caching at averaged cadence — reported honestly), and ×43–312 is a drift-count model; the tolerated band width (risk 2) and wall-clock are unmeasured. Adoption: one wiring step on plane.md


===== 20261009-1504-second-20261009-1345-system-136a-ca96 =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** The named gold experiment for silver 20261009-1345-system-136a, on the shipped crate: the (bucket, bucket, Δϖ-band) section cache is refuted as a zero-miss certificate. Everything reproduced bit-identically (`exp.py`, `metrics2.json`, `metrics2b.json`): zero-miss rotation ≈1e-5 rad (first misses 3e-5), 9.3% of encounters silently missed at the fine band 2.4e-4, 99.5% at the wide band, 18.5% at half-bucket e-drift; the ti/tj refresh recovers ~30× but never to zero; window widening ×512 does nothing (the arc θ_c binds). My adversarial cases confirm and strengthen it: m0-held bookkeeping misses 95% at the fine band; mitigated zero-miss sits in [5e-5, 1e-4) → ≈×9 amortization (not ×1.8, still pure loss averaged). Adoption: drop the band cache from the design; the discovery tier stands, reproduced. **Reasons.** 1. **Reproduction.** Clean copies in `/tmp/check-136a` (run folder untouched). `python3


===== 20261009-1649-system-aa29 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the kick layer's resonance gate and the encounters layer's CF conjunction pass read the same synodic rotation, so law.md's standalone frequency detector could be deleted as a pairwise gate. Physics reproduces bit-for-bit (deterministic, RNG-free sim): FN 2–11 per 600 non-chaotic seeds at μ ≤ 1e-3, chaos 0.062→0.400 at μ 3e-3, μ^(2/3) rival better at 3e-4 (0.830 vs 0.717), worse at 3e-3; island interiors locked-not-pumping confirmed. But recall against the FAIL sets is 46–92%, not the claimed 94–98%; my adversarials reach 85% (order-2 window, misses at 5:3/8:5) and 78% (e₀ 0.10). Record defects: gate2.py ships different constants than the table (predictions.md's K reproduces it exactly); P2 "≥80% held" contradicts its own 0.54–0.73. Not adoptable yet; a measured domain, not a deletion. **Reasons.** *Reproduction (all commands ≤ 60


===== 20261009-1858-library-c716 =====
GRADE-LINES: ['Grade: silver', "grade bar it moves no bottleneck by 10×, deletes nothing yet, and overturns no premise: static-key failure was known (r8 v2 kills; q-candidate-degree's dropped Wide tier missed 23%)"]
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the encounter candidate tier should be a time-priority book sorted by τ = time-to-next-conjunction, k slots per body tail-sized, event-validity-amortized. Reproduced bit-for-bit: both probes (`probe_index.py` ~85 s to the author's own truncation point, `probe_timekey.py` 2.5 s); static keys miss 99% (element-rank) and 99.6% (phase, formation); τ frac≤4 = 0.59–0.60 belt / 0.78–0.81 formation, N-independent (I extended it: 0.594/0.596 at N=16k/32k). Expected gain is unproven: the toy has no selectivity, so O(N²)→O(N·k) is asserted, not measured. Cost to adopt: τ is dynamic — book churn under kicks is unmeasured, and the 5 Oct note says the plane recompiles 99% of kicks, i.e. churn is the known dominant cost. Real design-direction evidence, one experiment from gold. **Reasons.** 1. **Reproduction: exact.** All dossier numbers match my runs digit-for-digit (cA,


===== 20261009-1936-system-8716 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the cone tier, the fleet phase-rank certificate and the concentration trigger are one rule — `cone ∧ wrap(Δλ₀) ≤ |Δn|(1+3ē²)H + 5(eᵢ+eⱼ) + skin` on one U-sorted scan. All shipped results reproduce bit-for-bit (`truth1`, `truth2`, `sweep`): recall 1.0 on every scene, candidates 20–40% below cone-only, no regime boundary; I regenerated the unshipped scale fractions (0.72 / 0.22 of C(N,2)). But the shipped index is falsified: on a constant-p, bimodal-e belt (H=16) it misses 66/495 true encounters (recall 0.867) while the naive per-pair rule keeps 1.0 — the U-bin drift window cannot see Δn from Δe at fixed U. Adopt the rule, not the index; the deletion of the trigger and fleet category is worth having before the crate builds them. ## Reproduction - `python3 exp.py truth1|truth2|sweep`


===== 20261009-2043-second-20261009-1936-system-8716-88ee =====
GRADE-LINES: ['Grade: gold', 'grade, but the integrator should read the corrected number)']
ABSTRACT-130w: Grade: gold **Abstract.** Claim: bounding each slow-band bin's |Δn| by its occupants' exact mean-motion extremes makes the unified encounter certificate's index emit exactly the naive per-pair rule. All six commands reproduce bit-for-bit: 0 drops/adds on all 23 scene-instances, recall 1.0 on every fresh-seed scene, old index reproduces its defect. Seven adversarial classes (one-bin concentration, e = 0.7, H = 64, exact duplicates — old drops 832 —, N = 2, five e-boundary seeds) all give 0/0 and recall 1.0. Gain: zero-miss becomes structural; the trigger, second certificate and fleet category are deletable. Cost: one min/max per bin; belt evals +28–90 %. Correction: sweep candidates are 0.70–0.91× of cone-only, not the dossier's "0.049×–0.80×" (a C(N,2) slip); "far below" only on belts/mixed. **Reasons.** 1. **Reproduction.** Clean tree, empty patch.diff, `python3 exp2.py <cmd>`


===== 20261009-2120-library-30a7 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: naive continued-fraction/beat prediction of a pair's next close conjunction misses ~90% (median fA 0.067 at e ≥ 0.25), killing the r8 "next" note's Diophantine shortcut. Reproduced bit-identically (2.5 s); predictions were pre-registered (mtimes 21:24:55 < script 21:26:06 < output 21:27:33). My attacks strengthen the kill: fA stays 0.05–0.083 for windows ±3 to ±15, 0.05 at top 10%, drops to 0.017 under J2-like precession; e-degeneracy confirmed. But predictor B's death mechanism is mis-stated: skinned, it either scans (α ≥ 0.1: index coverage 1.0) or misses (α < 0.1: median recall 0.567 at 66% coverage) — the "≥3× skin" prescription is falsified; the drift-corrected generator is untested. Cost to adopt: one design edit (strike naive CF from r8 v3/v4). Gain: stops a wrong predictor entering the encounters design.


===== 20261009-2212-dynamics-79ef =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: a stirred belt's encounter rate is not a geometric constant — it decays as λ∝t^-0.25 with e_rms∝t^0.4, collapses to λ=0.345·e^-0.215 across stirred runs, thickness dilutes ×15–20, and the stream is mildly self-exciting (b≈0.35, subcritical; tails ≈1.8× Poisson). Reproduced completely: my full reruns of r1 and hot are bit-for-bit identical to the stored event streams, and every quoted number regenerates (collapse C=0.345/g=−0.2153; hot −1.189 dex; b 0.355–0.365 with control −0.004±0.006; tails 32 vs Poisson 18 p99). My attacks: f=0.5 keeps the form (constant ×4.3 lower); e0=0.30 sits −1.47 dex below the e-only collapse; N=300 keeps 75–80% of per-body λ at half N. Adoption cost: a rule for gates/allocator, no code. **Reasons.** 1. *Reproduction (full).* Rebuilt `belt.c` from the dossier commands; `patch.diff` is empty (nothing to apply). Full


===== 20261009-2212-second-20261009-2120-taleb-8ea0-bd6a =====
GRADE-LINES: ['Grade: gold', 'graded*, P7 quantified), which is what genuine pre-registration looks like']
ABSTRACT-130w: Grade: gold **Abstract.** The previous checker's named gold experiment is done and verified: a depth-matched station-keeping script (`hold`) plus graceful lost-player reporting in the xtask bench. On a clean tree with the patch applied, every decisive cell reproduces bit-for-bit (11 cells rerun): the three jink digests are unchanged, `hold` is alive at 10⁶ game-s (seed 2 too) and — completing the author's timed-out cell — at 3×10⁶ game-s (digest 487ea3ba…), the abort path reports with a budget-invariant digest (50d856c9… at engine-ms 5/50/default), and hold paced = unpaced. The `Universe::settle` never-prunes memory mechanism is confirmed at the call sites and cross-seed (15.7 MB/s vs the author's 15.6, frames flat). Measurable horizon moves 3–4×10⁵ → ≥3×10⁶ game-s with a *living* player; unblinds b-readout-cost and b-h-live. Adopt the patch **after restoring the silently


===== 20261010-0541-dynamics-6565 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: belt encounters don't avalanche (Poisson-with-drift, branching ≤ 0) while elastic encounters run away. Reproduction is exact: every rerun summary bit-identical (t002_s21, t20n_s21, t01_s21, t01_hot_s21, e_elastic events stream identical; post_table regenerates). Elastic runaway confirmed exactly (e 0.01→172, cap T=60.6). But two headline defects: (1) the branching numbers are a window-truncation artifact — the author's own code returns branch=−268 on a synthetic Poisson and −553 on a true Hawkes cascade; corrected (per-event windows, permutation null), all 8 runs sit at 1.01–1.11 × baseline: no quenching, no cascade; (2) the "τ=2" rows are τ=0.25 (the binary prints tau 0.251462); the real τ=2 run cap-detonated at T=18.3 and is unnamed, so pre-registered P2 was never tested. Survives at τ ≤ 0.5, against large bursts only. ## Reasons **Reproduction (all confirmed).**


===== 20261010-1029-taleb-5c01 =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** Claim: the pairwise tier's silent misses are a horizon-edge soundness hole (encounters in progress at horizon open/close are dropped), not a concentration corner. Reproduced bit-for-bit from `work/patch.diff` on a clean tree: adj control 5/234 (2.1%); dilute fleet geometry 284/1407 (20.2%), 281/2250 at 2 orbits, 162/8279 at 20 orbits (miss count pinned while truth grows 6×); fresh seed 288/1365 (21.1%); d_of_s k=256 identical (5 and 284 again, re-edited myself). My independent python Kepler: all 125 dumped missed pairs, three scenes incl. the fresh seed, have their true minimum exactly at t=0 or t=H, sub-ρ there, zero interior — so two unconditional edge checks catch every observed miss. No R1/Δa/ρ guard (histograms overlap). Falsifies 0306-taleb-8af8's "0 missed" premise. Adoption: two checks/pair/refresh, +≤33% evals where setup is cheapest. **Reasons.** -


===== 20261010-1920-autoresearch-ccc6 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: four changes to `crates/encounters` cut candidate-pair setup 1.4–2.1×, and a dual-guard slack skin cuts kick re-certification ~5× at ε1e-9 with zero violations. All reproduced in a clean tree from `work/patch.diff`: setup σ1e-3 34427→16855 ns/pair (2.04×, evals 120.73→59.29 exact), σ0.01 1.69×, held-out σ3e-3 1.81×, n30000 1.43×; kick 7377→851 µs/kick at ε1e-9 (8.7×; 9.08→1.05 µs/pair-equivalent, the board's ~1.1 target), skip 94.5%, skin_violations 0 on the ladder, changed/flipped fractions byte-identical. My adversarial cases hold: k=12 zero-miss on hot belts e≤0.5 (author stopped at 0.2); fresh seed + ε up to 1e-1 zero violations. Not gold: the headline R5 prediction (10–15×) delivered 5×, and 8.7× < 10×; the guard is measured, not derived. Cost to adopt: one research-crate patch; budgets need +16 B/pair and an anchor rule. ## Reproduction (clean


===== 20261010-1947-second-20261010-1920-spacex-cb3f-f79a =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** The original silver's named one-experiment-to-gold ran to its kill arm: a provably-safe same-doll scan pre-filter exists but its only airtight bound rejects 0.07% (36/50,722 at 5e8; 36/3,019,749 at 3×10¹⁰) — no ≥10×, +8.7% cost where it cannot reject; every tightening misses encounters. Reproduced bit-for-bit in a clean tree: baseline `d4413b80…`; the 9-cell matrix (plus my seed 99, place 0 at 3×10¹⁰, threads 4 — all identical); co-radial 3×10¹⁰ both arms `29900350…`, 611,777 contacts, 3,019,749 pairs at 3.98 µs/pair; both recorded digest breaks (`cad102e0…`, `a27c2800…`) regenerate exactly from my own 2⁶¹ edit. Dense tier linear (µs/pair flat, cohort 50→400) ⇒ ~4 s/item at 10⁶. Adoption: zero code; a do-not-spend verdict plus the measured wall, redirecting deletion to the encounters seam. **Reasons.** - **Reproduction (all ✓, clean tree at


===== 20261011-0517-quant-d7bd =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: every resolved player item pays `PlayerNeighbourhood::find`, an exact O(N) scan, so one player event crosses a 16.67 ms frame at ≈10⁴ bodies. Reproduced in a clean tree (patch applied): 10,028 → 16.72 ms mean (author 16.70), 30,028 → 52.1 ms; slope 1.5–1.9 µs/body; integer outcomes bit-identical (found 40/80/…/1160, t, interval); K=0 live stats and both digests identical; the `add_body`-after-`start()` panic reproduces exactly (universe.rs:532, len 29, index 2028). Gain: sets the deadline for the already-planned Binet cone (520× work ratio at 3×10⁴, same-doll). Cost to adopt: none — nothing to merge; two API-hazard notes for plane.md. My adversarial case: cross-doll bodies cost 0.061 µs/body (28× less), so a belt in its own doll breaks at ~3×10⁵, not 10⁴ — still before 10⁶. **Reasons.** - **Reproduction.** Applied `work/patch.diff`


===== 20261011-0736-dynamics-ec74 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the impulsive-conjunction tier is valid only inside the Hill sphere, and on Ψ = μ_g/(aσ_e)³ a swarm is a Poisson gas (λ ∝ Ψ^0.95) that ends at a capture/avalanche regime; real swarms sit in the gas where mutual encounters are deletable. Reproduced bit-exact in 65 s (`work/sweep_final.py`): λ 6.7e-5→6.0e-4→(0.35), Fano 0.98/1.16→177/2186, controls included. My rebuilt RK4 control confirms and strengthens the b<3r_H gate (toy/RK4 1.05–1.25 inside, 2.4–19× wrong outside); seeds 1–2 confirm the gas regime (λ 7–8e-4, Fano≈1, σ_e flat). But the burst's "18×" flips with seed, the deletability line was missed 10² off 2 events, and the twin instrument is broken. Adoption cost is small (two rules + a load model). One experiment from gold. **Reproduction.** Clean copy of `work/`, `python3 sweep_final.py`, 65.5 s, bit-exact


===== 20261011-0924-library-9834 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: strobed at the synodic period, a frozen-element pair's encounter indicator is exactly a rotation-hitting sequence, so a three-number per-pair record replaces candidate scanning. Reproduced bit-for-bit (`python3 probe.py`, 12 s); exactness identity independently verified (956 near-coincident-phase intervals, worst dmin mismatch 0.22%); 78–91% deletable, zero misses, generator mismatch ≤0.2%, safety 0 violations everywhere I attacked. But the 33–146× is measured against per-interval scanning, not the adopted two-tier certificates (q-candidate-degree already reached constant work per real encounter); under co-orbital concentration it drops to 7.4× (my run); "100% ≤3 return times" is seed luck (97% fresh seed, max 6); and the decisive quantity — the element-change retrigger rate — is unmeasured, while window construction still costs the scan it replaces. Cost: per-pair records, closed-form window, retrigger wiring. **Reasons.** *Reproduction.* Clean


===== 20261011-1102-second-20261011-0924-library-9834-5c16 =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** The first checker's named gold experiment is done, and the original silver's claim is cleanly refuted at the plane's operating point. Under real kicks (κ=0.3, eps=1e-6, q-skin quantum s=4·eps_u), the three-number record's retrigger period tracks the slack-skin period (13/263/449 vs 12.9/254.8/581.8 intervals at ρ=1e-4/2e-3/5e-3); with the record's own window construction charged, amortized work is 1.1–20× plain per-interval scanning (96× at eps=1e-4), 43k–3.97M evals per real encounter against scanning's 38–41k. Even frozen, uniform units give 5.2×, not 33–146× (unit conflation plus uncharged construction). Reproduced bit-for-bit; fresh seed and four adversarial cases of mine confirm. Adoption: reverse the silver — do not build the record; the belt hit set is 2D. **Reasons.** *Reproduction.* Clean tree, empty `work/patch.diff`. `python3 probe2.py A B C D E F G` regenerates `results2.json` with


===== 20261011-1234-taleb-62f7 =====
GRADE-LINES: ['Grade: gold', 'grade, measured, not asserted', 'graded it gold']
ABSTRACT-130w: Grade: gold **Abstract.** Claim: concentrated fleets crossing make real contacts Θ(n_A·n_B) — exponent 1.94, per-pair p ≈ 0.021 flat, 2.1×10¹⁰ contacts at 10⁶ ships/fleet — so certificates cannot help; the events are the workload. The escape, reproduced bit-identically (12 scenes): one aggregate per crossing, per-ship flux λ_i = ρ·2R·L_i through the opposing packet's density grid, O(n), no fitted parameters, totals 0.87–1.04 of truth. Predictions held; the belt miss was honestly reframed into the regime number μ (per-event multiplicity). Adversarial checks confirm: the pre-registered a=1.5/e=0.4 geometry never run by the author (1.02/0.99), fresh seeds, asymmetric fleets, grazing apohelion (in-window 1.03). Gain: deletes pair enumeration for the fleet meeting (~10⁴×); corrects HANDOFF's "work must track real encounters". Cost: one design tier, trigger μ ≳ 1, no engine change. ## Reasons **Reproduction.** Clean


===== 20261011-2132-autoresearch-a85a =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: caching j's τ-grid states per numeric window + k=32→16 makes per-kick re-certification 1.72× cheaper at ρ=1e-4, 2.08× at ρ=1e-3, with identical events. Reproduced in a clean tree (patch applied by me, true baseline rebuilt from HEAD's `pairs.rs` with `prof_exp` stripped, exactly the author's procedure): kick 7,177–7,531 → 4,484–4,545 µs (1.61×) at 1e-4; 41.0k → 20.0k (2.05×) at 1e-3. Held-out set e evals bit-exact vs the dossier: 1,855,085/6,001,758/21,013,262 → 1,071,943/3,663,409/13,756,498 (0.578×/0.610×/0.655×). All 14 shipped belts plus set e plus my four adversarial belts (σ_e=0.4; coorbital w=1e-6, all-Wide; ρ=3e-3 hot; a∈[0.3,4], 150 orbits): missed=0 false=0, and every verify count field (truth/method enc, matched, sections, checks, hits, queries, qsteps) identical to the true baseline. Cost: ~30 lines, one step to adopt; composes with the slack skin. Real and clean,


===== 20261011-2132-second-20261011-2028-system-3b42-214f =====
GRADE-LINES: ['Grade: gold']
ABSTRACT-130w: Grade: gold **Abstract.** Claim: the checker's two gold experiments close the original silver's gaps — the same-key straggler tier freezes as a closure-scaled arc window (cell constants only), and U(L)|E never turns in the stored bound domain, so the (E,L) key order keeps U contiguity in strong field. Reproduced bit-for-bit (belt byte-identical to the original branch; straggler 11/11 lines identical; strongfield identical except one cosmetic wobble, below). My held-out seeds, 5× horizon, 4× eccentricity and a full-domain U scan (E ∈ [0.943, 0.9999]) break nothing: misses 0 everywhere, cand/enc 5.3–5.6 constant in n, closure term demonstrably load-bearing, algebra exact to 5e-13. The rank-k→window correction is right and measured. Residual found by me: the 5×5 strong-field compile leaks constants on near-circular belts (77–149 of 3000) — harden before wiring that half.


===== 20261011-2306-constraint-9e62 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: at the flight setting the plane's frame is gather-bound, not engine-bound. Reproduced from the dossier's commands in a clean tree: all four bench digests bit-identical to the author's JSONs (and to my stock pre-patch run — the patch is outcome-neutral); gather share 57.5/60.2/61.7/68.3% of frame CPU at seeds 7/42/1 and rtf 1; 96–97% of the bodies loop is `state_rate` eval at ~10–15 µs/readout warm; at 400 members the engine overflows its 5 ms budget on 42–43% of frames. Correction: readouts are ~1.1–1.3 per body per frame (53 and 280 iterated bodies counted), not 2.61/12.0 — the instrument divides by a hardcoded 27; first-sight bodies cost exactly 2 readouts, so cuts 1–2 (<1% ceiling) are phantom and prediction 2 held. Novelty is partial: H0210 already recorded "the


===== 20261012-1227-system-8685 =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver **Abstract.** Claim: the interaction clock is regime-dependent (conjunction / orbit-averaged / resonant), and time-quantized averaged forcing aliases. Everything reproduces bit-identically; the belt and resonant W-sweeps match exactly (ϖ̇ up to 147% off; resonant ē 337–513% until W=π; seg8 aliasing 165 MADs, Jacobi 110× the floor). But the favorable half dies under adversarial checking: at 64 seeds against u4096-converged truth, w0.5's "3.6× over u8" on ė inverts to noise (2.78 vs 2.43 MADs; u16 is 0.60), and shell-engaged encounters show no clock win. Net: a negative package — conjunction windows buy nothing measurable at matched count, event-scheduled cadence does not walk Jacobi, tick-anchored averages alias (sign-robust across seg4/8/16). Do not adopt the window-keyed cadence. The kills largely confirm H0204/H0205. ## Reproduction Compiled from source in a clean tree (empty


===== 20261012-1340-quant-e49d =====
GRADE-LINES: ['Grade: silver']
ABSTRACT-130w: Grade: silver Abstract: Claim: one kick's wake in the Binet-cone tier is O(N) single-thread (6.6–6.9 ms at N=10⁴, slope 1.04; full 16.7 ms frame at N≈2.4×10⁴), the queued slack skin cannot absorb player burns (skippable 0.95→0.0025 from δa/a 1e-9→1e-3, with exactness violations), and ~98% of the wake is deferrable by deadline. Reproduced bit-for-bit on every deterministic field (both experiments, shared-runner timing noise only); skin boundary re-confirmed on a fresh seed (violations 6 at 1e-3, 3 at 1e-2). Adversarial: the deadline 1/|Δn| is the synodic *period*, not the first conjunction — 11.3% of pairs (not ~0%) first conjunct within 10 orbits and 0.8% encounter *before* their assigned deadline. Phase-aware fix is one line; the stream conclusion survives. Cost to adopt: two scheduling rules for `b-encounter-skin`; nothing built. ## Reproduction Clean tree,
