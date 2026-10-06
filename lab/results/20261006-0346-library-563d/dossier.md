# Dossier — 20261006-0346-library-563d (library lens)

**Claim.** For the engine's one slack-queue allocator (board bottleneck 4, Julien: "the
algorithm that allocates the work to prevent those heavy tails, it's the most important
one"), a fat-tailed preemptive-queue probe shows online *ordering* is closed (LeastLaxity ≈
EDF within 1.18× p99), *utilization* dominates (10.9× p99 from ρ 0.7→0.95), ordering by
unit size starves the tail (SRPT max lateness 643–2753 vs 25–149), and the one remaining
10× lever is **prediction-fed compute-ahead** (deadline misses 31%→0.9% at ρ=0.9) — with
five library lessons wired to live decisions (author-final.md).

**Bottleneck.** Board #4 (smoothness/allocator: "i care about the p95/99 results", CL
09-25) and the representation's allocator rules (archive/engine.md rules 5–9). Expected
gain: not a speedup but a *deletion and a direction* — delete forecast-for-ordering and
any size-ordered queue; point idle time at speculative certificate renewal. It lets us
delete the idea that the one queue needs a cleverer key.

**Evidence** (all numbers from `data/probe_results.json`, regenerable in ≤ 60 s):

```
cd lab/results/20261006-0346-library-563d/work && python3 allocator_probe.py 5000 10
```
(re-run verified: all 90 cells bit-identical; only `wall_s`, the timing field, differs)

- P99 lateness (mean-service units), capped, α=1.5: LeastLaxity 14.5 / 60.1 / 158.4 at
  ρ = 0.7 / 0.9 / 0.95 (FIFO: 32.5 / 92.3 / 169.6; EDF within 1.18× of LeastLaxity in all
  nine capped cells).
- SRPT (size-ordered) Lmax: 643.5 / 1315.6 (ρ=0.9/0.95, α=1.5, capped) vs EDF 51.2 / 76.8
  — best mean flow, worst tail.
- Clairvoyant = EDF with arrivals pre-rolled to t=0 (perfect forecast + legal
  compute-ahead; an *upper* bound since it ignores speculation discards): p99 −3.6 vs EDF
  56.9 and misses 0.9% vs 30.8% at ρ=0.9, α=1.5; still 3.7%–10.6% misses at ρ=0.95 where
  every online policy misses 46–63%.
- Validity controls: 0 clairvoyant-vs-EDF violations; a Horn-rule clairvoyant was tried in
  a pilot, had 69 max-lateness violations (my bug), and was dropped (disclosed in
  predictions.md).

Model: 5,000 items × 10 seeds per cell; 70% cheap units (0.2+Exp) + 30% heavy
Pareto(α) capped at 40 mean-cheap-units (plane.md #7's bounded claim) or uncapped
(negative control); Pareto(1,1.5) interarrival gaps; slack log-uniform over 3 decades;
exact ρ by timeline rescaling; lateness normalized by mean service. Cloud Linux/x86,
20.5 s wall: orders of magnitude only.

**Predictions.** `predictions.md`, written before the decisive run (with two disclosed
corrections: an accidentally pre-filled results block removed before any full run; the
pilot's two model defects fixed and re-frozen). Held-out: P1 held (0.45× ≤ 0.6), P2 held
(≤1.18×), P4 held (10.9× ≥ 3×), P5 held (kill criterion did **not** fire), P3 failed at
its named cell with a diagnosed confound (cap vs deadline tightness via timeline
rescaling; the negative control does blow up 2.8×–39× in 7/9 other cells — kept as a lead).

**What would make it wrong.** The queue is a faithful model of neither the frame's
16.67 ms deadline nor per-item causal slack correlations (a huge unit in the engine often
carries large slack: compile in idle time), and arrivals there are forecastable with error,
not perfectly (clairvoyant is an upper bound). If B10 on the real plane shows the slack
queue already at the compute-ahead frontier, or if speculation discard rates approach
arrival rates, the 10× headroom estimate collapses. The five lessons: 1–3 are backed by
this run; 4 (Hayek/sufficient-statistic messages) and 5 (Musashi/cadence on the orbit's
own clock) are argued and must pass their named tests (two-mass 1PN from monoid messages;
B13's four near-parabolic seeds with periapsis-locked kicks) before adoption.

**Cost of adoption.** Small and local: no new component. (a) Keep the slack queue's key;
explicitly forbid size-ordering (nothing to build — a constraint). (b) Route idle time to
speculative renewal of the next predicted expiry (the plane already has the slack queue
and the phase clocks; this is a policy on existing machinery). (c) A B10 readout addition
(Lmax, p99) — the integrator owns that gate. Fits PRINCIPLES: "Compute only surprises"
(#3: idle-time compute-ahead is exactly "use idle time to compute ahead", OC#36/#17);
"the simulation decides; heuristics schedule" (#22: the tubes' phase clocks *are* the
simulation telling us what's next); "minimize spike compute... p95/99" (#12); "the best
part is no part" (#17: deleting forecast-for-ordering). All quotes in author-final.md are
UNVERIFIED: READWISE_TOKEN was set but empty, so no highlights were retrievable; books
confirmed via `lab/library/goodreads.csv`.

**Novelty.** engine.md lists least-laxity (1973), calendar queues, Time Warp as "build
from long-proven algorithms" — design, unmeasured; no HISTORY entry measures allocator
disciplines or forecast headroom (closest: H0210's plane tails, taleb-c271 replays,
q-skin's slack skin). The SRPT-starvation number and the ordering-vs-compute-ahead split
are new here.

**The lens.** A library lens sees practitioners where the math lens would see theorems;
its risk is analogy-dressing. I kept only lessons that name a decision and a cheapest
test, and ran the cheapest test for the three allocator lessons. What it may have made me
miss: the probe's queue is single-server and ignores the CPU/GPU split (dense order) and
memory locality; and the lens drew me to scheduling books while the *correlated* slack
structure of the engine (expensive unit ⇒ far deadline) might make the real system closer
to the clairvoyant column than my online columns — a measurement on the plane decides.
