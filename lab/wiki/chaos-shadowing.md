topic: chaos-shadowing
status: open
closed-by:
valid-while:
updated: 20261019-0435-dynamics-e56b

# Chaos, the shadowing clause, and trapping statistics under quantization

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
as pre-registered, P3's alternative branch, P5 held; unflown: gravity-held belts, the
plateau's slow decay constant, per-body two-temperature decomposition).**
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
geometry).

[Checker, adversarial — every probe confirms, and the threshold is sharper (evidence in
the run's check.md; checker flights in /tmp, digests recorded there): five arms rerun
digest-identical (aligned seed-freeness included); n = 25600 (next octave, 4x the grid's
largest) still trains with the same constants (maxc/n 0.499, conc 21.5, period 2496 ch =
3.65*extent, F64_late 28300, amplitude 1.002) and reads one-shot 3.43x at sigma = q/256
with a flat late tail (windows 0.93-1.08x, no second burst); n = 1600 aligned at H 16384
(25 crossings, 4x the horizon) holds amplitude 1.0019 — constant as far as flown; the
transverse ladder sigma_y = 2048/1024/512/256/64/16/1 ALL read one-shot, so the train
dies at ONE velocity quantum: the kill condition is exact transverse-velocity equality,
binary, and the dossier's q/256 was a tested sufficient point, not the boundary
(rng.range is inclusive, so sigma_y = 1 puts real +-1 quanta on ~2/3 of bodies). Corrugation
fixed: comb teeth every 8 ch at every n. Ops numbers reproduce exactly (mean burst-window
2.085M vs quiet 1.592M = 1.31x; worst burst window 2.254M = 1.42x quiet median — the
walk-dominated conclusion holds). Unflown, as the dossier says: mixed fleet+thermal, the
wall-reflection train, free space.]
[Checker2, adversarial — every probe confirms, and the regime boundary is now flown
from three more directions (flights in /tmp/adv, digests in check2.md): clean-tree
rebuild of patch.diff gives digest-identical tsvs on three arms; sigma_y = 1 quantum
kills (one-shot, F64_late 0.9-1.1, maxW 3.2x); teeth every 8 ch confirmed at n =
400/1600/6400; the ops pair reproduces exactly (2,085,467 burst vs 1,591,692 quiet =
1.310x on isotropic q/256 at n = 6400). NEW beyond both checkers: (a) OBLIQUE — fleet B
given a coherent +q/8 transverse drift (sigma = 0, no jitter, zero randomness) reads
the identical one-shot signature (maxW 3.05x, F64_late 0.9, width 2.94*extent): the
kill condition is transverse-velocity MISMATCH, not dispersion randomness. (b)
UNEQUAL — n/2 vs n/4 fleets, ky = 0 both, columns aligned: the TRAIN stands (6 peaks,
period 640, amp 0.951, F64_late 935, conc 18.6, maxc = n/4 per chronon), so the
operative condition is exact integer ky-equality + column alignment + no jitter;
"head-on swap symmetry" is a loose name (no mirror exists at unequal sizes) — the
dossier's stated condition predicts both directions correctly. (c) MIXED (the game
case, coherent n/2 fleet through a thermal n/2 cloud in half the box): NO 3x season
(worst 64-ch window 1.51x late mean) but NOT flat either — persistent m_late 8.2% vs
thermal 2.4-2.8%, F64_late 9.2-9.7, late rate 1.26x thermal: the fleet stays coherent
through a dilute cloud forever; "flat forever" is a fleet-fleet statement (bounded
exposure, permanent modulation). Also verified in worlds.rs:154: galaxy draws drift as
random integers within +-q/4 with dispersion +-q/16 and jitter +-q per component, so
GENERATED fleets always carry transverse structure — the train needs authored fleets.]


