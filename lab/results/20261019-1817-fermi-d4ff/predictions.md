# Predictions (pre-registered before the decisive computation)

Question: the 10⁹ ledger's stream row (91–97% of the composed CPU budget,
budget-1e9/3aec) counts only the clock cadence λ on an inert belt. Once every
body is real, the belt's own interaction stream (encounters at 2¹⁰·(r_i+r_j),
contacts at r_i+r_j) adds a term nobody has priced. I derive it from shipped
constants (scenario.rs genesis, exact integer lanes ported; encounter.rs
reaches; world.rs units) by 2D kinetic theory on the exact genesis
distribution, then fold it into the ledger.

My head-Fermi before running anything: ships are r_s = 34·2⁻¹⁰ root units
(49 m); belt annulus 2–3 AU, area ≈ 5π AU²; σ_e = 0.07 ⇒ ⟨|Δv|⟩ of order
e·v_circ ≈ 0.1·19 km/s ≈ 2 km/s; n at 10⁹ ≈ 6×10⁻⁹ root⁻².

- **P1 (the velocity scale):** mean relative speed ⟨|Δv|⟩ between two random
  belt members at random epochs, computed on the exact shipped genesis, lands
  in **1.5–4.0 km/s**.
- **P2 (held-out cross-check, not fitted):** f80a's published census digits
  (8.03 bindings/body at 174k game-s on the 3×10⁴ OFF arm) imply an effective
  belt binding rate 4.61×10⁻⁵/body/game-s; I predict it lands within
  **1.1–1.5×** of 0659's clock cadence λ = 3.55×10⁻⁵ (the excess is the onset
  wave plus locals, and cannot be below λ).
- **P3 (the missing row):** at 10⁹ in the shipped annulus, the encounter
  stream (pairs within 2¹⁰·(r_i+r_j) ≈ 100 km) is **1–10%** of the clock
  stream; the contact stream is **2×10⁻⁵–2×10⁻⁴** of it (0.3–5 contacts per
  game-second universe-wide at 10⁹).
- **P4 (wake-up rung):** the belt's contact channel reaches ≥ 1 contact per
  game-hour at **N between 3×10⁶ and 5×10⁷** (rate ∝ N² at fixed geometry);
  below 10⁶ no belt-belt contact can occur in any playable window.
- **P5 (the concentration threshold):** the encounter stream of a formation
  equals its own members' clock stream at concentration C* = n_local/n_belt
  between **20 and 80** (independent of fleet size), so a 10⁶-ship fleet must
  occupy more than ~a-few-thousand-km scale not to double its event budget.
- **P6 (lane non-event):** the a-grid's quantization (2⁻⁸ root unit ⇒
  2.6×10¹⁰ lanes) puts < 10⁻⁶ of all pairs on the same lane at 10⁹, and
  same-lane pairs have time-invariant separation (equal periods), so lane
  quantization contributes no stream.
- **P7 (ledger fold):** the added rows shift the composed 10⁹ totals
  (shipped 193 cores; split8+survival 39.3) by **< 0.5 cores** even priced at
  the full 82.5 µs/item fired cost — the closure sentence survives the belt's
  own physics in the shipped geometry.

Kill criteria: if P1 or P3 land outside their bands, my kinetic model or the
constant extraction is wrong — diagnose before claiming anything. If P7
fails (> 0.5 cores), the premise "closure survives" is wrong and the dossier
says so.
