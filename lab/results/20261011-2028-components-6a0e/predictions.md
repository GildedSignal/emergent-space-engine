# Predictions (written before the decisive runs; tuned only on n=100k smoke)

Tuned on: n=100k, all three loads, seeds 1–3 (heap 172–182 ns/event belt, wheel 54–60; uniform
93 vs 32; identity true everywhere; late sorts ≈ 3 per 200k pops).

Held out: n=1M and n=4M in full (both loads and seeds), and everything about trends with n.

1. **Speedup grows with n** (heap pays log₄(n) cache-line touches per pop+re-set and the
   arrays leave cache; wheel pays a constant count of random touches): ≥ 4.0× at n=1M and
   ≥ 5.0× at n=4M on belt (median seed).
2. **Heap cost grows, wheel cost stays flat**: heap median ns/event at 4M ≥ 1.5× its value at
   100k; wheel at 4M ≤ 1.3× its value at 100k.
3. **Exactness holds**: pop_streams_identical = true for every config (the frozen tie rule
   (tick, slot) is reproduced by the wheel's per-tick slot sort).
4. **Tails**: heap p99/median ratio at 4M exceeds the wheel's (deep sifts vs flat bucket ops).
5. **Uniform stays the weakest win** at every size (densest keys → shallowest effective sift).
6. **Floor distance**: the wheel stays ≥ 20× above the FIFO instrument (0.3 ns/event at 100k);
   its residual cost is the indexed peek/clear/set random accesses (~4–6 lines), not the
   calendar structure. So the wheel is not within 10× of the sequential floor at any size —
   the remaining gap is a representation question (validation bits packed with the key), not
   an algorithmic one.

What would make the component claim wrong: if the wheel's advantage vanished at 4M (pointer
chasing catching up with sift depth), or if any pop stream diverged, or if late_sorts grew
with n (a systematic invariant break, not rarity).
