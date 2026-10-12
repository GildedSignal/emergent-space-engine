# Predictions — 20261012-1019-quant-b29b (written before the decisive run)

Question: what does one presented frame of the shipped plane cost as the entity count N grows, and
which tier crosses the 16.7 ms budget first — the budgeted event tier or the unbudgeted fixed tier
(`rekey`'s per-entity deadline recompute, the defer/requeue drain, the digest)?

Held-out cases (not tuned on; the probe is first run at these N):

- P1 (fixed tier scaling): `rekey` alone grows ~linearly in N (the log factor is small), and an
  "empty frame" (`advance` with a zero-event budget) costs ≥ 2× `rekey`, both reaching ≥ 1 ms
  somewhere in N ∈ [3×10⁴, 3×10⁵] on this shared x86 runner.
- P2 (ceiling): at N = 1.2×10⁵ the fixed tier alone exceeds ~10% of a 16.7 ms frame; the frame
  becomes wall-dominated by the fixed tier (not events) at rtf 1, where events are rare.
- P3 (event tier flat): per-event wall cost from the settle throughput stays within 2× from
  N = 12 to N = 1.2×10⁵ (no hidden superlinearity in the law's own path). If per-event grows
  with N, the ceiling is the event tier instead and the finding inverts.
- P4 (digest): `digest` at a settled cut is Θ(N) and ≥ 10 ms at N = 1.2×10⁵ — unusable per frame,
  fine per settle.
- P5 (threads): 8 threads do not shrink the fixed tier (it is serial), only the event tier.

Kill criteria for my own reading: if the empty frame is flat in N (no rekey/drain cost at these N),
the "unbudgeted fixed tier" premise is wrong and the run reports that.
