topic: chaos-shadowing
status: open
closed-by:
valid-while:
updated: 20261019-1656-second-20261019-1551-dynamics-e3b7-9b3b

# Chaos, the shadowing clause, and trapping statistics under quantization


**NEW (9b3b, second author on e3b7 — the checker's named experiment folded in as the
run's own record, both checker digests reproduced bit-for-bit, and the ladder that
closes the mechanism's open link: the pump's entire address is the field's DK_CAP
clamp zone below r ≈ 2q).** The Pass control, extended: the same belt with
`Response::Pass` (contacts recorded, velocities untouched) is flat through H = 49152
— cold (maxk 91993 → 92196, +0.22%, frozen since t = 19362, esc 0, ke +0.00%) and
thermal ±q/256 (maxk frozen at 104180 since t = 5306, esc 0, ke −0.05%; its Bounce
twin: 449/800 evicted, 72.9M contacts) — and the H = 32768 flight reproduces the
checker's digest `b73b06dc…` exactly; the cadence flight reproduces `e98306bb…`
exactly (variant recovered: every 4th chronon, MU pre-scaled before rounding, cap
×4; onset 12236 = the checker's number; three other natural variants share the
onset invariance, so the cadence kill is variant-robust). All corrected season
numbers regenerate from this run's own TSVs (peak 102874 at t = 7808 = 173.8× the
cold same-time window; global max 183685 at t = 47744 vs cold 184250 = 1.0×; shell
77/21 at 4096/8192; esc 1379/1371 and 1374/1373; discriminator 1352 contacts and
maxk 379827 at t = 12288). **The new ladder (single body, same shipped field, 14
orbits, verdicts on integer rmax columns): bounded for every e ≤ 0.97 at a = 70q
(drift ≤ 0.9%, achieved e = target, Keplerian maxk to ≤ 1% [checker: 0.1% overstated —
deviations reach 0.8% at e = 0.97]) and at a = 36q e = 0.5
(r_p = 18q, the grinder remnant's own scale, drift 0.0%); ejected for e ≥ 0.975
(r_p ≤ 1.75q), within 14 orbits, by as few as 3 clamped chronons, with endpoint
speeds 577–708k bracketing the belt grinder's 686–740k ≈ v_esc(1q) — the grinder is
the clamp-zone slingshot, reproduced with one body and no contacts.** So the
mechanism is now fully located: Bounce contacts walk bodies' e to ≈ 0.97 (the only
thing they can do — elastic impulses cannot raise maxk), and the tide's inner clamp
zone (|dk| capped at q/16 below r ≈ 1.76q diagonal – 2.09q aligned [checker: "1.5q"
was wrong; geometry √(16·MU/(√2·Q)), observed clamp radii 0.98–2.01q]) is the sole
energy injector; outside
it the rounded tide holds even e = 0.97 orbits exactly-bounded. The gate gets its
constant: **no body's pericenter below r ≈ 2q (≈ 2 body radii) for ≥ 5× the belt's
dynamical time** (e < 1 − 2q/a) [checker2: the constant must be 2.1q strict — at
a = 100q, e = 0.98 puts r_p exactly at 2.0q and EJECTS (t = 70628, 5 clamps); write
the gate e < 1 − 2.1q/a]; the fix list narrows to Pass belt bodies or an
exact inner zone — not cadence, not the outer rounding (both with digests).
(20261019-1656-second-20261019-1551-dynamics-e3b7-9b3b; still unflown: the
belt-interior contact e-walk measured directly (per-body e-histograms), symmetric /
rotational rounding of the kick pair, the r_p ∈ (2.0, 2.09)q marginal-entry sliver,
self-gravity, multipoles, 3D.)

