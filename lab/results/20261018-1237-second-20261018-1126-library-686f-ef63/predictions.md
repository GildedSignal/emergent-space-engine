# Predictions (written before the corrected composition runs)

Second author on 20261018-1126-library-686f. The checker's named experiment: fix
compose_rung.py's re-kick line to (N/T*)×rtf with T*(10⁹) = k*/cadence from e29c's own
frozen bars, regenerate, and rewrite the add-back paragraph and page clause. This file is
written before `compose_rung.py` (the corrected copy) is executed; the hand arithmetic
below is mine, the script is the decisive instrument.

Ground truth I verified by hand before predicting (not from the checker's abstract alone):
- ladder.txt:143 carries the conversion: "357 kicks a game-second = 36,000 a wall second
  at rtf 100" — a per-game-second rate × 100 gives per-wall-second. The original script
  divided by rtf: an rtf² = 10⁴ error, direction confirmed.
- e29c (gold, 20261017-2142) frozen bars: T*(q_view) = 5.99×10⁷ / 3.37×10⁷ / 5.99×10⁶ gs
  at 10⁵/10⁶/10⁹; k* = 213 carried kicks at cadence 3.55×10⁻⁵ ev/(body·gs); identity
  cadence×T*(10⁹) = 3.55×10⁻⁵ × 5.99×10⁶ = 212.6 ≈ 213 ✓.
- e29c's 0.6 is a COST ratio (bars.py: REKICK_COST = 0.6, "f5bd: 0.51–0.6×" of one kick),
  not a firing-rate factor: re-kick share of the deleted stream = 0.6/(T*×cadence).

- P1 (T* law): e29c's three bars fit T* ∝ N^(−1/4) within 0.2% each (derived: q_view ∝
  N^(−1/2) at uniform belt density — e29c's own bars.py; drift ~ t² — f5bd's fence; so
  T* ∝ q_view^(1/2) ∝ N^(−1/4)). The fit's two independent ratios: 10^(1/4) = 1.7783 vs
  5.99×10⁷/3.37×10⁷ = 1.7774 (+0.05%); 1000^(1/4) = 5.6234 vs 3.37×10⁷/5.99×10⁶ = 5.6260
  (−0.05%). If either deviated > 2% I would not interpolate and would report bar-anchored
  bounds instead; prediction: both pass, so T*(N) = 5.99×10⁶·(N/10⁹)^(−1/4) is used.
- P2 (the named fix, 10⁹ lazy+RES): the corrected add-back is 0.547 s/s on e29c's 10⁹ bar
  (N_del = 9.944×10⁸ carried bodies / T* = 5.99×10⁶ gs × rtf 100 × 33 µs = 0.547), and
  0.097 s/s on the original's stale constant (T* frozen at the 10⁶ bar, 3.37×10⁷ gs) — the
  checker's named pair 0.098/0.55. Via e29c's published ratio (0.6/(T*×cadence) = 0.28% of
  the deleted stream at kick 30–50.4 µs): 0.30–0.50 s/s. Every reading ≥ 8% of the 0.72
  budget; the fence reading 76%. The original's "< 10⁻⁴ s/s at every N" is dead at 10⁹ by
  3–4 orders, and its "wrong by 4 orders" dismissal of the 0.28% reading is retracted
  (that reading is a cost identity, correct within a factor 2).
- P3 (interpolated decades): T*(10⁷) = 1.894×10⁷ gs → add-back 1.73×10⁻³ s/s (0.24% of
  budget; immaterial — every 10⁷ ordering conclusion unchanged); T*(10⁸) = 1.066×10⁷ gs →
  0.031 s/s (0.6× kick-cost reading 0.019; 2.6–4.3% of budget).
- P4 (the skipped decade): lazy+RES at 10⁸ fails the wave 1.8–3.1× the window budget
  (spared 562,825 bodies × 34.45–59.6 µs vs 10.678 s in-window budget); the 10⁷ pass is
  rung-exact, crossover at N ≈ 3.2–5.5×10⁷. Live 2.85 GB (under the 8 GB machine, under
  the 4 GiB gate); birth 1.58 GB compact.
- P5 (record identity): the corrected script reproduces every non-re-kick column of the
  original six rows bit-identically (anchor 15.0 s; delete fractions 0.385/0.9944; budget
  10.7 s) — the fix touches only the re-kick block, adds the 10⁸ row, the crossover solve,
  the deleted-stream cross-check and the T*-law verification. Shipped rows now print re-kick
  0 by construction (no delete → nothing carried), not the buggy 9.8×10⁻⁵.
- P6 (memory walls named): the 10⁹ row's birth 15.75 GB and live 28.43 GB each exceed the
  8 GB machine — the claim sentence must name them alongside the wave and the stream; with
  the corrected add-back the one-thread total at 10⁹ is 0.94–1.57 s/s against 0.72.

Kill criterion: if the corrected script's non-re-kick columns drift from the original
record, or the checker's named numbers (0.098 / 0.55 / 1.8–3.1× / 3.2–5.5×10⁷) do not
regenerate, the fix is wrong, not the checker. If the T*-law fit fails, the interpolated
rows' add-back is reported as bounds only.
