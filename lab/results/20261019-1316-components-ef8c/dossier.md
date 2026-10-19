# Dossier — the belt's cell census at the shipped 11+11 width

**Claim.** The 10⁹ population's standing-shape wall deletes under the shipped 11+11 cell: the
ladder belt stands on ~1,731–1,960 cells at 10⁵–10⁶ bodies (seed-stable, +230 cells a decade),
so serving the compiled shape from the cell (9eeb's carried form) deletes the belt's per-body
knot tables by 48.5× at 10⁵ and 394× at 10⁶ — 644 MB → 1.6 MB of standing tables at 10⁶, a
projected ~3–4×10⁵× at 10⁹ — with the serve's period error max 4.6e-4 / advance 1.6e-4 (inside
B1's 1e-2 and B2's 1e-3 bands), **but the cell is not knot-invariant at the belt: 0.80–0.82% of
members sit on a knot-count boundary at every scale** (the plane's B9 "knot counts identical"
does not transfer), so adoption needs a knot guard (compile on mismatch: 0.8% builds) or a
width-ladder step.

**Bottleneck.** Board item "memory at 10⁹" and the cell-rebind topic's gold rung (9eeb's
checker: "the belt census stays the open measurement"). The per-body compiled orbit is the
scoreboard's named term ("most of it the body's own compiled orbit"); PRINCIPLES 6 "Store the
generator, not the generated" — the knot table is the generated, the quantized-e class is the
generator. Idiot index of the shipped belt store at 10⁶: 644 B/body standing knots against a
floor of ~(cell id ≈ 11 bits + exact key the body carries anyway) + 1.6 MB of shared tables ≈
~400×; at 10⁹ ≈ 3–4×10⁵× [projection from the measured cells(K) growth]. This is the largest
measured idiot index in the record (the kick's is 10–12×, a765).

**Evidence.** All numbers from `lab/results/20261019-1316-components-ef8c/` (grid in
`belt_cells_grid.txt`, regenerable in <1 min):

| arm | cells | exact shapes | mean share | delete | max ΔP | max Δadv | knot≠ |
|---|---|---|---|---|---|---|---|
| 10⁴ seed 1 | 1,427 | 10,000 | 7.0 | 6.4× | 3.6e-4 | 1.5e-4 | 80 (0.80%) |
| 10⁵ seed 1 | 1,731 | 99,997 | 57.8 | 48.5× | 4.2e-4 | 1.6e-4 | 801 (0.80%) |
| 10⁵ seed 7 (held out) | 1,728 | 99,999 | 57.9 | 48.5× | 4.3e-4 | 1.6e-4 | 823 (0.82%) |
| 3×10⁵ seed 3 (held out) | 1,847 | 299,991 | 162.4 | 130.7× | 4.3e-4 | 1.5e-4 | 2,462 (0.82%) |
| 10⁶ seed 1 | 1,960 | 999,872 | 510.2 | 394× | 4.6e-4 | 1.6e-4 | 8,122 (0.81%) |

- Standing tables: 643.7 MB (644 B/body, 7–17 knots) → 1.63 MB at 10⁶; 10⁹ projection ≈
  644 GB → ~2–3 MB at ~2,400–2,700 cells [INFERENCE: cells grow +230/decade, 1,427→1,731→1,960].
- Mechanism, read off the shipped code (`orbit.rs`): the weak branch's shape identity drops
  radius (`shape_bits` = `(1<<44) | low 17 bits`), and `k = 2⁹⁶/(2⁴⁸+e)` makes the whole shape a
  function of e alone — so **every belt body with the same quantized eccentricity shares one
  shape table regardless of semi-major axis**. The cells are the Rayleigh(0.07) e-support at
  2⁻¹²-e resolution (~600 in the bulk, ~1,700–1,960 with tail), not a function of N.
- No comb: biggest cell 2.5–2.6× the mean at every scale; 0 cells > 10× mean (P7).
- Serve error is cell-width-limited, not N-limited: mean ΔP = 1.198–1.200e-4 identical across
  10⁴–10⁶ and seeds; max 4.6e-4 (d ln P = −3/2 d ln gap, the Kepler a = pk/gap chain).
- Exact sharing is nil (P4): 999,872 exact ShapeKeys at 10⁶ — sharing exists only through the
  11+11 quantization, so the width ladder is the only dial.

Commands (each ≤ 60 s; from the repo root, patch applied — `regen.sh` does all of it):
```
cargo run --release -p emergent-universe --example belt_cells -- 1 10000   # …and 100000, 1000000; seed 7 / 3 arms
```
The example is new (`crates/universe/examples/belt_cells.rs`); it reads only shipped APIs
(`ladder_ship`, `OrbitKey::bound`, `MemoCode::encode/decode`, `Orbit::compile`) and replicates
the private `shape_bits` weak-branch rule (3 lines, cited). Belt keys are flight-exact by
c4d3's bit-identity (doll-0 unit ONE); the ~300 locals are included in the population but
their doll-unit path was NOT replicated — they are ≤0.03% of the 10⁶ grid and their (wrong-p)
keys still land in correct cells because the weak-branch cell id depends only on e.

**Predictions** (`predictions.md`, written before the grid): P1 cells < 3,000 at 10⁵ ✓ (1,731);
P2 cells(10⁶)/cells(10⁵) < 1.5 ✓ (1.13); P3 max ΔP ≤ 2⁻¹⁰ ✓ (4.6e-4), Δadv ✓ (1.6e-4); P4
exact ≈ N ✓; P6 delete ≥ 100× at 10⁵ **✗ as written** (48.5×; it holds at 10⁶, 394×); P7 no
comb ✓; P8 knot_mismatch = 0 **✗ — the run's own finding**: 0.80–0.82% at every scale, constant
in K and seed, i.e. a per-member boundary probability (the worst member: 15 knots vs its rep's
16). P5 (locals contrast) dropped: the home doll's unit conversion is not replicated by the
harness; unmeasured, not claimed.

**What would make it wrong.** (1) The kicked belt: this is the birth population; a kick moves
the key by δ, and if δ typically exceeds the 2⁻¹¹ gap fraction the kicked body leaves its cell
and the compile-deletion half dies (the memory half survives: the body re-homes to a
neighbouring existing cell, tables stay O(cells)). The same-cell recurrence after a real kick —
`Rebinding::from_state` key dumps on a belt flight — is the named next measurement. (2) The
0.8% knot mismatch: if B9 re-judged on the belt rejects a served table with a different knot
count, adoption needs the guard (compile on mismatch, +0.8% builds) — priced here, not flown.
(3) The serve error is measured on period/advance/proper period only; crossing times inside
the table were not re-judged against B1/B2/B13-class gates (9eeb's own open item).
**Cost of adoption:** 9eeb's `get_carried` wiring already exists as a patch (FIT −64% on the
plane); this census adds its belt leg and one new requirement — the knot guard. **Fit:**
PRINCIPLES 6 "Store the generator, not the generated"; 33 "a raindrop is an event for an ant
and nothing for a lion" — the shape store resolves only what the cell resolves; 24 "The memory
floor is information" — the floor here is the e-class entropy (~11 bits), not bytes × bodies.

**The lens (first principles, one component).** Component: the standing-shape store. Floor:
the population's distinct quantized-orbit count — ~2×10³ cells for any belt ≥10⁵ (information
of the e-distribution at the law's own 2⁻¹¹ quantization), plus ~11 bits/body for the cell id.
Shipped: 644 B/body (birth). Idiot index ~400× at 10⁶, ~3–4×10⁵× at 10⁹. Design within 10× of
the floor: 9eeb's carried serve measured here at 394× (10⁶) — the store, not the census, is the
remaining gap. **Blind spot checked:** the neighbour component (the exact-key/residual channel)
is untouched — the deletion moves nothing onto it, but the kicked-key recurrence (above) is
where a local optimum could hide; the locals/strong-branch store was not measured.
