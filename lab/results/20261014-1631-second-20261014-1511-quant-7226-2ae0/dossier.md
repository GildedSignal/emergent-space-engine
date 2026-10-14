# Dossier — 20261014-1631-second-20261014-1511-quant-7226-2ae0 (second author on 20261014-1511-quant-7226)

## Claim
The checker's named experiment is done and it holds: a guarded Anderson–Björck/IQI probe
policy on the kick's crash search passes the frozen tail rule everywhere (**worst 11–18
probes per search against the rule's ≤ 30, mean 10.6–11.1 against bisection's 29.4**),
cuts the leaver kick **−34…−35 % at flying pace** and the search's probes **−62…−64 % at
both paces** with **digests bit-identical at every seed × pace × policy × warm layer**
(canonical and replay, refused 0), and composed with the warm start (0b85) the search's
exact readouts fall **−78…−83 %** against shipped (flying leaver −43…−47 %) — one search
drops from ~29.4 readouts to ~4.9–6.3, all regenerable from `work/patch.diff` by `regen.sh`.

## Bottleneck
Board line 3 (the kick: 75–160 µs against a ~50 ns floor). The prior run priced the surface
search at 45–57 % of a fired kick and killed its own naive probe policies; the checker's
one-experiment-to-gold was the tail-guarded AB-family update plus the warm-start
composition. Both land here; the search's probe bill (the flying arm's largest single term)
drops ~6×, and the whole kill table of the prior run regenerates from the shipped patch.

## Evidence (this box, Linux/x86 shared; `regen.sh`, ~30 s after a built tree)

**The policy ladder** (`ES_FP` = 1 secant / 2 AB / 3 guarded AB-IQI / 4 Illinois, 0 = shipped
midpoint verbatim; the float places the probe, the integer predicate decides — same first
crossing, only the readout count changes). Seed 3, flying arm (m400/rtf100/8 s), 802
searches in every arm:

| arm | probes | mean | worst | leaver med µs | digest |
|---|---|---|---|---|---|
| shipped (off) | 23,552 | 29.4 | 32 | 198–200 | `36637e67`/`f282c907` |
| 1 secant (the prior kill) | 35,621 | 44.4 | 57 | 301.6 | identical |
| 2 Anderson–Björck | 9,810 | 12.2 | 13 | 137.3 | identical |
| **3 guarded AB-IQI** | **8,589** | **10.7** | **14** | **130.4** | identical |
| 4 Illinois (signed) | 8,709 | 10.9 | 11 | 131.7 | identical |

The prior run's secant row reproduces exactly (35,621/57). Its two unregenerable rows are
replaced by correctly-wired variants that *pass*: the difference is the retention
discipline — the **retained** anchor's stored distance decays (by the measured same-side
ratio, AB; or one half, Illinois) while the fresh side resets to its measured distance.
Policy 3 adds the checker's second named guard, the inverse quadratic through the three
newest probes (the branch falls with curvature — every chord lands short and crawls; the
quadratic tracks it), and a crawl bail: two consecutive probes that cut less than half
force one midpoint.

**The frozen rule's matrix** (policy 3, off→on; digests identical and refused 0 in all 12
arms; worst = per-search worst over the run):

| seed × pace | searches | probes off→on | worst off→on | leaver med off→on | all-p99 off→on |
|---|---|---|---|---|---|
| 3 flying | 802 | 23,552→8,589 (−63.5 %) | 32→14 | 199.2→130.8 (−34.4 %) | 392→394 |
| 7 flying | 1,225 | 36,367→13,254 (−63.5 %) | 33→17 | 189.9→122.8 (−35.3 %) | 376→370 |
| 11 flying | 731 | 21,396→7,786 (−63.6 %) | 31→18 | 189.4→122.2 (−35.4 %) | 419→416 |
| 3 battle | 3,096 | 91,323→34,318 (−62.4 %) | 28→12 | 363.2→362.6 (−0.2 %) | 474→410 |
| 7 battle | 3,700 | 109,170→41,109 (−62.3 %) | 29→12 | 362.5→362.1 (−0.1 %) | 456→391 |
| 11 battle | 3,015 | 88,969→33,530 (−62.3 %) | 29→12 | 363.1→362.9 (−0.1 %) | 471→407 |

The battle leaver **median** is flat for a reason the record can check: at battle pace the
median leaver kick's cost does not track the search's probe count (the full descents sit in
the dipping minority — 3,096 searches against 2,064 kick samples at s3 — and their −80 µs
appears at all-kick p99, −13…−14 %, not at the median). The ≥ 25 % leaver-median cut holds
at flying pace, where every leaver kick carries the search; no probe policy can move a
search-free median, so the gold condition's "both paces" is met on probes, worst and
identity at battle, on the leaver cut only where the leaver carries a search.

