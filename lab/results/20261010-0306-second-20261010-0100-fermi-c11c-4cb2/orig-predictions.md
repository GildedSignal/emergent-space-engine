# Predictions (written before the decisive run; not tuned on)

The decisive experiment: `cargo run --release -p xtask -- universe --kick-bench --seconds 20`
on this Linux box (8 vCPU shared), plus `universe --bench --rtf 100 --seconds 20` for the
whole-loop event rate. These pin `t_kick` (ns per kick on the shipped integer law) and the
memo behaviour, the constants the whole 10⁹ budget multiplies.

Constants already known (not predictions): the 16-byte tube (law.md); H0190's 32.5 kicks
per low orbit, 0.285 averaged (114× cut), 0.6 core per 10⁶ low-orbit ships unaveraged, 0.01
averaged; belt-0 density gives 427 encounters / 1844 bodies / 20 orbits ≈ 0.012 encounters
per body per orbit (board, 30 Sept); a 3 AU orbit is 1.64×10⁸ s.

## Held-out predictions

P1. **Per-kick cost is compile-dominated, not kick-dominated.** The plane recompiles an
    orbit on ~99% of kicks and the exact memo hits 0% on distinct kicks (5 Oct correction).
    Predicted: median t_kick ∈ [0.5, 30] µs. If < 0.1 µs, kicks are pure drift updates and
    the memo finding is stale for this bench.

P2. **Memo split.** On distinct replayed kicks: exact-key shape reuse < 5%; quantized
    12+12-bit key reuse > 50% (the 5 Oct run saw 94.5% on the quantized cell).

P3. **Tail:** p99/median ≤ 30 (compile-dominated; rebinds are the only heavy tail).

P4. **Budget verdicts at 10⁹ bodies, rtf 100** (each game-second = 0.01 real seconds):
    - Storage breaks first: 16 B × 10⁹ = 16 GB > 8 GB unified (2×; 4× the 4 GiB sim budget).
    - Belt regime (a ~ 3 AU, 32 kicks/orbit): 10⁹ × 32 / 1.64×10⁸ × 100 ≈ 2×10⁴ kicks per
      real second → ≥ 3 orders of magnitude below the machine at any plausible t_kick.
    - Worst case, all 10⁹ in low orbit unaveraged (5.4×10³ s orbit): ≈ 6×10⁸ kicks per real
      second → breaks by ≥ 10× at any t_kick ≥ 130 ns on 8 cores.
    - Same but averaged (0.285 kicks/orbit): ≈ 5.3×10⁶ per real second → fits with ≥ 10×
      headroom iff median t_kick < 1.5 µs. **This is the verdict that flips on P1.**

P5. **H_live is battle-dominated, not billion-dominated.** Belt creation at 10⁹ bodies:
    0.012 encounters/body/orbit × ~128 bits/scar / 1.64×10⁸ s ≈ 10 bits per game-second —
    ≤ 1 kB/game-s in any belt-like mix. The binding creation rate is fleet contact epochs,
    which live in the battle's Fermi frame, not in the belt.

P6. **The board's "about 190 cores" for 10⁹ orbiting bodies is 3× optimistic against
    H0190's own rate** (0.6 core per 10⁶ → 600 cores); both are worst-case low-orbit
    figures, so both fall to ~10 cores once averaged tides are the default. Report, not a
    kill: under 10×.
