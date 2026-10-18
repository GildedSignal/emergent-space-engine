# Dossier — 20261018-1617-second-20261018-1530-system-afff-687c (second author)

## Claim

The checker's named experiment, done: re-flown in the swept metric across burn,
the 6,000-member dense crowd and seed 2, with k from a dimensionless density
trigger. **Both halves of the original claim's mechanism are settled: the
constant k ≈ 16 neighbour read is refuted in every metric (the swept metric
rescues 22 of 1,452 and 16 of 1,754 burn hits beyond Euclid rank 15 — the
failure is the window's density μ ≈ 57, not the metric; the swept and at-t
rank profiles coincide within 2% everywhere), and the record that does serve
every hit is the window-membership record — hold the μ_win bodies inside the
swept encounter window, maintained at sweep entries/exits — which is sound by
construction (a hit's out-ranking set is a subset of the window), measured
sound on every regime flown (max swept rank 52 < 432, 74 < 447, 3,493 < 4,334,
3,623 < 4,117), and measured cheap to maintain: 0.6 entry/exit per answered
scan under burn against 340 candidates walked per scan.** The gain is restated
from "K/k ≈ 20–1,500×" to the measured law K/μ_win: 85× (ladder), 16×
(shipped), 6.0–6.6× (crowds, burn included), 1.0–1.2× (the dense decade, where
the walk, the window and the answer are the same ~4,100 bodies and nothing is
deletable — the wall there is the answer's own size, i.e. the 2¹⁰·reach
encounter radius, not the walk).

## Bottleneck

Board #1 (the frame wall) and the checker's two refuting regimes. What the
correction deletes: the O(K) walk and the K-sized pin become a μ_win-sized
record plus per-event entry/exit maintenance (measured 0.6 touches per scan
under burn, ~0.2% of the 340 candidates the walk reads); at the ladder scene
(the locals' 5.3× walk inflation) the read shrinks 85×. What it does not
delete: the dense decade's answer itself (4,024 hits on one scan — that is the
output, and its cost belongs to the encounter radius or the doll split).

## Evidence

Shipped code + the author's census extended (swept-miss rank, window density
μ_win, receder pollution, membership churn between consecutive answers, the
k-rule k = max(16, ⌈α·μ_prev⌉) with μ_prev the previous answer's size, and a
float-vs-law consistency counter that stayed 0 on all 33,254 hits). Flights:
`nladder`, rtf 100, 1,500 frames, seed and MEMBERS knobs in the run's patch.
`regen.sh` regenerates every number (~35 s after a warm build; verified exit 0).

| scene | scans/answered | cand/scan | hits | max answer | μ_win mean/max | max swept rank | churn/answer | kviol α=1.25/2/4 | k=16 viol | K/μ_win |
|---|---|---|---|---|---|---|---|---|---|---|
| A shipped 48 | 241/241 | 33.3 | 128 | 1 | 2.1/22 | 0 | 0.2 | 0/0/0 | 0 | 16× |
| C ladder 20k | 241/241 | 177.8 | 128 | 1 | 2.1/22 | 0 | 0.2 | 0/0/0 | 0 | 85× |
| B1 crowd 600 s1 | 232/231 | 323.8 | 294 | 3 | 48.7/415 | 11 | 5.0 | 0/0/0 | 0 | 6.6× |
| B2 crowd 600 s2 | 222/222 | 330.4 | 278 | 3 | 52.0/441 | 4 | 5.2 | 0/0/0 | 0 | 6.4× |
| BU1 burn 600 s1 | 2169/1497 | 340.0 | 10559 | 93 | 56.6/432 | 52 | 0.6 | 0/0/0 | 1447 | 6.0× |
| BU2 burn 600 s2 | 2148/1487 | 354.6 | 13741 | 123 | 58.5/447 | 74 | 0.8 | 12/2/0 | 1762 | 6.1× |
| D1 dense 6000 | 3/1 | 4505 | 4024 | 4024 | 4334/4334 | 3493 | — (cold) | 3823/3823/3823 | 3823 | 1.0× |
| DB dense burn | 486/1 | 4761 | 4102 | 4102 | 4117/4117 | 3623 | — (cold) | 3862/3862/3862 | 3862 | 1.2× |

