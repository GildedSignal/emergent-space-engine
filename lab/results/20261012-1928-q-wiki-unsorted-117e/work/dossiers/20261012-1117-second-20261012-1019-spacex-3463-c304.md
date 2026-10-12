# Dossier — c304, second author on spacex-3463 (the attribution experiment the checker named)

## Claim

The checker's named experiment, done: the plane's ~845 MB at 4,000 members is **retained rebind
history — ~10 kB per ship kick, unpruned because `settle` bypasses the every-64-frames prune —
plus a true construction marginal of ~19 kB per handed-out body; battle churn is irrelevant
(no-battle ≈ stock, 781 vs 846 MB), the m40000 "cannot be constructed" reading was a wall-speed
artifact (all 40,000 construct at 19 kB/handout, then kick onset takes the same run to 1.8 GB),
and the dashboard's `bytes_per_body` under-reports honest unpruned state ~20× (8.0 vs 163 kB/body;
~4× against post-prune steady state ~33 kB/body) — mostly by not charging retired segments, not
by the flat-4096 Passage charge (real passages average 14 kB, tails rare).

The original run's headline ("~330 kB per body, growing with body count") is refuted; its
instrument-lie finding stands, now measured; the idiot index against the 16-byte tube is
~2,100× steady / ~10⁴× worst-window, not 20,000×.

## Bottleneck

Board focus item 5 (10⁹ in 8 GB) and the checker's "one experiment for gold". Expected gain: the
shipmem/B18b memory design now has the real per-body budget to hit (≈33 kB steady at this
workload — 33 GB at 10⁹, still 4× over 8 GB, but 100× closer than the 20,000× claim) and the
real lever (bound per-kick history retention: 10 kB × kicks-per-prune-horizon per body).

## Evidence (Linux/x86, shared 8-vCPU box, load ~1–3, seed 1 unless said; all under the patch in `work/c304-patch.diff`, release build, each run ≤ 83 s)

The instrumentation (all observation-only; digests unchanged): a counting global allocator
(`live` requested bytes), a per-25-handouts probe (RSS, live, honest tube bytes by kind, churn
counters, a 1.7 GB guard), an honest store account (current trajectories, retired segments'
trajectories behind their `Arc<Entry>`, plans, records), a post-prune account (the prune rule
applied at the final tick), end-of-run `malloc_trim`, and a `--gap` scene lever (fleets born
outside the frame's extent rule 4,740q/32: all members spill at t≈0, the frame dissolves, no
battle ever runs). Commands: `xtask universe --bench --rtf 100 --seconds S --unpaced --members N
[--gap 2000] [--seed 2]` with stderr kept (the author's lost-stderr failure mode is fixed: every
probe line is in `data/probe-*.err`, the accounts in each JSON's `memory_c304`).

| arm | bodies | peak RSS | kicks | hist now | hist after prune | trim returns |
|---|---|---|---|---|---|---|
| A m4000 stock, S=8 | 3,881 | **846 MB** | ~56k | 558 MB | **80 MB** | 0.1% |
| B m4000 `--gap 2000`, S=8 | 3,879 | **781 MB** | ~53k | 512 MB | 79 MB | 0.3% |
| C m40000 stock, S=8 | 38,026 → guard | **1.88 GB** (guard at 1.7) | 75.6k in last window | 869 MB at guard | — | — |
| D seed 2, S=4: A / B | 3,806 / 3,756 | 718 / 636 MB | — | 468 / 408 MB | 377 / 330 MB | — |

- **Record regenerates:** m4 and m48 S=8 digests match the author's bytes exactly (`6af71966…`,
  `29f440d6…`); A's m4000 digest `632b4b53e993af8d…` matches at a presented tick of 9.18M against
  the author's 3.67M — determinism across machine speed, at the canonical cut.
- **Retained, not transients** (prediction 1, held): live requested bytes track RSS (A2: 903 MB
  live / 845 MB rss); `malloc_trim` returns ≤0.3%; the honest account explains ~70% of live
  (A2: hist 558 + current 42 + recs 15 ≈ 615 of 903; the rest is view cache, queue, JSON DOM,
  Vec overallocation). The counting allocator + structural account + trim replaces the requested
  heap profile: it answers transients-vs-retained directly and decomposes the retained side.
- **Churn is irrelevant** (prediction 2, falsified — the falsifier I pre-registered): B (no
  battle: slices=1, frame dissolved at t≈0, zero encounters) lands within 8% of A. Both arms end
  with ~3,880 bodies × ~14 kicks each; every made ship kicks on its own cadence regardless of how
  it left the frame. The regime variable is **kicks, not battle churn and not body count**.
