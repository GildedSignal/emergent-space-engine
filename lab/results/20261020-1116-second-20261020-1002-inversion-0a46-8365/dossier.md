# Dossier — 20261020-1116-second-20261020-1002-inversion-0a46-8365 (second author on 0a46)

## Claim

The checker's named experiment, flown whole, **inverts 0a46's mechanism**: the 3×
cost alternation on identical arrivals is not the served path (no gulp, no latch) —
it is the **payload of the comb itself**: each belt ship's clock ticks every ~27.9k
game-s (one shared power-of-two fictitious tick) and emits a **kick comb and a
boundary comb exactly half a period apart**, so the "1.1 ev/body every 13.9k gs"
standing comb is two alternating combs — identical arrivals, **~46 µs/kick vs ~8.6
µs/boundary**; and a birth phase-stagger of one comb width **deletes the arrival
concentration and with it the burn freeze (718–1231 ms → 40.6 ms, no new stream
cost) but cannot equalize the era walls**, because the payload alternation is
per-ship structure, not phase.

## Bottleneck




Board #1 (bodies in the flyable engine) and PRINCIPLES #12 (smoothness, the p99):
0a46 left the nladder page with a "measured 3× served-path lever" ("make era 1 serve
like era 2") and a re-specified stagger target. Both are re-priced here: the 3× is
payload, so no scheduler can buy it; the freeze is the only path channel (the
player's nested pull), and the stagger kills exactly that one. The 1e9 arithmetic
gains the payload row: per 27.9k gs the belt costs ≈ 1e9 × 46 µs (kick comb, ~12.8 h
— ca63's 13.2 h is the kick comb, not "the" wave) then ≈ 1e9 × 8.6 µs (~2.4 h),
alternating forever.

## Evidence

Shipped bits (`nladder`, L8 burn/coast, 12 ms, rtf 400, seed 1), my patch
print-only + env-gated (`ES_FRAME_CSV=1`: per-frame CSV adding the Stats deltas —
items and wall-ns by class [planet, moon, ship, player, fleet]; `ES_STAGGER_GS=W`:
each belt ship's FIRST clock interval stretched by a deterministic id-hash offset
uniform over W game-s — ships only, the player and every re-synchronisation shipped;
off = shipped bits, `threads` default 1, so every ship item is a sequential
`resolve_entity`). Anchor (CSV off): max_ms 906.5, held 1813 — inside the record's
family (811–948). 

Regeneration note: `regen.sh` re-flies everything (no CSV reuse, ~3 min, exit 0;
`regen.log` in this folder). Wall-clock columns are shared-box draws — the re-flown
M1's era-1 freeze read cn3 3.56 s and the anchor 830.8 (906.5 the first draw; both
inside 811-948) — while every count reproduces: era kicks
105,780/6,131/104,933/5,905 and boundaries 5,924/105,565/6,020/102,949 (±0.1% of
the table below), era arrivals ±0.003, coast cn3 flat 0.46-0.49. The CSVs in
`work/` are the re-flown ones; the first draw's 1231-ms freeze is quoted as the box
family (712-1231 across the record incl. 0a46's 718 and its checker's 712.7).

**M1/M2 — the payload alternation (the checker's "why is era 2 clean"):**

| era (gs) | ev/body | kicks | boundaries | wall s | cn2 s | cn3 s | held~ | rss MB |
|---|---|---|---|---|---|---|---|---|
| burn 12–16k | 1.117 | **105,779** | 5,924 | 8.7 | 2.15 | **6.23** | 2 | 479 |
| burn 26–30k | 1.119 | 6,173 | **105,627** | 2.2 | 1.39 | 0.68 | 115 | 1494 |
| burn 40–44k | 1.108 | **104,897** | 5,888 | 5.8 | 3.56 | 1.86 | 200 | 1887 |
| burn 54–58k | 1.088 | 5,905 | **102,950** | 1.8 | 1.43 | 0.01 | 246 | 1887 |
| coast 12–16k | 1.110 | **104,925** | 6,094 | 5.6 | **4.85** | 0.47 | 66 | 484 |
| coast 26–30k | 1.122 | 6,355 | **105,809** | 1.6 | **0.93** | 0.46 | 0 | 485 |
| coast 40–44k | 1.024 | **96,365** | 6,070 | 5.2 | **4.38** | 0.47 | 68 | 489 |
| coast 54–58k | 1.092 | 6,092 | **103,140** | 1.6 | **0.86** | 0.46 | 0 | 490 |

1. **Odd eras are kick combs, even eras are boundary combs**, burn and coast alike:
   ~105k kicks + ~6k boundaries, then ~6k kicks + ~105k boundaries, every 13.9k gs
   (kick combs 12–16k and 40–44k: one 27.9k-gs clock period; the boundary comb sits
   half a period after each kick comb — `kick_clock` inserts boundary at `t+full/2`,
   kick at `t+full`, step.rs:717-718). Era arrivals match 0a46's record to ±0.003
   ev/body (1.117/1.119/1.108/1.088 vs 1.117/1.118/1.110/1.088).
2. **Coast is the clean kill of every path story**: no player gulp at all (cn3 flat
   0.46–0.47 s, it3 = 387±1 items in every era), max frame 12.0 ms, zero over —
   yet walls alternate 5.6/1.6/5.2/1.6 s. The carrier is cn2, the ships' own items:
   **45.9 µs/kick vs 8.6 µs/boundary** (9.23 s / 201,290 kicks; 1.79 s / 208,949
   boundaries) = 5.3×. 0a46's "gulped nested path vs budgeted drain" and the
   budget-latch reading both die: the same bodies, same sequential path, same
   budget, pay 5× more when the comb's payload is a kick (readout + field +
   quantize + rebind) than when it is a boundary (readout + certificate).
3. **The burn freeze is a second channel riding only the kick combs**: M1's worst
   frames (1231/1197/1161/1051 ms) each carry 13.1–15.6k kicks with **it2 = 0** and
   cn3 = the whole frame — the crest served nested inside the player's item
   (`pull_ships`, universe.rs:770), unbudgeted. Era 1's nested service is 86 µs/kick
   (6.23 s / ~72k nested kicks) vs era 3's ~52–63: [INFERENCE] era 1's kicks are the
   belt's FIRST kicks, which always fire and rebind (tube refit); era 3's mostly
   don't fire (dv under the quantum). The freeze size is draw-sensitive (record:
   718/712.7; this box: 1231 — shared machine), the alternation is not.
4. **Held/memory per era** (the checker's ask): held-climb on burn is monotone
   (2 → 115 → 200 → 246), not alternating — the checker's anti-correlation is the
   backlog's birth at era 1's freeze plus its game-time-locked repay, visible as
   35–55 ms over-frames in bins 18–26k and 34–40k of every burn arm **including the
   fully flattened S2** (arrivals flat, bumps unmoved: a schedule-locked channel the
   stagger does not touch). RSS per burn era 479 → 1494 → 1887 MB (the scan backlog
   and its structures); coast flat 484–490.

**S1/S2 — the stagger arm (the checker's "spreads clock phase ≥ the comb width"):**

| arm | max_ms | worst-frame content | crest bins ev/body | 4-bin conc. | era walls s | total wall | ev/body tot |
|---|---|---|---|---|---|---|---|
| off (M1) | 1231 (rec. 718) | 15.5k nested kicks, it2=0 | 0.37+0.75 | 49% | 8.7/2.2/5.8/1.8 | 45.0 s | 5.87 |
| S1 = 4k | **40.6** | cn3-only items, k=0–25 | 0.53+0.55 | 37% | 5.4/1.8/4.9/1.3 | 37.2 s | 5.74 |
| S2 = 14k | **42.0** | cn3-only items, k=4–76 | **0.20 flat** (14k on) | 16% | (flat + repay bumps) | 37.0 s | 5.14 |

5. **The freeze is the concentration's child**: spreading first-clock phases by one
   comb width (4k) already breaks the nested gulp (worst frame 40.6 ms ≈ budget +
   one scan item; over-frames shrink from 144 to 121 small ones); a full-period
   spread (14k) flattens arrivals to the stream's average (~0.20/bin from gs 14k)
   and the concentration falls 49% → 16%. The stream is unchanged —
   kicks/body/gs 4.889e-5 (S1/S2) vs 4.899e-5 (M1) — and total wall **drops 17–18%**
   (the freeze and its aftermath are pure waste).
6. **But no phase spread can equalize the walls**: S1's era walls still alternate
   5.4/1.8/4.9/1.3 (≈3×), because every ship still emits kick … half-period …
   boundary — the payload alternation is structural. Flattening cost needs the
   payloads interleaved across ships (half the belt's clocks offset by half a
   period), or the boundary comb gone (PRINCIPLES #3: a certificate nobody reads is
   the least surprising object in the engine — 105k of them arrive per comb).

## Predictions

`predictions.md` was written before any decisive flight (calibrations disclosed
therein). P1 held on its letter (cn3 explains 85% of era1−era2 wall; nested era-1
frames pure). **P2 refuted on its main branch — and that is the result**: coast's
alternation is cn2 (5.2×) with cn3 flat, exactly P2's branch B (the ships' own
service, no player) — the payload law. P3 split: worst-frame held 18–30× under the
bar (40.6 ≤ 250) and S2's flatness held (max bin 0.208 ≤ 0.35), but S1's max bin
read 0.547 against the ≤0.50 bar and the ≥2× concentration drop did not happen
(1.3×), nor wall equalization — the failures carry the finding (payload structure).
P4 held (−12% events, −17% wall, inside ±25%; identical kick rate). P5 held (anchor
906.5 in 811–948; era arrivals ±0.003; first-crest bins ±0.03 — the mega-frame's
schedule shifts arrivals across one bin edge, disclosed).

## What would make it wrong

- The payload costs are this box's (shared Linux, load ~1, sequential `threads=1`):
  orders of magnitude per the lab rules. The 27.9k period and the kick/boundary
  alternation are bit-structure (the plan's own ticks), not measurements, so they
  survive any box; the 46/8.6 µs split and the 86 µs first-kick cost are x86 draws.
- The stagger arm shifts each ship's first kick grid (first-interval midpoint only):
  bits differ from shipped on S1/S2 by design; it is a probe of the page's re-specified
  target, not an adoption. Off = shipped bits, anchored above.
- One scene, one seed per arm, 60k gs: the decay of the comb past era 8 (5e4, the
  checker's arm) is not re-flown here; nothing in the payload story depends on it.
- The 1e9 rows multiply measured per-item costs by 1e9 with no super-linearity —
  the page's own warning (no single-α 1e9 number) stands.

Cost of adoption: none for the record (re-pricing). Design consequences: (1) "make
era 1 serve like era 2" is dead as a scheduling lever — the 3× is payload; (2) the
freeze lever is confirmed as the nested pull (1d47's gate, ee4d's stream), and the
stagger at birth (≥ one comb width) is its cheapest prophylactic, worth 17% of total
wall at 1e5 before any kick-cost work; (3) the boundary comb (2.4 h/1e9 per period)
is the next cheapest target — it is 46% of the belt's stream events and carries no
kick; (4) a wall-flattening stagger must interleave payloads, not just phase.

Fit with PRINCIPLES: #3 "Compute only surprises" — half the belt's standing stream
is boundary certificates arriving in step; #19 "a fix signals the wrong
representation" — the alternating-cost mystery was two combs wearing one arrival
envelope; #12 smoothness — the freeze dies with the concentration, and what remains
over budget is the scan repay, itself schedule-locked.

## The lens

The second-author lens had the checker's question verbatim ("why is era 2 clean")
and nearly answered it with the budget latch before the coast arm killed that: what
it may have missed is the first-kick rebind share of era 1's nested cost (inferred,
not instrumented) and the repay channel's cost outside the crest windows (measured
as bumps, not decomposed). The stagger's failure half (walls stay alternating) was
not in my predictions' main branch — the checker's design earned it.