**NEW (ded5, second author on 84b2 — the checker's named gold experiment flown: the
ringdown is EXTINCT at n = 12800 within the horizon ∝ side; the 3.43% m reading was the
fixed window, not the law; the steady state is scale-free).** n = 12800 (side 240), burn
1024, horizon 24576 (102 side-units = 2.1× the 6400-relative extinction horizon), seeds
1-3, seed 1 bit-identical to the checker's committed arm through all 9216 ticks:
block F64 decays [404-421 → 87-109 → 49-60 → 21-27 → 11-18 → …] to **all-≤6 from
blocks 5-7 (t 10240-14336 post-burn), tail flat at 0.9-3.6** — no plateau, no return;
extinction onset grows 1.7-2.5× across the octave vs side ratio 1.41 (slightly
super-linear; horizon rule: fly ~2× the 6400-relative). The whole-run m trend 1.4 →
2.4 → 3.4% (3200 → 6400 → 12800) dissolves on one series: m(H 8192/12288/24576) =
3.37-3.54 / 2.79-2.94 / **2.00-2.10%** — and whole-run m never converges (block 0's
F64 ≈ 405 dominates the variance at any horizon); only windowed statistics do.
**The scale-free instrument is late-window F64 (= mean64_late·m_late², window ≥ one
lifetime past genesis), not raw m** (raw late-m falls on a 1/√mean64 counting floor:
2.4% at n = 400 → 0.75% at 3200 with F64_late flat): F64_late = 2.31 (400) / 2.44
(1600) / 1.95-2.09 (3200) / **2.86-5.15 (6400 — its H8192 window still holds ringdown,
blocks 2-3 of 4)** / **1.12-2.64 (12800 — window 5 lifetimes past extinction)**: the
thermal dense order's steady state is the same anti-bunched object at every scale
flown (400-12800, 32× in n), m_late 0.28-0.43% at 12800. Allocator ratios at 12800:
per-chronon p99/p50 1.093-1.099 whole, 1.044 late; per-64 max/p50 1.009-1.013 late —
**no smoothness cliff in either direction; the bounded-modulation deletion (no
batch-shaping or dephasing machinery for thermal dense scenes) holds across the
octave.** Record fixed: 6400 row = F64 38.18-43.77 (3 seeds), m 2.42%; poly_r = 17.26,
m 2.26%, mean64 33798 (late tail F64_late 7.06 — radius spread roughens the steady
state slightly); T = 4.8-7.9·side measured (censored ≥ 6-8.5); regen contains the
12800 arm. (20261019-0141-second-20261018-2312-dynamics-84b2-ded5; predictions
pre-registered — P1/P5 held, P2 held 2/3 seeds (s1 half a block past the band), P4
direction held / number missed (2.0-2.1% vs ≤1.6%) and the miss is the instrument
lesson; regenerable ~10-13 min.)
[Checker, adversarial — all three probes confirm (evidence in the run's `chk2/`): fresh
seed 4 at 12800 extinguishes at block 5 (m_late 0.37%, F64_late 1.88, m@8192 3.44% —
the artifact reads identically on a 4th seed); 6400 flown to H 16384 (prefix
bit-identical) reads blocks [117, 19.5, 7.3, 2.7, 0.9, 1.8, 2.6, 2.1] and F64_late
4.96 → 2.87 — the "6400 row smuggles ringdown" reading is flown, not inferred; 25600
partial (10 complete blocks, t ≤ 20480) decays monotonically [887, 451, 238, 119, 74,
43, 28, 11.7, 8.0, 4.3] to all-≤6 at t = 18432 — inside the predicted 18-30k band —
with m@8192 3.86% (the fixed-window artifact grows on at the next octave); onset ratio
1.29-1.80 vs side 1.41, so the super-linear hint was likely seed scatter; F64_late at
25600 stays open (one post-extinction block). Record caveat: this run's work/patch.diff
is empty — the harness source is 84b2's committed patch.]

**84b2, dynamics — checker2's two unpriced leads, first half priced: the breathing
mode's "N-scaling" is an identity, not a coherence growth, and the mode is the genesis
ringdown, not an attractor.** On the same surface as 834e (shipped `Chronon` +
`RelativisticV1`, Q = 2²⁰, `worlds::gas` touching lattice, fill 0.7, vmax 2¹⁶, burn 1024,
horizon 8192, seeds 1-3), the N-ladder n = 400 → 6400 reads: **Fano₆₄ = mean₆₄·m² exactly
at every n** (definitional — Fano = mean·relstd² for any window-count distribution; the
measured content is ν flat in n, 0.159-0.173, and m, the contact rate's *relative*
modulation, 1.2-2.5% seed-scattered over the n flown: n = 400/800/1600/3200/6400 → F64
1.8-2.2 / 1.9-2.7 / 2.4-3.2 / 6.4-7.9 / 38.2-43.8 with m = 2.2/1.6/1.3/1.4/2.4%,
e.g. 69032·0.0235² = 38.2 at n = 6400 seed 1 — and reproduces checker2's 33.4). The
checker2 scaling (1.2 → 33.4 from 400 → 6400) is counts ∝ n under a bounded modulation:
**no coherence grows with N.** The mode's spectral *share* grows with n (0.01 → 0.37)
only because the Poisson noise floor 1/√mean₆₄ falls (1.6% → 0.4%) past the fixed ~2%
oscillation — the "transition" between 1600 and 3200 is statistical emergence, not
dynamical onset. **The mode is the genesis shock's ringdown of the box, a transient**:
F64 in successive 2048-chronon blocks decays (n = 3200: 24.5 → 2.4 → 2.2 → 1.7; n = 6400:
117 → 19.5 → 7.3 → 2.7, three seeds tight), the late-block steady state returns to the anti-bunched baseline
F64 ≈ 1.3-2.7 n-independent, and the period scales with the box, T ≈ (4.8-7.9)·side
chronons (seed 1: side 43 → T 341; 85 → 409; 120 → 682; 170 → ≥1024 at the
resolution floor), against the cage-rattle alternative (T ≈ 22-45, side-independent):
an acoustic box mode with effective phase speed ~0.3-0.6c — the touching lattice's contact
network carries pressure ~10× faster than the particles (⟨|v|⟩ ≈ 0.044c) [c_eff inferred
from measured T; mode shape unmeasured — genesis-id band binning dies at maxdisp 25-37 lc,
band correlations ≈ 0 at 400/1600, caveat]. **The allocator letter holds at every n
flown: per-chronon p99/p50 ≤ 1.29 (worst at n = 400, small counts; ≤ 1.19 from 800 up),
per-64-window max/p50 ≤ 1.08 at every n ≤ 3200 and 1.115 inside n = 6400's strongest
ringdown block (F64 = 117, block 0)** — checker2's "allocator-visible" danger is
priced and bounded: a ratio-tail gate never sees it, and the absolute variance it adds to
batch sizes is the affine cost already counted. (20261018-2312-dynamics-84b2, this run;
harness `crates/lattice/examples/breathe.rs` + `analyze.py`, regenerable ≤ 15 min.)
[Checker, adversarial: reproduced bit-identically (three arms rerun, diff clean); at
vmax 2¹⁷ (β ≤ 0.18) the bound tightens (m 1.59%, F64 30.4 at mean64 120419, blocks
85.5 → 1.2); but at n = 12800 the whole-run m reads 3.43% (F64 164.0 = 139526·0.0343²,
identity holding) with ratio tails still flat (b0 max/p50 1.109, p99/p50 1.131) — the
fixed-8192-horizon m conflates the longer-lived ringdown (lifetime ∝ side) with the
steady state, so "m ≤ 2.4%" is a domain statement (n ≤ 6400), not a law; the n-invariant
instrument is late-window m or horizon ∝ side.]

**Prior standing (834e + checkers, unchanged where not refined above).** The dense order
at filling fractions 2%→78% has no avalanche regime for THERMAL (zero-drift) genesis:
the contact stream anti-bunches as caging sets in (Fano₁ 0.99 → 0.56 from φ = 0.05 to
0.78), frames stay flat (p99/p50 per-chronon ops ≤ 1.094 on every arm), no per-tick
contact component exceeds 20 at n = 400, and the per-chronon cost is affine in the
collision rate — with this run's refinement that the Fano₁ crossing 1 at n = 6400 (1.16
checker2; 1.34 here) is the same bounded-modulation identity at window 1, not a regime
change. Coherent formations (bulk drift) still bunch violently: wall-ram Fano₁ 128.6 /
97.1 / 10.7 by dispersion, head-on fleet-fleet Fano₁ 96-97 with n/2 pairs in one chronon,
p99/p50 2.08 (checker2) — **the formation burst law remains the unpriced half** (see Open
directions). The rate law stands: measured/Henderson declines 0.970 → 0.420 as φ → 0.78
(caged quasi-periodic rattling, distinct-partner fraction 0.78 → 0.008), PHASE DEPHASING
is the anti-bunching mechanism; engagement (ν = 1) needs ⟨|w|⟩/Q ≈ 0.18 at φ = 0.78,
unreachable (~8c) at fleet densities φ ≤ 0.1, and even at engagement the cost stays
linear. μ = 1e-2 runaway = root-clock event storm on slingshot ejections (taleb-6de0);
encounter-parity rate form: burst process with two clocks, plane/truth curves track to
max |ΔS| = 0.062 at μ = 1e-3 (80fe); the 48 co-orbital deaths = kick-time planet-disk
crossings (e846); the dense order's ensemble statistics equal its own continuum limit —
quantization innocent at the ensemble level, pass-through is the real fast-contact
semantics (87.5% exchange no impulse) (f50d).

## Refuted

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
2. **ANSWERED (90b7; e56b closes the named leftovers)** — the formation burst law is priced with the F64_late
   instrument: one-shot 3x for any transverse structure (see Current best); a standing
   train only under exact transverse-velocity equality (survives arbitrary sigma_x;
   checker: binary — sigma_y = 1 quantum kills);
   the comb (n/2 contacts per chronon, 21x concentration) only exactly aligned. The
   mixed scene, the wall-reflection train and free-space one-crossing are now flown
   (e56b): fleet×belt = one season + an extensive hot plateau (15.5× the cold belt
   while confined; free space: one season, no step; no train, no clock). Left for a
   next run: the gravity-held belt (confined without walls — the plateau's lifetime
   there), the plateau's slow decay constant (horizons ≥ 10⁵ ch), and the per-body
   two-temperature decomposition.
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

None open. This run resolves its own apparent tension with checker2 (33.4 vs 38.2 at
n = 6400: seed/protocol scatter inside the identity; F64 at n = 400 reads 1.8-2.2 here
vs 1.2 there — same order, same law). The toy (5cad) and the shipped laws measure
different error models at different Q, as recorded.

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
