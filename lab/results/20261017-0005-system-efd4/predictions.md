# Predictions (written before the run)

Cases not tuned on; what I expect, and what refutes what.

## P1 — The formation (512 co-orbital ships, one exact key)
- Standing entries ≈ 514 (512 ships + planet + star's relative orbit), distinct keys ≤ 3.
- The duplicate fraction (standing − distinct)/standing ≈ 0.996. If distinct keys come out ≫ 8,
  the claim "one orbit, one compiled cycle" is wrong at the quantizer and the intern is dead —
  that refutes the whole dossier.

## P2 — The scatter (512 distinct orbits): null control
- Standing ≈ distinct ≈ 514. No gain from interning; creation time per ship within ~2× of the
  formation's (both compile every orbit once). If the scatter builds markedly slower per ship,
  creation cost is orbit-shape-driven, not duplication-driven, and the "compile price" reading is wrong.

## P3 — Creation price
- Creation wall time per ship (both scenes) 10–100 µs (the compile dominates per b063's 84–89%
  re-fit share of kick cost; add_body's measured 9.2 µs c4d3 is the non-compiling path). If it is
  ~9 µs, the compile is already amortized in creation and the CPU side of the intern is negligible.

## P4 — The belt (plane_extra, 2000 ladder ships)
- Standing ≈ live ≈ 2060+ after the flight; distinct ≈ live (each ship its own exact orbit);
  duplication ≈ 0. Prediction: the intern does NOT move the belt's standing stock; only eviction
  (a cache bound) does. If duplication > 5% there, the ladder draws collide at Q48 and the belt
  claim understates the intern.

## P5 — Churn
- Over the flight, kicks on the formation rebind some ships; standing grows by ≈ the number of
  rebound bindings that keep a retired entry referenced... actually retire releases the old slot,
  so standing stays ≈ live + churn residue. If standing grows ≫ live during the flight, the churn
  leak (e4cc) reproduces here and the intern+eviction framing gains a second measured instance.

## What would kill the simplification
- Any reader that goes through `Catalogue::get` (none found by grep; if the checker finds one,
  sharing still cannot change bits, but the "nobody queries it" sentence dies).
- distinct keys ≫ standing/duplication on the formation (P1's refutation).
- A digest difference between a shared-entry build and the shipped one (not tested here — the
  digest leaves slot ids out by ties.rs's frozen comment; the checker should re-derive by patching
  if it doubts it).

## Honesty notes
- The kick-CPU half of the memo idea is already dead on shipped code (memo.rs: exact keys never
  recur on distinct kicks; hit < 5%). This run does not re-test it; the dossier adopts that kill.
- Cloud timings are Linux/x86 orders of magnitude only.