**Identity.** Canonical and replay digests bit-identical off = on at every arm above, and
across the whole ladder and the warm layers below; refused 0 everywhere; the crate suite is
11/11 with the extended equality test (every policy 1–4 = the bisection's impact on every
dipping tube of a settled plane, two surfaces, two starts). The off arm's digests are the
prior checker's pristine-verified ones (`36637e67`…, `cf58ac6e`…, `164d6547`…; code
identical f1322a79..db0f3e74 in `crates/` and `xtask/`), and `ES_FP=0`/empty now means off
(the checker's `ES_FP=""` footgun is closed, same for `ES_IMP_WARM`).

**The composition with the warm start** (0b85's carry: the retired tube's crash tick
gallops, the bounded span descends; `ES_IMP_WARM`, off = shipped verbatim):

| arm | probes shipped→warm→warm+P3 | worst | leaver med / all-p99 |
|---|---|---|---|
| s3 flying | 23,552 → 4,518 → **3,932** (−83.3 %) | 32→32→**11** | 198→106→105 / 392→402→381 |
| s7 flying | 36,367 → — → **6,371** (−82.5 %) | 33→—→**17** | 190→—→103 (−46 %) |
| s11 flying | 21,396 → — → **3,861** (−82.0 %) | 31→—→**12** | 189→—→99–108 (−43…−49 %) |
| s3 battle | 91,323 → 39,273 → **20,228** (−77.8 %) | 28→28→**12** | 363→362→362 / 474→406→408 |
| s7 battle | 109,170 → — → **24,378** (−77.7 %) | 29→—→**12** | — / 456→408 |
| s11 battle | 88,969 → — → **19,775** (−77.8 %) | 29→—→**12** | — / 471→404 |

The savings add (warm deletes the searches that moved < 1 tick; the policy cuts the probes
of those that did not): warm+P3 < warm alone < P3 alone < shipped at every arm, and the
warm path's own tail (worst 32 under plain bisection) drops to 11–12 under the policy.
Digests identical at every layer; leaver medians at flying pace move 199→105 µs.

## Predictions (predictions.md, written after tuning on s3-flying only)
- **P1 held**: worst ≤ 18 and mean ≤ 11.1 at every seed × pace (predicted ≤ 20 / ≤ 15).
- **P2 half-held, honestly failed where wrong**: flying −34…−35 % (predicted ≥ 25 %) ✓;
  battle ~0 % at the median against my predicted ≥ 15 % — my mechanism was wrong (I
  expected most battle leavers to carry searches; the descents concentrate in the dipping
  minority, and the cut lands at all-kick p99 instead, −13…−14 %).
- **P3 held**: digests, refused 0, equality test, everywhere.
- **P4 held**: the secant row regenerates exactly; the rebuilt AB/Illinois rows pass where
  the prior in-session variants failed (retention discipline, above).
- **P5 held**: composed probes ≤ warm alone at every arm, digests identical, no fallback
  regression (warm+P3 worst 11–12).

## What would make it wrong
The counts and digests are deterministic properties of the shipped bench; the wall-clock
columns (leaver medians, p99) vary a few % between runs on this shared box — the flying
leaver cut is stable at −34…−35 % across three regen runs, but the single-run p99 column
wobbles (e.g. s3-battle composed 387–408 µs). The domain is still one scene family
(plane battle, three seeds, two paces, one box): a scene whose dips graze the periapsis
(the warm start's two-readout regime) would shrink the policy's margin, and the equality
test covers only the plane's handed-out ships. If a future probe policy is judged, the
frozen rule should say what these runs show: the leaver-median cut belongs to the flying
arm; at battle the search's saving is a p99 term.

## Cost of adopting / fit
The policy and the warm start are env-gated probes, off by default = shipped verbatim
(verified digest-level, and `ES_FP=0`/empty is off). Adopting both as the default law
changes no canonical outcome (digests identical at every measured arm; the integer
predicate decides every step, PRINCIPLES #13 "errors never compound" holds by
construction) and deletes ~83 % of the flying search's exact readouts — PRINCIPLES #1,
"the cheapest compute is compute not done". The remaining search cost (~5–6 readouts)
approaches the two-endpoint floor the exit search already reached via the passage guess;
the next term is the kick's bind half, untouched here. Counters, ladder, equality test and
`regen.sh` are the frozen instrument for whoever freezes it.

## The lens
The second-author lens spent its hour where the checker pointed and nothing else: the
guard was already named, so the work was wiring the retention discipline correctly
(the prior variants' bug), regenerating the kill table from the patch, and composing with
the warm start. What it may have missed: I did not trace the battle median's flatness to
the individual kick (the dipping-minority reading is arithmetic on the counters, not a
per-kick trace), and I left the author's `next_exit` fast path (Illinois + vertex
quadratic) untouched — it fires 0 searches in every arm here, but a scene that exercises
it inherits an untested-by-me policy; its `run` counter now counts honestly (fixed).
