Working...
Check complete. `check.md` written, author's page corrected in place, nothing else touched, no git operations.

## Verdict: silver

**Reproduced exactly** — `regen.sh` bit-identical (md5 match); every shipped constant verified in `scenario.rs`/`encounter.rs` (genesis lanes, ship radius 49.04 m, ENCOUNTER_LOG2=10, reach = rᵢ+rⱼ); every cited digit verified on the source branches (f80a's 8.03 bindings/body @ 174k gs and wave onset 11k–16k, 0659's λ = 3.55×10⁻⁵, 3aec's 82.5 µs / 208/355). Predictions pre-dated the computation; P2/P4/P6/P7 held, P1/P3/P5 failed honestly. The "encounters fire no items" premise verified in code.

**The central law is 10–20× high — my main adversarial finding.** The strip formula is fed the *annular* ⟨|Δv|⟩ = 22.9 km/s, which averages pairs at the same radius on opposite sides of the annulus — pairs that can never conjunct. On the author's own genesis, exact-Kepler counts (counter validated 0.90 on a known-answer synthetic) measure:

| reach d (root) | occupancy | per-root pair rate at 10⁹ |
|---|---|---|
| 10⁵ | 0.077 | 27.75 (111 events, author's law predicts 336) |
| 10⁶ | 1.3 | 40.3 (events travel at **2.7 km/s**, not 24) |
| 2×10⁶ | 5.3 | 48.8 |

Below the headline 84.09 at every reach, falling with reach; co-located dispersion 1.74 km/s — inside the author's own discarded P1 band. Instrument-reach asymptote ≈ 4.9/root → TP bar ≈ 3×10²/game-s (not 5.7×10³), contacts ≈ 0.3/game-s (not 5.58) → ≤ +0.006 cores (not +0.054), wake-up ≈ 3×10⁷, C_contact ≈ 5×10⁴.

**Every conclusion survives a fortiori** (closure, emptiness, census refutation — that one is pure verified arithmetic); only the TP bar and concentration thresholds are load-bearing downstream. The page now carries the corrected constants; the one gold-making experiment is the co-located-dispersion fold plus a live conjunction counter on the stirred-belt flight (od 3).
