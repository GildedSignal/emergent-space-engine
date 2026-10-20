# Dossier — 20261020-1210-taleb-9ed1 (Taleb lens): the stagger's freeze-kill is real but rung-bound; the freeze is a hydra

## Claim (one sentence)

8365's birth-stagger deletes the kick-comb freeze **at every rung flown** (era-1 max 715/1,569/2,430 ms → **12.0 ms flat**, K-flat, through 3e5, seed 2, load-16 and 8 eras) — but it does **not** delete the player's worst frame: at 3e5 a second channel, one held-scan **answer** (100 events, 178 encounters, 1,225 ms ≈ 6.9 ms/encounter vs ~0.1 normal), becomes the maximum, is **not TTL-deletable** (TTL=8: 1,280 ms), and exceeds the *unstaggered* arm's own era-2 worst (375 ms) — so "with it the freeze" (8365) holds only below ~2e5, and the next freeze target is the scan answer's walk, not arrival spread.

## Bottleneck

The board's first gap (bodies in the flyable engine) and the wave's player-facing ruin (one mega-frame). The stagger is the one adoptable fix on the table (8365, gold-checked); whether it survives scale decides adoption. It does — for the channel it targets — and it names the next channel at exactly the rung where it bites (3e5).

## Evidence (this box: Linux x86, 8 vCPU shared; every flight the shipped `nladder` example, burn scene, rtf 400, budget 12 ms, CSV instrument = 8365's patch; fence `ES_SCAN_TTL_S=16` = ca63's gate, a disclosed law change carried by all decisive arms so 2e5/3e5 fit under the 2 GB cap)

| arm | N | seed | stagger | max_ms | worst-frame payload | peak MB |
|---|---|---|---|---|---|---|
| A0 anchor (fence off) | 1e5 | 1 | off | **714.9** | 14,362 kicks (f2142) | 1,887 |
| A1 fence | 1e5 | 1 | off | **727.5** | 14,643 kicks | 549 |
| A2 | 1e5 | 1 | 14k | **43.7** | 30 events, held=1 (repay) | 561 |
| A3 | 2e5 | 1 | off | **1,568.6** | 31,651 kicks, 49.6 µs/kick | 1,009 |
| A4 | 2e5 | 1 | 14k | **91.6** | 128 events (repay) | 1,012 |
| A5 | 3e5 | 1 | off | **2,430.4** | 47,915 kicks | 1,507 |
| A6 | 3e5 | 1 | 14k | **1,225.0** | **100 events, k=4, en=178, held 1→0** | 1,515 |
| A7 | 2e5 | 2 | 14k | **83.7** | 92 events (repay) | 1,006 |
| A8 load-16 | 1e5 | 1 | 14k | **351.5** | 1,635 events (drain), no comb batch > 1,852 | 560 |
| A9 8 eras (300 s) | 1e5 | 1 | 14k | **46.4** | repay; hot-bin share **decays** 21.6→14.9% | 652 |
| A11 TTL=8 | 3e5 | 1 | 14k | **1,280.4** | same object; tighter fence does not delete it | 1,582 |

Era maxima (kick combs are eras 1/3 at gs ~13.9k/41.8k, period 27.9k):

| era-1 (kick comb) max | off | stagger 14k |
|---|---|---|
| 1e5 | 714.9 ms | **11.9 ms** |
| 2e5 | 1,568.6 ms | **12.0 ms** |
| 3e5 | 2,430.4 ms | **12.0 ms** |