- **The mechanism:** each kick rebinds a fresh compiled trajectory and retires the old binding —
  trajectory included — into history (`apply` → `retire`); `prune` runs only in `frame_to` every
  64 frames, and the end-of-run `settle` loops `advance` directly, so nothing prunes. Measured:
  **10.2 kB retained per kick** (A2: 558 MB / 55,839 kicks ≈ 55,839 kicks to the last handout);
  applying the prune rule at the final tick drops history 86% (558→80 MB).
- **Construction marginal:** 19.2 kB/handout (median, C: 35,000 handouts at 40k members with
  kicks=0, live≈rss throughout; A/B early rows agree at 17–25 kB).
- **The m40000 artifact:** C constructs all 40,000 (675 MB at 19 kB/handout, `tick=136`, hist=0)
  and then, at handout #≈37,750, ships' first kicks come due — d_rss jumps to 590 MB per 25
  handouts, history 869 MB, guard fires at 1.88 GB. The author's own file (12,392 leavers in
  47.7 s wall, flat at ~19 kB) and the checker's flat reading are the same run on a slower
  window: wall-speed truncation, not a benign regime. "The plane cannot be constructed at 4×10⁴
  members on this box" is false.
- **The instrument, measured:** A2 dashboard `bytes_per_body` 8,022 B vs honest unpruned
  162,875 B (20×) vs honest post-prune 33,726 B (4×). Decomposition of the honest unpruned 159
  kB/body: ~144 kB history (88%), ~11 kB current trajectory, ~4 kB record+plans. The Passage
  flat-4096 charge is the small lie (passages: 1,773 bodies, 14 kB real average, 2,046 tail
  panels in total — tails are rare at this workload); the uncharged retired segments are the big
  one. Steady-state per body is prune-horizon-dependent: 33 kB at seed 1 S=8 (population older
  than the 2^26-tick horizon), 104–116 kB at seed 2 S=4 (young population; AU-scale haulers keep
  everything — light distance beyond any run).

## Predictions (predictions.md, written before A/B/C/D)

Held: (1) retained-not-transients with trim <30% and account ≥60%; (3) d_rss per handout rises
≥10× early→late in A (0.6→129 MB/25) — though it tracks kicks, not bodies; (5) the ≥15× lie
(measured 20×); (6) seed 2 keeps the orders (718/636 MB, same shape). **Falsified, and the
falsification is the result:** (2) B's marginal stayed ≤60 kB only while ships had not started
kicking — once they did, B converged to A (my pre-registered falsifier "B's late marginal ≈ A's"
fired, pointing at neither churn nor N but kick history); (4) C hit the guard after handout
#37,750 exactly when kicks started (construction itself stayed flat at 19 kB to #37,725).

## What would make it wrong

The account's history charge counts each retired segment's trajectory as unique — true here
(every rebind compiles a fresh shape; no `ShapeMemo` on the bind path), and `live`-vs-account
residual ~30% is attributed only by class (view cache, queue, JSON DOM), not by site; a dhat run
would name the remainder's sites. The steady-state number is horizon- and population-age-dependent
(33–116 kB/body measured); the prune horizon itself (2^26 ticks + 2·light_distance) is a law
constant I measured under, not a claim about. Linux/x86, shared box: orders only.

## Cost of adoption, fit with PRINCIPLES

Fix `bytes_of` (charge retired segments and the Passage's real bytes — now a measured ~20× lie,
not a code-read); prune inside `settle` (or at digest time) so records state steady state; the
memory design (B18b, shipmem) budgets **~19 kB per handed-out body + ~10 kB per kick inside the
prune horizon** — bounding kick-history retention is the lever, not the tube representation.
Nothing here weakens a gate; per "The cheapest compute is compute not done" (1) and "deeply
aware of von-neumann bottleneck and memory" (17), the queue's kick-law builds are untouched by
this result — the store, not the law, remains the wall at 10⁹, at ~2,100× the tube contract.

## The lens

The second-author lens trusts the checker's framing (churn-vs-construction) — that framing was
half wrong, and only the controlled pair (A vs B at one N) could show it; the lens also made me
run the prune-rule account rather than a profiler snapshot, which is what turned "retained" into
"retained-but-bounded". Missed by the lens: no allocation-site profile of the unexplained ~30%
of live; no paced (real-frame-cadence) confirmation that live play prunes as designed.

## Files

`data/bench-{A,A2,B,B2,DA,DB}-m4000*.json`, `data/bench-C-m40000.json` (guard-aborted: probe
record complete, dashboard JSON absent by design of the guard), `data/probe-*.err` (all probe,
END, PRUNE, GUARD lines), `work/c304-patch.diff` (the instrumentation, `git diff` of the tree),
`predictions.md`. Reproduce any row with the command pattern above, ≤ 83 s per run.
