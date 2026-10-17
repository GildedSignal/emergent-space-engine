# Dossier — 20261017-0428-taleb-3da3 (Taleb lens)

## Claim

**Capping the rollback ratchet (`ES_CAP`) is killed: the latch is convexity, not a tax — at
the 14,080-body conflict wave every cap arm still collapses to one region with digests
bit-identical to shipped and rollbacks that never recur (the quench rides the physical
conflict-merge, not the margin), while cap64 burns 2.3–3.6× shipped's wasted ops in every
paired run (cap16: 1.24× in its one run) and cap64 alone adds a fat wall tail (shipped:
60–74 s, 3/3 finish; cap64: 66 s, 189 s, and one 260 s DNF in 3 tries) — the wide latch's
margin-forced early merges are the cheap coalescence path, and bounding the latch buys
nothing at any size tried.**

## Bottleneck

The allocator page's open direction 1 ("cap the escalation: one line, untested — the named
next experiment", `lab/wiki/allocator-ratchet.md`). The sought gain was a bounded worst-case
latch (the wiki feared `2^rollbacks → E=512 at 28k bodies`). What the result deletes: the cap
candidate itself, and the premise that the latch level is a cost. Nothing else changes: the
ratchet ships as is.

## Evidence

Instrument: the prior gold run's `tax` verbatim (public API only; its `work/patch.diff`
re-applied, plus this run's `ES_CAP` arm — `work/patch.diff`, 3 files). The Fermi-cannon
battery, Newtonian, margin 2.0, min_region 1, q=256; every number below regenerates via
`regen.sh` (≤ 12 min). Machine: the lab's Linux box, 8 vCPU, load 1.3 at start; walls compare
only within this window (the no-conflict regime ran 3× slower here than on the prior gold's
box; the one-region regime matched it: shipped 81 c/s here vs ~82 c/s there at 14,080 bodies).

**S1 — no-conflict control (stagger 300, 1,408 bodies, horizon 6k, cap16):** 0 rollbacks,
escal 1.0, 354 regions end, 76 c/s. The cap is inert without conflicts. ✔

**S2 — conflict wave, 1,408 bodies (128 cells, stagger 30, horizon 6k), 3 arms:**

| arm | wall | rollbacks | escal_max | regions end | chr/s | digests |
|---|---|---|---|---|---|---|
| shipped | 3.34 s | 8 | 256 | 1 | 1798 | 49f5fc2b…/23291164… |
| cap16 | 3.57 s | 6 | 16 | 1 | 1679 | identical |
| cap64 | 3.53 s | 6 | 64 | 1 | 1698 | identical |

All three collapse to one region in the same wall (±5%). **The latch level (16 vs 64 vs 256)
changes nothing here** — same rollbacks (±2, within the known one-draw scheduling noise),
same end state, same digests.

**S3 — conflict wave, 14,080 bodies (1,280 cells, stagger 30, horizon 6k), 3 arms, rep 1:**

| arm | wall | rollbacks | wasted ops | merges/splits | escal_max | regions end | chr/s | digests |
|---|---|---|---|---|---|---|---|---|
| shipped | 73.9 s | 8 | 555k | 1136/72 | 256 | 1 | 81 | f0695d29…/a19963c5… |
| cap16 | 133.5 s | 8 | 688k | 598/252 | 16 | 1 | 45 | identical |
| cap64 | 189.4 s | 10 | 1435k | 1735/919 | 64 | 1 | 32 | identical |