- **The kick-kill is a law, not a coincidence:** era-1 max = the 12 ms budget at every rung; arrivals flat (full-period hottest 1k-gs bin 21.6% at 1e5, decaying to 14.9% by era 8 — no re-concentration through 120k gs); seed 2 same; under load-16 the biggest single batch is 1,852 events (vs 14,362+ unstaggered idle), the worst frame being drain-under-contention at ~215 µs/ev, not a comb.
- **The freeze is a hydra.** With combs flat, the maximum regrows through the scan channel: 43.7 → 91.6 → 1,225 ms at 1/2/3e5 (era 2, the boundary comb's repay window). At 3e5 the worst frame answers one held scan: `en=178` encounters, ~1 ms class-attributed, 1.2 s wall — the exact player-neighbourhood check's **walk**, [INFERENCE] proportional to the doll population at answer time, not to its 100 events (6.9 ms/encounter vs ~0.1 in normal answer frames like f72–75: 121 encounters at 10.7 ms).
- **Not staleness, not memory:** TTL=16→8 keeps the object (1,280 ms; held_max drops 205→141, peak MB unchanged); the fence deletable part was only the tail channel (ca63), never this.
- **Not masked by the comb:** unstaggered era-2 worst is a 28k-boundary batch at 375 ms (A5 f4224); the staggered arm's era-2 worst (1,225 ms) is **3.3× worse** — at 3e5 the stagger trades a 2.4 s kick freeze for a 1.2 s answer freeze; the player eats a freeze either way.
- Stream cost unchanged where windows match: kicks/body/gs 4.889e-5 anchor vs 4.890e-5 staggered at 1e5; at 120–130 s windows the stagger defers 12–26% of arrivals out of window (8365's P4), disclosed per arm.

Reproduce: `bash lab/results/20261020-1210-taleb-9ed1/regen.sh` (~12 min; builds the patched example, re-flies all 11 arms, reprints every number above from `work/*.csv`).

## Predictions (all pre-registered in `predictions.md` at 12:24, before A1–A11; anchor A0 flown before, disclosed there)

P1 held (727.5 ≥ 400: the fence does not eat the freeze). P2 held (43.7 ≤ 120). P3 held (1,568.6 ≥ 900). P4 held (91.6 ≤ 250: **the kill scales at 2×**). **P5 half-held, kill bar fired: A5 2,430.4 ≥ 1,500 held, A6 1,225.0 ≥ 800 — the freeze re-forms at 3× through the scan-answer channel; this failure is the finding.** P6 held (83.7). P7 failed on its letter (351.5 > 300) without the kill bar (< 600): under load the repay frames cost ~8× idle, but no comb re-concentration (max batch 1,852 events). P8 held (46.4 ≤ 150; no era ≥ 45% hot-bin; the share decays).

## What would make it wrong

The stagger gate touches only ship first-clock synchronisation (step.rs, 8365's patch, off = shipped bits); if the 3e5 answer freeze is an artifact of the fence (the fence drops *other* scans, changing which scan answers last), A11's TTL=8 arm argues against it (the object persists at both TTLs), and A5's unstaggered era-2 shows the same repay shape at 375 ms without any stagger. What is [INFERENCE]: the walk's proportionality to doll population (not measured directly — items_by_class shows 1.04 ms attributed; the rest is outside the class costs). If the exact check is O(candidates) with candidates ∝ N, the fix is the already-built-but-unwired encounter tiers (HANDOFF §3), not arrival spread.

## Cost of adopting, and fit with PRINCIPLES

Adopting the stagger (a birth-phase law change: every recorded flight digest changes) buys: era-1/3 mega-frames gone at every scale, era walls unchanged (8365), and the honest next target exposed. It costs nothing in stream (same kick count per period) and ~0 in per-event price. "Before removing a fence, why was it built" (Taleb lens): the comb is *birth synchrony*, an artifact of minting every belt ship at t=0 — the stagger removes the artifact, not a behaviour. Fits P1 (compute only surprises — the comb is our own synchrony, not physics), P12 (smoothness: the p99/player-facing max), P20 (behaviours over many seeds and rungs — this run's whole point). The scan-answer channel it exposes is the board's encounter-work question in the plane's own clothing.

## The lens (what Taleb may have made me miss)

The lens hunts fragility and found one, but it under-weights the positive result: the kick-kill's *robustness* (budget-flat at 3×, load, seed, 8 eras) is itself the adoptable fact, and a speed-focused lens would have stopped at 2e5 satisfied. Missed by construction: whether 4e5–5e5 (unflyable here under 2 GB even fenced — 2.1+ GB) reshapes the answer channel again, and the M1's thermal behaviour at these arms.

## Grade asked: silver (one named experiment from gold)

The named gold experiment: **fly the scan answer's walk directly** — instrument the exact player-neighbourhood check (encounter.rs) with its candidate count and doll population at answer time across 1e5–3e5, one freeze frame and one normal frame, and price the two built fixes: incremental answering (pay per frame at budget) and the encounter tiers' candidate set. If the walk is O(doll population), the freeze at 10⁹ bodies is ~an hour in one frame — the allocator's true ruin — and that, not the combs, is the smoothness gate at scale.
