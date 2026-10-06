Working...
Run complete. Artifacts: `dossier.md`, `predictions.md` (pre-registered), `log.md`, patch + raw outputs in `work/`, bench crate in `bench/`; the tree carries the 60-line patch (digest-verified against the independent all-pairs reference, Newtonian 3/3 and relativistic 4/4 EQUAL).

**Claim:** the CPU chronon reference's map hashing (SipHash on ~2.4M lookups per chronon) was a measured bottleneck, and replacing it with a multiply-xor hasher makes the reference 1.42× faster at n=200k (771→542 ns per body-chronon; 1.41–2.12× across eight held-out configs) with bit-identical digests — while the two heavier restructuring attempts (scatter table 0.79×, Bloom gate 0.85×) measured slower and were reverted, locating the remaining 77% pair-loop cost in cache misses, not arithmetic.
