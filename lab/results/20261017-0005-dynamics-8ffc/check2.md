Grade: gold

**Abstract.** Claim: the belt's freeze crest is a period-halved two-comb train — a kick comb (51.6–53.8 µs/event) and a boundary comb (12.6–13.2 µs), ≈1.00 events/body/interval each — recurring every doll interval, so idle-time compute-ahead fits the player's pace (10.8×/3.2× headroom at 3×10⁵/10⁶) but is 308× short at 10⁹, and kick-counted 10⁹ ledgers undercount belt CPU ~26%. Reproduced bit-identically (window-1: 310,225 kicks / 310,429 boundaries at 3×10⁵; 110,185 / 110,366 at 10⁵; ledger 11.4×/3.4×/0.003×). My arms: N=10⁴ holds the identity across three decades; rtf 150 holds it at the player's pace (freeze 16.8→9.0 s); 6.5 intervals at 3×10⁵ confirm recurrence with 3.5–5 %/interval shear decay. Adopt: reprice e7ef/98cb by +26 %; the scheduler is the integrator's.

## Reasons

**1. Reproduction (clean tree, patch applied by me, warm build).** Arms A and B re-flown
(`300000 coast 150 1800`, `100000 coast 60 3600`, sequential, load 0.7–2.1). Deterministic
core bit-identical to the runner's regen: window-1 masses 310,225 kicks / 310,429 bnd (3×10⁵)
and 110,185 / 110,366 (10⁵); locals' comb digits 10,046–10,302 at both N; gap 3.13–3.14
ev/game-s; 7 crests at both N, same epochs, same kick/boundary alternation (kick share
97–99 % / 1–2 %). Later windows within 0.06 %. Timing: kick crests 50.6–51.6 µs/ev, law
ratio 1.01–1.07 (clamp-law control holds); ledger 11.4× / 3.41× / 0.003× vs the claimed
10.8× / 3.2× / 0.003×. The patch is print-only as claimed (read in full: cfg-gated macOS
footprint + 9e75's Linux fallback, spell table, `ES_TRACE`, wall cap raised; no law or
schedule change) — and the deterministic outputs prove it.

**2. Predictions.** `predictions.md` (00:11) predates the flights (logs 00:39+, regen state
00:37:41). P2/P3/P5/P7 held; P7 (the consequence) exactly. P1 formally wrong on epochs —
reported by the author as the discovery (the second comb); P6 refuted for half the cycle —
same discovery. P4 failed on 2/7 boundary spells and was flagged with counts standing. No
kill criterion fired, correctly: K1 crest 2 = 0.89×E₁ (window mass) ≥ 0.1; K2 spacing =
interval per comb; K3 = 1.00 per comb after the locals' subtraction.

