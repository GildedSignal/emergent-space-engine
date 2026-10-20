# Dossier — 20261020-1815-inversion-9ff5 (inversion lens)

## Claim

On the time axis no run had flown — 34 eras / 954k game-s of the shipped 5e4 belt (≈ 20 min
of Julien's play at rtf 400, 3.6× the record's 267k-gs horizon; the N-ladder gate itself flew
2k gs and never met the comb) — the belt's era wall is **permanent** (3.72 kick+boundary
events/body/era, flat ±2% through era 33), its **live memory does not grow with play**
(counting-allocator baseline 242.8 MB ±0.4 from era 1 to 34; no ratchet), and the two
young-universe phenomena the page composes with both **age out**: comb concentration
self-softens −73% by era ~12 then floors at ~27% of era 1, and the held-scan (answer)
channel collapses from its era-6–12 peak to ~0 by era 15.

## Bottleneck

The board's memory-at-10⁹ line and every nladder-page 1e9 composition extrapolate constants
measured within 8–9.5 eras. This run flies the horizon itself. What it deletes: the
"memory that grows with play" failure mode for the coasting live belt (cleared, at 5e4,
3.6× deeper than 470f's 40k-gs flat path), and the unmeasured "forever" in a31c's
"alternating forever" (now measured flat). What it bounds: the stagger's required coverage
(~10–12 eras from birth, after which the engine's own kick noise has spread arrivals to the
floor) and 9ed1's answer-channel alarm (a young-universe transient on this scene: held peak
584 at era 9 → ≤20 from era 15 on; the 2048 latch never approached).

## Evidence

Shipped bits plus one print-only example (`crates/universe/examples/longflight.rs`, the
`nladder` loop without the 55-s cap, a counting GlobalAlloc, /proc RSS, one CSV line per
wall second; `ES_SEED` dial, default 1 = the shipped seed). All commands ≤ 6 min:

```
cargo build --release -p emergent-universe --example longflight
B=$CARGO_TARGET_DIR/release/examples/longflight   # /home/glmlab/lab-target-3/...
$B 50000 coast 75  1800 > work/control-c0.csv 2> work/control-c0.err   # 4.3 eras, 34 s
$B 50000 coast 556 1800 > work/long-a1.csv     2> work/long-a1.err     # 34.2 eras, 290 s
ES_SEED=2 $B 50000 coast 100 1800 > work/seed2-s2.csv 2> work/seed2-s2.err  # 5.6 eras, 59 s
python3 analyze.py work/long-a1.csv 50028   # fixed ±3.5k comb windows (the shear lesson)
python3 eras.py     work/long-a1.csv 50028   # full 27,900-gs era bins (the honest read)
```

**A1 (seed 1, 5e4 coast rtf 1800, 953,988 gs = 34.2 eras, 6.24M comb events):**
- Stream: 3,134,145 kicks + 3,107,741 boundaries; per full era bin 3.46–3.81 k+b/body,
  **no trend** (era 1: 3.81; era 20: 3.53; era 30: 3.74; scatter ±2%, seed-2 draws
  3.93–4.20 in its 5 eras — a belt-draw level shift, same flatness). The wall is not a
  birth transient.
- Memory: baseline (quiet-third min per era) 242.1–242.9 MB eras 1–33, **flat**; era 0
  pays the first-kick mint **+113.9 MB live = 2.28 KB/body** (seed 2: 122.4 MB, 2.45;
  9edc's ~2.1 KB/mint, one mint per belt body); mint transients per comb +3–15 MB pruned
  back within the era (live_pk ≤ 270.8). `cat_live` 50,076 constant, dead 0, bpb
  1,393–1,440 band, rss_end 254 MB, no truncation (guard 1.7 GB never approached).
- Concentration: peak-window events 47,662 (era 1) → 15,088 (era 10) → **12.3–13.1k flat
  eras 20–33** (−73%, floor ≈ 27% of era 1). Mass center shears +1.0–2.2k gs through era
  15, then recenters (~0 by era 32): spread without unbounded drift. My own fixed ±3.5k
  windows initially read this as "arrivals decay 1.23 → 0.48 by era 16 and cost halves"
  — **pure window artifact** (era totals flat), the same reading the record's "−26% by
  era 8" decay language risks; crest-anchored detection (ca63's argmax) is the cure.
- Cost: ship-class served µs/event per era 16.0–17.3 (eras 1–10) → 17.2–18.4 (eras
  22–31): **≤ +10% drift over 34 eras**, sub-linear, no cliff.
- Held: peaks 149 → 584 (era 9) → 176 (era 12) → **6–20 from era 15**; held_max 588,
  latch 2048 never engaged. Encounters 46,299 total, front-loaded the same way.
- Worst frame (drain regime, rtf 1800): 12–19 ms all eras — the 12-ms budget latch holds;
  the 0.3–2.4-s gulp class needs play-cadence delivery and is NOT re-measured here.

**S2 (seed 2, 5.6 eras):** baseline 242.3–242.8 MB flat, peak-window 43.3k → 23.1k,
cost 16.5–17.1, held peak 458, worst 18.0 ms, dead 0 — same laws at a different belt draw.

## Predictions

`predictions.md` was written 18:25 (file mtime), after C0 (18:23), before A1 launched. **P1's kill bar fired** (the
finding): average growth over eras 20–33 ≈ 0.0 MB/era (baseline 242.8 ± 0.4) against the
pre-registered "ratchet ≥ 2 MB/era" — the failure mode is cleared, not confirmed; knowledge
by subtraction. **P2 refuted in mechanism, held in letter**: fixed-window era-30 arrivals
0.45–0.50 ∈ [0.4, 0.8], but the honest era-binned reading shows no mass decay at all —
shear + spread, not a dying comb. P3 held (+10% ≤ ±25%; no +50% monotone). P4 held (no
monotone climb; the collapse was unregistered). P5 held (cat constant, dead 0, bpb band).
P6 held (rss ≤ 270 MB).

## What would make it wrong

- **Delivery coupling (the biggest caveat, disclosed):** rtf 1800 runs the budgeted-drain
  regime in permanent deficit (lag ~29 s); worst-frame columns measure the drain ceiling,
  not the 0.3–2.4-s gulp class, and held-scan counts are budget-path (470f's bimodality).
  The held collapse runs *against* the deficit bias (deficit should hold scans longer, not
  shorter), so I read it as real demand decay — but a play-cadence (rtf 400) long flight
  is the missing confirmation, ~29 min wall.
- Scale: 5e4 only; the ratchet and the floor could differ at 3e5 (9ed1's answer bills
  scale with N) and at 1e9 with the compact belt wired (promotion mints are a different
  stream). Coast only; burn adds the nested-pull class. One box, Linux/x86, orders of
  magnitude.

## Cost of adopting / fit

Nothing to adopt in the engine: this is a bounds measurement on shipped bits. It re-prices
two standing adoptions (stagger coverage ≈ 10–12 eras; the answer channel's alarm is
young-universe) and corrects one record ("decay" → shear + invariant mass). PRINCIPLES:
"Measure before claiming" and the test-ladder's extremes — the horizon was the unclimbed
rung; also #21 "rough first, refine when a certificate could break" (no certificate broke
at 34 eras: zero refusals, zero deaths, digests not compared across arms — within-run only).

## The lens

Inversion asked how the engine fails at 10× the flown horizon. What it may have made me
miss: I did not invert the *player* (coast only, one burn-less scene; the player's
causality-driven kick waves are the untested axis), and my first instrument (fixed windows)
reproduced the record's decay misreading before the era bins corrected it — a reminder that
the lens's own tool can share the target's bias.
