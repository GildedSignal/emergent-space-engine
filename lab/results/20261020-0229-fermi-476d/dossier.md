# Dossier — 20261020-0229-fermi-476d (fermi lens)

## Claim

The wave-excess "×2.37 per ×2 K" law (2d26, composed to 1e9 as coverage 6×10⁻⁵) is **not a
law**: the full-window excess has ±46% flight-to-flight spread at the same rung and scene
(2d26: 15,686 ms; this run: 22,866 ms at 2e5; both instruments agree at 1e5 to 0.5%), and it
conflates two channels with different exponents — a near-linear crest (the burn's synchronized
arrival burst, the stagger's target) and a super-linear memory tail (α ≈ 1.9, the scan channel
the TTL fence already deletes). The stable physics inside the burst: **arrivals per body FALL
with K (1.26 → 1.13 → 1.02 at 1e5/2e5/3e5) while per-kick over-budget cost RISES +18% per
doubling (36.8 → 43.5 → 51.0 µs, ≈ K^0.18, doll-depth memory)**.

## Bottleneck

Board item 1 (bodies: 28 against 1e9) and the smoothness question: 2d26's coverage table
decides which wave exits ("prepay ≤1e5, amortize ≤3e5, only the stagger scales") and prices
the wave at 1e9. If the law's unit is unstable and two-channels, the 1e9 row is order-of-
magnitude only and the exit ranking needs re-anchoring on the crest, not the blended window.
This run deletes the ×2.37 composition as evidence (it was hours old, today 01:43) at the
cost of 6 flights.

## Evidence (all: shipped `nladder` burn scene, seed 1, rtf 2000, 12 ms, this box, load 0.25;
instrument = my own print-only patch — per-frame CSV + wave decomposition — and a Linux
/proc footprint stand-in for the macOS probe, both disclosed; engine code untouched)

Reproduction (dossier commands in `regen.sh`, ~5 min):

- 1e5 full window: excess **6,651 ms** vs 2d26's 6,619 (+0.5%); ebb 2,098 vs 2,046; max 816.4
  vs 812.6; p99 161.7 vs 160.5; over 107 vs 108. Onset 456 vs 458.
- 3e5 (held out): max **2,854.4 ms** vs cc9d-checker's 2,840.8 (same law reading);
  excess(wave-1 zone) 15,578; RSS 1,427 MB; first_over 468 = onset directly.
- 2e5 s=17 full window: excess **22,866 ms** vs 2d26's 15,686 (**+46%**), over 120 vs 110,
  max 2,808 vs 1,652 — same scene, seed, rtf, budget; the rung's wave integrals are
  schedule-elastic. (This flight peaked at 2,758 MB — the 2 GB cap was not enforced this
  time; the 3e5 long arm was NOT flown for that reason and 4e5 is unflightable: the scan
  channel walls before the game-time-locked onset at gs ≈ 15k.)

The two-channel split (fixed frame windows, not onset-relative — onset itself drifts
452↔542 across same-rung flights):

| zone | 1e5 | 2e5 (s10) | 2e5 (s17) | 3e5 | exponent per ×2 K |
|---|---|---|---|---|---|
| wave-1 [440,600) | 4,633 | 9,814 | 15,231 | 15,578 | ratio 2.12–3.29 (α 1.08–1.7, ±22% same-rung) |
| tail [600,1020) | 2,019 | 0 (window) | 7,639 | 0 (window) | 2,019→7,639 (α 1.92) |

2d26's 2.37 anchor = crest (α noisy ~1.1–1.3) blended with the tail (α ~1.9, present in
longer windows only). The tail lives at gs 20k–34k in small over-frames (20–37 per 100) —
the era and shape of the held-scan channel (7b6f: scan 82–100% of the wall there; TTL fence
takes it to 0 from gs 18k), not of the arrival burst. The crest at 1e5 is flight-stable
(4,633 ↔ 4,568, ±1.4%); at 2e5 the drain is budget-schedule-coupled (overruns of 1.7–2.8 s
single frames) and the integral spreads ±22%.

