# Author fiAll deliverables are complete and verified (regen.sh reproduced end-to-end in 199 s; deterministic window masses match to ≤1 event in 310k).

**Claim:** the belt's freeze crest is a stable, period-halved **two-comb limit cycle** — a kick comb (≈51.6 µs/event) at phase ≈ interval/2 and a boundary comb (≈13 µs) at phase ≈ interval, each exactly ≈1.00 event per belt body per 28,141.5-game-s doll interval and decaying only −2.5 %/interval over 3.7 intervals (measured on shipped `nladder` coast at 3×10⁵ and 10⁵, bit-identical across rtf 300/1800; the mechanism is law-native, `boundary_clock` = "the synchronised output of the split, in the middle between two kicks") — so the freeze recurs every half-interval forever at shipped cadence, idle-time compute-ahead fits the whole cycle at the player's pace with 10.8× headroom at 3×10⁵ and 3.2× at 10⁶ but is 308× short at 10⁹ (≈24 h of clamped delivery per interval there), and every kick-counted 10⁹ stream ledger undercounts the belt by the boundary comb's ~+26 % CPU.
kicks"). Predictions were registered before the
flights: P1 held in substance (recurrence, all crests ≥ 0.75 × E₁) and missed the second
comb's period-halving — the miss is the finding; P7's ledger held exactly.

Everything regenerates: `regen.sh` (~4 min warm; patch = print-only instrument on shipped
`nladder`, no law touched). Numbers: `work/arm{A,B,C}.log`, `crest.txt`, `combs.txt`.