- **The swept metric is not the mechanism** (my P1, falsified): under burn,
  `euc_gt15_sweep_le15` = 22/1452 (s1) and 16/1754 (s2). The burn hits beyond
  rank 15 are not far-body sweep entries; their scans' windows hold 30–60
  members (μ_win 56.6 under burn vs 2.1 shipped), and the hits sit at rank up
  to 52 because that many bodies are nearer, in either metric (max ranks equal
  within 2% on every scene).
- **The record that serves every hit**: rank_swept(hit) < μ_win(scan)
  structurally, and measured: worst case 3,623 < 4,117. A record holding the
  window membership answers every scan by testing each member's approach flag.
- **The tight, warm trigger**: k = max(16, ⌈α·μ_prev⌉) covers 24,288/24,300
  burn hits at α = 1.25 and 24,298/24,300 at α = 2; α = 4 covers all. Cold
  start (a doll's first answer, the only answered scan at the dense scenes)
  has μ_prev = 0 and needs a seed walk or a doll-level density prior.
- **Churn** (the record's maintenance, unmeasured until now): under burn the
  membership changes by 0.6–0.8 bodies between consecutive answers (~17 ms
  apart) — against 340 candidates read per scan by the walk. At coast 5 per
  pair (pairs ~10 game-s apart). Worst single turnover 272 (burn onset / long
  coast gaps).
- **Reproduction**: A and C bit-identical to 20261018-1530-system-afff's
  dossier (241/240/33.3/113/128 and 241/0/177.8/113/128, all rank 0). The
  burn/crowd scan counts are wall-clock coupled at rtf 100 (2,147–2,169
  across re-flights) exactly as the checker scoped; every fraction above is
  stable across the three re-flights flown (BU1 kviol 0/0/0 in all three;
  BU2 10→12 at α = 1.25).

## Predictions

`predictions.md`, written before the flights (after one 8-s sanity flight of
scene A only). **P1 failed — and the failure is the finding**: the swept
metric does not absorb the burn entries (1.4%/0.9% rescued); the binding
variable is the window density. P2 held (dense: 95% of hits violate k = 16,
all within rank 3,493 < 2× the answer). P3 held (violations 0.09%/0.015%/0%
at α = 1.25/2/4, cold start excepted and named). P4 held (seed-2 coast: max
rank 4). P5 held in shape (gain 16–85× sparse, ~6× crowds, 1.0–1.2× dense).
The kill criterion (hits beyond 4× their window density, > 5%) never
triggered: no hit ever exceeded 1× μ_win.

## What would make it wrong

The record's per-**event** churn is still unmeasured (churn here is between
consecutive answers; at coast those are ~10 game-s apart, so coast churn is a
lower bound per unit time — burn, the loaded regime, is the number that
matters and its answers are 17 ms apart). The cold start needs one seed walk
per doll entry, or a doll-aggregate density prior, unmeasured. Fleet-wide
scans (another body as the origin) remain unmeasured, as in the author's run.
A genuine relativistic crosser remains unflown — but with the mechanism now
measured as density, a crosser arrives as μ_win growth, which the record
tracks by construction. The dense decade's 4,024-hit answers are the output,
not a defect of the record; if the integrator wants them cheaper, that is the
encounter radius (2¹⁰·reach) or the doll split, a different lever.

## Cost of adoption, and fit

One structure per scanned body: the window-membership record (μ_win entries),
maintained at sweep entry/exit events — the same record the encounters page's
open direction 1 proposes; one adoption still pays both pages. Measured cost:
μ_win ≈ 2 (shipped/ladder) to ~57 (crowd/burn) entries, 0.6 touches per
answer under burn; the pin falls from K×224 B to μ_win×224 B (85× at the
ladder scene). Fit — PRINCIPLES 3: "Compute only surprises. Cost follows
change and entropy": the walk re-reads 340 members to find 0.6 changes; the
record reads exactly the changes. Principle 33: "a body resolves only the
influences that are significant at its own scale" — μ_win is that significance
made a count, and it, not a constant, sizes the structure.

## The lens

The second-author lens took the checker's experiment at its word and found the
checker's own premise half-wrong: the swept metric was proposed as the fix and
is measured inert (the rank profiles are metric-independent at these regimes);
the density trigger the checker added in passing is the whole mechanism. What
this lens may have missed: the per-event churn (the adoption's real price),
and that μ_win is only known by walking — the trigger needs the seed walk or
the doll prior, so the record deletes the *repeated* walk, not the first one.
