# Dossier — the demand-measured keep, flown

**Run:** 20261020-0143-spacex-c8d5 (lens: SpaceX). **Topic:** `history-demand` (open direction 1).

## Claim

Retention at **one light leg** (`ES_KEEP_LEGS=1`, margin 2²⁶ ticks untouched) is **flight-proven
complete** on the shipped scene at bench cadence — no emitter beyond the stock's own two goes
missing — and costs nothing in gather time; but the delete it buys is **small at one-wave depth**
(−8% segments, −7 MB), and the flight shows the **shipped view already loses 2 of 10,050 emitters
at every gather past ~frame 76 through warm-guess probes past its own two-leg keep** — a
keep-independent search defect, not a retention question.

## Bottleneck

Memory at long play (the ratchet, `history-demand`/`wiki-memory`): retention is the supply the
view never asked for (c7a6: demand = one leg; keep pays two + 2²⁶). Expected gain at ratchet
depth: ~½ the retained generations × 1.9–2.2 KB/binding (4a71's constant). What it deletes:
channel 2 of the ratchet without a freeze (b911's approach was supply-side).

## Evidence (all numbers from `logs/`, reproduced by `regen.sh`, ~6 min)

Scene: the shipped ladder scene (`plane_extra` seed 1 Sparse 1 48, N=10⁴ → 10,028 bodies),
`nladder`'s loop, 12 ms engine budget, rtf 6000, gather every `every` frames. Six arms:

| arm | game gs | gathers | losses | worst seen (of 10,050) | gather nones | deepest none (gs) | segments/body | RSS MB |
|---|---|---|---|---|---|---|---|---|
| stock coast e=2 | 16,455 | 120 | 112 | **10,048** | 49 | 6,539 | 2.36 | 99 |
| **1-leg coast e=2** | 15,543 | 120 | 105 | **10,048** | 50 | 4,470 | 2.17 (−8%) | 92 (−7%) |
| stock sparse e=60 | 16,093 | 4 | 3 | **10,048** | 2 | 3,367 | 2.46 | 100 |
| **1-leg sparse e=60** | 16,042 | 4 | 3 | **10,048** | 4 | 6,125 | 2.44 | 101 |
| stock burn e=2 | 12,180 | 120 | 74 | **10,048** | 12 | 2,263 | 1.11 | 89 |
| **1-leg burn e=2** | 12,530 | 120 | 75 | **10,048** | 262 | 3,275 | 1.09 | 85 |

1. **Completeness is keep-independent.** Worst seen is 10,048 in all six arms — the same two
   emitters missing in stock and one-leg, at every cadence and in burn. The one-leg keep adds no
   lost emitter (`losses` 105 vs 112, 3 vs 3, 75 vs 74: run-to-run noise; the stock arm rerun in
   `logs-regen/stock_coast_again.txt` shows 111–112 too).
2. **The shipped law already loses them.** Stock coast: 49 gather `binding_at` → `None`, deepest
   6,539 gs back ≈ 4× a belt leg (1,000–1,500 gs): a warm-guess probe past even `2·ld + 2²⁶`
   (the failure needs a probe deeper than the keep; these are deeper still, so halving the keep
   changes nothing for them — the nones count stays ~50). One read of the code makes it sharp:
   in `view.rs::crossing`, one `None` from `eval` drops the emitter for that whole gather
   (`else { continue }`).
3. **Burn stresses the None path, not the outcome.** Gather nones ×22 (12 → 262) under one-leg,
   losses unchanged: the shorter boundary catches more probes, and the cache re-learns — the
   emitter reappears in later gathers. The None path is noisy, not lossy, when the miss is
   marginal.
4. **The delete is real but shallow here.** Segments −8% (coast), −1.5% (burn), RSS −7 MB, at a
   flight depth of 12–16.5k gs where the stock retains only 1.1–2.5 segments/body (one kick
   wave). The ratchet scenes (c7a6: 9.07/body at 197k gs) are where the halving multiplies;
   this bench cannot reach them inside 60 s (the full gather costs ~20 µs/emitter — 390–417 ms
   per gather at 10⁴ — so per-frame cadence buys only ~120 gathers).
5. **Cost: free.** Gather p50 384→403 ms (coast, +3–5%, inside the run-to-run spread 384–417),
   readouts/gather 19,834 vs 19,334 (±3%): the search reads the same bindings.
6. **Digest is wall-coupled at rtf 6000** (same binary, same args: `f94f69c387b0` then
   `20a606853bd4` in-session; `regen.sh`'s `stock_coast_again` reproduces): the presented tick
   follows the 12 ms wall budget, so digest identity is **not** an available certificate on this
   bench — engine-side, the census answers instead: engine nones = **0** coast (both legs), 2 in
   burn (both arms, same count: a guarded engine read, site unattributed).
7. **Instrument notes.** The `ES_KEEP_LEGS` dial is one expression, read once; unpinned it is
   arithmetically the shipped `2·ld + 2²⁶` (both sites route through it). The census is one
   relaxed atomic load per `binding_at` call when off; on, it counts calls/Nones/deepest-tick
   (9.5–10.7M calls/flight, 90–95% from the gather). `keep_probe` uses `/proc/self/statm`
   (Linux); `nladder`'s macOS `proc_pid_rusage` does not link here.

## Predictions (`predictions.md`, written before any arm ran)

- **P1 held** for the dial (no additional losses, stock-equal worst seen) — but its stock
  premise ("stock gathers lose nothing") was **false**: the shipped gather loses 2 emitters
  mid-flight, which c7a6's tail-gather instrument ("no gather ever loses an emitter") never saw.
- **P2 failed as stated** (−8% measured against a ≥20% prediction): the one-wave depth bounds
  the stock's retained stock at 2.4/body; the halving has little to halve. Not a law result.
- **P3 held** (gather cost within ±5%).
- **P4 refuted**: sparse cadence (e=60, 6,000 gs staleness) does **not** separate the arms — the
  missing pair is lost in stock too. The kill-side control failed to kill because the instrument
  (the view) is already failing in stock. A control that cannot pass is a broken instrument.
- **P5 held on completeness and cost**, failed on "slope halves" (unmeasurable at 12.5k gs).

## What would make it wrong

A scene whose demand actually probes the (ld, 2²⁶] band — bodies with legs ≫ the belt's, or a
player closing fast (arrival rate far from 1) — could make the one-leg keep lose emitters stock
keeps; this bench has none (all legs 1,000–1,500 gs, β ≪ 1). The 2 lost emitters' identity is
unattributed (the id-diagnostic was cut for time): if they are fleet members (pushed without a
crossing search) rather than crossing-searched bodies, mechanism 2 is misread. The engine's 2
burn nones are likewise unattributed (guarded `Refused` paths exist in `observe::partial` and
`step`; the census cannot tell which fired).

## Cost of adoption, fit with PRINCIPLES

One line, already written and env-gated (off = the shipped expression); no observable change on
this bench beyond memory. It is **delete before optimize** ("the cheapest compute is compute not
done") and **compute only surprises** — retention is supply the demand never reads. Against it:
the saving measured here is 8%, not the ratchet's halving, and Julien's word is that gates judge
representations, not sizes — the honest adoption case is c7a6's (channel 2 of the ratchet),
which this run flight-proves safe, not cheap.

## The lens (SpaceX) and what it missed

The idiot index sent me to the retention supply (2× the demand); the flight says the *view's own
search* is the worse part (two emitters dead at every gather, keep-independent) — delete/fix
that first, and the keep question becomes pure memory arithmetic. The lens's blind spot bit once:
I nearly certified with digests, and the wall coupling would have made a same-digest claim
fabricated luck. What the lens missed: it prices bytes and misses readers — the demand side is
about **who reads**, and the two missing emitters are exactly the question I did not finish
(whose reads die).

## Next (one experiment)

Attribute the 2 missing emitters (log the missing ids at the first loss gather; check fleet
members vs crossing-searched bodies), then the one-line search fix — on `eval → None`, clamp to
the oldest retained binding instead of dropping the emitter — and re-fly: if the fix holds the
view complete, the keep margin's last job disappears and the dial becomes adoptable together
with the fix.