Mechanism (wave-1 zone, `stats.kicks` deltas): kicks/body 1.26 / 1.13 / 1.02 (**falling**,
−10%/rung — cc9d's "0.16–0.17 kicks/gulp" is the worst-frame ratio, not the burst total);
over-budget µs per kick 36.8 / 43.5 / 51.0 (**rising** +18%/rung). The super-linearity that
remains is per-kick memory depth, not arrival count; the burst's arrival physics is
sub-linear in K.

Composition consequence (ebbing K-flat ≈ 2,070 ms, rtf 2000): coverage(1e9) = ebb/excess
spans **1×10⁻⁵ … 1×10⁻⁴** across the measured exponents and instruments (2d26's 6×10⁻⁵ is
one draw inside that span; crest-only α 1.1–1.15 gives 1–2×10⁻⁵ — prepay even deader). The
exit ranking survives qualitatively (nothing flips at 1e6: coverage there is 0.04–0.4 across
the span), but the table's precision claim does not. What does change in kind: the tail does
not need the stagger (the fence deletes it, 7b6f); the stagger's true target — the crest —
is ~K^1.1–1.3 × a falling-arrivals term, i.e. at 1e9 crest-work ≈ 9,750 ms × 5000^1.1 ≈
**1.3×10⁵ s ≈ 32 h one wave at this schedule** (deleted by the stagger, amortized by the
root-stream cure at the budget), with arrivals ≈ 1.02/body falling — the burst is a third
cheaper per body than the 1e5 anchor implies.

## Predictions

See `predictions.md` (written before the 2e5/3e5 arms). Scored: **P1 held** (my full-window
1e5 within +0.5%; matched ratio 2.14 ∈ (2.1, 2.6)). **P2 failed on its letter and its kill
bar did not fire**: measured 1.596 vs registered band (1.42, 1.58) and kill ≥1.62 — the
instrument's ±22% same-rung spread (discovered only with the second 2e5 flight, after the
decisive arms) means the 1.50-vs-1.66 discrimination I designed was not resolvable at ±3%;
the honest statement is the two-channel split, not a point exponent. **P3 half-held,
half-inverted**: kicks/body ≤ 0.18 held (1.02–1.26, and falling — stronger than predicted),
µs/kick ≤ 65 held (36.8–51.0), but "both flat" is false — the per-kick rise (+18%/rung) is
the measured residue of super-linearity. **P4 held in substance** (coverage(1e9) recomposed:
1–2×10⁻⁵ crest-only; the boundary rows move less than one rung). **P5 held** (3e5 completed
600 frames under 2 GB; the crest fits inside the window: cum flat after onset+39).

## What would make it wrong

- My 2e5 s=17 arm ran under late-flight memory pressure (RSS 2,758 MB); if the wave-1 zone
  itself (frames 440–600, RSS then ~1–1.3 GB) was materially slowed by pressure, my 15,231
  is inflated and the crest exponent leans lower than reported. The s10 arm (9,814, no
  pressure) brackets it; the true crest α is inside 1.08–1.3, which the claim already spans.
- The tail's α (1.92) is a two-point estimate (1e5, 2e5) with one point cross-instrument
  (2d26's 15,686 for the full window); a fence arm or a 3e5 long flight (unflightable here
  at 2 GB) would pin it. If the tail is NOT the scan channel, the "fence deletes it"
  attribution (7b6f's, cited) is wrong — my flights show the era/shape match, not the
  deletion.
- Onset-relative statistics are unreliable (onset drifts 452↔542); everything above uses
  fixed frame windows anchored on the game-time-locked burst zone.

## Cost of adoption

None in code: the patch is print-only (example file). The cost is to 2d26's table: the
coverage rows demote from "measured law composed to 1e9" to "order-of-magnitude span", and
any future wave exit must anchor on the crest with an ensemble of ≥3 flights per rung
(the ±22% same-rung spread is the new instrument floor).

## Fit with PRINCIPLES

"Measure before claiming" and "a failed expectation is not automatically a failed method":
the ×2.37 was one draw of a noisy, conflated instrument; this run measures the noise and
splits the channels. "Fat tails: judge behaviours over many seeds … never trust an average
where tails decide" — the wave IS the tail, and it needed more than one flight per rung.
"Error type over error size": the correction here is about which channel carries the
exponent, not the third decimal.

## The lens

The Fermi estimate said saturated arrivals ⇒ ×2 per doubling; measurement said the unit
itself was unstable — the estimate could not see schedule coupling in the drain. What the
lens did catch: the anchor pair (6,619 / 15,686) mixed windows and channels, which a
first-principles re-derivation (crest = arrivals × cost, both measured flat-to-mild) flagged
before any flight. Missed by the lens: the per-kick memory-depth term (K^0.18) has no
place in the arrival picture and was found only in the data.
