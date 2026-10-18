# Predictions (written before the decisive run)

Question: what does the u64 port of `dioph::first_hit` (shipped u128) cost/save on the
e87d-class belt arms, and is it sound there ("all section values < 2⁶³", encounters od 1)?

Cases not tuned on: the a-window 1e-5 arm (I tune nothing; both arms are fresh), and the
per-call depth law across arms.

1. **Soundness:** every tuple on both arms and both seeds has pi, c0, d, w < 2⁶³ (pi is a
   period in ticks ≈ 1.4e11 < 2³⁸ at a ≈ 3 AU, so far under), and the u64 port returns the
   identical k and identical step count to the shipped u128 on every tuple (0 mismatches).
2. **Depth:** steps p50 in 15–45, max < 90 (Euclid depth ~ log_φ(pi) ≈ 55 at pi ≈ 2³⁷–2³⁸);
   the depth distribution is window-independent: p50 within 10% between the 1e-4 and 1e-5
   arms (depth is set by the continued fraction of d/pi, not by w).
3. **Price:** shipped u128 p50 300–1,200 ns/call (u128 division is a `__udivti3` call,
   ~2–4 divisions per recursion level); u64 port p50 60–250 ns/call (native 64-bit div,
   ~25–40 cycles); win 3–8×.
4. **The row:** first_hit is a large share of e87d's composed 416 ns/pair/kick cached-section
   proposal (my guess 40–80%); with a 3–8× win on that share the 105-core row moves to
   ~30–70 cores.
5. **Failure modes that would falsify the port's value:** if the u64 win is < 2× (LLVM
   already lowers the u128 ops cheaply at these magnitudes — then the port is not worth a
   law-adjacent change), or if any tuple ≥ 2⁶³ appears (the port is unsound on this class),
   or if depth scales with the window (my depth law is wrong).