[Checker, adversarial — clean-tree rebuild reproduces every digest bit-for-bit
(C0 `e8a69ff7…`, A1 `b73b06dc…`, A2 `db751898…`, A4 `e98306bb…`, onset 12236; both
ladder arms integer-identical). Three probes beyond the author's range, two outside
it: a = 36q e = 0.94 (r_p = 2.16q) bounded 42 orbits at 0.02% drift, clamps 0; a = 36q
e = 0.95 (r_p = 1.8q) ejected t = 9458, 6 clamps — the boundary is a pericenter law
at a second semi-major axis and the gate constant e < 1−2q/a (0.9444 there) sits
between the measured arms; e = 0.97 at 2× horizon (196 608, 28 orbits) bit-stable
(maxk 526 815, rmax 138.0q every orbit). One letter correction: at e = 0.972
(r_p = 1.96q, aligned) the orbit takes a one-time pump (e → 0.982, rmax 138 → 224q,
7 clamps) and stays bounded ≥ 28 orbits — "ejects any orbit whose pericenter enters
the zone" holds only for r_p ≲ 1.8q, not the whole zone; the marginal band
(1.96, 2.1)q pumps without ejecting. The gate is unaffected: it flags that arm as
unsafe, and the safe side (r_p ≳ 2.1q) held everywhere tested. P3's <2% maxk-drift
bound failed (+9.3%, frozen tail verified: last change t = 5307); esc = 0 held.]
Checker2, adversarial — clean-tree rebuild (patch applied fresh) reproduces A1
bit-for-bit from my own build (`b73b06dc…`, contacts 3 072 187); every dossier
number recomputed from the TSVs independently and matches (season peak 102 877 vs
102 874 is a window-alignment hair; esc50 = first t with esc ≥ 800 = half of all
bodies). Three probes beyond both checkers' ranges, all confirming, one constant
sharpened: the ladder at a = 100q (third semi-major axis, T = 12 014 ch, 14 orbits)
— e = 0.97 (r_p = 3q) bounded (drift 0.11%, achieved e exact, clamps 0) while
e = 0.98 (r_p = 2.0q, exactly the gate line 1−2q/a) EJECTS (t = 70 628, 5 clamps)
and 0.981/0.99 eject faster: the boundary is a pericenter law at every a tested,
and the marginal band that pumps-without-ejecting at a = 70q EJECTS at a = 100q
within 6 orbits (checker1's caveat is horizon-limited, not a stable band). e = 0.5
at a = 70q at 4× horizon (393 216 ch, 56 orbits): still bounded, rmax never exceeds
the 14-orbit value 106.04q, pericenter creep −0.4% over the extra 42 orbits — no
slow mid-e pump. The unflown fleet×Pass scene (H = 8192): esc stops at exactly 800
(the unbound fleet itself; zero belt evictions; the Bounce twin at the same
horizon: 1379 evicted, n_in 200, maxk 739 345) — the fleet season is entirely
contact-mediated — and one hyperbolic fleet body is clamp-slingshotted 262 144 →
700 993 in 5 chronons (t = 390–394), inside the grinder band 686–740k, by a body
never on a bound orbit: the clamp pump's one-event signature. Letter nits: "27
orbits" at a = 36q blocks on T ∝ a (Kepler T = 2595 ch → ~38 orbits actually flown
— the drift verdict is period-insensitive, running-max); "14 orbits" at a = 70q is
13 complete; "achieved e to 3 digits" is 2 digits at e = 0.06 (0.065); the three
discarded cadence variants are not regenerable from the shipped patch (the
onset-invariance rests on unregenerable flights; the cadence kill stands on A4's
digest + onset alone); P3's registered "<2% maxk drift" failed (+9.3%) yet the
dossier's Predictions section says "P3 held" — the number is disclosed, the label
is spin.]

