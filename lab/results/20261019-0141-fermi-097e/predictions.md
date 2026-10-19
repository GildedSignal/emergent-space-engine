# Predictions — 20261019-0141-fermi-097e (written before the probe flights and the ledger run)

The run: the board's interlocking 10⁹ ledger (CPU = N·kick-rate·kick-cost + encounter work +
frame; memory = N·store-bits + N_live·live-bytes), assembled on the week's measured laws with
one fresh same-harness anchor (two shipped `nladder` flights, this box), page-citing every
other constant. The lens's question #1: which term breaks first at 10⁹ on one M1, by how many
orders, and which of the measured laws must not be extrapolated.

## Probe predictions (this box, x86, orders only)

- **P1 (build law).** `b_per_body` at N = 10⁴ and 10⁵ reproduces the page's 2,340–2,459 B/body
  law within ±10% (dcf1, 99da). If it reads < 2,000 or > 2,800, the memory row's anchor is
  machine-dependent and the 10⁹ extrapolation must be re-derived.
- **P2 (the belt's own stream is inert on the ladder).** Total kicks and events over the same
  coast flight are EQUAL at 10⁴ and 10⁵ within 50% (the player's stream is N-flat, the ladder
  belt fires ~nothing), so `kicks_per_body_gs` falls ~10× from 10⁴ to 10⁵. If total kicks
  instead grow ≈ ×10 (∝ N), the belt is NOT inert on the ladder and the frame's N-flatness at
  10⁶ does not transfer to 10⁹ — the claim's CPU half dies.
- **P3 (frame N-flatness at these rungs).** engine p50 ≤ 1.5 ms and p99 ≤ 12 ms at both rungs,
  held_max ≪ 2,048. If p50 grows > 3× from 10⁴ to 10⁵, some per-body frame term is alive that
  dcf1 did not see at 10⁵–3×10⁵.

## Ledger predictions (arithmetic on page-cited constants + P1–P3 anchors)

- **P4 (CPU composes within one order of the 4-core budget).** The composed 10⁹ CPU ledger —
  kick/event stream (cd3b: 5.3–8.4 composed) + certificate churn (08d0's epoch rule: 2.8–5.5)
  + key mint (≤ 1.9) + view serve (e6c9/e3a4: O(cells) + due events, ≤ ~0.1 cores, one named
  wiring debt) + frame (N-flat ≈ 0.06 cores) — lands between 8 and 25 cores, i.e. the board's
  ~10³ CPU gaps are composed away to ≤ ~6× the budget, every remaining lever named and ≤ 2.1×
  (cd3b's own closure arithmetic).
- **P5 (kill criterion).** If any CPU term cannot be held below ~50 cores at 10⁹ on the
  measured laws (a term ≥ 10× my assembly), the claim dies: the row keeps a live 10³ and the
  board's ranking stands.
- **P6 (memory is the top row's 10³, and it is wiring, not physics).** Shipped build
  extrapolates to 2.1–2.6 TB at 10⁹ (260–330× over 8 GB); the wired compact store's measured
  floor is 2.1–15.8 GB at 10⁹ (0.3–2× over: 1.7–2.4 B/body self-stirred, 126 bits/body driven
  worst). The build/floor ratio is ≥ 100×. If the build law's 10⁹ extrapolation were within
  10× of the floor, the top row's memory gap would be physics, not wiring.
- **P7 (the promotion residency dial, new arithmetic).** With HANDOFF's live cost ~5.1 KB and
  a9d7's fired-kick rate 3.6×10⁻⁵/body/game-s, an every-kick-promotes policy busts 8 GB at
  residency τ ≳ 40 game-s (predicting the arithmetic lands in 20–80); with promoters only
  (contacts 0.22/s + SOI transits 1.31×10⁻²/body/orbit), orbit-scale τ fits in ≤ 3 GB. So the
  dial is what fraction of fired kicks break the compact certificate — priced, not measured
  here, and named as the tier's open half.

## Honest misses will be reported as misses.