**3. Adversarial arms (mine; one beyond both grids).**
- **N=10⁴ (a decade below the author's range):** kick window 1 = 20,185 ≈ 10,100 locals +
  10,085 belt (1.008/body); bnd windows 20,366/20,054/20,026; the locals' comb reads the
  same digits (10,112/10,272/10,302) at 10⁴, 10⁵ and 3×10⁵. The 1.00+1.00 identity and the
  ~+26 % correction are N-robust across three decades.
- **rtf 150 (below the author's rtf grid; the player's pace class):** window 1 = 310,224
  kicks — the same digits as rtf 300; crest 1 clamps 9.0 s (vs 16.8 s at rtf 300), one
  frame over 12 ms in 130 s, p50 0.041 ms. The compute-ahead headroom reading holds at the
  pace that matters.
- **rtf 900 at 3×10⁵ to 6.5 intervals (~1.8× the author's horizon):** every kick window
  full (310,224→254,398; interval spacing 28,047–28,889) — recurrence confirmed at the
  decisive N. But mass decays 3.5–5 %/interval (per-body 1.034→0.848) and shears into a
  background growing 3.1→12.9 ev/game-s; boundary clamps vanish from the spell table by
  crest 6. The combs decay together (ratio stays ≈1:1), so the composition correction and
  the 308×-short verdict survive — the interval-1 constants the ledger uses are the peak
  bill. "Stable limit cycle / recurs forever" overstates; corrected on the page.
- **rtf 3600 at 3×10⁵ with longer wall:** the baseline saturates (p50 11.9 ms, lag 60 s) and
  presented coverage caps at ~3.6 intervals regardless of wall — horizon extension needs an
  intermediate rtf; the decay ratios are partly delivery-read artifacts (the author said
  this), but mass conservation plus the growing background say the shear decay is real.

**4. Novelty.** The published `lab/wiki/kick-cadence.md` holds "per interval was never
observed past one crest" (4093/9e75) and a kicks-only metronome; `promotion.md` direction 3
gates compute-ahead on exactly the ≥3-interval spell. docs/HISTORY.md has no two-comb or
boundary-comb entry. The run answers the gate and corrects the premise in adopted
arithmetic (e7ef's 0.999 kicks/body/interval, 98cb's composed ledger).

**5. Mechanism, verified in code.** `step.rs`: the kick plans `Boundary` at `t + full/2`
and `Kick` at `t + full`; `boundary_clock`'s doc: "the synchronised output of the split, in
the middle between two kicks". A genesis-phase-locked belt carries both combs by
construction. (Seed is fixed at 1 in `nladder.rs`; checker 1's seed-2 arm at 10⁵ agreed.)

**6. The page.** Faithful to the evidence; I corrected three overstatements in place — the
headline "stable … limit cycle", the Runs line "a stable two-comb limit cycle", and I
appended a checker2 block with the arms above.

**7. Goal fit.** Board #1/#3: it decides the 10⁹ compute-ahead question (capacity-bound,
no scheduling cure) and reprices the 10⁹ ledger (+26 % belt stream). PRINCIPLES #17: "Use
idle time to compute ahead — yes this is a whole important idea of this project"; #12:
"the algorithm that allocates the work to prevent those heavy tails" — the heavy tail is
now a measured, periodic, predictable comb. Premise shown wrong (kick-only identity) — the
gold bar.

## What the author missed

- "Forever"/"stable" (headline and dossier): the train decays and shears on every horizon
  flown; by interval 6 at 3×10⁵ the combs hold ~0.85 events/body and the between-comb
  background has quadrupled. The ledger survives (peak-bill constants, 1:1 ratio), the
  wording did not.
- rtf 3600 cannot extend the horizon at 3×10⁵ (saturation caps presented at ~3.6
  intervals); long-horizon flights need rtf ≈ 900.
- Coast-only, one scene; seed-2 flown only at 10⁵ (checker 1); the burn arm and the
  de-phased (stagger/chain) arms remain unflown with this instrument — the named next
  experiment (`BELT_SPLIT` and the boundary comb) is correctly stated and still open.
- The arm-C idle figure "p50 0.903 ms, events/frame p50 1" is not what the [19k,25k] gap
  trace reads (p50 0.074 ms, events p50 0): the engine is even idler than claimed;
  direction unaffected.
- The 10⁶ row is arithmetic on measured constants (2.34 GB build > the lab's 2 GB cap),
  cross-checked to 20 % by 9e75's independent 69–73 s derivation — acceptable, but it is
  not a flight.

## Reproduce

`git apply lab/results/20261017-0005-dynamics-8ffc/work/patch.diff; cargo build --release
-p emergent-universe --example nladder; ES_TRACE=1 <bin> 300000 coast 150 1800` (arms B/C
likewise; my adversarial arms: `10000 coast 60 3600`, `300000 coast 130 150`,
`300000 coast 300 900`), then `crest.py <log>` and the window-mass script in `regen.sh`.
Scripts and logs: `/home/glmlab/check2-8ffc/` (outside the run folder).
