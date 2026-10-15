topic: nladder
status: open
closed-by:
valid-while:
updated: 20261015-0128-second-20261014-2248-inversion-4af4-7dc6

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The checker's named experiments are done to this box's limit and the wave-train claim holds on a regenerating record: memory is a step through 25 wave periods, the dissolution is measured, and 4.2x10^5 (1.9 GB) is flown (20261015-0128-second-20261014-2248-inversion-4af4-7dc6, second author).** Arm D extends arm C's own flight to cut 700,000 game-s (~117 min of play at rtf 100; 420,062 frames; canonical digest `90348a69…`, reproduced bit-for-bit by the regen rerun): rss 905 -> 913 MB from wave 1 to wave 25 (+0.9%; +0 over the last 599 k game-s; hwm = rss at the end), catalogue 200,076 constant, opens N+637, census one retired binding per body standing (h2 <= 3 of 4,161 transiently at wave edges, hmax <= 2 — 4af4's "h2 = 0 at every census" clause corrected), refusals 0, encounters exactly linear (48.55/ks, 33,984 by the cut; the player's sweep, N-independent), lag 0.000 at every one of 2,801 samples, 0 frames over 12 ms in 420,062 (worst 11.96), settle 0. **The dissolution 4af4 extrapolated is now measured**: peak/floor 103x -> 2.3x by 685 k game-s, the last window above 10x the median at wave 5 (~99 k) — earlier than extrapolated, because the between-wave floor RISES (343 -> 1,479 kicks/sample; ~+2.5 per 1 k game-s after 250 k [checker 7dc6: corrected from the author's '+210']) as the sheared cohort fills toward the belt-rate equilibrium (implied mean kick interval lengthens 27.5 k -> ~33.8 k game-s; the stream rate converges on b30b's 3.33-3.50x10^-5, reaching 2.96x10^-5 at 685 k); memory and cadence stay flat through the transition. Arm E flies 4.2x10^5 — the largest N under the box's 2 GB/process rule (rss 1,909 MB = 4,766 B/body vs 4,743 at 3x10^5; step +2,372 B/body; catalogue N+76) — through two waves: wave 1 peaks at 76,620 kicks/sample (196x median, the sharpest load measured on the plane; 1 frame over at 12.24 ms, transient lag 0.905, held 267, absorbed with 0 backlog), wave 2 +13 MB. **The record regenerates**: 4af4's `analyze.py` crashed as shipped ('%'-format TypeError masked by `|| true`) — fixed here (tuple(s) + hist_sample=a/b), it regenerates 4af4's wave tables from that run's own shipped logs; this run's `regen.sh` unmasks errors and asserts both digests. The named 10^6 flight itself stays one command on a 6+ GB box (`wavetrain 1000000 90000`; build ~2.6 GB, steady ~5.1 GB — impossible at 2 GB/process), so the 10^6 memory line remains a constant extrapolated over 7x in N, never flown at 10^6.
*[7dc6, predictions pre-registered: 1/3-8 held; prediction 2's "stream median grows with play" clause FIRED as written (median 419 -> 2,034) and is reported failed with its diagnosis — the rise is the bounded shear-fill, not a compounding term; rss/frames/backlog flat through it. Internal consistency: arm D agrees with arm C's counters at 49/50 shared census samples; the one difference (game-s 15,002, inside wave 1, encounters 643 vs 630) is the census trigger's presented-time quantization, the same wobble class as the cut. The regen rerun, flown under box contention (load 7.4), reproduced the digest and every law counter bit-for-bit while the wall view moved as the budget model predicts: frames over 12 ms late-flight, held scans standing (held_max 2,048 vs 121 idle; rss 913 -> 995 MB, allocator-retained, settle 0.62 s, lag still 0.000) — the mechanism behind the known wall-column drift, with per-body retention unmoved. Arm D flew three times in full — once idle, twice contended — one digest every time, and the contention cost is bounded: held saturates at exactly the shipped `SCAN_BACKLOG` = 2,048 (universe.rs:79), rss capped near +90 MB at 2x10^5, lag 0.000 throughout.]*
*[Checker 7dc6 (silver): everything reproduces — my window's regen re-flew both arms bit-identical (digests `90348a69…`/`0dec42f3…`, every law counter; 4th full D flight, 3rd E); the analyze.py crash reproduced on the shipped orig and the fix regenerates 4af4's tables. Adversarial, all confirming and beyond the author's domain: 2x10^5 flown to 1,000 k game-s (36 waves) — rss flat, lag 0.000 at all 4,000 samples, opens/catalogue/b_per_body unchanged, and the floor rise REVERSES past 700 k (peak ~1,471, relaxing to ~1,333 by 950 k); 10^5 to 1,000 k — same shape scale-free (floor peak ~923 -> ~870; rss flat 459; encounters 48,509 = 48,509 across the two N to the digit); a third contention sample (held_max 2,048, +84/+89 MB, digest invariant; the E wave-1 peak reads 97,405 vs 76,620 on one digest — peak-per-sample is sample-grid dependent, an instrument reading). Not gold: the named 10^6 flight unflown (box-bound; `wavetrain 1000000 90000` recorded), no board number moved 10x, nothing deleted, and pre-registered prediction 2 fired as written (honestly reported, diagnosed bounded).]*

**The in-band ruin's site is counted and the transit is priced: one site, linear in band time (20261014-2248-second-20261014-2130-taleb-625b-c481).**
The checker's named experiment, done with a per-site counter build (`scanmem`, digest-neutral: home coast `2c16867e…`, band coast `d467a24f…` and the 10⁴ burn `28a621c8…` bit-identical through it; checker c481, independent box: the home burn control reads `128d1cd8…`, encounters 4,032 vs 4,016, stable over three runs — that arm's known wall-schedule instability (4487), not the counters): **every minted scan's `candidates` vector is the whole retention — 99,715 bindings × 224 B = 29.4 MB standing per mint (Drop-counted; the record's ~59 MB was 2×), mints ~2–3 per presented game-second under L8, answered never in flight at 10⁵ and exactly once at 10⁴** (the first answer, 38–620 ms, sets `scan_ns`; the drain's `2·scan_ns` guard at universe.rs:1190 then exceeds every 12-ms frame's remainder forever; the backlog cap would need 2,048 × 29.4 MB = 60 GB before it bites). The record's "completes flat at 1,330 MB" at 10⁴ is corrected: standing grows monotonically to 2,227.7 MB (607 mints × 3.67 MB) while RSS plateaus at 1,394 MB — the resident view of a monotone retention; settle answers all in 25 s and the heap returns. **The transit bills linearly and is saved only by not burning**: the ruin band is ≈ [1.7, 3.0] AU — wider than the belt below (eccentric hulls register down to 1.7 AU: windowed, 10,880 candidates at 10⁵, 1.4 GB in 20 s), walk-all from ≈ 1.9 through 2.5 (boundary between 1.85/1.9 at 10⁴; 3.0 AU is windowed-skirt like 1.7 — 11,184 candidates, 1,523 MB in 20 s, drain frozen — not the walk-all the dossier's table claims), clean outside (1.0/1.4 AU and 3.5/4.2 AU: 4–892 candidates, drain alive, standing ≈ 0). Crossing arms: below the band under burn the transit holds 5 candidates flat; at the edge the first mint is walk-all and the death is the parked arm's shape; coasting transits mint nothing (the player's first item is the belt's own cadence). A flown end-to-end crossing is unreachable by measurement: ≥ 4×10⁶ game-s inside the band at ≤ escape speed — the parked arms are the transit's steady state and the sweep is its integrand. Fix target now constants: the keep set carries its own scale (4–5 vs 99,715, a 20,000× headroom), the drain amortizes.
*[checker c481 (silver): every load-bearing number reproduced — kill arm 69 mints, answered 0, standing 2,025.8 MB = 29.4 MB/mint, walk-all 138/138, capture 11.3 ms/call; the 1500 rerun 1,644.2 MB at the same per-mint rate; the 10⁴ arm answered 1 of 607, standing monotone to 2,227.7 MB under an RSS plateau at 1,394 MB, settle 1,215 in 24 s; coast crossings 0 mints, digests `7ac8d225…`/`5df0ad8e…` bit-identical. Held out and adversarial, all confirming: 4.2 AU clean (4 candidates, 0 MB), 1.4 AU clean (892, 0.2 MB, drain alive), seed 3 at 2.0 kills with the identical shape, parked coast at 2.0 mints nothing, 2.5 AU kills walk-all — the one sweep point the shipped regen.sh cannot itself regenerate. Not gold on the record, not the physics: the home burn digest control does not reproduce on an independent box, and the dossier's 3.0 AU row (walk-all/99,715) is contradicted by its own regen output (windowed/11,184; the 1,523 MB and the frozen drain hold), so the band's mechanism splits: walk-all core [≈1.9, 2.5], windowed-skirt edges at 1.7 and 3.0.]*


