# Dossier — 20261010-0448-second-20261010-0352-taleb-cb7c-c2f8 (second author on 20261010-0352-taleb-cb7c)

**Claim.** The checker's named experiment is done and the original claim splits cleanly: its
memory/determinism half holds (digest `f8b75cec…` and `dd178af9…` reproduce bit-for-bit from
the shipped binary, across pacing regimes and 2× core oversubscription), while its smoothness
half is refuted as stated and sharpened: there is **no compute cliff at ~428 bodies** —
contention-controlled, the frame's thread-CPU cost sits at the 16.7 ms deadline from ~212
bodies (cpu_worst medians 15.2–17.4 ms at every point 212–424, zero-to-few CPU hitches
everywhere) — the author's 23.25 ms gather max is a *wall* number whose frame had **zero** CPU
hitches in the author's own stored JSON, my same-core spinner reproduces the wall inflation
(wall hitches 0→1,200/hr, gather wall max +28–62%) with zero CPU hitches, the N=124-worse-than-
N=213 inversion vanishes at controlled conditions (cpu_p50 is monotone: 5.4→8.7), so it was
load history, not contact chaos — yet the **readout-skin work order stands on stronger
evidence than before**: the gather is the dominant *compute* term at every load (median share
0.61–0.67 paced, 0.55–0.61 unpaced) and the only unbudgeted one. One new measured effect: the
60 Hz presentation cadence itself costs **×2.49 per-frame CPU** versus running the identical
frames dense (same digest, same cut: cpu_p50 8.06 vs 3.23 ms; engine ×3.1, gather ×1.59).

**Bottleneck.** Board #4 (smoothness, worst frame) and the queued `b-readout-cost`. The silver
was blocked on three named things: the gather table was wall-clock mixing contention with
compute; the ladder points ran at differing loads; the N=124 inversion had an unexamined
confounder. All three are closed (above), and the decision the integrator needed — order the
readout skin or not — is now based on CPU-attributed numbers: yes, order it; it is 55–68% of
frame compute at every load, while the engine is budget-clipped and even *shrinks* in CPU under
contention (preemption eats its wall budget: cpu_worst 18.95→9.82 under the spinner, digest
equal). The cadence tax adds a second lever for the same work order: a budgeted, deferrable
gather that runs ahead in the idle part of the frame buys both the deadline and the ×1.59
gather dividend of dense execution.

## Evidence (Linux x86 cloud, 8 vCPU shared, loads 0.56–2.65 recorded per run in each JSON;
all times thread-CPU unless marked wall; full tables in `data/summary.txt`)

- **The record regenerates** (E0, u30): pinned rerun of the author's `det_repeat` gives
  `f8b75cec…` EQUAL; unpaced 30 s at members 384 seed 1 gives `dd178af9…` = the paced rerun =
  the author's stored `mem384`. No code edits (patch empty); `perf` is blocked on this box
  (paranoid=4, binary stripped) so CPU attribution is the crate's own `CLOCK_THREAD_CPUTIME_ID`
  per frame plus two stall guards: worst-frame |wall−CPU| ≤ 1.5 ms (34/40 quiet runs pass; the
  6 misses gap by 1.6–5 ms and taint only their wall columns) and gather-max ≤ cpu_worst + 1.5
  (40/40 pass — every gather maximum reported here is bounded by an unstalled frame's CPU).
- **The ladder** (E1: `taskset -c 6`, paced 60 Hz, rtf 100, 30 s, 8 seeds/point at members
  256/320/384/400 → 277–428 bodies; E4 adds members 96/192, 4 seeds): cpu_worst medians
  13.6/16.6/17.4/15.2/15.6/14.6 ms at ~121/212/284/344/407/424 bodies — flat at the deadline
  from 212 up; CPU hitches (>16.7 ms) per 30 s run: medians 0/0/1/0/0/0, maxima 0/1/5/2/3/2.
  The cpu_p50 **median** jumps only at the first step (5.4→8.7) and then swings 2.5× with the
  seed at fixed N (3.3–8.8 at every point ≥ 284): above ~212 bodies the *seed* (the
  contact-cascade draw), not N, sets the typical frame. Gather p99 medians 5.9/7.7/8.2/7.5/
  7.8/6.7 ms; engine p99 5.4–6.4 (budget-clipped); gather median share 0.61–0.67 at every point (within-point 0.57–0.68).
- **Controlled contention** (E3: one SCHED_OTHER spinner sharing the bench's core, members
  400): wall hitches/hr 240→1,320 (s1) and 0→1,200 (s2); gather *wall* max 9.98→12.73 and
  8.36→13.57; cpu_worst **down** 18.95→9.82 and 14.18→11.91; cpu hitches 0 everywhere;
  digests EQUAL to the quiet runs. Wall gather max is a contention thermometer; the author's
  bursty load-3.9–5.0 machine plausibly reached 23.25 ms the same way (steady 2× here gives
  ~13).
- **The inversion** (E4): at controlled conditions cpu_p50 medians are 5.43 (~121 bodies) vs
  8.65 (~212) — monotone; the author's mem96>mem192 inversion was load history. Under load the
  engine's wall budget is spent on preemption, so contended runs look *cheaper* in CPU (their
  mem192 cpu p50 was 4.0 against my 8.6 at load < 1) while hitching in wall.
