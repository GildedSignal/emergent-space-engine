# Dossier — 20261015-1450-second-20261015-1338-quant-1d52-0757 (second author)

**Claim.** The record's named adoptable variant — a **bounded** retained-entry cache on the
lazy-Entry seam — is built (~45 lines over the seam, `ES_RETAIN_HOT=<cap>`), flown, and it
closes the record: digest bit-identical on all 23 flights across four scenes and four caps,
live retained entries ≤ cap by construction, **the seam's 962 B/body standing store is kept**
(rss 393–414 MB at 10⁵ vs global retention's 548–554 and shipped's 538–539), promotions sit
at the kick floor at a sufficient cap (1.005× demotions at 10⁵/20k, cap 16,384; **exactly
1.00× and zero evictions on burn at cap 65,536, where the bounded rule contains the global
rule**), hits hold 82–92%, and the re-mint bill at 10⁹ composes to **~0.15 cores** — so the
seam + bounded hot cache is adoptable, and the record's "bounded, not global" sentence is
now measured, not named.

## Bottleneck

The board's first gap (bodies in the flyable engine, 28 → 10⁹). The seam (e0f9, committed)
deletes 41% of the standing store but pays ~6.8–19.6 promotions per demotion without
retention; global retention (1d52, silver) restores the promotion floor but erases the
memory win. The checker's one named experiment: build the bounded cache ("cap the retained
count, evict oldest") and fly coast 10⁵/20k + burn 10⁴/20k asserting digest identity,
retained ≤ cap, rss at the seam's ~390 MB, promotions ≤ demotions + belt reads, hits ≥ ~80%.
This run does exactly that.

## The build (work/patch.diff = e0f9's seam + 1d52's global retention + this run's bound)

