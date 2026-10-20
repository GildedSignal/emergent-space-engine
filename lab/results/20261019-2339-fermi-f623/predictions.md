# Predictions (written before any flight or bench on this box)

Question: the mint stream's machine floors at 10⁹ — allocator throughput and memory
bandwidth per fired kick, the two rows no ledger entry prices — and whether they force
the kick-mint deletion (225d's "outright deletion target") beyond the memory/CPU case.

Priors from the record (not measured here): λ = 3.55–4×10⁻⁵ kicks/body/game-s (0659, 3aec);
mint ≈ 2.1 KB retained/binding (88e9: 2,098 B RSS/binding; 9edc: Binding 192 + Segment 208 +
Entry 288 + table); fired item 82.5 µs x86 player-stream / 44.7 µs x86 belt clock arm (3aec).

Cases I have NOT tuned on (held out):

- P1 (calls per kick): allocs+frees per fired kick, whole coast flight, K = 10⁴,
  lands in **[4, 24]**. Kill: < 4 → the allocator row is immaterial at any cadence
  (report the row as dead); > 24 → the mint drags more machinery than 9edc's anatomy
  — investigate before composing.
- P2 (bytes per kick): bytes ALLOCATED per fired kick lands in **[0.8, 5] KB**
  (9edc's 2.1 KB is retained; allocated ≥ retained because Vecs grow and die).
- P3 (the mint's fingerprint): in the highest-kick window, ≥ 50% of allocated bytes
  come from sizes in the mint family {192, 208, 288} × {1,2} (doubling included).
  If the top sizes are scattered (no family), the per-kick attribution is weaker and
  I must window-subtract instead of histogram-attribute.
- P4 (the composition at 10⁹, rtf 100, shipped cadence λ·K ≈ 3.6–4×10⁶ kicks/s):
  allocator CPU ≤ 2 M1-core-equivalents (NOT a wall); allocated-bytes write traffic
  ≤ 50% of the M1's ~60 GB/s (NOT a wall, but I expect ≥ 10% = material);
  both fall ≥ 4× under split8. Decision half: if either bound breaks, the mint
  deletion is machine-forced, not a preference — that would be the headline.
- P5 (N-flatness): K = 3×10⁴ reproduces P1/P2 per-kick constants within 2×
  (3aec found the item cost N-flat; the allocation law should ride it).

Bench anchor (this box, x86, order of magnitude only): one malloc+free pair of a
192 B object costs 20–100 ns single-thread; I predict the measured value in that band.
