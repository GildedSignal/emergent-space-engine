# Predictions (written before the decisive computation and the anchor flight)

Held-out cases: everything below is stated before `legality.py` (the exact arithmetic from
shipped source constants) and before any flight on this tree.

## P1 — the anchor flight (shipped code, this tree)

`nladder 1000 coast 20` (seed 1, the ladder's own): the locals' storm stands, N-flat:
- max events/frame in [300, 460] (ladder.txt's merged-tree band 348–452; today's tree adds the
  recorder and range merges, counts are seed-deterministic);
- p99 events/frame in [190, 260]; p50 in [1, 6].
At N = 10⁴ (if flown): the same max within ±20% (the comb is N-independent above N = 600).

## P2 — the metronome identity (source arithmetic, `legality.py`)

The belt's measured stream (3.55–4.62×10⁻⁵ events/body/game-s, gold 20261008-2113-a9d7 and
7da3) is the same metronome as the locals' comb: 2^(step_log2) kicks per period P_D of the
doll's shortest secondary. Predicted: 128/P_Cinder computed from shipped constants lands
within 2× of the measured fired-kick rate (my hand estimate: Cinder P ≈ 89 d from
`periapsis 35_600_000`, e = 1/10; the flight-measured P_D is 77.24 d, cf45 — the exact
factor f'(c) of the Δs law absorbs the rest).

## P3 — r9's secular bound on the shipped populations (the decisive case)

R_H(Home) = a_Home·(2⁻¹⁸/3)^(1/3) ≈ 1.1×10⁶ root units (a_Home ≈ 1.013×10⁸). Predicted:
- in-situ locals (a uniform over 5 octaves in [5,200, 166,400) root units): ≥ 90% have
  τ = (a/R_H)³ under r9's τ₀ = 3.6×10⁻³ (a < 0.153 R_H); the median sits ≥ 50× under;
- the L4/L5 quarter (a ≈ 260,000·(1±3%) root units, the Moon's): τ ≈ 4× OVER τ₀
  (a ≈ 0.25 R_H) — resonant, exactly the class law.md's own kick rule excludes from averaging;
- the quiet belt (2–3 AU, root doll): τ under the Giant's tide ≈ 4×10⁻⁵, ~90× UNDER τ₀;
  under Home's tide ≈ 2×10⁻⁵ — secular-legal.

Adversarial variants (not tuned on): if Home's mass were 2⁻¹⁹ (one octave lighter), the
in-situ inside-fraction drops below ~60% (the top two octaves cross the bound); at 2⁻¹⁷ it
rises to ~100%.

## P4 — the wall ladder (composition from measured constants)

- Shipped letter N (12-ms frame, rtf 100, storm 334 events ≈ 9.8 ms at the M1's 29.3 µs/event):
  N ≈ 4–10×10⁵ (7da3's checker said ≈ 6×10⁵).
- Every cure arm (de-phase 334→53, translate 335→141, hybrid delete ~120) pushes the letter
  past the post-wave memory wall: 6–8 GB ÷ 4.85–5.06 kB/body ≈ 1.2–1.6×10⁶ bodies. All arms
  tie at memory; none exceeds it by more than 3×.
- 10⁹ neutrality: the comb is 300 bodies ≈ 4–8 ev/game-s against a 10⁹ stream of
  3.6–4.6×10⁴ ev/game-s: every cure's total event delta at 10⁹ ≤ 10⁻⁴ of the stream. No comb
  decision can move the 10⁹ CPU ledger. The delete lever alone also touches the stream's own
  constant (it is the same metronome, P2).