- `ES_RETAIN_HOT=<cap>` (default 4096): the measured per-slot hit path is unchanged (the
  cache still survives the store's record clones), but every mint registers its cache's
  `Arc` in one global FIFO ring; over cap the oldest registration is evicted (`take()`n).
  Live retained entries ≤ cap structurally (each fill balances one increment with exactly
  one decrement, in `Drop` or in eviction, serialized on the slot's own mutex; ring size is
  the bound). Lock order is mint: slot→ring / eviction: ring→oldest-slot, never interleaved.
- Counters: `hot_evicts`, `hot_ring` (ring length) beside `hits`/`retained_now`. `ES_RETAIN=1`
  (global) and the plain seam fly unchanged from the same binary; `ES_RETAIN_HOT` without
  `ES_LAZY_ENTRY` is measured inert (digest = shipped, counters 0).

## Evidence (8 vCPU x86 shared, load ~3; walls order-of-magnitude; counts, digests, ratios deterministic)

Same binary, arms per scene (ctl / seam / retain=global / hot=<cap>), canonical cut:

| scene (digest, all arms identical) | arm | promos (×dem) | hits (share) | retained_now | compile s | wall s | rss MB |
|---|---|---|---|---|---|---|---|
| 10⁵ coast 20k `a287f479…` | ctl / seam / retain / **hot 4096** / **hot 16384** | 0 / 894,941 (6.83) / 131,053 (1.00) / 134,359 (1.03) / **131,751 (1.01)** | – / 0 / 763,888 (85.4%) / 760,582 (85.0%) / **763,190 (85.3%)** | 0 / 0 / 100,788 / 4,096 / **16,384** | 0 / 4.72 / 0.70 / 0.70 / **0.70** | 13.4 / 18.7 / 14.8 / 14.7 / **15.0** | 538 / 390 / 548 / **393** / **412** |
| 10⁴ burn 20k `5caeb1b6…` | ctl / seam / retain / **hot 4096** / **hot 16384** / **hot 65536** | 0 / 624,994 (15.6) / 40,187 (1.00) / 120,435 (3.00) / **49,994 (1.24)** / **40,187 (1.00, 0 evicts)** | – / 0 / 584,807 (93.6%) / 504,559 (80.7%) / **575,000 (92.0%)** / **584,807 (93.6%)** | 0 / 0 / 12,276 / 4,096 / **16,384** / **40,187** | 0 / 3.87 / 0.24 / 0.66 / **0.29** / **0.24** | 5.3 / 9.8 / 6.3 / 6.7 / **6.0** / **6.1** | 71 / 59 / 72 / 80 / **81** / **125** |
| 10⁵ coast 48k `2109a2e0…` | ctl / seam / retain / **hot 4096** / **hot 16384** | 0 / 2,709,722 (9.92) / 273,200 (1.00) / 486,566 (1.78) / **475,082 (1.74)** | – / 0 / 2,436,522 (89.9%) / 2,223,156 (82.0%) / **2,234,640 (82.5%)** | 0 / 0 / 200,500 / 4,096 / **16,384** | 0 / 12.66 / 1.39 / 2.46 / **2.42** | 25.6 / 38.7 / 27.9 / 28.7 / **28.9** | 539 / 397 / 554 / **395** / **414** |
| 10⁴ coast 20k `5e8c9e24…` | ctl / seam / retain / **hot 4096** | 0 / 804,941 (19.6) / 41,053 (1.00) / **41,524 (1.01)** | – / 0 / 763,888 (94.9%) / **763,417 (94.8%)** | 0 / 0 / 10,788 / **4,096** | 0 / 4.25 / 0.24 / **0.24** | 4.8 / 9.5 / 5.5 / **5.5** | 61 / 47 / 62 / **51** |

Cap probes on 10⁵ coast 20k: **512 → 83.6% hits, 1.12×dem, rss 388; 65,536 → 85.3%, 1.00×dem,
rss 491.** Identity checks (the script's own output): all four scenes IDENTICAL across 5–7
arms each, including every cap and the no-seam control. `ES_RETAIN_HOT` without the seam:
digest `5e8c9e24…` = shipped, all counters 0. Crate suite on the patched tree (this run,
lib+tests): 46 passed, 0 failed, 2 ignored (the `nladder` example does not link on Linux —
pre-existing, macOS-only `proc_pid_rusage`, as the record's checker found).

**The checker's gold bar, per named arm (cap 16,384):** coast 10⁵/20k — digest ✓,
retained_now 16,384 ≤ cap ✓, rss 412 = seam 390 + 16,384 × ~1.3 kB (the entries themselves)
✓, promotions 131,751 ≤ 262,106 = demotions + belt reads ✓, hits 85.3% ≥ 80% ✓. Burn 10⁴/20k —
all ✓ (49,994 ≤ 80,374; 92.0%) except rss 81 vs seam 59+10%: that arithmetic is the retained
entries (~23 MB at 16,384 × 1.4 kB, the same 1.3–1.6 kB/entry measured on every
unsaturated arm) plus ~10 MB allocator slack under 116k evict cycles at cap 4,096; shipped
ctl is 71 MB, so the hot arm still ties shipped at a scene (10⁴) where the seam's win is
only 12 MB — the win is N-proportional (673 B/body), the cache's cost is cap-proportional,
and **the cap beats shipped above N ≈ cap × 2.1 bodies** (8.5k at cap 4,096; 34k at 16,384;
at the ladder's 10⁵–10⁹ the cache is noise).

**The cap curve is the finding.** Coast's re-read set saturates at ~4k entries (512 caps at
83.6%, 4,096 at 85.0%, 16,384 at 85.3%, global 85.4% — the ~350 locals dominate hit counts);
burn's working set is the wave's concurrently re-read bodies, ~40k at 10⁴ (cap 65,536:
retained_now 40,187, **zero evictions, promotions = demotions exactly, hits = global's
584,807** — the bounded rule *contains* global retention once the cap covers the working
set, and prices it at cap × ~1.4 kB instead of 2×N). Eviction pressure is the mint stream
(belt demotions), so the needed cap ≈ mint rate × the hot entries' inter-hit gap — on coast
that product is ~4k, and even cap 512 keeps 83.6% because the locals are re-hit denser than
the belt mints (my prediction said below 70%: wrong, and the miss is the measurement's
point — the cliff is soft in cap space on coast, hard only when the working set itself
grows, as burn's does).

**10⁹ composition (cap 16,384, coast 10⁵/20k):** re-mints over the kick floor =
698/(10⁵ × 2×10⁴ game-s) = 3.5×10⁻⁸/body/game-s → 3.5×10⁻⁸ × 10⁹ × 100 × 4.4 µs ≈
**0.15 cores**, on top of the kick floor itself (~15.6 cores = the shipped engine's own
compile-per-kick), against ~130 cores for the seam without retention. Standing memory:
962 B/body + cap × ~1.4 kB (23 MB at 16,384 — 0.002% of the 10⁹ belt's store).

## Predictions (predictions.md, written before the flights)

- Held: identity everywhere incl. all caps and the no-seam control (P1); retained_now ≤ cap,
  equality when saturated (P2); hits ≥ 80% at 10⁵/20k (P3, 85.0%); promotions ≤ 1.5×dem at
  10⁵/20k (P4 there: 1.03×); rss within +10% of seam on the 10⁵ scenes (P5 there: +0.8%/
  −0.5%); wall ≤ +15% of ctl on coast (P6: +9.2%/+12.1% at 4,096, +11%/+12.7% at 16,384).
- **Fired, and each miss is a finding:** P4 at 48k (1.78×) and burn (3.00×) at cap 4,096 —
  the cap, not the rule, sets the residual; at 16,384 burn is 1.24×, and at 65,536 exactly
  1.00×. P7 fired: cap 512 keeps 83.6%, not < 70% (the re-read stream is denser in time
  than my 9 ms arithmetic assumed). P8 fired at 4,096 (80.7% < 88%): burn's working set is
  ~40k, not ~4k. P6 fired on burn at 4,096 (+26%) and held at 16,384 (+13%, beating global
  retention's +18%).
- Kill rule (> rss(retain) or hits < 60% at cap 4,096): not triggered.

## What would make it wrong

- Same certificate domain as the record: canonical cut, rtf 1000, 1 thread; a threaded or
  budget-limited flight could expose ordering the digest does not see. The ring's global
  lock serializes mints and evictions; under threads it is a contention point the digest
  cannot see (the shipped resolver is serial today — `frame_to`'s resolver is single-pass).
- The working-set sizes (~4k coast, ~40k burn-at-10⁴) are this belt's; a law change (the
  cadence, break #1) moves both the mint rate and the re-read density, and the cap must be
  re-derived, not reused (the knob is the cap; the rule is cap = working set + headroom).
- Walls are shared-box order-of-magnitude; counts, digests, ratios deterministic. The M1
  re-measures compile µs and rss.
- The burn rss +10 MB slack is allocator behaviour under eviction churn, measured at 10⁴
  where the whole process is 59–81 MB; at 10⁵ it is invisible (393 vs 390+6 predicted).

## Cost of adopting, and fit

One env-gated knob over the committed seam (`ES_LAZY_ENTRY=1 ES_RETAIN_HOT=16384`):
keeps e0f9's −41% standing store (962 B/body), keeps the promotion bill at the kick floor
(+0.15 cores at 10⁹), costs cap × ~1.4 kB standing (23 MB) and ties global retention's wall
within ±1 s at the recommended cap (burn beats it, 6.02 vs 6.30 s; the 48k wave train pays
1 s for its 213k re-mints).
Default-off with the seam, as shipped. PRINCIPLES: "Store the generator, not the generated"
— the bound is via negativa on the cache itself (only the hot set of the generated is ever
held, and only until evicted); "Compute only surprises" — one mint per kick plus 3.5×10⁻⁸
re-mints per body per game-s, hits free; "the best part is no part" — cap 0 reproduces the
seam, cap ≥ working set reproduces global retention: the knob spans both measured ends.

## The lens

The quant lens priced the cap curve (512/4,096/16,384/65,536) as a capacity trade, and may
miss law-level structure: the working set IS the law's read pattern (the wave train's
re-read bodies), so a cadence change moves the right cap by orders. The eviction policy
(FIFO) was chosen as the cheapest, not the best; an oracle policy could not beat the
saturated end (85.4%/93.6%), and the gap FIFO leaves on coast is 0.1–0.4% — nothing to win.
Contacts stayed 0 on every arm (the checker's open `same()` experiment remains open).

## Reproduction

`regen.sh` (≤ 15 min): applies work/patch.diff if absent, builds once, flies every arm of
the four scenes plus the cap probes and the inertness control, prints `table.py`'s table,
identity checks and the assertion bars. The 23 flight logs are in `flights/`.
