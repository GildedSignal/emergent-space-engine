# Dossier — 20261020-0036-second-20261019-2339-inversion-1d47-4063 (second author on 1d47)

## Claim

The checker's named experiment is done, and it splits 1d47's claim in 1d47's favour on this record:
flown with the canonical-cut instrument (`cut_digest`: the nladder burn with its decision at a
canonical tick, `frame_to(limit = cut)`, `settle(cut)`), **both** the all-to-queue gate
(`ES_ROOT_SHIPS_TO_QUEUE`) **and** the checker's reach-gated form (`ES_ROOT_SHIPS_REACH=16`, new this
run) hold the shipped digest at 10⁵ and 2×10⁵ on every schedule tested (unlimited / 12 ms ×3 reruns /
3 ms / no-flight settle / 4 threads / a deeper 18,000-game-s cut) — 34 cut runs (16 at 10⁵, 18 at 2×10⁵), one digest per rung
(`581ced1a…` at 10⁵, `a5edea1c…` at 2×10⁵; OFF = ON = REACH, encounter logs byte-identical across
reruns) — while the burst stays deleted (max_ms 22.8/… ms against OFF's ~800/1,650). The checker's
bistability did not reproduce; the stale reads it feared are real (3.8-11.2k captured candidates a
run) and **do** answer encounters at the two tightest conjunctions of the scene (3-6 answers a run,
|d| ≤ 0.71 of the window, staleness 60-230 game-s), but every one of those answers agreed with the
fresh read — verdict-preserving, not verdict-flipping, at these rungs.

## Bottleneck

The board's first (bodies in the flyable engine): the root burst. This closes the "what kept 1d47
from gold" question — the digest-schedule-invariance half — on the shipped record.

## Evidence

All from this run's arms on this tree (Linux lab box, load printed per run; orders of magnitude).
Patch: `work/patch.diff` = 1d47's (the gate, the scan probe, the Linux footprint shim) plus this
run's additions: `ES_ROOT_SHIPS_REACH` (`pull_ships_near`, universe.rs), the stale-encounter half of
the probe (which answered encounters came from a stale candidate, at what |d|/window and age,
encounter.rs), and `examples/cut_digest.rs` (the canonical-cut instrument). Unset = shipped bit for
bit. Reproduce: `regen.sh` (~13 min).

**The instrument** (`cut_digest N 17000 <sched> [threads]`): `plane_extra`, the burn's decision
scheduled at its canonical tick (200,000·rtf/1000; not `input(now)` — the decision cannot ride the
presented time), frames at rtf 1000 to the cut with `limit = cut`, then `settle(cut)`, then
`digest/kicks/encounters/contacts` + the probe counts.

**Cut 17,000 game-s (past the first kick wave), 10⁵** — `581ced1a98b7…`, kicks 127,671, encounters
1,802, contacts 0 on every row: OFF unl/12/3/no-flight; ON 12 ms ×3 (stale 4,914-5,050, max ~500 a
scan, stale_enc 0); REACH 12 ms ×3 (stale 4,954-5,024, stale_enc 0), unl (stale 3), 3 ms (stale
5,705), no-flight (stale 5,555, stale_enc 3); ON 12 ms 4 threads (stale 4,453). **Deeper cut
18,000 game-s:** OFF = ON, `15a5d8a26be0…`, kicks 129,240, encounters 1,848.

**Cut 17,000 game-s, 2×10⁵** — `a5edea1c64aa…`, kicks 227,671, encounters 1,838 on every row: OFF
unl/12/3/no-flight (stale 0); ON 12 ms ×3 (stale 10,327-10,356, stale_enc 0); REACH 12 ms ×3 (stale
10,450-10,478), unl (stale 8), 3 ms (stale 11,141), no-flight (stale 10,817, stale_enc 6). **Deeper
cut 18,000, 4 threads:** OFF = ON, `7f39534565ae…`. The ON arm's complete encounter logs (1,838
entries, under the 4,096 cap) are byte-identical across reruns (md5 `461ee701…`; dumps in `work/`).

**The offenders, named** (the probe prints each stale-answered encounter): ships 22070 and 160822,
items due 13.1M/12.0M ticks before the scans at t≈2,897M/2,930M (≈60-230 game-s stale — their
**The burst** (`nladder burn`, seed 1, rtf 1000, 12 ms, this box, sequential, state printed): 10⁵
OFF max 801.4 / p99 45.3 / over 14 → **REACH max 19.3 / p99 15.8 / over 17, lag 16.667 s, rss 483 →
361 MB**; 2×10⁵ OFF max 1,640.5 / p99 199.5 / over 18 → **REACH max 45.7 / p99 22.7 / over 12, lag
16.667 s, rss 947 → 536 MB**; refusals 0, dead 0, alive everywhere (the wave drains at the budget,
1d47's +1.4-1.6 s presented-time price unchanged).


## Predictions

`predictions.md`, written before the arms. **P1 held** (OFF one digest across all schedules, both
rungs). **P2 failed as a reproduction** — the prediction expected ON bistable at 12 ms; ON was
stable and equal to OFF on every rerun, schedule, thread count and cut. **P3 held and sharpened**:
stale_enc > 0 exactly in the no-flight arms (3 at 10⁵, 6 at 2×10⁵) — but these are verdict-preserving
answers, so they did not move the digest; the predicted equivalence "stale_enc > 0 ⟺ digest moves"
is refuted in the benign direction. **P4 held** — (a) the burst stays deleted, (b) REACH = OFF
everywhere, stale_enc 0 on all flight schedules. **P5 held** (the lag is ON's).

## What would make it wrong

A scene where a stale extrapolation crosses the window while the fresh fit does not (or the
reverse): the checker's own runs (its scene's decision landed ~20 ticks differently — `input(now)` at
frame 60 — and its box was loaded, so its deferral patterns differed) saw ±5 encounters and once
−11 kicks move; that did not reproduce here, but nothing in the reach construction forbids it — the
offenders are 10⁷ ticks of light distance out, beyond any pull. The guarantee is empirical (34 runs,
0 flips), not structural: the fence bounds *where* stale candidates live, not *what their
extrapolations answer*. Adoption therefore still re-freezes the digest on the M1 (the author already
priced that), and if the integrator wants the structural guarantee, the scan itself must read
canonical bindings (retire-on-read or a settled re-read), which is a different, small change to
`capture`, not to the pull. The 10⁶ rung remains unbuildable in this container (2 GB cap).

## Cost of adoption, fit with PRINCIPLES

One gated line either form (the queue already orders by `key + light_distance`, universe.rs:564);
no digest re-freeze *on this record* (measured; the integrator re-freezes per process anyway); no
new state. PRINCIPLES: "No work for no reason" (14) — the pull resolved the whole root wave inside
one item; "i care about the p95/99 results" (12) — max ≈ 800-1,850 → ~15-23 ms; "errors never
compound" (13) — the residual risk above is the honest counterweight, priced and named.

## The lens

Second-author lens: run the named experiment, trust the instrument over both priors (the author's
"cannot flip" and the checker's "bistable"). What it may have missed: the checker's exact harness is
not in the record (its `check_cut` was reverted), so the non-reproduction is against my
reconstruction of its recipe (the differences: the decision's landing tick, its fixed-1080-frame
loop, its box's load); and 90 minutes bought 34 cut runs on one scene/seed — the structural fix
(read canonical bindings in `capture`) is the follow-up if the integrator wants a law, not a
measurement.
