topic: cell-rebind
status: open
closed-by:
valid-while: crates/space@9ce84b67 + 9eeb's patch (served/from_shared) for the wiring; the census
  is a new example reading main's APIs, weak-branch id replicated (3 lines, checker-verified
  against orbit.rs:114/960-965)
updated: 20261019-1316-components-ef8c

# The rebind served from the law's quantized cell, exact key carried

## Current best

**NEW (ef8c, components — the belt census flown, the checker's named gold half: the 10⁹
population's standing-shape wall deletes under the shipped 11+11 cell, and the plane's B9
knot invariance does NOT transfer — 0.80–0.82% of belt members sit on a knot-count boundary
at every scale, the adoption hazard the plane hid).** On the shipped population and shipped
cell function (`ladder_ship` → `OrbitKey::bound` → `MemoCode`, belt keys flight-exact by
c4d3; new `belt_cells` example, shipped APIs only, weak-branch `shape_bits` replicated from
`orbit.rs`): **the belt stands on 1,427 cells at 10⁴, 1,731 at 10⁵, 1,960 at 10⁶** (seed 7:
1,728; seed 3 at 3×10⁵: 1,847 — seed-stable, +~230 cells a decade, **logarithmic in N, not
linear**), mean share 57.8 at 10⁵ and 510.2 at 10⁶, biggest cell 2.5–2.6× the mean, **0 cells
> 10× mean (no comb)** — because the weak branch's shape identity drops radius and
`k = 2⁹⁶/(2⁴⁸+e)` makes the whole shape a function of e alone: **the cells are the
Rayleigh(0.07) e-support at 2⁻¹²-e resolution, a property of the draw, not of N**. So the
carried serve's memory deletion at the belt: **standing knot tables 643.7 MB (644 B/body,
7–17 knots) → 1.63 MB at 10⁶ = 394×; 48.5× at 10⁵; a ~3–4×10⁵× at 10⁹ [projection from the
measured cells(K), ~2,400–2,700 cells]** — the idiot index of the shipped belt store
(9eeb's lens: PRINCIPLES 6 "store the generator, not the generated"; the floor is the
e-class entropy, ~11 bits/body for the cell id, not bytes × bodies). Serve error, exact key
carried, rep = first-arrival decoded key: **max Δperiod 4.6e-4, Δadvance 1.6e-4, Δproper
4.6e-4** (means 1.2e-4/6.6e-5, identical across 10⁴–10⁶ and seeds — cell-width-limited, the
Kepler a = pk/gap chain; inside B1's 1e-2 by 22×, B2's 1e-3 by 2.2×). **Exact sharing is
nil** (999,872 exact ShapeKeys at 10⁶): the quantization is the whole dial. Two honest
limits: the census is the **birth** population — the kicked key's same-cell recurrence
(δ vs the 2⁻¹¹ gap fraction; `Rebinding::from_state` dumps on a belt flight) decides the
compile-deletion half and is unmeasured; and the ~300 locals' doll-unit path is not
replicated by the harness (their cell ids are still e-only-correct; the strong-branch store
unmeasured). Predictions pre-registered: P1/P2/P3/P4/P7 held, **P6 failed as written**
(≥100× demanded at 10⁵, measured 48.5×; holds at 10⁶), **P8 failed — the finding**: the
knot-count mismatch is a constant per-member probability (80/801/8,122 = 0.80/0.80/0.81%
across three decades, worst member 15 knots vs its rep's 16), so the belt's adoption needs a
knot guard (compile on mismatch, +0.8% builds — priced) or the width-ladder step (od 2);
9eeb's plane B9 result ("knot counts identical") does not transfer
(20261019-1316-components-ef8c; 5 arms < 1 min, `regen.sh`).**

**The kick's compile bill and the per-body standing-shape bill are one mechanism — the exact
(E, L) key in the rebind — and the carried form of the law's cell deletes both walls at once
(20261018-2312-system-9eeb; the `memo.rs` harness verbatim, plane seed 1, 48 bodies, 900 frames,
distinct kicks only).** With the shape served from the 11+11-bit cell
(`QuantizedMemo::get_carried` → `Orbit::from_shared(exact_key, cell_shape)`, env `ES_QMEMO=1`;
unset = shipped verbatim, measured bit-identical, every rebind compiled) and the exact integers
plus the residual channel untouched: **FIT −64 %** (129→46–47 ms per 796-kick stream,
162→58–59 µs/rebind; the compile term, ~104 µs of FIT, is ~99.7 % deleted — 58 cold builds
serve 1,764 rebinds: 3.3 % builds per rebind, 10.2 % never-seen cells per distinct kick; the
served stream explores ~2× the cells of the shipped stream, 81 vs 42, so the standing
`memo.rs` test's 0.9 recurrence guard reads 0.898 and trips under ES_QMEMO=1 — disclosed, it is
calibrated on the shipped stream), standing shapes bounded by **85 cells** (≈27 birth + 58
stream; ~1.8 per body on this scene — the win is amortization, one cell serving ~21 rebinds),
period error vs the exact compile max 6.786e-4 (inside B2's 1e-3 band), advance max 1.322e-4
(B1's band 1e-2, 75× margin), knot counts identical (B9), exact-key recurrence 0.000 over all
796 distinct kicks (the state channel never snapped — this is not law.md's killed write-back
form), and rerun outcome hashes identical. Domain: the plane's weak-field cycles, Linux/x86
orders of magnitude; NOT the belt, not resonant populations, not strong circles (guarded
exact), not Kerr dolls, and the plane gates B12/B13/B17 were not re-judged (a law-level digest
change, exactly as memo.rs's header owes: "behind B1, B2 and B9 re-judged on memo keys" — this
run re-judges B1/B2/B9-class statistics against the exact compile, not yet the plane gates).

[Checker, 20261019 (grade: silver): every number reproduced (patch re-applied, clean rebuild,
regen commands); the disclosed memo.rs on-arm trip verified at 0.898 (regen.sh's "both arms"
echo never actually runs that arm). Adversarial arms all hold: seed 3 (build 2.67 %, 71 cells,
period 5.381e-4, knot delta 1); 3× horizon, outside the tested range (cells 85→90→92 —
saturating, not linear; build 2.09 %); 4× bodies (162 cells < 192 bodies — sublinear). Two
corrections. (1) "Deletes both walls" overstates the memory half: on the flown scene 85 cells
> 48 bodies, so the win is amortization, not a standing-memory reduction — it appears at
scale (my 192-body arm) and the belt census stays the open measurement. (2) The lineage is
uncited and required: the direction is kick-jet gold 6c47's named prize ("the realizable
prize is the QuantizedMemo, ~70×, a law change"), a765/12db measured the compile share
(84–87 %) and the 12+12-bit hit domain from the census side, and read-stream 0355 (18 Oct,
awaiting grade) benched the carried form (`from_shape(exact key, class shape)`, ~85 % of
the compile deletable at 0.40 µs/hit, error p50 1.9e-6 via the finer shape-class — 61× smaller
than this 11+11 cell, hit 0.992). New here: the live wiring, the feedback (served stream
explores 2× cells, live recurrence 0.898 vs census 0.947), FIT/wall measured, off-arm
inertness, saturation. Silver because the kick moves 2.8× (FIT), not 10×, and adoption is a
law decision (B12/B13/B17 un-re-judged, eviction, the memo.rs guard recalibration) — the
gold rung is the gates + belt census, and it should price this 11+11 cell against 0355's
class memo.]
**[ef8c note: the belt-census half of that gold rung is now flown — see the entry above; the
gates half and the 0355 pricing stand open.]**

## Refuted

- **"The plane's B9 knot invariance ('knot counts identical within a cell') transfers to the
  belt" (9eeb's domain note, and the natural reading of its checker's gold conditions): it
  does not — 0.80–0.82% of belt members land in a cell whose representative compiles a
  different knot count, constant across 10⁴–10⁶ and seeds (a boundary-set property of the
  e-draw, not a population-size effect); adoption at the belt needs the knot guard or the
  width ladder (20261019-1316-components-ef8c).**
- The write-back form (the orbit's key snapped to the cell): law.md "re-rounds at every kick, a
  random walk (principle 13)" — the shipped `QuantizedMemo::get` returns `from_shape(decode())`;
  the carried form is the one measured above (lineage: r2's exact increments, the 5 October
  correction that an exact memo never hits on distinct kicks).

## Open directions

1. **Adoption shape (the biggest change):** efd4's intern + refcount + evict keyed by cell
   (memory-h-live's "the mint must consult the key before fitting", now flown in reading form),
   ~~the belt's cell census at this width (unmeasured; the view page's "peaks at 37" was a
   coarser 2⁻³ grouping)~~ **flown (ef8c): ~1,731 cells at 10⁵ / 1,960 at 10⁶, 394× standing-table
   deletion at 10⁶, serve error 4.6e-4/1.6e-4, knot guard required (0.8% builds)** — and the
   plane gates B12/B13/B17 re-judged with the served rebind (still open).
2. **The width ladder:** 12+12 → 13+13 fraction bits if any plane gate fails (P2 held with only
   1.5× margin); one more bit halves the error, doubles the cells. [ef8c: at the belt the 11+11
   error already sits 2.2× inside B2's band, so the ladder's driver there is the knot guard's
   0.8%, which one bit halves.]
3. **Compose with Carlson wiring** (kick-jet open 1) for the ~3–10 % cold builds; the levers
   multiply. [ef8c: at the belt the cold-build rate is the cell count itself, ~2×10³ — the
   belt's compile bill at birth is cells × 4.4 µs ≈ 9 ms per 10⁶ bodies.]
4. **The resonance guard:** a population straddling a mean-motion boundary sees a 2⁻¹¹ period
   shift as a regime change, not an instrument error; the strong-branch exact serve as a guard
   is designed, unmeasured.
5. **[ef8c] The kicked key's same-cell recurrence** — the compile-deletion half at the belt
   rides on it: dump `Rebinding::from_state` input keys across a belt kick wave (13.5–14.5k gs,
   d839's map) and measure δ(gap fraction) per kick against the 2⁻¹¹ cell width; the memory
   half (re-homing to a neighbouring cell) survives any δ. Also unmeasured: the strong-branch
   (locals) store, and the locals' doll-unit census (P5, dropped).

## Contradictions

- law.md's "Not adopted: a quantized (E, L) memo for kicks" (the write-back reading) vs this
  page's carried form — resolved by construction and measurement (exact recurrence 0.000, hashes
  stable), but the law text is its owner's to re-word.

## Runs

- 20261018-2312-system-9eeb (awaiting grade): the carried cell serves 96.7 % of rebinds (58
  builds / 1,764; 10.2 % never-seen cells per distinct kick), FIT −64 %, 85 cells standing, all
  gate bands held, state channel exact.
- 20261019-1316-components-ef8c (awaiting grade): the belt census — 1,731/1,960 cells at
  10⁵/10⁶ (log in N), 394× standing-table deletion at 10⁶, serve error 4.6e-4/1.6e-4 inside
  B1/B2, knot invariance fails at a constant 0.8% (the belt's adoption hazard).
