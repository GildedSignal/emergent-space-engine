# Predictions (written after the sizes pilot, before the micro/wave arms)

Cases I have NOT tuned on (the e-ladder timings and the wave come after this file):

1. **Read (`signed_state`) hot vs cold.** Hot will land at the record's 2.5–9 µs
   (b8fc/6701: 4.0–5.4 µs at planet-like keys). The cold delta (evictor between
   calls) will be **under 20% of the hot read** at every e, including the held-out
   deepest-search case e=0.99 (124 knots): the read is compute (bracket+Newton over
   ~3 panels), and the search over ≤124×88 B records is ≤7 dependent probes.
   KILL my premise if any key's cold delta ≥ 50% of its hot read (then the read is
   latency-bound and every timing in the record is cache-flattered at scale).
2. **Compile hot vs cold.** Delta ≤ 5% of the hot compile at every e: the input is a
   200 B key; the output is fresh writes (write-allocate traffic ≈ 2× 24 KB ≈ 5 µs
   at this box's ~10 GB/s vs a 70–110 µs compute). KILL if delta ≥ 15%.
3. **Wave (N=3000 and held-out N=10000).** Per fired kick: 15–35 KB of allocation
   traffic (≈2.2× the table from Vec growth + the per-event Vec<Secondary> churn),
   flat in N (per-event bill is N-independent). The wave's alloc bandwidth at N=3000
   stays under 0.5 GB/s on this box.
4. **Roofline.** With ~2×10⁴ B/event and the ladder's measured kick rates, the event
   stream at 10⁶ live bodies needs < 15 GB/s — under the M1's ~68 GB/s roof and the
   ~4-core compute wall hits first at ~10⁵ live bodies regardless. So the event path
   is **compute-bound at every N the plane can hold; the memory wall at scale is
   capacity (bytes stored per live body), not bandwidth (bytes moved per event)**.
   KILL if measured bytes/kick × the 10⁶-rung kick rate ≥ 68 GB/s.

Controls: the evictor-only loop is timed in the same shape and subtracted; arms are
interleaved 5× (hot batch, cold batch) per key; the stream pass calibrates the box's
bandwidth so the delta→bytes conversion is measured, not assumed.