**Rep 2 (interleaved shipped, cap64, shipped, cap64):** shipped 59.8 s and 63.5 s (8
rollbacks both, 680k/1065k wasted); cap64 66.1 s (7 rollbacks, 2.46M wasted) then **DNF at
260 s** (no RESULT; cause unopened — load-slowness versus wedge not distinguished, no worker
instrumentation attached). Rep-2 digests were not captured (the author's grep cut the line).

Reading both reps together: no arm ever recurs rollbacks (7–10 across every run, shipped's
own count) and every finish is one region — the quench needs no margin; it rides the physical
conflict-merge (each rollback merges the clashing lineages). What the caps lose is the
coalescence path: shipped's E=256 margins plan merges early (1,136–1,224 merges, 8–72
splits), cap64 coalesces late through conflicts and regroup churn (up to 1,735 merges, 919
splits). The load-free cost metric is the wasted-ops counter: **cap64 burned 2.3–3.6×
shipped's wasted ops in every paired run** (1.43M and 2.46M vs 0.56–1.06M; cap16's one run:
1.24×, 688k vs 555k — its 1.8× rep-1 wall is not explained by ops and stays
load-unresolved, but it too gains nothing). The wall is
load-confounded on this shared box (rep 1's 2.6× factor blurred to 1.1× in rep 2's first
pair) but its tail is asymmetric: shipped 60–74 s, 3/3 finish; cap64 66 s / 189 s / DNF in 3
tries — the capped arm lengthens exactly the many-region churn phase that is load-sensitive
here (the stagger-300 control ran 3× slower on this box than on the prior gold's), and it is
the only arm with a DNF draw.

**S0 — 44-body original (horizon 34k):** shipped and cap16 both finish (0 vs 2 rollbacks,
both escal ≤ 16, code-identical below the cap), digests identical. Confirms the one-draw
noise floor on rollback counts (thread timing, not the arm).

## Predictions

`predictions.md`, written before S2/S3. **P1 held** (digests bit-identical across arms in
every run where captured: 8/8 — S0, S2, S3 rep 1; rep 2's digests were cut by the author's
grep). **P2 failed on recurrence, half-held on ruin**: cap16 below the wiki's latch band did
NOT recur (8 rollbacks = shipped's) — the quench rides conflict-merges, permanence survives
the cap; but one cap64 run did DNF at 260 s (cause unopened). **P3 failed in its cost
half**: cap64 is not inert — 2.3–3.6× shipped's wasted ops in every paired run, and a wall
tail shipped does not show. **P4 held** (no separations at 1,408, all collapse, digests
equal). **P5 unexercised** (no instrumented wedge; the one DNF was not opened).

## What would make it wrong

- **A scene that should not coalesce.** The battery's wave wants one region, so margin-forced
  early merging is always the cheap path. In a scene with many independent quiet regions plus
  one local conflict wave, the latch is **global**: one wave's doublings (E=256) widen every
  quiet region's margins and may plan-merge work that never needed it — an over-merging tax
  the capped arm would not pay. That experiment (quiet archipelago + one cannon) is the named
  next probe; it is also the honest version of what ES_LOCAL tried to fix.
- **The one-draw caveat**: rollback counts and walls are scheduling-noisy (S0 shows identical
  code drawing 0 vs 2), and rep 2 blurred rep 1's wall factor (2.6× → 1.1× on the first pair)
  — the box is shared. What is stable across reps: cap64's wasted-ops ratio (2.3–3.6× every
  paired run), the end state (one region, always), non-recurring rollbacks, and shipped's
  3/3 finishes against cap64's 66 s/189 s/DNF. If a quieter machine erases the ops ratio
  too, the cap degrades from "killed on cost" to "inert" — still not adoptable.
- Only sizes ≤ 14,080 bodies were run (the 28,160 stretch is a commented block in
  `regen.sh`; the wiki's own 28,160 datum, one region at 10 c/s, is already the collapse's
  signature, which the caps do not prevent — they prolong).

## Cost of adopting, and fit with PRINCIPLES

Adopting: nothing — the cap is killed, `escalation *= 2` ships unchanged. The result is via
negativa (PRINCIPLES #1: "the cheapest compute is compute not done; delete before
optimizing"): it deletes the last open controller change to the rollback path and closes the
page's open direction 1. It also fits #25 ("not making mistakes matters more than doing
things efficiently"): the mirror-class arms' wedge remains the allocator's only reachable
ruin; the ratchet's unbounded latch is not one (E=256 here, E≈6×10²⁹ in the wiki's margin-0.5
census, both finished).

## The lens

Taleb asked where the ruin is; the answer is that the feared tail (the latch) is a phantom and
the tail that looked like upside (fast collapse through early merges) is the real convexity —
"capping the downside" here capped the upside instead. What this lens may have missed: I did
not build the scene where global latch coupling could hurt (the archipelago probe above), and
I measured no frames runs (the collapse at 10⁴ bodies is the visible surface per the wiki, so
batch is the honest judge here); the barbell's speculative end went unexercised.
