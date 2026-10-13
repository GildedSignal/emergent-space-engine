# Predictions (written before the patched A/B)

Primitive evidence already measured (not a prediction): cos shipped 41.6 ns, tuned 41.2 ns
(codegen at the single-chain latency floor), cos4 lane 27.6 ns (1.51× by interleaving four
independent chains), isqrt(u128) 56.0 ns on `d << 62` shapes. 7d2b's "cos 77 ns" node
attribution is ~1.9× inflated on this box; the shipped loop already sits at its ISA
dependency-chain floor (~13 × ~11.5 cycles ≈ 42 ns at 3.6 GHz).

Predictions for the patched tree (fast_quad and weak_quad evaluate their four cos per panel
through interleaved `cos4`):

1. **Compile median: −4% to −12%** (base median 18.9–19.4 µs → 17.0–18.4 µs), 3 runs per arm,
   medians compared. Ceiling: 14 ns saved/cos × 4 cos/node; the realized saving is smaller
   because divisions, isqrt and products share the node and out-of-order execution already
   overlaps the four chains partially.
2. **Per-key gradient: the saving grows with panel count.** The cheapest keys (e = 0, few
   panels) move < 3%; the most expensive (e = 0.99, most panels) move the most, > 8%. If the
   saving is flat or largest on cheap keys, the mechanism is wrong and the run reports that.
3. **Bit-identity holds:** the plane settle digest is identical base vs patched, and the
   space test suite passes unmodified (cos4 is the same floored products lane-wise; fuzzed
   2M operands lane-wise against cos).
4. **The tuned single-chain cos is NOT a lever** (measured equal at the primitive; no
   compile-level run spent on it).
5. Held-out risk, honestly: the OoO window may already interleave the four chains inside
   fast_quad (they are independent in the unrolled loop), in which case the compile-level
   gain is < 4% and the honest claim becomes "the panel's cos chains are already
   interleaved by the hardware; the primitive's 1.51× does not survive the node."
