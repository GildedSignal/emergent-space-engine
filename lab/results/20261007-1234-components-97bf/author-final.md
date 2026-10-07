Working...
Run complete. Dossier at `lab/results/20261007-1234-components-97bf/dossier.md`, predictions pre-registered, all numbers regenerable by the commands inside.

**Claim:** because event times are canonical integer ticks, the engine's event calendar needs no comparison structure — a bitmapped base-2 timing wheel with one 24-byte packet per body delivers the bit-identical (tick, id) delivery stream at 2.2–4.5× lower cost than the shipped indexed 4-ary heap (4,243 → 946 ns/op at 16.7 M bodies) with a flat tail (p999/p50 2.1 vs 6.3), sitting ~3.5× above the measured two-line memory floor where the heap sits ~16×, its cost being cache lines per event rather than algorithm — adoptable as a ~150-line drop-in for `lattice-event`'s `Calendar` with determinism unchanged.