- **The cadence tax** (u30 vs E1 same point/seed): identical 1,800 frames, identical cut,
  identical digest; paced-at-60 Hz cpu_p50 8.06 ms vs dense 3.23 ms (wall 30.0 s vs 7.9 s);
  engine p50 0.42→0.13, gather p50 4.09→2.57. The 12 unpaced 20 s runs agree (wall==cpu to
  0.01 ms, share 0.55–0.61, gather p99 2.6–4.2). Mechanism not isolated here [INFERENCE:
  cache eviction / clock behaviour across the ~13 ms inter-frame sleep on a shared L3]; the
  effect is 13/13 reproduced and is the player's regime, so the paced numbers are the ones the
  skin must meet.

**Reproduce** (repo root; each bench run ≤ 35 s, whole scripts ~40 min single-threaded, ≤ 60 MB
RSS each):
```
cd lab/results/20261010-0448-second-20261010-0352-taleb-cb7c-c2f8
./ladder.sh    # E0 + first 10 ladder runs (tool killed it at 300 s; files kept)
./ladder3.sh   # resume: E1 remainder, E2, E3, E4, skipping what exists
taskset -c 6 /home/glmlab/lab-target-3/release/xtask universe --bench --seconds 30 \
  --rtf 100 --seed 1 --members 384 --unpaced > data/u30_M384_s1.json   # the cadence pair
python3 analyze.py    # prints data/summary.txt's tables
```

**Predictions** (`predictions.md`, written before the ladder): P1 held (digest EQUAL). P2
held on the guard that matters (gather-max 40/40) and missed on the letter (34/40 on the
worst-frame guard, 6 gaps of 1.6–5 ms). P3 **failed informatively**: no crossing inside
[380, 428] — CPU hitches appear sporadically from 212 bodies and cpu_worst is flat-at-the-
deadline from there; the cliff was a wall artifact. P4 held (share 0.55–0.68 everywhere;
gather p99 4–8.2 ms; engine clipped). P5 half-held: wall hitches ×5.5 (stronger than
predicted), gather wall max +28–62% (below the predicted ≥15 ms), but cpu_worst moved −48%,
outside my ±25% — contention makes frames *lighter* in CPU (budget eaten by preemption), a
mechanism I did not predict. P6 held in substance, failed in letter: the 5-hitch seed is at
284 bodies, not at the cap (M400 spread is [2,0,0,0,0,0,0,0]).

**What would make it wrong.** The 1.5 ms stall tolerances are judgement calls; a smaller
tolerance would flag more runs' wall columns (never the CPU columns). Bodies are end-of-run
counts (contacts spawn during play), so points are bands. The 4790-era shared cloud box with
other window runs means absolute ms are orders-of-magnitude only; the M1 re-measure should
keep the two stall guards and the paced/unpaced pair — the cadence tax may differ there
(unified memory, different L3 behaviour). The 300–500-body ask was truncated at 428 by the
scene's `--members` clamp(4, 400) (xtask/src/universe/mod.rs:32); no crate edit was allowed.
E4 has 4 seeds/point, not 8 (window budget); its verdict is monotonicity, not location.

**Cost of adoption, fit with PRINCIPLES.** Adoption is still a work order, now with numbers:
the readout skin (`b-readout-cost`) should be budgeted and deferrable like the engine, and
should exploit the idle part of the frame (PRINCIPLES #17 "Use idle time to compute ahead":
the dense dividend is ×1.59 on the gather, ×2.49 on the frame); load rungs need ≥ 8 seeds and
must report thread-CPU beside wall (#12 "i care about the p95/99 results i want the game to be
smooth" — the tail the player feels is wall, but only CPU numbers compare across machines);
plane.md §7's "nothing takes an unbounded synchronous claim on the frame … or **a gather**" is
confirmed as the binding clause, now with the CPU share that sizes the skin.

**The lens.** The second-author lens ran the checker's experiment faithfully and adds only
what the checker flagged; what it may have missed: it did not isolate the cadence-tax
mechanism (cache vs clock — one perf-equipped box or an M1 settles it), it cannot see the
browser/HTTP path at all, and with the gather dominant but engine budget-clipped the next
representation question (screen-space or cone-skinned readout, so the gather pays per *seen*
emitter, not per body) stays with the lens that owns the view. It also leaves the gather's
own split (Newton crossings vs `Seen` serialisation) unmeasured; the json term (~10%) bounds
only the serialisation half of that.