**The steady state through the waves is measured and it is a plateau: the plane survives its own
wave train, and memory — not CPU — is the flyable-N wall at every N (20261014-2248-fermi-b30b).**
At-Home coast flown past the first wave for the first time (rtf 6000 through shipped `frame_to` frames,
prune on, digests bit-identical across chunkings at two cuts; the 88-line read-only instrument
`wave_steady.rs` in the run's patch): N 3x10^4-2x10^5, seeds 1-2, 4 wave periods. Memory 2.45 kB/body
pre-wave -> x1.95 at wave 1 -> **4.85-5.06 kB/body steady, slope <= 5 B/body/wave over waves 2-4**
(kill bar 200 B; the churn regime — a retained compiled orbit per wave off a669's 1.00 compiles/kick
mint — is killed by 3 orders: it needed +2.5 kB/wave); catalogue constant at every cut (n+76),
dashboard bytes plateau 1.38-1.41 kB. The wave train is **one spacing number, ~27-28 k game-s** on
this scene (27,500 at 2,500-s slice resolution every wave; leading edges 27,000 apart at 1,000-s
slices — the period is slice-quantized, not an exact 27,500; bf21's 26.1-29.1 k sharpened); belt
rate end-to-end **3.33-3.50x10^-5/body/game-s** (cf45's read-only 3.553x10^-5 confirmed at 25x its
N); wave CPU 59-76 us a kick at 10^5-2x10^5 (to 119 at 3x10^4), incl. attendant events, flat waves
2-4 at 10^5 (at 3x10^4 the drift is 74->119 us over waves 1-4: +60%, under the 2x kill bar, not
flat); between waves the engine idles at ~2% of a core. `stats.encounters` is exactly N-independent
(2,886=2,886 at 10^5/2x10^5; 5,609=5,609 at 3x10^4/10^5/10^4): the belt contributes zero while the
player is at Home — the counter is the player's scan, not a belt stream.
[Checker b30b: reproduced and extended — plateau holds through wave 6 at 10^5 (cut 170,000, RSS
489-490 MB flat, cat constant), seed 3 same class (steady 4.90 kB), N=10^4 same class (steady
5.58 kB/body — overheads amortize worse below the swept range); regen deltas recorded in check.md
(slope 5.0 B not 0.00 at 10^5 s1; wave CPU 63-69 us at 10^5).]
[Checker-2 b30b: gold, independently reproduced bit-for-bit (digest d193e8d8..., 576,011 kicks,
enc 5,609, RSS 489-490); extensions disjoint from checker 1 — N=3x10^5 (wave-1 -> 4.71 kB/body,
kicks 3x, no knee), 8 waves at 3x10^4 (RSS flat 152 MB to t=230,000, slope 0; the wave shape
disperses by waves 6-8: young-train sharpness is not a permanent of the scene), chunking digest
identical at 10^5 across two waves, seed 5 same class, enc=5,609 confirmed at 10^4. Dossier prose
slips (0.00 B vs 5.0 B; 5.8/4.5/6.2/6.3 s and 55-69 us vs the regenerable 6.3/6.3/6.2/6.6 s and
63-69 us) recorded in check2.md — decision-neutral, regen exits 0 bit-identical.]
Composed at 10^9: 1.6 cores at rtf 1 / 157 at
rtf 100 at 45-69 us a kick; memory kill-N **8.8x10^5 (4 GiB) / 1.12x10^6 (~5.5 GB usable; 10^7 = 49
GB)** vs CPU kill-N 6.4x10^6 (2.4-3.8x10^6 at the measured 76-119 us — still above the memory wall) —
**memory binds first at every point, one-time at wave 1**: the merged
"10^6 for 20 s" rung sits on the wall (the 20-s window ends ~9,000 game-s before the first wave),
and break 4's promotion wiring is safe against the train (waves add no standing memory after the
first). Domain: at-Home coast only — the player-seam ruin (break 3, 625b, d7e3) is excluded by design
and stands; Linux VmRSS (HWM=RSS everywhere; the ladder's macOS post-wave 5.2-5.4 kB brackets from
above); the 10^6 line extrapolates a constant measured flat over 6.7x in N, 2 seeds, never at 10^6
itself.

**The wave train is flown and the plane is flat in play time: memory is a step, not a staircase, and the standing digest instability is the cut, not the engine (20261014-2248-inversion-4af4, inversion lens).** The record's break 2 ("2.6 -> 5.1 KB a body at the first kick, exponent 1.0 in kicked bodies") assumed the step happens once; no flight had reached a second wave. `examples/wavetrain.rs` (this run) flies the plane bit for bit (`plane_extra`, seed 1, coast, rtf 100, 12 ms, player at Home) through the train: at N=3x10^5, cut 150,002 game-s (25 min of play, 90,062 frames, 137 s wall), five waves at 13.5-15.75k / 40.75-43.5k / 68.25-72.25k / 96.25-101.25k / 124.25-130k game-s, each ~N kicks (304,341...282,069). Memory: 672 MB at build (2,233 B/body rss) -> 1,357 after wave 1 (the climb is linear through the wave, ~78 MB per 250 game-s = one binding per kicked body) -> **+7/+2/0/0 MB at waves 2-5** (hwm = rss = 1,366); the catalogue free list returns every rebound slot (300,076 live at every sample), the history census holds exactly one retired binding per body (h2 = 0 between waves at every census; transiently inside a wave up to 1 of 4,106 holds 2 at 3x10^5 — checker regen and seed 2, up to 4 — and up to 3 at 2x10^5), settle at cut finds 0 events outstanding, lag 0.000 at every sample including wave peaks, 3 frames over 12 ms in 90,062 (worst 14.08 ms), held scans only inside wave 1 (0 -> 191 -> 0, flushed as the wave passes). At 2x10^5 to 250,000 game-s (10 wave windows): rss 906 -> 914 MB (deltas <= +3), catalogue constant, 0 frames over 12 ms, worst 11.96 ms. So the memory term is bounded by kicked bodies, not by play time — the plane at 3x10^5 is certifiable for play-length flights and the binding constraint for longer flights is the cadence (break 1), not retention. The train also **shears**: width 1,750-2,250 -> 5,000-5,750 game-s by waves 5-10, peak 32-36k -> 8-20k kicks/sample — the birth wave is a session's worst frame-load event and dissolves toward the steady stream (~20 waves), so the birth stagger buys the most exactly where it matters most. **Digest protocol:** two identical wall-budgeted flights cut on presented time differ — game_s 150,002 vs 150,001 (one tick; the presented tick is wall-quantized by the budget) and exactly the 5 kicks due in that tick; the same flights under the canonical cut (`frame_to(limit)` + `settle(limit)`, universe.rs:1067) are identical to the digit on every counter and digest (`58de94ab...`, kicks 1,743,559 = 1,743,559); at N=3,000 both protocols agree (`47fd4a85...`). This closes direction 12 (4487's "two pristine runs differ") and generalizes 38bf's checker note: *any* digest at a presented-time cut is wall-unstable under budget pressure; wave rungs freeze cuts at absolute ticks. Domain: seed 1, coast, player at Home (in-band is 625b/d7e3's ruin; burn re-measures the second seam), N <= 3x10^5 (this box's 2 GB rule; 10^6 = 5.1 GB is M1 territory), rss is Linux VmRSS (~9% under the ladder's macOS phys_footprint at equal B/body).
*[Checker 4af4 (silver): the canonical arms reproduce bit-for-bit — digest `58de94ab…`, kicks 1,743,559 = 1,743,559, rss 1,366, frames 90,062, b_per_body 1,378 — and the presented-cut wobble reproduces in kind (±1 tick, 6 kicks here vs the author's 5, digests differ; at N=3,000 both protocols agree). Wall-dependent micro-numbers move run-to-run: frames over 12 ms 0 (worst 11.98 ms) in the regen vs 3 (14.08) as written, armC's wave-1 peak 35.6k vs 32.4k as written, the mid-wave census 2,858/4,106 vs 2,784; the "4,515 B/body" post-wave figure mixes MiB with 10^6 (1,357 MiB / 300,028 = 4,743 B/body; the ladder's 5.1 KB still closes via the stated ~9% platform offset). `analyze.py` crashes as shipped (TypeError in the window formatter, masked by `|| true`), so the wave tables were re-derived by hand from the raw logs — the run's own script cannot regenerate them. Held out beyond the author's domain, all supporting: seed 2 at 3x10^5 (three waves, rss 1,364 -> 1,371 -> 1,371, same train spacing, lag 0.000, h2 <= 4 transiently); half budget 6 ms (max transient lag 1.24 game-s, 66/37,890 frames over, settle finds 0 outstanding, memory step identical — the zero-lag result is not knife-edge at 12 ms); and N=3x10^3 flown to 300 k game-s, ~161 kicks a body, ~28x the author's per-body depth (rss 17 -> 21 MB, flat from 100 k on; hmax <= 2; b_per_body ~1,480). Silver, not gold: no bottleneck number moved (the certificate extends flight length 200 s -> 25 min, ~7.5x on the time axis), nothing is deleted from the engine, and the inversion failed to kill — a confirmation, not a premise refutation; the gold experiment is named below in check.md.]*


**The wave's untested exposure is measured and it is a memory ceiling, not a stutter: the player
inside the belt band turns the first-kick wave into a process-killing accumulation of held scans
(20261014-2130-quant-d7e3, quant lens).** Scene: the plane bit for bit except the player orbits
at 2.5 AU in the root doll among the belt ships (`plane_extra_belt_player`), L8 burn, rtf 100,
12 ms budget, the 16,000 game-s cut — 38bf's `wave_input` protocol with only the player moved;
the validity control reproduces 38bf's digest `c2b834bb…` exactly (capped and uncapped, kicks
225,949 = 225,949, encounters 1,624 = 1,624). Findings, all on shipped main + the pending
`ES_PULL_CAP` patch: (1) **at every N ≥ 5×10⁴ measured, both arms are OOM-killed** — 2×10⁵ uncapped 77 s in and
capped ~210 s in; 5×10⁴ uncapped and capped at the same 6.88/6.87 GB peak with identical
trajectories (the accumulation is deterministic and pull-independent: the cap does not touch
it); 10⁵ capped at 11.83 GB (the per-held answer scales with N); no in-band digest exists at
any N ≥ 5×10⁴, so the cap's digest certificate cannot even be posed there; (2) **the
mechanism is the held-scan standing memory**: in-band at 5×10⁴ uncapped the RSS climbs
monotonically through the flight (6.05 GB at frame 5,700 → 6.6 GB at frame 9,000 → killed at
6.88 GB peak before the cut; ~6.5 MB per held scan, held count 1,110→1,196 with no demotion —
an all-bodies-sized answer per held scan where the out-of-band record's is ~10 KB), against
0.89 GB for the whole out-of-band flight at 4× the bodies;
(3) **at N=10³ in-band the engine holds frame budget** (0 over, max 11.6 ms, 96 MB, digest
`ad8a0e78…`; one noisy pass's 351 ms spikes were box contention — same digest, clean rerun): the
exposure is not frame time but memory growth; (4) the player itself becomes a root-doll ship
under thrust: its burn chain owns the kick counter (26,054 by the cut at N=10³).
The guard the cap needs before merge, named: hold the capture keyed on the candidate's doll
being mid-wave (the `SCAN_BACKLOG` idiom) **and bound the held answers' standing size** — a2c1's
"~10 KB a held scan" is an out-of-band number; in-band each stands ~650× that at 5×10⁴ (~2.6×10³× at 2×10⁵). Domain: seeds 1
(seed 7's arm started and was killed to free the box), N ∈ {10³, 5×10⁴, 10⁵, 2×10⁵}, a = 2.5 AU
planar near-circular, one shared Linux box with a 2 GB/process ceiling; the OOM's exact interior
(held-answer contents vs capture buffers) is inferred from the per-scan growth rate, not heap-
profiled; the 5×10⁴ digest pair and the 10⁵ capped arm are in the run's `out/`.
*[checker d7e3: every digest reproduces bit-for-bit; the 5×10⁴ pair completes on the regen's
quieter box (digest `0898731…` cap-identical — "no in-band digest at any N ≥ 5×10⁴" withdrawn),
and there BOTH arms run 606/607 frames over 12 ms (p99 15.7/17.8, max 200.9/208.8 ms, only 15 in
the wave window) — the cap does not tame the in-band frame seam at 5×10⁴. Held out: seed 7 at 10³
and a full through-the-wave 10³ flight (the author's arm flew only ~1,500 game-s and settled the
wave) both clean, digest `ad8a0e78…`, held saturating at 82 — demotion works at 10³; N=10⁴
completes at 1.36 GB with held 1,215, per-scan standing ∝ N (peak ratio 5.05×).]*
**The a669 dial is refuted on shipped code, and the mint it targeted is counted: 1.00 compiles/kick
(20261014-2130-second-20261014-2012-system-a669-eb2d).** The flip-gated rebind is wired (patch in the
run: quantize the fitted key by a dial, reuse the compiled trajectory and `Arc`-reuse the entry on
key equality, default bit-identical to pristine on the wave, crossing and frame_digest), and the
shipped stream is 34,606 compiles for 34,537 kicks with zero exact-key reuses. But the live
`OrbitKey`'s key words walk far faster than the replica's arithmetic — fat-tailed, not one constant
(checker-2: the coarse arms fit ~2^-13, the fine arms track ~2^-22.5 = the replica's own p50, and the
de-gated (2,16) reuses 0.009 in a wrecked scene) — so at every map-alive grain the run is >=10x shorter
than q/p50 predicts (checker-2: (12,16) predicted ~158, measured 3.1); the flip run saturates at ~4 at
scale quantum 2^-11 (reuse 0.747) where the map is already dead (encounters 934->0, 1,342 refusals);
map death is grain-idiosyncratic, not a scale threshold ((12,16) alive, (33,20)/(24,16)/(12,12) dead),
and the best measured map-alive cut is 3.1x at (12,16; reuse 0.682, encounters 928, 9 refusals —
checker-2), 1.75x at (12,20; reuse 0.430, encounters 928, 1 refusal), 1.33x at (12,24) — and the
(`Space(Range)`) on this scene at every material-reuse grain measured ((12,12), (12,16), (12,20),
(12,24) — checker-2 ran the last three). Mechanism: the key is re-fit from decode(tube)+residual and the residual is a frozen
Cartesian offset that maps to element changes each rebind — the walk is representation-driven, which
is law.md:36's recorded objection, now measured with the gate wired. The lever that remains is a key
that does not walk (carry the fit's drift as an integer phasor), not a coarser quantum.
   *[Checker eb2d: the table regenerates end-to-end (runner) and the arms hold beyond the author's
   domain — N=10^4 keeps the mint at 1.00 (41,606/41,537) and (12,24) map-safe (reuse 0.207,
   encounters 928). Two corrections. (1) The map-safe frontier is scale >= 20, not (12,24): the
   untested (12,20) is map-safe with reuse 0.430 — a 1.75x cut, the best measured, still <= 2x and
   nowhere near 10^2x. (2) The Space(Range) panic is not metered by reuse or coarseness: the
   quantizer path panics the same readout at the full-width identity dial (48,62 — wave counters
   bit-equal to default, digest moves at the last ulp, so the dial is never bit-neutral when on)
   while coarser (16,32)/(20,36) run — a rounding-boundary fragility of quantize() on this scene,
   not the walk; the held-walk evidence is the 30-500x/900-1600x arms, and patched-default jacobi
   equals pristine exactly. Dossier typo: 24,16 kicks are 33323, not 33223.]*
   *[Checker 2 eb2d: everything reproduces from a clean tree (wave raw-identical; frame5/crossing
   wall-times only; patched-default jacobi byte-equal; every table cell and both refusal counts).
   New arms, all outside the author's coast/seed-1/N=3000 domain: burn L8 keeps the mint at 1.00
   (37,426/37,338) and the same frontier ((12,20) reuse 0.397, encounters -0.05%; (12,12) 0.691
   with -2.7% encounters and 422 refusals); N=10^3 (0.264/0.456) and N=10^4 (0.207) hold; seed 2
   **leaks: map-alive dials drop encounters -14%** ((12,20) 2406->2052), so "-0.6%" is a seed-1
   number. Two corrections folded in above: (12,16) is map-alive at reuse 0.682 — a 3.1x cut, the
   best measured, refuting "scale >= 20" and "encounters 0 at scale <= 16" as rules (map death is
   grain-idiosyncratic; (2,16) wrecks the scene instead: kicks -34%, encounters 250); and the
   ~2^-13 single-constant walk is a tail statement, not a median — it fits the coarse arms, the
   fine arms sit on ~2^-22.5 (the replica's own p50). The verdict is unchanged by both: the
   maximum reuse measured anywhere is 0.747 (run 4, map dead), the map-alive maximum 0.682 (run
   3.1, readout panics), and a669's composition needs run ~22-100 — unbought at every grain. The
   1.00/kick mint holds at N 10^3-10^4, coast and burn, seeds 1-2.]* 
**The seam the record twice declined to test is measured, and it is ruin, not cost: the player inside the belt band (20261014-2130-taleb-625b).**
With the player a circular 2.5 AU body of doll 0 (`plane_extra_band`: everything else bit-for-bit `plane_extra`) at
 N = 10^5, an in-band L8 burn retains **~465 MB/s from the flight's first seconds, plateaus at 11.2 GB and is killed
 (exit 137) before the cut** — every at-Home arm of the same scene flies in ~1.1 GB (the plateau value is box-bound: the
 checker's watched rerun was killed at a 5.1 GB plateau — the kill, the retention and the ~0.45-0.5 GB/s growth are the
 invariants). The term is the scan, **214x**
(capture 30.2 ms/call) to **1,087x** (a held answer 614.6 ms/call) its at-Home cost, times the burn's ~50-frame
re-plan cadence (~190 scans x ~59 MB ≈ the 11.2 GB plateau; coast's 2 player items stay flat; the retaining site
unlocalized, one counter away). Under coast the wave still lands **one 2,008 ms frame — 30,341 events, the player's
first item mid-wave sweeping the belt's overdue backlog** (`pull_ships(key, !in_root = false)` from tick 0: the bill
6138 measured after the burn's rebind at frame 950, here native); seed 2: 1,062 ms. At 10^4 seed 1 the same burn
completes flat (1,330 MB, max 47 ms) but seed 2 lives at the seam's other face: **max 17,261 ms, 111 frames over, 101
game-s of lag** — a 364x seed spread on the worst frame. Certificate: unlimited vs 12 ms budget, digest `d467a24f...`
 bit-identical (the seam is a cost, never a law). Domain: a parked player mid-band, held L8 burn, Linux shared box,
 10^4-10^5 only; a player crossing the band (the transit case) unmeasured; both kills had prof on (the checker's
 prof-off rerun runs away the same: ~0.5 GB/s, killed — not prof-only). Checker's domain edges: 10^3 in-band L8 flies
 flat (max 11.9 ms, 0 over — the cliff sits between 10^3 and 10^4); L1 at 10^5 completes but retains ~4.2 GB with 350
 frames over budget — the ruin is dose-dependent on the re-plan cadence.

**The ladder's breaks 1, 2 and 4 are one dial: the tube key's own quantum (20261014-2012-system-a669, system lens).**
The belt's per-kick dL/L is 2.1e-7 (p01 3.0e-9) against the key's documented L range
(1/4 <= L <= 4096, Q32): 226 L-quanta a kick at the coarsest legal scaling, 3.7e6 at the
finest — the key flips on 100% of kicks at every legal scaling, so `Rebinding::from_state`'s
unconditional `Orbit::compile` (binding.rs:422) mints a compiled orbit per kick: the wave's
~30 us/kick CPU (break 1), the 2.6->5.1 KB first-kick doubling and the retired-segment churn
(break 2), and the birth build's compile term (break 4) are the same bill. The velocity-word
carry gate (step.rs:424) never blocks on this belt (p01 |dv| = 2,363 quanta; early returns
0.0%). The binding's residual already carries sub-quantum exactness legally (bind.rs: "the
remainder is carried and never dropped"), so a per-population coarser key with a flip-gated
rebind divides all three breaks by the run length — measured exactly linear (diffusion-
limited, no synodic-absorption bonus: cancellation 0.168): E 3.3 kicks at Q48 (flip
fraction 0.300, |dE| p50 0.23 quanta) -> 107 at 2^5 -> 857 at 2^8; L measured linear too by the
checker: run 107 needs ~2^15-2^16 (at 2^13 the L run is ~28, not the dossier's ~2^12-2^13).
Composed: the pair run at 2^5/2^13 is ~22 (~10^1.3x, checker); ~10^2x needs ~2^5(E)/2^15(L) —
off the wave CPU, the churn and the build compile. Adoption check: B5/B12 on the coarser walk (between-events readout drift grows by
the coarsening factor, ~2 km/step at 2^13 = 6e-9 relative, re-anchored per flip). Hole
named: the naive root-doll reading puts the belt's L at 1.6e4, outside [1/4,4096] — either
doll 0 rescales (the bracket is invariant) or belt tubes are keyed otherwise and only the E
axis (319.3 m^2/s^2, f0a2) stands (3.3->107x at 2^5). Checker corrections: the live tube key is
`OrbitKey{periapsis: Scalar, k: Q48}` (orbit.rs:31-34), finer than the legacy Darwin `Key` whose
[1/4,4096] range the bracket uses (that `Key` survives for shipmem fixtures only, ENVELOPE.md) —
the flip conclusion holds a fortiori, the quoted quanta describe the legacy words; and the standing
record must be answered, not just B5/B12: law.md "Not adopted: a quantized (E, L) memo for kicks:
it re-rounds the orbit at every kick, a random walk (principle 13)" and crates/universe/tests/memo.rs
(exact keys never recur on distinct kicks; the law's quantized cell already hits >90%; wiring it is a
law-level choice behind B1/B2/B9) — the delta claimed here is the flip gate plus the residual carry.
The 100%-flip holds at the shipped 2.814e4 s cadence (at h/4 the p01 |dL|/L falls below the coarsest
legal quantum — checker). Domain: SI Kepler replica of the shipped roster and cadence, cold belt only
(the checker's inner system, 0.45-0.85 AU, also flips at any grain); silver, one build from gold.

**The input seam inside a wave is measured and bounded: with the pull capped, a player decision
mid-wave costs O(1) — 0.168 ms once, ≤ 0.229 ms at 60 Hz through the whole wave — and a no-op
decision moves no kick but can move the log (20261014-2012-components-38bf).** On shipped main plus
this run's re-derivation of bf21's cap (`ES_PULL_CAP`, default-unset; bench `wave_input`), the wave
scene (2×10⁵, seed 1, L8 burn, rtf 100, 12 ms, cut 16,000 game-s settled): uncapped worst frame
1,486.9 ms / 9 over; capped 12.487 ms with the digest bit-identical (`c2b834bb…`, kicks 225,949
equal — bf21's certificate reproduced independently); then one no-op decision at the wave's p50
costs 0.168 ms (≤ 2 events), and 657 of them (every frame of p01–p99, an adversarial bound: the
shipped page calls `input` on key change only, `session.rs:118`) cost ≤ 0.229 ms each — max frame
12.5 ms, 1 over, lag +0.21 game-s. The checker-2-bf21 exposure (`input` resolving the player's
items over an overdue backlog outside the queue) is **bounded, with or without the cap**: O(1), not
O(backlog); the input path needs no deferral machinery. Margin: kicks bit-equal
everywhere, but the 657 no-op decisions add encounters at the log's margin (+1 measured; +2 on the
checker's re-run — pace-dependent: the decision's requeue carries scans at ticks the scheduled items
never scan) — "same keys" is not "no
event". Unmeasured: a key-**changing** decision mid-wave (a turn re-plans the player), the player
inside the belt band, 4×10⁵, a busy box (4487's 1-event second seam is load-conditional; it did not
appear here — the worst frames are the budgeted drain itself, and P1 vs P2 digests equal under
settle-at-cut on one pair, which does not retire 4487's instability finding).
   *[Checker 38bf: every counter and the P1/P2 digest identity reproduce (8 further flights);
   the exposure never fired **even uncapped** — one mid-wave decision with the cap unset costs
   0.154 ms at rtf 100 and 0.158 ms at rtf 200 (the uncapped frame monsters 1.3–1.9 s are the
   scheduled pulls, not the input path; the lane is already tiled to the player's key), so "real
   as a mechanism" is structure, not a measured cost. The named untested arm is answered: a
   key-changing decision (`word(5,8)`) costs 0.20 ms at 2×10⁵, and 657 of them every frame at
   3×10⁵ hold max frame 11.97 ms (0.26 ms a call, RSS 1.38 GB; `one` at 3×10⁵: 0.161 ms, max
   12.1 ms — the window is N-independent, `belt_first`). The one-decision digest does not
   regenerate (three runs, three values at the same frame — decision-bearing digests at the 16 k
   cut are wall-unstable, 4487's direction 12; compare counters, not those digests). And
   `session.rs:118` does not exist in this tree — no shipped caller of `input` outside examples;
   the realism caveat rests on an unverifiable citation.]*
**The frame path's first standing deletion is executed, digest-identical, and its horizon constant is
refuted (20261014-2012-second-20261014-1631-library-7f99-5903).**
The radial index's two shared-state sensors are deleted on shipped code: the doll-wide write-once `speed_cap`
(a2c1's 84x poison) and the all-dolls density rule whose misfire walked every body; each body's registration is
widened by **its own** speed bound over one scan horizon instead, with a loud exact fallback (`h` beyond the
horizon walks the doll). The universe digest is **bit-identical on all four flight arms** (10^3 and 10^5 coast
`6895ce06...`/`f98d6b13...`, 128 encounters = 128 each; 10^4 burn `d1822b88...`, 3,946 = 3,946; the
`ES_SCAN_H=1` walk-all control identical), and the walk is **constant in N: 66/call at 10^3 and 10^5** -
15x under the density walk-all (1,017), 2.9x under the poisoned window (194), kept 319 -> 49. The sustained
certificate need is ~49 kept: the "~17-body keep set" was the pre-kick transient (seq 1). But the one-constant
horizon is **refuted as the contract's equal on three independent signs**: the burn's finer h pays the coarse
widening (75 -> 248 walked/call); belt scale pays 12x build and ~9 kB/body (98.5 s, 1.1 GB at 10^5); and the
shipped drop-contract test fails (`the_radial_index_finds_what_the_brute_force_finds`: at h=2e9 the far ships
widen back in, 38/38 kept). Exactness never breaks - the drop contract does: the widening must carry its own
scale (a dyadic widening level per interval class, or per-doll units), the named next experiment. The same run
measured the library lens's promote-on-refusal on the 18d2 surface (branch, re-emitted probe - the "shipped"
chatter case is not shipped): at all 193 of the 0.49 R_H retrograde chatter's would-be handoffs the current
doll's refit **succeeds** (0 refusals), and gated on it the chatter collapses 193 -> 0 - at 3.9-8.8x the events
on the body (the child doll never engages): the refusal gate is a kill-switch, not a surface.
  *[Checker 5903: the constant-in-N walk is **coast-only** — at 10^5 burn (the decade the author did not fly)
  the deletion walks 1,975/call against base 74.9 (kept 1,970: the coarse widening pulls the far belt into the
  window; the penalty grows with N in burn, 3.3x at 10^4 -> 26x at 10^5), digest `c53c2de6...` identical with
  3,946 = 3,946 logged: exactness holds, and this is a fourth sign the widening must be interval-and-scale
  relative. The chatter half's probe source (`tests/handoff.rs`) is not in the run record — its numbers were
  verified on the run's surviving compiled binary — and the gated refusal also fails the branch's own
  `a_moon_born_in_the_planets_doll_never_leaves` (passes ungated): load-bearing handoffs die with the chatter.]*

**The wave's fix is measured and certified, and the wave is a standing train (20261014-1719-dynamics-bf21).**
Capping the player's look-ahead pull (`pull_ships_capped`, 9 lines, `ES_PULL_CAP`-gated; the pull resolves every
ship below the player's *next* item inside its current one, outside the budget — the burst 6138 named) holds the
same 2×10⁵ burn flight at **max 11.97 ms, 0 frames over 12 ms** against the baseline's **1,364.9 ms / 12 over**
(114×; monsters 25,547 events, spaced exactly 50 frames, reproduced from 6138's basin), with the digest
**bit-identical**, encounters 4,060 = 4,060 and kicks 225,975 = 225,975; the wave's cost becomes the drain's
1.45 s lag, unchanged from the coast control. The certificate *kills the literal fix*: deferring the capture to
answer time (the "hold the scan" reading) breaks it — 4,029 encounters, digest differs (the late capture meets
pruned history: the drain's ~1.45 s game lag against the prune's 2×light-distance retention) — so the capture
stays at the player's item (every item before its tick is resolved by key order; the pull-ahead was eagerness),
and only the answer is held, which `Held` already did. The wave itself is **not a one-shot shock**: every belt
body's step is ≈ 26.1–29.1 k game-s (a continuum, not one power of two), and the cohort recurs with its shape
(second items 26,101–29,084, width 1.1 k → 3.0 k game-s: no phase mixing), so a rung must fly past *every* wave
(~27.5 k game-s apart, ≈ 4.6 min at rtf 100), not just the first; the arrival width is a generation choice
(stagger the birth grid over one step → ~24× flatter drain utilisation), unmeasured here. Domain: seed 1, the
ladder belt, Linux shared box, 2×10⁵ burn only; the view's gather during the deferred window unmeasured.
   *[Checker bf21: reproduced three ways — clean tree, patched-unset and capped are one digest
(`ba1a66b4…`), so the patch is default-neutral and the cap changes no bit; held out on seed 7
(1416 → 12.1 ms, digest equal) and at 4×10⁵ (3276 → 12.0 ms, 61,701-event items, 1.88 GB RSS —
this box's ceiling). The digest is cap-value-invariant (ES_PULL_CAP 0 and 1 also give `ba1a66b4…`,
equal counts): on these scenes the scan's candidates never overlap the wave backlog, so "the
pull-ahead was eagerness" is scene-structural, not a law — a player inside the belt band during a
wave is the untested exposure. And the frame profile is not cap-monotone: cap 0 leaves 734 ms
monsters, cap 1 leaves 94 ms (other unbudgeted terms near the player's item re-emerge), so
"any small bound" is wrong — 64 is a measured operating point. The patch's comments describe a
capture-deferral that is not in the code (`backlog` is dead; the capture is immediate): rewrite
them at adoption. The wrong-variant numbers are the author's killed build, not rebuilt by the
checker.]*
   *[Checker 2 bf21: every certificate reproduced independently — pristine main (universe.rs
   reverted, same example) gives the same digest `ba1a66b4…`, so default-neutrality is proven, not
   argued; held out on seed 3 (1,257 → 11.96 ms, digest `618d9d23…` equal, counts equal), at 4×10⁵
   (3,901 ms / 65,556-event items → 11.97 ms, 0 over, digest `1d13ab6a…` equal, RSS 1.84-1.86 GB
   — this box's ceiling) and coast (`c55dcf84…` equal). Two corrections to the notes above: (a) the
   non-monotone caps are NOT reproduced on a quiet box — cap 0 and cap 1 both hold 11.98/11.97 ms
   with the same 333-events/frame profile and the same digest, and 333 events ≈ 16 ms of engine
   work leaves nothing to bill a 734 ms frame to: those spikes were box contention (wall time,
   descheduling), not engine terms, so "64 is a measured operating point" rests on schedule noise;
   (b) the neutrality is law on the queue path — the scan reads `binding_at(j, t)` (encounter.rs
   capture, same-doll candidates only), and key order makes every binding at t final before the
   player's item pops — the one hole is `input` (universe.rs:1182), which resolves the player's
   item over an overdue backlog outside the queue: a player issuing input inside a same-doll wave
   is the real untested exposure. Settle at 4×10⁵ grows to 11 s (the deferred backlog answered
   after the flight): the drain, not the frame, scales with N.]*

**The belt's cadence is the doll's clock, and the 10⁹ rate law is corrected 24× (20261014-1719-fermi-cf45).**
Measured on shipped main (`examples/cadence.rs`, read-only, seed 1 + held-out 11, N 1000/4000):
every root-doll ship steps at 2^step_log2 per period of the doll's **shortest secondary**
(P_D = 77.24 d — the record's "Cinder 88 d" is off 14%), Δs rounded one octave down and refined
+7.9% by f'(U_P+c): interval **2.814×10⁴ s p50, flat in a** across 2–3 AU (quartile means
2.818→2.805×10⁴ s; the own-period law demands ×1.84), rate **3.553×10⁻⁵ /game-s/body** seed- and
N-stable, kicks/own-orbit 2,674–5,484 (5–11× the old 512/orbit bar); three instruments agree
(plan interval; per-body counter exactly 2 kicks in 60,333 game-s; first kicks at 1.41×10⁴ s inside
taleb-6138's measured wave window), and `step_for` on the same bodies gives 6.77×10⁵ s — **24.1×
slower**: effb's "rate = 2⁷/P_own, a pure birth constant — the whole bill" is the *secondary-doll*
law read onto the root doll (`step.rs:554` reaches `step_for` only when `!on_clock()`; the roster
reproductions 3071/7497, 202–223 kicks/orbit, live in secondary dolls — a code-path reading, not
re-measured). Recomposed at 10⁹
(`compose.py`): 3.55×10⁴ kicks/game-s = 8.2 cores at 231 µs, 1.07 at the M1's 30 µs, 0.10 Carlson,
0.0039 key arm (rtf 1); **at flying pace the shipped step_log2 7 is 148× over even at 30 µs** —
the dial fits only at its coarse end (step_log2 0: 1.16×; Carlson ≤ 2–3: 0.45–0.90×; key arm
already 5: 0.14×; as shipped only the key arm fits, 0.54×), and its anchor is **P_D × the
f'(U_P+c) refinement, never P_own**. The birth wave at 10⁹ (all bodies at tick 0, first kicks
1.34–1.45×10⁴ game-s) is 26× the steady stream — 10 s/s at rtf 100 even at the key arm: birth-phase
staggering is not optional. effb's kick-term composition, its checker's "0.5 AU belt 5.3 cores at
231 µs" line, and the cadence axis of 1738's cube all inherit the correction; ladder.txt's law was
right with the wrong period label. Domain: the ladder's belt (Rayleigh e 0.07, periapsis > 1.2 AU,
planar, prograde) at 2–3 AU, one Linux box; not measured: belts inside P_D's orbit, near
secondaries (f' shortens), under thrust, or a P_D that itself rebinds (the doll's clock is
dynamic); the locals' arm of the probe carried a doll-unit bug and made no claim.

**The deletion program gets its method, priced from Julien's library mined verbatim for the first
time (20261014-1631-library-7f99; 762 highlighted books, 4,580 highlights cached in the run).**
A grep-backed audit of the engine's own record: **26 kills, 5 revival-shaped events** — landed
same-job add-backs 2 (the rotating binary doll — the family H0210 killed; the chronon kept as test
judge) = **8%**, all five = 19%: the law level brackets Musk's 10% add-back quota ("if you do not
end up adding back at least 10% of them, then you didn't delete enough", Isaacson). The shipped
frame path holds **0 add-backs** (only the frame tier and the old view search were ever deleted
there) — below quota, and the unfired backlog is exactly the named terms: a2c1's two sensors, b29a's
sticky promotion, 0e37's `entry` field. Ordering: automation last (the allocator lands after the
deletions; the 6 anchored guard/fallback sites — the caps, the density rule + walk-all, the hull
widening — exist only to manage undeleted state). Promotion collapses to a **filter**: the refit's
refusal is the trigger (b29a's 9–26% at Δv/v ≈ 1), no hysteresis machinery, no sticky binding. The
direction-0 build gets its acceptance number: **427 (p95) – 877 (p50) recompiles/frame** at 33 ms
against measured demand 0/s (belt) and 1.4/s (cast) — ≥ 9×10³ headroom; the +24 B two-word
completion is the expected add-back (4.6% of the 520 B deleted). All numbers: the run's `audit.py`.
   *[Checker 7f99: the revival census misses one landed scoped restoration — r9 killed kick-avg,
   yet `docs/law.md` keeps kicks orbit-averaged on stable orbits (PRINCIPLES register) — a sixth
   revival-shaped event, putting the law level at 3/26 ≈ 12% landed; and the 26 kills are a sample
   (the Refuted sections of encounters/b12/kick-cadence/kick-jet hold more). The frame-path 0 and
   the ordering survive both corrections.]*
**The wave's freeze is the player's doll, measured on shipped main: the shock a 20 s rung never
sees (F1's window ends 11,000 game-s before it) is absorbed as 1.45 s of lag when the player is out of
the root doll and as unbudgeted 0.3–1.2 s single frames when it is in it (20261014-1631-taleb-6138).**
Every belt body is born at tick 0 with one Δs, so the first kicks arrive as one smooth wave at
13,037–14,542 game-s (belt_first, 199,700 bodies: p01 13,377, p50 14,072, p99 14,473; ~221 bodies a
frame mean, no intrinsic spike — the monsters are accumulation). On this Linux box, 200 s flights at
rtf 100, budget 12 ms, L8 burn: worst frame **315 ms at 10⁵, 1,213 ms at 2×10⁵ (seed 1), 1,244 ms
(seed 2: structural, 1.03×)** against 12 ms; the monster frames sit in the wave, spaced 49–50 frames
(the player's item cadence), each carrying up to 24,467 events at ~49 µs inside one item; between
them the budgeted drain saturates at 11.9 ms / ~235 events and cannot catch up — it only reaches the
frame's 1.67 game-s tick, while `pull_ships(key, !in_root)` (`universe.rs:769`) resolves every ship
below the player's next item (~83 game-s of horizon under burn): **batch = wave density × the
player's item horizon, linear in N** (6,443 → 24,467 → the M1 record's 37,938 at 3×10⁵ ≈ 5 s a pull
at 10⁶). Control: same seed, same wave, coast — max 12.0 ms, zero frames over, 1.45 s of lag
recovered after the wave (the overload is real in both flights; the seam decides its shape). The
freeze does not ratchet (past the wave ≤ 1.2 ms sampled; bits held: refusals 0, dead 0). The M1's
45 ms at 10⁵ vs 315 ms here: the exact monster is schedule-conditional (where the item lands in
the wave), the phenomenon is not. *[checker 6138: one reading of two — at 5×10⁴ burn on this box
the wave passes with zero frames over budget (the only failures are the second seam, 1 event,
17-19 ms), so the onset N moves with the drain rate: machine-conditional as much as
schedule-conditional; and the batch model misses its drain term: at rtf 200 (2×10⁵ burn, same
seed) the monsters carry 30,301 events against 24,535 at rtf 100, the extra ≈ the halved drain's
25 frames × ~245 events — batch = wave demand in the item horizon − what the budget-cut drain
removed, and the first doubling (6,393 → 24,535, 3.8× for 2× N) is superlinear, so "linear in N"
holds for the demand term only.]* Named fix, in the engine's own idiom: the scan is already holdable off
the critical path (`universe.rs:1164`); hold it when the backlog it would read is over a threshold
and let the budgeted drain resolve it — certificate: `frame_digest` unchanged. Gate consequence: an
N rung flown 20 s certifies a window that excludes every belt body's first event; the rung must fly
past the wave (≥ 150 s) before F1 can certify scale. Domain: Linux shared box, one box, burn arms at
10⁵–2×10⁵ only (3×10⁵ quoted from the M1 record: it exceeds this box's 2 GB cap); a second milder
burn-only seam at frames 11,094+ (13–55 ms, event-thin, every ~50 frames) is unnamed.

**Break #3's scan half is decomposed: the player's scan walks its certificate's poison, not the
doll — a write-once speed cap and a global-count density rule (20261014-1511-components-a2c1).**
An env-gated census on the shipped `PlayerNeighbourhood::capture`/`Radial::candidates` (counters
only, digest-neutral; the ladder's own arms, 20 s flights): the unpoisoned certificate keeps
**15 + 2 bodies at every N** (the first call's window: bins 479–486 around the player), but one
hot kicked tube (a local on a periapsis-heavy ellipse) raises the doll's `speed_cap` 84×
(1.16e-4 → 9.76e-3, monotone: `note` only maxes and `rebuild` only maxes, so it never falls for
the process's life), and `scap·h` (h = the player's plan step, 1.1e12) becomes 96% of the window:
±9× the player's radius, hit 2,402 bin-entries, **walked 194 a call (flight average; late calls
203) at 10⁴–3×10⁵, 12× the
certificate's own keep set, kept 177** *[checker a2c1: 10⁶ untested — 3×10⁵ reproduced
identically (194/177, 711 MB); the claim's domain ends where the measurement does]*; the
hull-of-history registration widens entries 905 → 2,885 (~14 bins/body) as kicks land. At
**N=10³ the density rule fires on 183/193 calls and the fallback walks every body of every doll
(1,017 of 1,028)** — the rule compares a doll-local hit against `bodies/4` counted over all
dolls, so the misfire is N-dependent and inverted (adding belt bodies to other dolls
un-poisons doll 2) *[checker a2c1: the misfire domain is wider than the author's "N ≲ 2×10³" —
it fires at 2,000/3,000/5,000/9,000 and passes at 9,500; the crossover is bodies ≈ 4×(2,425−64)
≈ 9,444, so the 10⁴ arm sits ~5% above it — a 9,000-body universe walks everything, a
10,000-body one does not]*; capture then costs **more at 10³ than at 10⁵ per
call on this box (author 178 vs 129 µs; checker regen 110.8 vs 105.7 µs — direction holds, the
gap is inside shared-box noise)**, and the held answers (idle-time) scale the same
(1,428 vs 824 µs author; checker regen 1,299 vs 777 µs; standing ~10 KB a held scan ≈ 57 B a
kept candidate, held max 270 at 10⁴ burn / 191 at 10⁵ in regen — schedule-dependent, the
author's 1,020 not reproduced). The ladder break-3 "one item 14.6 ms" near the belt
*[checker: inferred, not observed — 3×10⁵ × 48 ns ≈ 14.4 ms fits the walk-all arithmetic, but
no root-doll scan was recorded in any arm (40 s burn included: the player's binding stays in
doll 2 past frame 948)]* is this walk-all at the M1's ~48 ns/body.
Named fixes, in cost order: `rebuild` resets-then-maxes the caps over the retained bindings
(one line); the density rule counts the doll's own membership and the fallback iterates the
doll's registered ids, not `0..total` (a few lines); the window's representation — each body's
bins widened by its **own** speed bound, not the doll-wide cap (slow bodies stay in 1–2 bins,
hot ones correctly spread). Burn arms: finer `h`, 79 walked/call, density never fires (P4 held);
**unmeasured**: the belt's registration state (no belt events in 20 s flights — its first kicks
are at 13,051 game-s), the player inside the belt (the case the density rule was written for),
and the found set per scan. PRINCIPLES #5: the scan reads its neighbourhood, not the doll.

**Break #2's "representation's lever" is measured: the compiled orbit is write-only memory for
the engine, exactly its key, and the view's ramp completion is its one real reader
(20261014-1221-components-0e37).** On the wave scene (N=100,028, 80 wall s at rtf 200, past the
first-kick wave): held tables 2.0/body (100,076 current + 100,491 retired); standing 1,806 B/body
of which 74.3% is derived knots (current shape 672, retired 670; rec+plan 464); law-mandated
floor 673 B/body — idiot index 2.68× accounted, ~4.6× on footprint (459 MiB = 4.59 KB/body;
+2.33 KB/body across the wave, ladder's 2.6→5.1 reproduced). Flight table-reads are **O(1) in
N** (107–191 decodes/frame at N=10⁵, the same as N=2×10³; 2.2M reads ≈ the wave's own kicks ×
~10–15, ≈6.9×10⁻⁴/held-table/game-s) and **the belt's retired tables are read 0 times in
flight** — read only in the burst at their own next kick *[checker 0e37, all-path counter: true
of the belt (fetch rate flat across the wave), but the fixed cast's retired bindings are fetched
~1.4/game-s by the player's encounter scan (`encounter.rs:180` — all 56,454 in-flight retired
fetches over 40,000 game-s; state_of 0) — deletion costs ~0.1–1 % CPU in recompiles, not zero,
or one kept exception for the cast]*. 1,001/1,001 sampled current
Cycle tables regenerate **exactly** from `Orbit::compile(key)` (knots, crossings, all three
channel increments): the cache holds nothing beyond the key. The one mass reader is the view's
gather: cold 4,238.7 ms, 10.71 decodes/row, and **309,227 rows completed through a retired
binding in two gathers** (≥1/row post-wave — `observe::partial`'s ramp decodes the previous tube
2–3× per mid-window row), which the **two-word (a, ȧ) completion** replaces (a-word's open
direction 1; the one-word form is gate-refuted, the two-word is second order at the handover by
construction). Design, priced: `Segment` drops `entry`, gains key (+56 B) + word (~24 B) →
deletes ~520 B/body accounted (~800 B/body footprint) at ≈zero flight CPU *[checker: ~0.1–1 %
above]*; the current generation
follows the same route once the Carlson kernel lands (2.9 µs/channel family, kick-jet de99) →
~750 B/body ≈ 1.1× the floor, moving the 4-GiB-at-10⁶ wall to ~2×10⁶ (free half) / ~4×10⁶ (with
kernel). Instrument digest-neutral: `frame_digest` identical pristine vs patched on every
flight. Domain: belt band (e ~0, ~7 knots), planar, headless flight (no per-frame gather),
Linux footprint; passages/plunges unsampled, high-e members are the same lever at 5–20× the
bytes (thinner tables, closed-form-kernel 5a3b), the gather's retired-read share is a post-wave
snapshot — the mid-window phase peak (≥2/row cold); at 40,000 game-s it is 0.02/row (checker),
the synchronized cadence's phase setting the share.

**The smallest promotion is no promotion: one belt event is a stack-local function on the compact
row, and the live bind is a regime change, not an event (20261014-0450-scout-b29a).** Composed from
shipped pub APIs (`Population::body`/`scar`, `Key::darwin`, `Orbit::compile`, readout,
`binding::cartesian`, `Rebinding::from_state`) on the lab belt band: ~38 µs p50 / ~78 µs p95 per
event and 12–40 B of standing state, against the wired sticky `resolve_handout`'s 486–585 µs and
8,257 B with no demotion (367f) — ~13× on CPU, ≥ 200× on bytes, zero standing body. The refit term
(`from_state`) is 21 µs p50 at belt keys; the **key-space arm** (integer ΔE/ΔL on the key's own
Q48/Q32 quanta) is 0.11 µs and stays at the kicked state's birth quantization floor at every
scale Δv/v ≤ 1e-1 (E 3.0 Q48 / L 7.6 Q32 quanta from the f64 invariants), with shape agreement
with the refit ≤ 1e-9 typical (tail 7.7e-8 at 65,536 — checker), impulse-independent — the r2
finding ("kicks are integers native to the law") made the cheapest exact arm, pending the
encounters tier delivering ΔE/ΔL as exact integers. At 10⁹ quiet the stream is 1.4 Linux cores
(refit arm) / 0.004 (key arm): the kick stops being the quiet-belt wall; encounter discovery stays
the cold rail's large term. The 8-byte scar's i16 grade ends near Δv/v ~ 1e-5 (92% Wide at 1e-4);
w/t column anchoring is a wiring decision (naive wiring forces Wide at 53%/47%; anchored in-order
deltas measure 12.07 B/event, checker). Domain: planar,
prograde, one belt band, Linux shared-cloud; not 3-D, not the GR doll, not the real contact-impulse
distribution. Checker: the 13× is cold-belt (σ0.07); at σ0.3/e≤0.9 the composed cost is ~76 µs
(6.4× under sticky); Δv/v=1 refuses 9–26% (the regime trigger observed); `Key::darwin` caps the
composed path at p ≤ 8192 M — belt bands beyond it (the store's `Spec` allows to 65536 M) need a
different row→key path.

**The 10⁹ ledger is composed, and the scoreboard's gaps resolve into two rails: the kick
gap is the hot rail's alone, and the cold rail is encounter-bound by ~1.9×10³ skin-on
(20261014-0059-fermi-effb).** The cadence law is now code-verified: `step_for` is one
step per 2⁻⁷ of the radial period, power-of-two rounded (`ctx.rs:44` `step_log2: 7`;
`step.rs:75-97`), so **rate = 2⁷/P with κ ∈ [128, 256] — a pure birth constant**; it
reproduces 3071's roster endpoints (top 0.0462 vs 0.0484, ratio 0.96 — 4.7% *above*
the κ=256 ceiling, so band-edge-tight; floor 3×10⁻⁵, which the hauler band cannot
reach — its κ<256 top at 0.5 AU is 2.29×10⁻⁵ — while Cinder's band [1.7, 3.3]×10⁻⁵
contains it at κ≈231 — **no period-independent clock floor** on either reading;
checker: the floor body's identity is unverified), contains 7497's Orbiters
(202–223 ⊂ [128, 256]), and validates the SI unit reading (root unit 1.477 km, c = 1,
game-second = second). Composed at 10⁹ quiet (rtf 1, 4 cores): kicks 0.12–1.065 cores
at Carlson (code-derived 1–2 AU belt 0.043–0.243, a9d7 rate 1.065; checker: at the
shipped 231 µs the true 1–2 AU band is 0.33–1.87 — the ledger's 0.94 is the κ=128@1 AU
edge — and a 0.5 AU belt runs up to 5.3 cores at 231 µs; Carlson busts 4 cores only
inside ~0.16 AU)
— 8.2 only at the a9d7 rate × 231 µs (367f's 8.3 and ad26's 1.08 re-derived
independently; both stand, the spread is the period mix: the record's per-body rate
constants span ~100× by instrument — roster mean 3.3×10⁻³, a9d7 3.55×10⁻⁵, haulers
1.8×10⁻⁷–2.3×10⁻⁵); **encounters 7.7×10³ cores skin-on (1,925× over; 9.66×10⁴
no-skin), 7,051× the kick term at Carlson pricing**; memory 2.6–5 GB quiet (fits),
15.75 driven (the quanta); hot 90–186 MB; H_live ~0; frame tier deleted (gate open).
Rails: hot (battle density 0.041/member/s) measured ceiling 2.8×10⁴ at the stack
(790b), model-scaled to ~4–6×10⁸ at the 42–55 ns floor (the ledger's own 4.9×10⁸;
checker-corrected from ~10⁷–10⁸) — the kick gap (10^3.3) buys
this rail, 4+ of the bodies gap's 6.4 orders; cold (belt) never kick-bound, encounter-
and memory-bound. **Expected break order as the plane grows: promotion stream ~10³
(367f) → hot D-slope 2.8×10⁴ (790b) → the wired encounter tier at ~5.2×10⁵ bodies
skin-on (~4.1×10⁴ no-skin; held-out, falsifiable when H0216 wires it) → memory at 10⁹
(quiet: never; driven: the quanta).** The cold rail's entire CPU bill is chosen at
generation: when shipmem's belt is wired, pick its `step_log2` knowing rate =
2^step_log2/P is the whole bill.

**The rule-2 conflict is resolved by decomposition: the tail is manufactured, and the
promotion certificate is arithmetic on stored birth constants (20261014-0000-fermi-3071,
adjudicating 20261013-2252-dynamics-ea91 against
20261013-2252-second-20261013-2130-library-ae3d-7497).** ea91's ho1 scene reproduces
bit-identically (digest `aca905ad…`). The plane's 28 natives carry compiled rates
0.0484 → 3×10⁻⁵/s (1,613:1 by construction — now derived from the cadence law above):
same-rate bodies have identical census counts (133,133 / 67,67,67 / 17,17 at T = 5,500
game-s), counts are identical across seeds 3/7/11 and member counts 48/120/400, and
exactly 2× under a doubled window (kicks 266 = 2·133 exactly; 133 = 2·67−1, 33 =
2·17−1). Roster-predicted native Gini 0.759 vs measured 0.718–0.745 (ρ = 0.94–0.96);
the model "natives = rate×T, members = measured" reproduces G_all within 0.017 (worst
case, tune) and even the Zipf slope (−1.6…−2.0). Held-out: seed 11 m120 held 5/5; the
doubled window held the ladder exactly (2× per ladder body; the roster Gini is
T-invariant by construction) while the player proved schedule-bound (350 ≠ 2×417) and
G_all *rose* (0.753) as dead members' one-time bursts froze against ∝T ladder bodies —
both misses in the driver/member channels no rank reads. So: **rule 2 is dead as a
ladder rule** (7497's verdict, now decomposed); **every ea91 measurement stands** as a
correct description of a manufactured distribution; the live fraction is set at
generation (12 of 28 natives above 3×10⁻³/s here), and the promotion cost question
stays at frame-cost's `resolve_handout`.

**The surprise-rate distribution as measured (ea91, instrument = the env-gated
per-body census in `Universe::apply`, digest-neutral):** across bodies, resolved items
have Gini 0.72–0.74, top-decile 47–56 %, Zipf −1.6…−2.0, busiest ~100× median; ranks are
regime-frozen among the living (natives ρ = 0.98–1.0; promoted ρ = 0.85–0.93 at 55 s
windows, at the Poisson null, below it at 30 s) — the regime is now explained: it is
the compiled period ladder. The churn channel is **death**: 47–64 % of promotions crash
within one run window, each after a birth burst, then 1–3 items per half-run of
quiescence; the steady stream avalanches (Fano 8–28, top 1 % of frames carry 10–26 % of
items, zero-frames 0–86 % by scene, lag-1 |ρ| ≤ 0.17). Domain: the plane's battle
scenes, m48–m400, windows 30–55 s at rtf 100 (the bench clamps `--members` to [4, 400]
and `--seconds` to ≤ 55); not the quiet belt, not below half-run scale.

**The kick census as measured (7497, instrument = `Update.kick` + `kick_log`,
digest-neutral):** the tube bulk is flat per orbit by construction (CV 0.17–0.20,
max/median 1.4–1.5, Gini ≤ 0.12; Orbiters 202–223/orbit across scenes and seeds); the
per-second spread is three decades (4.8×10⁻² → 3×10⁻⁵) but it is structure — rank per
second = rank in 1/P_orbit plus the clock's regime, knowable from body constants at
birth. The head is driver-caused: a held L12 burn puts 70.6 % of kicks on the player;
the 4,000-member battle spreads over 3,769 promoted members (p50 5, mean 20.6, max 174,
top member 0.07 %) — dispersed, headless, discovered by due-ness.

**The store's update path is population-independent by construction (events touch one
shard, sharded at 2²⁰ members) and its spikes live in compaction steps, not the append —
measured on shipped code (20261013-2130-library-ae3d; checker-corrected; store rows
re-regenerated by the 7497 run: 12.347 bits/member at 7 ns, storm 48.38 with graceful
fallback, convoy hot max 10.9 µs vs a 1.29 ms compaction step).**

The four rules that survive, with rule 2 struck and adjudicated:
1. **Delete before you measure cheaper, and to the quota** (Musk's algorithm + his 10% rule,
   library-7f99): every ladder term gets a *deleted* rung before a *cheaper* rung, and ~10% of
   deleted terms must come back — else the deletion was too timid. Audit 7f99: law level 8–19%
   (at quota), frame path 0% (backlog unfired: the caps, the density rule, the hull, the sticky
   promotion, `entry`).
2. ~~**The live set is a rank, not a count**~~ — **dead by measurement and by
   decomposition** (7497, adjudicated 3071): the distribution's bulk is flat per orbit
   by construction, its native concentration is the compiled period ladder (a birth
   constant), its head is driver-caused, and its churn is death. The live-set bar is a
   period/clock-regime threshold knowable at generation; falsify further on belt scenes
   (conjunction clustering), not the plane.
3. **Promotion judges on event time, not frame time** (sampling noise): the judged form is a
   **filter, not machinery** (library-7f99): the refit's refusal is the promote-to-live trigger
   (b29a: 9–26% refusal at Δv/v ≈ 1) — no hysteresis windows, no rank state. *[At the half-run
   scale live ranks sit at the counting-noise null (ea91). Held-out: the 210-handoff chatter
   vanishes if those handoffs never refuse the refit.]*
4. **Buy the option, not the headroom** (optionality): no ahead-of-demand promotion;
   the promotion to make cheap is the *ephemeral* one (demote at commit, frame-cost),
   and the repack/compaction step (1.29–12.1 ms) is the scheduled spike.
5. **One mechanism at every scale** (Waitzkin): a rung that needs a special case for
   the head of the distribution fails the rung, whatever its numbers.
6. **Automation last** (Musk, via library-7f99): the allocator lands after the frame-path
   deletions; a guard or fallback that exists to manage undeleted shared state (the 6 anchored
   sites) is a deletion marker, not a scheduling input.
7. **Shared state pays sensor cost** (Karpathy, via library-7f99): a doll-wide or singleton cache
   is priced procure + maintain + incorporate (the monotone cap, the window widening) — delete it
   for one exact per-body instrument rather than repair it (a2c1's fix order inverts).

## Refuted

- "Memory grows with play across the belt's waves" (the inversion kill attempt on break 2): rss +0.7% over waves 2-5 at 3x10^5 and +8/2,000 game-s-equivalent at 2x10^5 to 250k game-s; catalogue constant; one retired binding per body; no backlog survives a wave (20261014-2248-inversion-4af4).
- Same kill attempt, longer axes: +0.9% over 25 wave periods (700 k game-s) at 2x10^5 and +13 MB at wave 2 of 4.2x10^5 (1.9 GB); and "the sharp train persists into long play" — the last window above 10x the median is wave 5, the floor rising to the belt-rate equilibrium with no term moving (20261015-0128-second-20261014-2248-inversion-4af4-7dc6).

- The library lens's "the walk lands at the keep set (~17)" (7f99's lesson-3 headline): 17 is the pre-kick
  transient (seq 1; the old early window already walked 31-40 by seq 2); the sustained need at 10^3 is ~49 kept
  / 66 walked - measured on the digest-identical deletion (5903). "The shipped chatter case" is not shipped
  either: it lives on 18d2's lead branch (5903 re-emitted the probe; 193 handoffs/20 periods, the checker's 210
  same phenomenon).
- "Hold the scan" read as holding the whole scan (capture at answer time): digest-refuted — the late capture
  reads pruned history (4,029 ≠ 4,060 encounters, digest differs); only the answer is holdable, and the capture
  must stay at the player's item, where the bindings at its tick are final (20261014-1719-dynamics-bf21).
- "The first kicks arrive as one smooth wave" (the one-shock reading of 6138's measurement): the arrivals are a
  standing train — the cohort recurs one step (~27.5 k game-s) later with its shape, width growing only 1.1 k →
  3.0 k game-s per pass; and the steps are a continuum, not the single power of two the pow2-rounding reading
  predicted (same run).
- "The wave is the drain's problem": the drain holds the coast at 12.0 ms through the same wave
  (0 frames over, 1.45 s lag); the freeze is the player's item alone (`pull_ships` at the root doll)
  (20261014-1631-taleb-6138).
- "The scan's walk is O(N) at ladder scale" (the reading of the ladder's before-fix capture
  profile, 45–50 ns a body, carried into break 3's wording): at 10⁴–3×10⁵ the walk is
  doll-scoped, 194 bodies a call (79 on the burn arms) — the O(N) reading holds only where the
  density rule fires, which by measurement is N ≲ ~9.4×10³ on these arms (checker: fires at
  9,000, passes at 9,500; the author's first reading was 2×10³), and there it walks every
  body of every doll (1,017 of 1,028 at 10³; 8,604 of 9,028 at 9,000) (20261014-1511-components-a2c1).
- "The density rule protects the walk": it inverts — its threshold (`bodies/4`, counted over all
  dolls) grows with populations the window never touches, so the same poisoned window passes at
  10⁴⁺ and fails at 10³, where the fallback (`0..total`, a `binding_at` a body) costs more than
  the 10⁵ scan it was meant to save (author 178 vs 129 µs/call; checker regen 110.8 vs 105.7 —
  direction only, the gap is inside shared-box noise) (same run).

- "The retired compiled orbit is needed by the engine between kicks" (the assumption under
  ladder break #2's memory wall): flight reads of held tables are O(1) in N and the *belt's*
  retired tables are read exactly 0 times in a headless flight past the wave *[checker: the
  cast's are fetched ~1.4/game-s by the player's scan — 56,454 over 40,000 game-s, all at
  `encounter.rs:180`; ~0.1–1 % CPU to recompile]*; the knots are a pure cache of the
  `OrbitKey` (1,001/1,001 sampled regen; checker: every current and retired table, knot-for-knot,
  300,520/300,520) (20261014-1221-components-0e37).
- "Deleting the retired generation is free at today's view": post-wave, the gather completes
  ≥1 row in 1 through the previous binding (309,227 completions in two gathers of 100,048 rows,
  10.71 decodes/row) — the deletion needs the two-word completion (a, ȧ), not just a key
  (same run; the one-word form already gate-refuted by a-word's f2b7).

- "Cost follows events, not bodies" as a measured update-path scaling law: the timed
  path is one shard by construction, and 6→7 ns is inside the 6–9 ns repeat noise
  (20261013-2130-library-ae3d, checker).
- "The repack is the allocator's enemy": population-specific — `battle`'s worst
  compaction step is 12.1 ms at 0 repacks (20261013-2130-library-ae3d, checker). The
  general rule is the compaction step, not the repack.
- **"The live set is a rank, not a count" (rule 2): dead by its own named falsifier and
  by decomposition** — the per-body distribution on shipped plane scenes is not an
  intrinsic surprise tail (bulk flat per orbit; native concentration = compiled period
  ladder, identical across seeds and exactly T-scaling; head driver-caused; churn is
  death) (20261013-2252-second-…-7497; adjudicated 20261014-0000-fermi-3071).
- "The live set chatters rank-to-rank and needs hysteresis at the half-run scale": ranks
  among live bodies are at the Poisson re-noise null; the churn is death
  (20261013-2252-dynamics-ea91).
- "Most promoted bodies go dormant (zero events in the second half)": true only of the
  dead; among live promotions 0–9 % are dormant in a half-run (20261013-2252-dynamics-ea91).
**The wave's freeze is deleted, and the fix is certified bit-exact where the cut is canonical
(20261014-1719-second-20261014-1631-taleb-6138-4487; the checker's named gold experiment, built and
flown).** The named fix in the engine's own idiom: the player's in-root item pulls at most `PULL_HOLD
= 64` ship items; over that the rest goes to a drain inside `advance` (the ships below the oldest held
key, in the pull's own key order, one item a pass behind the same `spent_before` gate as any other
item), and the scan that needed the pull is held as a `Waiting` entry that captures only once the ship
lane is clear of its key (answered FIFO, folded into the digest like any held scan; the children-only
pull is untouched). Measured, 200 s flights at rtf 100, budget 12 ms, this Linux box: worst frame
**315→37.7 ms at 10⁵, 1,213→90.3 ms at 2×10⁵ (seed 1; seed 2 1,244→81.4), 1,280 (M1 record)→123.8 ms
at 3×10⁵** (peak 1,705 MB, inside the box's 2 GB cap); events/frame max 24,467→**333**; the wave region
itself now runs at **11.94 ms worst** (the budgeted drain saturated, exactly the coast control's shape),
the overload appearing as 1.67 s of recovered lag instead of 1.2 s freezes. Certificates:
`frame_digest` (8 scripted flights × 4 schedules) identical pristine vs fixed vs every-pull-forced
(`set_pull_hold(0)`, a doc-hidden control); belt flights bit-identical at the post-wave canonical cut
(21,000 game-s, deterministic 25-events budget: digest `ae06c773…`, kicks/events/encounters equal to
the digit), at all three cuts at N=2,000, and both cuts on the coast control. *[checker 4487: seed 3
and every-pull-held (`NLADDER_HOLD=0`) reproduce the post-drain identity (hold 0 matches at both
cuts); the 3×10⁵ arm is a quiet-box number — under a loaded box its worst frame inflates ~4× on
0-event frames while evmax stays 333.]* *[checker2 4487, from the patch on a clean tree: 3×10⁵ under
the deterministic budget joins the identity — pristine 2,615 ms worst / 52,846 events in a frame vs
fixed 12.0 ms / 218, digest `d4f4441e…` equal to the digit; seed 7 and `NLADDER_HOLD=1` (minimum
slice) also match at 21,000 game-s — and at seed 7 the resolved-events counter sits 6,116 apart at the
identical digest, so the counter is pace-dependent and the digest is the certificate.]* Two findings bound the
claim: (a) a **mid-drain cut is not canonical** — at 16,000 game-s the fixed engine holds 11,473 fewer
resolved events (the drain's unfinished share) and the digest differs; (b) the instrument itself — a
wall-budgeted 2×10⁵ belt flight — **is not schedule-stable on shipped main** (two pristine runs differ
at both cuts: `f6869cbb…`/`02570fef…`), so belt digests compare only under a deterministic budget.
Residual: the worst frames are now the unnamed **second seam** (1 event each, every ~50 frames, burn
only: 37.7/90.3/123.8 ms at 1/2/3×10⁵ — it grows with N and now binds F1; the fix does not touch it).

**The wave's freeze is the player's doll, measured on shipped main (20261014-1631-taleb-6138).** Every
belt body is born at tick 0 with one Δs, so the first kicks arrive as one smooth wave at 13,037–14,542
game-s; the player in the root doll resolves the whole backlog inside one unbudgeted item
(`pull_ships` at `universe.rs:769`), worst 315/1,213/1,244 ms, while the coast control holds 12.0 ms
through the same wave. *[checker 6138: the onset N is drain-rate conditional (5×10⁴ passes clean
here); the batch has a drain term — batch = wave demand in the item horizon − what the budget-cut
drain removed.]*

**The deletion program gets its method, priced from Julien's library mined verbatim for the first
time (20261014-1631-library-7f99; 762 highlighted books, 4,580 highlights cached in the run).**
A grep-backed audit of the engine's own record: 26 kills, 5 revival-shaped events (8–19%): the law
level brackets Musk's 10% add-back quota, the shipped frame path holds 0 add-backs and its unfired
backlog is exactly the named terms (a2c1's two sensors, b29a's sticky promotion, 0e37's `entry`
field); promotion collapses to a filter; automation last. *[Checker 7f99: one landed scoped
restoration missed (r9 killed kick-avg, `docs/law.md` keeps kicks orbit-averaged) — a sixth
revival-shaped event; the frame-path 0 and the ordering survive.]*

**Break #3's scan half is decomposed (20261014-1511-components-a2c1): the player's scan walks its
certificate's poison, not the doll** — a monotone `speed_cap` (84×) and an inverted density rule
(`bodies/4` over all dolls, misfiring at N ≲ 9.4×10³) put 194 walked entries a call against the
certificate's keep 15+2; named fixes in cost order: reset-then-max the caps, doll-local density,
per-body window widths.

**Break #2's lever is measured (20261014-1221-components-0e37): the compiled orbit is write-only
memory for the engine, exactly its key** — flight reads O(1) in N, the belt's retired tables read 0
times in flight, 1,001/1,001 sampled tables regenerate exactly from `Orbit::compile(key)`; the
deletion is priced (~520 B/body) pending the two-word (a, ȧ) ramp completion.

**The smallest promotion is no promotion (20261014-0450-scout-b29a): one belt event is a stack-local
function on the compact row** (~38 µs p50, 12–40 B standing) against the wired sticky resolve's
486–585 µs and 8,257 B; the key-space arm (integer ΔE/ΔL on the key's own quanta) is 0.11 µs.

**The 10⁹ ledger is composed (20261014-0059-fermi-effb): the kick gap is the hot rail's alone, the
cold rail is encounter-bound by ~1.9×10³ skin-on**; the cadence law is code-verified (`step_for` is
one step per 2⁻⁷ of the radial period: rate = 2⁷/P, a birth constant).

**The rule-2 conflict is resolved by decomposition (20261014-0000-fermi-3071): the tail is
manufactured, the live fraction is set at generation**; the surprise-rate distribution's regime is
the compiled period ladder, its head is driver-caused, its churn is death.

(The longer standing blocks — the store's update path, the four surviving rules with rule 2 struck,
the kick census, the surprise-rate distribution — are unchanged below this point on the page.)


- "The wave is the drain's problem": the drain holds the coast at 12.0 ms through the same wave; the
  freeze is the player's item alone (20261014-1631-taleb-6138).
- "The unbudgeted pull is the price of the scan's bit-exactness": the held pull — a 64-item slice,
  a budgeted key-ordered drain, and a scan that captures once the lane clears — is bit-identical on
  every scripted flight and at every canonical cut past the drain; the freeze it deletes was not
  buying the bits (20261014-1719-second-20261014-1631-taleb-6138-4487).
- "A belt flight's digest at a cut is a canonical comparison": two pristine 2×10⁵ wall-budgeted
  flights of shipped main differ at both cuts tested (16,000 and 21,000 game-s); only a deterministic
  budget (events, no wall) makes the comparison exact — and under it the engines agree bit for bit
  past the drain (same run).
- "The scan's walk is O(N) at ladder scale" / "the density rule protects the walk": the walk is
  doll-scoped (194 a call) and the rule inverts (20261014-1511-components-a2c1).
- "The retired compiled orbit is needed by the engine between kicks" / "deleting it is free at
  today's view": read-0 in flight but the view's ramp completes through it — the two-word completion
  is the prerequisite (20261014-1221-components-0e37).

- "effb's cadence law `rate = 2⁷/P with κ ∈ [128, 256]` — a pure birth constant, the cold rail's whole bill" (and the checker's 0.5-AU/5.3-core composition): right only inside secondary dolls; the root-doll belt runs on the doll's clock — measured 3.553×10⁻⁵/s flat in a, 24× the own-period law at p50; the dial's anchor is P_D (77.24 d), not P_own (20261014-1719-fermi-cf45).
- "A player decision inside a same-doll wave is an unbudgeted backlog drain" (the checker-2-bf21
  exposure, read as a cost): the drain never manifests — ≤ 0.229 ms a call at 2×10⁵ mid-wave, every
  frame through the wave, max frame 12.5 ms, and (checker) 0.154–0.158 ms **with the cap unset** at
  rtf 100 and 200: the scheduled pulls keep the ship lane tiled to the player's key, so `input`
  finds ≤ 2 due items regardless; what a no-op decision can still move is the log, not the kicks
  (+1 to +2 encounters per 657 decisions, pace-dependent) (20261014-2012-components-38bf).
- ladder.txt's "period of Cinder … 88 days": the root doll's shortest secondary is 77.24 d (same run).

## Open directions

0. **The key-changing decision mid-wave** (38bf's untested arm): a turn under burn re-plans the
   player (the no-op arm never re-derived the plan); one flight with `word(5,8)` at the wave's p50
   against the no-op control, judged on the frame profile and the counters. With it, the wave seam's
   player-facing story is closed and the cap can be adopted without an input caveat.
   *[Checker 38bf: flown — 0.201 ms at 2×10⁵ (encounters −3, kicks equal, max frame 12.48 ms), and
   657 key-changing decisions every frame of the window at 3×10⁵ hold max frame 11.97 ms (0.26 ms a
   call): answered affirmatively on this scene; the player inside the belt band and a busy box stay
   open.]*
0. **The capped pull is measured and certified** (bf21, above): adopt the constant (the env gate comes out;
   any small bound works — the cap only bites when the queue is behind, which is the wave), then re-fly the N rung
   past a *whole wave train period* (≥ 27.5 k game-s, not just past the first wave) so F1's window contains a
   wave; at 10⁶ the frame holds but real time does not (~34 s of lag per pass on this box) — the generation-side
   stagger (birth grid over one step, ~24× flatter) is the measured-next lever, a `shipmem` wiring decision
   (effb's direction 9). The event-thin 13–55 ms seam at frames 11,094+ under burn stays unnamed and open.
1. **The break-#2 build (the lever is now measured):** `Segment` drops `entry`, gains the key
   (+56 B) and the two-word (a, ȧ) completion (~24 B; a-word's open direction 1 is its missing
   half — the write needs the field's derivative at the kick); `observe::partial`'s ramp reads

   the word instead of decoding the previous tube; `binding_at` recompiles on the rare
   non-window read. Deletes ~520 B/body accounted (~800 B/body footprint) at zero flight CPU;
   with the Carlson kernel (kick-jet de99) the current generation deletes too (~750 B/body,
   ~1.1× the floor). The gather's retired-read census then re-runs as the acceptance check.
1. **Wire the belt's events through the scar batch, not `resolve_handout`** (b29a): the composed
   path deletes the sticky promotion entirely; the contract to settle at wiring is the tier → law
   kick interface (exact integer ΔE/ΔL in the key's quanta vs state-space impulse at 21 µs) and
   the w/t column anchoring. The refit's *refusal* is the true promote-to-live trigger.
2. **The deleted rungs** (rule 1): per term, what does the frame loop look like with the
   term gone; count what the per-frame walk visits that the hot tier did not touch.
3. **Event-time hysteresis on the chatter case** (rule 3): retrograde 0.49 R_H,
   boundary evaluated at the doll's events; expect handoffs per 20 periods to collapse.
   *[5903: the promote-on-refusal variant is measured on 18d2's branch - chatter 193 -> 0 with 0 refusals at
   every would-be handoff, but 3.9-8.8x events on the body (the child doll never engages): the refusal gate is
   a kill-switch, not a surface; the hysteresis question stands.]*
4. **Compaction as the scheduled spike** (measured): fold the storm row's update stream
   into the shipped allocator and check the p99 frame. Primary direction for the
   promotion work (rule 2's death redirects it here and to ephemeral promotion).
5. **The wired encounter wall** (effb's held-out number): when H0216 wires the encounters
   tier into the plane, the first CPU wall lands at ~5.2×10⁵ belt bodies skin-on
   (~4.1×10⁴ no-skin) — measure it there; the further ~1.9×10³ cut (cells, setup, what
   never needs a pair test) is the cold rail's 10⁹ lever, ahead of any kick-cost work.
   *[0e37: once wired, re-run the read census — the tier is the one consumer that could
   read belt tables between kicks; today's flight has none.]*
6. **The belt revival path** (both runs and the adjudication point here): a dense belt
   where conjunctions cluster on bodies could still be heavy-tailed *without* a driver —
   unmeasured; it is the one scene class that could revive a measured rank.
7. **The death channel at belt scale** (ea91): the 47–64 % promotion death rate is the
   battle pocket; measure the quiet belt's promotion mix (death vs dormancy) before
   sizing retirement vs demotion. The avalanche stream (Fano 8–28) is the allocator's
   target for burst absorption (PRINCIPLES #12).
   *[7f99: automation last — this direction and any allocator build fire after directions 0–2's
   deletions land; the quota expects ~10% back, the cast exception the candidate.]*
8. The haulers' far-field clock cadence per orbit is extrapolated from ~1 kick
   (0.03–0.3 % of an orbit measured); a full-orbit measurement needs ~10⁷–10⁸ game-s
   (wall-days) — only worth it if the ladder reaches the root-doll bulk. *[effb: the
   cadence law rate = 2⁷/P now explains why the haulers sit at ~1 kick per *measured
   window* without any separate far-field clock: their κ/P is simply small; no extra
   law is needed.]*
9. **Pick the belt's `step_log2` as a budget decision** (effb): the cold rail's whole
   CPU bill is 2^step_log2/P summed over the period mix; the billion's event load is a
   content policy, not an engine property — set it when wiring shipmem, with the
   encounter term (not the kick) as the binding constraint it must leave room for.
10. **The second seam now binds F1** (the fix removed the wave's monsters): 1-event frames at
   37.7/90.3/123.8 ms for 10⁵/2×10⁵/3×10⁵ burn, every ~50 frames (the player's item cadence), burn
   only — and from 5×10⁴ up (19–22 ms there, both engines, the same frames: it predates the fix;
   checker 4487) — the player's own item cost under burn (a2c1's walk-all and cap candidates name
   the suspects); unnamed, cheaper to diagnose than the pull was.
11. **The mid-drain cut** (16,000 game-s): the fixed engine's digest differs there by exactly the
   drain's unfinished share (11,473 events at 2×10⁵) — a cut is canonical for the held pull only
   once no held key remains below it; the rung writer's cut choice must respect that (or the settle
   must drain before the digest, which it does — the residual is the *flight's* pace, not the
   settle's).
12. The wall-schedule instability of the belt digest on shipped main (two pristine runs differ):
   worth its own run — it breaks the "digest independent of schedule" contract at 2×10⁵ belt scale
   even without any fix; the deterministic-budget mode (`NLADDER_EBUDGET`) is the instrument until
   it is understood. *[4af4: closed — the digest is schedule-independent; the CUT was not: a
   presented-time cut is wall-quantized by the budget (±1 tick, ±5 kicks at 3×10⁵), and the
   canonical `frame_to(limit)`+`settle(limit)` cut reproduces bit for bit; freeze cuts at
   absolute ticks (20261014-2248-inversion-4af4).]*
13. The standing directions from a2c1 (the caps, the density rule, the per-body window), 0e37 (the
   two-word completion), b29a (the filter promotion), and the ladder's 10⁶ arm.

## Contradictions

- None open on this topic. (The main/taleb-6138 page conflict was two concurrent current-bests; both
  blocks are kept above, the newer first.)

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author): rule 2's falsifier run on four shipped scenes — distribution not heavy-tailed (bulk flat per orbit by construction, head driver-caused); promotion is a fixed fraction; digest-neutral probe.
- 20261014-0000-fermi-3071 (awaiting grade): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window, roster-predicted Gini 0.759 vs measured 0.718–0.745; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (awaiting grade): the 10⁹ ledger composed — cadence law rate = 2⁷/P code-verified (roster endpoints 0.96/0.76, Orbiters ⊂ [128,256]); encounters 1,925× over skin-on, 7,051× the kicks; two rails (hot = kick gap, cold = encounters + memory); held-out: wired wall ~5.2×10⁵.
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured — ~34–38 µs/12–40 B ephemeral vs 486 µs/8,257 B sticky; key-space kick 0.11 µs at the birth floor; checker: cold-belt 13×, 6.4× at σ0.3, darwin domain p ≤ 8192 M.
- 20261014-1221-components-0e37 (this run, awaiting grade): break #2's lever measured — compiled orbits are write-only in flight (retired: 0 reads; flight reads O(1) in N), exactly the key (1,001/1,001 regen), floor 673 vs standing 1,806 B/body; the view's ramp is the one reader (≥1 retired read/row post-wave) — the two-word completion deletes the retired generation free.
- 20261014-1511-components-a2c1 (this run, awaiting grade): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-library-7f99 (this run, awaiting grade): the library mined verbatim (4,580 highlights cached); deletion audit 26 kills / 2 landed add-backs (8%; law level at quota, frame path 0%); automation debt 6 anchored sites; promotion = refusal filter; lookup budget 427–877 recompiles/frame vs demand ≤ 1.4/s.
- 20261014-1631-taleb-6138 (this run, awaiting grade): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10⁵/2×10⁵ burn (seed-stable), the batch = wave density × the player's item horizon at universe.rs:769, coast 12.0 ms through the same wave; fix named (hold the scan), rung must fly past the wave.
- 20261014-1719-dynamics-bf21 (this run, awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical; holding the whole scan is digest-refuted.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); effb's rate law corrected 24x at the plane's belt (its 1-2 AU core numbers move little; the anchor does not); shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the checker's named gold
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at
- 20261014-1631-library-7f99 (gold): the deletion program's method — 26 kills, the 10% add-back
- 20261014-1511-components-a2c1 (silver): break 3's scan half decomposed — the cap's monotone walk
- 20261014-1221-components-0e37 (silver): break 2's lever — the compiled orbit is write-only memory,
- 20261014-0450-scout-b29a (silver): the smallest promotion is no promotion.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed; the cadence law code-verified.
- 20261014-0000-fermi-3071 (silver): rule 2 dead by decomposition; the tail manufactured.
- 20261014-0000-fermi-3071 (silver): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window, roster-predicted Gini 0.759 vs measured 0.718–0.745; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed — cadence law rate = 2⁷/P code-verified (roster endpoints 0.96/0.76, Orbiters ⊂ [128,256]); encounters 1,925× over skin-on, 7,051× the kicks; two rails (hot = kick gap, cold = encounters + memory); held-out: wired wall ~5.2×10⁵.
- 20261014-1221-components-0e37 (silver): break #2's lever measured — compiled orbits are write-only in flight (retired: 0 reads; flight reads O(1) in N), exactly the key (1,001/1,001 regen), floor 673 vs standing 1,806 B/body; the view's ramp is the one reader (≥1 retired read/row post-wave) — the two-word completion deletes the retired generation free.
- 20261014-1511-components-a2c1 (silver): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than at 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-library-7f99 (gold): the library mined verbatim (4,580 highlights cached); deletion audit 26 kills / 2 landed add-backs (8%; law level at quota, frame path 0%); automation debt 6 anchored sites; promotion = refusal filter; lookup budget 427–877 recompiles/frame vs demand ≤ 1.4/s.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10⁵/2×10⁵ burn (seed-stable), the batch = wave density × the player's item horizon at universe.rs:769, coast 12.0 ms through the same wave; fix named (hold the scan), rung must fly past the wave.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, 1,280→123.8 at 3×10⁵; bit-exact at every canonical cut past the drain; the mid-drain cut and the belt digest's wall-schedule instability named.
- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical, +1 to +2 encounters per 657 no-op decisions (checker: 0.15–0.16 ms even uncapped; silver).
- 20261014-2012-second-20261014-1631-library-7f99-5903: sensors deleted digest-identical (10^3 walk 15x); horizon not belt-scale; chatter 193 -> 0 under refusal at 3.9x events.
- 20261014-2012-system-a669 (silver): key quantum vs per-kick dL — breaks 1/2/4 one dial; flip-gated rebind.
- 20261014-2130-quant-d7e3 (this run, awaiting grade): in-band wave exposure measured — OOM at
- 20261014-2130-second-20261014-2012-system-a669-eb2d: flip-gated rebind wired, default-neutral; the dial's run caps at 4 — 10^2x refuted, mint counted 1.00/kick.
- 20261014-2130-taleb-625b (silver): the player in the belt band: in-band burn = memory ruin (11.2 GB, killed); scan 214-1,087x; coast monster 2 s.
- 20261014-2248-fermi-b30b (awaiting grade): the steady state through waves measured — memory plateaus 4.85-5.06 kB/body (slope <= 5 B/wave; churn killed 3 orders), rate 3.33-3.50e-5 confirmed end-to-end, train ~27-28 k game-s; memory binds the flyable N at every point.
- 20261014-2248-inversion-4af4 (this run, awaiting grade): the wave train flown — memory a step not a staircase, the train shears, and the digest wobble is the presented-time cut.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (second author, awaiting grade): the site is counted — candidates vectors 29.4 MB/mint, drain frozen after one answer; transit linear, ruin band [1.7,3.0] AU.
- 20261015-0128-second-20261014-2248-inversion-4af4-7dc6 (this run, awaiting grade): the checker's named in-box experiments done — 25 wave periods flat (700 k game-s, digest-stable), dissolution measured (floor rises to the belt-rate equilibrium), 4.2x10^5 at the box ceiling, 4af4's record made to regenerate.
