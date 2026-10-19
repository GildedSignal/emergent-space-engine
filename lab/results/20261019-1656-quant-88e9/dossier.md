# Dossier — 20261019-1656-quant-88e9 (quant lens)

## Claim
The cadence split (`BELT_SPLIT`, the belt's measured 8× CPU lever) is also a memory lever, and its
memory ratio is the **bulk's share of the kick stream**, not the split factor: the history ratchet's
post-onset slope *is* the total kick-mint stream (measured 96.1% of it on OFF), so the split divides
the ratchet by 1.76× at 3×10⁴ (the belt is 42% of the stream there), by 2.6× at 10⁵, 6.3× at 10⁶,
and by S = 8.0× only at 10⁹ where the belt is 99.99% of the stream — and on the compact side the
same law gives τ (0659's residency dwell at p = 1.0) ×8 for free.

## Bottleneck
Board item 1 (bodies: 10⁶ → 10⁹) and item 4 (memory): the history-ratchet channel 2 (nladder's page,
f80a/b911) is the live-plane memory wall; the split is the cadence lever already measured legal.
This run prices one lever on the other market. Deletes nothing yet; it re-prices the split's
adoption case (CPU + memory on both sides of the wiring) and kills the naive "slope ÷ S" reading
before someone adopts expecting 8× at today's rungs.

## Evidence (all from this run's flights, main 9b0fdb9b + patch.diff)
Binary: main + f80a's probes verbatim (print-only + `LADDER_RSS_MB` guard; their OFF digits
reproduce: hist_total 240,354 at 174k gs vs f80a's 241,552, gt1 30,065 vs 30,064 — the instrument
match) + the split re-derived from f790's patch (env-gated `BELT_SPLIT`; f790's checker verified
off ≡ shipped byte-for-byte). Scene: shipped `nladder 30000 burn <s> 2000 12`, seed 1, 48 members,
1 thread (f80a/527a's arm). Full logs in `work/`.

| arm | game-s | hist slope/1k gs (140–245k) | RSS slope/1k | RSS @245k | kicks/gs | over 12 ms |
|---|---|---|---|---|---|---|
| OFF (shipped cadence) | 249k | 2,432 | 4.06 MB (f80a: 4.19) | 1,253 MB | 2,530 | 213 |
| ON (`BELT_SPLIT=1`) | 277k | 1,380 | 2.18 MB | 945 MB | 1,589 | 175 |

1. **The mint law.** OFF post-onset hist slope 2,432/1k gs vs its own kick stream 2,530/1k gs
   (96.1%); ON 1,380 vs 1,589 (86.8%; ON's onset is later — its first wave lands 110–125k, belt
   bodies' keep windows are younger in the matched window). Every kick mints one binding; after
   onset the keep law retains them all: **the ratchet's slope is the kick stream.**
2. **The split's share.** ON's stream pre-wave = the locals' 1,589/gs; belt alone = 30,000/28,141 =
   1,066/gs = 42.1% of OFF's stream. Measured slope ratio 2,432/1,380 = **1.76×**; stream-share
   prediction (B+L)/(B/8+L) = 1.58×. The naive "÷S" (P2's letter, band [4,16]) is **refuted** at
   mixed scenes — my own pre-registered falsifier (<2) fired.
3. **Scaling (arithmetic on the same law):** ratio = (B+L)/(B/8+L): 1.58× at 3×10⁴, 2.63× at 10⁵
   (B = 3.543/gs), 6.27× at 10⁶ (35.52), **8.00× at 10⁹** (locals 1.46/gs become 4×10⁻⁵ of the
   stream). RSS: −307.9 MB at 245k (−24.6%), Δhist 146,756 bindings → **2,098 B/binding** RSS
   (b911's 1,760, window mix).
4. **Channel 1 untouched (P4 held):** held/mints trajectories identical between arms (held 521 vs
   525 at 245k; mints 3.3k both at 50k) — the scan channel is player-driven, exactly as predicted.
5. **Engagement (P1 held):** belt first wave deferred 11–16k → 110–125k gs (de7b's 112,574);
   ON's kick rate pre-wave = locals only. Refusals 0, dead 0, both arms, 277k gs.
6. **Compact side (arithmetic on 0659's published constants, no flight):** at p = 1.0 promotion
   rate = item rate λ = 3.55×10⁻⁵/body/game-s (= 1/28,141 ✓ their 3.6–4.3×10⁻⁵); the split takes
   the belt to λ/8, so τ = 43.6 → 349 game-s at 5.1 KB/live-body (8 GB), 171 → 1,368 at 1.3 KB;
   b911's retained-extra ≈ 1.4·λ·(2·ld+330 s) divides by 8 on the belt. The contacts arm (0659's
   checker, τ ≲ 0.02 orbit) is cadence-free and does not move.

## Predictions
`predictions.md`, written before the decisive flights. P1 held, P3 held (RSS follows: −24.6% at
245k, ratio 1.86×), P4 held, P5 held (ON at 975 MB at 275k, guard never fired; OFF 1,253 at 245k).
**P2's letter failed** (ratio 1.76 < band [4,16]) — reported as the run's content: the law is the
share, not the factor.

## What would make it wrong
- The mint identity (slope = stream) is measured on two arms of one scene at one rung; a rung where
  prune's visit order interacts differently (K = 10⁵, where channel 1 guards first) could break the
  96% closure. The scaling column (10⁵–10⁹) is arithmetic, not flight.
- The compact-side τ ×8 dies with 0659's p = 1.0 (their 170.9k items) and assumes the split's item
  rate really is λ/8 at belt scale (measured here only as the kick stream at 3×10⁴).
- Legality of the split itself is cited (7f97 B17, f790, 98cb), not re-flown; each split kick
  carries ~8× the tidal impulse (|dvq| still fires ≥ 16 quanta a fortiori; dead 0, refusals 0 here).

## Cost of adoption / fit
The split is a law change (digests move; B-gates re-freeze) — that bill is unchanged by this run;
what changes is its value: one lever now buys CPU (crest halves here: max frame 237 → 190 ms,
over-budget frames 213 → 175) *and* memory on both sides of the wiring. PRINCIPLES 12/17 ("the
algorithm that allocates the work … is the most important one"; "use idle time / each part of the
machine") and 33 ("each scale resolves only what matters at that scale"): the belt at 8× coarser
cadence pays 8× less of *both* currencies, and the locals keep theirs.

## The lens
Quant's blind spot is shaving ns at the cost of exactness; the split is constants-only and
digest-auditable, so nothing here prices simplicity away. What the lens may have missed: the
frame-tail reading (over/max) is load-shared-box x86, orders of magnitude only; the M1 re-measure
is the integrator's; and I did not fly a second seed (the mint law is a count identity, not a
chaotic observable, so seed spread should be nil — unverified).

## Reproduce
`regen.sh` (~5 min: build + two flights + the slope script). Raw logs: `work/off_200k.log`,
`work/on_260k.log`, smoke logs beside them.
