# Dossier — 20261020-0143-library-2d26 (library lens)

**Claim.** The kick wave's three exits are now typed by one measured law — prepay coverage = (pre-onset ebb)/(wave excess), which is cadence-bought and rung-dying: 2.55 at play-side cadence (rtf 400, 2×10⁵) but 0.13 at test cadence (rtf 2000), and 0.34 at 10⁶ even at rtf 400 — so compute-ahead (0c0f's open direction 3) is a ≤10⁵ patch, amortization (ee4d/1d47's drain) covers ≤ ~3×10⁵ and its price is presented-time lag ∝ K, and only deleting the burn's mint-synchrony scales.

**Bottleneck.** The board's #1: bodies in the flyable engine (28 → 10⁶ flown, 10⁹ goal). The page's live decision after 4063: adopt the measured cure (ee4d's stream + 1d47's deferral, burst deleted 58–111×) — at what price, guaranteed how, and does anything still favor prepaying the wave on the idle ebb (0c0f od 3, never priced)?

**Evidence** (all arms the shipped `nladder` burn scene, seed 1, 12 ms, Linux box; the only patch is print-only — an env-gated per-frame trace + the macOS rss probe's /proc stand-in, `work/patch.diff`; timings are orders-of-magnitude, the integrator re-measures on the M1):

| arm (rtf) | p50 | p99 | max | over | onset frame | pre-onset ebb | wave excess | coverage | lag max→end |
|---|---|---|---|---|---|---|---|---|---|
| 10⁵ burn (2000) | 5.74 | 160.5 | 812.6 | 108/1020 | 458 | 2,046 ms | 6,619 ms | **0.31** | 32.0 → 0.0 s |
| 2×10⁵ burn (2000) | 6.07 | 319.5 | 1,652.0 | 110/1020 | 455 | 2,036 ms | 15,686 ms | **0.13** | 32.4 → 0.0 s |
| 2×10⁵ burn (400) | 0.39 | **11.94 = budget** | 1,590.4 | 13/2700 | 2,067 | 20,775 ms | 8,160 ms | **2.55** | 5.5 → 0.0 s |
| 10⁵ coast (2000), control | 8.98 | 11.9 | 11.95 | 0/1020 | none | — | 0 | — | 32.6 → 0.0 |

Laws: excess ×2.37 per ×2 K (6,619→15,686) while pre-onset ebb is K-flat (2,046→2,036 ms; onset is game-time-locked at gs ≈ 15k, so frames-before-onset is set by cadence alone — 458/455 at rtf 2000, 2,067 at rtf 400). Whole-flight ebb no longer repays the wave: excess/total-slack 1.26 → 3.13. The 10⁵/2×10⁵ arms reproduce 0c0f's laws (6.12/150.6/891.8/104/32 and 5.39/380.8/1,675.6/55/32; my over-count 110 vs 55 at 2×10⁵ is the known rerun band) and the rtf-400 arm reproduces 0c0f's checker (p50 0.42 vs 0.43, over 13 vs 13, max 1,590 vs 1,730). The rtf-2000 lag ≈ 32 s is cadence-structural (12 ms × 60 × 2000 = 1,440 < 2,000 game-s per wall-s) — the wave's marginal lag is what recovers to 0.0 in every arm: bounded, never compounding. At play-side cadence the whole wave is **one 1.59-s freeze in 46 s with p99 at budget** — the player-facing disease is a single freeze, not a stutter.

**Commands** (≤ 60 s each; full regen ≤ 15 min: `./regen.sh`):
- `cargo build --release -p emergent-universe --example nladder`
- `ES_FRAME_TRACE=f100000_burn.txt <bin> 100000 burn 18 2000 12` (likewise `200000 burn 18 2000 12`, `200000 burn 46 400 12`, `100000 coast 18 2000 12`)
- `python3 work/analyze.py` + the rtf-400 block; `python3 work/verify_quotes.py`

**Predictions** (`predictions.md`, written before any flight): P1 held (coverage 0.31/0.13 < 1, in band). P2 held at 10⁵ (1.26), **failed at 2×10⁵ by 4%** (3.13 vs band ≤ 3) — the honest reading is stronger than registered: amortization is horizon-bound and the bound shrinks as K grows. P3 held on both letters (lag 2×10⁵ > 10⁵; recovery to 0.0) with the rtf-2000 baseline disclosed as cadence-structural. P4 held (0.48/0.51 ∈ [0.30, 0.65]). P5 held (coast: over 0, max = budget). P6 held (5/5 quotes byte-identical). The registered rtf-100 coverage drop is confirmed at rtf 400 in the good direction: coverage rises as cadence slows (2.55 > 0.13).

**What would make it wrong.** (a) Excess is budget-crossing work, a lower bound: at rtf 400 part of the wave runs inside idle frames (excess 8.2 s vs 15.7 s at rtf 2000), so prepay's true deficit at play cadence is between 0.5× and 1× my coverage — the crossover 4.6×10⁵ could sit nearer 3×10⁵; the ordering (prepay < amortize < delete) is unchanged. (b) One seed, one scene, one box: the excess law's exponent 1.24 rests on two rungs (cc9d's K-law 8.1–9.5 µs/body supports it); a 3×10⁵ rtf-400 arm is the named next flight. (c) If the wave's arrivals were pre-computable one frame ahead (they are: the kick grid is known at mint), "prepay" could mean pre-EVALUATE, not pre-schedule — that is the stagger's twin, and it changes lesson 5's small-N band only. **Cost of adopting:** zero for the decisions (no code change proposed); the drain's adoption (ee4d/1d47) carries the named re-freeze. **Fit with PRINCIPLES:** "Use idle time to compute ahead — yes this is a whole important idea of this project" (OC#36) — the lesson disciplines where the idea pays: the ebb is K-flat, the surprise is K-proportional, so idle time buys constancy, never scale; and "bandaids are basically fixes resulting due to a poor representation" (CL 09-29) — prepay at 10⁶ would be one.

**The lens (what it may have missed).** The library lens reaches for practitioners' quotes after the measurement; it did not wire the stagger (the deletion itself, the only K-scaling exit, stays unflown) and did not test seeds beyond 1 (the shipped harness has no seed dial). The five quotes were chosen to hold decisions, but a dynamics or quant lens might have flown the 3×10⁵ arm instead of the coast control.