**NEW (e3b7, dynamics — open direction 2's named leftover flown: the gravity-held
belt. Verdict: the question is unanswerable on today's wiring, because the only
gravity the lattice exposes — per-body, per-chronon rounded 1/r² kicks through
`Kickable::kick` — is itself unstable at belt scale [checker: the kicks ALONE hold the
belt; it is Bounce+tide together that fail — see (1)]; the run prices the fleet season
inside the wiring's clean window and names the missing gate).** Harness:
`crates/lattice/examples/gravitybelt.rs` (this run's patch; shipped `Chronon` +
`RelativisticV1`, Q = 2^20, MU = 70·2^52, v_circ(70q) = q/16, belt 800 bodies on
rings 36–102q, fleet 800-body stream at 0.25 q/ch ≈ 1.9–3.6× v_esc; `--slim` mode
digest-identical, verified). (1) **The wiring (Bounce contacts + per-chronon tide
kicks) self-destructs a cold belt; the tide alone does NOT — checker correction, the
author's "contact-free" attribution is refuted**: C0 (thermal = 0, 0.02–5 contacts/ch)
walks maxk 99k → 727k, rms radius out 77.7 → 91.8q, escapers from t ≈ 12k, both
seeds — but with the same seeds and `Response::Pass` (contacts recorded, velocities
untouched) the same 800-body belt is flat for 32k ch (maxk 92159 → 92196 = +0.04%,
rms constant 77.7q, esc 0, ke +0.02%; checker flight, digest `b73b06dc…`), and
isolated bodies at 36q and 70q, exact and +1-quantum circular, stay bounded 19/7
orbits (maxk drift ≤ 0.25%). So the instability is contact-TRIGGERED, tide-FED
(elastic contacts cannot raise maxk; only the field injects the energy — that half of
the author's sentence stands), and cadence-independent (kicks every 4th chronon at 4×:
onset 12236 vs 13022, within the lens note's < 4× prediction; digest `e98306bb…`).
The thermal cold control follows: calm to t ≈ 4–8k (0.26–2.26 contacts/ch), then 72.9M
contacts, 449/800 evicted, endpoint 2871/ch, both seeds. **Gate the belt wiring
lacks: a cold gravity-held belt must hold bounded eccentricity ≥ 5× the belt's
dynamical time at the shipped tide cadence — this one fails its own gate.** (2) The
fleet season, inside the clean window (t ≤ 8192, cold esc ≤ 5 there), stands on both
seeds: one crossing evicts 83% of all bodies by t = 4096, 86% at saturation (esc_max
1379, esc_last 1371 s1; 1374/1373 s2); the 140–250q shell drains to 77 bodies (4.8%)
at t = 4096 and 21 at 8192 (checker: "empty from t ≈ 4k" overstated; trend supports
no persistent halo); the ~200-body
remnant then contracts (rms 46q → 15–21q) with contacts rising 1431 → 2771/ch at flat
ke (compaction, not heating; late rattle 0.63) — but the cold belt reaches the same
grinder alone, so the late state is the wiring's attractor, not the fleet's bequest
(the fleet buys earlier entry, ~2k vs ~10k ch; the season's own peak 64-ch window is
102 874 at t ≈ 7808 = 174× the cold same-window — the dossier's "season peak 183 685"
is the late GRINDER's peak at t ≈ 47.7k, where the cold control's window is 184 250).
(3) Walls on the same scene (±150q): esc 0 from t ≈ 400 on (301 bodies start beyond
250q by genesis geometry — "always" overstated), rms arrested at 72–90q, but contacts climb 403 → 5732/ch (78.3M contacts, 14 896
wall hits over 24.6k ch, wall rate falling 0.88 → 0.31/ch) — containment recycles the leaking tide's
debris; e56b's "the persistence is the confinement's" holds only in this contaminated
sense. (4) Instrument lessons: a 2048-ch smoke calibration was blind to a 10k-ch
onset (same class as ded5's fixed-window lesson); P1's kill branch fired as
pre-registered and the C0 zero-contact discriminator (flown after the kill, to
separate field pump from contact amplifier) is the run's load-bearing control
(20261019-1551-dynamics-e3b7; unflown: symmetric/rotational rounding of the kick pair,
MU ladder, self-gravity, horizon > 49k; kick cadence was flown by the checker — ruled
out).**

**NEW (e56b, dynamics — open direction 2's unflown half closed: the game case is NOT a
wall-reflection train; it is one season plus an AREA-EXTENSIVE HOT PLATEAU, and free
space is one season with no step).** `--scene mixed` on 90b7's harness (one coherent n/2
fleet at drift q/4 crossing a thermal n/2 belt at q/16, band [1.5e, 2.5e]; `--boxscale`
moves only the far wall; `--nofleet` the matched control, `--free` drops the container):
16 stored flights incl. H=24576 at n=6400, rerun digest-identical. (1) **No 4·w clock in either
series** — wall hits are a continuous rain (max 4-10/chronon vs a block bounce's n/2),
contacts autocorrelation peaks at one window (64 ch, |r| 0.38-0.98), smoothed-maxima
spacings drift and wash out (2752, 2304 against a predicted 3480): the predicted
wall-reflection train is REFUTED as the mixed case's mechanism. (2) The attractor: at
n=1600, w=435/870/1305 → late 64-ch mean 1007.5/496.0/357.0, **mean×w = 438k/431k/466k,
constant within 9% while the box triples** — the late rate follows density (energy per
area), 15.5× the matched cold control (31.9, F64 0.91), F64_late 1.29-2.61, m_late
3.6-8.6%: checker2's "persistent m_late 8.2%" is this plateau, and their "the fleet
stays coherent forever" is REFUTED — the formation dies in the first crossing (velocity
exchange; no block wall signature ever), what persists is its energy. (3) Season 1 costs
1.36·per_row contacts per fleet body at n=1600 (39.5/29; checker: σ=q/256 fleet 39.9) and
1.15·per_row at n=400 (17.2/15) — linear-ish in the lane optical depth, not one constant;
jitter fleet 38.9 — internal structure irrelevant), the momentum echo (fixed 2048-ch window,
both seeds: checker) carries 0.60-0.63 of season 1 at per_row 29 but ~1.13-1.17 at per_row 15
(the analyzer's trough windows read 0.31-0.35 on one seed and 1.0 on the other — window
artifacts; the flip is robust): arrival-time diffusion through the belt, the same
death σₓ dealt the fleet-fleet train, dosed by the belt's optical depth. (4) n=6400 to
H=24576: block means 3373→2286→2209 — stationary within horizon. (5) `--free`: one
season (peak at the geometric meet time), then dispersal to ≤1.6 contacts/window,
walls=0: **the persistence is the confinement's (walls), not the fleet's**. Sizing rule
for the belt wiring: budget one ~14·extent season (peak window ~65× the cold belt's rate), and expect a
standing ~15× rate step inside any confined region; the trigger is confinement × optical
depth, not transverse symmetry (20261019-0435-dynamics-e56b; P1/P2 kill branches fired
as pre-registered, P3's alternative branch, P5 held; NOTE e3b7: under a gravity
container instead of walls, the standing step does not survive the wiring's own
10k-ch instability — see the e3b7 entry above).**
[Checker, adversarial — all four probes confirm, and the two constants above are corrected
(evidence in the run's check.md; flights in /tmp/adv_*, digests recorded there): clean rerun
of mb1600_bs2_s1 digest-identical; boxscale 4 (outside the flown ladder) reads late×w = 417k,
inside the 431-466k band, walls max 9/chronon; free space at n=6400 (outside: free was flown
at n ≤ 1600) shows one season (peak t=2048) and walls=0 — the flat tail is untestable there at
H=8192 (the season itself is ~4.8k ch); σ = q/256 fleet dispersion (the untested axis: a
generic formation) reproduces the season (39.93/fleet body) and the plateau (492.6 vs 496.0
coherent): "energy, not formation" survives its hardest probe; the long arm's autocorrelation
at 4·w = 6840 ch is |r| 0.039 with top-5 lags all ≤ 320 ch, closing the one lag-range gap in
analyze2 (its H=16384 autocorr could not see 4·w at n=6400). The corrected echo constant on a
fixed 2048-ch window is 0.60-0.63 at per_row 29, both seeds (the 0.31-0.35 and the s1 1.0 were
the same trough-detection artifact in opposite directions); the per_row 29-vs-15 flip holds.]
[Checker2, adversarial — all three outside-range probes confirm, and both corrections
verified independently (evidence in the run's check2.md; flights in /tmp/adv2, digests
there): clean-tree rebuild reruns digest-identical (mb400: 9355d32a…); horizon 32768 at
n=1600 bs2 (2× the author's longest, and 4·w=3480 ch now inside the lag range) reads
blocks [656, 506, 485, 483], mean×w 421k, and NO clock in either series at 4·w
(contacts r=−0.078, walls r=−0.057) — the plateau is stationary to at least 32768 ch;
belt at cloudvmax q/64 (4× colder than the coldest flown): late 485.0 vs 496.0, season
41.6/fleet body, walls_max 6 — the standing rate is belt-temperature-independent (the
fleet's energy sets it, so 15.5× is a lower bound on the step); n=12800 (next octave):
walls ≤9/chronon (a block bounce is 6400), no clock, plateau present. The corrected echo
0.60-0.63 reproduces on my own fixed-window computation (0.625/0.601/0.629 across s1/s2/
jitter), confirming the 0.31-0.35 letter as a trough artifact; the season-cost letter is
1.36·per_row (n=1600) and 1.15·per_row (n=400), i.e. linear-ish, not one constant.]

**NEW (90b7, taleb — open direction 2 flown: the formation burst law is priced, and the
"unpriced half" closes split — generic formations are a ONE-SHOT 3x episode, never a
standing train; recurrence needs the head-on swap symmetry, which one quantum of
TRANSVERSE structure kills and arbitrary TIMING spread does not).** Two counter-streaming
n/2 fleets (galaxy conventions: spacing 6q, radius q, drift +-q/4, jitter +-q, dispersion
sigma/component) in a Bounce box, shipped `Chronon` + `RelativisticV1`, Q = 2^20, n =
400/1600/6400 x seeds 1-2, 38 flights, regen ~2 min, digest-identical on rerun. The law,
worst over seeds (`work/table.txt`): (1) ANY transverse structure — position jitter +-q
alone, or transverse velocity dispersion (author: sigma_y >= q/256; checker ladder: a
SINGLE velocity quantum, sigma_y = 1, already kills) — => ONE crossing burst — worst 64-ch
window 2.8-3.4x the late mean, width 2.8-2.9*extent ch (interpenetration; ~2x a train
crossing: merged streams pile up), ~0.4*ceil(sqrt(n/2)) excess contacts per body, then
FLAT FOREVER (horizon doubled to 8192: no second burst where a re-meet would fall at
~5100; late rate 1.20x thermal; F64_late 0.7-8.5 vs thermal 0.8-1.4): momentum
conservation zeroes the merged cloud's drift. (2) sigma_y = 0 AND no jitter => a standing
TRAIN: bursts 2.6-2.7x mean every 320/640/1280-1344 ch at n = 400/1600/6400, silent gaps
(windows 0.0-0.2x), amplitude constant (last/first 0.87-0.99 over 6 crossings), and it
SURVIVES arbitrary timing spread (sigma_x = q/256: 0.905-0.959 over 6 crossings at 1600
and 5 at 6400; sigma_x = q/16 smears it out in 3-4 crossings — arrival-time diffusion
through random pairing). Per crossing both regimes pay the same ~0.4*ceil(sqrt(n/2))
contacts/body — they differ in whether it repeats. (3) Exactly aligned (sigma = 0, no
jitter): the burst is a COMB — single chronons carry n/2 contacts (maxc/n 0.487-0.499) in
teeth every 8 ch (heights ramp 405->794 within each ~224-ch burst; checker: 8 ch at every
n, not 4), top-1% of chronons carry 21.4-21.5x their share of contacts, F64_late
437/1815/7035 at the three rungs, undecaying — checker2's fleet Fano1 96-128 was this
first crossing. (4) The allocator caveat: at n = 6400 a burst window costs 2.085M charged
ops vs 1.592M quiet (1.31x) — the O(n) walk dominates ops, so the 3x (and the comb's 21x)
lives in the contact/response stream, which event-driven modes and response work pay; an
ops-budgeted scheduler under-reacts to crossing seasons. Sizing rule: budget one 3x season
of duration 2.8*extent per crossing pair for generic formations; the n/2-per-chronon comb
needs exact integer equality of transverse velocity AND column alignment — representable
under the engine's own quantized conventions (velocities are integers; galaxy draws its
drifts as integers within +-q/4, not multiples of q/4),
so the belt/formation wiring gets a dimensionless trigger (transverse-velocity equality)
rather than the allocator a new tail guard (20261019-0325-taleb-90b7, taleb; predictions
pre-registered, P1's kill branch and P2/P3's numbers honestly reported in dossier.md;
unflown: mixed fleet+thermal scenes, the wall-reflection train, free-space one-crossing
geometry). [e3b7 note: the mixed and free cases are flown by e56b; the gravity container
by e3b7.]

[Checker and Checker2 blocks of 90b7 retained verbatim in git history of this page's
run; unchanged by e3b7.]

## Refuted

- **NEW — "the gravity-held belt can be flown on the lattice's kick surface to answer
  the plateau-lifetime question" (e56b's named leftover, this run's own premise)**: the
  per-body per-chronon rounded 1/r² tide self-destructs a contact-free belt by t ≈ 10–25k
  ch (C0: maxk 99k → 727k at 0.02–5 contacts/ch; thermal control: 72.9M contacts, 449/800
  evicted by 49k), so any late-time gravity-confinement reading on this wiring measures
  the tide's error flow, not the physics; the question needs a tide representation that
  passes the cold-belt gate first (20261019-1551-dynamics-e3b7).**
- **NEW — "the fleet's deposited energy holds the late contact load under gravity"
  (the pre-registered P3 prior)**: the cold belt alone reaches the same grinder (2871/ch,
  n_in 309, rms 37q at 49k without any fleet); the fleet only buys earlier entry (~2k vs
  ~10k ch) (20261019-1551-dynamics-e3b7).**
- **NEW — "The wall-reflection train" (90b7's named unflown case) as the mixed
  fleet×belt mechanism, and checker2's "the fleet stays coherent through a dilute cloud
  forever"**: no 4·w clock in walls or contacts (autocorr at one window; spacings drift),
  no block wall bounce ever (max 4-10 wall hits/chronon), and free space shows one season
  then dispersal — the formation dies in the first crossing; what persists confined is
  its energy, an extensive plateau (mean×w constant within 9% across a 3× box) at 15.5×
  the cold belt (20261019-0435-dynamics-e56b).**

- **NEW — "coherent formations keep bunching violently as a standing allocator-visible
  danger" (checker2's fleet arms read as a sustained case, and this run's own P1
  expectation)**: for any transverse structure >= 1 quantum the crossing is one-shot and
  the box settles flat — the sustained train exists ONLY with matched transverse velocity
  and aligned columns (sigma_y = 0, no jitter), where it survives arbitrary sigma_x
  (20261019-0325-taleb-90b7).**

- **NEW — "whole-run m at n = 12800 reads 3.43% against the ≤ 2.4% letter, so the
  m-bound does not extend past n = 6400" (checker's adversarial arm, horizon fixed at
  8192)**: the reading is the window, not the law — at horizon ∝ side (24576) the same
  series reads 2.00-2.10%, the ringdown is extinct from blocks 5-7, and late-window
  F64 returns to the n-independent 1.1-2.6 baseline; whole-run m never converges at
  any finite horizon (block 0's F64 ≈ 405 dominates the variance)
  (20261019-0141-second-20261018-2312-dynamics-84b2-ded5).**
- **NEW — "The breathing mode's N-scaling is an allocator-visible danger that grows with
  the formation" (checker2's reading of 834e's Fano₆₄ ladder, 1.2 → 33.4 at n = 400 →
  6400, 'both allocator-visible, both unpriced')**: the growth is the identity
  Fano₆₄ = 64·ν·n·m² with m bounded at 1.3-2.4% — per-window max/p50 ≤ 1.08 at every n
  measured, inside the strongest ringdown block included; no ratio tail grows with N
  (20261018-2312-dynamics-84b2).**
- **NEW — "A long-lived coherent breathing mode" as a steady-state object (834e's
  current-best phrasing, 'a rate modulation visible only to a scheduler that batches
  whole 64-chronon windows')**: it is the genesis shock's ringdown — block F64 decays
  117 → 2.7 at n = 6400 within the horizon, the late state is the anti-bunched baseline,
  and its period scales with the box (T ∝ side), not the cage; its lifetime grows with
  side (∝ √n at fixed fill), which is why fixed-burn measurements see more of it at
  larger n (20261018-2312-dynamics-84b2).**
- **"Denser contact work avalanches: one event triggers a chain, Fano > 1, frames spike"**
  — measured anti-bunching instead, thermal genesis (834e); refuted for thermal genesis
  only — coherent formations read Fano₁ 10-129 at fleet density (checker2).
- **"A cold dense gas collides at the equilibrium-fluid rate (Henderson g)"**: falls to
  0.42 at φ = 0.78 — caged ordered gas is cheaper than equilibrium theory (834e).
- **"A thicker layer at μ = 1e-2 raises the encounter rate"**: first-entry rate FALLS
  40 → 32, per-synodic 0.0076 → 0.0019 (80fe).
- **"The plane's co-orbital deaths are false deaths"**: kick-time planet-disk crossings,
  19/47 resolved crossers, the P/256 instrument was blind by 180× (e846).
- **"The deaths are spurious planned terminals"**: 0% terminals, 100% planet_kick (e846).
- **"The runaway is the planet doll's octave"**: root-clock far-field kick ratchet +
  drift-interval collapse on a minted ejection (taleb-6de0).
- **"Zero-velocity confinement could prove some deaths impossible"**: every IC 1.0-1.3%
  below J(L1) (e846).
- "A deterministic law with the right statistics is a true orbit of nearby ICs"
  (representation.md thesis 2) in mixed phase space (toy, 5cad); statistics side holds on
  both shipped surfaces (f50d, b9be).
- "Deterministic rounding per event ≈ noise of same magnitude": 14.1% vs 1.2% traps at
  Q = 10⁻³ (5cad).
- "The standard map's Q-scaling transfers to the shipped dense order": engine-vs-exact
  statistics flat across Q = 2¹⁶→2²⁰ (3ca8, f50d).
- "State quantization is the channel" / "the integer response's ensemble behaviour":
  refuted by the exact twin (3ca8, f50d).
- "The dense order deviates 15-45% with 5× max-dwell" / "every contact is continuum to
  1e-5" / "the neg-scene rate gap is per-contact": instrument errors and phase snapshots
  (3ca8, f50d).

## Open directions

1. **Freeze the trapping-statistics rung on the shipped dense order** — the exact twin
   (f50d) is the positive control; include the survival/death class (b9be's warning).
2. **ANSWERED (90b7; e56b; e3b7) — the formation/belt burst law is priced at walls and
   in free space; the gravity container is now measured too, with a negative instrument
   verdict: the lattice's per-chronon kick tide fails the cold-belt gate (e3b7, see
   Current best).** [9b3b, second author: the checker's Pass control is now the
   run's own record — flat to H = 49152, cold and thermal, digests `b73b06dc…` and
   `e98306bb…` reproduced bit-for-bit — and the isolated ladder locates the pump
   entirely: held at every e ≤ 0.97 (r_p ≳ 2.1q), ejected at e ≥ 0.975 (r_p ≤ 1.75q),
   so the fix target is the DK_CAP inner zone below r ≈ 2q, not the outer rounding
   and not cadence; "does not pump contact-eccentricized orbits at pericenter" is
   TRUE for every pericenter outside the clamp zone — contacts' only job is walking
   e past 0.97.] Remaining for a next run: an exact inner zone (or Pass belt bodies,
   now measured flat to 49k), the belt-interior contact e-walk measured directly
   (per-body e-histograms through the self-destruction), rotational/symmetric
   rounding of the kick pair, a per-cell tide like the engine's frame — then re-fly
   the plateau-lifetime question on the fixed wiring.
3. **The ringdown beyond n = 12800 and its onset law**: extinction at 12800 is flown
   (ded5: all-≤6 from blocks 5-7, t 10240-14336; tail = the scale-free baseline
   F64_late 1.1-2.6); onset grew 1.7-2.5× across the octave vs side ratio 1.41 —
   slightly super-linear, so the safe horizon rule is ~2× the 6400-relative horizon;
   the next octave (25600, ~40 min/arm) would pin the onset exponent, predicted
   extinction by t ≈ 18-30k, F64_late 1-3. Detuning does NOT kill the mode — mass
   spread {1,2,4} strengthens it (m 2.91%, F64 65.98, blocks [188, 50, 20, 7.4]) and
   radius spread {0.75,1} leaves it standing (F64 17.26, mean64 33798; its late tail
   F64_late 7.06 is slightly rougher than monodisperse) — the ringdown is the box's
   acoustic response, so both dephasing fixes are dead ends for it (84b2, held-out
   P5 both halves refuted). Gapped genesis (fill ≤ 0.5, cell ≥ 3) rings none (checker:
   fill 0.3 → F64 3.80, no ringdown blocks).
4. The encounter-parity certificate's negative control (a law that skips at conjunction
   must fail it) and the μ = 1e-2 horizon past 4 P, blocked by the runaway tail.
5. The 3-IC driver discrepancy (b9be ↔ e846, one vote cleaner here: same crates code,
   later HEAD, reproduces e846 exactly).
6. The tilted oblique reflection: per-contact up to 0.155 rad, ensemble-invisible;
   integrator decision.
7. Stress the preservation: γ ≫ 250, resonant three-body, longer horizons.
8. Hunt a stronger cantorus (K near critical) to bound the Q → 0 distortion rate (toy).

## Contradictions

None open. e3b7's apparent tension with e56b (plateau vs no-plateau under gravity) is
resolved by the wiring verdict: e56b's container is a wall (energy-exact), e3b7's is a
leaking quantized field — different instruments, both correctly reporting their own
law. The toy (5cad) and the shipped laws measure different error models at different Q,
as recorded.

## Runs
- 20261014-2248-redteam-5cad (awaiting grade): shadowing clause false in mixed chaos;
- 20261015-0128-dynamics-b9be (silver): dwell arm on the shipped law — trapping preserved
- 20261015-0128-inversion-3ca8 (silver, corrected in checking): shipped dense order
- 20261015-0128-dynamics-b9be (silver): dwell arm on the shipped plane law — trapping
- 20261015-0250-second-20261015-0128-inversion-3ca8-f50d (awaiting grade): exact
- 20261016-1319-dynamics-e846 (this run, awaiting grade): the 48 deaths decided —
- 20261016-1319-dynamics-e846 (gold): the 48 deaths decided —
- 20261018-0143-dynamics-80fe (this run, awaiting grade): the parity rate form — burst
- 20261018-0543-taleb-6de0 (this run, awaiting grade): the μ=1e-2 runaway is a clock
- 20261018-2040-dynamics-834e (this run): dense order to φ=0.78 — no avalanche, affine cost
- 20261015-0250-second-20261015-0128-inversion-3ca8-f50d (awaiting grade): exact twin
- 20261016-1319-dynamics-e846 (gold): the 48 deaths decided — real disk crossings
- 20261018-0143-dynamics-80fe (awaiting grade): the parity rate form — burst, two clocks
- 20261018-0543-taleb-6de0 (awaiting grade): the μ=1e-2 runaway is a clock storm
- 20261018-2040-dynamics-834e (awaiting grade): dense order to φ=0.78 — no avalanche
- 20261018-2312-dynamics-84b2 (this run): breathing mode priced — identity, ringdown
- 20261019-0141-second-20261018-2312-dynamics-84b2-ded5 (this run): 12800 flown to
- 20261019-0325-taleb-90b7 (taleb, awaiting grade): formation burst law — one-shot 3x; train needs swap symmetry
- 20261019-0435-dynamics-e56b (dynamics, awaiting grade): game case flown — one season, extensive hot plateau; no train; free space one-shot
- 20261018-2312-dynamics-84b2 (awaiting grade): breathing mode priced — identity, ringdown
- 20261019-0141-second-20261018-2312-dynamics-84b2-ded5 (awaiting grade): 12800 flown to
- 20261019-0325-taleb-90b7 (awaiting grade): formation burst law — one-shot 3x; train needs swap symmetry
- 20261019-0435-dynamics-e56b (awaiting grade): game case flown — one season, extensive hot plateau; no train; free space one-shot
- 20261019-1551-dynamics-e3b7 (awaiting grade): gravity-held belt — the kick tide fails its own cold-belt gate; fleet season evicts 86%
- 20261019-1656-second-20261019-1551-dynamics-e3b7-9b3b (awaiting grade): Pass belt flat to 49k (checker digests bit-for-bit); ladder: pump = the DK_CAP clamp zone below r≈2q (held e≤0.97, ejected e≥0.975, 3 clamped ch suffice; grinder speeds reproduced one-body)
