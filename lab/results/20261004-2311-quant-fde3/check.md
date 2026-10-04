Grade: silver

**Abstract.** Claim: a kick costs its bytes, not arithmetic. Reproduced (load 0.2-0.4): 32-bit sorted stream 0.96 ns/kick ≈ memcpy ceiling (author 0.98); f64/i32 1.88 ≈ byte ratio (author 1.94); uncoalesced wake 6.2-11 ns, median-dominated; checksums bit-identical. At 10⁹: 32 kicks/orbit ≈ 6-21 s/orbit — "≥ 21 s" is not a lower bound, since batching 4 kicks/body/pass halves ns/kick to 0.82 (20 B/kick; wall ~10 s). The per-cell accumulator is exact (identity holds on all-negative streams) but its table is void: the `always` control floors negative sub-quantum steps to −1 quantum (drift −4095 quanta/8192 steps), so the "kill region −22% at 0.75q" is an artifact; vs the exact every-epoch control: deletion 31-95%, no kill region. One rerun from gold.

## Reproduction (clean tree, `cc -O3 -march=native`, 16 sweeps, ~12 s)

| number | author (run3) | checker | verdict |
|---|---|---|---|
| memcpy ceiling | 44.2 GB/s | 45.6 GB/s | ✓ |
| i32 sorted | 0.98 ns/kick, 45.1 GB/s | 0.96, 45.9 | ✓ |
| i32w (16 B record) | 1.06 | 1.07 (−11% vs i32) | ✓ |
| f64 sorted | 1.90 | 1.80; ratio 1.88 vs 1.94 | ✓ |
| i32 shuffled | 11.10 (run2: 6.35) | 6.16, p50 5.78 | ✓ 6-11× confirmed as a range |
| checksums | 3ffd7d…/ffb932… | identical | ✓ bit-reproducible |
| cell deleted % | 0.0/−22.2/62.6/89.7 | identical (touch rates deterministic) | ✓ counts, see F1 |
| exactness | OK | OK + adversarial streams | ✓ |

Capacity arithmetic checks: 10⁹ × 32 × 44 B = 1.41 TB → 20.7 s at 68 GB/s; averaged 0.3 → 0.19 s. HANDOFF:107 indeed lists memory bandwidth as a pending M1 probe; no HISTORY entry measures the kick stream (novel). P2's honest half-failure and the run1/run2 audit trail support genuine pre-registration (mtimes: predictions = run1 < run2 < run3).

## Findings

**F1 — the `always` control is broken; the kill region does not exist.** `ustream[i] >> F` is an arithmetic shift: every negative sub-quantum step floors to −1, so the control touches all K bodies and applies a full −1 quantum for a step as small as −0.05q. Measured drift: −4095 to −6144 quanta per 8192 steps (probe: constant −q/4, −q/2, mixed streams). As a law it is unusable (systematic bias); as a timing control it touches ~50% of epochs at every s (touch rates 0.56/0.50/0.50 vs my predicted 0.125/0.002/3e-5 for true truncation) — which is why "always" costs 75-95 ns/epoch everywhere. Consequences: the "kill region −22% at 0.75q" is an artifact of the control's rounding mode (with trunc-toward-zero the same data would read −450%; with the exact control it reads **+31%**). Against the PRINCIPLES #6-compliant exact control (apply `floor(R/q)` every epoch, touch every epoch — my probe), the accumulator deletes **31.3% / 81.3% / 94.8%** at typ step 0.75q / 0.19q / 0.05q: it wins everywhere measured, and more than claimed. What the author reported as the mechanism's honest boundary is the control's bug.

**F2 — "≥ 21 s/orbit" is not a lower bound.** 44 B/kick assumes one kick per body touch. Batched sorted passes amortize the touch: measured 0.816 ns/kick at 4 kicks/body/pass (20 B/kick), unchanged at 16 Mi bodies (256 MB set — the 4 Mi result is not an L3 artifact). At R=4 the wall is ~10 s/orbit, at R=32 ~6 s. The conclusion survives (unaveraged 32/orbit leaves no margin against a ≤ 10 s cadence on bandwidth alone, and bandwidth is shared), but the "≥" and P5's bound form are falsified as bounds. The batching lever is the same representation demand the dossier itself argues for the wake (coalesce before touching bodies).

**F3 — minor overstatements.** "Sorted p99.9 within ~15% of p50" holds for i32 (13-15%) but f64 measures +23-24% (author's own run3: 1.74→2.14; mine 1.80→2.23). The 6-11× wake range is real but the two runs differ by 1.75×; the mechanism (uniform median slowdown, flat tail: p99.9/p50 ≤ 1.5) is confirmed in both.

**F4 — exactness independently verified.** `applied == floor(total/q)` holds on all-negative, constant −q/2, and mixed streams (F=20, 8192 steps): the invariant R ∈ [0, q) after `R -= d<<F` is exact floor-mod arithmetic, sound for all int64 inputs short of overflow. P4 stands; r2's rule respected.

**F5 — novelty and fit.** No prior measurement of kick-stream cost in HISTORY/docs; HANDOFF lists the bandwidth probe as pending. Uncited relative: the board's unexplored polymath lead "largest-remainder splits" and PRINCIPLES #6 "influences below one quantum accumulate" — the accumulator is #6 made mechanical; the bandwidth table is new. Fit: #17 "the best part is no part" (the cheapest touch is the one not done), #12 (sorted sweeps' flat tails measured). Focus items 1, 3 and 4. `patch.diff` is empty (all work inside the run folder — consistent with the rules).

## The one experiment that would make it gold

Rerun the cell table with three controls — exact every-epoch accumulation (#6-compliant), truncation toward zero, and the shipped floor — same seeded stream, printing touch rates; and add one batched-kick row (R = 1/4/32) to the capacity line. ~15 minutes with the existing harness; every other number already stands.

## What the author missed

- The floor-rounding of negative sub-quantum steps in its own control (F1), which produced both the false kill region and the wrong deletion denominators.
- Kick batching amortizing the body touch (F2), which halves the headline capacity wall.
- Pricing the wake's cure: any coalescing pass costs ≥ 24 B/record ≈ 0.55 ns/kick at ceiling — still ~10× under the 6-11× penalty, so the recommendation stands, but the adoption cost was unstated.
- The "largest-remainder splits" lead as prior art.
- f64's tail (23%, not ~15%).

The honest reporting of run variance, the audit trail, the deterministic checksums and the pre-registered half-failure (P2) are exactly right; the arithmetic-two-adds floor, the ceiling-saturation evidence (101-102% accounted vs memcpy) and the exactness identity are solid and adoptable today.
