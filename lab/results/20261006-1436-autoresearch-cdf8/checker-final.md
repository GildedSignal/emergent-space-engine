Working...
Check complete. `lab/results/20261006-1436-autoresearch-cdf8/check.md` written; tree restored to pristine + `work/patch.diff` only; nothing committed or pushed.

**Grade: lead** — everything reproduces, but both central claims of the dossier fail, and the check surfaced a new engine bug the run stopped one inch short of.

What I did and found:

- **Reproduced** (clean tree + patch): all six scene digests byte-identical to `heldout-final.txt`; timings within noise; the P-kill event reproduces exactly (47 vs 69 encounters, 0 vs 19 contacts, same `UNSAFE SKIP j=16` line, digest matches `round1b.txt`); predictions discipline genuine (file times confirm `predictions.md` preceded all measurements).
- **Claim 1 fails**: the saved `round1-filter-encounter.rs` carries an unconditional decode-on-skip self-check, so rebuilt from it A measures **1889 vs 1497 ns/item (26% slower)**, matching the author's own `round1-final.txt` — the headline "445 vs 1495 (3.4×)" is real only for a self-check-free build that was never saved (I measure 432 vs 1503 after deleting the block).
- **Claim 2 fails**: decoded directly, j=16's readout sits **above** its key's periapsis — the band premise held; the "readout 1.7e8 inside periapsis" was the player-band gap. My adversarial pure-test-particle belt (`E09L`, e=0.9, 16× interval, no secondaries) fails identically, killing the "secondaries only" boundary and the proposed one-flag fix.
- **Real mechanism (new, no HISTORY entry)**: `hit()`'s `cross*cross` overflows i128 (cross ≈ 6.5e20 → cross² ≈ 4.2e41) and wraps in release, passing `cross² ≤ rr·ww` — verified false in exact bignum. On the plane, the **shipped** finder reports 69 encounters/19 contacts where exact arithmetic gives **47/0**: 22 phantom encounters and *every* contact is phantom, in the live player-encounter check (HANDOFF bottleneck #4). On A/B/HO1-3 the predicate is overflow-free, which is exactly why bit-identity held there. The filter's skips were geometrically right everywhere measured — the pre-registered kill fired on oracle noise.
