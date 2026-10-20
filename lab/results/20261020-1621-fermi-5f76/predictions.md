# predictions.md — 20261020-1621-fermi-5f76 (written before the decisive arms)

Question: are 8994's one-seed allocation constants laws (od 6(c)), and does ladder arithmetic
close the 194 KB/player-item (od 6(a)'s mechanism, answered at the census instead of a backtrace)?

Arms flown after this file: A2 (seed 2, K=10⁴ coast), A3 (seed 3, K=10⁴ coast),
A4 (seed 2, K=3×10⁴ coast), A5 (seed 2, K=10⁵ coast). The reproduction anchor
A1 (seed 1 = 8994's D1 verbatim) may fly before this file's final edit; it is not decisive.

The Fermi model (before any seed-2 run):
- The player scratch is a pull Vec grown by realloc doubling, top capped at 56 KiB (57,344 B),
  entries ~352 B (the census's own family) → a full ladder's traffic ≈ 2 × top ≈ 115 KB.
- 8994's 193.4 KB/item = 1.68 full-ladder-equivalents: either a mixture of full and short
  ladders (mean 1.68 rung-sums) or a second growing Vec. The census rung counts decide: one
  family at exact multiples of the {352,384,704} family with top 57,344 = one capped ladder,
  mixture-shaped; two disjoint tops = two Vecs (od 6(a) answered "two").
- The ladder top is doll-size-driven with a binding cap at K=10⁴ (163 entries of 352 B), so the
  per-item constant should be seed-flat (the seed moves orbit phases, not Vec policy) and
  K-flat (the cap already binds).

Predictions, with kill bars:

P1 (seed-flatness, the decisive one): player-scope KB per player item (traffic ÷ stats.items[3],
  the checker's denominator) at seed 2 and seed 3, K=10⁴ coast, both in [135, 251] KB
  (0.7–1.3× of 193.4). KILL BAR: any seed outside [97, 387] KB (0.5–2×) demotes the constant
  from law to one-draw (the page's own caveat fires).

P2 (K-flatness at seed 2): player KB/item at K=3×10⁴ and 10⁵ within ±15% of seed-2 K=10⁴.
  KILL BAR: a ≥2× move with K at fixed seed (the cap reading dies; the term is doll-proportional
  per body and the 10⁹ "~19 KB/game-s" row must be re-derived).

P3 (ship item): ship-scope KB per ship item at seed 2 in [2.6, 4.8] KB (0.7–1.3× of 3.7).

P4 (the headline, 8994 P1 on a second seed): item-scope ≥ 8 KB per fired kick at seed 2
  (the OLS-attribution refutation survives a second seed). Band predicted [8, 16] KB/kick.

P5 (base): frame-base 1.0–4.5 KB/game-s coast at seeds 2/3 (seed-1: 2.0–2.2).

P6 (mechanism): the player-scope >2 KiB census at seed 2 sums to ≥75% of the player term with
  ONE ladder family (exact multiples of the {352,384,704} heap family, top mean 57,344 ±2×),
  realloc-dominated (≥50% of player bytes in realloc new sizes).
  KILL BAR: the top mean moves off 57,344 B by >2×, or two disjoint top families appear —
  then the one-ladder model dies and od 6(a)'s answer is "two Vecs" (still a result: named).

Controls: A1 must reproduce 8994's D1 within 5% on item KB/kick (11.35) — if not, the
instrument or tree drifted and the run is VOID on its own control. ES_SEED off (unset) = seed 1
= shipped bits verbatim (the override defaults to 1; assert by A1 vs 8994's numbers).

## Outcome (appended after the arms; the predictions above were not edited)

- P1 HELD: player KB/item = 193.4 (A1, seed 1 — reproduces 8994's 193.4 to the digit) /
  193.8 (A2, seed 2) / 199.0 (A3, seed 3). All inside [135, 251]; no kill bar fired.
- P2 HELD: seed-2 K-series 193.8 (10⁴) / 193.8 (3×10⁴) / 194.0 (10⁵) — 0.1% spread. The cap
  reading survives: the ladder top is 57,344 B EXACTLY in all five arms.
- P3 HELD: ship KB/ship-item 2.8 / 3.0 at seeds 2/3 (band [2.6, 4.8]).
- P4 HELD at its arm (10.14 KB/kick ≥ 8 at seed-2 K=10⁴); the K=10⁵ arm reads 7.23 — below the
  letter's band, but it reproduces the page's known dilution (8994 checker: 6.31 at 10⁵),
  not a surprise. Disclosed as band-miss-by-dilution.
- P5 HELD: base 2.04–2.88 KB/game-s.
- P6 HALF-HELD: ONE ladder family, top mean 57,344 ±0.01% in every arm (kill bar not fired),
  realloc-share 79–80% (≥50% ✓) — but the >2KiB census share is 69–72%, under the ≥75% letter
  (the <2KiB small-call term is ~55–62 KB/item, ~30%, bigger than my ≤25% estimate).
  The structure the census counts, per player item: 2.07–2.12 ladder STARTS that reach rungs
  1–3, 1.03–1.06 that reach the 56-KiB cap — TWO array-builds per item, one capped, one short
  (seed 2 also shows a third, rung-1-only start: r1 3.12–3.18 vs 2.08 at seeds 1/3).
- NEW, not predicted: the ship term's per-KICK marginal RISES with K (1.45/1.53/1.45 at 10⁴;
  2.18 at 3×10⁴; 2.99 KB/kick at 10⁵) while per-ITEM it falls (3.7→2.3 KB) — the "1.6 KB/kick"
  constant the 10⁹ row cites is the bottom of a K-rising range.
- Control: A1 reproduced 8994's D1 on item KB/kick (11.35 vs 11.35), base (2.04 vs 2.03),
  kicks (108,282 vs 108,383, 0.1%), ship items (42,415 vs 42,422) — instrument faithful.
